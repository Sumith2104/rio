-- =============================================================================
-- SMART CAMPUS INTELLIGENCE & STUDENT SUCCESS PLATFORM
-- Institutional Database Initialization Schema (REVA University)
-- Author: Sumith U (SRN: R24EA807)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS smart_campus_db;
USE smart_campus_db;

-- 1. Courses & Curriculum Blueprints
CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(32) PRIMARY KEY,
    course_title VARCHAR(255) NOT NULL,
    department VARCHAR(128) NOT NULL,
    semester INT NOT NULL,
    academic_year VARCHAR(32) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Curriculum Concept Inventory (Mirrors Part 4 Concept Graph)
CREATE TABLE IF NOT EXISTS concepts (
    concept_id VARCHAR(64) PRIMARY KEY,
    course_id VARCHAR(32) NOT NULL,
    concept_name VARCHAR(255) NOT NULL,
    unit_module VARCHAR(128) NOT NULL,
    difficulty_level VARCHAR(32) NOT NULL,
    description TEXT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- 3. Question Bank for Adaptive Remediation Drills
CREATE TABLE IF NOT EXISTS question_bank (
    question_id VARCHAR(64) PRIMARY KEY,
    concept_id VARCHAR(64) NOT NULL,
    blooms_taxonomy VARCHAR(64) NOT NULL, -- Remember, Understand, Apply, Analyze, Evaluate
    question_text TEXT NOT NULL,
    correct_option VARCHAR(255) NOT NULL,
    distractor_1 VARCHAR(255) NOT NULL,
    distractor_2 VARCHAR(255) NOT NULL,
    distractor_3 VARCHAR(255) NOT NULL,
    explanation TEXT,
    difficulty FLOAT DEFAULT 0.5,
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id) ON DELETE CASCADE
);

-- 4. Student Profiles & Academic Standing
CREATE TABLE IF NOT EXISTS students (
    srn VARCHAR(32) PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    program VARCHAR(128) NOT NULL,
    semester INT NOT NULL,
    section VARCHAR(8) NOT NULL,
    risk_level VARCHAR(32) DEFAULT 'LOW', -- LOW, MEDIUM, HIGH
    dropout_probability FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Student Diagnostic Quiz & Formative Evidence
CREATE TABLE IF NOT EXISTS student_quiz_logs (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    srn VARCHAR(32) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    selected_option VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    response_time_seconds FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (srn) REFERENCES students(srn) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES question_bank(question_id) ON DELETE CASCADE
);

-- Seed Initial Course Blueprint
INSERT IGNORE INTO courses (course_id, course_title, department, semester, academic_year) VALUES
('AIML-401', 'Machine Learning & Deep Learning Intelligence Systems', 'School of Computing & Information Technology', 7, '2026-2027');

-- Seed Sumith U profile
INSERT IGNORE INTO students (srn, student_name, email, program, semester, section, risk_level, dropout_probability) VALUES
('R24EA807', 'Sumith U', 'sumith.u@reva.edu.in', 'B.Tech CSE (AI & ML)', 7, 'B', 'LOW', 0.04);

