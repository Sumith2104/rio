"""
Module: deploy_system_design_tables.py
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Deploys tables required by smart-campus-system-design.pdf:
  1. users & auth (login credentials & roles)
  2. audit_logs (append-only log for login, view, export)
  3. data_change_log (audit trail for IA marks & attendance edits)
  4. ai_call_log (AWS AI / Bedrock prompt, tokens, latency, status)
  5. ia_question_scores (topic-level IA marks for weak topic detection)
  6. student_study_plans (RAG-generated remediation plans)
"""

import os
import json
import logging
from student_success_platform.src.fluxbase_client import FluxbaseClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def deploy_tables():
    client = FluxbaseClient()
    logger.info("Connected to Fluxbase Cloud PostgreSQL.")

    ddl_statements = [
        # 1. Users & Authentication table
        """
        CREATE TABLE IF NOT EXISTS platform_users (
            user_id VARCHAR(50) PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'faculty', 'admin')),
            entity_id VARCHAR(50) NOT NULL, -- SRN for student, faculty_id for faculty
            display_name VARCHAR(100) NOT NULL,
            department VARCHAR(50) DEFAULT 'AI & ML',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # 2. Audit logs (append-only)
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            log_id BIGSERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            actor_id VARCHAR(50) NOT NULL,
            actor_role VARCHAR(20) NOT NULL,
            action VARCHAR(50) NOT NULL, -- LOGIN_OK, LOGIN_FAIL, VIEW_STUDENT, UPLOAD_IA, RAG_QUERY, etc.
            resource VARCHAR(100),
            resource_id VARCHAR(100),
            ip_address VARCHAR(45) DEFAULT '127.0.0.1',
            status VARCHAR(20) DEFAULT 'SUCCESS',
            detail JSONB
        );
        """,

        # 3. Data Change Log (marks, attendance change history)
        """
        CREATE TABLE IF NOT EXISTS data_change_log (
            change_id BIGSERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            actor_id VARCHAR(50) NOT NULL,
            table_name VARCHAR(50) NOT NULL,
            record_id VARCHAR(50) NOT NULL,
            action_type VARCHAR(20) NOT NULL, -- INSERT, UPDATE, BATCH_INGEST
            old_values JSONB,
            new_values JSONB,
            change_reason TEXT
        );
        """,

        # 4. AI Call Log (AWS / Bedrock inference monitoring)
        """
        CREATE TABLE IF NOT EXISTS ai_call_log (
            call_id BIGSERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            actor_id VARCHAR(50),
            task_type VARCHAR(50) NOT NULL, -- RAG_SYLLABUS, WEAK_TOPIC_PLAN, CHAT
            model_id VARCHAR(100) NOT NULL,
            prompt_summary TEXT,
            input_tokens INT DEFAULT 0,
            output_tokens INT DEFAULT 0,
            latency_ms INT DEFAULT 0,
            status VARCHAR(20) DEFAULT 'SUCCESS'
        );
        """,

        # 5. Question-Level IA Marks & Weak Topic Tracking
        """
        CREATE TABLE IF NOT EXISTS ia_question_scores (
            score_id VARCHAR(50) PRIMARY KEY,
            student_srn VARCHAR(20) NOT NULL,
            course_id VARCHAR(20) NOT NULL,
            ia_number INT NOT NULL, -- 1 for IA-1, 2 for IA-2
            question_no VARCHAR(10) NOT NULL,
            topic_id VARCHAR(50) NOT NULL,
            topic_title VARCHAR(100) NOT NULL,
            marks_obtained NUMERIC(4,1) NOT NULL,
            max_marks NUMERIC(4,1) NOT NULL,
            score_percentage NUMERIC(5,2) NOT NULL,
            is_weak BOOLEAN NOT NULL, -- True if score_percentage < 50%
            evaluated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        """,

        # 6. RAG-Generated Weak Topic Remedial Study Plans
        """
        CREATE TABLE IF NOT EXISTS student_study_plans (
            plan_id VARCHAR(50) PRIMARY KEY,
            student_srn VARCHAR(20) NOT NULL,
            course_id VARCHAR(20) NOT NULL,
            weak_topics JSONB NOT NULL,
            retrieved_syllabus_citations JSONB NOT NULL,
            study_plan_text TEXT NOT NULL,
            tasks JSONB,
            generated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'ACTIVE'
        );
        """
    ]

    for sql in ddl_statements:
        try:
            res = client.execute_query(sql)
            logger.info(f"Executed DDL: {sql.split('(')[0].strip()} -> Success: {res.get('success', True)}")
        except Exception as e:
            logger.error(f"Error executing DDL: {e}")

if __name__ == "__main__":
    deploy_tables()

