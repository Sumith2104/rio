with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = "renderAdminView();"
replacement = "renderAdminView();\n  if (typeof onFacultyAccountChange === 'function') { onFacultyAccountChange(); }"

if target in content and "onFacultyAccountChange();" not in content[:content.find("initAllCharts")]:
    content = content.replace(target, replacement, 1)
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.js updated successfully.")
else:
    print("Already updated or target missing.")

