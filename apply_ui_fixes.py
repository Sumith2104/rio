import re

# 1. FIX index.html
with open("index.html", "r", encoding="utf-8") as f:
    idx_content = f.read()

# Remove style.css link
idx_content = idx_content.replace('<link rel="stylesheet" href="css/style.css">', '<!-- style.css removed for clean glassmorphism -->')

# Remove hardcoded credentials from inputs
idx_content = idx_content.replace('value="STU-807"', '')
idx_content = idx_content.replace('value="password123"', '')
idx_content = idx_content.replace('value="FAC_AIML_01"', '')

# Remove redundant Sign Out button in student profile
redundant_btn_stu = '''          <button class="btn-outline" style="font-size: 12px; padding: 6px 12px; display: inline-flex; align-items: center; gap: 5px;" onclick="studentSignOut()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Sign Out
          </button>'''

idx_content = idx_content.replace(redundant_btn_stu, '')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx_content)
print("index.html updated successfully!")


# 2. FIX student.html
with open("student.html", "r", encoding="utf-8") as f:
    stu_content = f.read()

# Remove hardcoded credentials
stu_content = stu_content.replace('value="STU-807"', '')
stu_content = stu_content.replace('value="password123"', '')

# Remove redundant Sign Out button
stu_redundant = '<button class="btn-outline" style="font-size: 11px; padding: 4px 10px;" onclick="studentSignOut()">Sign Out</button>'
stu_content = stu_content.replace(stu_redundant, '')

with open("student.html", "w", encoding="utf-8") as f:
    f.write(stu_content)
print("student.html updated successfully!")


# 3. FIX faculty.html
with open("faculty.html", "r", encoding="utf-8") as f:
    fac_content = f.read()

# Remove hardcoded credentials
fac_content = fac_content.replace('value="FAC_AIML_01"', '')
fac_content = fac_content.replace('value="password123"', '')

# Remove redundant Sign Out button
fac_redundant = '''          <button id="btn-faculty-logout" class="btn-outline" style="font-size: 12px; padding: 6px 12px; display: inline-flex; align-items: center; gap: 5px;" onclick="facultySignOut()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
            Sign Out
          </button>'''
fac_content = fac_content.replace(fac_redundant, '')

with open("faculty.html", "w", encoding="utf-8") as f:
    f.write(fac_content)
print("faculty.html updated successfully!")


# 4. FIX js/faculty.js action button styling
with open("js/faculty.js", "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace harsh colored buttons with sleek monochrome glass buttons
js_content = js_content.replace('background: #ef4444; border-color: #ef4444;', 'background: #18181b; border-color: #27272a;')
js_content = js_content.replace('background: #7c3aed; border-color: #7c3aed;', 'background: #000000; border-color: #000000;')

with open("js/faculty.js", "w", encoding="utf-8") as f:
    f.write(js_content)
print("js/faculty.js updated with sleek monochrome button styling!")

