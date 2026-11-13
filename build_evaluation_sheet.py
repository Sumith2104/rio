import os, sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

REVA_LOGO = r"C:\Users\sumit\Downloads\rio\assets\reva_logo.png"
SDG_LOGO = r"C:\Users\sumit\Downloads\rio\assets\sdg4_logo.png"

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
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

def set_table_borders(table, color="000000", sz="4"):
    table.style = 'TableGrid'
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), str(sz))
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    tblPr.append(tblBorders)

def clear_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def build_evaluation_sheet():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(0.4)
    sec.bottom_margin = Inches(0.4)
    sec.left_margin = Inches(0.5)
    sec.right_margin = Inches(0.5)

    # Header Table with Logos
    t_hdr = doc.add_table(rows=1, cols=3)
    t_hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
    clear_table_borders(t_hdr)
    col_w = [Inches(1.0), Inches(5.5), Inches(1.0)]
    for idx, cell in enumerate(t_hdr.rows[0].cells):
        cell.width = col_w[idx]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    if os.path.exists(REVA_LOGO):
        p0 = t_hdr.rows[0].cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.add_run().add_picture(REVA_LOGO, width=Inches(0.85))

    p_center = t_hdr.rows[0].cells[1].paragraphs[0]
    p_center.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_center.add_run("REVA UNIVERSITY\n")
    r1.bold = True
    r1.font.name = 'Calibri'
    r1.font.size = Pt(13)
    r2 = p_center.add_run("SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY\nDEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING\n")
    r2.bold = True
    r2.font.name = 'Calibri'
    r2.font.size = Pt(9.0)
    r2.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    r3 = p_center.add_run("MAJOR PROJECT PHASE-1 REVIEW (RIO) – EVALUATION SHEET")
    r3.bold = True
    r3.font.name = 'Calibri'
    r3.font.size = Pt(10.5)
    r3.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    if os.path.exists(SDG_LOGO):
        p2 = t_hdr.rows[0].cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.add_run().add_picture(SDG_LOGO, width=Inches(0.85))

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(1)
    p_div.paragraph_format.space_after = Pt(2)

    # Student & Project Details Table
    t_info = doc.add_table(rows=4, cols=2)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_info)
    w_info = [Inches(2.0), Inches(5.5)]
    
    info_rows = [
        ("Project Title", "PACD-RAG: Prerequisite-Aware Contextual Diagnostic & Retrieval-Augmented Generation for Student Academic Success"),
        ("Project Candidates", "Candidate 1: Sumith U (SRN: R24EA807) | 7th Sem B.Tech AIML (Sec B)\nCandidate 2: Shreehari (SRN: R23EA116) | 7th Sem B.Tech AIML (Sec B)"),
        ("Faculty Guide", "Dr Sailaja Thota, Associate Professor, Department of AIML, REVA University"),
        ("Review Details", "Phase-1 Review (Target: ~70% Completion)  |  Date: 14 November 2026")
    ]
    for r_i, (k, v) in enumerate(info_rows):
        r = t_info.rows[r_i]
        c0, c1 = r.cells[0], r.cells[1]
        shade_cell(c0, "F8FAFC")
        shade_cell(c1, "FFFFFF")
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)
        c0.width, c1.width = w_info[0], w_info[1]
        
        p_k = c0.paragraphs[0]
        p_k.text = k
        p_k.runs[0].bold = True
        p_k.runs[0].font.name = 'Calibri'
        p_k.runs[0].font.size = Pt(9.0)
        
        p_v = c1.paragraphs[0]
        p_v.text = v
        p_v.runs[0].font.name = 'Calibri'
        p_v.runs[0].font.size = Pt(9.0)

    p_sp1 = doc.add_paragraph()
    p_sp1.paragraph_format.space_before = Pt(2)
    p_sp1.paragraph_format.space_after = Pt(2)

    # Evaluation Rubrics Table
    p_rub = doc.add_paragraph()
    p_rub.paragraph_format.space_before = Pt(2)
    p_rub.paragraph_format.space_after = Pt(1)
    r_rub = p_rub.add_run("Rubric Evaluation Criteria (Maximum Marks: 50)")
    r_rub.bold = True
    r_rub.font.name = 'Calibri'
    r_rub.font.size = Pt(10)

    t_rub = doc.add_table(rows=7, cols=5)
    t_rub.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_rub)
    w_rub = [Inches(0.5), Inches(3.2), Inches(1.0), Inches(1.4), Inches(1.4)]
    
    headers = ["Sl.", "Evaluation Component", "Max Marks", "Marks: Sumith U (R24EA807)", "Marks: Shreehari (R23EA116)"]
    for c_i, h in enumerate(headers):
        cell = t_rub.rows[0].cells[c_i]
        shade_cell(cell, "F2F2F2")
        set_cell_margins(cell, 50, 50, 50, 50)
        cell.width = w_rub[c_i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.text = h
        p.runs[0].bold = True
        p.runs[0].font.name = 'Calibri'
        p.runs[0].font.size = Pt(8.5)

    criteria = [
        ("1", "Problem Definition, Literature Survey & Gap Analysis\n(Learning gap clarity, relevance of 5 surveyed papers)", "10", "", ""),
        ("2", "Requirement Specification & System Architecture\n(Functional R1-R6, Non-Functional, ADRs, Traceability)", "10", "", ""),
        ("3", "Detailed Design & Engineering Methodology\n(68-concept OKF DAG, Acyclicity, Hybrid BM25+ChromaDB RRF)", "10", "", ""),
        ("4", "Implementation Progress & Code Quality (~70% Target)\n(Multi-model risk ensemble, batch IA marks pipeline, UI Console)", "10", "", ""),
        ("5", "Testing, Benchmark Evaluation & Oral Presentation\n(RAGAS 88.3%, 42/42 testcases passed, Viva Q&A, Demonstration)", "10", "", ""),
        ("TOTAL", "TOTAL MARKS AWARDED", "50", "", "")
    ]
    for r_i, row_data in enumerate(criteria):
        row = t_rub.rows[r_i + 1]
        is_total = (r_i == len(criteria) - 1)
        for c_i, val in enumerate(row_data):
            cell = row.cells[c_i]
            shade_cell(cell, "F8FAFC" if is_total else "FFFFFF")
            set_cell_margins(cell, 40, 40, 50, 50)
            cell.width = w_rub[c_i]
            p = cell.paragraphs[0]
            align = WD_ALIGN_PARAGRAPH.CENTER if c_i in [0, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            p.alignment = align
            p.text = val
            if p.runs:
                p.runs[0].font.name = 'Calibri'
                p.runs[0].font.size = Pt(8.5 if not is_total else 9.0)
                if is_total or c_i == 0:
                    p.runs[0].bold = True

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(2)
    p_sp2.paragraph_format.space_after = Pt(2)

    # Examiner Feedback / Remarks Box
    p_rem = doc.add_paragraph()
    p_rem.paragraph_format.space_before = Pt(2)
    p_rem.paragraph_format.space_after = Pt(1)
    r_rem = p_rem.add_run("Examiner Remarks & Suggestions for Phase-2:")
    r_rem.bold = True
    r_rem.font.name = 'Calibri'
    r_rem.font.size = Pt(9.5)

    t_rem = doc.add_table(rows=1, cols=1)
    t_rem.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_rem)
    cell_rem = t_rem.rows[0].cells[0]
    cell_rem.width = Inches(7.5)
    set_cell_margins(cell_rem, 40, 40, 60, 60)
    p_blank = cell_rem.paragraphs[0]
    p_blank.text = " \n "

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_before = Pt(4)
    p_sp3.paragraph_format.space_after = Pt(4)

    # Signatures Table
    t_sig = doc.add_table(rows=1, cols=3)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    clear_table_borders(t_sig)
    w_sig = [Inches(2.5), Inches(2.5), Inches(2.5)]
    
    sigs = [
        ("__________________________\nDr Sailaja Thota\nFaculty Guide", WD_ALIGN_PARAGRAPH.LEFT),
        ("__________________________\nInternal Examiner\nSignature & Date", WD_ALIGN_PARAGRAPH.CENTER),
        ("__________________________\nExternal Examiner\nSignature & Date", WD_ALIGN_PARAGRAPH.RIGHT)
    ]
    for c_i, (txt, align) in enumerate(sigs):
        c = t_sig.rows[0].cells[c_i]
        c.width = w_sig[c_i]
        p = c.paragraphs[0]
        p.alignment = align
        p.text = txt
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(9.0)

    out_docx = r"C:\Users\sumit\Downloads\Major_Project_Phase1_Evaluation_Sheet.docx"
    doc.save(out_docx)
    print(f"Evaluation sheet saved: {out_docx}")

    # Convert to PDF
    try:
        import win32com.client
        w = win32com.client.Dispatch("Word.Application")
        w.Visible = False
        doc_c = w.Documents.Open(os.path.abspath(out_docx), ReadOnly=True)
        out_pdf = r"C:\Users\sumit\Downloads\Major_Project_Phase1_Evaluation_Sheet.pdf"
        doc_c.ExportAsFixedFormat(os.path.abspath(out_pdf), 17)
        doc_c.Close(False)
        w.Quit()
        print(f"Evaluation sheet PDF saved: {out_pdf}")
    except Exception as e:
        print(f"PDF export note: {e}")

if __name__ == "__main__":
    build_evaluation_sheet()
