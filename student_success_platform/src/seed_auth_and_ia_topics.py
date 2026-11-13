"""
Module: seed_auth_and_ia_topics.py
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Seeds:
  1. platform_users with bcrypt-hashed passwords.
  2. ia_question_scores with per-question marks and weak topic tags.
  3. Indexes syllabus topics into local ChromaDB.
"""

import bcrypt
import logging
from student_success_platform.src.fluxbase_client import FluxbaseClient
from student_success_platform.src.vector_db_manager import VectorDBManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def hash_pw(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def seed_users(client: FluxbaseClient):
    users = [
        ("USR_807", "sumith.u@reva.edu.in", hash_pw("password123"), "student", "R24EA807", "Sumith U", "AI & ML"),
        ("USR_842", "priya.n@reva.edu.in", hash_pw("password123"), "student", "R24EA842", "Priya Nair", "AI & ML"),
        ("USR_818", "vikram.p@reva.edu.in", hash_pw("password123"), "student", "R24EA818", "Vikram Patel", "AI & ML"),
        ("USR_FAC01", "ramesh.kumar@reva.edu.in", hash_pw("password123"), "faculty", "FAC_AIML_01", "Dr. Ramesh Kumar", "AI & ML"),
        ("USR_FAC02", "ananya.s@reva.edu.in", hash_pw("password123"), "faculty", "FAC_AIML_02", "Prof. Ananya Sharma", "AI & ML"),
        ("USR_FAC03", "rajesh.v@reva.edu.in", hash_pw("password123"), "faculty", "FAC_AIML_03", "Dr. Rajesh V", "AI & ML"),
        ("USR_ADMIN", "admin@reva.edu.in", hash_pw("admin123"), "admin", "ADMIN_REVA", "Campus Administrator", "Administration")
    ]

    for uid, email, hpw, role, ent_id, name, dept in users:
        sql = f"""
        INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department)
        VALUES ('{uid}', '{email}', '{hpw}', '{role}', '{ent_id}', '{name}', '{dept}')
        ON CONFLICT (email) DO UPDATE SET
            hashed_password = EXCLUDED.hashed_password,
            entity_id = EXCLUDED.entity_id,
            display_name = EXCLUDED.display_name;
        """
        client.execute_query(sql)
    logger.info("Successfully seeded platform users.")

def seed_ia_question_scores(client: FluxbaseClient):
    # Questions for AIML-401 IA-1:
    # Q1: Multivariable Calculus (Partial Derivatives) - max 10
    # Q2: Multivariate Chain Rule - max 10
    # Q3: Backpropagation & Computational Graphs - max 10
    scores = [
        # Student 1: Sumith U (R24EA807) - High Performance
        ("IA_807_Q1", "R24EA807", "AIML-401", 1, "Q1", "MATH_PARTIAL_DERIV", "Multivariable Calculus: Partial Derivatives", 9.5, 10.0, 95.0, False),
        ("IA_807_Q2", "R24EA807", "AIML-401", 1, "Q2", "MATH_CHAIN_RULE", "Multivariate Chain Rule & Graph Propagation", 10.0, 10.0, 100.0, False),
        ("IA_807_Q3", "R24EA807", "AIML-401", 1, "Q3", "DL_BACKPROP", "Reverse-Mode Autodiff & Backpropagation", 10.0, 10.0, 100.0, False),

        # Student 2: Vikram Patel (R24EA818) - Critical Learning Deficits in Chain Rule & Backprop
        ("IA_818_Q1", "R24EA818", "AIML-401", 1, "Q1", "MATH_PARTIAL_DERIV", "Multivariable Calculus: Partial Derivatives", 6.5, 10.0, 65.0, False),
        ("IA_818_Q2", "R24EA818", "AIML-401", 1, "Q2", "MATH_CHAIN_RULE", "Multivariate Chain Rule & Graph Propagation", 3.0, 10.0, 30.0, True),
        ("IA_818_Q3", "R24EA818", "AIML-401", 1, "Q3", "DL_BACKPROP", "Reverse-Mode Autodiff & Backpropagation", 3.5, 10.0, 35.0, True),

        # Student 3: Priya Nair (R24EA842) - Moderate Deficit in Backprop
        ("IA_842_Q1", "R24EA842", "AIML-401", 1, "Q1", "MATH_PARTIAL_DERIV", "Multivariable Calculus: Partial Derivatives", 8.0, 10.0, 80.0, False),
        ("IA_842_Q2", "R24EA842", "AIML-401", 1, "Q2", "MATH_CHAIN_RULE", "Multivariate Chain Rule & Graph Propagation", 6.5, 10.0, 65.0, False),
        ("IA_842_Q3", "R24EA842", "AIML-401", 1, "Q3", "DL_BACKPROP", "Reverse-Mode Autodiff & Backpropagation", 4.5, 10.0, 45.0, True),
    ]

    for sid, srn, cid, ia_no, qno, tid, ttitle, marks, max_m, pct, is_weak in scores:
        sql = f"""
        INSERT INTO ia_question_scores (score_id, student_srn, course_id, ia_number, question_no, topic_id, topic_title, marks_obtained, max_marks, score_percentage, is_weak)
        VALUES ('{sid}', '{srn}', '{cid}', {ia_no}, '{qno}', '{tid}', '{ttitle}', {marks}, {max_m}, {pct}, {str(is_weak).lower()})
        ON CONFLICT (score_id) DO UPDATE SET
            marks_obtained = EXCLUDED.marks_obtained,
            score_percentage = EXCLUDED.score_percentage,
            is_weak = EXCLUDED.is_weak;
        """
        client.execute_query(sql)
    logger.info("Successfully seeded IA question-level marks.")

def seed_chroma_syllabus_topics():
    try:
        vdb = VectorDBManager()
        collection = vdb.get_or_create_collection(VectorDBManager.COLLECTION_SYLLABUS)

        syllabus_topics = [
            {
                "id": "SYLL_AIML_401_U1_T1",
                "text": "Unit 1: Foundations of Optimization & Multivariable Calculus. Topics include Partial Derivatives, Directional Gradients, Hessian Matrices, and Taylor Series approximations for convex optimization in deep learning models.",
                "metadata": {"course_id": "AIML-401", "unit_no": 1, "topic_id": "MATH_PARTIAL_DERIV", "title": "Multivariable Calculus: Partial Derivatives"}
            },
            {
                "id": "SYLL_AIML_401_U1_T2",
                "text": "Unit 1: Multivariate Chain Rule & Computational Graphs. Topics include Scalar and vector chain rule expansions, Forward and Reverse accumulators, Directed computational graphs for neural layers, and intermediate gradient caching.",
                "metadata": {"course_id": "AIML-401", "unit_no": 1, "topic_id": "MATH_CHAIN_RULE", "title": "Multivariate Chain Rule & Graph Propagation"}
            },
            {
                "id": "SYLL_AIML_401_U2_T1",
                "text": "Unit 2: Deep Learning Optimization & Backpropagation Algorithms. Topics include Reverse-Mode Automatic Differentiation, gradient descent variants (SGD, Adam, RMSprop), Vanishing/Exploding Gradients, and weight initialization strategies (Xavier, He).",
                "metadata": {"course_id": "AIML-401", "unit_no": 2, "topic_id": "DL_BACKPROP", "title": "Reverse-Mode Autodiff & Backpropagation"}
            },
            {
                "id": "SYLL_AIML_401_U3_T1",
                "text": "Unit 3: Recurrent Architectures & Sequence Modeling. Topics include Recurrent Neural Networks (RNN), Backpropagation Through Time (BPTT), Spectral Radius of transition matrices, and LSTM/GRU gated memory cells.",
                "metadata": {"course_id": "AIML-401", "unit_no": 3, "topic_id": "DL_RNN_BPTT", "title": "Recurrent Sequences & BPTT"}
            }
        ]

        ids = [t["id"] for t in syllabus_topics]
        documents = [t["text"] for t in syllabus_topics]
        metadatas = [t["metadata"] for t in syllabus_topics]

        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        logger.info(f"Successfully indexed {len(syllabus_topics)} syllabus topics in ChromaDB.")
    except Exception as e:
        logger.error(f"Error seeding ChromaDB syllabus: {e}")

if __name__ == "__main__":
    client = FluxbaseClient()
    seed_users(client)
    seed_ia_question_scores(client)
    seed_chroma_syllabus_topics()

