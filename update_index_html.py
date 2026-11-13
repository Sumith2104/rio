import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Clean style overrides
html = re.sub(
    r"#student-login-view\s*\{[^}]*\}",
    """#student-login-view {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: calc(100vh - 160px);
      width: 100%;
    }""",
    html
)

html = re.sub(
    r"#student-dashboard-view\s*\{[^}]*\}",
    """#student-dashboard-view {
      display: none;
    }""",
    html
)

html = html.replace('id="student-login-view" style="display: none !important;">', 'id="student-login-view">')
html = html.replace('id="student-dashboard-view" style="display: block !important;">', 'id="student-dashboard-view" style="display: none;">')
html = html.replace('id="faculty-login-view" style="display: none !important;', 'id="faculty-login-view" style="display: flex;')
html = html.replace('id="faculty-dashboard-view" style="display: block !important;"', 'id="faculty-dashboard-view" style="display: none;"')

# 2. Make Password mode default and hide OTP mode initially in index.html
html = html.replace('id="stu-pwd-mode" style="display: none;"', 'id="stu-pwd-mode" style="display: block;"')
html = html.replace('id="stu-otp-mode"', 'id="stu-otp-mode" style="display: none;"')
html = html.replace(
    'id="stu-tab-otp" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: #000; color: #fff;',
    'id="stu-tab-otp" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: transparent; color: var(--text-muted);'
)
html = html.replace(
    'id="stu-tab-pwd" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: transparent; color: var(--text-muted);',
    'id="stu-tab-pwd" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: #000; color: #fff;'
)

html = html.replace('id="fac-pwd-mode" style="display: none;"', 'id="fac-pwd-mode" style="display: block;"')
html = html.replace('id="fac-otp-mode"', 'id="fac-otp-mode" style="display: none;"')
html = html.replace(
    'id="fac-tab-otp" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: #000; color: #fff;',
    'id="fac-tab-otp" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: transparent; color: var(--text-muted);'
)
html = html.replace(
    'id="fac-tab-pwd" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: transparent; color: var(--text-muted);',
    'id="fac-tab-pwd" type="button" style="flex: 1; border: none; font-size: 12px; font-weight: 600; background: #000; color: #fff;'
)

# 3. Add error message boxes
if 'id="student-login-error"' not in html:
    html = html.replace(
        '<form id="student-login-form" onsubmit="handleStudentLogin(event)">',
        '<div id="student-login-error" style="display: none; background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; margin-bottom: 1rem; text-align: left;"></div>\n          <form id="student-login-form" onsubmit="handleStudentLogin(event)">'
    )
if 'id="faculty-login-error"' not in html:
    html = html.replace(
        '<form id="faculty-login-form" onsubmit="handleFacultyPasswordLogin(event)">',
        '<div id="faculty-login-error" style="display: none; background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; margin-bottom: 1rem; text-align: left;"></div>\n          <form id="faculty-login-form" onsubmit="handleFacultyPasswordLogin(event)">'
    )

# 4. Remove Quick Select Demo chips and titles
html = re.sub(
    r'<div class="login-presets-title">Quick Select Demo Students</div>\s*<div class="quick-preset-chips">[\s\S]*?</div>\s*</div>\s*</div>',
    '</div>\n        </div>',
    html
)
html = re.sub(
    r'<div class="login-presets-title">Quick Select Demo Faculty</div>\s*<div class="quick-preset-chips">[\s\S]*?</div>\s*</div>\s*</div>',
    '</div>\n        </div>',
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html cleaned of mock chips and updated for proper auth!")

