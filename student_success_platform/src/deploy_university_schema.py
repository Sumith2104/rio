"""
=============================================================================
UNIVERSITY-LEVEL DATABASE SCHEMA DEPLOYER (FLUXBASEDB.ME)
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
Deploys a comprehensive, relational university database schema on Fluxbase
PostgreSQL to support:
  - Academic hierarchy (Departments, Faculty, Courses, Enrolled Students)
  - Curriculum blueprints & Prerequisite DAG dependencies
  - Subject-scoped learning materials & lecture slide embeddings tracking
  - Student formative diagnostic marks & cognitive mastery
  - Faculty advising action logs & counseling interventions
=============================================================================
"""

import os
import sys
import logging

# Ensure src is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from fluxbase_client import FluxbaseClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def deploy_university_schema():
    """Execute DDL statements individually on Fluxbase AWS PostgreSQL."""
    client = FluxbaseClient()
    logger.info(f"Connecting to Fluxbase Project {client.project_id}...")

    # Ordered DDL statements ensuring foreign key validity
    ddl_statements = [
        # 1. Departments
        """
        CREATE TABLE IF NOT EXISTS departments (
            department_id VARCHAR(32) PRIMARY KEY,
            department_name VARCHAR(255) NOT NULL,
            school VARCHAR(255) NOT NULL,
            dean_name VARCHAR(128),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # 2. Faculty
        """
        CREATE TABLE IF NOT EXISTS faculty (
            faculty_id VARCHAR(32) PRIMARY KEY,
            department_id VARCHAR(32) REFERENCES departments(department_id) ON DELETE SET NULL,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            designation VARCHAR(128) NOT NULL,
            phone VARCHAR(32),
            specialization VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # 3. Courses / Subjects
        """
        CREATE TABLE IF NOT EXISTS courses (
            course_id VARCHAR(32) PRIMARY KEY,
            course_title VARCHAR(255) NOT NULL,
            department_id VARCHAR(32) REFERENCES departments(department_id) ON DELETE SET NULL,
            credits INT DEFAULT 4,
            semester INT NOT NULL,
            academic_year VARCHAR(32) DEFAULT '2026-2027',
            syllabus_overview TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # 4. Students
        """
        CREATE TABLE IF NOT EXISTS students (
            srn VARCHAR(32) PRIMARY KEY,
            student_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            department_id VARCHAR(32) REFERENCES departments(department_id) ON DELETE SET NULL,
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
        # 5. Course Enrollments & Assessment Vectors
        """
        CREATE TABLE IF NOT EXISTS course_enrollments (
            enrollment_id SERIAL PRIMARY KEY,
            srn VARCHAR(32) REFERENCES students(srn) ON DELETE CASCADE,
            course_id VARCHAR(32) REFERENCES courses(course_id) ON DELETE CASCADE,
            semester INT NOT NULL,
            ia1_score FLOAT DEFAULT 0.0,
            ia2_score FLOAT DEFAULT 0.0,
            assignment_score FLOAT DEFAULT 0.0,
            attendance_pct FLOAT DEFAULT 85.0,
            overall_grade VARCHAR(8) DEFAULT 'In-Progress',
            UNIQUE(srn, course_id, semester)
        );
        """,
        # 6. Curriculum Concept Catalog (Part 4 Link)
        """
        CREATE TABLE IF NOT EXISTS curriculum_concepts (
            concept_id VARCHAR(64) PRIMARY KEY,
            course_id VARCHAR(32) REFERENCES courses(course_id) ON DELETE CASCADE,
            unit_name VARCHAR(128) NOT NULL,
            concept_name VARCHAR(255) NOT NULL,
            difficulty_level VARCHAR(32) DEFAULT 'Intermediate',
            description TEXT
        );
        """,
        # 7. Concept Prerequisite Directed Dependencies (DAG)
        """
        CREATE TABLE IF NOT EXISTS concept_prerequisites (
            prereq_id SERIAL PRIMARY KEY,
            source_prereq_id VARCHAR(64) REFERENCES curriculum_concepts(concept_id) ON DELETE CASCADE,
            target_dependent_id VARCHAR(64) REFERENCES curriculum_concepts(concept_id) ON DELETE CASCADE,
            relationship_type VARCHAR(64) DEFAULT 'prerequisite',
            description TEXT,
            UNIQUE(source_prereq_id, target_dependent_id)
        );
        """,
        # 8. Learning Materials (Subject-Scoped RAG Source Documents)
        """
        CREATE TABLE IF NOT EXISTS learning_materials (
            material_id VARCHAR(64) PRIMARY KEY,
            course_id VARCHAR(32) REFERENCES courses(course_id) ON DELETE CASCADE,
            unit_name VARCHAR(128) NOT NULL,
            concept_id VARCHAR(64) REFERENCES curriculum_concepts(concept_id) ON DELETE SET NULL,
            material_type VARCHAR(64) NOT NULL, -- syllabus, lecture_notes, question_bank, lab_manual
            title VARCHAR(255) NOT NULL,
            content_text TEXT NOT NULL,
            file_name VARCHAR(255),
            uploaded_by_faculty_id VARCHAR(32) REFERENCES faculty(faculty_id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # 9. Student Formative Diagnostic Assessment Logs (Cognitive Diagnosis)
        """
        CREATE TABLE IF NOT EXISTS student_assessment_records (
            record_id SERIAL PRIMARY KEY,
            srn VARCHAR(32) REFERENCES students(srn) ON DELETE CASCADE,
            course_id VARCHAR(32) REFERENCES courses(course_id) ON DELETE CASCADE,
            concept_id VARCHAR(64) REFERENCES curriculum_concepts(concept_id) ON DELETE CASCADE,
            score FLOAT NOT NULL,
            is_needs_review BOOLEAN NOT NULL DEFAULT FALSE,
            attempt_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        # 10. Faculty Advising & Counseling Interventions
        """
        CREATE TABLE IF NOT EXISTS faculty_interventions (
            intervention_id SERIAL PRIMARY KEY,
            srn VARCHAR(32) REFERENCES students(srn) ON DELETE CASCADE,
            faculty_id VARCHAR(32) REFERENCES faculty(faculty_id) ON DELETE SET NULL,
            course_id VARCHAR(32) REFERENCES courses(course_id) ON DELETE SET NULL,
            intervention_type VARCHAR(128) NOT NULL,
            action_notes TEXT NOT NULL,
            status VARCHAR(32) DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]

    print("\n--- Deploying University Relational Schema to Fluxbase ---")
    for idx, stmt in enumerate(ddl_statements, 1):
        res = client.execute_query(stmt)
        if not res.get("success"):
            print(f"FAILED on statement {idx}: {res.get('error')}")
            return False
        print(f"  [OK] Table {idx}/10 verified.")

    print("\n--- Seeding University Academic Hierarchy ---")
    seed_statements = [
        # Seed Department
        """
        INSERT INTO departments (department_id, department_name, school, dean_name)
        VALUES ('DEPT_CIT', 'Computer Science & Artificial Intelligence', 'School of Computing & Information Technology', 'Dr. Mallikarjun M. Kodabagi')
        ON CONFLICT (department_id) DO NOTHING;
        """,
        # Seed Courses / Subjects
        """
        INSERT INTO courses (course_id, course_title, department_id, credits, semester, academic_year, syllabus_overview)
        VALUES 
            ('AIML-401', 'Machine Learning & Deep Learning Intelligence Systems', 'DEPT_CIT', 4, 7, '2026-2027', 'Foundations of multivariable calculus, optimization, deep feedforward networks, backpropagation, and XAI.'),
            ('AIML-402', 'Natural Language Processing & Large Language Models', 'DEPT_CIT', 4, 7, '2026-2027', 'Statistical NLP, sequence modeling, attention mechanisms, transformers, and Retrieval-Augmented Generation.')
        ON CONFLICT (course_id) DO NOTHING;
        """,
        # Seed Faculty
        """
        INSERT INTO faculty (faculty_id, department_id, department, name, email, designation, phone, specialization)
        VALUES 
            ('FAC_AIML_01', 'DEPT_CIT', 'School of CIT', 'Dr. Ramesh Kumar', 'ramesh.kumar@reva.edu.in', 'Professor & HoD', '+91 98450 11223', 'Machine Learning & Deep Neural Networks'),
            ('FAC_AIML_02', 'DEPT_CIT', 'School of CIT', 'Prof. Ananya Sharma', 'ananya.sharma@reva.edu.in', 'Associate Professor', '+91 98450 22334', 'Natural Language Processing & RAG'),
            ('FAC_AIML_03', 'DEPT_CIT', 'School of CIT', 'Dr. Rajesh V', 'rajesh.v@reva.edu.in', 'Senior Advisor & Mentor', '+91 98450 33445', 'Educational Data Mining & XAI')
        ON CONFLICT (faculty_id) DO UPDATE SET 
            department_id = EXCLUDED.department_id,
            name = EXCLUDED.name;
        """,
        # Seed Student Cohort
        """
        INSERT INTO students (srn, student_name, email, department_id, program, semester, section, assigned_advisor_id, risk_level, dropout_probability, curricular_units_approved, attendance_rate)
        VALUES 
            ('R24EA807', 'Sumith U', 'sumith.u@reva.edu.in', 'DEPT_CIT', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_01', 'LOW', 0.042, 12, 94.5),
            ('R24EA801', 'Aarav Sharma', 'aarav.s@reva.edu.in', 'DEPT_CIT', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_02', 'LOW', 0.081, 11, 91.0),
            ('R24EA842', 'Priya Nair', 'priya.n@reva.edu.in', 'DEPT_CIT', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_02', 'MEDIUM', 0.425, 7, 72.0),
            ('R24EA818', 'Rohan Verma', 'rohan.v@reva.edu.in', 'DEPT_CIT', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_03', 'HIGH', 0.785, 2, 58.5),
            ('R24EA895', 'Sneha Patel', 'sneha.p@reva.edu.in', 'DEPT_CIT', 'B.Tech in CSE (AI & ML)', 7, 'B', 'FAC_AIML_03', 'HIGH', 0.842, 1, 51.0)
        ON CONFLICT (srn) DO UPDATE SET 
            risk_level = EXCLUDED.risk_level,
            dropout_probability = EXCLUDED.dropout_probability;
        """,
        # Seed Enrollments
        """
        INSERT INTO course_enrollments (srn, course_id, semester, ia1_score, ia2_score, assignment_score, attendance_pct, overall_grade)
        VALUES 
            ('R24EA807', 'AIML-401', 7, 28.5, 29.0, 9.5, 95.0, 'A+'),
            ('R24EA801', 'AIML-401', 7, 26.0, 27.5, 9.0, 91.0, 'A'),
            ('R24EA842', 'AIML-401', 7, 19.0, 21.0, 7.5, 72.0, 'B'),
            ('R24EA818', 'AIML-401', 7, 12.0, 14.5, 5.0, 58.5, 'C'),
            ('R24EA895', 'AIML-401', 7, 9.0, 11.0, 4.0, 51.0, 'D')
        ON CONFLICT (srn, course_id, semester) DO NOTHING;
        """,
        # Seed Concepts from Part 4 Graph
        """
        INSERT INTO curriculum_concepts (concept_id, course_id, unit_name, concept_name, difficulty_level, description)
        VALUES 
            ('MATH_DERIV', 'AIML-401', 'Unit 1: Mathematical Foundations', 'Partial Derivatives', 'Foundational', 'Multivariable calculus, rate of change, and gradients.'),
            ('MATH_CHAIN_RULE', 'AIML-401', 'Unit 1: Mathematical Foundations', 'Chain Rule', 'Foundational', 'Derivative of composite functions for backward error propagation.'),
            ('ML_LOSS_FUNC', 'AIML-401', 'Unit 2: Classical Machine Learning', 'Loss Functions', 'Intermediate', 'MSE, Cross-Entropy Loss, and error objectives.'),
            ('ML_GRAD_DESC', 'AIML-401', 'Unit 2: Classical Machine Learning', 'Gradient Descent', 'Intermediate', 'Iterative weight updates along negative loss gradients.'),
            ('DL_BACKPROP', 'AIML-401', 'Unit 3: Deep Neural Networks', 'Backpropagation', 'Advanced', 'Layer-wise recursive gradient computation using chain rule.'),
            ('DL_NN_TRAIN', 'AIML-401', 'Unit 3: Deep Neural Networks', 'Neural Network Training', 'Advanced', 'End-to-end training loops: forward, loss, backward, step.')
        ON CONFLICT (concept_id) DO NOTHING;
        """,
        # Seed Prerequisite Edges from Part 4 Graph
        """
        INSERT INTO concept_prerequisites (source_prereq_id, target_dependent_id, relationship_type, description)
        VALUES 
            ('MATH_DERIV', 'MATH_CHAIN_RULE', 'prerequisite', 'Derivatives are required before applying chain rule to composites.'),
            ('MATH_CHAIN_RULE', 'DL_BACKPROP', 'prerequisite', 'Backpropagation is the recursive chain rule across neural layers.'),
            ('DL_BACKPROP', 'DL_NN_TRAIN', 'prerequisite', 'Training loops require backpropagation for gradient calculation.')
        ON CONFLICT (source_prereq_id, target_dependent_id) DO NOTHING;
        """,
        # Seed Initial Faculty Advising Intervention
        """
        INSERT INTO faculty_interventions (srn, faculty_id, course_id, intervention_type, action_notes, status)
        VALUES 
            ('R24EA818', 'FAC_AIML_03', 'AIML-401', 'PACD-RAG Calculus Remediation', 'Student diagnosed with prerequisite deficit in Chain Rule. Assigned targeted micro-drills.', 'In-Progress')
        ON CONFLICT DO NOTHING;
        """
    ]

    for idx, stmt in enumerate(seed_statements, 1):
        res = client.execute_query(stmt)
        if not res.get("success"):
            print(f"FAILED on seed {idx}: {res.get('error')}")
            return False
        print(f"  [OK] Academic seed batch {idx}/{len(seed_statements)} applied.")

    print("\n--- University Schema & Academic Data Successfully Deployed ---")
    return True


if __name__ == "__main__":
    deploy_university_schema()
