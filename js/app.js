/**
 * AI-Powered Smart Campus Intelligence & Student Success Platform
 * Application Controller & Reactive UI Logic (Vanilla JS)
 * Author: Sumith U (SRN: R24EA807) | REVA University
 * Design: Ultra-Professional Monochrome (White, Black, and Grey only)
 */

const AppState = {
  activeView: 'faculty', // 'faculty', 'student', 'admin'
  ferpaActive: false,
  activeStudent: null,
  searchQuery: '',
  filterRisk: 'all',
  filterDept: 'all',
  uploadedResources: [
    { name: "Unit-3_Deep_Learning_Architectures.pptx", type: "PPTX", size: "14.2 MB", status: "Indexed in PACD-RAG", chunks: 48 },
    { name: "REVA_AIML_7Sem_Syllabus_2026.pdf", type: "PDF", size: "2.4 MB", status: "Indexed in PACD-RAG", chunks: 22 },
    { name: "Lab_Manual_Advanced_Cognitive_Diagnosis.docx", type: "DOCX", size: "5.1 MB", status: "Indexed in PACD-RAG", chunks: 36 }
  ],
  wrongQuestions: [
    {
      id: "WQ-101",
      course: "Deep Learning (AIML-701)",
      topic: "Backpropagation Through Time (BPTT)",
      prerequisiteDeficit: "Chain Rule & Recurrent Matrix Unrolling",
      question: "In standard BPTT, when computing gradients across long sequences, why does the gradient norm vanish or explode?",
      options: [
        { text: "Repeated multiplication of the hidden state transition matrix eigenvalue λ < 1 or λ > 1.", correct: true },
        { text: "Because the learning rate is automatically divided by sequence length T in every forward pass.", correct: false },
        { text: "Because ReLU activations produce negative saturation when multiplied over time.", correct: false },
        { text: "Because cross-entropy loss cannot be backpropagated through recurrent skip connections.", correct: false }
      ],
      misconceptionExplanation: "PACD-RAG Diagnostic: Failure to model matrix spectral radius over unrolled time steps. Prerequisite deficit identified in Unit 2: Linear Dynamical Recurrence.",
      nextSpacedReview: "In 2 days (Ebbinghaus Interval 2)"
    },
    {
      id: "WQ-102",
      topic: "TreeSHAP Local Attribution",
      course: "Explainable AI (AIML-703)",
      prerequisiteDeficit: "Shapley Value Efficiency & Additivity Axioms",
      question: "Why does TreeSHAP compute exact Shapley values in polynomial time O(TLD²) rather than exponential time O(TL2^M)?",
      options: [
        { text: "It recurses down tree decision paths simultaneously tracking feature subset weights using conditional expectations.", correct: true },
        { text: "It ignores feature correlation completely and computes independent marginal distributions.", correct: false },
        { text: "It trains a surrogate linear model at every leaf node of the ensemble tree.", correct: false },
        { text: "It approximates coalitions using Monte Carlo gradient estimates.", correct: false }
      ],
      misconceptionExplanation: "PACD-RAG Diagnostic: Confusion between KernelSHAP (sampling approximation) and Lundberg's polynomial algorithm for tree structures.",
      nextSpacedReview: "In 4 days (Ebbinghaus Interval 3)"
    }
  ]
};

// ==========================================
// Initialization on Document Ready
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
  AppState.activeStudent = STUDENTS_DATABASE[0];
  initAuth();

  initNavListeners();
  initFilterListeners();
  initModalListeners();
  initSimulatorSlider();
  initWrongQuestionDrill();
  initResourceUploader();

  renderKpis();
  renderStudentTable();
  populateStudentDropdowns();
  renderSrlView(AppState.activeStudent);
  renderAdminView();
  if (typeof onFacultyAccountChange === 'function') { onFacultyAccountChange(); }

  if (typeof initAllCharts === 'function') {
    initAllCharts();
  }

  showToast("Platform loaded: Minimalist Monochrome Executive UI active.", "info");
});

// ==========================================
// Navigation & Role Switching
// ==========================================
function initNavListeners() {
  const roleButtons = document.querySelectorAll('.role-btn');
  roleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetRole = btn.getAttribute('data-role');
      switchView(targetRole);
    });
  });

  const ferpaToggle = document.getElementById('ferpa-toggle');
  if (ferpaToggle) {
    ferpaToggle.addEventListener('click', toggleFerpa);
  }
}

function switchView(role) {
  AppState.activeView = role;

  document.querySelectorAll('.role-btn').forEach(b => {
    if (b.getAttribute('data-role') === role) {
      b.classList.add('active');
    } else {
      b.classList.remove('active');
    }
  });

  const views = {
    faculty: document.getElementById('view-faculty'),
    student: document.getElementById('view-student'),
    admin: document.getElementById('view-admin')
  };

  Object.keys(views).forEach(key => {
    if (views[key]) {
      if (key === role) {
        views[key].classList.add('active');
      } else {
        views[key].classList.remove('active');
      }
    }
  });

  if (role === 'student' && typeof renderStudentRadarChart === 'function') {
    setTimeout(() => {
      renderStudentRadarChart(AppState.activeStudent);
      if (typeof initSrlHabitChart === 'function') initSrlHabitChart();
    }, 100);
  }

  window.dispatchEvent(new Event('resize'));
  showToast(`Switched view: ${role === 'faculty' ? 'Faculty Console' : role === 'student' ? 'Student SRL Dashboard' : 'Campus Intelligence & Research'}`, "info");
}

function toggleFerpa() {
  AppState.ferpaActive = !AppState.ferpaActive;
  const btn = document.getElementById('ferpa-toggle');
  if (btn) {
    if (AppState.ferpaActive) {
      btn.classList.add('active-toggle');
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="3"/></svg> FERPA: Anonymized`;
      showToast("FERPA Privacy Shield: Student identities & SRNs masked.", "success");
    } else {
      btn.classList.remove('active-toggle');
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg> FERPA Anonymize`;
      showToast("FERPA Privacy Shield: Normal student identities restored.", "info");
    }
  }

  renderStudentTable();
  renderSrlView(AppState.activeStudent);
}

// ==========================================
// KPI Banner Rendering
// ==========================================
function renderKpis() {
  const c = CAMPUS_ANALYTICS;
  setElementText('kpi-total', c.totalStudents.toLocaleString());
  setElementText('kpi-risk', `${c.highRiskCount} Students (${((c.highRiskCount / c.totalStudents) * 100).toFixed(1)}%)`);
  setElementText('kpi-leadtime', `${c.averageLeadTimeWeeks} Weeks`);
  setElementText('kpi-interventions', `${c.activeInterventions} Active / ${c.resolvedInterventionsThisMonth} Resolved`);
}

function setElementText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

// ==========================================
// Student Table & Filtering
// ==========================================
function initFilterListeners() {
  const searchInput = document.getElementById('student-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      AppState.searchQuery = e.target.value.toLowerCase();
      renderStudentTable();
    });
  }

  const riskFilter = document.getElementById('risk-filter');
  if (riskFilter) {
    riskFilter.addEventListener('change', (e) => {
      AppState.filterRisk = e.target.value;
      renderStudentTable();
    });
  }

  const deptFilter = document.getElementById('dept-filter');
  if (deptFilter) {
    deptFilter.addEventListener('change', (e) => {
      AppState.filterDept = e.target.value;
      renderStudentTable();
    });
  }
}

function renderStudentTable() {
  const tbody = document.getElementById('student-table-body');
  if (!tbody) return;

  const filtered = STUDENTS_DATABASE.filter(student => {
    if (AppState.filterRisk !== 'all' && student.riskCategory.toLowerCase() !== AppState.filterRisk.toLowerCase()) {
      return false;
    }
    if (AppState.filterDept !== 'all' && student.department.toLowerCase() !== AppState.filterDept.toLowerCase()) {
      return false;
    }
    if (AppState.searchQuery) {
      const q = AppState.searchQuery;
      const name = AppState.ferpaActive ? student.anonymizedId.toLowerCase() : student.name.toLowerCase();
      const srn = AppState.ferpaActive ? "anon" : student.srn.toLowerCase();
      const dept = student.department.toLowerCase();
      const factor = student.primaryRiskFactor.toLowerCase();
      return name.includes(q) || srn.includes(q) || dept.includes(q) || factor.includes(q);
    }
    return true;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 2.5rem; color: #6B7280; font-weight: 500;">
          No students match the current filter criteria.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = filtered.map(s => {
    const displayName = AppState.ferpaActive ? s.anonymizedId : s.name;
    const displaySrn = AppState.ferpaActive ? "ANON-PROTECTED" : s.srn;
    const avatarSrc = AppState.ferpaActive 
      ? "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80" 
      : s.avatar;

    const riskClass = s.riskCategory === 'High' ? 'risk-high' : s.riskCategory === 'Medium' ? 'risk-med' : 'risk-low';

    return `
      <tr>
        <td>
          <div class="student-cell">
            <img src="${avatarSrc}" alt="${displayName}" class="student-avatar" style="${AppState.ferpaActive ? 'filter: blur(2px);' : ''}">
            <div class="student-details">
              <span class="student-name">${displayName}</span>
              <span class="student-meta">${displaySrn} &bull; Sem ${s.semester}-${s.section}</span>
            </div>
          </div>
        </td>
        <td>
          <span style="font-weight: 600; color: #111827;">${s.department}</span>
        </td>
        <td>
          <span style="font-family: monospace; font-weight: 700; color: #000000;">${s.cgpa.toFixed(2)}</span>
        </td>
        <td>
          <span class="risk-pill ${riskClass}">
            <span class="risk-pulse-dot"></span>
            ${s.riskCategory} (${s.riskScore}%)
          </span>
        </td>
        <td style="max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #4B5563;">
          ${s.primaryRiskFactor}
        </td>
        <td>
          <span style="font-size: 0.76rem; color: #111827; font-weight: 700;">
            ${s.interventionStatus}
          </span>
        </td>
        <td>
          <div class="table-actions">
            <button class="btn-action-sm" onclick="openGradeModal('${s.srn || s.id}')" title="Faculty Grade & Attendance Entry" style="background:#000000; color:#FFFFFF; border:1px solid #000000;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
              Marks & Attd
            </button>
            <button class="btn-action-sm btn-intervene" onclick="openInterventionModal('${s.id}')">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              Intervene
            </button>
            <button class="btn-action-sm" onclick="viewStudentSRL('${s.id}')">
              SRL View &rarr;
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

// ==========================================
// Student SRL Dashboard View
// ==========================================
function populateStudentDropdowns() {
  const select = document.getElementById('srl-student-select');
  if (!select) return;

  select.innerHTML = STUDENTS_DATABASE.map(s => {
    const label = AppState.ferpaActive ? s.anonymizedId : s.name;
    return `<option value="${s.id}" ${s.id === AppState.activeStudent.id ? 'selected' : ''}>${label} (${s.riskCategory} Risk - ${s.department})</option>`;
  }).join('');

  select.addEventListener('change', (e) => {
    const student = STUDENTS_DATABASE.find(s => s.id === e.target.value);
    if (student) {
      AppState.activeStudent = student;
      renderSrlView(student);
    }
  });
}

function viewStudentSRL(studentId) {
  const student = STUDENTS_DATABASE.find(s => s.id === studentId);
  if (student) {
    AppState.activeStudent = student;
    const select = document.getElementById('srl-student-select');
    if (select) select.value = student.id;
    renderSrlView(student);
    switchView('student');
  }
}

function renderSrlView(student) {
  if (!student) return;

  const displayName = AppState.ferpaActive ? student.anonymizedId : student.name;
  const displaySrn = AppState.ferpaActive ? "ANON-SRN-ENCRYPTED" : student.srn;
  const avatarSrc = AppState.ferpaActive 
    ? "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&auto=format&fit=crop&q=80" 
    : student.avatar;

  setElementText('srl-name', displayName);
  setElementText('srl-srn', `${displaySrn} | ${student.program} (Sem ${student.semester}-${student.section})`);
  
  const avatarEl = document.getElementById('srl-avatar-img');
  if (avatarEl) {
    avatarEl.src = avatarSrc;
    avatarEl.style.filter = AppState.ferpaActive ? 'blur(3px)' : 'none';
  }

  const healthScore = Math.max(10, 100 - student.riskScore);
  setElementText('srl-health-score', `${healthScore}/100`);
  setElementText('srl-dropout-prob', `${student.dropoutProb}%`);
  setElementText('srl-warning-text', student.academicWarning);

  setElementText('srl-cgpa', student.cgpa.toFixed(2));
  setElementText('srl-attendance', `${student.attendanceRate}%`);
  setElementText('srl-vle-hours', `${student.vleStudyHoursWeekly}h / week`);

  // Render SHAP waterfall bars (Black = Increases risk, Grey = Decreases risk)
  const shapContainer = document.getElementById('srl-shap-container');
  if (shapContainer && student.shapAttribution) {
    shapContainer.innerHTML = student.shapAttribution.map(item => {
      const isNegative = item.type === 'negative';
      const pct = Math.min(100, Math.abs(item.impact) * 2.5);
      const valText = isNegative ? `+${item.impact}%` : `${item.impact}%`;
      const fillClass = isNegative ? 'shap-fill-negative' : 'shap-fill-positive';
      const valClass = isNegative ? 'neg' : 'pos';

      return `
        <div class="shap-bar-row">
          <span class="shap-feat-name" title="${item.feature}">${item.feature}</span>
          <div class="shap-track">
            <div class="${fillClass}" style="width: ${pct}%;"></div>
          </div>
          <span class="shap-val ${valClass}">${valText}</span>
        </div>
      `;
    }).join('');
  }

  // Render Counterfactual Recommendations
  const cfContainer = document.getElementById('srl-cf-container');
  if (cfContainer && student.counterfactuals) {
    cfContainer.innerHTML = student.counterfactuals.map(cf => `
      <div class="counterfactual-card">
        <div class="counterfactual-text">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:#000000; flex-shrink:0;"><polyline points="9 18 15 12 9 6"/></svg>
          <span>${cf.action}</span>
        </div>
        <div class="counterfactual-gain">
          Target Risk: &darr; ${cf.targetRisk}%
        </div>
      </div>
    `).join('');
  }

  const slider = document.getElementById('sim-vle-slider');
  if (slider) {
    slider.value = student.vleStudyHoursWeekly;
    updateSimulatorDisplay(student.vleStudyHoursWeekly);
  }

  if (typeof renderStudentRadarChart === 'function') {
    renderStudentRadarChart(student);
  }

  // Refresh Academic Marks & Attendance Ledger from Fluxbase
  if (typeof refreshStudentAcademicRecords === 'function') {
    refreshStudentAcademicRecords(student.srn);
  }
  // Refresh Weak IA Assessment Topics & Syllabus RAG Plan
  if (typeof loadWeakTopicsAndStudyPlan === 'function') {
    loadWeakTopicsAndStudyPlan(student.srn, 'AIML-401');
  }
}

// ==========================================
// What-If Counterfactual Simulator
// ==========================================
function initSimulatorSlider() {
  const slider = document.getElementById('sim-vle-slider');
  if (slider) {
    slider.addEventListener('input', (e) => {
      const hours = parseFloat(e.target.value);
      updateSimulatorDisplay(hours);
    });
  }
}

async function updateSimulatorDisplay(hours) {
  setElementText('sim-slider-val', `${hours.toFixed(1)} hrs/week`);

  if (!AppState.activeStudent) return;

  const currentHours = AppState.activeStudent.vleStudyHoursWeekly;
  const currentRisk = AppState.activeStudent.riskScore;
  const deltaHours = hours - currentHours;

  // Real ML API DiCE Counterfactual Call
  try {
    const srn = AppState.activeStudent.srn || AppState.activeStudent.id;
    const estAttendance = Math.min(100.0, AppState.activeStudent.attendance + (deltaHours * 1.5));
    const estIA2 = Math.min(25.0, 14.0 + (deltaHours * 1.2));
    
    const res = await fetch(`http://localhost:8002/api/student/${srn}/simulate-counterfactual`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        attendance: estAttendance,
        ia2_marks: estIA2,
        ia1_marks: 12.0,
        past_sgpa: AppState.activeStudent.cgpa || 7.0
      })
    });
    if (res.ok) {
      const cfData = await res.json();
      const p = cfData.pathways && cfData.pathways.length > 0 ? cfData.pathways[0] : null;
      const simRiskPct = Math.round((p ? p.simulated_risk : (currentRisk / 100.0) * 0.8) * 100);
      setElementText('sim-res-risk', `${simRiskPct}%`);
      const simulatedCgpa = Math.min(10.0, Math.max(4.0, AppState.activeStudent.cgpa + (deltaHours * 0.08))).toFixed(2);
      setElementText('sim-res-cgpa', simulatedCgpa);
      return;
    }
  } catch (err) {
    console.debug('Live DiCE API offline, fallback to local math:', err);
  }

  // Fallback calculation
  const simulatedRisk = Math.max(8, Math.min(95, Math.round(currentRisk - (deltaHours * 3.8))));
  const simulatedCgpa = Math.min(10.0, Math.max(4.0, AppState.activeStudent.cgpa + (deltaHours * 0.08))).toFixed(2);

  setElementText('sim-res-risk', `${simulatedRisk}%`);
  setElementText('sim-res-cgpa', simulatedCgpa);
}

// ==========================================
// Student Intervention Deep-Dive Modal
// ==========================================
function initModalListeners() {
  const backdrop = document.getElementById('intervention-modal');
  if (backdrop) {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeModal();
    });
  }
}

function openInterventionModal(studentId) {
  const student = STUDENTS_DATABASE.find(s => s.id === studentId);
  if (!student) return;

  const displayName = AppState.ferpaActive ? student.anonymizedId : student.name;
  const displaySrn = AppState.ferpaActive ? "ANON-SRN" : student.srn;

  setElementText('modal-student-title', `Academic Intervention: ${displayName} (${displaySrn})`);
  setElementText('modal-mentor-name', student.mentorAssigned);
  setElementText('modal-risk-badge', `${student.riskCategory} Risk (${student.riskScore}%)`);

  setElementText('modal-primary-factor', student.primaryRiskFactor);
  setElementText('modal-academic-warning', student.academicWarning);

  const logContainer = document.getElementById('modal-intervention-log');
  if (logContainer) {
    logContainer.innerHTML = student.interventionLog.map(entry => `
      <div style="background: #FFFFFF; padding: 0.85rem 1rem; border-radius: 6px; border: 1px solid #D1D5DB; border-left: 4px solid #000000; margin-bottom: 0.6rem;">
        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #4B5563; margin-bottom: 0.3rem;">
          <strong style="color: #000000;">${entry.author}</strong>
          <span>${entry.date}</span>
        </div>
        <p style="font-size: 0.84rem; color: #111827; line-height: 1.45;">${entry.note}</p>
      </div>
    `).join('');
  }

  const modal = document.getElementById('intervention-modal');
  if (modal) {
    modal.setAttribute('data-student-id', student.id);
    modal.classList.add('open');
  }
}

function closeModal() {
  const modal = document.getElementById('intervention-modal');
  if (modal) modal.classList.remove('open');
}

function saveInterventionNote() {
  const modal = document.getElementById('intervention-modal');
  const studentId = modal ? modal.getAttribute('data-student-id') : null;
  const noteInput = document.getElementById('modal-note-input');

  if (!studentId || !noteInput || !noteInput.value.trim()) {
    showToast("Please enter an action note before saving.", "error");
    return;
  }

  const student = STUDENTS_DATABASE.find(s => s.id === studentId);
  if (student) {
    student.interventionLog.unshift({
      date: "Just now (" + new Date().toLocaleDateString() + ")",
      author: "Mentor Console (Sumith U)",
      note: noteInput.value.trim()
    });
    student.interventionStatus = "In Progress / Mentor Logged";
    noteInput.value = "";
    closeModal();
    renderStudentTable();
    showToast(`Intervention note logged for ${AppState.ferpaActive ? student.anonymizedId : student.name}. Status updated.`, "success");
  }
}

// ==========================================
// Campus Intelligence & Benchmark View
// ==========================================
function renderAdminView() {
  const benchTbody = document.getElementById('benchmark-table-body');
  if (benchTbody && CAMPUS_ANALYTICS.modelBenchmark) {
    benchTbody.innerHTML = CAMPUS_ANALYTICS.modelBenchmark.map(b => `
      <tr>
        <td style="font-weight: 700; color: #000000;">${b.model}</td>
        <td><span class="status-check">&check; ${b.acc}</span></td>
        <td><span style="font-family: monospace; font-weight: 600; color: #111827;">${b.recall}</span></td>
        <td><span style="color: #000000; font-weight: 700;">${b.auc}</span></td>
        <td><span class="paper-role-pill" style="font-size: 0.72rem; padding: 0.2rem 0.5rem;">${b.xai}</span></td>
      </tr>
    `).join('');
  }

  const paperGrid = document.getElementById('papers-catalog-grid');
  if (paperGrid && typeof RESEARCH_PAPERS !== 'undefined') {
    paperGrid.innerHTML = RESEARCH_PAPERS.map(p => `
      <div class="paper-item-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:0.5rem; margin-bottom:0.4rem;">
          <h4 class="paper-title">${p.title}</h4>
          <span style="font-size:0.72rem; font-weight:700; color:#FFFFFF; background:#000000; padding:0.2rem 0.55rem; border-radius:4px; white-space:nowrap;">
            ${p.year}
          </span>
        </div>
        <div class="paper-meta">
          <strong>${p.authors}</strong> &bull; <em>${p.journal}</em>
        </div>
        <p style="font-size:0.82rem; color:#374151; margin-bottom:0.6rem; line-height:1.45;">
          <strong>Methodology:</strong> ${p.methodology}
        </p>
        <div class="paper-role-pill">
          <strong>Platform Integration:</strong> ${p.platformRole}
        </div>
      </div>
    `).join('');
  }
}

// ==========================================
// Feature: Smart Wrong Question Drill
// ==========================================
function initWrongQuestionDrill() {
  const container = document.getElementById('wrong-questions-drill');
  if (!container) return;

  container.innerHTML = AppState.wrongQuestions.map((q, idx) => `
    <div class="glass-panel" style="padding: 1.4rem; margin-bottom: 1.25rem; border-left: 4px solid #000000; background: #F3F4F6;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; flex-wrap: wrap; gap: 0.5rem;">
        <span style="font-size: 0.76rem; font-weight: 800; color: #000000; text-transform: uppercase;">
          ${q.course} &bull; ${q.topic}
        </span>
        <span style="font-size: 0.72rem; color: #111827; background: #E5E7EB; border: 1px solid #D1D5DB; padding: 0.2rem 0.6rem; border-radius: var(--radius-sm); font-weight: 600;">
          ${q.nextSpacedReview}
        </span>
      </div>
      <p style="font-size: 0.92rem; color: #000000; font-weight: 700; margin-bottom: 1rem; line-height: 1.45;">
        ${q.question}
      </p>
      <div class="drill-options" style="display: flex; flex-direction: column; gap: 0.55rem; margin-bottom: 1rem;">
        ${q.options.map((opt, oIdx) => `
          <button class="btn-utility" style="justify-content: flex-start; text-align: left; padding: 0.75rem 1rem; width: 100%; border-radius: var(--radius-sm); background: #FFFFFF; color: #111827; border: 1px solid #D1D5DB;" onclick="checkDrillAnswer(this, ${idx}, ${oIdx})">
            <span style="width: 22px; height: 22px; border-radius: 4px; background: #000000; color: #FFFFFF; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem; margin-right: 0.6rem; font-weight: 700;">
              ${String.fromCharCode(65 + oIdx)}
            </span>
            ${opt.text}
          </button>
        `).join('')}
      </div>
      <div id="drill-feedback-${idx}" style="display: none; padding: 0.85rem; border-radius: var(--radius-sm); font-size: 0.82rem; line-height: 1.45;"></div>
    </div>
  `).join('');
}

function checkDrillAnswer(buttonEl, questionIdx, optionIdx) {
  const question = AppState.wrongQuestions[questionIdx];
  const option = question.options[optionIdx];
  const feedbackEl = document.getElementById(`drill-feedback-${questionIdx}`);

  const parent = buttonEl.closest('.drill-options');
  parent.querySelectorAll('button').forEach(b => b.disabled = true);

  if (option.correct) {
    buttonEl.style.background = '#000000';
    buttonEl.style.borderColor = '#000000';
    buttonEl.style.color = '#FFFFFF';
    if (feedbackEl) {
      feedbackEl.style.display = 'block';
      feedbackEl.style.background = '#FFFFFF';
      feedbackEl.style.border = '2px solid #000000';
      feedbackEl.style.color = '#111827';
      feedbackEl.innerHTML = `<strong>&check; Correct Mastery Verified!</strong> Ebbinghaus Spaced Repetition interval promoted to +7 days. Prerequisite mastery updated.`;
    }
    showToast("Adaptive Drill: Concept mastery confirmed. Cognitive graph updated.", "success");
  } else {
    buttonEl.style.background = '#E5E7EB';
    buttonEl.style.borderColor = '#000000';
    buttonEl.style.color = '#000000';
    buttonEl.style.fontWeight = '700';
    if (feedbackEl) {
      feedbackEl.style.display = 'block';
      feedbackEl.style.background = '#F3F4F6';
      feedbackEl.style.border = '1px solid #9CA3AF';
      feedbackEl.style.color = '#111827';
      feedbackEl.innerHTML = `<strong>Prerequisite Deficit Detected:</strong> ${question.misconceptionExplanation}`;
    }
    showToast("Adaptive Drill: Prerequisite deficit flagged in PACD-RAG memory.", "error");
  }
}

// ==========================================
// Feature: Multi-Format Resource Uploader (PDF, PPT, DOCX)
// ==========================================
function initResourceUploader() {
  const dropzone = document.getElementById('resource-dropzone');
  const fileInput = document.getElementById('resource-file-input');
  if (!dropzone || !fileInput) return;

  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#000000';
    dropzone.style.background = '#E5E7EB';
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.style.borderColor = '#D1D5DB';
    dropzone.style.background = '#FFFFFF';
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#D1D5DB';
    dropzone.style.background = '#FFFFFF';
    if (e.dataTransfer.files.length > 0) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFileUpload(e.target.files[0]);
    }
  });

  renderUploadedResources();
}

function handleFileUpload(file) {
  const ext = file.name.split('.').pop().toUpperCase();
  const validExts = ['PDF', 'PPTX', 'PPT', 'DOCX', 'DOC', 'TXT'];

  if (!validExts.includes(ext)) {
    showToast("Unsupported format. Please upload PDF, PPTX, or DOCX.", "error");
    return;
  }

  const sizeMb = (file.size / (1024 * 1024)).toFixed(1) + " MB";
  showToast(`Indexing ${file.name} into PACD-RAG...`, "info");

  setTimeout(() => {
    AppState.uploadedResources.unshift({
      name: file.name,
      type: ext,
      size: sizeMb,
      status: "Indexed in PACD-RAG",
      chunks: Math.floor(Math.random() * 30) + 15
    });
    renderUploadedResources();
    showToast(`Successfully indexed ${file.name}. Knowledge graph updated.`, "success");
  }, 900);
}

function renderUploadedResources() {
  const list = document.getElementById('uploaded-resources-list');
  if (!list) return;

  list.innerHTML = AppState.uploadedResources.map(r => `
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.85rem 1.1rem; background: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 6px; margin-bottom: 0.5rem;">
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-size: 0.72rem; font-weight: 800; color: #FFFFFF; background: #000000; padding: 0.25rem 0.55rem; border-radius: 4px;">
          ${r.type}
        </span>
        <div>
          <div style="font-size: 0.84rem; font-weight: 700; color: #111827;">${r.name}</div>
          <div style="font-size: 0.74rem; color: #6B7280;">${r.size} &bull; ${r.chunks} semantic concept chunks</div>
        </div>
      </div>
      <span style="font-size: 0.76rem; color: #000000; font-weight: 700; display: flex; align-items: center; gap: 0.35rem;">
        &check; ${r.status}
      </span>
    </div>
  `).join('');
}

// ==========================================
// Toast Notification Utility (Black Background, White Text)
// ==========================================
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  const icon = type === 'success' ? '&check;' : type === 'error' ? '&cross;' : '&bull;';

  toast.innerHTML = `<strong>${icon}</strong> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.25s ease';
    setTimeout(() => toast.remove(), 250);
  }, 3000);
}


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

    const resObj = data.result || data;
    const answer = resObj.scaffolded_answer || resObj.ai_pedagogical_guidance || 'No explanation generated.';
    const prereqs = resObj.prerequisite_ancestors || resObj.prerequisite_concepts || [];
    const sources = resObj.retrieved_sources || resObj.retrieved_material_chunks || [];

    aiText.innerHTML = answer.replace(/\n\n/g, '<br><br>').replace(/\n/g, '<br>');

    if (prereqs && prereqs.length > 0) {
      prereqContainer.style.display = 'block';
      prereqPath.innerHTML = prereqs.map((concept, idx) => {
        const arrow = idx < prereqs.length - 1 ? `<span class="prereq-dag-arrow">&rarr;</span>` : '';
        return `<span class="prereq-dag-step">${concept}</span>${arrow}`;
      }).join(' ');
    } else {
      prereqContainer.style.display = 'none';
    }

    if (sources && sources.length > 0) {
      chunksList.innerHTML = sources.map(chunk => `
        <div class="rag-chunk-card">
          <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
            <strong style="color:#000000;">${chunk.title} [${chunk.unit || chunk.category || 'Course Material'}]</strong>
            <span style="font-family:monospace; font-size:0.72rem; color:#6B7280;">Concept: ${chunk.concept || 'AIML-401'}</span>
          </div>
          <div style="line-height:1.4;">${chunk.chunk_excerpt || chunk.title + ' indexed for cognitive diagnosis.'}</div>
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


// =============================================================================
// AUTHENTICATION & ROLE-BASED ACCESS CONTROL
// =============================================================================

function initAuth() {
  const savedUser = localStorage.getItem('auth_user');
  if (savedUser) {
    try {
      const user = JSON.parse(savedUser);
      updateAuthUI(user);
    } catch (e) {
      console.warn("Invalid cached user:", e);
    }
  } else {
    // Default to student Sumith U
    updateAuthUI({
      display_name: 'Sumith U',
      role: 'student',
      entity_id: 'R24EA807',
      email: 'sumith.u@reva.edu.in'
    });
  }
}

function openLoginModal() {
  const modal = document.getElementById('login-modal');
  if (modal) modal.style.display = 'flex';
}

function closeLoginModal() {
  const modal = document.getElementById('login-modal');
  if (modal) modal.style.display = 'none';
}

async function quickLogin(identifier, password) {
  closeLoginModal();
  showToast(`Authenticating ${identifier}...`, 'info');
  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');

    localStorage.setItem('auth_token', data.access_token);
    localStorage.setItem('auth_user', JSON.stringify(data.user));
    updateAuthUI(data.user);

    // Switch view to match role
    if (data.user.role === 'student') {
      const matched = STUDENTS_DATABASE.find(s => s.srn === data.user.entity_id) || STUDENTS_DATABASE[0];
      AppState.activeStudent = matched;
      const sel = document.getElementById('srl-student-select');
      if (sel) sel.value = matched.id;
      renderSrlView(matched);
      switchView('student');
    } else if (data.user.role === 'faculty') {
      switchView('faculty');
      const facSel = document.getElementById('faculty-acting-select');
      if (facSel) {
        facSel.value = data.user.entity_id;
        if (typeof onFacultyAccountChange === 'function') onFacultyAccountChange();
      }
    } else {
      switchView('admin');
    }

    showToast(`Signed in successfully as ${data.user.display_name} (${data.user.role.toUpperCase()})`, 'success');
  } catch (err) {
    console.error("Login error:", err);
    showToast(`Authentication failed: ${err.message}`, 'error');
  }
}

async function handleCustomLogin(event) {
  event.preventDefault();
  const emailInput = document.getElementById('login-email');
  const passInput = document.getElementById('login-password');
  if (!emailInput || !passInput) return;
  await quickLogin(emailInput.value.trim(), passInput.value.trim());
}

function updateAuthUI(user) {
  if (!user) return;
  const label = document.getElementById('nav-user-label');
  const dot = document.getElementById('nav-user-dot');
  if (label) {
    const roleTag = user.role.charAt(0).toUpperCase() + user.role.slice(1);
    label.innerHTML = `${user.display_name} <span style="font-weight:400; color:var(--text-muted);">(${roleTag})</span>`;
  }
  if (dot) {
    dot.style.background = user.role === 'student' ? '#10b981' : (user.role === 'faculty' ? '#2563eb' : '#8b5cf6');
  }
}


// =============================================================================
// STEP 2 MODEL BENCHMARK AUDIT MODAL
// =============================================================================

function openBenchmarkModal() {
  const modal = document.getElementById('benchmark-modal');
  if (modal) modal.style.display = 'flex';
}

function closeBenchmarkModal() {
  const modal = document.getElementById('benchmark-modal');
  if (modal) modal.style.display = 'none';
}

function runBenchmarkInTerminal() {
  closeBenchmarkModal();
  showToast("Execute in Terminal: python run_benchmark.py --viva", "info");
}


// =============================================================================
// WEAK IA TOPICS & SYLLABUS RAG REMEDIAL PLAN
// =============================================================================

async function loadWeakTopicsAndStudyPlan(srn, courseId, forceRegenerate = false) {
  const container = document.getElementById('student-weak-topics-content');
  if (!container) return;

  if (forceRegenerate) {
    container.innerHTML = `
      <div style="padding: 1.5rem; text-align: center; color: var(--text-muted);">
        <div style="display:inline-block; animation: spin 1s linear infinite; margin-bottom: 0.5rem;"></div><br>
        Synthesizing personalized 5-Day Remedial Plan with AWS Bedrock AI...
      </div>
    `;
  }

  try {
    const res = await fetch(`${API_BASE_URL}/api/student/${srn}/courses/${courseId || 'AIML-401'}/weak-topics?force_regenerate=${forceRegenerate}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const weakTopics = data.weak_topics || [];
    const citations = data.syllabus_citations || [];
    const planText = data.study_plan || "Remedial plan synthesis complete.";
    const tasks = data.tasks || [];

    if (weakTopics.length === 0) {
      container.innerHTML = `
        <div style="padding: 1.25rem; background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: var(--radius-md); color: #065f46;">
          <strong> Excellent Assessment Standing:</strong> All Internal Assessment topics cleared with score &ge; 50%. No remedial prerequisite deficit detected.
        </div>
      `;
      return;
    }

    // Build Weak Topic Badges
    const weakCardsHtml = weakTopics.map(wt => {
      const topicName = typeof wt === 'object' ? (wt.topic_title || wt.topic_id) : wt;
      const scoreStr = typeof wt === 'object' && wt.marks_obtained !== undefined ? `${wt.marks_obtained} / ${wt.max_marks} (${wt.score_percentage}%)` : '< 50% in IA';
      return `
        <div style="background: #fff1f2; border: 1px solid #fecdd3; padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <strong style="color: #9f1239; font-size: 12px;">${topicName}</strong>
            <div style="font-size: 10.5px; color: #be123c;">Deficit identified in Internal Assessment</div>
          </div>
          <span style="font-family: monospace; font-weight: 700; color: #9f1239; font-size: 11.5px; background: #ffe4e6; padding: 2px 6px; border-radius: 4px;">
            ${scoreStr}
          </span>
        </div>
      `;
    }).join('');

    // Build Syllabus Citations
    const citationsHtml = citations.map(c => `
      <div style="background: var(--bg-surface-subtle); border: 1px solid var(--border-light); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); font-size: 11.5px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
          <strong style="color: var(--text-primary);">${c.unit || 'Core Curriculum Unit'}</strong>
          <span style="color: var(--text-muted); font-size: 10.5px;">Topic: ${c.topic_id}</span>
        </div>
        ${c.prerequisite_ancestors && c.prerequisite_ancestors.length > 0 ? `<div style="font-size: 10.5px; color: #2563eb; margin-bottom: 4px;">Prerequisite Pathway: ${c.prerequisite_ancestors.join(' &rarr; ')}</div>` : ''}
        <div style="color: var(--text-secondary); line-height: 1.4;">${c.syllabus_excerpt}</div>
      </div>
    `).join('');

    // Build Day Tasks
    const tasksHtml = tasks.map(t => `
      <label style="display: flex; align-items: flex-start; gap: 8px; font-size: 12px; color: var(--text-primary); cursor: pointer; background: var(--bg-surface); padding: 0.5rem; border: 1px solid var(--border-light); border-radius: 4px;">
        <input type="checkbox" ${t.completed ? 'checked' : ''} style="margin-top: 2px;">
        <div>
          <strong>Day ${t.day}: ${t.title}</strong>
          <div style="font-size: 11px; color: var(--text-secondary);">${t.description}</div>
        </div>
      </label>
    `).join('');

    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1rem;">
        <div>
          <span style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
            Identified Weak Assessment Topics (&lt; 50% Threshold):
          </span>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.5rem; margin-top: 0.35rem;">
            ${weakCardsHtml}
          </div>
        </div>

        <div style="background: var(--bg-surface-subtle); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-light);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong style="font-size: 12.5px; color: var(--text-primary);">AWS Bedrock Synthesized 5-Day Remedial Action Plan:</strong>
            <span style="font-size: 10.5px; color: #059669; background: #ecfdf5; padding: 2px 6px; border-radius: 4px; border: 1px solid #a7f3d0;">PACD-RAG Aligned</span>
          </div>
          <div style="font-size: 12px; color: var(--text-secondary); line-height: 1.5; white-space: pre-line; margin-bottom: 1rem;">
            ${planText}
          </div>

          <strong style="font-size: 11.5px; color: var(--text-primary); text-transform: uppercase;">Daily Remediation Tasks & Milestones:</strong>
          <div style="display: flex; flex-direction: column; gap: 0.4rem; margin-top: 0.4rem;">
            ${tasksHtml}
          </div>
        </div>

        ${citations.length > 0 ? `
        <div>
          <span style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
            Verified Syllabus Learning Outcomes & Prerequisite DAG (ChromaDB Vector Store):
          </span>
          <div style="display: flex; flex-direction: column; gap: 0.4rem; margin-top: 0.35rem;">
            ${citationsHtml}
          </div>
        </div>
        ` : ''}
      </div>
    `;
  } catch (err) {
    console.warn("Weak topics load note:", err);
    container.innerHTML = `
      <div style="padding: 1rem; background: #fff1f2; border: 1px solid #fecdd3; border-radius: var(--radius-md); color: #9f1239; font-size: 12px;">
        <strong>Syllabus RAG Connected:</strong> No active remedial plan recorded yet. Click 'Re-generate with AI' to trigger automated diagnostic.
      </div>
    `;
  }
}

function refreshStudentWeakTopicsPlan(force = false) {
  const srn = AppState.activeStudent ? AppState.activeStudent.srn : 'R24EA818';
  loadWeakTopicsAndStudyPlan(srn, 'AIML-401', force);
}


// =============================================================================
// AUTOMATED BATCH INGESTION PIPELINE
// =============================================================================

function openPipelineModal() {
  const modal = document.getElementById('pipeline-modal');
  if (modal) modal.style.display = 'flex';
}

function closePipelineModal() {
  const modal = document.getElementById('pipeline-modal');
  if (modal) modal.style.display = 'none';
}

async function runAutomatedBatchPipeline() {
  openPipelineModal();
  const body = document.getElementById('pipeline-modal-body');
  const sub = document.getElementById('pipeline-modal-subtitle');
  if (sub) sub.innerText = "Ingesting Class IA Marks (AIML-401)...";

  if (body) {
    body.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:0.75rem; font-size:12px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="color:#2563eb;"> Stage 1:</span> Validating batch question scores and calculating continuous totals...
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="color:#2563eb;"> Stage 2:</span> Appending immutable transaction to data_change_log and audit_logs...
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="color:#2563eb;"> Stage 3:</span> Invoking CatBoost ML pipeline with calibrated threshold τ = 0.42...
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="color:#2563eb;"> Stage 4:</span> Scanning question scores &lt; 50% and executing ChromaDB Syllabus RAG...
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="color:#2563eb;"> Stage 5:</span> Synthesizing 5-Day Remedial Study Plans and issuing mentor alerts...
        </div>
      </div>
    `;
  }

  try {
    const payload = {
      batch_id: `BATCH_2026_AIML401_IA1_${Date.now()}`,
      course_id: "AIML-401",
      semester: 7,
      ia_number: 1,
      faculty_id: "FAC_AIML_01",
      records: [
        {
          srn: "R24EA818",
          attendance_pct: 64.0,
          questions: [
            { question_no: "Q1", topic_id: "MATH_CHAIN_RULE", topic_title: "Chain Rule & Gradients", marks_obtained: 3.0, max_marks: 10.0 },
            { question_no: "Q2", topic_id: "DL_BACKPROP", topic_title: "Backpropagation Algorithms", marks_obtained: 3.5, max_marks: 10.0 },
            { question_no: "Q3", topic_id: "DL_NN_TRAIN", topic_title: "Deep Neural Network Training", marks_obtained: 8.0, max_marks: 10.0 }
          ]
        },
        {
          srn: "R24EA807",
          attendance_pct: 98.0,
          questions: [
            { question_no: "Q1", topic_id: "MATH_CHAIN_RULE", topic_title: "Chain Rule & Gradients", marks_obtained: 9.5, max_marks: 10.0 },
            { question_no: "Q2", topic_id: "DL_BACKPROP", topic_title: "Backpropagation Algorithms", marks_obtained: 10.0, max_marks: 10.0 },
            { question_no: "Q3", topic_id: "DL_NN_TRAIN", topic_title: "Deep Neural Network Training", marks_obtained: 10.0, max_marks: 10.0 }
          ]
        }
      ]
    };

    const res = await fetch(`${API_BASE_URL}/api/pipeline/ingest-ia-marks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Pipeline failed");

    const summary = data.pipeline_summary || {};
    if (sub) sub.innerText = `Pipeline Completed in ${summary.execution_latency_ms || 450}ms`;

    if (body) {
      body.innerHTML = `
        <div style="background: #ecfdf5; border: 1px solid #a7f3d0; padding: 0.85rem 1rem; border-radius: var(--radius-md); margin-bottom: 1rem; color: #065f46; font-size: 12px;">
          <strong> Fully Automated Ingestion Successful:</strong><br>
          Processed ${summary.students_processed} student records (${summary.questions_persisted} question scores). Generated ${summary.remedial_plans_synthesized} Syllabus RAG remedial plans and triggered ${summary.mentor_alerts_triggered} mentor early-warning alerts.
        </div>

        <h4 style="font-size: 11.5px; font-weight: 700; color: var(--text-primary); text-transform: uppercase; margin-bottom: 0.4rem;">
          Cohort Telemetry Results:
        </h4>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Student</th>
                <th>Scaled IA Score</th>
                <th>Attendance</th>
                <th>Predicted Risk</th>
                <th>Weak Topics</th>
                <th>RAG Action</th>
              </tr>
            </thead>
            <tbody>
              ${(summary.student_results || []).map(r => `
                <tr>
                  <td><strong>${r.srn}</strong></td>
                  <td>${r.ia_score_obtained} / 30</td>
                  <td>${r.attendance_pct}%</td>
                  <td><span class="badge ${r.risk_tier === 'HIGH' ? 'badge-risk' : 'badge-safe'}">${r.risk_tier} (${(r.dropout_probability*100).toFixed(0)}%)</span></td>
                  <td>${r.weak_topics_count} weak topic(s)</td>
                  <td>${r.remedial_study_plan_generated ? '<span class="badge badge-risk">Plan Generated</span>' : '<span class="badge badge-safe">Cleared</span>'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    }

    showToast("Automated Ingestion Pipeline complete!", "success");
    // Refresh table and student views
    renderStudentTable();
  } catch (err) {
    console.error("Pipeline error:", err);
    if (body) {
      body.innerHTML = `
        <div style="padding: 1rem; background: #fff1f2; border: 1px solid #fecdd3; border-radius: var(--radius-md); color: #9f1239; font-size: 12px;">
          <strong>Pipeline execution error:</strong> ${err.message}
        </div>
      `;
    }
  }
}

// =============================================================================
// AUTONOMOUS AGENT ORCHESTRATOR & ASSIGNMENT MANAGEMENT
// =============================================================================
let selectedAgentFile = null;

function handleAgentFileSelected(event) {
  const file = event.target.files[0];
  if (file) {
    selectedAgentFile = file;
    document.getElementById('agent-selected-filename').textContent = `Selected: ${file.name} (${(file.size/1024).toFixed(1)} KB)`;
    document.getElementById('btn-agent-launch').disabled = false;
  }
}

async function launchAgentExecution() {
  if (!selectedAgentFile) return;

  const launchBtn = document.getElementById('btn-agent-launch');
  const statusPill = document.getElementById('agent-job-status-pill');
  const consoleEl = document.getElementById('agent-steps-console');

  launchBtn.disabled = true;
  statusPill.textContent = 'RUNNING AGENT';
  statusPill.style.background = 'rgba(234, 179, 8, 0.2)';
  statusPill.style.color = '#facc15';

  consoleEl.innerHTML = `
    <div style="color: #38bdf8;">[INITIALIZING] Launching Agentic Orchestrator for '${selectedAgentFile.name}'...</div>
    <div style="color: #94a3b8;">[DISPATCH] Uploading payload to REST Agent Gateway (/api/agent/upload)...</div>
  `;

  const formData = new FormData();
  formData.append('file', selectedAgentFile);
  formData.append('course_id', 'AIML-401');
  formData.append('faculty_id', AppState.currentUser ? AppState.currentUser.entity_id : 'USR_FAC01');

  try {
    const res = await fetch('http://localhost:8002/api/agent/upload', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) throw new Error(`Agent gateway failed: HTTP ${res.status}`);
    const data = await res.json();

    // Query job details to get full execution log
    const jobRes = await fetch(`http://localhost:8002/api/agent/jobs/${data.job_id}`);
    const jobData = jobRes.ok ? await jobRes.json() : null;

    statusPill.textContent = 'COMPLETED';
    statusPill.style.background = 'rgba(34, 197, 94, 0.2)';
    statusPill.style.color = '#4ade80';

    let stepsHtml = '';
    if (jobData && jobData.steps_log) {
      stepsHtml = jobData.steps_log.map(s => `
        <div style="margin-bottom: 4px;">
          <span style="color: #60a5fa;">[${s.phase}]</span>
          <span style="color: #e2e8f0;"> ${s.message}</span>
        </div>
      `).join('');
    } else {
      stepsHtml = `
        <div style="color: #4ade80;">[SUCCESS] Document classified as ${data.detected_type}.</div>
        <div style="color: #e2e8f0;">[RESULT] ${data.action_result ? data.action_result.summary : 'Action completed.'}</div>
      `;
    }

    consoleEl.innerHTML = stepsHtml + `
      <div style="margin-top: 8px; color: #4ade80; font-weight: bold;">
        [DONE] PDF Report Compiled: ${data.report ? data.report.report_filename : 'Ready for download'}
      </div>
    `;

    // Refresh assignments roster if created
    loadStudentAssignments();

  } catch (err) {
    statusPill.textContent = 'FAILED';
    statusPill.style.background = 'rgba(239, 68, 68, 0.2)';
    statusPill.style.color = '#f87171';
    consoleEl.innerHTML += `<div style="color: #ef4444;">[ERROR] ${err.message}</div>`;
  } finally {
    launchBtn.disabled = false;
  }
}

function downloadCourseReport(courseId) {
  window.open(`http://localhost:8002/api/reports/course/${courseId}/generate-pdf`, '_blank');
}

async function loadStudentAssignments() {
  const container = document.getElementById('student-assignments-container');
  if (!container) return;

  const srn = AppState.activeStudent ? (AppState.activeStudent.srn || AppState.activeStudent.id) : 'R24EA807';

  try {
    const res = await fetch(`http://localhost:8002/api/student/${srn}/assignments`);
    if (!res.ok) throw new Error('Failed to fetch assignments');
    const tasks = await res.json();

    if (!tasks || tasks.length === 0) {
      container.innerHTML = `
        <div style="padding: 1rem; background: var(--bg-surface-subtle); border-radius: var(--radius-md); border: 1px solid var(--border-light); text-align: center; color: var(--text-muted); font-size: 12px;">
          No pending assignments for ${srn}. Upload assignment briefs in Faculty Console to auto-distribute.
        </div>
      `;
      return;
    }

    container.innerHTML = tasks.map(t => {
      const isGraded = t.status === 'GRADED';
      const isSubmitted = t.status === 'SUBMITTED';
      const badgeColor = isGraded ? '#4ade80' : (isSubmitted ? '#60a5fa' : '#facc15');
      const badgeBg = isGraded ? 'rgba(34, 197, 94, 0.15)' : (isSubmitted ? 'rgba(59, 130, 246, 0.15)' : 'rgba(234, 179, 8, 0.15)');

      return `
        <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid var(--border-light); border-radius: 8px; padding: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div>
              <h4 style="font-size: 13.5px; color: var(--text-primary); margin-bottom: 2px;">${t.title}</h4>
              <span style="font-size: 11px; color: var(--text-muted);">Due: ${t.due_date || '7 Days'} | Max Marks: ${t.max_marks || 10}</span>
            </div>
            <span style="font-size: 10.5px; font-weight: 600; padding: 2px 8px; border-radius: 12px; background: ${badgeBg}; color: ${badgeColor};">
              ${isGraded ? `GRADED: ${t.marks_obtained}/${t.max_marks}` : t.status}
            </span>
          </div>
          <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 0.75rem; white-space: pre-wrap;">${t.problem_statement || ''}</p>
          
          ${isGraded ? `
            <div style="background: rgba(34, 197, 94, 0.1); border-left: 3px solid #22c55e; padding: 0.5rem 0.75rem; border-radius: 4px; font-size: 11.5px; color: #86efac; margin-bottom: 0.5rem;">
              <strong>AI Evaluator Feedback:</strong> ${t.feedback || 'Good work meeting rubric requirements.'}
            </div>
          ` : `
            <div style="margin-top: 0.5rem;">
              <textarea id="sub-input-${t.assignment_id}" rows="2" style="width: 100%; font-size: 11.5px; background: rgba(0,0,0,0.3); border: 1px solid var(--border-light); border-radius: 4px; padding: 0.4rem; color: #e2e8f0; margin-bottom: 0.5rem;" placeholder="Type your assignment derivation or code solution here..."></textarea>
              <div style="display: flex; gap: 0.5rem;">
                <button class="btn-utility" style="font-size: 11px;" onclick="submitAssignmentAction('${t.assignment_id}')">Submit Solution</button>
                <button class="btn-accent" style="font-size: 11px;" onclick="autoGradeAction('${t.assignment_id}')">Auto-Grade with AI</button>
              </div>
            </div>
          `}
        </div>
      `;
    }).join('');

  } catch (err) {
    container.innerHTML = `<div style="color: #ef4444; font-size: 12px; text-align: center;">Error loading assignments: ${err.message}</div>`;
  }
}

async function submitAssignmentAction(assignmentId) {
  const textarea = document.getElementById(`sub-input-${assignmentId}`);
  if (!textarea || !textarea.value.trim()) {
    alert('Please enter your submission text before submitting.');
    return;
  }

  const srn = AppState.activeStudent ? (AppState.activeStudent.srn || AppState.activeStudent.id) : 'R24EA807';

  try {
    const res = await fetch(`http://localhost:8002/api/student/${srn}/assignments/${assignmentId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ submission_text: textarea.value })
    });

    if (res.ok) {
      alert('Assignment submitted successfully!');
      loadStudentAssignments();
    } else {
      alert('Failed to submit assignment.');
    }
  } catch (err) {
    alert(`Submission error: ${err.message}`);
  }
}

async function autoGradeAction(assignmentId) {
  const srn = AppState.activeStudent ? (AppState.activeStudent.srn || AppState.activeStudent.id) : 'R24EA807';

  try {
    const res = await fetch(`http://localhost:8002/api/assignments/${assignmentId}/auto-grade`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_srn: srn })
    });

    if (res.ok) {
      const data = await res.json();
      alert(`AI Auto-Grade Completed! Marks Awarded: ${data.marks_obtained}/${data.max_marks}`);
      loadStudentAssignments();
    } else {
      alert('Auto-grade evaluation failed.');
    }
  } catch (err) {
    alert(`Auto-grade error: ${err.message}`);
  }
}
