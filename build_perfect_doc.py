import os, shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import pymupdf

ARTIFACT_DIR = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

def get_img(name):
    p = os.path.join(ARTIFACT_DIR, name)
    return p if os.path.exists(p) else None

def set_cell_margins(cell, top=30, bottom=30, left=30, right=30):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_top_border(cell, color='CBD5E1', sz='4'):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), sz)
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), color)
    tcBorders.append(top)
    for b_name in ['left', 'bottom', 'right']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'none')
        tcBorders.append(b)
    tcPr.append(tcBorders)

def clear_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def add_dynamic_field(p, field_name, font_name='Calibri', sz_val='17', color_val='64748B'):
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), f' {field_name} ')
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    f = OxmlElement('w:rFonts')
    f.set(qn('w:ascii'), font_name)
    f.set(qn('w:hAnsi'), font_name)
    rPr.append(f)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), sz_val)
    rPr.append(sz)
    col = OxmlElement('w:color')
    col.set(qn('w:val'), color_val)
    rPr.append(col)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = '1'
    r.append(t)
    fld.append(r)
    p._p.append(fld)

def format_clean_table_footer(ftr_obj):
    """Format footer with 1-row, 2-column table: Left candidates, Right dynamic Page X of Y."""
    for p in ftr_obj.paragraphs:
        p.text = ""
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0

    # Remove existing tables in footer if any
    for t in ftr_obj.tables:
        t._element.getparent().remove(t._element)

    tbl = ftr_obj.add_table(rows=1, cols=2, width=Inches(7.0))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    c0 = tbl.cell(0, 0)
    c0.width = Inches(5.2)
    set_cell_top_border(c0, color='CBD5E1', sz='4')
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(0)
    p0.paragraph_format.line_spacing = 1.0
    r0 = p0.add_run("PACD-RAG Platform  |  Candidates: Sumith U (R24EA807) & Shreehari (R23EA116)")
    r0.font.name = 'Calibri'
    r0.font.size = Pt(8.5)
    r0.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    c1 = tbl.cell(0, 1)
    c1.width = Inches(1.8)
    set_cell_top_border(c1, color='CBD5E1', sz='4')
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(4)
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.0
    r1 = p1.add_run("Page ")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(8.5)
    r1.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    add_dynamic_field(p1, 'PAGE')
    r_of = p1.add_run(" of ")
    r_of.font.name = 'Calibri'
    r_of.font.size = Pt(8.5)
    r_of.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    add_dynamic_field(p1, 'NUMPAGES')

def build_perfect():
    src_file = r"C:\Users\sumit\Downloads\rio\PACD_RAG_Major_Project_Report_Phase1_Unified.docx"
    doc = docx.Document(src_file)

    # 1. Update footer across all sections
    for sec in doc.sections:
        sec.different_first_page_header_footer = True
        format_clean_table_footer(sec.first_page_footer)
        format_clean_table_footer(sec.footer)

    # 2. Convert stacked figures into side-by-side figure tables
    # Find figure pairs and their paragraphs
    fig_pairs = [
        (1, 2, "ui_fixed_student_dashboard_top.png", "ui_fixed_faculty_dashboard_top.png"),
        (3, 4, "verified_student_ia_diagnostics_table.png", "verified_student_weak_topic_explanation_modal.png"),
        (5, 6, "ui_fixed_faculty_dashboard_materials.png", "verified_faculty_batch_ingestion_modal.png"),
        (7, 8, "verified_faculty_batch_ingestion_executed.png", "ui_fixed_index_login.png")
    ]

    for num1, num2, img1_name, img2_name in fig_pairs:
        # Find paragraphs containing Figure num1 and Figure num2 captions
        cap1_idx = None
        cap2_idx = None
        for i, p in enumerate(doc.paragraphs):
            if p.text.startswith(f"Figure {num1}:"):
                cap1_idx = i
            elif p.text.startswith(f"Figure {num2}:"):
                cap2_idx = i

        if cap1_idx is not None and cap2_idx is not None:
            img1_p = doc.paragraphs[cap1_idx - 1]
            cap1_p = doc.paragraphs[cap1_idx]
            img2_p = doc.paragraphs[cap2_idx - 1]
            cap2_p = doc.paragraphs[cap2_idx]

            cap1_text = cap1_p.text
            cap2_text = cap2_p.text

            # Parse title and description
            def parse_cap(text, num):
                prefix = f"Figure {num}: "
                rest = text[len(prefix):] if text.startswith(prefix) else text
                if " - " in rest:
                    parts = rest.split(" - ", 1)
                    return parts[0].strip(), parts[1].strip()
                elif " — " in rest:
                    parts = rest.split(" — ", 1)
                    return parts[0].strip(), parts[1].strip()
                else:
                    return rest.strip(), ""

            t1, d1 = parse_cap(cap1_text, num1)
            t2, d2 = parse_cap(cap2_text, num2)

            # Create side-by-side table right before img1_p
            tbl = doc.add_table(rows=1, cols=2)
            tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            tbl.autofit = False
            clear_table_borders(tbl)

            col_w = Inches(3.45)
            # Cell 1
            c0 = tbl.cell(0, 0)
            c0.width = col_w
            set_cell_margins(c0, top=20, bottom=20, left=20, right=20)
            p0_img = c0.paragraphs[0]
            p0_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p0_img.paragraph_format.space_before = Pt(2)
            p0_img.paragraph_format.space_after = Pt(2)
            p0_img.paragraph_format.keep_with_next = True
            p0_img.add_run().add_picture(get_img(img1_name), width=Inches(3.25))

            p0_cap = c0.add_paragraph()
            p0_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p0_cap.paragraph_format.space_before = Pt(1)
            p0_cap.paragraph_format.space_after = Pt(2)
            p0_cap.paragraph_format.line_spacing = 1.05
            r1 = p0_cap.add_run(f"Figure {num1}: {t1}\n")
            r1.bold = True
            r1.font.name = 'Calibri'
            r1.font.size = Pt(8.5)
            r1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if d1:
                r1_d = p0_cap.add_run(f"• {d1}")
                r1_d.italic = True
                r1_d.font.name = 'Calibri'
                r1_d.font.size = Pt(7.5)
                r1_d.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

            # Cell 2
            c1 = tbl.cell(0, 1)
            c1.width = col_w
            set_cell_margins(c1, top=20, bottom=20, left=20, right=20)
            p1_img = c1.paragraphs[0]
            p1_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p1_img.paragraph_format.space_before = Pt(2)
            p1_img.paragraph_format.space_after = Pt(2)
            p1_img.paragraph_format.keep_with_next = True
            p1_img.add_run().add_picture(get_img(img2_name), width=Inches(3.25))

            p1_cap = c1.add_paragraph()
            p1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p1_cap.paragraph_format.space_before = Pt(1)
            p1_cap.paragraph_format.space_after = Pt(2)
            p1_cap.paragraph_format.line_spacing = 1.05
            r2 = p1_cap.add_run(f"Figure {num2}: {t2}\n")
            r2.bold = True
            r2.font.name = 'Calibri'
            r2.font.size = Pt(8.5)
            r2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if d2:
                r2_d = p1_cap.add_run(f"• {d2}")
                r2_d.italic = True
                r2_d.font.name = 'Calibri'
                r2_d.font.size = Pt(7.5)
                r2_d.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

            # Move tbl before img1_p in XML
            img1_p._p.addprevious(tbl._tbl)

            # Remove the old individual figure paragraphs
            for p_to_del in [img1_p, cap1_p, img2_p, cap2_p]:
                p_to_del._p.getparent().remove(p_to_del._p)

    # Save to all target paths
    target_paths = [
        r"C:\Users\sumit\Downloads\rio\report_final.docx",
        r"C:\Users\sumit\Downloads\rio\PACD_RAG_Major_Project_Report_Phase1_Unified.docx",
        r"C:\Users\sumit\Downloads\rio\PACD_RAG_Major_Project_Report_Phase1.docx",
        r"C:\Users\sumit\Downloads\rio\PACD_RAG_Major_Project_Report_Phase1_Final.docx"
    ]

    for p in target_paths:
        try:
            doc.save(p)
            print(f"Saved: {p} ({os.path.getsize(p):,} bytes)")
        except Exception as e:
            print(f"Failed to save {p}: {e}")

    # Generate reference PDF using Word COM
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        word.ScreenUpdating = False
        try:
            wdoc = word.Documents.Open(os.path.abspath(target_paths[0]), False, False, False)
            for story in wdoc.StoryRanges:
                story.Fields.Update()
            wdoc.Fields.Update()
            wdoc.Save()
            pdf_path = os.path.abspath(r"C:\Users\sumit\Downloads\rio\report_final.pdf")
            wdoc.SaveAs(pdf_path, 17) # 17 = wdFormatPDF
            wdoc.Close(False)
            print(f"Word COM PDF exported: {pdf_path}")
        finally:
            word.Quit()
    except Exception as e:
        print(f"Word COM note: {e}")

if __name__ == "__main__":
    build_perfect()

