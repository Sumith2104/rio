import os
import asyncio
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

async def test_full_auth():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        print("=== TEST 1: Student Unauthenticated Screen ===")
        await page.goto("http://localhost:8002/student.html", wait_until="networkidle")
        await page.evaluate("() => { sessionStorage.clear(); checkStudentAuth(); }")
        await asyncio.sleep(1)

        is_login = await page.is_visible("#student-login-view")
        is_dash = await page.is_visible("#student-dashboard-view")
        print(f"Login Screen: {is_login}, Dashboard: {is_dash}")
        assert is_login and not is_dash

        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "auth_verified_student_login_screen.png"), full_page=False)

        print("\n=== TEST 2: Student Login with Database Credentials ===")
        await page.fill("#login-srn", "sumithu.dev@gmail.com")
        await page.fill("#login-pwd", "password123")
        await page.click('#student-login-form button[type="submit"]')

        await page.wait_for_selector("#student-dashboard-view", state="visible", timeout=10000)
        await asyncio.sleep(2)

        name_text = await page.inner_text("#srl-name")
        srn_text = await page.inner_text("#srl-srn")
        att_text = await page.inner_text("#stu-kpi-att")
        print("Authenticated Student Profile:", name_text, "|", srn_text, "| Attendance:", att_text)
        assert "Sumith" in name_text and "94.5%" in att_text

        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "auth_verified_student_dashboard.png"), full_page=False)

        print("\n=== TEST 3: Student Logout & Persistence ===")
        await page.click("#btn-student-logout")
        await page.wait_for_selector("#student-login-view", state="visible", timeout=10000)
        await asyncio.sleep(1)

        is_dash_after = await page.is_visible("#student-dashboard-view")
        print(f"Dashboard Visible After Logout: {is_dash_after}")
        assert not is_dash_after

        # Refresh page to verify user remains logged out
        await page.reload(wait_until="networkidle")
        await asyncio.sleep(1)
        assert await page.is_visible("#student-login-view") and not await page.is_visible("#student-dashboard-view")
        print("Student stays securely logged out upon page reload!")

        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "auth_verified_student_logged_out.png"), full_page=False)

        print("\n=== TEST 4: Faculty Login with Database Credentials ===")
        await page.goto("http://localhost:8002/faculty.html", wait_until="networkidle")
        await page.evaluate("() => { sessionStorage.clear(); checkFacultyAuth(); }")
        await asyncio.sleep(1)

        assert await page.is_visible("#faculty-login-view") and not await page.is_visible("#faculty-dashboard-view")

        await page.fill("#fac-login-id", "FAC_AIML_01")
        await page.fill("#fac-login-pwd", "password123")
        await page.click('#faculty-login-form button[type="submit"]')

        await page.wait_for_selector("#faculty-dashboard-view", state="visible", timeout=10000)
        await page.wait_for_selector("#cohort-table-body tr td strong", state="visible", timeout=10000)
        await asyncio.sleep(2)

        badge_text = await page.inner_text("#faculty-user-badge")
        cohort_content = await page.inner_text("#cohort-table-body")
        print("Faculty Badge:", badge_text.encode("ascii", "ignore").decode())
        print("Sample Cohort Records:", [line.encode("ascii", "ignore").decode() for line in cohort_content.splitlines()[:5]])
        assert "Dr. Ramesh Kumar" in badge_text
        assert "R24EA807" in cohort_content or "R24EA818" in cohort_content

        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "auth_verified_faculty_dashboard.png"), full_page=False)

        print("\n=== TEST 5: Faculty Logout ===")
        await page.click("#btn-faculty-logout")
        await page.wait_for_selector("#faculty-login-view", state="visible", timeout=10000)
        await asyncio.sleep(1)

        fac_dash_after = await page.is_visible("#faculty-dashboard-view")
        print(f"Faculty Dashboard Visible After Logout: {fac_dash_after}")
        assert not fac_dash_after

        await page.screenshot(path=os.path.join(ARTIFACT_DIR, "auth_verified_faculty_logged_out.png"), full_page=False)

        await browser.close()
        print("\n>>> ALL 5 ADVANCED PROPER AUTHENTICATION & ZERO-MOCK TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    asyncio.run(test_full_auth())
