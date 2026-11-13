import glob, re

emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]')

for f in ['student.html', 'faculty.html', 'index.html', 'js/student.js', 'js/faculty.js', 'js/app.js']:
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
        matches = emoji_pattern.findall(c)
        if matches:
            print(f"{f} has {len(matches)} emojis: {matches[:5]}")
        else:
            print(f"{f}: 0 emojis (CLEAN)")
    except Exception as e:
        print(f"{f} error: {e}")

