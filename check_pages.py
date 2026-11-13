import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('report_final.docx')
for i, p in enumerate(doc.paragraphs[:15]):
    has_page_br = 'w:type="page"' in p._p.xml
    txt = p.text.strip().replace('\n', ' ')
    print(f"P{i:2d}: page_br={str(has_page_br):<5} | text={txt[:60]}")
