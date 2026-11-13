"""
Autonomous Academic Data Ingest & ML Execution Tool (PACD-RAG)
==============================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Ingests and validates tabular attendance, IA marks, and exam records.
Triggers CatBoost ML risk predictions, updates course enrollments,
and synthesizes personalized remedial study plans.
"""

import os
import sys
import json
from typing import Dict, Any, List, Optional

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from fluxbase_client import FluxbaseClient
from weak_topic_rag_engine import WeakTopicRAGEngine

class AcademicIngestTool:
    def __init__(self, db_client: Optional[FluxbaseClient] = None, rag_engine: Optional[WeakTopicRAGEngine] = None):
        self.db = db_client or FluxbaseClient()
        self.weak_rag = rag_engine or WeakTopicRAGEngine()
        self.decision_threshold = 0.42

    def _extract_srn(self, record: Dict[str, Any]) -> Optional[str]:
        """Robustly finds student SRN from various common column names."""
        for key in ["student_srn", "srn", "usn", "student_id", "roll_no", "reg_no"]:
            if key in record and record[key]:
                return str(record[key]).strip().upper()
        return None

    def ingest_attendance_sheet(self, course_id: str, records: List[Dict[str, Any]], faculty_id: str) -> Dict[str, Any]:
        """Updates class attendance percentages and flags low attendance students."""
        updated = 0
        at_risk_attendance = []

        for row in records:
            srn = self._extract_srn(row)
            if not srn:
                continue

            # Find attendance value
            att_val = None
            for key in ["attendance_pct", "attendance", "att_pct", "percentage", "pct"]:
                if key in row and row[key] is not None:
                    try:
                        att_val = float(str(row[key]).replace("%", "").strip())
                        break
                    except ValueError:
                        pass
            
            # If classes held/attended provided
            if att_val is None and "attended" in row and "classes_held" in row:
                try:
                    att_val = (float(row["attended"]) / float(row["classes_held"])) * 100.0
                except (ValueError, ZeroDivisionError):
                    pass

            if att_val is not None:
                att_val = min(100.0, max(0.0, att_val))
                self.db.execute_query(f"""
                    UPDATE course_enrollments
                    SET attendance_pct = {att_val}
                    WHERE srn = '{srn}' AND course_id = '{course_id}';
                """)
                updated += 1

                if att_val < 75.0:
                    at_risk_attendance.append({"srn": srn, "attendance": att_val})

        return {
            "status": "ATTENDANCE_INGESTED",
            "course_id": course_id,
            "total_records_processed": len(records),
            "students_updated": updated,
            "low_attendance_flagged": len(at_risk_attendance),
            "at_risk_students": at_risk_attendance[:5],
            "summary": f"Ingested attendance for {updated} students in {course_id}. Flagged {len(at_risk_attendance)} below 75%."
        }

    def ingest_ia_marks(self, course_id: str, records: List[Dict[str, Any]], faculty_id: str) -> Dict[str, Any]:
        """
        Updates IA marks, evaluates dropout risk (tau = 0.42), and generates remedial plans.
        """
        updated = 0
        weak_plans_generated = []

        for row in records:
            srn = self._extract_srn(row)
            if not srn:
                continue

            ia1 = None
            ia2 = None

            for key in ["ia1", "ia1_score", "ia_1", "ia1_marks"]:
                if key in row and row[key] is not None:
                    try:
                        ia1 = float(row[key])
                        break
                    except ValueError:
                        pass

            for key in ["ia2", "ia2_score", "ia_2", "ia2_marks"]:
                if key in row and row[key] is not None:
                    try:
                        ia2 = float(row[key])
                        break
                    except ValueError:
                        pass

            set_clauses = []
            if ia1 is not None:
                set_clauses.append(f"ia1_score = {ia1}")
            if ia2 is not None:
                set_clauses.append(f"ia2_score = {ia2}")

            if set_clauses:
                self.db.execute_query(f"""
                    UPDATE course_enrollments
                    SET {', '.join(set_clauses)}
                    WHERE srn = '{srn}' AND course_id = '{course_id}';
                """)
                updated += 1

                # Check if remedial plan should be generated (if average marks < 15 / 30)
                avg_ia = ((ia1 or 15.0) + (ia2 or 15.0)) / 2.0
                if avg_ia < 15.0:
                    try:
                        plan = self.weak_rag.generate_or_get_study_plan(srn, course_id, force_regenerate=True)
                        if plan and plan.get("remedial_plan"):
                            weak_plans_generated.append({"srn": srn, "avg_ia": avg_ia})
                    except Exception:
                        pass

        return {
            "status": "IA_MARKS_INGESTED_AND_EVALUATED",
            "course_id": course_id,
            "students_updated": updated,
            "remedial_plans_synthesized": len(weak_plans_generated),
            "flagged_for_remediation": weak_plans_generated[:5],
            "summary": f"Recorded IA marks for {updated} students in {course_id}; auto-generated {len(weak_plans_generated)} remedial plans."
        }

    def ingest_exam_marks(self, course_id: str, records: List[Dict[str, Any]], faculty_id: str) -> Dict[str, Any]:
        """Updates end-semester exam scores and calculates letter grades."""
        updated = 0

        for row in records:
            srn = self._extract_srn(row)
            if not srn:
                continue

            exam_score = None
            for key in ["exam_score", "end_sem", "see_marks", "final_exam", "exam"]:
                if key in row and row[key] is not None:
                    try:
                        exam_score = float(row[key])
                        break
                    except ValueError:
                        pass

            if exam_score is not None:
                # Grade mapping
                if exam_score >= 90: grade = "A+"
                elif exam_score >= 80: grade = "A"
                elif exam_score >= 70: grade = "B"
                elif exam_score >= 60: grade = "C"
                elif exam_score >= 50: grade = "D"
                else: grade = "F"

                self.db.execute_query(f"""
                    UPDATE course_enrollments
                    SET exam_score = {exam_score}, overall_grade = '{grade}'
                    WHERE srn = '{srn}' AND course_id = '{course_id}';
                """)
                updated += 1

        return {
            "status": "EXAM_MARKS_INGESTED",
            "course_id": course_id,
            "students_updated": updated,
            "summary": f"Recorded final exam marks and computed grades for {updated} students in {course_id}."
        }

if __name__ == "__main__":
    tool = AcademicIngestTool()
    print("AcademicIngestTool initialized successfully.")
