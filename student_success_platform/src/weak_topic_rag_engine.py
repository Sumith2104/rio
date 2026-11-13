"""
=============================================================================
WEAK-TOPIC SYLLABUS RAG & REMEDIAL PLAN ENGINE
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
Identifies question/topic-level weaknesses in Internal Assessments (IA < 50%),
retrieves matching syllabus units & prerequisite DAG ancestors from ChromaDB,
and synthesizes a personalized, day-by-day remedial study plan with AWS AI.
=============================================================================
"""

import os
import sys
import time
import json
import uuid
import logging
from typing import Dict, Any, List, Optional

# Ensure src is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fluxbase_client import FluxbaseClient
from vector_db_manager import VectorDBManager
from prerequisite_graph import PrerequisiteKnowledgeGraph
from flux_ai_service import FluxAIService
from auth_service import AuthService
from hybrid_rag_service import HybridPrerequisiteRAG
from rag_guard_service import RAGFaithfulnessGuard

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class WeakTopicRAGEngine:
    """Detects weak IA topics, performs syllabus hybrid vector retrieval, and builds study plans."""

    def __init__(self):
        self.flux_db = FluxbaseClient()
        self.vdb = VectorDBManager(host="localhost", port=8001)
        self.flux_ai = FluxAIService()
        self.auth_service = AuthService()
        self.hybrid_rag = HybridPrerequisiteRAG()
        self.rag_guard = RAGFaithfulnessGuard()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        graph_json = os.path.join(base_dir, "data", "concept_prerequisites.json")
        self.pkg = PrerequisiteKnowledgeGraph(graph_json)

    def get_student_weak_topics(self, srn: str, course_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query question-level IA scores from PostgreSQL to find topics where student scored < 50%.
        """
        course_clause = f"AND course_id = '{course_id}'" if course_id else ""
        sql = f"""
        SELECT 
            score_id, student_srn, course_id, ia_number, question_no,
            topic_id, topic_title, marks_obtained, max_marks, score_percentage, is_weak
        FROM ia_question_scores
        WHERE student_srn = '{srn}' AND is_weak = TRUE {course_clause}
        ORDER BY score_percentage ASC;
        """
        res = self.flux_db.execute_query(sql)
        rows = res.get("rows", [])

        # If no explicit entries found in DB, provide fallback based on low marks in course_enrollments
        if not rows and course_id:
            check_enrollment_sql = f"SELECT ia1_score, ia2_score FROM course_enrollments WHERE srn = '{srn}' AND course_id = '{course_id}';"
            enr_res = self.flux_db.execute_query(check_enrollment_sql)
            enr = enr_res.get("rows", [{}])[0] if enr_res.get("rows") else {}
            if (enr.get("ia1_score") or 30) < 15.0:
                rows = [
                    {
                        "score_id": "FALLBACK_Q1",
                        "student_srn": srn,
                        "course_id": course_id,
                        "ia_number": 1,
                        "question_no": "Q1",
                        "topic_id": "MATH_CHAIN_RULE",
                        "topic_title": "Multivariable Calculus Chain Rule & Gradient Propagation",
                        "marks_obtained": 3.0,
                        "max_marks": 10.0,
                        "score_percentage": 30.0,
                        "is_weak": True
                    },
                    {
                        "score_id": "FALLBACK_Q2",
                        "student_srn": srn,
                        "course_id": course_id,
                        "ia_number": 1,
                        "question_no": "Q2",
                        "topic_id": "DL_BACKPROP",
                        "topic_title": "Backpropagation Algorithm & Reverse-Mode Autodiff",
                        "marks_obtained": 3.5,
                        "max_marks": 10.0,
                        "score_percentage": 35.0,
                        "is_weak": True
                    }
                ]

        return rows

    def retrieve_syllabus_context(self, course_id: str, topic_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Executes Top-Level Hybrid RAG (BM25 + ChromaDB Cosine + OKF DAG Ancestors + RRF)
        to retrieve authoritative lecture excerpts, primary formulas, and slide references.
        """
        citations = []
        for tid in topic_ids:
            hybrid_res = self.hybrid_rag.retrieve_hybrid_context(
                course_id=course_id,
                target_concept_id=tid,
                query_text=f"{tid} theoretical derivation, algorithm steps, and worked examples",
                include_prerequisites=True,
                top_k=2
            )

            target_cits = hybrid_res.get("target_retrieved_citations", [])
            primary_chunk = target_cits[0] if target_cits else {}
            
            # Format combined excerpt
            prereq_cits = hybrid_res.get("foundational_prerequisite_citations", [])
            prereq_names = [p["title"] for p in prereq_cits]
            
            target_concept_meta = hybrid_res.get("target_concept", {})
            slide_citation = primary_chunk.get("slide_ref") or target_concept_meta.get("slide_ref", f"Slide-{tid}")
            formula_citation = target_concept_meta.get("primary_formula", "")
            unit_name = primary_chunk.get("unit") or target_concept_meta.get("unit", "Curriculum Foundations")
            excerpt = primary_chunk.get("excerpt", f"Comprehensive academic curriculum coverage of {tid}.")

            citations.append({
                "topic_id": tid,
                "topic_name": target_concept_meta.get("name", tid),
                "unit": unit_name,
                "slide_citation": slide_citation,
                "primary_formula": formula_citation,
                "bloom_taxonomy": target_concept_meta.get("bloom_taxonomy", "Apply"),
                "syllabus_excerpt": excerpt,
                "prerequisite_ancestors": prereq_names,
                "foundational_prerequisite_slides": [
                    {
                        "concept_id": p["concept_id"],
                        "title": p["title"],
                        "slide": p["slide_ref"],
                        "formula": p.get("primary_formula", "")
                    }
                    for p in prereq_cits
                ]
            })

        return citations

    def generate_or_get_study_plan(
        self,
        srn: str,
        course_id: str = "AIML-401",
        force_regenerate: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves existing plan from student_study_plans or automatically synthesizes a new
        remedial study plan targeting the student's exact weak IA topics using Syllabus RAG.
        """
        # 1. Check if cached plan exists on Fluxbase
        if not force_regenerate:
            check_sql = f"""
            SELECT * FROM student_study_plans 
            WHERE student_srn = '{srn}' AND course_id = '{course_id}'
            ORDER BY generated_at DESC LIMIT 1;
            """
            existing_res = self.flux_db.execute_query(check_sql)
            if existing_res.get("rows"):
                row = existing_res["rows"][0]
                return {
                    "status": "success",
                    "plan_id": row.get("plan_id"),
                    "student_srn": srn,
                    "course_id": course_id,
                    "weak_topics": row.get("weak_topics", []),
                    "syllabus_citations": row.get("retrieved_syllabus_citations", []),
                    "study_plan": row.get("study_plan_text"),
                    "tasks": row.get("tasks", []),
                    "generated_at": row.get("generated_at"),
                    "source": "cached_cloud_plan"
                }

        # 2. Identify weak IA topics
        weak_topics = self.get_student_weak_topics(srn, course_id)
        if not weak_topics:
            return {
                "status": "success",
                "message": "Student has cleared all IA topics with score >= 50%. No remedial intervention required.",
                "weak_topics": [],
                "study_plan": "Excellent academic performance! You have demonstrated strong mastery across all tested topics."
            }

        topic_ids = list(set(t["topic_id"] for t in weak_topics))

        # 3. Retrieve Syllabus citations via Hybrid RAG
        citations = self.retrieve_syllabus_context(course_id, topic_ids)

        # 4. Perform Root-Cause DAG Traversal & Prerequisite Gap Scoring
        primary_topic = topic_ids[0] if topic_ids else "DL_BACKPROP"
        evidence_map = {t["topic_id"]: (t["marks_obtained"] / max(1.0, t["max_marks"])) for t in weak_topics}
        gap_analysis = self.pkg.trace_prerequisite_gaps(primary_topic, topic_ids)
        pgs_eval = self.pkg.calculate_prerequisite_gap_score(primary_topic, evidence_map)

        # 5. Construct Rigorous Grounded AI Prompt
        prompt_lines = [
            f"Student SRN: {srn}",
            f"Course Code: {course_id}",
            f"Primary Target Deficit: {gap_analysis['target_concept']['name']} ({primary_topic})",
            f"Cognitive Prerequisite Gap Score (PGS): {pgs_eval['normalized_pgs_score']} (Risk Tier: {pgs_eval['risk_tier']})"
        ]
        if gap_analysis.get("root_cause_bottleneck"):
            prompt_lines.append(f"Root-Cause Bottleneck Identified: {gap_analysis['root_cause_bottleneck']['name']} (Blocking {gap_analysis['root_cause_bottleneck']['blocked_downstream_count']} downstream concepts)")

        prompt_lines.append("\nIdentified Weak Assessment Topics (< 50% in Internal Assessment):")
        for wt in weak_topics:
            prompt_lines.append(f"- {wt.get('topic_title')} ({wt.get('topic_id')}): Score {wt.get('marks_obtained')}/{wt.get('max_marks')} ({wt.get('score_percentage')}%)")

        prompt_lines.append("\nRetrieved Syllabus Learning Outcomes & Slide Citations (ChromaDB + BM25 Fused):")
        retrieved_texts_for_guard = []
        for cit in citations:
            prompt_lines.append(f"• Concept: {cit['topic_name']} ({cit['topic_id']}) | Slide Citation: {cit['slide_citation']} | Bloom Level: {cit.get('bloom_taxonomy', 'Apply')}")
            if cit.get("primary_formula"):
                prompt_lines.append(f"  Governing Formula: {cit['primary_formula']}")
            if cit.get("foundational_prerequisite_slides"):
                for pslide in cit["foundational_prerequisite_slides"]:
                    prompt_lines.append(f"  Foundational Slide: {pslide['title']} ({pslide['slide']}) -> Formula: {pslide.get('formula', '')}")
            prompt_lines.append(f"  Curriculum Excerpt: {cit['syllabus_excerpt']}")
            retrieved_texts_for_guard.append(cit['syllabus_excerpt'])

        prompt_context = "\n".join(prompt_lines)

        system_instruction = (
            "You are the Lead Academic Remediation Mentor & Senior AI Professor at REVA University. "
            "A student has scored poorly (< 50%) in specific Internal Assessment (IA) topics. "
            "Synthesize a rigorous, encouraging 5-Day Remedial Action Plan that directly resolves the root-cause prerequisite deficits "
            "and grounds every study milestone with explicit syllabus slide citations and primary equations."
        )

        user_instruction = (
            f"Based on the following assessment data and verified syllabus context:\n\n"
            f"{prompt_context}\n\n"
            f"Generate a structured 5-Day Remedial Action Plan with:\n"
            f"1. Executive Root-Cause Diagnostic & Cognitive Gap Summary (citing PGS score and root bottleneck)\n"
            f"2. Day 1 & 2: Prerequisite Foundations Refresher (cite exact foundational slide references and formulas)\n"
            f"3. Day 3 & 4: Core IA Topic Step-by-Step Analytical Derivation & Vectorized Code Walkthrough\n"
            f"4. Day 5: Adaptive Micro-Drill Self-Assessment & Faculty Checkpoint\n"
            f"Maintain strict academic fidelity, cite slide references verbatim, and format with clean bullet points."
        )

        start_time = time.time()
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_instruction}
        ]
        ai_resp = self.flux_ai.chat_completion(messages, model="flux-flash", max_tokens=750)
        study_plan_text = ai_resp.get("content", "")
        latency_ms = int((time.time() - start_time) * 1000)

        # 6. Evaluate Faithfulness with RAGAS Guard
        guard_eval = self.rag_guard.evaluate_grounding(
            query=f"Remedial plan for {primary_topic}",
            retrieved_contexts=retrieved_texts_for_guard,
            generated_response=study_plan_text
        )

        # 7. Extract structured tasks aligned with diagnosed root-cause
        bottleneck_name = gap_analysis.get("root_cause_bottleneck", {}).get("name", "Foundational Calculus")
        target_name = gap_analysis["target_concept"]["name"]
        tasks = [
            {
                "day": 1,
                "title": f"Root Foundational Review: {bottleneck_name}",
                "description": f"Review slide {citations[0].get('slide_citation', 'Unit-01-Slide-45')} and derive governing equations for {bottleneck_name}.",
                "completed": False
            },
            {
                "day": 2,
                "title": "Computational Mechanism & Forward Pass",
                "description": "Trace forward activations and intermediate computational graph representations.",
                "completed": False
            },
            {
                "day": 3,
                "title": f"Core Topic Mastery: {target_name}",
                "description": f"Solve 3 analytical examination problems targeting {target_name} from syllabus materials.",
                "completed": False
            },
            {
                "day": 4,
                "title": "Vectorized Code Implementation",
                "description": f"Implement clean NumPy / PyTorch worked examples verifying {primary_topic} dynamics.",
                "completed": False
            },
            {
                "day": 5,
                "title": "Adaptive Formative Micro-Drill & Faculty Sign-Off",
                "description": "Complete adaptive isomorphic quiz on smart platform and submit error log for faculty sign-off.",
                "completed": False
            }
        ]

        # 6. Persist generated plan in Fluxbase PostgreSQL
        plan_id = f"PLAN_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        weak_topics_json = json.dumps([t["topic_id"] for t in weak_topics]).replace("'", "''")
        citations_json = json.dumps(citations).replace("'", "''")
        clean_plan_text = study_plan_text.replace("'", "''")
        tasks_json = json.dumps(tasks).replace("'", "''")

        sql_insert = f"""
        INSERT INTO student_study_plans (plan_id, student_srn, course_id, weak_topics, retrieved_syllabus_citations, study_plan_text, tasks)
        VALUES ('{plan_id}', '{srn}', '{course_id}', '{weak_topics_json}', '{citations_json}', '{clean_plan_text}', '{tasks_json}');
        """
        try:
            self.flux_db.execute_query(sql_insert)
        except Exception as e:
            logger.warning(f"Could not persist study plan in PostgreSQL: {e}")

        # 7. Log AI inference call
        self.auth_service.log_ai_call(
            actor_id=srn,
            task_type="WEAK_TOPIC_REMEDIAL_PLAN",
            model_id="AWS_BEDROCK_CLAUDE_3.5_SONNET",
            prompt_summary=f"Remedial plan for {len(weak_topics)} weak IA topics in {course_id}",
            input_tokens=len(user_instruction.split()),
            output_tokens=len(study_plan_text.split()),
            latency_ms=latency_ms,
            status="SUCCESS"
        )

        return {
            "status": "success",
            "plan_id": plan_id,
            "student_srn": srn,
            "course_id": course_id,
            "weak_topics": weak_topics,
            "syllabus_citations": citations,
            "prerequisite_gap_analysis": gap_analysis,
            "prerequisite_gap_score": pgs_eval,
            "ragas_faithfulness_guard": guard_eval,
            "study_plan": study_plan_text,
            "tasks": tasks,
            "source": "freshly_synthesized_rag_plan"
        }

    def get_class_weak_topics_summary(self, course_id: str, assessment: str = "all") -> Dict[str, Any]:
        """
        Aggregates question-level IA and Assignment scores across the entire class to give faculty
        a distribution of which syllabus topics students are failing most frequently.
        Optionally filters by assessment: 'all', 'ia1', 'ia2', 'asg1', 'asg2'.
        """
        where_clause = f"WHERE course_id = '{course_id}'"
        assessment_norm = (assessment or "all").lower().strip()
        ia_filter_map = {
            "ia1": "AND ia_number = 1",
            "ia-1": "AND ia_number = 1",
            "ia2": "AND ia_number = 2",
            "ia-2": "AND ia_number = 2",
            "asg1": "AND ia_number = 11",
            "assignment1": "AND ia_number = 11",
            "asg-1": "AND ia_number = 11",
            "asg2": "AND ia_number = 12",
            "assignment2": "AND ia_number = 12",
            "asg-2": "AND ia_number = 12",
        }
        if assessment_norm in ia_filter_map:
            where_clause += f" {ia_filter_map[assessment_norm]}"

        sql = f"""
        SELECT 
            ia_number,
            topic_id, 
            topic_title,
            COUNT(*) as total_attempts,
            COUNT(CASE WHEN is_weak THEN 1 END) as weak_count,
            ROUND(AVG(marks_obtained), 2) as avg_marks,
            ROUND(AVG(score_percentage), 2) as avg_percentage
        FROM ia_question_scores
        {where_clause}
        GROUP BY ia_number, topic_id, topic_title
        ORDER BY ia_number ASC, weak_count DESC, avg_percentage ASC;
        """
        res = self.flux_db.execute_query(sql)
        rows = res.get("rows", [])
        
        # Calculate class-level percentage struggling
        summary = []
        assessment_labels = {
            1: {"code": "IA-1", "name": "IA-1 Midterm", "type": "Internal Assessment"},
            2: {"code": "IA-2", "name": "IA-2 Midterm", "type": "Internal Assessment"},
            11: {"code": "ASG-1", "name": "Assignment 1", "type": "Course Assignment"},
            12: {"code": "ASG-2", "name": "Assignment 2", "type": "Course Assignment"},
        }
        for r in rows:
            try:
                attempts = float(r.get("total_attempts") or 1)
                weaks = float(r.get("weak_count") or 0)
                weak_pct = round((weaks / attempts) * 100, 1) if attempts > 0 else 0.0
            except Exception:
                attempts = 1.0
                weaks = 0.0
                weak_pct = 0.0

            ia_num = int(r.get("ia_number") or 1)
            meta = assessment_labels.get(ia_num, {"code": f"IA-{ia_num}", "name": f"Assessment {ia_num}", "type": "Assessment"})

            summary.append({
                "ia_number": ia_num,
                "assessment_code": meta["code"],
                "assessment_name": meta["name"],
                "assessment_type": meta["type"],
                "topic_id": r.get("topic_id"),
                "topic_title": r.get("topic_title"),
                "total_students": attempts,
                "students_struggling": weaks,
                "struggle_rate_pct": weak_pct,
                "avg_marks": r.get("avg_marks"),
                "avg_percentage": r.get("avg_percentage"),
                "priority": "HIGH" if weak_pct >= 50 else ("MEDIUM" if weak_pct >= 25 else "LOW")
            })

        return {
            "course_id": course_id,
            "filter_applied": assessment_norm,
            "total_analyzed_topics": len(summary),
            "class_weakness_distribution": summary
        }
