"""
Master Autonomous Agent Orchestrator (PACD-RAG)
==============================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Autonomous ReAct-style Agent Orchestrator:
Ingests any file uploaded by faculty (syllabus, slides, attendance, IA marks, assignments, exams),
determines cognitive intent, and executes tool chains across VectorDB, PostgreSQL, ML Models,
RAG Engines, Rubric Builders, and PDF Report Generators.
"""

import os
import sys
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from fluxbase_client import FluxbaseClient
from file_parser_tool import FileParserTool
from assignment_manager_tool import AssignmentManagerTool
from syllabus_indexer_tool import SyllabusIndexerTool
from academic_ingest_tool import AcademicIngestTool
from report_generator_tool import ReportGeneratorTool

class AgentOrchestrator:
    def __init__(self):
        self.db = FluxbaseClient()
        self.parser = FileParserTool()
        self.assignment_tool = AssignmentManagerTool(self.db)
        self.syllabus_tool = SyllabusIndexerTool(db_client=self.db)
        self.academic_tool = AcademicIngestTool(self.db)
        self.report_tool = ReportGeneratorTool(self.db)

    def _log_step(self, steps_log: List[Dict[str, Any]], phase: str, message: str, details: Optional[Dict[str, Any]] = None):
        """Appends structured trace item to execution log."""
        steps_log.append({
            "step_number": len(steps_log) + 1,
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "message": message,
            "details": details or {}
        })

    def process_faculty_upload(
        self,
        file_path: str,
        course_id: str = "AIML-401",
        faculty_id: str = "USR_FAC01"
    ) -> Dict[str, Any]:
        """
        Master execution pipeline triggered whenever faculty uploads any document.
        Runs fully autonomously without requiring manual category selection.
        """
        job_id = f"JOB_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
        filename = os.path.basename(file_path)
        steps_log: List[Dict[str, Any]] = []

        # Initialize job in DB
        self._log_step(steps_log, "INITIALIZATION", f"Received upload '{filename}' for course {course_id}")
        self.db.execute_query(f"""
            INSERT INTO agent_execution_jobs (job_id, faculty_id, course_id, original_filename, detected_type, status, steps_log)
            VALUES (
                '{job_id}',
                '{faculty_id}',
                '{course_id}',
                '{filename}',
                'ANALYZING',
                'PROCESSING',
                '{json.dumps(steps_log).replace("'", "''")}'::jsonb
            );
        """)

        try:
            # 1. PERCEIVE & PARSE
            self._log_step(steps_log, "PERCEPTION", f"Invoking FileParserTool on '{filename}'")
            parsed = self.parser.parse_file(file_path)
            file_type = parsed.get("file_type")
            classification = parsed.get("classification", {})
            doc_type = classification.get("detected_type", "GENERAL_ACADEMIC_DOCUMENT")
            target_tool = classification.get("target_tool", "syllabus_indexer_tool")

            self._log_step(
                steps_log,
                "CLASSIFICATION",
                f"Document classified as '{doc_type}' with {int(classification.get('confidence', 0.8)*100)}% confidence.",
                {"doc_type": doc_type, "target_tool": target_tool}
            )

            # Update detected type in DB
            self.db.execute_query(f"""
                UPDATE agent_execution_jobs
                SET detected_type = '{doc_type}'
                WHERE job_id = '{job_id}';
            """)

            action_result = {}

            # 2. AUTONOMOUS TOOL EXECUTION
            if doc_type == "ASSIGNMENT_SPECIFICATION":
                self._log_step(steps_log, "TOOL_EXECUTION", "Executing AssignmentManagerTool: Parsing rubric & auto-assigning to cohort")
                raw_text = parsed.get("raw_text", "")
                asg_res = self.assignment_tool.create_and_distribute_assignment(
                    course_id=course_id,
                    faculty_id=faculty_id,
                    raw_text=raw_text,
                    filename=filename
                )
                action_result = asg_res
                self._log_step(
                    steps_log,
                    "ACTION_COMPLETE",
                    f"Created assignment '{asg_res.get('title')}' and distributed to {asg_res.get('students_assigned')} students.",
                    asg_res
                )

            elif doc_type == "SYLLABUS_OR_SLIDES":
                self._log_step(steps_log, "TOOL_EXECUTION", "Executing SyllabusIndexerTool: Chunking & vectorizing into ChromaDB")
                raw_text = parsed.get("raw_text", "")
                idx_res = self.syllabus_tool.index_syllabus_or_slides(
                    course_id=course_id,
                    faculty_id=faculty_id,
                    raw_text=raw_text,
                    filename=filename
                )
                action_result = idx_res
                self._log_step(
                    steps_log,
                    "ACTION_COMPLETE",
                    f"Indexed {idx_res.get('total_chunks_created')} chunks into ChromaDB vector store; extracted {idx_res.get('prerequisite_concepts_discovered')} prerequisite concepts.",
                    idx_res
                )

            elif doc_type == "ATTENDANCE_SHEET":
                self._log_step(steps_log, "TOOL_EXECUTION", "Executing AcademicIngestTool: Updating class attendance records")
                records = parsed.get("records", [])
                att_res = self.academic_tool.ingest_attendance_sheet(course_id, records, faculty_id)
                action_result = att_res
                self._log_step(
                    steps_log,
                    "ACTION_COMPLETE",
                    f"Updated attendance for {att_res.get('students_updated')} students. Flagged {att_res.get('low_attendance_flagged')} at-risk below 75%.",
                    att_res
                )

            elif doc_type == "IA_MARKS":
                self._log_step(steps_log, "TOOL_EXECUTION", "Executing AcademicIngestTool: Updating IA marks and evaluating risk pipeline")
                records = parsed.get("records", [])
                ia_res = self.academic_tool.ingest_ia_marks(course_id, records, faculty_id)
                action_result = ia_res
                self._log_step(
                    steps_log,
                    "ACTION_COMPLETE",
                    f"Recorded marks for {ia_res.get('students_updated')} students. Synthesized {ia_res.get('remedial_plans_synthesized')} personalized 5-Day Remedial Plans.",
                    ia_res
                )

            elif doc_type == "EXAM_MARKS":
                self._log_step(steps_log, "TOOL_EXECUTION", "Executing AcademicIngestTool: Recording final exam marks & calculating grades")
                records = parsed.get("records", [])
                exam_res = self.academic_tool.ingest_exam_marks(course_id, records, faculty_id)
                action_result = exam_res
                self._log_step(
                    steps_log,
                    "ACTION_COMPLETE",
                    f"Computed final grades for {exam_res.get('students_updated')} students.",
                    exam_res
                )

            else:
                # Default document ingestion
                raw_text = parsed.get("raw_text", "")
                idx_res = self.syllabus_tool.index_syllabus_or_slides(course_id, faculty_id, raw_text, filename)
                action_result = idx_res
                self._log_step(steps_log, "ACTION_COMPLETE", f"Indexed {idx_res.get('total_chunks_created')} chunks.", idx_res)

            # 3. REPORT SYNTHESIS TOOL
            self._log_step(steps_log, "REPORT_GENERATION", "Invoking ReportGeneratorTool: Generating PDF performance dossier")
            try:
                rep_res = self.report_tool.generate_course_summary_pdf(course_id, faculty_id)
                self._log_step(steps_log, "REPORT_READY", f"PDF report compiled: {rep_res.get('report_filename')}", rep_res)
            except Exception as e:
                rep_res = {"status": "SKIPPED", "error": str(e)}

            # 4. FINALIZATION
            now_iso = datetime.now().isoformat()
            self._log_step(steps_log, "SUCCESS", "Autonomous agent job completed with zero manual interventions.")

            summary = {
                "job_id": job_id,
                "filename": filename,
                "course_id": course_id,
                "detected_type": doc_type,
                "status": "COMPLETED",
                "action_result": action_result,
                "report": rep_res,
                "steps_log": steps_log,
                "total_steps": len(steps_log)
            }

            # Update DB with final status and log
            self.db.execute_query(f"""
                UPDATE agent_execution_jobs
                SET status = 'COMPLETED',
                    completed_at = '{now_iso}',
                    steps_log = '{json.dumps(steps_log).replace("'", "''")}'::jsonb,
                    result_summary = '{json.dumps(summary).replace("'", "''")}'::jsonb
                WHERE job_id = '{job_id}';
            """)

            return summary

        except Exception as e:
            now_iso = datetime.now().isoformat()
            self._log_step(steps_log, "ERROR", f"Agent encountered an exception: {str(e)}")
            self.db.execute_query(f"""
                UPDATE agent_execution_jobs
                SET status = 'FAILED',
                    completed_at = '{now_iso}',
                    steps_log = '{json.dumps(steps_log).replace("'", "''")}'::jsonb
                WHERE job_id = '{job_id}';
            """)
            raise e

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Returns the real-time execution log and status of an agent job."""
        res = self.db.execute_query(f"""
            SELECT * FROM agent_execution_jobs WHERE job_id = '{job_id}';
        """)
        rows = res.get("rows", [])
        return rows[0] if rows else None

    def list_recent_jobs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Lists recent agent execution runs for the faculty portal."""
        res = self.db.execute_query(f"""
            SELECT job_id, faculty_id, course_id, original_filename, detected_type, status, created_at, completed_at
            FROM agent_execution_jobs
            ORDER BY created_at DESC
            LIMIT {limit};
        """)
        return res.get("rows", [])

if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    print("AgentOrchestrator initialized successfully.")

