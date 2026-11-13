import os
import asyncio
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

async def test_auth():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        page.on("console", lambda msg: print(f"[CONSOLE] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGEERROR] {err}"))

        print("\n=== STEP 1: Verify Student Unauthenticated Login View ===")
        await page.goto("http://localhost:8002/student.html", wait_until="networkidle")
        await asyncio.sleep(1)

        await page.evaluate("() => { sessionStorage.clear(); checkStudentAuth(); }")
        await asyncio.sleep(1)

        is_login_vis = await page.is_visible("#student-login-view")
        is_dash_vis = await page.is_visible("#student-dashboard-view")
        print(f"Login View Visible: {is_login_vis}, Dashboard Visible: {is_dash_vis}")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_student_login_screen.png"), full_page=False)

        print("\n=== STEP 2: Verify Invalid Credentials Rejection ===")
        await page.fill("#login-srn", "R24EA807")
        await page.fill("#login-pwd", "wrongpassword")
        
        # Trigger login
        print("Clicking submit button...")
        await page.click('#student-login-form button[type="submit"]')
        await asyncio.sleep(2)

        err_vis = await page.is_visible("#student-login-error")
        err_text = await page.inner_text("#student-login-error") if err_vis else "NOT VISIBLE"
        print(f"Error Visible: {err_vis}, Text: '{err_text}'")

        print("\n=== STEP 3: Verify Valid Student Login ===")
        await page.fill("#login-srn", "sumithu.dev@gmail.com")
        await page.fill("#login-pwd", "password123")
        await page.click('#student-login-form button[type="submit"]')
        await asyncio.sleep(2)

        dash_vis = await page.is_visible("#student-dashboard-view")
        login_vis = await page.is_visible("#student-login-view")
        student_name = await page.inner_text("#srl-name")
        print(f"Dashboard Visible: {dash_vis}, Login Visible: {login_vis}, Student: '{student_name}'")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_student_logged_in.png"), full_page=False)

        print("\n=== STEP 4: Verify Student Logout ===")
        await page.click("#btn-student-logout")
        await asyncio.sleep(1)

        dash_vis_out = await page.is_visible("#student-dashboard-view")
        login_vis_out = await page.is_visible("#student-login-view")
        print(f"Post-Logout - Login Visible: {login_vis_out}, Dashboard Visible: {dash_vis_out}")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_student_logged_out.png"), full_page=False)

        print("\n=== STEP 5: Verify Faculty Login & Live Cohort ===")
        await page.goto("http://localhost:8002/faculty.html", wait_until="networkidle")
        await page.evaluate("() => { sessionStorage.clear(); checkFacultyAuth(); }")
        await asyncio.sleep(1)

        await page.fill("#fac-login-id", "FAC_AIML_01")
        await page.fill("#fac-login-pwd", "password123")
        await page.click('#faculty-login-form button[type="submit"]')
        await asyncio.sleep(2)

        fac_dash = await page.is_visible("#faculty-dashboard-view")
        cohort_html = await page.inner_html("#cohort-table-body")
        has_real_srn = "R24EA" in cohort_html
        print(f"Faculty Dashboard Visible: {fac_dash}, Cohort has real SRNs: {has_real_srn}")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_faculty_logged_in.png"), full_page=False)

        print("\n=== STEP 6: Verify Faculty Logout ===")
        await page.click("button:has-text('Sign Out')")
        await asyncio.sleep(1)

        fac_login_out = await page.is_visible("#faculty-login-view")
        fac_dash_out = await page.is_visible("#faculty-dashboard-view")
        print(f"Post-Logout - Faculty Login Visible: {fac_login_out}, Dashboard Visible: {fac_dash_out}")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_faculty_logged_out.png"), full_page=False)

        await browser.close()
        print("\nSUCCESS: All steps executed cleanly!")

if __name__ == "__main__":
    asyncio.run(test_auth())

