import re

with open("faculty.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix CSS / inline style for views
html = html.replace(
    'id="faculty-login-view" style="display: none !important;',
    'id="faculty-login-view" style="display: flex;'
)
html = html.replace(
    'id="faculty-dashboard-view" style="display: block !important;"',
    'id="faculty-dashboard-view" style="display: none;"'
)

# 2. Make Password mode default and hide OTP mode initially
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

# 3. Add error message box to faculty login card
if 'id="faculty-login-error"' not in html:
    html = html.replace(
        '<form id="faculty-login-form" onsubmit="handleFacultyPasswordLogin(event)">',
        '<div id="faculty-login-error" style="display: none; background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; margin-bottom: 1rem; text-align: left;"></div>\n          <form id="faculty-login-form" onsubmit="handleFacultyPasswordLogin(event)">'
    )

# 4. Remove Quick Select Demo Faculty chips and title
html = re.sub(
    r'<div class="login-presets-title">Quick Select Demo Faculty</div>\s*<div class="quick-preset-chips">[\s\S]*?</div>\s*</div>\s*</div>',
    '</div>\n      </div>',
    html
)

with open("faculty.html", "w", encoding="utf-8") as f:
    f.write(html)

print("faculty.html cleaned of mock chips and updated for proper auth!")

