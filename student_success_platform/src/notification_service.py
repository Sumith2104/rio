"""
=============================================================================
REVA SMART CAMPUS PLATFORM - SMTP NOTIFICATION DISPATCHER SERVICE
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
Provides automated SMTP Nodemailer student alerts for:
  1. Faculty Document / Lecture Notes Uploads (doc_upload)
  2. Course Homework & Problem Distribution (assignment)
  3. Low Attendance & Eligibility Threshold Warnings (attendance)

Emails are resolved directly from the live PostgreSQL database (platform_users & students).
=============================================================================
"""

import os
import sys
import json
import logging
import subprocess
import time
from typing import Dict, Any, Optional, List

logger = logging.getLogger("NotificationService")
logger.setLevel(logging.INFO)

# Root directory for invoking node smtp_mailer.js
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, "..", ".."))
SMTP_MAILER_PATH = os.path.join(PROJECT_ROOT, "smtp_mailer.js")

class NotificationService:
    def __init__(self):
        from fluxbase_client import FluxbaseClient
        self.flux_db = FluxbaseClient()

    def get_student_contact(self, srn_or_id: str) -> Dict[str, str]:
        """
        Query student's full name and email from PostgreSQL (platform_users & students).
        Falls back to default student Sumith U if not found.
        """
        clean_id = (srn_or_id or "").strip()
        alias_map = {
            "STU-807": "R24EA807",
            "STU-818": "R24EA818",
            "STU-842": "R24EA842",
            "STU-801": "R24EA801",
            "STU-895": "R24EA895"
        }
        resolved_srn = alias_map.get(clean_id, clean_id)
        
        # Query platform_users with cache-buster nonce
        nonce = time.time_ns()
        sql = f"""
        /* notif_lookup_nonce={nonce} */
        SELECT email, display_name, entity_id, role
        FROM platform_users
        WHERE (LOWER(entity_id) = LOWER('{resolved_srn}') OR LOWER(user_id) = LOWER('{clean_id}') OR LOWER(email) = LOWER('{clean_id}'))
          AND role = 'student'
        LIMIT 1;
        """
        try:
            # First check students table for authentic full name
            st_res = self.flux_db.execute_query(f"SELECT srn, student_name, email FROM students WHERE LOWER(srn) = LOWER('{resolved_srn}') LIMIT 1;")
            st_rows = st_res.get("rows", [])
            if st_rows:
                r = st_rows[0]
                return {
                    "email": r.get("email") or "sumithu.dev@gmail.com",
                    "name": r.get("student_name") or "Student",
                    "entityId": resolved_srn
                }

            res = self.flux_db.execute_query(sql)
            rows = res.get("rows", []) or res.get("data", [])
            if rows:
                row = rows[0]
                email = row.get("email") or "sumithu.dev@gmail.com"
                name = row.get("display_name") or "Student"
                entity_id = row.get("entity_id") or resolved_srn
                return {
                    "email": email,
                    "name": name,
                    "entityId": entity_id
                }
        except Exception as e:
            logger.warning(f"Error querying student contact: {e}")

        # Default fallback to primary student profile
        return {
            "email": "sumithu.dev@gmail.com",
            "name": "Sumith U",
            "entityId": resolved_srn or "R24EA807"
        }

    def dispatch_email(self, cmd_args: List[str]) -> Dict[str, Any]:
        """Execute node smtp_mailer.js with provided CLI parameters."""
        cmd = ["node", SMTP_MAILER_PATH] + cmd_args
        try:
            logger.info(f"Invoking SMTP Mailer: {' '.join(cmd)}")
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, timeout=15)
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()

            # Parse JSON output from smtp_mailer.js
            # Look for JSON line starting with {
            for line in stdout.splitlines():
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        return json.loads(line)
                    except Exception:
                        pass

            if proc.returncode == 0:
                return {
                    "success": True,
                    "output": stdout,
                    "transport": "smtp"
                }
            else:
                return {
                    "success": False,
                    "error": stderr or stdout or "Non-zero exit code from node mailer"
                }
        except Exception as ex:
            logger.error(f"Failed to execute smtp_mailer.js: {ex}")
            return {
                "success": False,
                "error": str(ex)
            }

    def notify_material_uploaded(
        self,
        title: str,
        unit_name: str = "Unit 3: Deep Neural Networks",
        uploaded_by: str = "Dr. Ramesh Kumar",
        course: str = "AIML-401 Deep Learning",
        target_srn: str = "STU-807"
    ) -> Dict[str, Any]:
        """Send doc_upload notification to student."""
        contact = self.get_student_contact(target_srn)
        args = [
            "--type", "doc_upload",
            "--to", contact["email"],
            "--name", contact["name"],
            "--entityId", contact["entityId"],
            "--title", title,
            "--unit", unit_name,
            "--uploadedBy", uploaded_by,
            "--course", course
        ]
        res = self.dispatch_email(args)
        res["recipient"] = contact
        return res

    def notify_assignment(
        self,
        title: str,
        due_date: str = "2026-11-10",
        marks: str = "10 Marks",
        course: str = "AIML-401 Deep Learning",
        target_srn: str = "STU-807"
    ) -> Dict[str, Any]:
        """Send assignment notification to student."""
        contact = self.get_student_contact(target_srn)
        args = [
            "--type", "assignment",
            "--to", contact["email"],
            "--name", contact["name"],
            "--entityId", contact["entityId"],
            "--title", title,
            "--dueDate", due_date,
            "--marks", marks,
            "--course", course
        ]
        res = self.dispatch_email(args)
        res["recipient"] = contact
        return res

    def notify_attendance_alert(
        self,
        attendance_rate: str = "68.0%",
        threshold: str = "75.0%",
        course: str = "AIML-401 Deep Learning",
        target_srn: str = "STU-807"
    ) -> Dict[str, Any]:
        """Send attendance alert notification to student."""
        contact = self.get_student_contact(target_srn)
        args = [
            "--type", "attendance",
            "--to", contact["email"],
            "--name", contact["name"],
            "--entityId", contact["entityId"],
            "--att", str(attendance_rate),
            "--threshold", str(threshold),
            "--course", course
        ]
        res = self.dispatch_email(args)
        res["recipient"] = contact
        return res


    def notify_dice_recourse(
        self,
        target_srn: str = "R24EA895",
        advice: str = "",
        weak_topics: Optional[List[str]] = None,
        targets_str: str = "",
        projected_pass_prob: float = 76.5,
        course: str = "AIML-401 Deep Learning"
    ) -> Dict[str, Any]:
        """Send DiCE counterfactual prescriptive advice and diagnosed weak topics to student."""
        contact = self.get_student_contact(target_srn)
        weak_list = weak_topics or [
            "Multivariable Calculus: Partial Derivatives",
            "Multivariate Chain Rule & Graph Propagation",
            "Reverse-Mode Autodiff & Backpropagation"
        ]
        weak_joined = "||".join(weak_list)
        args = [
            "--type", "dice_plan",
            "--to", contact["email"],
            "--name", contact["name"],
            "--entityId", contact["entityId"],
            "--course", course,
            "--advice", advice or "Attend next 6 consecutive lectures without absence and complete the 5-day remedial drills on Chain Rule & Backpropagation to score >= 18/30 on IA-2.",
            "--weakTopics", weak_joined,
            "--targets", targets_str or "Attendance >= 75.0% (+24%), IA-2 >= 18.0/30 (+7.0 marks), Assignment 2 >= 7.0/10 (+3.5 marks)",
            "--projectedPass", f"{projected_pass_prob}%"
        ]
        res = self.dispatch_email(args)
        res["recipient"] = contact
        res["advice"] = advice
        res["weak_topics"] = weak_list
        res["targets"] = targets_str
        res["projected_pass_prob"] = projected_pass_prob
        return res


# Global singleton instance
notification_service = NotificationService()
