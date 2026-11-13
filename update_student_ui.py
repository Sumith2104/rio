import re

with open("student.html", "r", encoding="utf-8") as f:
    stu_html = f.read()

# 1. Clean up login view to only pure password login
# Remove any OTP toggles or forms if present
stu_html = re.sub(r'<!-- Auth Mode Toggle -->.*?</div>\s*</div>', '', stu_html, flags=re.DOTALL)
stu_html = re.sub(r'<div id="stu-otp-mode".*?</div>\s*</div>\s*</div>', '', stu_html, flags=re.DOTALL)

# 2. Add IA Diagnostic Panel right before Course Learning Materials
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

target_learning = '<!-- 2. Course Learning Materials & Lecture Notes'
if target_learning in stu_html and "panel-ia-diagnostics" not in stu_html:
    stu_html = stu_html.replace(target_learning, diag_panel_html + "\n      " + target_learning)
    print("Added IA Diagnostic Panel to student.html.")
elif "panel-ia-diagnostics" not in stu_html:
    # Fallback to before Counterfactual simulator
    target_sim = '<!-- 3. COUNTERFACTUAL SIMULATOR'
    if target_sim in stu_html:
        stu_html = stu_html.replace(target_sim, diag_panel_html + "\n      " + target_sim)
        print("Added IA Diagnostic Panel before simulator in student.html.")

# 3. Add Explain Weak Topic Modal before </body>
modal_weak_html = '''
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

if "modal-explain-weak-topic" not in stu_html:
    stu_html = stu_html.replace("</body>", modal_weak_html + "\n</body>")
    print("Added modal-explain-weak-topic to student.html.")

with open("student.html", "w", encoding="utf-8") as f:
    f.write(stu_html)
print("student.html updated.")

