import re

with open('redesign_report.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean up p21: replace single paragraph with embedded \n with clean paragraphs
p21_old = '''    p21 = doc.add_paragraph(
        "PACD-RAG is engineered as a decoupled three-tier architecture that fuses two foundational intelligence systems: "
        "a RAG + OKF (Retrieval-Augmented Generation + Open Knowledge Format) root-cause diagnostic engine and a "
        "Multi-Model predictive risk assessment setup:\\n\\n"
        "1. Presentation Tier: Pure semantic HTML5, Vanilla JavaScript, and a high-contrast Glassmorphism design system "
        "(student.html, faculty.html, index.html) with zero external CSS frameworks, ensuring microsecond render performance, "
        "sub-50ms DOM updates, and complete zero-emoji compliance.\\n"
        "2. Application Tier: An asynchronous Python FastAPI server (api_server.py) orchestrating micro-routed endpoints across "
        "auth_router, student_router, faculty_router, and pipeline_router with Pydantic contract enforcement.\\n"
        "3. Data & Dual-Intelligence Tier:\\n"
        "   • RAG + OKF Engine: An Open Knowledge Format (OKF) DAG (prerequisite_graph.py, concept_prerequisites.json "
        "with 68 concept nodes and 112 prerequisite edges) integrated with a local ChromaDB vector store (fastembed BAAI/bge-small-en-v1.5). "
        "When an assessment deficit (<50%) occurs, the OKF engine performs topological DAG traversal to isolate upstream prerequisite gaps, "
        "and triggers targeted RAG vector retrieval against faculty curriculum slides to generate personalized 5-Day Remedial Plans.\\n"
        "   • Multi-Model Predictive Risk Setup: A 4-tier model hierarchy combining an Early-Warning Baseline Model (pre-admission records), "
        "a Behavioral & Engagement Velocity Model (attendance and LMS access rates), an Academic Mastery Deficit Model (IA marks momentum), "
        "and a Blended Non-Linear Ensemble (CatBoost + XGBoost + Random Forest with cost-sensitive threshold tau = 0.42), stored in models/ "
        "and PostgreSQL (Fluxbase)."
    )
    p21.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p21.paragraph_format.line_spacing = 1.15
    p21.paragraph_format.space_after = Pt(8)'''

p21_new = '''    p21_lead = doc.add_paragraph(
        "PACD-RAG is engineered as a decoupled three-tier architecture that fuses two foundational intelligence systems: "
        "a RAG + OKF (Retrieval-Augmented Generation + Open Knowledge Format) root-cause diagnostic engine and a "
        "Multi-Model predictive risk assessment setup:"
    )
    p21_lead.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p21_lead.paragraph_format.line_spacing = 1.15
    p21_lead.paragraph_format.space_after = Pt(4)

    tier_items = [
        ("1. Presentation Tier: ", "Pure semantic HTML5, Vanilla JavaScript, and a high-contrast Glassmorphism design system (student.html, faculty.html, index.html) with zero external CSS frameworks, ensuring microsecond render performance, sub-50ms DOM updates, and complete zero-emoji compliance."),
        ("2. Application Tier: ", "An asynchronous Python FastAPI server (api_server.py) orchestrating micro-routed endpoints across auth_router, student_router, faculty_router, and pipeline_router with Pydantic contract enforcement."),
        ("3. Data & Dual-Intelligence Tier: ", "Comprises two synergistic intelligence engines:"),
        ("   • RAG + OKF Engine: ", "An Open Knowledge Format (OKF) DAG (prerequisite_graph.py, concept_prerequisites.json with 68 concept nodes and 112 prerequisite edges) integrated with a local ChromaDB vector store (fastembed BAAI/bge-small-en-v1.5). When an assessment deficit (<50%) occurs, the OKF engine performs topological DAG traversal to isolate upstream prerequisite gaps, and triggers targeted RAG vector retrieval against faculty curriculum slides to generate personalized 5-Day Remedial Plans."),
        ("   • Multi-Model Predictive Risk Setup: ", "A 4-tier model hierarchy combining an Early-Warning Baseline Model (pre-admission records), a Behavioral & Engagement Velocity Model (attendance and LMS access rates), an Academic Mastery Deficit Model (IA marks momentum), and a Blended Non-Linear Ensemble (CatBoost + XGBoost + Random Forest with cost-sensitive threshold tau = 0.42), stored in models/ and PostgreSQL (Fluxbase).")
    ]
    for b_title, b_desc in tier_items:
        p_tier = doc.add_paragraph()
        p_tier.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_tier.paragraph_format.left_indent = Inches(0.2)
        p_tier.paragraph_format.line_spacing = 1.15
        p_tier.paragraph_format.space_after = Pt(3)
        r_t1 = p_tier.add_run(b_title)
        r_t1.bold = True
        r_t1.font.name = 'Calibri'
        r_t1.font.size = Pt(10)
        r_t2 = p_tier.add_run(b_desc)
        r_t2.font.name = 'Calibri'
        r_t2.font.size = Pt(10)'''

if p21_old in text:
    text = text.replace(p21_old, p21_new)
    print("Replaced p21 successfully")
else:
    print("Warning: p21_old not matched exactly, checking regex...")

# 2. Clean up p51: replace single paragraph with embedded \n with clean paragraphs
p51_old = '''    p51 = doc.add_paragraph(
        "This project was collaboratively designed, implemented, and verified by Sumith U (R24EA807) and Shreehari (R23EA116).\\n"
        "• Sumith U (R24EA807): Led the research, architecture, and implementation of the RAG + OKF (Retrieval-Augmented Generation + Open Knowledge Format) engine. Designed the Prerequisite Knowledge Graph DAG traversal algorithms in prerequisite_graph.py (resolving deep ancestor deficits across 68 concept nodes and 112 edges), integrated the ChromaDB local vector store (fastembed BAAI/bge-small-en-v1.5) for syllabus retrieval, built the asynchronous FastAPI backend routes, implemented direct bcrypt credential authentication, and developed the automated Playwright E2E verification test harness across Weeks 1–14.\\n"
        "• Shreehari (R23EA116): Led the development, training, and deployment of the Multi-Model Predictive Risk Setup. Architected the 4-tier model hierarchy: Tier 1 Early-Warning Baseline Model (pre-admission & historical grades), Tier 2 Behavioral Engagement Velocity Model (LMS and attendance drops), Tier 3 Academic Mastery Model (IA credit deficits), and Tier 4 Blended Champion Ensemble (CatBoost + XGBoost + Random Forest with calibrated decision threshold tau=0.42). Engineered cohort feature pipelines, automated batch IA marks ingestion logic, and faculty cohort management modules across Weeks 1–14.\\n"
        "Together, both candidates integrated Module-1 (Multi-Model Risk Engine) with Module-2 (RAG + OKF Diagnostic Engine), eliminated OTP friction with direct secure bcrypt authentication, harmonized the high-contrast glassmorphism theme, and achieved 100% test pass rates across all review milestones."
    )
    p51.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p51.paragraph_format.line_spacing = 1.15
    p51.paragraph_format.space_after = Pt(4)'''

p51_new = '''    p51_lead = doc.add_paragraph("This project was collaboratively designed, implemented, and verified by Sumith U (R24EA807) and Shreehari (R23EA116).")
    p51_lead.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p51_lead.paragraph_format.line_spacing = 1.15
    p51_lead.paragraph_format.space_after = Pt(4)

    contribs = [
        ("• Sumith U (R24EA807): ", "Led the research, architecture, and implementation of the RAG + OKF (Retrieval-Augmented Generation + Open Knowledge Format) engine. Designed the Prerequisite Knowledge Graph DAG traversal algorithms in prerequisite_graph.py (resolving deep ancestor deficits across 68 concept nodes and 112 edges), integrated the ChromaDB local vector store (fastembed BAAI/bge-small-en-v1.5) for syllabus retrieval, built the asynchronous FastAPI backend routes, implemented direct bcrypt credential authentication, and developed the automated Playwright E2E verification test harness across Weeks 1–14."),
        ("• Shreehari (R23EA116): ", "Led the development, training, and deployment of the Multi-Model Predictive Risk Setup. Architected the 4-tier model hierarchy: Tier 1 Early-Warning Baseline Model (pre-admission & historical grades), Tier 2 Behavioral Engagement Velocity Model (LMS and attendance drops), Tier 3 Academic Mastery Model (IA credit deficits), and Tier 4 Blended Champion Ensemble (CatBoost + XGBoost + Random Forest with calibrated decision threshold tau=0.42). Engineered cohort feature pipelines, automated batch IA marks ingestion logic, and faculty cohort management modules across Weeks 1–14.")
    ]
    for c_title, c_desc in contribs:
        p_c = doc.add_paragraph()
        p_c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_c.paragraph_format.left_indent = Inches(0.2)
        p_c.paragraph_format.line_spacing = 1.15
        p_c.paragraph_format.space_after = Pt(4)
        r_c1 = p_c.add_run(c_title)
        r_c1.bold = True
        r_c1.font.name = 'Calibri'
        r_c1.font.size = Pt(10)
        r_c2 = p_c.add_run(c_desc)
        r_c2.font.name = 'Calibri'
        r_c2.font.size = Pt(10)

    p51_close = doc.add_paragraph("Together, both candidates integrated Module-1 (Multi-Model Risk Engine) with Module-2 (RAG + OKF Diagnostic Engine), eliminated OTP friction with direct secure bcrypt authentication, harmonized the high-contrast glassmorphism theme, and achieved 100% test pass rates across all review milestones.")
    p51_close.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p51_close.paragraph_format.line_spacing = 1.15
    p51_close.paragraph_format.space_after = Pt(6)'''

if p51_old in text:
    text = text.replace(p51_old, p51_new)
    print("Replaced p51 successfully")
else:
    print("Warning: p51_old not matched exactly, checking regex...")

# 3. Remove artificial page breaks before Section 2, 3, 4, 5
text = text.replace('doc.add_page_break()\n    h2 = doc.add_heading', '# doc.add_page_break()\n    h2 = doc.add_heading')
text = text.replace('doc.add_page_break()\n    h3 = doc.add_heading', '# doc.add_page_break()\n    h3 = doc.add_heading')
text = text.replace('doc.add_page_break()\n    h4 = doc.add_heading', '# doc.add_page_break()\n    h4 = doc.add_heading')
text = text.replace('doc.add_page_break()\n    h5 = doc.add_heading', '# doc.add_page_break()\n    h5 = doc.add_heading')

with open('redesign_report.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("redesign_report.py updated successfully!")

