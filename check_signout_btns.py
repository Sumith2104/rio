import glob

for f in ['student.html', 'faculty.html', 'index.html']:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    print(f, "has studentSignOut?", "studentSignOut" in c, "has facultySignOut?", "facultySignOut" in c)

