"""
=============================================================================
FLUXBASE CLOUD DATABASE CLIENT (FLUXBASEDB.ME)
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
This module integrates the cloud-hosted Fluxbase PostgreSQL database
(https://fluxbasedb.me) to store, query, and manage:
  1. Faculty Profiles & Academic Advisors
  2. Student Records, Demographics, & Early-Warning Risk Levels
  3. Faculty Advising Notes & Intervention Action Logs
=============================================================================
"""

import os
import json
import logging
import requests
import time
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class FluxbaseClient:
    """
    Client for interacting with the Fluxbase Cloud Database via its REST API.
    Connects to the project's PostgreSQL engine on https://fluxbasedb.me.
    """

    DEFAULT_BASE_URL = "https://fluxbasedb.me"

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        config_path: Optional[str] = None
    ):
        """
        Initialize the Fluxbase client.
        
        Args:
            api_key: Secret API key (starts with 'fl_').
            project_id: Hexadecimal project identifier.
            config_path: Optional path to JSON configuration file.
        """
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "fluxbase_config.json")

        self.api_key = api_key
        self.project_id = project_id
        self.base_url = self.DEFAULT_BASE_URL

        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    if not self.api_key:
                        self.api_key = cfg.get("api_key")
                    if not self.project_id:
                        self.project_id = cfg.get("project_id")
                    if "base_url" in cfg:
                        self.base_url = cfg["base_url"].rstrip("/")
            except Exception as e:
                logger.warning(f"Could not load config file {config_path}: {e}")

        if not self.api_key or not self.project_id:
            raise ValueError("Both 'api_key' and 'project_id' are required to connect to Fluxbase.")

        self.execute_url = f"{self.base_url}/api/execute-sql"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """
        Execute an arbitrary SQL query (DDL or DML) on the Fluxbase database.
        
        Args:
            sql_query: Valid SQL string.
            
        Returns:
            Dictionary containing 'success', 'rows', 'columns', 'rowCount', 'executionInfo'.
        """
        clean_q = sql_query.strip()
        if not clean_q.startswith("/*"):
            clean_q = f"/* edge_nonce={time.time_ns()} */ " + clean_q
        payload = {
            "projectId": self.project_id,
            "query": clean_q
        }

        try:
            response = requests.post(
                self.execute_url,
                json=payload,
                headers=self.headers,
                timeout=15
            )

            if response.status_code != 200:
                logger.error(f"Fluxbase HTTP Error {response.status_code}: {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "rows": []
                }

            data = response.json()
            if not data.get("success", False):
                err_msg = data.get("error", "Unknown SQL Error")
                logger.error(f"Fluxbase SQL Execution Error: {err_msg}")
                return {
                    "success": False,
                    "error": str(err_msg),
                    "rows": []
                }

            result = data.get("result", {})
            return {
                "success": True,
                "rows": result.get("rows", []),
                "columns": result.get("columns", []),
                "rowCount": result.get("rowCount", len(result.get("rows", []))),
                "message": result.get("message", ""),
                "executionInfo": data.get("executionInfo", {})
            }

        except Exception as e:
            logger.error(f"Exception communicating with Fluxbase: {e}")
            return {
                "success": False,
                "error": str(e),
                "rows": []
            }

    # =========================================================================
    # SCHEMA INITIALIZATION (FACULTY & STUDENTS TABLES)
    # =========================================================================

    def init_schema(self) -> Dict[str, Any]:
        """
        Initialize relational PostgreSQL tables for Faculty, Students, and Advising Logs.
        Executes each DDL statement individually as required by Fluxbase security policy.
        """
        statements = [
            """
            CREATE TABLE IF NOT EXISTS faculty (
                faculty_id VARCHAR(32) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                department VARCHAR(128) NOT NULL,
                designation VARCHAR(128) NOT NULL,
                phone VARCHAR(32),
                specialization VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS students (
                srn VARCHAR(32) PRIMARY KEY,
                student_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                program VARCHAR(128) NOT NULL,
                semester INT NOT NULL,
                section VARCHAR(8) NOT NULL,
                assigned_advisor_id VARCHAR(32) REFERENCES faculty(faculty_id) ON DELETE SET NULL,
                risk_level VARCHAR(32) DEFAULT 'LOW',
                dropout_probability FLOAT DEFAULT 0.0,
                curricular_units_approved INT DEFAULT 0,
                attendance_rate FLOAT DEFAULT 85.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS academic_advising_logs (
                log_id SERIAL PRIMARY KEY,
                srn VARCHAR(32) REFERENCES students(srn) ON DELETE CASCADE,
                faculty_id VARCHAR(32) REFERENCES faculty(faculty_id) ON DELETE SET NULL,
                intervention_type VARCHAR(128) NOT NULL,
                notes TEXT NOT NULL,
                status VARCHAR(32) DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]

        logger.info("Initializing Fluxbase database schema for Faculty & Students...")
        results = []
        for stmt in statements:
            res = self.execute_query(stmt)
            results.append(res)
            if not res.get("success"):
                return res

        return {"success": True, "details": results}

    # =========================================================================
    # SEEDING ACADEMIC RECORDS
    # =========================================================================

    def seed_academic_data(self) -> Dict[str, Any]:
        """
        Seed initial records for REVA University faculty and student cohorts.
        Executes each insertion statement individually.
        """
        statements = [
            """
            INSERT INTO faculty (faculty_id, name, email, department, designation, phone, specialization)
            VALUES 
                ('FAC_AIML_01', 'Dr. Ramesh Kumar', 'ramesh.kumar@reva.edu.in', 'School of CIT', 'Professor & HoD', '+91 98450 11223', 'Machine Learning & Deep Learning'),
                ('FAC_AIML_02', 'Prof. Ananya Sharma', 'ananya.sharma@reva.edu.in', 'School of CIT', 'Associate Professor', '+91 98450 22334', 'Natural Language Processing & RAG'),
                ('FAC_AIML_03', 'Dr. Rajesh V', 'rajesh.v@reva.edu.in', 'School of CIT', 'Senior Advisor & Mentor', '+91 98450 33445', 'Educational Data Mining & XAI')
            ON CONFLICT (faculty_id) DO UPDATE SET 
                name = EXCLUDED.name,
                designation = EXCLUDED.designation;
            """,
            """
            INSERT INTO students (srn, student_name, email, program, semester, section, assigned_advisor_id, risk_level, dropout_probability, curricular_units_approved, attendance_rate)
            VALUES 
                ('R24EA807', 'Sumith U', 'sumith.u@reva.edu.in', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_01', 'LOW', 0.042, 12, 94.5),
                ('R24EA801', 'Aarav Sharma', 'aarav.s@reva.edu.in', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_02', 'LOW', 0.081, 11, 91.0),
                ('R24EA842', 'Priya Nair', 'priya.n@reva.edu.in', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_02', 'MEDIUM', 0.425, 7, 72.0),
                ('R24EA818', 'Rohan Verma', 'rohan.v@reva.edu.in', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_03', 'HIGH', 0.785, 2, 58.5),
                ('R24EA895', 'Sneha Patel', 'sneha.p@reva.edu.in', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_03', 'HIGH', 0.842, 1, 51.0)
            ON CONFLICT (srn) DO UPDATE SET 
                risk_level = EXCLUDED.risk_level,
                dropout_probability = EXCLUDED.dropout_probability,
                curricular_units_approved = EXCLUDED.curricular_units_approved,
                attendance_rate = EXCLUDED.attendance_rate;
            """,
            """
            INSERT INTO academic_advising_logs (srn, faculty_id, intervention_type, notes, status)
            VALUES 
                ('R24EA818', 'FAC_AIML_03', 'Prerequisite Remediation', 'Student struggling with multivariable calculus. Assigned PACD-RAG Chain Rule micro-drills.', 'In-Progress'),
                ('R24EA895', 'FAC_AIML_03', 'Attendance & Fee Advisory', 'Counseling meeting scheduled regarding fee clearance and missed laboratory sessions.', 'Open');
            """
        ]

        logger.info("Seeding faculty and student cohorts into Fluxbase...")
        results = []
        for stmt in statements:
            res = self.execute_query(stmt)
            results.append(res)
            if not res.get("success"):
                return res

        return {"success": True, "details": results}

    # =========================================================================
    # HIGH-LEVEL DATA ACCESS METHODS
    # =========================================================================

    def get_students(self, risk_filter: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve students from Fluxbase, optionally filtered by risk level.
        """
        if risk_filter:
            sql = f"""
            SELECT s.*, f.name as advisor_name 
            FROM students s
            LEFT JOIN faculty f ON s.assigned_advisor_id = f.faculty_id
            WHERE s.risk_level = '{risk_filter.upper()}'
            ORDER BY s.dropout_probability DESC
            LIMIT {limit};
            """
        else:
            sql = f"""
            SELECT s.*, f.name as advisor_name 
            FROM students s
            LEFT JOIN faculty f ON s.assigned_advisor_id = f.faculty_id
            ORDER BY s.dropout_probability DESC
            LIMIT {limit};
            """
        res = self.execute_query(sql)
        return res.get("rows", [])

    def get_student_by_srn(self, srn: str) -> Optional[Dict[str, Any]]:
        """Retrieve single student record by institutional SRN."""
        alias_map = {
            "STU-807": "R24EA807",
            "STU-818": "R24EA818",
            "STU-842": "R24EA842",
            "STU-801": "R24EA801",
            "STU-895": "R24EA895"
        }
        resolved = alias_map.get(srn, srn)
        sql = f"""
        SELECT s.*, f.name as advisor_name, f.email as advisor_email
        FROM students s
        LEFT JOIN faculty f ON s.assigned_advisor_id = f.faculty_id
        WHERE s.srn = '{resolved}';
        """
        res = self.execute_query(sql)
        rows = res.get("rows", [])
        return rows[0] if rows else None

    def get_faculty_list(self) -> List[Dict[str, Any]]:
        """Retrieve all registered faculty members and academic mentors."""
        sql = """
        SELECT f.*, COUNT(s.srn) as assigned_mentees_count
        FROM faculty f
        LEFT JOIN students s ON f.faculty_id = s.assigned_advisor_id
        GROUP BY f.faculty_id, f.name, f.email, f.department, f.designation, f.phone, f.specialization, f.created_at
        ORDER BY f.faculty_id ASC;
        """
        res = self.execute_query(sql)
        return res.get("rows", [])

    def log_faculty_intervention(
        self,
        srn: str,
        faculty_id: str,
        intervention_type: str,
        notes: str,
        status: str = "Open"
    ) -> Dict[str, Any]:
        """Record an official faculty advising or remedial intervention note."""
        # Sanitize single quotes in notes
        clean_notes = notes.replace("'", "''")
        sql = f"""
        INSERT INTO academic_advising_logs (srn, faculty_id, intervention_type, notes, status)
        VALUES ('{srn}', '{faculty_id}', '{intervention_type}', '{clean_notes}', '{status}')
        RETURNING log_id, created_at;
        """
        return self.execute_query(sql)

    def get_advising_history(self, srn: str) -> List[Dict[str, Any]]:
        """Retrieve all advising history and counseling notes for a student."""
        sql = f"""
        SELECT l.*, f.name as faculty_name, f.designation as faculty_designation
        FROM academic_advising_logs l
        LEFT JOIN faculty f ON l.faculty_id = f.faculty_id
        WHERE l.srn = '{srn}'
        ORDER BY l.created_at DESC;
        """
        res = self.execute_query(sql)
        return res.get("rows", [])


# Standalone CLI execution demonstration
if __name__ == "__main__":
    print("\n" + "=" * 75)
    print("  FLUXBASE CLOUD DATABASE (FLUXBASEDB.ME) INITIALIZATION")
    print("  Cloud Relational Store for Faculty, Students, & Advising Logs")
    print("=" * 75)

    client = FluxbaseClient()
    print(f"1. Connected to Fluxbase Project: {client.project_id}")

    print("\n2. Initializing Database Schema (faculty, students, advising logs)...")
    schema_res = client.init_schema()
    print(f"   * Schema Setup Status: {'SUCCESS' if schema_res.get('success') else 'FAILED'}")

    print("\n3. Seeding Initial REVA Academic Cohort...")
    seed_res = client.seed_academic_data()
    print(f"   * Seeding Status: {'SUCCESS' if seed_res.get('success') else 'FAILED'}")

    print("\n4. Querying Faculty Members from Fluxbase:")
    faculty_list = client.get_faculty_list()
    for fac in faculty_list:
        print(f"   * [{fac['faculty_id']}] {fac['name']} - {fac['designation']} ({fac['specialization']})")

    print("\n5. Querying Student Cohort from Fluxbase:")
    students = client.get_students()
    for s in students:
        prob_pct = round(s['dropout_probability'] * 100, 1)
        print(f"   * [{s['srn']}] {s['student_name']} - Risk: {s['risk_level']} ({prob_pct}% dropout risk) | Advisor: {s.get('advisor_name')}")

    print("\n" + "=" * 75)
    print("  FLUXBASE CLOUD DATABASE READY AND FULLY OPERATIONAL.")
    print("=" * 75 + "\n")
