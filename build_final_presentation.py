import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

TEMPLATE_PATH = r"C:\Users\sumit\Downloads\Project_Presentation_Template.pptx"
OUTPUT_PATH = r"C:\Users\sumit\Downloads\Project_Presentation_PACD_RAG_Final.pptx"
REVA_LOGO = r"C:\Users\sumit\Downloads\rio\assets\reva_logo.png"
SDG_LOGO = r"C:\Users\sumit\Downloads\rio\assets\sdg4_logo.png"
ARTIFACT_DIR = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

def get_art(name):
    p = os.path.join(ARTIFACT_DIR, name)
    return p if os.path.exists(p) else None

def set_font(run, name="Calibri", size_pt=12, bold=False, color=(0,0,0)):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color)

def build_presentation():
    prs = Presentation(TEMPLATE_PATH)
    cand_header = "Project Presentation  |  Sumith U (R24EA807) & Shreehari (R23EA116)"

    # =========================================================================
    # SLIDE 1: Title
    # =========================================================================
    s1 = prs.slides[0]
    for shape in s1.shapes:
        if shape.name == "Text 2":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "PACD-RAG: Prerequisite-Aware Contextual Diagnostic & Retrieval-Augmented Generation for Student Academic Success"
            set_font(p.runs[0], "Calibri", 26, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 3":
            shape.text_frame.clear()
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "Sumith U (R24EA807) & Shreehari (R23EA116)  |  B.Tech AIML (7th Sem, Section B)"
            set_font(p1.runs[0], "Calibri", 14, bold=True, color=(30, 41, 59))
            
            p2 = shape.text_frame.add_paragraph()
            p2.text = "Faculty Guide: Dr Sailaja Thota, Associate Professor, AIML   Phase-1 (70% complete)"
            set_font(p2.runs[0], "Calibri", 13, bold=False, color=(71, 85, 105))

            p3 = shape.text_frame.add_paragraph()
            p3.text = "REVA University  |  RIO Review  |  November 2026  |  UN SDG 4: Quality Education"
            set_font(p3.runs[0], "Calibri", 12, bold=False, color=(100, 116, 139))
    
    # Add REVA Logo and SDG 4 Logo to Slide 1
    if os.path.exists(REVA_LOGO):
        s1.shapes.add_picture(REVA_LOGO, Inches(10.8), Inches(0.4), width=Inches(1.0), height=Inches(1.0))
    if os.path.exists(SDG_LOGO):
        s1.shapes.add_picture(SDG_LOGO, Inches(12.0), Inches(0.4), width=Inches(1.0), height=Inches(1.0))

    # =========================================================================
    # SLIDE 2: Problem Statement and Literature Gaps
    # =========================================================================
    s2 = prs.slides[1]
    for shape in s2.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = cand_header
            set_font(p.runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name == "Text 7":
            shape.text_frame.clear()
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "The Problem: Modern engineering institutions face high academic underperformance and course dropouts due to delayed, post-exam identification of foundational learning gaps without actionable prerequisite remediation."
            set_font(p1.runs[0], "Calibri", 12, color=(15, 23, 42))

            p2 = shape.text_frame.add_paragraph()
            p2.text = "Who Uses It: Faculty academic advisors managing 1,400+ student cohorts and students struggling with mathematical and architectural concepts across Units 1 to 4."
            set_font(p2.runs[0], "Calibri", 12, color=(15, 23, 42))

            p3 = shape.text_frame.add_paragraph()
            p3.text = "Measurable Success: Proactive 4.2-week advance warning lead-time, 88.3% Composite RAG quality (Grade A), and 100% prerequisite gap resolution."
            set_font(p3.runs[0], "Calibri", 12, bold=True, color=(16, 185, 129))
        elif shape.name == "Text 10":
            shape.text_frame.clear()
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "Gap 1 (Diagnostic): Existing LMS systems provide only coarse, retrospective aggregate marks without question-level diagnostic root-cause breakdown."
            set_font(p1.runs[0], "Calibri", 12, color=(15, 23, 42))

            p2 = shape.text_frame.add_paragraph()
            p2.text = "Gap 2 (Pedagogical): Conventional Vector RAG dumps advanced solutions without verifying mastery of upstream DAG prerequisites, causing student frustration."
            set_font(p2.runs[0], "Calibri", 12, color=(15, 23, 42))

            p3 = shape.text_frame.add_paragraph()
            p3.text = "Our Module's Solution: Bridges predictive risk with a 68-concept OKF Ontological Graph and Hybrid BM25+ChromaDB retrieval to isolate root blockers and scaffold 5-day remedial plans."
            set_font(p3.runs[0], "Calibri", 12, bold=True, color=(30, 58, 138))

    # =========================================================================
    # SLIDE 3: Literature Survey Table
    # =========================================================================
    s3 = prs.slides[2]
    for shape in s3.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.has_table:
            t = shape.table
            rows_data = [
                ["Paper (author, year)", "Approach", "Strength", "Limitation"],
                ["Baker & Inventado (2022)\nLAK Conference", "Bayesian Knowledge Tracing (BKT) on sequential quizzes", "Probabilistic latent skill mastery modeling over time", "Binary right/wrong data only; no multi-step root-cause diagnostics"],
                ["Al-Radaideh et al. (2022)\nPeerJ CS", "Multi-model ensemble (RF + SVM + Decision Trees)", "Robust accuracy across student demographic cohorts (88.5%)", "Coarse midterm features; lacks question-level prerequisite reasoning"],
                ["Ncube et al. (2023)\nEduc. Inf. Technol.", "Gradient boosting early-warning risk detector (CatBoost)", "Identifies at-risk candidates 3.5 weeks prior to final exams", "Predictive classification only; offers no automated pedagogical remediation"],
                ["PACD-RAG (Our Platform)\nPhase-1 Implementation", "Hybrid RAG (BM25 + ChromaDB) + 68-node OKF DAG Ontology", "4.2-week lead-time (tau=0.42), 88.3% RAGAS score, 100% prerequisite coverage", "Full syllabus validation; ongoing Phase-2 LMS webhook integration"]
            ]
            for r_idx, row in enumerate(rows_data):
                for c_idx, val in enumerate(row):
                    cell = t.cell(r_idx, c_idx)
                    cell.text = val
                    for p in cell.text_frame.paragraphs:
                        for run in p.runs:
                            is_hdr = (r_idx == 0)
                            set_font(run, "Calibri", 9.5 if not is_hdr else 10.5, bold=is_hdr, color=(0,0,0) if is_hdr else (30,41,59))

    # =========================================================================
    # SLIDE 4: Requirements
    # =========================================================================
    s4 = prs.slides[3]
    for shape in s4.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.has_table:
            t = shape.table
            req_data = [
                ["ID", "Requirement Specification", "Type", "Priority"],
                ["R1", "Multi-Model Risk Engine: Calibrated CatBoost+XGBoost+RF ensemble with tau=0.42 decision threshold for 4.2-week advance warning.", "Functional", "High"],
                ["R2", "Ontological Knowledge Framework (OKF): 68-concept DAG with Kahn's acyclicity validation and recursive Prerequisite Gap Scoring (PGS).", "Functional", "High"],
                ["R3", "Hybrid PACD-RAG Retrieval: Okapi BM25 sparse keyword ranker fused with ChromaDB dense cosine vector store via RRF (k=60).", "Functional", "High"],
                ["R4", "Batch IA Marks Ingestion & Remediation: Instructor section-marks CSV pipeline generating 5-day remedial plans with slide citations.", "Functional", "High"]
            ]
            for r_idx, row in enumerate(req_data):
                for c_idx, val in enumerate(row):
                    cell = t.cell(r_idx, c_idx)
                    cell.text = val
                    for p in cell.text_frame.paragraphs:
                        for run in p.runs:
                            is_hdr = (r_idx == 0)
                            set_font(run, "Calibri", 10 if not is_hdr else 11, bold=is_hdr, color=(0,0,0) if is_hdr else (30,41,59))

    # =========================================================================
    # SLIDE 5: System Design
    # =========================================================================
    s5 = prs.slides[4]
    for shape in s5.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name == "Text 6":
            shape.text_frame.clear() # clear placeholder
        elif shape.name == "Text 8":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Architecture Design Decisions"
            set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 9":
            shape.text_frame.clear()
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "Key Choice 1: Hybrid BM25 + ChromaDB RAG (RRF k=60)"
            set_font(p1.runs[0], "Calibri", 11, bold=True, color=(30, 58, 138))
            p1_b = shape.text_frame.add_paragraph()
            p1_b.text = "• Rejected: Pure dense vector search, which overlooks mathematical operators (dJ/da) and exact slide IDs.\n• Selected: Okapi BM25 sparse ranker ensures exact symbol retention; ChromaDB captures semantic context. Yields 95.0% Context Precision."
            set_font(p1_b.runs[0], "Calibri", 10, color=(51, 65, 85))

            p2 = shape.text_frame.add_paragraph()
            p2.text = "Key Choice 2: 68-Concept OKF Ontological DAG"
            set_font(p2.runs[0], "Calibri", 11, bold=True, color=(30, 58, 138))
            p2_b = shape.text_frame.add_paragraph()
            p2_b.text = "• Rejected: Flat vector search dumping advanced concepts on confused students.\n• Selected: Strict DAG traversal with depth-weighted Prerequisite Gap Scoring (PGS) identifying upstream foundational blockers."
            set_font(p2_b.runs[0], "Calibri", 10, color=(51, 65, 85))

    # Embed architecture screenshot on Slide 5
    img_arch = get_art("ui_fixed_student_dashboard_top.png")
    if img_arch:
        s5.shapes.add_picture(img_arch, Inches(0.85), Inches(1.75), width=Inches(7.3), height=Inches(4.5))

    # =========================================================================
    # SLIDE 6: Detailed Design
    # =========================================================================
    s6 = prs.slides[5]
    for shape in s6.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name in ["Text 6", "Text 8", "Text 10"]:
            shape.text_frame.clear()
        elif shape.name == "Text 11":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Design Traceability: Ingestion (R4) -> Multi-Model Risk Engine (R1) -> DAG Deficit Traversal (R2) -> Hybrid RAG Scaffolding (R3) -> 5-Day Remedial Plan Delivery (R5) via Glassmorphism Portals (R6)."
            set_font(p.runs[0], "Calibri", 11, bold=True, color=(15, 23, 42))

    # Add 3 diagrams/figures to Slide 6
    img_d1 = get_art("verified_student_ia_diagnostics_table.png")
    img_d2 = get_art("verified_student_weak_topic_explanation_modal.png")
    img_d3 = get_art("verified_faculty_batch_ingestion_modal.png")
    if img_d1:
        s6.shapes.add_picture(img_d1, Inches(0.85), Inches(1.75), width=Inches(3.6), height=Inches(3.8))
    if img_d2:
        s6.shapes.add_picture(img_d2, Inches(4.75), Inches(1.75), width=Inches(3.6), height=Inches(3.8))
    if img_d3:
        s6.shapes.add_picture(img_d3, Inches(8.65), Inches(1.75), width=Inches(3.8), height=Inches(3.8))

    # =========================================================================
    # SLIDE 7: Implementation Progress
    # =========================================================================
    s7 = prs.slides[6]
    for shape in s7.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name == "Text 6":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "target about 30%  |  actual: 35%"
            set_font(p.runs[0], "Calibri", 12, bold=True, color=(16, 185, 129))
        elif shape.name == "Text 10":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "target about 55%  |  actual: 60%"
            set_font(p.runs[0], "Calibri", 12, bold=True, color=(16, 185, 129))
        elif shape.name == "Text 14":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "target about 70%  |  actual: 75%"
            set_font(p.runs[0], "Calibri", 12, bold=True, color=(16, 185, 129))
        elif shape.name == "Text 17":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Features Completed at Phase-1 (75% Complete):\n• Week 8: PostgreSQL database schema, RBAC authentication, specialist baseline/velocity/mastery risk models.\n• Week 10: 68-concept OKF DAG curriculum graph, Kahn's acyclicity validation, ChromaDB lecture vector indexing.\n• Week 14: Hybrid RRF RAG retrieval, RAGAS composite evaluation (88.3%), batch marks pipeline, and glassmorphism UI."
            set_font(p.runs[0], "Calibri", 11, color=(15, 23, 42))

    # =========================================================================
    # SLIDE 8: Key Features and Demo
    # =========================================================================
    s8 = prs.slides[7]
    for shape in s8.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name in ["Text 6", "Text 8", "Text 10"]:
            shape.text_frame.clear()
        elif shape.name == "Text 12":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "How We Built It"
            set_font(p.runs[0], "Calibri", 13, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 13":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "• Core files: hybrid_rag_service.py (BM25 + ChromaDB RRF), prerequisite_graph.py (depth-weighted PGS penalty), and academic_recovery_predictor.py (calibrated ensemble)."
            set_font(p.runs[0], "Calibri", 11, color=(51, 65, 85))
        elif shape.name == "Text 15":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Key Optimization"
            set_font(p.runs[0], "Calibri", 13, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 16":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Expanded context excerpt slicing from 400 to 1,200 chars to retain complete mathematical derivations, raising Context Recall to 95.0% and composite RAG score to 88.3%."
            set_font(p.runs[0], "Calibri", 11, color=(51, 65, 85))

    # Embed 3 demo screenshots
    if img_d1:
        s8.shapes.add_picture(img_d1, Inches(0.85), Inches(1.6), width=Inches(3.6), height=Inches(3.5))
    if img_d2:
        s8.shapes.add_picture(img_d2, Inches(4.75), Inches(1.6), width=Inches(3.6), height=Inches(3.5))
    if img_d3:
        s8.shapes.add_picture(img_d3, Inches(8.65), Inches(1.6), width=Inches(3.8), height=Inches(3.5))

    # =========================================================================
    # SLIDE 9: Testing & RAGAS Benchmarks
    # =========================================================================
    s9 = prs.slides[8]
    for shape in s9.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name == "Text 6":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "42"
            set_font(p.runs[0], "Calibri", 28, bold=True, color=(30, 58, 138))
        elif shape.name == "Text 7":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "testcases designed"
            set_font(p.runs[0], "Calibri", 12, color=(71, 85, 105))
        elif shape.name == "Text 9":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "42"
            set_font(p.runs[0], "Calibri", 28, bold=True, color=(16, 185, 129))
        elif shape.name == "Text 10":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "passed (100%)"
            set_font(p.runs[0], "Calibri", 12, color=(71, 85, 105))
        elif shape.name == "Text 12":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "0"
            set_font(p.runs[0], "Calibri", 28, bold=True, color=(239, 68, 68))
        elif shape.name == "Text 13":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "failed / fixed"
            set_font(p.runs[0], "Calibri", 12, color=(71, 85, 105))
        elif shape.has_table:
            t = shape.table
            bench_data = [
                ["RAGAS Metric / Test ID", "Evaluation Scope", "Threshold / Expected", "Achieved Score", "Result"],
                ["Composite Quality Score", "End-to-end RAG remedial synthesis quality", "> 80.0% (Grade A)", "88.3% [Grade A]", "PASS"],
                ["Prerequisite Coverage", "Scaffolding of upstream parent DAG concepts", "> 90.0%", "100.0%", "PASS"],
                ["Context Precision & Recall", "Lecture slide chunk relevance & citation match", "> 85.0%", "95.0% / 95.0%", "PASS"]
            ]
            for r_idx, row in enumerate(bench_data):
                for c_idx, val in enumerate(row):
                    cell = t.cell(r_idx, c_idx)
                    cell.text = val
                    for p in cell.text_frame.paragraphs:
                        for run in p.runs:
                            is_hdr = (r_idx == 0)
                            set_font(run, "Calibri", 10 if not is_hdr else 11, bold=is_hdr, color=(0,0,0) if is_hdr else (30,41,59))

    # =========================================================================
    # SLIDE 10: Debugging and Integration
    # =========================================================================
    s10 = prs.slides[9]
    for shape in s10.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name in ["Text 6", "Text 8"]:
            shape.text_frame.clear()
        elif shape.name == "Text 10":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Root Cause and Fix"
            set_font(p.runs[0], "Calibri", 13, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 11":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "• Symptom: Partial mathematical formula rendering and slide citation loss.\n• Root Cause: 400-char context excerpt slicing truncated LaTeX equations before outcomes.\n• Fix: Extended slicing to 1,200 chars and built standalone pure-Python OkapiBM25 ranker."
            set_font(p.runs[0], "Calibri", 10.5, color=(51, 65, 85))
        elif shape.name == "Text 13":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Module-1 + Module-2 Integration"
            set_font(p.runs[0], "Calibri", 13, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 14":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "• Connection: Module-1 predictive risk engine feeds question-level IA deficit concept IDs directly into Module-2 OKF DAG traversal.\n• Integration Bug: Foreign key constraints on student_marks table during repeated section CSV ingestion attempts.\n• Resolution: Implemented ON CONFLICT DO UPDATE upsert handlers and cached prerequisite topological sorts."
            set_font(p.runs[0], "Calibri", 10.5, color=(51, 65, 85))

    # Embed Before & After screenshots
    img_before = get_art("ui_fixed_index_login.png")
    img_after = get_art("verified_faculty_batch_ingestion_executed.png")
    if img_before:
        s10.shapes.add_picture(img_before, Inches(0.85), Inches(1.6), width=Inches(2.7), height=Inches(2.2))
    if img_after:
        s10.shapes.add_picture(img_after, Inches(3.75), Inches(1.6), width=Inches(2.7), height=Inches(2.2))

    # =========================================================================
    # SLIDE 11: My Contribution and Phase-2 Plan
    # =========================================================================
    s11 = prs.slides[10]
    for shape in s11.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name == "Text 6":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Candidate Contributions Breakdown"
            set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 7":
            shape.text_frame.clear()
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "Sumith U (R24EA807):"
            set_font(p1.runs[0], "Calibri", 11.5, bold=True, color=(30, 58, 138))
            p1_b = shape.text_frame.add_paragraph()
            p1_b.text = "• Weeks 1–4: Multi-model predictive risk architecture (CatBoost, XGBoost, RF ensemble with tau=0.42 calibration).\n• Weeks 5–8: Batch IA question marks ingestion pipeline and PostgreSQL relational schema design.\n• Weeks 9–14: Hybrid RAG engine (Okapi BM25 + ChromaDB RRF), RAGAS evaluation suite, and GitHub CI deployment."
            set_font(p1_b.runs[0], "Calibri", 10, color=(51, 65, 85))

            p2 = shape.text_frame.add_paragraph()
            p2.text = "Shreehari (R23EA116):"
            set_font(p2.runs[0], "Calibri", 11.5, bold=True, color=(30, 58, 138))
            p2_b = shape.text_frame.add_paragraph()
            p2_b.text = "• Weeks 1–4: Comprehensive literature survey on learning analytics and educational recommender systems.\n• Weeks 5–8: 68-concept OKF Ontological Graph schema across Units 1–4 with Kahn's DAG acyclicity validation.\n• Weeks 9–14: Curriculum lecture material vectorization in ChromaDB and high-contrast glassmorphism student/faculty UI."
            set_font(p2_b.runs[0], "Calibri", 10, color=(51, 65, 85))
        elif shape.has_table:
            t = shape.table
            p2_data = [
                ["Pending Work (Phase-2: ~25%)", "Technical Approach", "Target Week"],
                ["LMS Webhook Synchronization", "REST Webhooks + Kafka message queue for real-time grade events", "Week 16"],
                ["Local LLM Fine-Tuning", "Fine-tune LLaMA-3-8B-Instruct on STEM syllabus Q&A pairs with LoRA", "Week 18"],
                ["Cross-Platform Mobile App", "Flutter client for proactive mobile push alerts & remedial study cards", "Week 20"]
            ]
            for r_idx, row in enumerate(p2_data):
                for c_idx, val in enumerate(row):
                    cell = t.cell(r_idx, c_idx)
                    cell.text = val
                    for p in cell.text_frame.paragraphs:
                        for run in p.runs:
                            is_hdr = (r_idx == 0)
                            set_font(run, "Calibri", 9.5 if not is_hdr else 10.5, bold=is_hdr, color=(0,0,0) if is_hdr else (30,41,59))

    # =========================================================================
    # SLIDE 12: Learnings and Thank You
    # =========================================================================
    s12 = prs.slides[11]
    for shape in s12.shapes:
        if shape.name == "Text 4":
            shape.text_frame.clear()
            shape.text_frame.paragraphs[0].text = cand_header
            set_font(shape.text_frame.paragraphs[0].runs[0], "Calibri", 10, color=(100, 116, 139))
        elif shape.name == "Text 6":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Hardest Problem and Learnings"
            set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 7":
            shape.text_frame.clear()
            p1 = shape.text_frame.paragraphs[0]
            p1.text = "• Hardest Problem: Bridging discrete graph theory (DAG topological traversal) with continuous vector search without hallucinating syllabus slides or cognitive overloading students."
            set_font(p1.runs[0], "Calibri", 11, color=(51, 65, 85))

            p2 = shape.text_frame.add_paragraph()
            p2.text = "• What Worked: Ontology-conditioned query expansion—injecting upstream parent prerequisites directly into retrieval queries before fetching lecture slides."
            set_font(p2.runs[0], "Calibri", 11, color=(51, 65, 85))

            p3 = shape.text_frame.add_paragraph()
            p3.text = "• What We Would Do Differently: Implement asynchronous background vector embeddings during document upload rather than synchronous batch indexing."
            set_font(p3.runs[0], "Calibri", 11, color=(51, 65, 85))
        elif shape.name == "Text 8":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Thank You. Questions?"
            set_font(p.runs[0], "Calibri", 16, bold=True, color=(15, 23, 42))
        elif shape.name == "Text 9":
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "sumithsumith4567890@gmail.com  |  https://github.com/Sumith2104/rio.git"
            set_font(p.runs[0], "Calibri", 12, bold=True, color=(30, 58, 138))

    prs.save(OUTPUT_PATH)
    print(f"Presentation saved successfully: {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH):,} bytes)")

if __name__ == "__main__":
    build_presentation()
