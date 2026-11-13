"""
Deploy Database Schema for Fully Agentic Smart Campus Platform
==============================================================
Creates tables for:
- assignments & student_assignments
- agent_execution_jobs
- student_attendance_logs
"""

import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from fluxbase_client import FluxbaseClient
import json

def deploy_agentic_schema():
    client = FluxbaseClient()
    print("Connecting to Fluxbase PostgreSQL...")

    # 1. assignments table
    print("Creating assignments table...")
    client.execute_query("""
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id VARCHAR(64) PRIMARY KEY,
            course_id VARCHAR(32) NOT NULL,
            faculty_id VARCHAR(32) NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            problem_statement TEXT,
            max_marks FLOAT DEFAULT 10.0,
            due_date VARCHAR(64),
            rubric JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. student_assignments table
    print("Creating student_assignments table...")
    client.execute_query("""
        CREATE TABLE IF NOT EXISTS student_assignments (
            id SERIAL PRIMARY KEY,
            assignment_id VARCHAR(64) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
            student_srn VARCHAR(32) NOT NULL,
            status VARCHAR(32) DEFAULT 'ASSIGNED',
            submission_text TEXT,
            marks_obtained FLOAT,
            feedback TEXT,
            submitted_at TIMESTAMP,
            graded_at TIMESTAMP
        );
    """)

    # 3. agent_execution_jobs table
    print("Creating agent_execution_jobs table...")
    client.execute_query("""
        CREATE TABLE IF NOT EXISTS agent_execution_jobs (
            job_id VARCHAR(64) PRIMARY KEY,
            faculty_id VARCHAR(32) NOT NULL,
            course_id VARCHAR(32) NOT NULL,
            original_filename TEXT NOT NULL,
            detected_type VARCHAR(64),
            status VARCHAR(32) DEFAULT 'PROCESSING',
            steps_log JSONB DEFAULT '[]'::jsonb,
            result_summary JSONB DEFAULT '{}'::jsonb,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        );
    """)

    # 4. student_attendance_logs table
    print("Creating student_attendance_logs table...")
    client.execute_query("""
        CREATE TABLE IF NOT EXISTS student_attendance_logs (
            id SERIAL PRIMARY KEY,
            student_srn VARCHAR(32) NOT NULL,
            course_id VARCHAR(32) NOT NULL,
            session_date VARCHAR(32) NOT NULL,
            status VARCHAR(16) DEFAULT 'PRESENT',
            recorded_by VARCHAR(32),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    print("Agentic schema deployment completed successfully!")

if __name__ == "__main__":
    deploy_agentic_schema()
