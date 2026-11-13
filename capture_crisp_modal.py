from playwright.sync_api import sync_playwright
import os

artifact_dir = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8000/faculty.html")
    page.fill("#fac-login-id", "FAC_AIML_01")
    page.fill("#fac-login-pwd", "password123")
    page.evaluate("handleFacultyPasswordLogin()")
    page.wait_for_selector("#faculty-dashboard-view", state="visible", timeout=10000)
    page.wait_for_timeout(1000)
    
    # Open Batch Ingestion Modal
    page.click("#btn-run-batch-pipeline")
    page.wait_for_selector("#batch-ia-marks-modal", state="visible")
    page.wait_for_timeout(1500)
    
    # Screenshot modal
    page.screenshot(path=os.path.join(artifact_dir, "verified_faculty_batch_ingestion_modal.png"))
    print("Saved crisp verified_faculty_batch_ingestion_modal.png!")

    # Click submit pipeline to also capture clean executed telemetry
    page.click("#btn-submit-batch-pipeline")
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(artifact_dir, "verified_faculty_batch_ingestion_executed.png"))
    print("Saved crisp verified_faculty_batch_ingestion_executed.png!")

    browser.close()

