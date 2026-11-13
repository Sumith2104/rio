import os

with open('redesign_report.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Normal style config
normal_cfg = '''    doc = Document()
    
    # Configure Normal Style for consistent font, size, justification, and line spacing
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(10)
    style_normal.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(4)'''

if 'style_normal = doc.styles' not in content:
    content = content.replace('    doc = Document()', normal_cfg, 1)

# 2. Page break after Table 0
old_t0_end = '''    for r_idx, (k, v) in enumerate(t0_data):
        style_data_row(t0.rows[r_idx + 1], [k, v], widths_t0, is_zebra=False, font_size=9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)'''

new_t0_end = '''    for r_idx, (k, v) in enumerate(t0_data):
        style_data_row(t0.rows[r_idx + 1], [k, v], widths_t0, is_zebra=False, font_size=9.5)

    # Executive Cover Page complete: start Section 1 on fresh page
    doc.add_page_break()'''

if old_t0_end in content:
    content = content.replace(old_t0_end, new_t0_end, 1)

# 3. Justify p11
old_p11 = '''    p11.paragraph_format.line_spacing = 1.15
    p11.paragraph_format.space_after = Pt(8)'''
new_p11 = '''    p11.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p11.paragraph_format.line_spacing = 1.15
    p11.paragraph_format.space_after = Pt(8)'''
content = content.replace(old_p11, new_p11, 1)

# 4. Justify p13
old_p13 = '''    p13.paragraph_format.line_spacing = 1.15
    p13.paragraph_format.space_after = Pt(8)'''
new_p13 = '''    p13.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p13.paragraph_format.line_spacing = 1.15
    p13.paragraph_format.space_after = Pt(8)'''
content = content.replace(old_p13, new_p13, 1)

# 5. Justify p21
old_p21 = '''    p21.paragraph_format.line_spacing = 1.15
    p21.paragraph_format.space_after = Pt(8)'''
new_p21 = '''    p21.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p21.paragraph_format.line_spacing = 1.15
    p21.paragraph_format.space_after = Pt(8)'''
content = content.replace(old_p21, new_p21, 1)

# 6. Justify p_d
old_pd = '''    for d in decisions:
        p_d = doc.add_paragraph(d)
        p_d.paragraph_format.left_indent = Inches(0.2)
        p_d.paragraph_format.line_spacing = 1.15
        p_d.paragraph_format.space_after = Pt(4)'''
new_pd = '''    for d in decisions:
        p_d = doc.add_paragraph(d)
        p_d.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_d.paragraph_format.left_indent = Inches(0.2)
        p_d.paragraph_format.line_spacing = 1.15
        p_d.paragraph_format.space_after = Pt(4)'''
content = content.replace(old_pd, new_pd, 1)

# 7. Justify p_feat
old_pfeat = '''    for title, desc in features:
        p_feat = doc.add_paragraph()
        p_feat.paragraph_format.left_indent = Inches(0.2)
        p_feat.paragraph_format.line_spacing = 1.15
        p_feat.paragraph_format.space_after = Pt(4)'''
new_pfeat = '''    for title, desc in features:
        p_feat = doc.add_paragraph()
        p_feat.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_feat.paragraph_format.left_indent = Inches(0.2)
        p_feat.paragraph_format.line_spacing = 1.15
        p_feat.paragraph_format.space_after = Pt(4)'''
content = content.replace(old_pfeat, new_pfeat, 1)

# 8. Justify p33
old_p33 = '''    p33.paragraph_format.line_spacing = 1.15
    p33.paragraph_format.space_after = Pt(8)'''
new_p33 = '''    p33.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p33.paragraph_format.line_spacing = 1.15
    p33.paragraph_format.space_after = Pt(8)'''
content = content.replace(old_p33, new_p33, 1)

# 9. Justify p_dev
old_pdev = '''    for dev in deviations:
        p_dev = doc.add_paragraph(dev)
        p_dev.paragraph_format.left_indent = Inches(0.2)
        p_dev.paragraph_format.line_spacing = 1.15
        p_dev.paragraph_format.space_after = Pt(4)'''
new_pdev = '''    for dev in deviations:
        p_dev = doc.add_paragraph(dev)
        p_dev.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_dev.paragraph_format.left_indent = Inches(0.2)
        p_dev.paragraph_format.line_spacing = 1.15
        p_dev.paragraph_format.space_after = Pt(4)'''
content = content.replace(old_pdev, new_pdev, 1)

# 10. Justify p42
old_p42 = '''    p42.paragraph_format.line_spacing = 1.15
    p42.paragraph_format.space_after = Pt(8)'''
new_p42 = '''    p42.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p42.paragraph_format.line_spacing = 1.15
    p42.paragraph_format.space_after = Pt(8)'''
content = content.replace(old_p42, new_p42, 1)

# 11. Justify p44
old_p44 = '''    p44.paragraph_format.line_spacing = 1.15
    p44.paragraph_format.space_after = Pt(8)'''
new_p44 = '''    p44.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p44.paragraph_format.line_spacing = 1.15
    p44.paragraph_format.space_after = Pt(8)'''
content = content.replace(old_p44, new_p44, 1)

# 12. Justify p51, p53, p_v, p_dec
old_p51 = '''    p51.paragraph_format.line_spacing = 1.15
    p51.paragraph_format.space_after = Pt(8)'''
new_p51 = '''    p51.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p51.paragraph_format.line_spacing = 1.15
    p51.paragraph_format.space_after = Pt(4)'''
content = content.replace(old_p51, new_p51, 1)

old_p53 = '''    p53.paragraph_format.line_spacing = 1.15
    p53.paragraph_format.space_after = Pt(8)'''
new_p53 = '''    p53.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p53.paragraph_format.line_spacing = 1.15
    p53.paragraph_format.space_after = Pt(4)'''
content = content.replace(old_p53, new_p53, 1)

old_pv = '''    for q_title, q_desc in viva_items:
        p_v = doc.add_paragraph()
        p_v.paragraph_format.left_indent = Inches(0.2)
        p_v.paragraph_format.line_spacing = 1.15
        p_v.paragraph_format.space_after = Pt(4)'''
new_pv = '''    for q_title, q_desc in viva_items:
        p_v = doc.add_paragraph()
        p_v.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_v.paragraph_format.left_indent = Inches(0.2)
        p_v.paragraph_format.line_spacing = 1.15
        p_v.paragraph_format.space_after = Pt(2)'''
content = content.replace(old_pv, new_pv, 1)

old_pdec = '''    h_dec = doc.add_heading("Declaration", level=2)
    h_dec.paragraph_format.space_before = Pt(12)
    h_dec.paragraph_format.space_after = Pt(4)

    p_dec = doc.add_paragraph("We declare that this report is our own work and that the evidence uploaded is genuine.")
    p_dec.paragraph_format.line_spacing = 1.15
    p_dec.paragraph_format.space_after = Pt(10)'''

new_pdec = '''    h_dec = doc.add_heading("Declaration", level=2)
    h_dec.paragraph_format.keep_with_next = True
    h_dec.paragraph_format.space_before = Pt(8)
    h_dec.paragraph_format.space_after = Pt(2)

    p_dec = doc.add_paragraph("We declare that this report is our own work and that the evidence uploaded is genuine.")
    p_dec.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dec.paragraph_format.keep_with_next = True
    p_dec.paragraph_format.line_spacing = 1.15
    p_dec.paragraph_format.space_after = Pt(6)'''
content = content.replace(old_pdec, new_pdec, 1)

# Keep headings with next
headings_to_keep = [
    'h1 = doc.add_heading',
    'h2 = doc.add_heading',
    'h3 = doc.add_heading',
    'h4 = doc.add_heading',
    'h5 = doc.add_heading',
    'h_meta = doc.add_heading',
    'p11_head = doc.add_paragraph()',
    'p12_head = doc.add_paragraph()',
    'p13_head = doc.add_paragraph()',
    'p14_head = doc.add_paragraph()',
    'p21_head = doc.add_paragraph()',
    'p22_head = doc.add_paragraph()',
    'p23_head = doc.add_paragraph()',
    'p24_head = doc.add_paragraph()',
    'p31_head = doc.add_paragraph()',
    'p32_head = doc.add_paragraph()',
    'p33_head = doc.add_paragraph()',
    'p34_head = doc.add_paragraph()',
    'p41_head = doc.add_paragraph()',
    'p42_head = doc.add_paragraph()',
    'p43_head = doc.add_paragraph()',
    'p44_head = doc.add_paragraph()',
    'p51_head = doc.add_paragraph()',
    'p52_head = doc.add_paragraph()',
    'p53_head = doc.add_paragraph()',
    'p54_head = doc.add_paragraph()',
]
for h in headings_to_keep:
    if h in content:
        varname = h.split(' = ')[0].strip()
        keep_line = f'    {varname}.paragraph_format.keep_with_next = True'
        if keep_line not in content:
            content = content.replace(h, f'{h}\n{keep_line}')

with open('redesign_report.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated redesign_report.py successfully!')

