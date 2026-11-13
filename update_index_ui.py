import re

with open("index.html", "r", encoding="utf-8") as f:
    idx_html = f.read()

# 1. Remove Student OTP elements in index.html
# Replace the toggle and OTP mode in student-login-view
student_login_old = re.search(r'<!-- Auth Mode Toggle -->.*?<div id="stu-pwd-mode".*?<form id="student-login-form"', idx_html, re.DOTALL)
if student_login_old:
    clean_stu_form = '''<div id="stu-pwd-mode" style="display: block;">
            <div id="student-login-error" style="display: none; background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; margin-bottom: 1rem; text-align: left;"></div>
            <form id="student-login-form"'''
    idx_html = idx_html[:student_login_old.start()] + clean_stu_form + idx_html[student_login_old.end():]
    print("Cleaned up student login in index.html.")

# 2. Remove Faculty OTP elements in index.html
fac_login_old = re.search(r'<div style="display: flex; gap: 6px; margin-bottom: 1.25rem; background: rgba\(0,0,0,0.04\); padding: 4px; border-radius: 9px;">.*?<button id="fac-tab-otp".*?<div id="fac-pwd-mode".*?<form id="faculty-login-form"', idx_html, re.DOTALL)
if fac_login_old:
    clean_fac_form = '''<div id="fac-pwd-mode" style="display: block;">
            <div id="faculty-login-error" style="display: none; background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; margin-bottom: 1rem; text-align: left;"></div>
            <form id="faculty-login-form"'''
    idx_html = idx_html[:fac_login_old.start()] + clean_fac_form + idx_html[fac_login_old.end():]
    print("Cleaned up faculty login in index.html.")

# 3. Add IA Diagnostic Panel to student view in index.html
diag_panel_html = '''
      <!-- 2. INTERNAL ASSESSMENT (IA) DIAGNOSTIC PERFORMANCE & PREREQUISITE GAPS -->
      <div class="glass-card" style="margin-bottom: 1.5rem;" id="panel-ia-diagnostics">
        <div class="panel-header">
          <div>
            <h2>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
              </svg>
              Internal Assessment (IA) Diagnostic Performance &amp; Prerequisite Gaps
            </h2>
            <p>Section-by-section breakdown of your midterm scores. Click any weak section to diagnose the root prerequisite gap in the Knowledge Graph DAG and start your 5-Day Remedial Action Plan.</p>
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <button class="btn-black" id="stu-tab-ia-1" onclick="switchStudentIADiagnostics(1)" style="font-size: 11.5px; padding: 5px 14px; border-radius: 20px;">IA-1 Midterm</button>
            <button class="btn-outline" id="stu-tab-ia-2" onclick="switchStudentIADiagnostics(2)" style="font-size: 11.5px; padding: 5px 14px; border-radius: 20px;">IA-2 Midterm</button>
          </div>
        </div>

        <!-- Student Assessment Diagnostic Summary KPIs -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
          <div style="background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">ASSESSMENT SCORE</div>
            <div id="stu-diag-score-display" style="font-size: 20px; font-weight: 800; color: #000; margin-top: 4px;">Loading...</div>
          </div>
          <div style="background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">MASTERY STATUS</div>
            <div id="stu-diag-status-badge" style="margin-top: 6px;">Loading...</div>
          </div>
          <div style="background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">PREREQUISITE GAPS DETECTED</div>
            <div id="stu-diag-gaps-count" style="font-size: 20px; font-weight: 800; color: #dc2626; margin-top: 4px;">0 Gaps</div>
          </div>
        </div>

        <div style="overflow-x: auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Question #</th>
                <th>Topic Domain / Concept</th>
                <th>Marks Obtained</th>
                <th>Percentage</th>
                <th>Status</th>
                <th>Prerequisite Dependencies</th>
                <th>Cognitive Diagnostic</th>
              </tr>
            </thead>
            <tbody id="student-ia-diagnostics-body">
              <tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Loading section performance diagnostics...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
'''

target_student_materials = '<!-- 2. Course Learning Materials & Lecture Notes'
if target_student_materials in idx_html and "panel-ia-diagnostics" not in idx_html:
    idx_html = idx_html.replace(target_student_materials, diag_panel_html + "\n      " + target_student_materials)
    print("Added IA Diagnostic Panel to student view in index.html.")

# 4. Add QP and Batch Ingestion buttons to faculty view in index.html
btn_target = '<button class="btn-black" onclick="runAutomatedBatchPipeline()" id="btn-run-batch-pipeline">Run Batch Pipeline</button>'
qp_and_batch_btns = '''<button class="btn-black" onclick="openUploadQPModal()"><svg class="icon-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg> Upload IA Question Paper &amp; Blueprint</button>
          <button class="btn-black" onclick="openBatchIAMarksModal()" id="btn-run-batch-pipeline"><svg class="icon-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg> Batch Ingest IA Marks</button>'''

if btn_target in idx_html:
    idx_html = idx_html.replace(btn_target, qp_and_batch_btns)
    print("Added QP and Batch Ingest buttons to faculty view in index.html.")

# 5. Add Modals before <footer> in index.html
modals_all = '''
    <!-- MODAL: UPLOAD IA QUESTION PAPER & BLUEPRINT -->
    <div id="upload-qp-modal" class="modal-backdrop" style="display: none;">
      <div class="glass-modal" style="max-width: 680px; width: 95%;">
        <div class="modal-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #000; color: #fff; display: flex; align-items: center; justify-content: center;">
              <svg class="icon-svg standalone" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
            </div>
            <div>
              <h3 style="margin: 0; font-size: 15px; font-weight: 700;">Upload IA Question Paper &amp; Section Blueprint</h3>
              <p style="margin: 2px 0 0; font-size: 12px; color: var(--text-muted);">Indexes blueprint into ChromaDB and registers exam rubrics in PostgreSQL</p>
            </div>
          </div>
          <button class="btn-close" onclick="closeUploadQPModal()">&times;</button>
        </div>

        <form id="upload-qp-form" onsubmit="handleUploadQPSubmit(event)" style="padding: 1.25rem 1.5rem;">
          <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 1rem; margin-bottom: 1rem;">
            <div>
              <label style="font-size: 12px; font-weight: 600; display: block; margin-bottom: 4px;">Assessment</label>
              <select id="qp-ia-number" class="form-control" onchange="populateDefaultQPBlueprint()" style="font-size: 13px;">
                <option value="1">IA-1 (Midterm 1)</option>
                <option value="2">IA-2 (Midterm 2)</option>
              </select>
            </div>
            <div>
              <label style="font-size: 12px; font-weight: 600; display: block; margin-bottom: 4px;">Paper Title</label>
              <input type="text" id="qp-title" class="form-control" placeholder="e.g. IA-1 Question Paper &amp; Section Blueprint: Deep Learning" required style="font-size: 13px;">
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
            <div>
              <label style="font-size: 12px; font-weight: 600; display: block; margin-bottom: 4px;">Curriculum Unit Focus</label>
              <input type="text" id="qp-unit-name" class="form-control" placeholder="e.g. Unit 1 &amp; Unit 2: Differential Optimization" style="font-size: 13px;">
            </div>
            <div>
              <label style="font-size: 12px; font-weight: 600; display: block; margin-bottom: 4px;">QP Document File Name</label>
              <input type="text" id="qp-file-name" class="form-control" placeholder="e.g. IA1_Question_Paper_AIML401.pdf" style="font-size: 13px;">
            </div>
          </div>

          <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <label style="font-size: 12px; font-weight: 700;">Section-by-Section Assessment Blueprint</label>
              <span style="font-size: 11.5px; color: var(--text-muted);">Total Exam Weight: 30 pts</span>
            </div>
            <div style="background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px;">
              <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
                <thead>
                  <tr style="border-bottom: 1px solid var(--border-color); text-align: left; color: var(--text-muted);">
                    <th style="padding: 6px;">Section / Q#</th>
                    <th style="padding: 6px;">Concept Identifier</th>
                    <th style="padding: 6px;">Topic Title</th>
                    <th style="padding: 6px; text-align: right;">Max Marks</th>
                  </tr>
                </thead>
                <tbody id="qp-sections-table-body">
                </tbody>
              </table>
            </div>
          </div>

          <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 10px 14px; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 10px;">
            <svg class="icon-svg standalone" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#166534" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <div style="font-size: 11.5px; color: #166534;">
              <strong>Student Notification Enabled:</strong> Submitting will index the blueprint into ChromaDB and automatically dispatch email notification to enrolled student: <strong>sumithu.dev@gmail.com</strong>.
            </div>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 8px;">
            <button type="button" class="btn-outline" onclick="closeUploadQPModal()">Cancel</button>
            <button type="submit" class="btn-black" id="btn-submit-upload-qp">
              <svg class="icon-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
              Upload Question Paper &amp; Register Blueprint
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: BATCH IA MARKS INGESTION BY SECTION -->
    <div id="batch-ia-marks-modal" class="modal-backdrop" style="display: none;">
      <div class="glass-modal" style="max-width: 860px; width: 95%;">
        <div class="modal-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #000; color: #fff; display: flex; align-items: center; justify-content: center;">
              <svg class="icon-svg standalone" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
            </div>
            <div>
              <h3 style="margin: 0; font-size: 15px; font-weight: 700;">Batch IA Section Marks Ingestion &amp; Automated Pipeline</h3>
              <p style="margin: 2px 0 0; font-size: 12px; color: var(--text-muted);">Batch commit question-level marks to ia_question_scores, detect weak topics (&lt; 50%), and calibrate ML risk (tau=0.42)</p>
            </div>
          </div>
          <button class="btn-close" onclick="closeBatchIAMarksModal()">&times;</button>
        </div>

        <form id="batch-ia-marks-form" onsubmit="handleBatchIAMarksSubmit(event)" style="padding: 1.25rem 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <label style="font-size: 12.5px; font-weight: 600;">Target Assessment:</label>
              <select id="batch-ia-num" class="form-control" onchange="renderBatchMarksGrid()" style="font-size: 12.5px; width: 160px;">
                <option value="1">IA-1 Midterm</option>
                <option value="2">IA-2 Midterm</option>
              </select>
            </div>
            <div style="font-size: 12px; color: var(--text-muted);">
              Course: <strong style="color: #000;">AIML-401</strong> &bull; Weight: <strong>30.0 Max Marks</strong>
            </div>
          </div>

          <div style="overflow-x: auto; margin-bottom: 1.25rem; border: 1px solid var(--border-color); border-radius: 8px;">
            <table class="data-table" style="margin: 0;">
              <thead>
                <tr>
                  <th>Student SRN</th>
                  <th>Student Name</th>
                  <th id="th-batch-q1">Q1: Partial Deriv (/10)</th>
                  <th id="th-batch-q2">Q2: Chain Rule (/10)</th>
                  <th id="th-batch-q3">Q3: Backpropagation (/10)</th>
                  <th>Calculated Total</th>
                  <th>Predicted Risk Tier</th>
                </tr>
              </thead>
              <tbody id="batch-ia-table-body">
              </tbody>
            </table>
          </div>

          <div id="batch-pipeline-telemetry" style="display: none; margin-bottom: 1.25rem; background: #0f172a; color: #fff; padding: 12px 16px; border-radius: 8px; font-family: monospace; font-size: 12px; line-height: 1.6;">
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
            <div style="font-size: 11.5px; color: var(--text-muted);">
              &bull; Scores &lt; 5.0/10 (50%) automatically flag <strong style="color: #dc2626;">DEFICIT</strong> and trigger WeakTopicRAGEngine.
            </div>
            <div style="display: flex; gap: 8px;">
              <button type="button" class="btn-outline" onclick="closeBatchIAMarksModal()">Cancel</button>
              <button type="submit" class="btn-black" id="btn-submit-batch-pipeline">
                <svg class="icon-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                Execute Automated Ingestion Pipeline
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL: EXPLAIN WEAK TOPIC & PREREQUISITE ROOT CAUSE -->
    <div id="modal-explain-weak-topic" class="modal-backdrop" style="display: none;">
      <div class="glass-modal" style="max-width: 760px; width: 95%; max-height: 90vh; overflow-y: auto;">
        <div class="modal-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #000; color: #fff; display: flex; align-items: center; justify-content: center;">
              <svg class="icon-svg standalone" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <div>
              <h3 id="modal-weak-topic-title" style="margin: 0; font-size: 15px; font-weight: 700;">Question 3: Reverse-Mode Autodiff &amp; Backpropagation</h3>
              <p id="modal-weak-score-badge" style="margin: 2px 0 0; font-size: 12px; color: var(--text-muted);">Score: 2.5 / 10.0 pts (25.0% - DEFICIT)</p>
            </div>
          </div>
          <button class="btn-close" onclick="closeExplainWeakTopicModal()">&times;</button>
        </div>

        <div style="padding: 1.25rem 1.5rem;">
          <!-- 1. Executive Diagnostic Root Cause -->
          <div style="margin-bottom: 1.25rem; background: #fef2f2; border: 1px solid #fecaca; border-left: 4px solid #dc2626; border-radius: 8px; padding: 12px 16px;">
            <div style="font-size: 12px; font-weight: 700; color: #991b1b; text-transform: uppercase; margin-bottom: 4px;">
              Prerequisite Knowledge Graph DAG Diagnostic
            </div>
            <div id="modal-weak-root-cause" style="font-size: 13px; color: #7f1d1d; line-height: 1.5;">
              Analyzing root-cause deficit...
            </div>
          </div>

          <!-- 2. Prerequisite Concepts Gaps Trace -->
          <div style="margin-bottom: 1.25rem;">
            <h4 style="margin: 0 0 8px; font-size: 13px; font-weight: 700; color: #000;">
              Prerequisite Dependencies Required for Concept Mastery
            </h4>
            <div id="modal-weak-prereqs-container" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px;">
            </div>
          </div>

          <!-- 3. Syllabus Excerpt / Learning Objectives (ChromaDB RAG) -->
          <div style="margin-bottom: 1.25rem;">
            <h4 style="margin: 0 0 8px; font-size: 13px; font-weight: 700; color: #000;">
              Official Syllabus &amp; Course Notes Context (ChromaDB RAG)
            </h4>
            <div id="modal-weak-syllabus-box" style="background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 14px; font-size: 12.5px; color: #334155; line-height: 1.5;">
              Retrieving curriculum excerpts...
            </div>
          </div>

          <!-- 4. 5-Day Remedial Action Plan -->
          <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <h4 style="margin: 0; font-size: 13px; font-weight: 700; color: #000;">
                Synthesized 5-Day Remedial Action Plan
              </h4>
              <span style="font-size: 11px; background: #000; color: #fff; padding: 2px 8px; border-radius: 12px;">5 Days to Exam Recovery</span>
            </div>
            <div id="modal-weak-schedule-container" style="display: flex; flex-direction: column; gap: 8px;">
            </div>
          </div>

          <div style="display: flex; justify-content: flex-end; gap: 8px; border-top: 1px solid var(--border-color); padding-top: 1rem;">
            <button class="btn-outline" onclick="closeExplainWeakTopicModal()">Close</button>
            <button class="btn-black" onclick="triggerWeakTopicChatAssistant()">
              <svg class="icon-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              Ask AI Copilot about this Topic
            </button>
          </div>
        </div>
      </div>
    </div>
'''

if "upload-qp-modal" not in idx_html:
    idx_html = idx_html.replace("<footer>", modals_all + "\n  <footer>")
    print("Added modals to index.html.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx_html)
print("index.html updated.")

