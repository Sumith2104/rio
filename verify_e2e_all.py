import os
import time
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\sumit\.gemini\antigravity\brain\6c071a0d-b327-4228-9609-281a735f3580"

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 950})
        page = context.new_page()

        print("\n--- STEP 1: TEST STUDENT DIRECT LOGIN WITH EMAIL (sumithu.dev@gmail.com) ---")
        page.goto("http://localhost:8000/student.html")
        page.wait_for_selector("#student-login-view", state="visible")
        
        # Verify NO OTP input is present
        otp_visible = page.locator("#stu-otp-code").is_visible()
        print("Is OTP input visible on login?", otp_visible)
        assert not otp_visible, "OTP input should NOT be visible on direct login!"

        # Fill credentials & login
        page.fill("#login-srn", "sumithu.dev@gmail.com")
        page.fill("#login-pwd", "password123")
        page.evaluate("handleStudentLogin()")

        # Wait for dashboard to unlock
        page.wait_for_selector("#student-dashboard-view", state="visible", timeout=12000)
        print("Direct Login with sumithu.dev@gmail.com successful! Dashboard unlocked.")
        page.wait_for_timeout(1000)

        # Check notification recipient display
        notif_email = page.inner_text("#stu-notif-email-display")
        print("Notification Banner Recipient:", notif_email)

        # Verify IA diagnostics panel
        page.wait_for_selector("#panel-ia-diagnostics", state="visible")
        print("IA Diagnostics panel is visible for Sumith U.")

        # Test Logout
        page.click("button:has-text('Sign Out')")
        page.wait_for_selector("#student-login-view", state="visible", timeout=6000)
        print("Sign Out successful! Back to login view.")

        print("\n--- STEP 2: TEST SNEHA PATEL (R24EA895) - WEAK TOPIC DIAGNOSTICS & EXPLANATION ---")
        page.fill("#login-srn", "R24EA895")
        page.fill("#login-pwd", "password123")
        page.evaluate("handleStudentLogin()")
        page.wait_for_selector("#student-dashboard-view", state="visible", timeout=12000)
        print("Sneha Patel logged in successfully.")

        # Wait for diagnostic data to finish loading and deficit badge to appear
        page.wait_for_selector("#stu-diag-status-badge:has-text('DEFICIT')", timeout=10000)
        status_text = page.inner_text("#stu-diag-status-badge")
        print("Mastery Status Badge:", status_text)
        assert "DEFICIT" in status_text, "Sneha should have DEFICIT DETECTED!"

        diag_rows = page.locator("#student-ia-diagnostics-body tr").count()
        print(f"IA-1 questions rendered: {diag_rows}")

        # Screenshot of IA diagnostics panel
        page.screenshot(path=os.path.join(artifact_dir, "verified_student_ia_diagnostics_table.png"))
        print("Saved verified_student_ia_diagnostics_table.png")

        # Click Explain Weak Topic & Gap on Backpropagation (Q3)
        explain_btns = page.locator("button:has-text('Explain Weak Topic & Gap')")
        print(f"Explain buttons available: {explain_btns.count()}")
        explain_btns.last.click()

        # Wait for Modal to open and load API diagnostic
        page.wait_for_selector("#modal-explain-weak-topic", state="visible")
        page.wait_for_selector("#modal-weak-root-cause:not(:has-text('Querying Knowledge Graph'))", timeout=10000)
        page.wait_for_timeout(1000)

        modal_title = page.inner_text("#modal-weak-topic-title")
        root_cause = page.inner_text("#modal-weak-root-cause")
        print("Weak Topic Modal Opened:", modal_title)
        print("Root Cause Diagnostic Preview:", root_cause[:120])

        page.screenshot(path=os.path.join(artifact_dir, "verified_student_weak_topic_explanation_modal.png"))
        print("Saved verified_student_weak_topic_explanation_modal.png")

        # Close modal
        page.click("#modal-explain-weak-topic button:has-text('Close')")
        page.wait_for_timeout(500)

        # Test asking OmniAssistant in chat
        print("\n--- STEP 3: TEST OMNI CHAT WEAK TOPIC EXPLANATION ---")
        page.fill("#omni-chat-input", "Why am I weak in backpropagation?")
        page.click("#omni-send-btn")
        page.wait_for_timeout(4000)

        chat_messages = page.inner_text("#omni-chat-log")
        print("AI Tutor Response snippet:", chat_messages[-300:])
        page.screenshot(path=os.path.join(artifact_dir, "verified_student_omni_weak_topic_chat.png"))
        print("Saved verified_student_omni_weak_topic_chat.png")

        # Sign out student
        page.click("button:has-text('Sign Out')")
        page.wait_for_selector("#student-login-view", state="visible")

        print("\n--- STEP 4: TEST FACULTY CONSOLE QP & BATCH INGESTION ---")
        page.goto("http://localhost:8000/faculty.html")
        page.wait_for_selector("#faculty-login-view", state="visible")

        # Faculty login
        page.fill("#fac-login-id", "FAC_AIML_01")
        page.fill("#fac-login-pwd", "password123")
        page.evaluate("handleFacultyPasswordLogin()")
        page.wait_for_selector("#faculty-dashboard-view", state="visible", timeout=12000)
        print("Faculty logged in successfully!")
        page.wait_for_timeout(1500)

        # Open Upload QP Modal
        print("\nOpening Upload IA Question Paper & Blueprint Modal...")
        page.click("button:has-text('Upload IA Question Paper & Blueprint')")
        page.wait_for_selector("#upload-qp-modal", state="visible")
        page.wait_for_timeout(1000)

        page.screenshot(path=os.path.join(artifact_dir, "verified_faculty_upload_qp_modal.png"))
        print("Saved verified_faculty_upload_qp_modal.png")

        # Close QP modal
        page.click("#upload-qp-modal button.btn-close")
        page.wait_for_timeout(500)

        # Open Batch Ingestion Modal
        print("\nOpening Batch Ingest IA Marks Modal...")
        page.click("button:has-text('Batch Ingest IA Marks')")
        page.wait_for_selector("#batch-ia-marks-modal", state="visible")
        page.wait_for_timeout(1000)

        page.screenshot(path=os.path.join(artifact_dir, "verified_faculty_batch_ingestion_modal.png"))
        print("Saved verified_faculty_batch_ingestion_modal.png")

        # Click Execute Automated Ingestion Pipeline
        print("Executing Automated Batch Ingestion Pipeline from modal...")
        page.click("#btn-submit-batch-pipeline")
        page.wait_for_timeout(3000)

        page.screenshot(path=os.path.join(artifact_dir, "verified_faculty_batch_ingestion_executed.png"))
        print("Saved verified_faculty_batch_ingestion_executed.png")

        # Close Batch Modal
        if page.locator("#batch-ia-marks-modal").is_visible():
            page.click("#batch-ia-marks-modal button.btn-close")
            page.wait_for_timeout(500)

        # Test Faculty Logout
        page.click("button:has-text('Sign Out')")
        page.wait_for_selector("#faculty-login-view", state="visible", timeout=6000)
        print("Faculty Sign Out successful!")

        # STEP 5: VERIFY UNIFIED PORTAL (index.html)
        print("\n--- STEP 5: TEST UNIFIED INDEX.HTML ---")
        page.goto("http://localhost:8000/")
        page.wait_for_selector("#student-login-view", state="visible")
        idx_otp_visible = page.locator("#stu-otp-code").is_visible()
        print("Is OTP visible in index.html?", idx_otp_visible)
        assert not idx_otp_visible, "OTP should NOT be visible in index.html!"

        # Direct login on index.html
        page.fill("#login-srn", "sumithu.dev@gmail.com")
        page.fill("#login-pwd", "password123")
        page.evaluate("handleStudentLogin()")
        page.wait_for_selector("#student-dashboard-view", state="visible", timeout=12000)
        print("Unified index.html Student Dashboard unlocked successfully!")

        page.screenshot(path=os.path.join(artifact_dir, "verified_unified_index_logged_in.png"))
        print("Saved verified_unified_index_logged_in.png")

        browser.close()
        print("\nALL BROWSER E2E TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    run_verification()
