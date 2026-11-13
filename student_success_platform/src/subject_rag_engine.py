"""
=============================================================================
SUBJECT-SCOPED INTELLIGENT RAG ENGINE (PACD-RAG)
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
This engine provides subject-partitioned Retrieval-Augmented Generation:
  1. Uploads and indexes course files (syllabus, notes, question banks) strictly scoped by course_id.
  2. Stores document metadata in Fluxbase Cloud PostgreSQL (learning_materials table).
  3. Indexes semantic text embeddings into local Docker ChromaDB.
  4. Implements Prerequisite-Aware RAG (PACD-RAG): when a student asks a question,
     it retrieves foundational prerequisite materials first to prevent cognitive overload.
  5. Synthesizes scaffolded explanations using the Flux AI Gateway ('flux' model).
=============================================================================
"""

import os
import sys
import uuid
import logging
from typing import List, Dict, Any, Optional

# Ensure src is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from vector_db_manager import VectorDBManager
from fluxbase_client import FluxbaseClient
from flux_ai_service import FluxAIService
from prerequisite_graph import PrerequisiteKnowledgeGraph
from hybrid_rag_service import HybridPrerequisiteRAG

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SubjectRAGEngine:
    """
    Intelligent RAG engine partitioned by academic subject/course.
    Binds ChromaDB vector chunks with Fluxbase CRUD tables and Flux AI reasoning.
    """

    COLLECTION_COURSE_MATERIALS = "course_learning_materials"

    def __init__(self):
        """Initialize all subsystems (Vector DB, Cloud Relational DB, Prerequisite DAG, Flux AI, Hybrid Retriever)."""
        self.vdb = VectorDBManager(host="localhost", port=8001)
        self.flux_db = FluxbaseClient()
        self.flux_ai = FluxAIService()
        self.hybrid_rag = HybridPrerequisiteRAG()

        # Initialize Curriculum DAG
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        graph_json = os.path.join(base_dir, "data", "concept_prerequisites.json")
        self.pkg = PrerequisiteKnowledgeGraph(graph_json)

    # =========================================================================
    # DOCUMENT UPLOAD & SUBJECT-SCOPED INDEXING (CRUD)
    # =========================================================================

    def ingest_course_material(
        self,
        course_id: str,
        title: str,
        content_text: str,
        material_type: str = "lecture_notes",
        unit_name: str = "General",
        concept_id: Optional[str] = None,
        file_name: Optional[str] = None,
        uploaded_by_faculty_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload and index an academic document for a specific course.
        Registers the master record in Fluxbase and chunk embeddings in ChromaDB.
        """
        material_id = f"MAT_{course_id}_{uuid.uuid4().hex[:8].upper()}"

        # Step 1: Infer concept_id from content if not provided
        if not concept_id:
            concept_id = self._infer_concept_id(content_text)

        # Step 2: Register master document in Fluxbase PostgreSQL
        clean_content = content_text.replace("'", "''")
        clean_title = title.replace("'", "''")
        sql = f"""
        INSERT INTO learning_materials (material_id, course_id, unit_name, concept_id, material_type, title, content_text, file_name, uploaded_by_faculty_id)
        VALUES ('{material_id}', '{course_id}', '{unit_name}', {'NULL' if not concept_id else f"'{concept_id}'"}, '{material_type}', '{clean_title}', '{clean_content}', '{file_name or "text_input"}', {'NULL' if not uploaded_by_faculty_id else f"'{uploaded_by_faculty_id}'"})
        ON CONFLICT (material_id) DO UPDATE SET 
            title = EXCLUDED.title,
            content_text = EXCLUDED.content_text;
        """
        db_res = self.flux_db.execute_query(sql)

        # Step 3: Chunk content and index embeddings in ChromaDB
        chunks = self._chunk_text(content_text, chunk_size=350, overlap=50)
        chunk_ids = [f"{material_id}_C{i}" for i in range(len(chunks))]
        chunk_metas = [
            {
                "material_id": material_id,
                "course_id": course_id,
                "unit": unit_name,
                "concept_id": concept_id or "GENERAL",
                "material_type": material_type,
                "title": title,
                "chunk_index": i
            }
            for i in range(len(chunks))
        ]

        self.vdb.add_documents(
            self.COLLECTION_COURSE_MATERIALS,
            documents=chunks,
            metadatas=chunk_metas,
            ids=chunk_ids
        )

        logger.info(f"Ingested material '{title}' [{material_id}] for subject {course_id} ({len(chunks)} chunks).")
        return {
            "success": True,
            "material_id": material_id,
            "course_id": course_id,
            "title": title,
            "concept_id": concept_id,
            "chunks_indexed": len(chunks),
            "db_registered": db_res.get("success", False)
        }

    # =========================================================================
    # PREREQUISITE-AWARE RAG QUERY (PACD-RAG)
    # =========================================================================

    def query_subject_rag(
        self,
        course_id: str,
        student_query: str,
        student_srn: Optional[str] = None,
        target_concept_id: Optional[str] = None,
        top_k: int = 4
    ) -> Dict[str, Any]:
        """
        Execute an intelligent, prerequisite-aware search scoped to a course.
        
        Logic:
          1. Detects target concept from query using catalog or semantic matching.
          2. Traverses OKF Ontological Graph for upstream prerequisite foundations.
          3. Executes Hybrid RAG (Okapi BM25 Sparse + ChromaDB Dense Vector + RRF).
          4. Scaffolds foundational prerequisite formulas prior to target concepts.
          5. Synthesizes a grounded explanation using Flux AI.
        """
        # 1. Concept identification
        concept = target_concept_id or self._infer_concept_id(student_query)

        # 2. Retrieve hybrid context (Sparse BM25 + Dense ChromaDB + OKF DAG)
        hybrid_res = self.hybrid_rag.retrieve_hybrid_context(
            course_id=course_id,
            target_concept_id=concept or "DL_BACKPROP",
            query_text=student_query,
            include_prerequisites=True,
            top_k=top_k
        )

        prereq_ancestors = hybrid_res.get("prerequisite_ancestors", [])
        prereq_citations = hybrid_res.get("foundational_prerequisite_citations", [])
        target_citations = hybrid_res.get("target_retrieved_citations", [])

        # 3. Assemble Pedagogically Scaffolded Context
        context_blocks = []
        if prereq_citations:
            context_blocks.append("=== FOUNDATIONAL PREREQUISITE PRINCIPLES (COGNITIVE SCAFFOLDING) ===")
            for pc in prereq_citations:
                context_blocks.append(
                    f"[{pc['title']} | Slide: {pc['slide_ref']} | Bloom: {pc.get('bloom_taxonomy', 'Understand')}]\n"
                    f"Governing Formula: {pc.get('primary_formula', 'N/A')}\n"
                    f"{pc['excerpt']}"
                )

        context_blocks.append("=== PRIMARY SUBJECT LEARNING MATERIALS (TARGET TOPIC) ===")
        for tc in target_citations:
            context_blocks.append(
                f"[{tc['title']} | Slide: {tc['slide_ref']} | Bloom: {tc.get('bloom_taxonomy', 'Apply')} | RRF: {tc.get('rrf_score', 'N/A')}]\n"
                f"{tc['excerpt']}"
            )

        full_context = "\n\n".join(context_blocks)

        # 4. Synthesize Answer with Flux AI
        system_prompt = (
            "You are the Intelligent Academic RAG Tutor and Lead AI Professor at REVA University. "
            "Explain technical concepts clearly and rigorously using the retrieved subject materials. "
            "Cite relevant lecture slides verbatim (e.g., [Unit-03-Slide-32]) and incorporate governing LaTeX equations. "
            "Explain how the foundational prerequisite concepts enable mastery of the target topic."
        )

        user_prompt = (
            f"Course: {course_id}\n"
            f"Student Question: \"{student_query}\"\n\n"
            f"Retrieved Course Materials & Prerequisite Context:\n{full_context}\n\n"
            f"Please provide an educational, clear response linking the prerequisite to the answer with slide citations."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        ai_response = self.flux_ai.chat_completion(messages, model="flux", temperature=0.3, max_tokens=550)

        return {
            "course_id": course_id,
            "query": student_query,
            "detected_concept": concept,
            "target_concept_meta": hybrid_res.get("target_concept", {}),
            "prerequisite_ancestors": prereq_ancestors,
            "foundational_prerequisites": prereq_citations,
            "retrieved_sources": [
                {
                    "title": c.get("title"),
                    "unit": c.get("unit"),
                    "concept": c.get("concept_id"),
                    "slide_ref": c.get("slide_ref"),
                    "rrf_score": c.get("rrf_score")
                }
                for c in target_citations
            ],
            "scaffolded_answer": ai_response.get("content", "Explanation currently unavailable.")
        }

    # =========================================================================
    # SUBJECT CRUD HELPERS
    # =========================================================================

    def list_subject_materials(self, course_id: str) -> List[Dict[str, Any]]:
        """Retrieve all learning materials registered for a course from Fluxbase."""
        sql = f"""
        SELECT m.material_id, m.course_id, m.unit_name, m.concept_id, m.material_type, m.title, m.file_name, m.created_at, f.name as uploaded_by
        FROM learning_materials m
        LEFT JOIN faculty f ON m.uploaded_by_faculty_id = f.faculty_id
        WHERE m.course_id = '{course_id}'
        ORDER BY m.created_at DESC;
        """
        res = self.flux_db.execute_query(sql)
        return res.get("rows", [])

    # =========================================================================
    # INTERNAL UTILITIES
    # =========================================================================

    def _infer_concept_id(self, text: str) -> Optional[str]:
        """Match query text to concept catalog across all 68 OKF curriculum concepts."""
        text_lower = text.lower()
        
        # Exact keyword rules for high-frequency terms
        keyword_map = [
            ("chain rule", "MATH_CHAIN_RULE"),
            ("backprop", "DL_BACKPROP"),
            ("gradient descent", "MATH_GRAD_DESC"),
            ("sgd", "MATH_SGD_MOMENTUM"),
            ("momentum", "MATH_SGD_MOMENTUM"),
            ("adam", "MATH_ADAM_OPT"),
            ("rmsprop", "MATH_ADAM_OPT"),
            ("tree", "ML_DEC_TREE"),
            ("forest", "ML_BAGGING_RF"),
            ("xgboost", "ML_XGBOOST"),
            ("catboost", "ML_CATBOOST"),
            ("shap", "XAI_SHAP"),
            ("lime", "XAI_LIME"),
            ("counterfactual", "XAI_COUNTERFACTUAL"),
            ("calibration", "XAI_PROB_CALIBRATION"),
            ("ece", "XAI_PROB_CALIBRATION"),
            ("reliability", "XAI_RELIABILITY_DIAG"),
            ("dag", "OKF_CONCEPT_DAG"),
            ("gap score", "OKF_PREREQ_GAP_SCORE"),
            ("bottleneck", "OKF_ROOT_CAUSE_TRACE"),
            ("transformer", "DL_TRANSFORMER"),
            ("attention", "DL_SELF_ATTENTION"),
            ("lstm", "DL_LSTM_GRU"),
            ("convolution", "DL_CONV2D"),
            ("cnn", "DL_CNN_ARCH"),
            ("dropout", "DL_DROPOUT"),
            ("batch norm", "DL_BATCH_NORM"),
            ("vanishing", "DL_VANISHING_GRAD"),
            ("logistic", "ML_LOG_REG"),
            ("linear reg", "ML_LIN_REG"),
            ("svm", "ML_SVM_LINEAR"),
            ("kernel", "ML_SVM_KERNEL"),
            ("eigen", "MATH_EIGEN"),
            ("svd", "MATH_SVD"),
            ("bayes", "MATH_BAYES"),
            ("likelihood", "MATH_MLE"),
            ("jacobian", "MATH_JACOBIAN"),
            ("hessian", "MATH_JACOBIAN"),
            ("taylor", "MATH_TAYLOR"),
            ("convex", "MATH_CONVEXITY"),
            ("pruning", "ML_TREE_PRUNING"),
            ("entropy", "ML_ENTROPY_GINI"),
            ("gini", "ML_ENTROPY_GINI")
        ]

        for kw, cid in keyword_map:
            if kw in text_lower:
                return cid

        # Match against concept names in catalog
        for cid, c in self.pkg.concept_catalog.items():
            cname = c.get("name", "").lower()
            if cname in text_lower:
                return cid

        return None

    def _chunk_text(self, text: str, chunk_size: int = 350, overlap: int = 50) -> List[str]:
        """Simple word-based chunker with sliding window overlap."""
        words = text.split()
        if len(words) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            if end >= len(words):
                break
            start += (chunk_size - overlap)
        return chunks


# Standalone CLI execution demonstration
if __name__ == "__main__":
    print("\n" + "=" * 75)
    print("  INTELLIGENT SUBJECT-SCOPED RAG ENGINE (PACD-RAG)")
    print("=" * 75)

    rag = SubjectRAGEngine()

    print("\n1. Ingesting Course Lecture Note for AIML-401:")
    sample_note = (
        "In deep neural networks, backpropagation recursively calculates gradients of the loss "
        "function across each hidden layer. However, computing these partial derivatives is fundamentally "
        "impossible without applying the calculus chain rule for composite functions. If a student does "
        "not understand how composite functions differentiate, backpropagation derivations become confusing."
    )
    ingest_res = rag.ingest_course_material(
        course_id="AIML-401",
        title="Backpropagation & Calculus Foundations Lecture Note",
        content_text=sample_note,
        material_type="lecture_notes",
        unit_name="Unit 3: Deep Neural Networks",
        concept_id="DL_BACKPROP",
        file_name="backprop_lecture_03.pdf",
        uploaded_by_faculty_id="FAC_AIML_01"
    )
    print(f"   * Ingest Result: {ingest_res}")

    print("\n2. Executing Prerequisite-Aware RAG Query on 'AIML-401':")
    q = "Why do I need to know the calculus chain rule to understand backpropagation in neural networks?"
    answer_payload = rag.query_subject_rag(course_id="AIML-401", student_query=q)

    print(f"\nTarget Concept Detected: {answer_payload['detected_concept']}")
    print(f"Prerequisite Ancestors Traced: {answer_payload['prerequisite_ancestors']}")
    print(f"\nFlux AI Scaffolded Explanation:\n{answer_payload['scaffolded_answer']}")
    print("=" * 75 + "\n")

