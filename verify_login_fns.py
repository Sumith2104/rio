with open('js/student.js', 'r', encoding='utf-8') as f:
    c = f.read()
import re
print("student login fn:\n", re.search(r'async function handleStudentLogin.*?\{.*?\n\}', c, re.DOTALL).group(0)[:300])

with open('js/faculty.js', 'r', encoding='utf-8') as f:
    c2 = f.read()
print("faculty login fn:\n", re.search(r'async function handleFacultyPasswordLogin.*?\{.*?\n\}', c2, re.DOTALL).group(0)[:300])

