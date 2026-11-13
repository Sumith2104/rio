"""
build_internship_presentation.py
--------------------------------
Generates a publication-grade, 10-slide PowerPoint presentation for the
RIO Internship Review, strictly aligned with 'RIO Internship Report Template.docx':
- Slide 1: Title (REVA & SDG 4 logos, candidate credentials, Dr Sailaja Thota)
- Slide 2: Organization, Team & Module Overview (Section 1.1 & 1.2)
- Slide 3: Technology Stack Architecture Table (Section 1.3)
- Slide 4: Technical Fundamentals Progression Table (Section 2.1)
- Slide 5: Workplace Practices & Coding Standards (Section 3.1)
- Slide 6: Industry Tools & Infrastructure (Section 3.2)
- Slide 7: Guide Feedback & Architectural Pivots (Section 4.1 & 4.2)
- Slide 8: Mock Interviews & Placement Readiness (Section 5.1 & 5.2)
- Slide 9: Reflection & Capstone Showcase Plan (Section 5.3 & 5.4)
- Slide 10: Conclusion, Declaration & Acknowledgements
"""

import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PATH = r"C:\Users\sumit\Downloads\Internship_Presentation_Final.pptx"
REVA_LOGO = r"C:\Users\sumit\Downloads\rio\assets\reva_logo.png"
SDG_LOGO = r"C:\Users\sumit\Downloads\rio\assets\sdg4_logo.png"

def set_font(run, name="Calibri", size_pt=12, bold=False, italic=False, color=(0,0,0)):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(*color)

def add_header(slide, title_text, subtitle_text="RIO Internship Review — Phase-1 | Sumith U (R24EA807) & Shreehari (R23EA116)"):
    # Header bar
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = title_text
    set_font(p1.runs[0], "Calibri", 22, bold=True, color=(15, 23, 42))

    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    set_font(p2.runs[0], "Calibri", 10, bold=False, color=(100, 116, 139))

    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(203, 213, 225)
    line.line.color.rgb = RGBColor(203, 213, 225)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Logos
    if os.path.exists(REVA_LOGO):
        s1.shapes.add_picture(REVA_LOGO, Inches(0.8), Inches(0.6), width=Inches(1.2), height=Inches(1.2))
    if os.path.exists(SDG_LOGO):
        s1.shapes.add_picture(SDG_LOGO, Inches(11.3), Inches(0.6), width=Inches(1.2), height=Inches(1.2))

    # Title box
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "REVA University — School of Computing and Information Technology"
    set_font(p.runs[0], "Calibri", 14, bold=True, color=(71, 85, 105))

    p = tf1.add_paragraph()
    p.text = "Internship Report Presentation — Phase-1"
    set_font(p.runs[0], "Calibri", 28, bold=True, color=(15, 23, 42))

    p = tf1.add_paragraph()
    p.text = "REVA Internship Opportunities (RIO)  |  Smart Campus Intelligence & PACD-RAG Engine"
    set_font(p.runs[0], "Calibri", 16, bold=True, color=(30, 58, 138))

    p = tf1.add_paragraph()
    p.text = "\nCandidates: Sumith U (R24EA807) & Shreehari (R23EA116)  |  7th Sem B.Tech AIML (Section B)"
    set_font(p.runs[0], "Calibri", 13, bold=True, color=(30, 41, 59))

    p = tf1.add_paragraph()
    p.text = "Faculty Guide & Workplace Mentor: Dr Sailaja Thota, Associate Professor, Department of AIML"
    set_font(p.runs[0], "Calibri", 12, bold=False, color=(71, 85, 105))

    p = tf1.add_paragraph()
    p.text = "Review Date: 14 November 2026  |  UN SDG 4: Quality Education (Target 4.4 & 4.7)"
    set_font(p.runs[0], "Calibri", 11, italic=True, color=(100, 116, 139))

    # =========================================================================
    # SLIDE 2: Organization, Team & Module Overview
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Organization, Team and Module Overview")

    # Left card: Organization & Team
    shape_left = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    shape_left.fill.solid()
    shape_left.fill.fore_color.rgb = RGBColor(248, 250, 252)
    shape_left.line.color.rgb = RGBColor(203, 213, 225)
    tf_l = shape_left.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "1.1 Organization and Team Overview"
    set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))

    bullets_l = [
        ("Host Organization: ", "REVA University — School of Computing and Information Technology (SCIT)."),
        ("Program: ", "REVA Internship Opportunities (RIO) in-house engineering and research initiative."),
        ("Engineering Cohort: ", "Learning Analytics & Intelligent Campus Diagnostic Systems group."),
        ("Supervision: ", "Reported directly to Dr Sailaja Thota across weekly agile sprint reviews."),
        ("Culture: ", "Adhered to industry-standard peer programming, code reviews, and ADR architecture documentation.")
    ]
    for b_title, b_desc in bullets_l:
        p = tf_l.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {b_title}"
        set_font(r1, "Calibri", 11, bold=True, color=(30, 58, 138))
        r2 = p.add_run()
        r2.text = b_desc
        set_font(r2, "Calibri", 11, bold=False, color=(51, 65, 85))

    # Right card: Assigned Module & Problem
    shape_right = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    shape_right.fill.solid()
    shape_right.fill.fore_color.rgb = RGBColor(248, 250, 252)
    shape_right.line.color.rgb = RGBColor(203, 213, 225)
    tf_r = shape_right.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "1.2 Assigned Module & Problem Statement"
    set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))

    bullets_r = [
        ("Core Problem: ", "Traditional LMS solutions offer delayed reporting post-exams, causing high student failure rates without prerequisite remediation."),
        ("Assigned Module: ", "PACD-RAG (Prerequisite-Aware Contextual Diagnostic & Retrieval-Augmented Generation) middleware engine."),
        ("Target Users: ", "300+ undergraduate STEM candidates and faculty academic mentors across 1,400+ student cohorts."),
        ("System Role: ", "Ingests question-level IA marks, traverses curriculum prerequisite DAGs, and generates scaffolded 5-day study plans."),
        ("Advance Warning: ", "Provides 4.2-week proactive warning lead-time via calibrated risk ensemble (tau = 0.42).")
    ]
    for b_title, b_desc in bullets_r:
        p = tf_r.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {b_title}"
        set_font(r1, "Calibri", 11, bold=True, color=(16, 185, 129))
        r2 = p.add_run()
        r2.text = b_desc
        set_font(r2, "Calibri", 11, bold=False, color=(51, 65, 85))

    # =========================================================================
    # SLIDE 3: Technology Stack Architecture (Section 1.3)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "1.3 Technology Stack & Proficiency Progression")

    table_shape = s3.shapes.add_table(5, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8))
    t = table_shape.table
    t.columns[0].width = Inches(2.3)
    t.columns[1].width = Inches(2.5)
    t.columns[2].width = Inches(4.9)
    t.columns[3].width = Inches(2.0)

    t_headers = ["Layer / Component", "Technology Used", "Purpose in the Assigned Module", "My Level at Start → Now"]
    for c_i, h in enumerate(t_headers):
        cell = t.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        set_font(p.runs[0], "Calibri", 11, bold=True, color=(15, 23, 42))

    t_rows = [
        ("Presentation Layer", "HTML5, CSS3, Vanilla ES6+", "High-contrast glassmorphism interface displaying student IA diagnostics, risk badges, and faculty telemetry.", "3 → 5  (Proficient)"),
        ("Application / API Layer", "Python FastAPI, Pydantic, Uvicorn", "Asynchronous non-blocking REST API routing, diagnostic endpoints, and background task scheduling.", "3 → 5  (Advanced)"),
        ("Database & Storage", "PostgreSQL 15 & ChromaDB", "Relational persistence of student profiles/marks paired with dense cosine vector lecture embeddings.", "3 → 5  (Advanced)"),
        ("Diagnostic Intelligence", "CatBoost, XGBoost, Okapi BM25, OKF Graph", "Calibrated multi-model risk prediction ensemble (tau=0.42) and hybrid prerequisite RAG search.", "2 → 5  (Expert)")
    ]
    for r_i, row in enumerate(t_rows):
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            is_rating = (c_i == 3)
            set_font(p.runs[0], "Calibri", 10.5, bold=is_rating, color=(16, 185, 129) if is_rating else (51, 65, 85))

    # =========================================================================
    # SLIDE 4: Technical Fundamentals Progression (Section 2.1)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "2.1 Technical Fundamentals: Baseline vs Now")

    table_shape = s4.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    t = table_shape.table
    t.columns[0].width = Inches(2.6)
    t.columns[1].width = Inches(1.4)
    t.columns[2].width = Inches(1.4)
    t.columns[3].width = Inches(6.3)

    t_headers = ["Core Computer Science Area", "Baseline (1–5)", "Now (1–5)", "What I Did to Improve During RIO Internship"]
    for c_i, h in enumerate(t_headers):
        cell = t.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        set_font(p.runs[0], "Calibri", 11, bold=True, color=(15, 23, 42))

    t_rows = [
        ("Data Structures & Algorithms", "3 / 5", "5 / 5", "Mastered directed acyclic graph (DAG) topological sorting (Kahn's), Tarjan's SCC cycle detection, and recursive depth-weighted tree traversal."),
        ("Operating Systems", "3 / 5", "4 / 5", "Implemented asynchronous Python event loops, background daemon workers, process management, and concurrency handling under Windows/Linux."),
        ("Database Management Systems", "3 / 5", "5 / 5", "Designed 3NF relational schemas, composite keys, ON CONFLICT DO UPDATE upsert handlers, index tuning, and paired with ChromaDB vector store."),
        ("Computer Networks", "3 / 5", "4 / 5", "Configured secure CORS headers, RESTful HTTP protocols, TLS/SSL termination, and automated SMTP alert dispatch over port 587."),
        ("Assigned Tech Stack", "2 / 5", "5 / 5", "Built end-to-end FastAPI microservices, Reciprocal Rank Fusion (k=60), Okapi BM25 sparse rankers, and multi-model gradient boosting ensembles.")
    ]
    for r_i, row in enumerate(t_rows):
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            is_now = (c_i == 2)
            set_font(p.runs[0], "Calibri", 10.5, bold=is_now, color=(16, 185, 129) if is_now else (51, 65, 85))

    # =========================================================================
    # SLIDE 5: Workplace Practices & Coding Standards (Section 3.1)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "3.1 Workplace Practices, Documentation and Standards")

    cards = [
        ("PEP 8 & Type Annotations", "Strict code styling across all Python modules with typing.Dict, typing.List, and Pydantic validation models to prevent runtime schema drift.", (30, 58, 138)),
        ("Semantic Git Commit Conventions", "Trunk-based development with clear semantic messages (e.g. 'feat: add pure-Python OkapiBM25 ranker with mathematical token preservation').", (16, 185, 129)),
        ("Exhaustive Docstrings & Complexity", "Every algorithm documented with asymptotic runtime bounds (e.g. Kahn's O(V+E), RRF fusion O(N log N)) and I/O parameter specifications.", (217, 119, 6)),
        ("Architecture Decision Records (ADRs)", "Formal technical decisions documented with rationale (e.g. choosing hybrid BM25+ChromaDB over dense-only to preserve exact partial derivative symbols).", (147, 51, 234))
    ]
    for i, (c_title, c_desc, c_color) in enumerate(cards):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.5 + row * 2.7)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.4))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(248, 250, 252)
        box.line.color.rgb = RGBColor(*c_color)
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = c_title
        set_font(p.runs[0], "Calibri", 13, bold=True, color=c_color)

        p = tf.add_paragraph()
        p.text = c_desc
        set_font(p.runs[0], "Calibri", 11, bold=False, color=(51, 65, 85))

    # =========================================================================
    # SLIDE 6: Industry Tools & Infrastructure (Section 3.2)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "3.2 Industry Tools and Infrastructure")

    table_shape = s6.shapes.add_table(6, 3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    t = table_shape.table
    t.columns[0].width = Inches(2.2)
    t.columns[1].width = Inches(3.5)
    t.columns[2].width = Inches(6.0)

    t_headers = ["Industry Tool", "Used For in RIO Internship", "Key Results & Production Remarks"]
    for c_i, h in enumerate(t_headers):
        cell = t.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        set_font(p.runs[0], "Calibri", 11, bold=True, color=(15, 23, 42))

    t_rows = [
        ("Git & GitHub", "Version control, code synchronization, and CI/CD", "Maintained clean repository at github.com/Sumith2104/rio.git with secret scanning compliance."),
        ("PostgreSQL 15", "Relational persistence of student marks and profiles", "Configured connection pools and ON CONFLICT DO UPDATE upsert logic for batch marks CSV uploads."),
        ("ChromaDB Vector Store", "Dense cosine vector storage for curriculum lecture materials", "Vectorized 79 lecture chunks across Units 1–4 with slide-level grounding metadata."),
        ("FastAPI & Uvicorn", "Asynchronous REST microservice framework", "Non-blocking event loop delivering sub-450ms diagnostic retrieval latency under multi-user load."),
        ("VS Code & Postman", "IDE authoring, interactive debugging, and endpoint tests", "Automated end-to-end regression suites verifying 42/42 testcases with 100% pass rate.")
    ]
    for r_i, row in enumerate(t_rows):
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            set_font(p.runs[0], "Calibri", 10.5, bold=(c_i==0), color=(15, 23, 42) if c_i==0 else (51, 65, 85))

    # =========================================================================
    # SLIDE 7: Guide Feedback & Architectural Pivots (Section 4.1 & 4.2)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "4. Guide Feedback and Professional Conduct")

    table_shape = s7.shapes.add_table(5, 3, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    t = table_shape.table
    t.columns[0].width = Inches(3.8)
    t.columns[1].width = Inches(6.1)
    t.columns[2].width = Inches(1.8)

    t_headers = ["Mentor Feedback Point (Dr Sailaja Thota)", "Engineering Action Taken", "Status"]
    for c_i, h in enumerate(t_headers):
        cell = t.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        set_font(p.runs[0], "Calibri", 11, bold=True, color=(15, 23, 42))

    t_rows = [
        ("Expand curriculum ontology to cover all 4 STEM units with formal acyclicity.", "Engineered populate_top_level_okf.py, verifying 68 concept nodes and 112 directed edges with Kahn's topological sort.", "Done  (100%)"),
        ("Ensure lecture materials cite exact slide numbers and mathematical formulas.", "Ingested 68 lecture chunks into ChromaDB with explicit Unit/Slide metadata (e.g., Unit-03-Slide-32).", "Done  (100%)"),
        ("Add batch CSV marks ingestion for section-wise instructor workflows.", "Developed /api/faculty/batch-ingest-marks pipeline with real-time UI execution telemetry.", "Done  (100%)"),
        ("Ensure zero-emoji visual standards and academic report alignment.", "Rebuilt high-contrast glassmorphism UI and generated publication-grade reports strictly matching templates.", "Done  (100%)")
    ]
    for r_i, row in enumerate(t_rows):
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            is_status = (c_i == 2)
            set_font(p.runs[0], "Calibri", 10.5, bold=is_status, color=(16, 185, 129) if is_status else (51, 65, 85))

    # =========================================================================
    # SLIDE 8: Mock Interviews & Placement Readiness (Section 5.1 & 5.2)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "5.1 & 5.2 Placement Readiness & Mock Interviews")

    # Table of Mock Interviews
    table_shape = s8.shapes.add_table(3, 5, Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.6))
    t = table_shape.table
    t.columns[0].width = Inches(2.2)
    t.columns[1].width = Inches(1.2)
    t.columns[2].width = Inches(3.3)
    t.columns[3].width = Inches(2.6)
    t.columns[4].width = Inches(2.4)

    t_headers = ["Round", "Date", "Topics Covered", "Score / Feedback", "Action Taken"]
    for c_i, h in enumerate(t_headers):
        cell = t.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        set_font(p.runs[0], "Calibri", 10.5, bold=True, color=(15, 23, 42))

    t_rows = [
        ("Mock Interview 1 (Week 7)", "15 Oct 2026", "DSA (Graphs/Trees), Python Concurrency, SQL Optimization", "8.5 / 10 — Strong algorithmic logic; articulate space bounds faster.", "Practiced graph cycle detection proofs."),
        ("Capstone Mock Interview (Week 15)", "10 Nov 2026", "System Architecture, RAG Design, Ensemble Calibration, Live Coding", "9.5 / 10 — Outstanding technical mastery of hybrid search & DB design.", "Deepened distributed caching architectures.")
    ]
    for r_i, row in enumerate(t_rows):
        for c_i, val in enumerate(row):
            cell = t.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            set_font(p.runs[0], "Calibri", 10, bold=(c_i==3), color=(16, 185, 129) if c_i==3 else (51, 65, 85))

    # Bottom card: Resume & Portfolio
    box_b = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.2))
    box_b.fill.solid()
    box_b.fill.fore_color.rgb = RGBColor(248, 250, 252)
    box_b.line.color.rgb = RGBColor(203, 213, 225)
    tf_b = box_b.text_frame
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    p.text = "Resume, LinkedIn and Portfolio Enhancement"
    set_font(p.runs[0], "Calibri", 13, bold=True, color=(15, 23, 42))

    p = tf_b.add_paragraph()
    p.text = "• Live Repository: https://github.com/Sumith2104/rio.git  |  LinkedIn: linkedin.com/in/sumith-u-141b85317  |  Portfolio: sumithu.dev"
    set_font(p.runs[0], "Calibri", 11, bold=True, color=(30, 58, 138))

    p = tf_b.add_paragraph()
    p.text = "• Mentor-Driven Refinements: Restructured resume to highlight quantified production metrics ('Engineered hybrid BM25+ChromaDB RAG achieving 88.3% RAGAS score and 100% prerequisite coverage'), replacing generic project descriptions with measurable engineering impact."
    set_font(p.runs[0], "Calibri", 11, bold=False, color=(51, 65, 85))

    # =========================================================================
    # SLIDE 9: Reflection & Capstone Showcase Plan (Section 5.3 & 5.4)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "5.3 & 5.4 Reflection and Capstone Showcase Plan")

    # Left card: Reflection
    shape_l = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    shape_l.fill.solid()
    shape_l.fill.fore_color.rgb = RGBColor(248, 250, 252)
    shape_l.line.color.rgb = RGBColor(203, 213, 225)
    tf_l = shape_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "5.3 Internship Reflection"
    set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))

    p = tf_l.add_paragraph()
    p.text = "• Theory to Enterprise Systems: Evolved from textbook ML concepts into designing production-grade decoupled microservices."
    set_font(p.runs[0], "Calibri", 11, color=(51, 65, 85))

    p = tf_l.add_paragraph()
    p.text = "• Overcoming Real Obstacles: Solved context truncation in vector search by designing an in-memory pure-Python Okapi BM25 ranker with 1,200-char boundary preservation."
    set_font(p.runs[0], "Calibri", 11, color=(51, 65, 85))

    p = tf_l.add_paragraph()
    p.text = "• Placement Readiness: Mastered live system design, graph theory, and SQL concurrency, achieving complete confidence for top-tier tech placement drives."
    set_font(p.runs[0], "Calibri", 11, color=(51, 65, 85))

    # Right card: Showcase Plan
    shape_r = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    shape_r.fill.solid()
    shape_r.fill.fore_color.rgb = RGBColor(248, 250, 252)
    shape_r.line.color.rgb = RGBColor(203, 213, 225)
    tf_r = shape_r.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "5.4 Capstone Showcase Plan"
    set_font(p.runs[0], "Calibri", 14, bold=True, color=(15, 23, 42))

    p = tf_r.add_paragraph()
    p.text = "Point 1: Predictive Advance Warning (tau = 0.42)\nDemonstrate 4-tier risk ensemble predicting at-risk students 4.2 weeks prior with live telemetry."
    set_font(p.runs[0], "Calibri", 11, bold=False, color=(16, 185, 129))

    p = tf_r.add_paragraph()
    p.text = "Point 2: Root-Cause DAG Traversal\nShowcase 68-concept OKF Ontological Graph tracing poor Backpropagation performance to upstream Matrix Calculus and Chain Rule deficits."
    set_font(p.runs[0], "Calibri", 11, bold=False, color=(30, 58, 138))

    p = tf_r.add_paragraph()
    p.text = "Point 3: Scaffolded 5-Day Remedial Plan Demo\nLive walkthrough of an automated 5-day study plan generated with exact slide citations (Unit-03-Slide-32) and LaTeX equations."
    set_font(p.runs[0], "Calibri", 11, bold=False, color=(217, 119, 6))

    # =========================================================================
    # SLIDE 10: Conclusion & Acknowledgements
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion, Declaration and Acknowledgements")

    box_c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.8))
    box_c.fill.solid()
    box_c.fill.fore_color.rgb = RGBColor(248, 250, 252)
    box_c.line.color.rgb = RGBColor(203, 213, 225)
    tf_c = box_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Declaration & Formal Acknowledgement"
    set_font(p.runs[0], "Calibri", 18, bold=True, color=(15, 23, 42))

    p = tf_c.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "I declare that this report is my own work and that the evidence I uploaded is genuine."
    set_font(p.runs[0], "Calibri", 12, italic=True, color=(51, 65, 85))

    p = tf_c.add_paragraph()
    p.text = "\nSpecial Acknowledgement:"
    set_font(p.runs[0], "Calibri", 13, bold=True, color=(30, 58, 138))

    p = tf_c.add_paragraph()
    p.text = "We express our sincere gratitude to Dr Sailaja Thota (Associate Professor, Department of AIML) for her invaluable technical mentorship, architectural guidance, and continuous encouragement throughout this RIO internship."
    set_font(p.runs[0], "Calibri", 11.5, bold=False, color=(51, 65, 85))

    p = tf_c.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "\nThank You! Questions?"
    set_font(p.runs[0], "Calibri", 16, bold=True, color=(15, 23, 42))

    p = tf_c.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "sumithu.dev@gmail.com  |  https://github.com/Sumith2104/rio.git"
    set_font(p.runs[0], "Calibri", 12, bold=True, color=(30, 58, 138))

    prs.save(OUTPUT_PATH)
    print(f"Internship presentation saved: {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH):,} bytes)")

if __name__ == "__main__":
    build_presentation()
