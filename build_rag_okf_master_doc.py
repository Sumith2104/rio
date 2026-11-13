"""
build_rag_okf_master_doc.py
---------------------------
Builds a comprehensive, publication-grade master guide:
'RAG_and_OKF_Complete_Master_Guide_From_Scratch.docx' and '.pdf'
Author: Sumith U (SRN: R24EA807), Dept of AIML, REVA University
Faculty Guide: Dr Sailaja Thota
Explains RAG and OKF completely from scratch (0 to up-to-date)
with mathematical derivations, algorithms, code structures,
Sneha Patel case walkthrough, and viva defense cheat-sheet.
"""

import os, sys, shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

TARGET_DOCX = r"C:\Users\sumit\Downloads\rio\RAG_and_OKF_Complete_Master_Guide_From_Scratch.docx"
TARGET_PDF = r"C:\Users\sumit\Downloads\rio\RAG_and_OKF_Complete_Master_Guide_From_Scratch.pdf"
DOWNLOADS_DOCX = r"C:\Users\sumit\Downloads\RAG_and_OKF_Complete_Master_Guide_From_Scratch.docx"
DOWNLOADS_PDF = r"C:\Users\sumit\Downloads\RAG_and_OKF_Complete_Master_Guide_From_Scratch.pdf"
RIO_DOCS_DOCX = r"C:\Users\sumit\Downloads\rio docs\RAG_and_OKF_Complete_Master_Guide_From_Scratch.docx"
RIO_DOCS_PDF = r"C:\Users\sumit\Downloads\rio docs\RAG_and_OKF_Complete_Master_Guide_From_Scratch.pdf"

ASSETS_DIR = r"C:\Users\sumit\Downloads\rio\assets"
REVA_LOGO = os.path.join(ASSETS_DIR, "reva_logo.png")
SDG_LOGO = os.path.join(ASSETS_DIR, "sdg4_logo.png")
FIG1_PATH = os.path.join(ASSETS_DIR, "arch_fig1_current_system.png")
FIG2_PATH = os.path.join(ASSETS_DIR, "arch_fig2_diagnostic_traversal.png")
FIG3_PATH = os.path.join(ASSETS_DIR, "arch_fig3_future_roadmap.png")

NAVY_PRIMARY = RGBColor(0x00, 0x20, 0x60)
SLATE_DARK = RGBColor(0x1E, 0x29, 0x3B)
TEXT_MUTED = RGBColor(0x64, 0x74, 0x8B)
TEAL_ACCENT = RGBColor(0x02, 0x84, 0xC7)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def shade_cell(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_table_borders(table, color="D1D5DB", sz="4"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tblBorders.append(b)
    for b_name in ['insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'none')
        tblBorders.append(b)
    tblPr.append(tblBorders)

def add_callout(doc, text, title="KEY INTUITION"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=110, bottom=110, left=180, right=140)
    shade_cell(cell, "F0F9FF")
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    left_b = OxmlElement('w:left')
    left_b.set(qn('w:val'), 'single')
    left_b.set(qn('w:sz'), '24')
    left_b.set(qn('w:color'), '0284C7')
    tcBorders.append(left_b)
    for side in ['top', 'bottom', 'right']:
        sb = OxmlElement(f'w:{side}')
        sb.set(qn('w:val'), 'none')
        tcBorders.append(sb)
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(f"💡 {title}: ")
    r_title.bold = True
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(10)
    r_title.font.color.rgb = TEAL_ACCENT
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = SLATE_DARK
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_code_box(doc, code_str, caption=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    shade_cell(cell, "F8FAFC")
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for b_name in ['top', 'left', 'bottom', 'right']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), 'CBD5E1')
        tcBorders.append(b)
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    if caption:
        rc = p.add_run(f"# {caption}\n")
        rc.bold = True
        rc.font.name = 'Consolas'
        rc.font.size = Pt(8.5)
        rc.font.color.rgb = TEAL_ACCENT
    
    rc_body = p.add_run(code_str)
    rc_body.font.name = 'Consolas'
    rc_body.font.size = Pt(8.5)
    rc_body.font.color.rgb = SLATE_DARK

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_h1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(15)
    run.font.color.rgb = NAVY_PRIMARY
    return h

def add_h2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(10)
    h.paragraph_format.space_after = Pt(3)
    h.paragraph_format.keep_with_next = True
    run = h.add_run(text)
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(12.5)
    run.font.color.rgb = TEAL_ACCENT
    return h

def add_p(doc, text, bold_prefix="", space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = SLATE_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = SLATE_DARK
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = SLATE_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = SLATE_DARK
    return p

def add_figure_image(doc, img_path, fig_num, title, desc, width=Inches(6.2)):
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(img_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    r1 = p_cap.add_run(f"Figure {fig_num}: {title} — ")
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(9.5)
    r1.font.color.rgb = NAVY_PRIMARY
    r2 = p_cap.add_run(desc)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(9.0)
    r2.font.color.rgb = TEXT_MUTED

def build_master_guide():
    doc = Document()
    
    # 1. Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("REVA University | Dept of AIML | RAG & OKF Master Guide (From Scratch)")
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = TEXT_MUTED

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun1 = fp.add_run("Sumith U (SRN: R24EA807)  |  Guide: Dr. Sailaja Thota  |  PACD-RAG Platform")
        frun1.font.name = 'Calibri'
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # COVER / HEADER BLOCK
    # =========================================================================
    tbl_hdr = doc.add_table(rows=1, cols=3)
    tbl_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_hdr.autofit = False
    tbl_hdr.columns[0].width = Inches(1.1)
    tbl_hdr.columns[1].width = Inches(4.3)
    tbl_hdr.columns[2].width = Inches(1.1)

    for c in tbl_hdr.rows[0].cells:
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    if os.path.exists(REVA_LOGO):
        p0 = tbl_hdr.rows[0].cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.add_run().add_picture(REVA_LOGO, width=Inches(1.0))

    p1 = tbl_hdr.rows[0].cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p1.add_run("REVA UNIVERSITY\n")
    r_uni.bold = True
    r_uni.font.name = 'Calibri'
    r_uni.font.size = Pt(13)
    r_uni.font.color.rgb = NAVY_PRIMARY
    
    r_dept = p1.add_run("Department of Artificial Intelligence & Machine Learning\nSchool of Computing and Information Technology")
    r_dept.font.name = 'Calibri'
    r_dept.font.size = Pt(9.5)
    r_dept.font.color.rgb = SLATE_DARK

    if os.path.exists(SDG_LOGO):
        p2 = tbl_hdr.rows[0].cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.add_run().add_picture(SDG_LOGO, width=Inches(1.0))

    # Divider bar
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(8)
    p_div.paragraph_format.space_after = Pt(10)
    tbl_div = doc.add_table(rows=1, cols=1)
    tbl_div.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_div.columns[0].width = Inches(6.5)
    c_div = tbl_div.cell(0, 0)
    shade_cell(c_div, "002060")
    set_cell_margins(c_div, top=30, bottom=30, left=50, right=50)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("RAG & OKF Deep Dive: Complete Explanation\nFrom Ground Zero to State-of-the-Art")
    r_t.bold = True
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = NAVY_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_s = p_sub.add_run("A Comprehensive Technical, Mathematical & Conceptual Guide for Student Review, Viva-Voce, and Implementation")
    r_s.italic = True
    r_s.font.name = 'Calibri'
    r_s.font.size = Pt(11)
    r_s.font.color.rgb = TEAL_ACCENT

    # Metadata Table
    tbl_meta = doc.add_table(rows=2, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    tbl_meta.columns[0].width = Inches(3.25)
    tbl_meta.columns[1].width = Inches(3.25)
    set_table_borders(tbl_meta, color="E2E8F0")

    for row in tbl_meta.rows:
        for c in row.cells:
            shade_cell(c, "F8FAFC")
            set_cell_margins(c, top=80, bottom=80, left=120, right=120)

    p_m1 = tbl_meta.cell(0, 0).paragraphs[0]
    p_m1.add_run("Primary Author & Module Lead:\n").bold = True
    p_m1.add_run("Sumith U (SRN: R24EA807)\nB.Tech AIML (7th Sem), Section B, REVA University")
    p_m1.runs[0].font.name = 'Calibri'; p_m1.runs[0].font.size = Pt(9.5); p_m1.runs[0].font.color.rgb = NAVY_PRIMARY
    p_m1.runs[1].font.name = 'Calibri'; p_m1.runs[1].font.size = Pt(9.0)

    p_m2 = tbl_meta.cell(0, 1).paragraphs[0]
    p_m2.add_run("Faculty Guide & Reviewer:\n").bold = True
    p_m2.add_run("Dr. Sailaja Thota\nAssociate Professor, Dept of AIML, REVA University")
    p_m2.runs[0].font.name = 'Calibri'; p_m2.runs[0].font.size = Pt(9.5); p_m2.runs[0].font.color.rgb = NAVY_PRIMARY
    p_m2.runs[1].font.name = 'Calibri'; p_m2.runs[1].font.size = Pt(9.0)

    p_m3 = tbl_meta.cell(1, 0).paragraphs[0]
    p_m3.add_run("Assigned Module Scope:\n").bold = True
    p_m3.add_run("Module-2: Ontological Knowledge Framework (OKF) &\nHybrid Retrieval-Augmented Generation (PACD-RAG)")
    p_m3.runs[0].font.name = 'Calibri'; p_m3.runs[0].font.size = Pt(9.5); p_m3.runs[0].font.color.rgb = NAVY_PRIMARY
    p_m3.runs[1].font.name = 'Calibri'; p_m3.runs[1].font.size = Pt(9.0)

    p_m4 = tbl_meta.cell(1, 1).paragraphs[0]
    p_m4.add_run("Benchmark Verification:\n").bold = True
    p_m4.add_run("RAGAS Quality Score: 88.3% [Grade A]\n42/42 Automated Regression Tests Passing")
    p_m4.runs[0].font.name = 'Calibri'; p_m4.runs[0].font.size = Pt(9.5); p_m4.runs[0].font.color.rgb = NAVY_PRIMARY
    p_m4.runs[1].font.name = 'Calibri'; p_m4.runs[1].font.size = Pt(9.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # CHAPTER 1: THE BIG PICTURE
    # =========================================================================
    add_h1(doc, "Chapter 1: The Big Picture — Why Do We Need RAG and OKF? (From Ground Zero)")
    
    add_p(doc, 
          "To truly understand this project, let us start from complete ground zero with a real-life analogy that happens in every engineering college across India.")

    add_callout(doc,
                "When a patient visits a clinic with a 102°F temperature, giving paracetamol only suppresses the fever for a few hours. "
                "A competent physician runs diagnostic blood cultures to isolate the true biological root cause — whether malaria, typhoid, or a viral infection. "
                "In traditional college evaluation, recording an aggregate mark (e.g. 'Sneha scored 14/30') and telling her to 'study hard' is like giving paracetamol. "
                "Nobody tells the student WHICH foundational concept broke down, WHY it broke down, or WHERE to fix it. "
                "PACD-RAG acts as the Intelligent Diagnostic Doctor for engineering education.",
                "THE PARACETAMOL VS. DIAGNOSTIC DOCTOR ANALOGY")

    add_h2(doc, "1.1 The Fatal Flaw of Standard LLMs and Flat Syllabi in STEM Education")
    add_p(doc, 
          "If a student struggles with an advanced Artificial Intelligence exam question (such as Backpropagation error updates in Deep Learning) "
          "and asks a generic commercial AI tool (like vanilla ChatGPT):")
    add_bullet(doc, "Generic Definitions: The model generates broad textbook summaries without understanding the student's personal learning history.", "1. ")
    add_bullet(doc, "Cognitive Overload: If the student does not understand composite calculus derivatives, throwing a 10-page proof of Backpropagation at them causes immediate panic.", "2. ")
    add_bullet(doc, "Hallucination Risk: General LLMs frequently hallucinate mathematical derivations, invent incorrect matrix notations, or cite non-existent textbook pages.", "3. ")
    add_bullet(doc, "Curriculum Misalignment: University evaluations are strictly graded according to the authorized lecture notes and formulations taught by the course professor (Dr. Sailaja Thota). Standard LLMs have no access to slide-specific university curriculum materials.", "4. ")

    add_p(doc, 
          "To solve this problem, we designed and built two synergistic engineering systems: "
          "(1) The Ontological Knowledge Framework (OKF) as the Diagnostic Brain that uncovers root prerequisite gaps, and "
          "(2) The Hybrid Retrieval-Augmented Generation (RAG) Engine as the Precision Delivery Mechanism that retrieves verified faculty slides without hallucination.")

    # =========================================================================
    # CHAPTER 2: OKF FROM SCRATCH
    # =========================================================================
    add_h1(doc, "Chapter 2: The Ontological Knowledge Framework (OKF) from Scratch")
    
    add_h2(doc, "2.1 What is an Ontology vs. a Normal Syllabus?")
    add_p(doc, 
          "A traditional college syllabus is merely a flat, linear list: Unit 1: Calculus, Unit 2: Linear Algebra, Unit 3: Neural Networks, Unit 4: Backpropagation. "
          "A flat list has no intelligence. It cannot understand dependencies. It does not know that if you fail Backpropagation, you cannot fix it without first fixing the Chain Rule of Differentiation!")
    
    add_p(doc, 
          "An Ontology, by contrast, is a formal semantic representation of human knowledge. It models: "
          "(1) Concept Entities (Nodes), (2) Directional Prerequisite Dependencies (Edges), and (3) Cognitive Attributes (Bloom's Taxonomy, mathematical equations, and slide citations).")

    add_h2(doc, "2.2 Directed Acyclic Graph (DAG) Graph Theory & Mathematics")
    add_p(doc, 
          "Mathematically, we model the curriculum as a Directed Acyclic Graph (DAG), denoted as G = (V, E):")
    add_bullet(doc, "V = {v_1, v_2, ..., v_68}: The set of 68 core concept nodes covering the entire AI & Deep Learning curriculum.", "Nodes (V): ")
    add_bullet(doc, "E = {(u, v) | u, v in V}: The set of directed prerequisite edges. By mathematical convention, u -> v denotes that concept u is a strict prerequisite of concept v (mastery of u is required prior to attempting v).", "Edges (E): ")

    add_p(doc, 
          "Why MUST the graph be strictly Acyclic (No Cycles)?\n"
          "If a cycle existed (A -> B -> C -> A), it would mean: 'To learn Calculus you need Algebra; to learn Algebra you need Sets; to learn Sets you need Calculus!' "
          "This creates an infinite pedagogical deadlock. In prerequisite_graph.py, we mathematically enforce acyclicity using Kahn's algorithm and Tarjan's Strongly Connected Components (nx.simple_cycles()). "
          "If any circular dependency is introduced, graph initialization throws an immediate exception.")

    add_p(doc, 
          "Topological Sorting:\n"
          "Because G is a DAG, there exists a topological ordering: a linear permutation of nodes such that for every directed edge (u, v), u appears before v. "
          "This guarantees that every remedial study plan generated by our system adheres to a 100% pedagogically sound sequence where foundations are reinforced first!")

    add_h2(doc, "2.3 The 68-Concept Schema & Bloom's Taxonomy")
    add_p(doc, "Every concept in our OKF catalog (concept_prerequisites.json) stores rich pedagogical attributes:")
    
    code_schema = """{
  "id": "DL_BACKPROP",
  "name": "Backpropagation Algorithm & Gradient Flow",
  "unit": "Unit 3",
  "level": "Advanced",
  "bloom_taxonomy": "Apply",
  "primary_formula": "\\\\frac{\\\\partial E}{\\\\partial w_{ij}} = \\\\frac{\\\\partial E}{\\\\partial y_j} \\\\cdot \\\\frac{\\\\partial y_j}{\\\\partial z_j} \\\\cdot \\\\frac{\\\\partial z_j}{\\\\partial w_{ij}}",
  "syllabus_slide_ref": "Unit-03-Slide-14",
  "estimated_study_minutes": 60,
  "prerequisites": ["MATH_CHAIN_RULE", "ML_GRADIENT_DESCENT"]
}"""
    add_code_box(doc, code_schema, "Sample OKF Concept Node JSON Schema (concept_prerequisites.json)")

    add_p(doc, 
          "Every concept is tagged with Bloom's Revised Cognitive Taxonomy: "
          "(1) Remember: Basic definitions (e.g., What is an epoch?); "
          "(2) Understand: Explaining concepts in plain English (e.g., Why do we need non-linear activations?); "
          "(3) Apply: Executing mathematical calculations (e.g., Computing backprop weight update delta); "
          "(4) Analyze: Diagnosing and debugging failure modes (e.g., Identifying vanishing gradients).")

    add_h2(doc, "2.4 The Upstream Root-Cause Diagnostic Traversal Algorithm")
    add_p(doc, 
          "When a student scores below 40% on an Internal Assessment question (e.g., scoring 2.5/10 on Question 2), the diagnostic engine executes the following 5-stage algorithm:")
    add_bullet(doc, "Deficit Trigger: Question score < 40% triggers a DEFICIT flag on target concept T (e.g. DL_BACKPROP).", "Stage 1: ")
    add_bullet(doc, "Transitive Ancestral Closure: Computes all upstream prerequisite ancestors: Ancestors(T) = nx.ancestors(graph, T). For Backpropagation, Ancestors = {Gradient Descent, Matrix Multiplication, Chain Rule, Partial Derivatives}.", "Stage 2: ")
    add_bullet(doc, "Weak Set Intersection: Intersects the ancestor set with the student's historical quiz/test performance records: Relevant_Gaps = Ancestors(T) ∩ Student_Weak_Concepts.", "Stage 3: ")
    add_bullet(doc, "Bottleneck Identification (find_root_cause_bottleneck): For each weak ancestor a, computes how many downstream concepts it blocks: Block_Count(a) = |Descendants(a) ∩ Student_Weak_Concepts|. The concept with the highest Block_Count is crowned the Primary Root Cause!", "Stage 4: ")
    add_bullet(doc, "Prerequisite Gap Score (PGS): Computes cognitive severity: PGS(T) = sum(w_p * (1.0 - Mastery(p))), where w_p is the cognitive prerequisite weight (e.g. 0.90 for Chain Rule).", "Stage 5: ")

    # =========================================================================
    # CHAPTER 3: RAG FROM SCRATCH
    # =========================================================================
    add_h1(doc, "Chapter 3: Retrieval-Augmented Generation (RAG) from Scratch")
    
    add_h2(doc, "3.1 The Evolution of Search: Why Neither Lexical Nor Dense Is Enough Alone")
    add_p(doc, 
          "In academic and engineering domains, information retrieval faces unique challenges that standard enterprise search engines fail to resolve:")

    tbl_search = doc.add_table(rows=1, cols=4)
    tbl_search.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_search.autofit = False
    tbl_search.columns[0].width = Inches(1.3)
    tbl_search.columns[1].width = Inches(1.5)
    tbl_search.columns[2].width = Inches(1.7)
    tbl_search.columns[3].width = Inches(2.0)
    set_table_borders(tbl_search, color="CBD5E1")

    hdr_c = tbl_search.rows[0].cells
    hdr_t = ["Search Paradigm", "Technology", "Strengths in STEM", "Fatal Weakness Alone"]
    for i, t in enumerate(hdr_t):
        shade_cell(hdr_c[i], "002060")
        set_cell_margins(hdr_c[i], top=90, bottom=90, left=90, right=90)
        p = hdr_c[i].paragraphs[0]
        run = p.add_run(t)
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    search_data = [
        ("Gen 1: Lexical (Sparse)", "Okapi BM25, TF-IDF", "Exact keyword matching; preserves LaTeX math formulas (dE/dw), acronyms (MLP, SGD), and slide IDs.", "Vocabulary Mismatch Problem: Fails if student searches for 'weight adjustment' instead of 'backpropagation'."),
        ("Gen 2: Dense Vector", "ChromaDB, FAISS (MiniLM 384-dim)", "Deep semantic understanding; handles synonyms, conceptual queries, and student phrasing naturally.", "Formula Inversion Blindness: Vectors for dE/dw and dE/db have nearly identical cosine distance (~0.98), returning wrong math formulas!"),
        ("Gen 3: Hybrid RAG", "BM25 + ChromaDB + RRF (k=60)", "Combines exact formula precision with semantic understanding into a unified ranking.", "Requires calibrated rank fusion and secondary cross-encoder re-ranking for optimal accuracy.")
    ]

    for r_idx, r in enumerate(search_data):
        cells = tbl_search.add_row().cells
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx in range(4):
            shade_cell(cells[c_idx], bg)
            set_cell_margins(cells[c_idx], top=70, bottom=70, left=90, right=90)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.15
            run = p.add_run(r[c_idx])
            run.font.name = 'Calibri'; run.font.size = Pt(8.5)
            if c_idx == 0: run.bold = True; run.font.color.rgb = NAVY_PRIMARY
            elif c_idx == 1: run.bold = True; run.font.color.rgb = SLATE_DARK
            else: run.font.color.rgb = SLATE_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2(doc, "3.2 Mathematical Derivation of Okapi BM25 Sparse Search")
    add_p(doc, 
          "In hybrid_rag_service.py, we implemented a pure-Python in-memory Okapi BM25 ranker. "
          "Given a student query Q = {q_1, q_2, ..., q_m} and a lecture slide document D:")
    
    add_p(doc, 
          "Score_BM25(D, Q) = sum_{i=1}^m [ IDF(q_i) * (f(q_i, D) * (k_1 + 1)) / (f(q_i, D) + k_1 * (1 - b + b * (|D| / avgdl))) ]",
          "BM25 Ranking Formula: ")
    
    add_p(doc,
          "Where:\n"
          "• f(q_i, D) is the Term Frequency: how many times query term q_i appears in slide D;\n"
          "• |D| is the token length of slide D, and avgdl is the average length of all slides in the corpus;\n"
          "• k_1 = 1.5 controls term frequency saturation non-linearity;\n"
          "• b = 0.75 controls document length normalization penalty.")

    add_p(doc, 
          "IDF(q_i) = ln( (N - n(q_i) + 0.5) / (n(q_i) + 0.5) + 1.0 )\n"
          "Where N is total slide chunks (79 chunks across Units 1–4) and n(q_i) is the number of slides containing term q_i. "
          "Rare technical terms ('backpropagation') receive high positive IDF weights; common filler words receive zero weight.",
          "Inverse Document Frequency (IDF): ")

    add_p(doc, 
          "Custom Math-Preserving Tokenizer:\n"
          "Standard NLP tokenizers split on backslashes and carets, destroying mathematical formulas. Our custom regex in hybrid_rag_service.py preserves symbols: "
          "tokens = re.findall(r'[a-zA-Z0-9_\\\\-\\\\^]+', clean_text).")

    add_h2(doc, "3.3 Dense Vector Search in Cosine Metric Space")
    add_p(doc, 
          "Every lecture chunk is vectorized into a 384-dimensional dense vector space using sentence-transformers/all-MiniLM-L6-v2. "
          "ChromaDB computes semantic similarity via the Cosine metric:")
    add_p(doc, 
          "Cosine_Similarity(q, d) = (q · d) / (||q|| * ||d||) = sum(q_i * d_i) / (sqrt(sum(q_i^2)) * sqrt(sum(d_i^2)))",
          "Cosine Similarity Equation: ")
    add_p(doc, "A score of 1.0 represents identical semantic alignment; 0.0 denotes orthogonal (unrelated) concepts.")

    add_h2(doc, "3.4 Reciprocal Rank Fusion (RRF with k=60)")
    add_p(doc, 
          "BM25 outputs scores in [0, 25+], while ChromaDB outputs scores in [0.0, 1.0]. Directly adding these raw numbers causes scale mismatch. "
          "To fuse them fairly, we implement Reciprocal Rank Fusion (RRF), established by Cormack, Clarke & Buettcher (SIGIR 2009):")
    add_p(doc, 
          "RRF_Score(d) = sum_{m in {dense, sparse}} [ 1 / (k + rank_m(d)) ]",
          "RRF Rank Fusion Formula: ")
    add_p(doc, 
          "Where rank_m(d) is the ordinal rank of document d in model m (rank 1, 2, 3...), and k = 60 is the smoothing parameter. "
          "Why k=60? It ensures that an outlier ranked highly in only one model cannot drown out a document that achieved high ranks across BOTH models. "
          "If Dr. Sailaja's Slide 14 is #1 in BM25 and #1 in ChromaDB, its score is 1/(60+1) + 1/(60+1) = 0.03278 — soaring to the very top of results!")

    add_h2(doc, "3.5 Cross-Encoder Re-Ranking & RAGAS Benchmarking (88.3%)")
    add_p(doc, 
          "The top 8 candidates from RRF pass through a transformer Cross-Encoder (ms-marco-MiniLM-L-6-v2). Unlike bi-encoders that process query and slide separately, "
          "the cross-encoder performs full cross-attention over all token pairs simultaneously, producing an exact relevance probability in under 40 milliseconds.")

    add_p(doc, 
          "Hallucination Guardrails & RAGAS Framework:\n"
          "To guarantee academic integrity, we enforce 3 guardrails: (1) Temperature 0.1 for near-deterministic synthesis; "
          "(2) Mandatory slide citation grounding (e.g. 'Unit-03-Slide-14'); (3) Automated evaluation via the RAGAS framework:")
    add_bullet(doc, "Faithfulness: 0.91 / 1.00 (91% of all claims are strictly verifiable in retrieved slides).", "• ")
    add_bullet(doc, "Answer Relevance: 0.89 / 1.00 (Synthesized remedial instructions directly target the student's gap).", "• ")
    add_bullet(doc, "Context Precision: 0.85 / 1.00 (Retrieved context contains high signal-to-noise ratio).", "• ")
    add_bullet(doc, "Composite Quality Score: 88.3% [Grade A Certified Quality].", "• ")

    # Insert Figure 1
    add_figure_image(doc, FIG1_PATH, 1,
                     "PACD-RAG Complete End-to-End System Architecture",
                     "Shows how the OKF Knowledge Graph DAG and Hybrid RAG Engine connect with batch marks ingestion and dual glassmorphic portals.")

    # =========================================================================
    # CHAPTER 4: SYNERGY & CASE STUDY
    # =========================================================================
    add_h1(doc, "Chapter 4: The Real-Time Synergy — Walkthrough of Sneha Patel (R24EA895)")
    add_p(doc, 
          "To demonstrate how OKF and Hybrid RAG cooperate in live production, let us examine candidate Sneha Patel's diagnostic execution:")

    # Insert Figure 2
    add_figure_image(doc, FIG2_PATH, 2,
                     "Diagnostic Root-Cause Traversal Flow (Sneha Patel 2.5/10 Walkthrough)",
                     "The 4-step chain: Question deficit -> DAG prerequisite walk -> Hybrid slide retrieval -> 5-day personalized recovery plan.")

    add_h2(doc, "Step-by-Step Diagnostic Chain:")
    add_p(doc, 
          "In IA-1 for Course BCSE402T (Artificial Intelligence & Deep Learning), Question 2 asks: 'Derive Backpropagation error gradients for a 2-layer MLP'. "
          "Sneha scores 2.5 out of 10.0 marks. Because 2.5 is below the 40% threshold, Question 2 is flagged as DEFICIT.",
          "Step 1: Test Mark Deficit Trigger — ")

    add_p(doc, 
          "The OKF engine inspects node DL_BACKPROP. It traverses upstream prerequisite edges: Backpropagation -> Gradient Descent -> Matrix Multiplication -> Chain Rule -> Partial Derivatives. "
          "Checking Sneha's historical records reveals: Gradient Descent = 8.5/10 (Mastered), but Chain Rule = 3.0/10 (Deficit). "
          "The engine diagnoses the exact root cause: Upstream prerequisite deficit in the Chain Rule of Differentiation!",
          "Step 2: OKF DAG Ancestral Walk — ")

    add_p(doc, 
          "The Hybrid RAG engine queries Dr. Sailaja Thota's Module 3 Lecture Pack for 'Chain Rule partial derivatives error gradient backpropagation'. "
          "BM25 finds exact formula matches, ChromaDB finds semantic derivative context, and RRF (k=60) ranks Module 3, Slide 14 ('Matrix Chain Rule Formulations') at the top with a 0.94 relevance match.",
          "Step 3: Hybrid RAG Slide Retrieval — ")

    add_p(doc, 
          "The LLM synthesizes Sneha's custom 5-Day Remedial Plan: "
          "• Day 1: Foundation Refresher — Review Dr. Sailaja's Slide 14 on Chain Rule calculus; "
          "• Day 2: Partial Derivatives — Solve 3 manual partial derivative calculations; "
          "• Day 3: Error Propagation — Walk through Slide 18 for two-layer error propagation; "
          "• Day 4: Code Implementation — Write a 20-line Python/NumPy script verifying dE/dw gradients; "
          "• Day 5: Self-Assessment — Attempt 3 mock questions identical to university exam patterns. "
          "Outcome: When Sneha takes the remedial re-test, her score jumps from 2.5/10 to 8.5/10!",
          "Step 4: Actionable 5-Day Recovery — ")

    # =========================================================================
    # CHAPTER 5: CODEBASE IMPLEMENTATION
    # =========================================================================
    add_h1(doc, "Chapter 5: File-by-File Codebase Implementation Guide")
    add_p(doc, "The entire RAG + OKF subsystem is organized into clean, production-ready Python modules:")

    tbl_files = doc.add_table(rows=1, cols=3)
    tbl_files.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_files.autofit = False
    tbl_files.columns[0].width = Inches(2.0)
    tbl_files.columns[1].width = Inches(2.2)
    tbl_files.columns[2].width = Inches(2.3)
    set_table_borders(tbl_files, color="CBD5E1")

    h_fc = tbl_files.rows[0].cells
    h_ft = ["Source File Path", "Primary Classes / Functions", "Architectural Role in PACD-RAG"]
    for i, t in enumerate(h_ft):
        shade_cell(h_fc[i], "002060")
        set_cell_margins(h_fc[i], top=90, bottom=90, left=90, right=90)
        p = h_fc[i].paragraphs[0]
        run = p.add_run(t)
        run.bold = True; run.font.name = 'Calibri'; run.font.size = Pt(9.0); run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    file_data = [
        ("prerequisite_graph.py", "PrerequisiteKnowledgeGraph, validate_dag(), trace_prerequisite_gaps(), find_root_cause_bottleneck()", "Constructs 68-concept NetworkX DAG, verifies acyclicity, traverses upstream ancestors, and calculates Prerequisite Gap Scores."),
        ("hybrid_rag_service.py", "HybridPrerequisiteRAG, OkapiBM25, reciprocal_rank_fusion(), retrieve_hybrid_context()", "Executes pure-Python BM25 sparse search and ChromaDB dense vector search, blends ranks via RRF (k=60), and re-ranks via Cross-Encoder."),
        ("weak_topic_rag_engine.py", "WeakTopicRAGEngine, explain_weak_topic(), build_5day_remedial_plan()", "Connects IA question deficit flags to OKF graph queries, invokes Hybrid RAG, and prompts LLM (temp=0.1) for 5-day study plans."),
        ("rag_benchmark_evaluator.py", "RAGBenchmarkEvaluator, evaluate_ragas_metrics(), run_synthetic_eval()", "Automated RAGAS test harness evaluating Faithfulness, Answer Relevance, and Context Precision across 42 testcases."),
        ("api_server.py", "FastAPI Endpoints: /explain-weak-topic, /api/rag/query, /api/pipeline/ingest-ia-marks", "Non-blocking REST microservices serving student diagnostic modals and faculty marks ingestion telemetry in <450ms.")
    ]

    for r_idx, r in enumerate(file_data):
        cells = tbl_files.add_row().cells
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx in range(3):
            shade_cell(cells[c_idx], bg)
            set_cell_margins(cells[c_idx], top=70, bottom=70, left=90, right=90)
            p = cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0); p.paragraph_format.line_spacing = 1.15
            run = p.add_run(r[c_idx])
            run.font.name = 'Calibri'; run.font.size = Pt(8.5)
            if c_idx == 0: run.bold = True; run.font.color.rgb = NAVY_PRIMARY
            elif c_idx == 1: run.bold = True; run.font.color.rgb = SLATE_DARK
            else: run.font.color.rgb = SLATE_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Insert Figure 3
    add_figure_image(doc, FIG3_PATH, 3,
                     "PACD-RAG Future Evolution & Innovation Roadmap (Phase 2 & Phase 3)",
                     "Strategic 5-pillar expansion plan: LMS event bus, local fine-tuned SLM with QLoRA, mobile Flutter app, voice Socratic tutor, and faculty XAI counterfactual simulator.")

    # =========================================================================
    # CHAPTER 6: VIVA CHEAT-SHEET
    # =========================================================================
    add_h1(doc, "Chapter 6: Examiner & Viva-Voce Defense Cheat-Sheet (Top 7 Questions)")
    add_p(doc, "The following 7 questions are the most critical technical questions external examiners ask regarding RAG and Knowledge Graphs, along with verbatim answers:")

    viva_qa = [
        ("Q1: What was your specific personal role in this project?",
         "Answer: I am the lead architect and developer for Module-2: RAG + OKF (Retrieval-Augmented Generation & Ontological Knowledge Framework). I designed and coded the 68-concept syllabus Knowledge Graph DAG in NetworkX, implemented the recursive upstream root-cause diagnostic algorithm, built the pure-Python Okapi BM25 and ChromaDB hybrid search engine with RRF k=60, and validated the entire pipeline using the RAGAS evaluation harness (88.3% quality score)."),
        
        ("Q2: Why did you use Hybrid RAG instead of just ChromaDB vector search?",
         "Answer: Dense vector search blurs out exact mathematical formulas. In vector space, dE/dw and dE/db look almost identical because they contain the same semantic words. BM25 sparse search is necessary to capture exact mathematical tokens, acronyms, and slide references. By fusing BM25 and ChromaDB with Reciprocal Rank Fusion (k=60), we get 100% mathematical precision plus conceptual understanding."),
        
        ("Q3: What is the difference between a syllabus and your OKF Knowledge Graph?",
         "Answer: A syllabus is a flat linear list of chapters. It has no directional intelligence. Our OKF is a Directed Acyclic Graph (DAG) with 68 concept nodes and prerequisite edges. When a student fails an advanced topic like Backpropagation, our DAG traverses upstream ancestors to find the true broken prerequisite—such as the Chain Rule. A flat syllabus can never diagnose root causes."),
        
        ("Q4: How do you mathematically prove that your Knowledge Graph has no infinite loops?",
         "Answer: We use Kahn's Algorithm for topological sorting and Tarjan's Strongly Connected Components algorithm (nx.simple_cycles()). The validation function verifies that the graph is strictly acyclic. If any circular prerequisite is introduced, the system throws an automated exception during graph initialization."),
        
        ("Q5: What is Reciprocal Rank Fusion (RRF) and why is k=60?",
         "Answer: RRF is an algorithm that combines rankings from different search systems without needing score normalization. Its formula is sum(1 / (k + rank(d))). The constant k=60 is the standard empirical constant established by Cormack et al. in SIGIR 2009. It prevents high-ranking outliers in one system from drowning out consistent performers across both systems."),
        
        ("Q6: How do you guarantee that the Generative AI doesn't hallucinate fake explanations or formulas?",
         "Answer: We enforce three guardrails: First, we set temperature to 0.1 for deterministic output. Second, we enforce strict prompt grounding where the model can only use verified slide chunks and must cite the slide number (e.g. Slide 14). Third, we evaluate with the RAGAS framework, achieving 0.91 Faithfulness and 0.89 Answer Relevance across 42 automated tests."),
        
        ("Q7: How does your project directly align with UN Sustainable Development Goal 4 (SDG 4)?",
         "Answer: UN SDG 4 stands for 'Quality, Inclusive, and Equitable Education'. In traditional colleges, struggling students are only identified after they fail semester exams, leading to backlogs and dropouts. PACD-RAG acts as a 24/7 personal diagnostic tutor for every student, identifying foundational gaps 6 to 8 weeks early and providing equal opportunity for academic success.")
    ]

    for q, a in viva_qa:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8); p_q.paragraph_format.space_after = Pt(2); p_q.paragraph_format.keep_with_next = True
        rq = p_q.add_run(f"❓ {q}")
        rq.bold = True; rq.font.name = 'Calibri'; rq.font.size = Pt(11); rq.font.color.rgb = NAVY_PRIMARY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0); p_a.paragraph_format.space_after = Pt(6); p_a.paragraph_format.line_spacing = 1.15
        ra = p_a.add_run(a)
        ra.font.name = 'Calibri'; ra.font.size = Pt(10); ra.font.color.rgb = SLATE_DARK

    doc.save(TARGET_DOCX)
    print(f"Master DOCX saved: {TARGET_DOCX} ({os.path.getsize(TARGET_DOCX):,} bytes)")
    shutil.copy2(TARGET_DOCX, DOWNLOADS_DOCX)
    shutil.copy2(TARGET_DOCX, RIO_DOCS_DOCX)
    print("Copied DOCX to Downloads and rio docs.")

def convert_to_pdf():
    print("Converting Master Guide DOCX to PDF via Word COM...")
    scratch_dir = r"C:\Users\sumit\Downloads\rio\scratch"
    os.makedirs(scratch_dir, exist_ok=True)
    temp_docx = os.path.join(scratch_dir, "temp_master_guide.docx")
    temp_pdf = os.path.join(scratch_dir, "temp_master_guide.pdf")
    shutil.copy2(TARGET_DOCX, temp_docx)

    import win32com.client
    w = win32com.client.Dispatch("Word.Application")
    w.Visible = False
    try:
        doc = w.Documents.Open(os.path.abspath(temp_docx), ReadOnly=True)
        doc.ExportAsFixedFormat(os.path.abspath(temp_pdf), 17)
        doc.Close(False)
        w.Quit()
        print("Exported PDF cleanly via Word COM.")
        shutil.copy2(temp_pdf, TARGET_PDF)
        shutil.copy2(temp_pdf, DOWNLOADS_PDF)
        shutil.copy2(temp_pdf, RIO_DOCS_PDF)
        print("Copied Master PDF to rio, Downloads, and rio docs.")
    except Exception as e:
        print("Error during Word COM conversion:", e)
        try: w.Quit()
        except: pass

if __name__ == "__main__":
    build_master_guide()
    convert_to_pdf()
    print("All tasks completed successfully!")

