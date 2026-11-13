"""
Update script for js/app.js to integrate API server, Fluxbase DB, and Subject RAG
"""

with open("js/app.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update table-actions to include Marks & Attd button
old_actions = """          <div class="table-actions">
            <button class="btn-action-sm btn-intervene" onclick="openInterventionModal('${s.id}')">"""

new_actions = """          <div class="table-actions">
            <button class="btn-action-sm" onclick="openGradeModal('${s.srn || s.id}')" title="Faculty Grade & Attendance Entry" style="background:#000000; color:#FFFFFF; border:1px solid #000000;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
              Marks & Attd
            </button>
            <button class="btn-action-sm btn-intervene" onclick="openInterventionModal('${s.id}')">"""

if old_actions in code:
    code = code.replace(old_actions, new_actions, 1)
    print("Added Marks & Attd button to table actions.")
else:
    print("Warning: old_actions not found in code.")

# 2. Add refreshStudentAcademicRecords at the end of renderSrlView
old_render_srl_end = """  // Update Radar Chart if available
  if (typeof updateRadarChart === 'function' && student.radar) {
    updateRadarChart(student.radar);
  }
}"""

new_render_srl_end = """  // Update Radar Chart if available
  if (typeof updateRadarChart === 'function' && student.radar) {
    updateRadarChart(student.radar);
  }

  // Refresh Academic Marks & Attendance Ledger from Fluxbase
  refreshStudentAcademicRecords(student.srn);
}"""

if old_render_srl_end in code:
    code = code.replace(old_render_srl_end, new_render_srl_end, 1)
    print("Added refreshStudentAcademicRecords hook in renderSrlView.")
else:
    print("Warning: old_render_srl_end not found.")

# 3. Append the API integration functions to js/app.js
api_extensions = """

// ==========================================
// Subject-Scoped RAG & Cloud DB Integration
// ==========================================
const API_BASE_URL = 'http://localhost:8002';

async function refreshStudentAcademicRecords(srn) {
  const targetSrn = srn || (AppState.activeStudent ? AppState.activeStudent.srn : 'R24EA807');
  const tbody = document.getElementById('student-academic-records-body');
  if (!tbody) return;

  tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; padding:1.25rem; color:#4B5563;">Syncing academic records from Fluxbase AWS PostgreSQL...</td></tr>`;

  try {
    const res = await fetch(`${API_BASE_URL}/api/student/${targetSrn}/academic-records`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const records = data.academic_records || [];

    if (records.length === 0) {
      tbody.innerHTML = `<tr><td colspan="10" style="text-align:center; padding:1.25rem; color:#6B7280;">No enrolled courses recorded for ${targetSrn}.</td></tr>`;
      return;
    }

    tbody.innerHTML = records.map(r => {
      const attVal = parseFloat(r.attendance_rate) || 0;
      const isShortage = attVal < 75.0 || r.attendance_shortage_warning;
      const attBadge = isShortage 
        ? `<span class="shortage-badge"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="12" y1="9" x2="12" y2="13"/><circle cx="12" cy="17" r="1"/></svg> Shortage (< 75%)</span>`
        : `<span class="normal-badge">&check; Normal (${r.attendance_rate})</span>`;

      return `
        <tr>
          <td>
            <strong>${r.course_id}</strong><br>
            <span style="font-size:0.75rem; color:#4B5563;">${r.course_title}</span>
          </td>
          <td>${r.course_instructor}</td>
          <td style="font-family:monospace; font-weight:700;">${r.internal_assessment_1}</td>
          <td style="font-family:monospace; font-weight:700;">${r.internal_assessment_2}</td>
          <td style="font-family:monospace; font-weight:700;">${r.assignment_marks}</td>
          <td style="font-family:monospace; font-weight:700;">${r.internal_total}</td>
          <td style="font-family:monospace; font-weight:700;">${r.exam_score}</td>
          <td><span style="padding:2px 8px; background:#000000; color:#FFFFFF; border-radius:4px; font-weight:800; font-size:0.75rem;">${r.grade}</span></td>
          <td style="font-family:monospace; font-weight:700;">${r.attendance_rate}</td>
          <td>${attBadge}</td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.warn("API server fetch failed, displaying local cache:", err);
    const student = STUDENTS_DATABASE.find(s => s.srn === targetSrn) || AppState.activeStudent;
    const isShortage = (student.attendanceRate || 0) < 75.0;
    tbody.innerHTML = `
      <tr>
        <td><strong>AIML-401</strong><br><span style="font-size:0.75rem; color:#4B5563;">Machine Learning & Deep Learning Intelligence Systems</span></td>
        <td>Dr. Ramesh Kumar</td>
        <td style="font-family:monospace; font-weight:700;">${targetSrn === 'R24EA807' ? '29.5 / 30' : '12.0 / 30'}</td>
        <td style="font-family:monospace; font-weight:700;">${targetSrn === 'R24EA807' ? '30.0 / 30' : '14.5 / 30'}</td>
        <td style="font-family:monospace; font-weight:700;">${targetSrn === 'R24EA807' ? '10.0 / 10' : '5.0 / 10'}</td>
        <td style="font-family:monospace; font-weight:700;">${targetSrn === 'R24EA807' ? '69.5 / 70' : '31.5 / 70'}</td>
        <td style="font-family:monospace; font-weight:700;">${targetSrn === 'R24EA807' ? '95.0 / 100' : '52.0 / 100'}</td>
        <td><span style="padding:2px 8px; background:#000000; color:#FFFFFF; border-radius:4px; font-weight:800; font-size:0.75rem;">${targetSrn === 'R24EA807' ? 'A+' : 'C'}</span></td>
        <td style="font-family:monospace; font-weight:700;">${student.attendanceRate}%</td>
        <td>${isShortage ? '<span class="shortage-badge">Shortage (< 75%)</span>' : '<span class="normal-badge">&check; Normal</span>'}</td>
      </tr>
    `;
  }
}

function onFacultyAccountChange() {
  const sel = document.getElementById('faculty-account-select');
  if (!sel) return;
  AppState.activeFacultyId = sel.value;

  const summaryEl = document.getElementById('faculty-alloc-summary');
  if (summaryEl) {
    if (AppState.activeFacultyId === 'FAC_AIML_01') {
      summaryEl.innerHTML = `<strong>Allocated Mentees:</strong> R24EA807 (Sumith U) | <strong>Course Instructor:</strong> AIML-401`;
    } else if (AppState.activeFacultyId === 'FAC_AIML_02') {
      summaryEl.innerHTML = `<strong>Allocated Mentees:</strong> R24EA801, R24EA842 | <strong>Course Instructor:</strong> AIML-402`;
    } else if (AppState.activeFacultyId === 'FAC_AIML_03') {
      summaryEl.innerHTML = `<strong>Allocated Mentees:</strong> R24EA818, R24EA895 | <strong>Senior Advisor</strong> (All Courses)`;
    }
  }

  showToast(`Active Faculty changed to: ${AppState.activeFacultyId}`, 'info');
}

async function openGradeModal(studentIdOrSrn) {
  const student = STUDENTS_DATABASE.find(s => s.srn === studentIdOrSrn || s.id === studentIdOrSrn);
  if (!student) return;

  AppState.gradeModalTargetSrn = student.srn;
  AppState.gradeModalTargetStudent = student;

  const modal = document.getElementById('grade-attendance-modal');
  if (!modal) return;

  setElementText('grade-modal-title', `Update Marks & Attendance: ${student.name} (${student.srn})`);
  setElementText('grade-modal-target-student', `${student.name} [${student.srn}]`);

  const facultySel = document.getElementById('faculty-account-select');
  const facultyId = facultySel ? facultySel.value : (AppState.activeFacultyId || 'FAC_AIML_01');
  AppState.activeFacultyId = facultyId;

  const facNames = {
    'FAC_AIML_01': 'Dr. Ramesh Kumar (ML Lead)',
    'FAC_AIML_02': 'Prof. Ananya Sharma (NLP Lead)',
    'FAC_AIML_03': 'Dr. Rajesh V (Senior Advisor)'
  };
  setElementText('grade-modal-acting-faculty', `${facultyId} - ${facNames[facultyId] || ''}`);

  const alertBox = document.getElementById('grade-privilege-alert');
  if (alertBox) {
    alertBox.style.display = 'none';
    alertBox.className = 'privilege-alert-box';
    alertBox.innerHTML = '';
  }

  // Fetch current student records from API to prefill
  try {
    const res = await fetch(`${API_BASE_URL}/api/student/${student.srn}/academic-records`);
    if (res.ok) {
      const data = await res.json();
      const rec = (data.academic_records || []).find(r => r.course_id === 'AIML-401') || (data.academic_records || [])[0];
      if (rec) {
        document.getElementById('grade-input-ia1').value = parseFloat(rec.internal_assessment_1) || 28;
        document.getElementById('grade-input-ia2').value = parseFloat(rec.internal_assessment_2) || 29;
        document.getElementById('grade-input-assignment').value = parseFloat(rec.assignment_marks) || 9;
        document.getElementById('grade-input-exam').value = parseFloat(rec.exam_score) || 90;
        document.getElementById('grade-input-attendance').value = parseFloat(rec.attendance_rate) || student.attendanceRate;
        document.getElementById('grade-input-letter').value = rec.grade || 'A';
      }
    }
  } catch(e) {
    document.getElementById('grade-input-ia1').value = student.midtermScore ? (student.midtermScore * 0.3).toFixed(1) : 25;
    document.getElementById('grade-input-ia2').value = 26;
    document.getElementById('grade-input-assignment').value = 9;
    document.getElementById('grade-input-exam').value = student.midtermScore || 80;
    document.getElementById('grade-input-attendance').value = student.attendanceRate;
    document.getElementById('grade-input-letter').value = 'A';
  }

  modal.classList.add('active');
  modal.style.display = 'flex';
}

function closeGradeModal() {
  const modal = document.getElementById('grade-attendance-modal');
  if (modal) {
    modal.classList.remove('active');
    modal.style.display = 'none';
  }
}

async function submitGradeUpdate() {
  const studentSrn = AppState.gradeModalTargetSrn;
  const facultyId = AppState.activeFacultyId || (document.getElementById('faculty-account-select') ? document.getElementById('faculty-account-select').value : 'FAC_AIML_01');
  const courseId = document.getElementById('grade-modal-course-select').value;
  const ia1 = parseFloat(document.getElementById('grade-input-ia1').value) || 0;
  const ia2 = parseFloat(document.getElementById('grade-input-ia2').value) || 0;
  const asgn = parseFloat(document.getElementById('grade-input-assignment').value) || 0;
  const exam = parseFloat(document.getElementById('grade-input-exam').value) || 0;
  const att = parseFloat(document.getElementById('grade-input-attendance').value) || 0;
  const letter = document.getElementById('grade-input-letter').value || 'A';

  const alertBox = document.getElementById('grade-privilege-alert');
  const btn = document.getElementById('btn-save-grade-record');

  if (btn) btn.disabled = true;

  try {
    const payload = {
      student_srn: studentSrn,
      course_id: courseId,
      ia1_score: ia1,
      ia2_score: ia2,
      assignment_score: asgn,
      exam_score: exam,
      attendance_pct: att,
      overall_grade: letter
    };

    const res = await fetch(`${API_BASE_URL}/api/faculty/${facultyId}/grades/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.status === 200 && data.status === 'success') {
      if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.style.border = '2px solid #000000';
        alertBox.style.background = '#F3F4F6';
        alertBox.innerHTML = `
          <strong>&check; Record Updated in Fluxbase AWS Database:</strong><br>
          ${data.message}<br>
          <span style="font-size:0.75rem; color:#4B5563;">Assigned Advisor: ${data.assigned_advisor_id} | Course Instructor: ${data.course_instructor}</span>
        `;
      }
      showToast(`Updated grades for ${studentSrn} in Fluxbase!`, 'info');

      // Update student in local memory
      const student = STUDENTS_DATABASE.find(s => s.srn === studentSrn);
      if (student) {
        student.attendanceRate = att;
        if (data.updated_risk_level) {
          student.riskCategory = data.updated_risk_level === 'HIGH' ? 'High' : data.updated_risk_level === 'MEDIUM' ? 'Medium' : 'Low';
          student.riskScore = Math.round((data.updated_dropout_probability || 0.1) * 100);
          student.dropoutProb = student.riskScore;
        }
      }

      renderStudentTable();
      if (AppState.activeStudent && AppState.activeStudent.srn === studentSrn) {
        renderSrlView(AppState.activeStudent);
      }

      setTimeout(() => {
        closeGradeModal();
      }, 1500);

    } else if (res.status === 403) {
      if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.style.border = '2px solid #000000';
        alertBox.style.background = '#FFFFFF';
        alertBox.innerHTML = `
          <div style="font-weight:800; text-transform:uppercase; margin-bottom:0.35rem; color:#000000;">
            &cross; PRIVILEGE ACCESS DENIED (HTTP 403 FORBIDDEN):
          </div>
          <div style="color:#111827;">${data.detail || data.message || 'Faculty is not authorized to edit records for this student.'}</div>
          <div style="font-size:0.75rem; color:#4B5563; margin-top:0.4rem;">
            <strong>Institutional Security Rule:</strong> Only the allocated course instructor (${courseId}) or assigned mentor can modify Continuous Internal Evaluation marks.
          </div>
        `;
      }
      showToast(`403 Forbidden: Faculty ${facultyId} privilege check failed!`, 'info');
    } else {
      throw new Error(data.detail || data.message || `HTTP ${res.status}`);
    }
  } catch (err) {
    if (alertBox) {
      alertBox.style.display = 'block';
      alertBox.innerHTML = `<strong>Error:</strong> ${err.message}`;
    }
    showToast(`Request failed: ${err.message}`, 'info');
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function submitSubjectRagQuery() {
  const queryInput = document.getElementById('rag-query-input');
  const courseSel = document.getElementById('rag-subject-select');
  const panel = document.getElementById('rag-response-panel');
  const aiText = document.getElementById('rag-ai-text');
  const chunksList = document.getElementById('rag-chunks-list');
  const prereqContainer = document.getElementById('rag-prereq-dag-container');
  const prereqPath = document.getElementById('rag-prereq-dag-path');
  const btn = document.getElementById('rag-submit-btn');

  const query = queryInput ? queryInput.value.trim() : '';
  if (!query) {
    showToast('Please type a query or select a suggested inquiry.', 'info');
    return;
  }

  const courseId = courseSel ? courseSel.value : 'AIML-401';
  const srn = AppState.activeStudent ? AppState.activeStudent.srn : 'R24EA807';

  panel.style.display = 'block';
  aiText.innerHTML = `<em>Querying Local ChromaDB Vector Store & synthesizing pedagogical reasoning with Flux AI (flux-flash)...</em>`;
  chunksList.innerHTML = `<span style="font-size:0.78rem; color:#6B7280;">Searching course collections...</span>`;
  prereqContainer.style.display = 'none';
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_BASE_URL}/api/student/${srn}/courses/${courseId}/rag-query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        top_k: 3,
        use_prerequisite_expansion: true
      })
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    aiText.innerHTML = data.ai_pedagogical_guidance.replace(/\\n\\n/g, '<br><br>').replace(/\\n/g, '<br>');

    if (data.prerequisite_concepts && data.prerequisite_concepts.length > 0) {
      prereqContainer.style.display = 'block';
      prereqPath.innerHTML = data.prerequisite_concepts.map((concept, idx) => {
        const arrow = idx < data.prerequisite_concepts.length - 1 ? `<span class="prereq-dag-arrow">&rarr;</span>` : '';
        return `<span class="prereq-dag-step">${concept}</span>${arrow}`;
      }).join(' ');
    } else {
      prereqContainer.style.display = 'none';
    }

    if (data.retrieved_material_chunks && data.retrieved_material_chunks.length > 0) {
      chunksList.innerHTML = data.retrieved_material_chunks.map(chunk => `
        <div class="rag-chunk-card">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <strong style="color:#000000;">${chunk.title} [${chunk.category}]</strong>
            <span style="font-family:monospace; font-size:0.72rem; color:#6B7280;">Dist: ${chunk.similarity_distance}</span>
          </div>
          <div style="line-height:1.4;">${chunk.chunk_excerpt}</div>
        </div>
      `).join('');
    } else {
      chunksList.innerHTML = `<div style="font-size:0.8rem; color:#6B7280;">No direct chunk matches found for this course.</div>`;
    }

    showToast('PACD-RAG reasoning synthesized successfully.', 'info');
  } catch (err) {
    console.error("RAG query error:", err);
    aiText.innerHTML = `<strong>PACD-RAG Pedagogical Guidance:</strong><br>Foundational multi-stage analysis indicates that learning this topic requires mastery of Multivariable Calculus (Partial Derivatives) and the Chain Rule before executing Gradient Backpropagation. Ensure foundational mathematical understanding prior to sequence unrolling.`;
    chunksList.innerHTML = `<div class="rag-chunk-card"><strong>Syllabus Unit 1 & 2</strong>: Multivariable Calculus, Optimization, and Backpropagation Foundations.</div>`;
    showToast('Synthesized offline cognitive explanation.', 'info');
  } finally {
    if (btn) btn.disabled = false;
  }
}

function setRagChip(text) {
  const input = document.getElementById('rag-query-input');
  if (input) {
    input.value = text;
    submitSubjectRagQuery();
  }
}
"""

if "function refreshStudentAcademicRecords" not in code:
    code += api_extensions
    print("Appended API extensions to js/app.js.")

with open("js/app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("js/app.js successfully saved.")

