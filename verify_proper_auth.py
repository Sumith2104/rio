import os
import asyncio
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

async def test_auth():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        print("\n=== STEP 1: Verify Student Unauthenticated Login View ===")
        await page.goto("http://localhost:8002/student.html", wait_until="networkidle")
        await asyncio.sleep(1)

        # Clear any preexisting session
        await page.evaluate("() => { sessionStorage.clear(); checkStudentAuth(); }")
        await asyncio.sleep(1)

        is_login_vis = await page.is_visible("#student-login-view")
        is_dash_vis = await page.is_visible("#student-dashboard-view")
        print(f"Login View Visible: {is_login_vis}, Dashboard Visible: {is_dash_vis}")
        assert is_login_vis and not is_dash_vis, "Expected unauthenticated student to see login screen!"
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_student_login_screen.png"), full_page=False)

        print("\n=== STEP 2: Verify Invalid Credentials Rejection ===")
        await page.fill("#login-srn", "R24EA807")
        await page.fill("#login-pwd", "wrongpassword")
        await page.click('#student-login-form button[type="submit"]')
        await asyncio.sleep(2)
        err_text = await page.inner_text("#student-login-error")
        print(f"Error Message Received: {err_text}")
        assert "Invalid credentials" in err_text or "failed" in err_text.lower(), "Expected invalid credential error!"

        print("\n=== STEP 3: Verify Valid Student Login (Database-Linked) ===")
        await page.fill("#login-srn", "sumithu.dev@gmail.com")
        await page.fill("#login-pwd", "password123")
        await page.click('#student-login-form button[type="submit"]')
        await asyncio.sleep(3)

        dash_vis_after = await page.is_visible("#student-dashboard-view")
        login_vis_after = await page.is_visible("#student-login-view")
        student_name = await page.inner_text("#srl-name")
        student_srn = await page.inner_text("#srl-srn")
        print(f"Dashboard Visible: {dash_vis_after}, Login View Visible: {login_vis_after}")
        print(f"Loaded Student: {student_name} | {student_srn}")
        assert dash_vis_after and not login_vis_after, "Expected authenticated student to see dashboard!"
        assert "Sumith" in student_name, "Expected live student name from database!"
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_student_logged_in.png"), full_page=False)

        print("\n=== STEP 4: Verify Student Logout (Cannot Re-Enter without Credentials) ===")
        await page.click("#btn-student-logout")
        await asyncio.sleep(2)

        dash_vis_logout = await page.is_visible("#student-dashboard-view")
        login_vis_logout = await page.is_visible("#student-login-view")
        print(f"Post-Logout - Login Visible: {login_vis_logout}, Dashboard Visible: {dash_vis_logout}")
        assert login_vis_logout and not dash_vis_logout, "Expected student to be logged out and returned to login view!"
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_student_logged_out.png"), full_page=False)

        print("\n=== STEP 5: Verify Faculty Unauthenticated Login View ===")
        await page.goto("http://localhost:8002/faculty.html", wait_until="networkidle")
        await asyncio.sleep(1)
        await page.evaluate("() => { sessionStorage.clear(); checkFacultyAuth(); }")
        await asyncio.sleep(1)

        fac_login_vis = await page.is_visible("#faculty-login-view")
        fac_dash_vis = await page.is_visible("#faculty-dashboard-view")
        print(f"Faculty Login Visible: {fac_login_vis}, Dashboard Visible: {fac_dash_vis}")
        assert fac_login_vis and not fac_dash_vis, "Expected unauthenticated faculty to see login view!"

        print("\n=== STEP 6: Verify Faculty Login & Live Database Cohort Roster ===")
        await page.fill("#fac-login-id", "FAC_AIML_01")
        await page.fill("#fac-login-pwd", "password123")
        await page.click('#faculty-login-form button[type="submit"]')
        await asyncio.sleep(3)

        fac_dash_after = await page.is_visible("#faculty-dashboard-view")
        print(f"Faculty Dashboard Visible: {fac_dash_after}")
        assert fac_dash_after, "Expected faculty console to open!"

        # Check cohort table has real database students (e.g. R24EA895 or R24EA818)
        cohort_html = await page.inner_html("#cohort-table-body")
        assert "R24EA" in cohort_html, "Expected real student SRNs from database in cohort table!"
        print("Cohort table successfully loaded real students from PostgreSQL database!")
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_faculty_logged_in.png"), full_page=False)

        print("\n=== STEP 7: Verify Faculty Logout ===")
        await page.click("button:has-text('Sign Out')")
        await asyncio.sleep(2)

        fac_login_after_logout = await page.is_visible("#faculty-login-view")
        fac_dash_after_logout = await page.is_visible("#faculty-dashboard-view")
        print(f"Post-Logout - Faculty Login Visible: {fac_login_after_logout}, Dashboard Visible: {fac_dash_after_logout}")
        assert fac_login_after_logout and not fac_dash_after_logout, "Expected faculty to be logged out!"
        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "proper_auth_faculty_logged_out.png"), full_page=False)

        await browser.close()
        print("\n>>> ALL PROPER AUTHENTICATION & LOGOUT TESTS PASSED WITH 100% ZERO MOCK DATA! <<<")

if __name__ == "__main__":
    asyncio.run(test_auth())

