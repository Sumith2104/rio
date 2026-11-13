from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))
    page.on("request", lambda req: print(f"[REQ] {req.method} {req.url}") if "api" in req.url else None)

    page.goto("http://localhost:8000/student.html")
    page.wait_for_selector("#student-login-view", state="visible")

    print("Evaluating handleStudentLogin directly in browser:")
    eval_res = page.evaluate("""() => {
        return typeof window.handleStudentLogin;
    }""")
    print("typeof handleStudentLogin:", eval_res)

    page.fill("#login-srn", "R24EA895")
    page.fill("#login-pwd", "password123")
    
    print("Calling handleStudentLogin via page.evaluate()...")
    res = page.evaluate("""async () => {
        try {
            await handleStudentLogin();
            return {
                auth: sessionStorage.getItem('student_authenticated'),
                sid: sessionStorage.getItem('active_student_id'),
                dashDisplay: document.getElementById('student-dashboard-view').style.display
            };
        } catch (e) {
            return { error: e.message, stack: e.stack };
        }
    }""")
    print("Evaluation result:", res)

    browser.close()

