import sys
import os
import bcrypt

sys.path.insert(0, 'student_success_platform/src')
from fluxbase_client import FluxbaseClient

db = FluxbaseClient()

pwd_hash = bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# 1. Insert into students first
sql_s = """
INSERT INTO students (srn, student_name, email, program, semester, section, attendance_rate, risk_level, dropout_probability, department_id)
VALUES ('R23EA116', 'Shreehari', 'shreehari@reva.edu.in', 'B.Tech AIML', 7, 'B', 93.0, 'LOW', 0.052, 'DEPT_AIML')
ON CONFLICT (srn) DO UPDATE SET student_name = EXCLUDED.student_name, email = EXCLUDED.email;
"""
res_s = db.execute_query(sql_s)
print("Student inserted/updated:", res_s.get("rowCount"))

# 2. Insert into platform_users
sql_u = f"""
INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department, is_active)
VALUES ('USR_R23EA116', 'shreehari@reva.edu.in', '{pwd_hash}', 'student', 'R23EA116', 'Shreehari', 'AIML', TRUE)
ON CONFLICT (email, role) DO UPDATE SET hashed_password = EXCLUDED.hashed_password, entity_id = EXCLUDED.entity_id;
"""
res_u = db.execute_query(sql_u)
print("Platform user inserted/updated:", res_u.get("rowCount"))

# 3. Insert into course_enrollments
sql_e = """
INSERT INTO course_enrollments (srn, course_id, semester, ia1_score, ia2_score, attendance_pct)
VALUES ('R23EA116', 'AIML-401', 7, 28.0, 28.5, 93.0)
ON CONFLICT (srn, course_id, semester) DO UPDATE SET ia1_score = EXCLUDED.ia1_score;
"""
res_e = db.execute_query(sql_e)
print("Course enrollment inserted/updated:", res_e.get("rowCount"))

# 4. Insert IA scores
db.execute_query("DELETE FROM ia_question_scores WHERE student_srn = 'R23EA116' AND course_id = 'AIML-401';")
scores = [
    ("SC_R23EA116_AIML-401_IA1_Q1", "R23EA116", "AIML-401", 1, "Q1", "MATH_PARTIAL_DERIV", "Multivariable Calculus: Partial Derivatives", 9.5, 10.0, 95.0, False),
    ("SC_R23EA116_AIML-401_IA1_Q2", "R23EA116", "AIML-401", 1, "Q2", "MATH_CHAIN_RULE", "Multivariate Chain Rule & Graph Propagation", 9.5, 10.0, 95.0, False),
    ("SC_R23EA116_AIML-401_IA1_Q3", "R23EA116", "AIML-401", 1, "Q3", "DL_BACKPROP", "Reverse-Mode Autodiff & Backpropagation", 9.0, 10.0, 90.0, False),
]
for sc_id, srn, cid, ia_n, q_no, tid, t_title, obt, max_m, pct, is_w in scores:
    sql_sc = f"""
    INSERT INTO ia_question_scores (score_id, student_srn, course_id, ia_number, question_no, topic_id, topic_title, marks_obtained, max_marks, score_percentage, is_weak)
    VALUES ('{sc_id}', '{srn}', '{cid}', {ia_n}, '{q_no}', '{tid}', '{t_title}', {obt}, {max_m}, {pct}, {'TRUE' if is_w else 'FALSE'});
    """
    db.execute_query(sql_sc)
print("Inserted Shreehari IA question scores successfully!")
