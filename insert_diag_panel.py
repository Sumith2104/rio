diag_panel_html = '''
      <!-- SECTION: INTERNAL ASSESSMENT (IA) DIAGNOSTIC PERFORMANCE & PREREQUISITE GAPS -->
      <div class="glass-panel" style="margin-bottom: 1.5rem;" id="panel-ia-diagnostics">
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

# 1. Update student.html
with open('student.html', 'r', encoding='utf-8') as f:
    stu_content = f.read()

target = '<!-- SECTION 1: Course Assignments & Handwritten Photo AI Evaluation -->'
if target in stu_content and 'panel-ia-diagnostics' not in stu_content:
    stu_content = stu_content.replace(target, diag_panel_html + "\n      " + target)
    with open('student.html', 'w', encoding='utf-8') as f:
        f.write(stu_content)
    print("Inserted panel-ia-diagnostics into student.html.")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

if target in idx_content and 'panel-ia-diagnostics' not in idx_content:
    idx_content = idx_content.replace(target, diag_panel_html + "\n      " + target)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx_content)
    print("Inserted panel-ia-diagnostics into index.html.")

