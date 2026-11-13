import re

with open('redesign_report.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Ensure NO page breaks anywhere in the document
# Replace all active doc.add_page_break() with comments
text = re.sub(r'(?<!#\s)doc\.add_page_break\(\)', '# doc.add_page_break()', text)

# 2. Update default figure width in add_figure_with_frame
text = re.sub(r'def add_figure_with_frame\([^)]+\):', 
              'def add_figure_with_frame(doc, img_path, fig_num, title, description, width=Inches(4.2)):', 
              text)

# 3. For Fig 6 (modal card), make width=Inches(3.4)
old_fig6 = 'add_figure_with_frame(doc, get_img("verified_faculty_batch_ingestion_modal.png"), 6,'
new_fig6 = 'add_figure_with_frame(doc, get_img("verified_faculty_batch_ingestion_modal.png"), 6,\n                          "Automated Batch IA Marks Ingestion by Section Modal",\n                          "Instructor interface for batch ingesting Internal Assessment (IA) section-wise question marks across the student cohort (including Shreehari R23EA116 and Sumith U R24EA807) featuring CSV template download, real-time table rendering, automated deficit evaluation (<50%), and ML risk recalibration.",\n                          width=Inches(3.4))\n    #'
# Let's replace the whole fig 6 call cleanly
fig6_pattern = r'add_figure_with_frame\(doc,\s*get_img\("verified_faculty_batch_ingestion_modal\.png"\),\s*6,.*?\)'
replacement_fig6 = '''add_figure_with_frame(doc, get_img("verified_faculty_batch_ingestion_modal.png"), 6,
                          "Automated Batch IA Marks Ingestion by Section Modal",
                          "Instructor interface for batch ingesting Internal Assessment (IA) section-wise question marks across the student cohort (including Shreehari R23EA116 and Sumith U R24EA807) featuring CSV template download, real-time table rendering, automated deficit evaluation (<50%), and ML risk recalibration.",
                          width=Inches(3.4))'''
text = re.sub(fig6_pattern, replacement_fig6, text, flags=re.DOTALL)

# 4. Spacing inside add_figure_with_frame
old_sp = '''    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(6)'''

new_sp = '''    p_img.paragraph_format.space_before = Pt(3)
    p_img.paragraph_format.space_after = Pt(1)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(4)'''
text = text.replace(old_sp, new_sp)

# 5. Save updated redesign_report.py
with open('redesign_report.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('apply_tight_fill.py applied successfully!')

