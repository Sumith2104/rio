from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
    page.on("response", lambda res: print(f"[HTTP {res.status}] {res.url}") if "api" in res.url else None)

    page.goto("http://localhost:8000/student.html")
    page.fill("#login-srn", "R24EA895")
    page.fill("#login-pwd", "password123")
    page.click("#student-login-form button[type='submit']")
    page.wait_for_timeout(3000)

    err = page.locator("#student-login-error").inner_text()
    print("Error element text:", err)
    dash_vis = page.locator("#student-dashboard-view").is_visible()
    print("Dashboard visible?", dash_vis)

    browser.close()

