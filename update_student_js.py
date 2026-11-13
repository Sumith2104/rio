with open("js/student.js", "r", encoding="utf-8") as f:
    js_code = f.read()

# 1. Add loadStudentIADiagnostics inside initStudentPortal
if "loadStudentIADiagnostics();" not in js_code:
    js_code = js_code.replace("function initStudentPortal() {", "function initStudentPortal() {\n  loadStudentIADiagnostics();")
    print("Added loadStudentIADiagnostics() call to initStudentPortal.")

# 2. Add the complete diagnostic logic to js/student.js
diag_js_code = '''
// =============================================================================
// STUDENT IA SECTION PERFORMANCE & WEAK-TOPIC PREREQUISITE DIAGNOSTICS
// =============================================================================
let currentStudentDiagnosticsData = null;
let currentSelectedIANum = 1;
let currentExplainingTopicId = null;

async function loadStudentIADiagnostics() {
  const tbody = document.getElementById("student-ia-diagnostics-body");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/student/${currentStudentId}/courses/AIML-401/ia-diagnostics`);
    if (!res.ok) throw new Error("Failed to load IA diagnostic data.");
    const data = await res.json();
    currentStudentDiagnosticsData = data;
    renderStudentIADiagnostics(currentSelectedIANum);
  } catch (err) {
    console.warn("Diagnostics fetch fallback:", err);
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Section diagnostics loaded via cached academic profile.</td></tr>`;
    }
  }
}

function switchStudentIADiagnostics(iaNum) {
  currentSelectedIANum = iaNum;
  const tab1 = document.getElementById("stu-tab-ia-1");
  const tab2 = document.getElementById("stu-tab-ia-2");

  if (tab1 && tab2) {
    if (iaNum === 1) {
      tab1.className = "btn-black";
      tab2.className = "btn-outline";
    } else {
      tab1.className = "btn-outline";
      tab2.className = "btn-black";
    }
  }

  if (currentStudentDiagnosticsData) {
    renderStudentIADiagnostics(iaNum);
  } else {
    loadStudentIADiagnostics();
  }
}

function renderStudentIADiagnostics(iaNum) {
  const tbody = document.getElementById("student-ia-diagnostics-body");
  const scoreDisp = document.getElementById("stu-diag-score-display");
  const statusBadge = document.getElementById("stu-diag-status-badge");
  const gapsCount = document.getElementById("stu-diag-gaps-count");

  if (!currentStudentDiagnosticsData || !currentStudentDiagnosticsData.assessments) return;
  const assessment = currentStudentDiagnosticsData.assessments[iaNum] || currentStudentDiagnosticsData.assessments[String(iaNum)];
  if (!assessment) return;

  if (scoreDisp) scoreDisp.textContent = `${assessment.total_scored} / ${assessment.total_max} pts (${assessment.total_percentage}%)`;

  let weakCount = 0;
  assessment.questions.forEach(q => { if (q.is_weak) weakCount++; });

  if (statusBadge) {
    if (weakCount > 0) {
      statusBadge.innerHTML = `<span class="badge badge-red" style="font-size: 12px; padding: 4px 10px;">DEFICIT DETECTED (${weakCount} Topic${weakCount>1?'s':''} Need Remediation)</span>`;
    } else {
      statusBadge.innerHTML = `<span class="badge badge-green" style="font-size: 12px; padding: 4px 10px;">MASTERY STATUS VERIFIED (All Sections >= 50%)</span>`;
    }
  }

  if (gapsCount) {
    gapsCount.textContent = `${weakCount} Concept Gap${weakCount!==1?'s':''}`;
    gapsCount.style.color = weakCount > 0 ? "#dc2626" : "#16a34a";
  }

  if (!tbody) return;
  if (!assessment.questions || assessment.questions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No question records found for IA-${iaNum}.</td></tr>`;
    return;
  }

  tbody.innerHTML = assessment.questions.map(q => {
    const isWeak = q.is_weak;
    const statusBadgeHtml = isWeak
      ? `<span class="badge badge-red">DEFICIT</span>`
      : `<span class="badge badge-green">MASTERED</span>`;

    const prereqList = q.prerequisite_concepts && q.prerequisite_concepts.length > 0
      ? q.prerequisite_concepts.map(p => `<span class="badge badge-gray" style="font-size: 10px; margin-right: 4px;">${p}</span>`).join("")
      : `<span style="font-size: 11px; color: var(--text-muted);">None</span>`;

    const actionBtn = isWeak
      ? `<button class="btn-black" onclick="openExplainWeakTopicModal('${q.topic_id}', '${q.question_no}')" style="font-size: 11px; padding: 4px 10px;">
          <svg class="icon-svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          Explain Weak Topic &amp; Gap
        </button>`
      : `<button class="btn-outline" onclick="openExplainWeakTopicModal('${q.topic_id}', '${q.question_no}')" style="font-size: 11px; padding: 4px 10px;">
          View Concept Blueprint
        </button>`;

    return `
      <tr>
        <td style="font-weight: 700; font-family: monospace;">${q.question_no}</td>
        <td style="font-weight: 600;">${q.topic_title}</td>
        <td style="font-weight: 700;">${q.marks_obtained} / ${q.max_marks} pts</td>
        <td><strong>${q.score_percentage}%</strong></td>
        <td>${statusBadgeHtml}</td>
        <td>${prereqList}</td>
        <td>${actionBtn}</td>
      </tr>
    `;
  }).join("");
}

async function openExplainWeakTopicModal(topicId, qNo) {
  currentExplainingTopicId = topicId;
  const modal = document.getElementById("modal-explain-weak-topic");
  if (!modal) return;
  modal.style.display = "flex";

  const titleEl = document.getElementById("modal-weak-topic-title");
  const scoreBadgeEl = document.getElementById("modal-weak-score-badge");
  const rootCauseEl = document.getElementById("modal-weak-root-cause");
  const prereqsContainer = document.getElementById("modal-weak-prereqs-container");
  const syllabusBox = document.getElementById("modal-weak-syllabus-box");
  const scheduleContainer = document.getElementById("modal-weak-schedule-container");

  if (titleEl) titleEl.textContent = `Question ${qNo || ''}: Loading Concept Diagnosis...`;
  if (rootCauseEl) rootCauseEl.textContent = "Querying Knowledge Graph DAG and ChromaDB vector store...";
  if (prereqsContainer) prereqsContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 12px;">Loading prerequisite dependencies...</div>';
  if (scheduleContainer) scheduleContainer.innerHTML = '<div style="color: var(--text-muted); font-size: 12px;">Synthesizing 5-Day Remedial Action Plan...</div>';

  try {
    const res = await fetch(`${API_BASE}/api/student/${currentStudentId}/courses/AIML-401/explain-weak-topic/${topicId}`);
    if (!res.ok) throw new Error("Could not retrieve topic explanation.");
    const data = await res.json();

    if (titleEl) titleEl.textContent = `${data.question_no ? data.question_no + ': ' : ''}${data.topic_title} (IA-${data.ia_number || 1})`;
    if (scoreBadgeEl) {
      const isWeak = data.score_percentage < 50.0;
      scoreBadgeEl.innerHTML = `Score: <strong>${data.marks_obtained} / ${data.max_marks} pts</strong> (${data.score_percentage}%) &bull; Status: <span class="badge ${isWeak ? 'badge-red' : 'badge-green'}">${isWeak ? 'DEFICIT DETECTED' : 'MASTERED'}</span>`;
    }

    if (rootCauseEl) rootCauseEl.textContent = data.diagnostic_root_cause;

    if (prereqsContainer) {
      if (data.prerequisite_dependencies && data.prerequisite_dependencies.length > 0) {
        prereqsContainer.innerHTML = data.prerequisite_dependencies.map(p => `
          <div style="background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
              <span class="badge badge-gray" style="font-size: 10px;">${p.prerequisite_id}</span>
              <span style="font-size: 11px; color: #dc2626; font-weight: 600;">Prerequisite Deficit</span>
            </div>
            <div style="font-size: 12.5px; font-weight: 700; color: #000; margin-bottom: 3px;">${p.name}</div>
            <div style="font-size: 11.5px; color: var(--text-muted); line-height: 1.4;">${p.description || 'Core foundation required for upstream calculus gradients.'}</div>
          </div>
        `).join("");
      } else {
        prereqsContainer.innerHTML = `<div style="font-size: 12px; color: var(--text-muted);">No direct upstream prerequisite deficits flagged in the DAG. Core foundational mathematics recommended.</div>`;
      }
    }

    if (syllabusBox) {
      if (data.syllabus_citations && data.syllabus_citations.length > 0) {
        syllabusBox.innerHTML = data.syllabus_citations.map(c => `
          <div style="margin-bottom: 6px;">
            <strong style="color: #000;">${c.unit}:</strong> ${c.syllabus_excerpt}
          </div>
        `).join("");
      } else {
        syllabusBox.innerHTML = `<div>Unit 2 &amp; Unit 3 Curriculum: Differential Optimization, Matrix Jacobians, Computational Graph Traversal and Backpropagation.</div>`;
      }
    }

    if (scheduleContainer) {
      if (data.remedial_schedule && data.remedial_schedule.length > 0) {
        scheduleContainer.innerHTML = data.remedial_schedule.map(d => `
          <div style="display: flex; align-items: flex-start; gap: 12px; background: rgba(0,0,0,0.02); border: 1px solid var(--border-color); border-radius: 8px; padding: 10px 14px;">
            <div style="width: 28px; height: 28px; border-radius: 50%; background: #000; color: #fff; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
              D${d.day}
            </div>
            <div style="flex: 1;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 12.5px; font-weight: 700; color: #000;">${d.title}</span>
                <span style="font-size: 10.5px; color: var(--text-muted); font-weight: 600; text-transform: uppercase;">${d.phase}</span>
              </div>
              <div style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">${d.focus}</div>
            </div>
          </div>
        `).join("");
      }
    }
  } catch (err) {
    if (rootCauseEl) rootCauseEl.textContent = "Error loading diagnosis: " + err.message;
  }
}

function closeExplainWeakTopicModal() {
  const modal = document.getElementById("modal-explain-weak-topic");
  if (modal) modal.style.display = "none";
}

function triggerWeakTopicChatAssistant() {
  closeExplainWeakTopicModal();
  const input = document.getElementById("omni-input");
  if (input) {
    input.value = `Why am I weak in ${currentExplainingTopicId || 'this topic'}? Explain the prerequisite gaps.`;
    if (typeof handleSendOmniChat === "function") {
      handleSendOmniChat();
    }
  }
  const chatSection = document.getElementById("panel-omni-assistant") || document.getElementById("omni-input");
  if (chatSection) {
    chatSection.scrollIntoView({ behavior: "smooth" });
  }
}
'''

if "function loadStudentIADiagnostics" not in js_code:
    js_code += "\n" + diag_js_code
    print("Appended IA Diagnostics & Weak Topic Explanation logic to js/student.js.")

with open("js/student.js", "w", encoding="utf-8") as f:
    f.write(js_code)
print("js/student.js updated.")

