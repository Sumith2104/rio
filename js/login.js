/**
 * =============================================================================
 * REVA Smart Campus Intelligence & Student Success Platform (PACD-RAG)
 * Authentication & Landing Gateway Controller
 * =============================================================================
 */

var API_BASE = window.API_BASE || (window.location && window.location.origin && window.location.origin !== "null" ? window.location.origin : "http://localhost:8002");
let currentRole = "student";

document.addEventListener("DOMContentLoaded", () => {
  initLoginPage();
});

function initLoginPage() {
  checkActiveSession();
  checkSystemHealth();
  setupEventListeners();
}

function setupEventListeners() {
  const form = document.getElementById("login-form");
  if (form) {
    form.addEventListener("submit", handleLogin);
  }

  // Pre-fill student role by default
  switchRole("student");
}

/**
 * Switch between Student and Faculty role modes
 */
function switchRole(role) {
  currentRole = role;
  hideAlert();

  const btnStudent = document.getElementById("tab-student");
  const btnFaculty = document.getElementById("tab-faculty");
  const roleBadge = document.getElementById("auth-role-badge");
  const titleEl = document.getElementById("auth-form-title");
  const descEl = document.getElementById("auth-form-desc");
  const idLabel = document.getElementById("id-field-label");
  const idInput = document.getElementById("identifier-input");
  const submitBtn = document.getElementById("auth-submit-btn");
  const studentDemoGroup = document.getElementById("student-demo-group");
  const facultyDemoGroup = document.getElementById("faculty-demo-group");

  if (role === "student") {
    if (btnStudent) {
      btnStudent.className = "auth-tab-btn active-student";
    }
    if (btnFaculty) {
      btnFaculty.className = "auth-tab-btn";
    }

    if (roleBadge) {
      roleBadge.textContent = "STUDENT SUCCESS PORTAL";
      roleBadge.className = "auth-badge-role student-theme";
    }
    if (titleEl) titleEl.textContent = "Sign In as Student";
    if (descEl) {
      descEl.textContent = "Access syllabus-grounded remedial plans, interactive tutor, and auto-graded assignments.";
    }
    if (idLabel) idLabel.textContent = "Student ID or Institutional Email";
    if (idInput) {
      idInput.placeholder = "e.g. STU-807 or student.profile@reva.edu.in";
      idInput.className = "input-custom";
    }
    if (submitBtn) {
      submitBtn.className = "auth-submit-btn student-btn";
      submitBtn.innerHTML = `
        <span>Sign In to Student Portal</span>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      `;
    }

    if (studentDemoGroup) studentDemoGroup.style.display = "flex";
    if (facultyDemoGroup) facultyDemoGroup.style.display = "none";
  } else {
    if (btnFaculty) {
      btnFaculty.className = "auth-tab-btn active-faculty";
    }
    if (btnStudent) {
      btnStudent.className = "auth-tab-btn";
    }

    if (roleBadge) {
      roleBadge.textContent = "FACULTY & MENTOR CONSOLE";
      roleBadge.className = "auth-badge-role faculty-theme";
    }
    if (titleEl) titleEl.textContent = "Sign In as Faculty Advisor";
    if (descEl) {
      descEl.textContent = "Access autonomous multi-format file ingestion, ReAct agent traces, and cohort risk diagnostics.";
    }
    if (idLabel) idLabel.textContent = "Faculty ID or Institutional Email";
    if (idInput) {
      idInput.placeholder = "e.g. FAC_AIML_01 or ramesh.kumar@reva.edu.in";
      idInput.className = "input-custom faculty-focus";
    }
    if (submitBtn) {
      submitBtn.className = "auth-submit-btn faculty-btn";
      submitBtn.innerHTML = `
        <span>Sign In to Faculty Console</span>
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
      `;
    }

    if (studentDemoGroup) studentDemoGroup.style.display = "none";
    if (facultyDemoGroup) facultyDemoGroup.style.display = "flex";
  }
}

/**
 * Handle form authentication
 */
async function handleLogin(e) {
  if (e) e.preventDefault();
  hideAlert();

  const idInput = document.getElementById("identifier-input");
  const pwdInput = document.getElementById("password-input");
  const submitBtn = document.getElementById("auth-submit-btn");

  const identifier = idInput ? idInput.value.trim() : "";
  const password = pwdInput ? pwdInput.value : "";

  if (!identifier) {
    showAlert("Please enter your Institutional ID or Email.", "error");
    if (idInput) idInput.focus();
    return;
  }
  if (!password) {
    showAlert("Please enter your account password.", "error");
    if (pwdInput) pwdInput.focus();
    return;
  }

  // Loading state
  const originalBtnHtml = submitBtn ? submitBtn.innerHTML : "";
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
      <svg class="spin-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
      <span>Authenticating...</span>
    `;
  }

  try {
    const response = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ identifier, password })
    });

    const data = await response.json();

    if (!response.ok || !data.authenticated) {
      const errorMsg = data.detail || data.message || "Authentication failed. Please verify credentials.";
      showAlert(errorMsg, "error");
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnHtml;
      }
      return;
    }

    // Login successful
    showAlert("Authentication successful! Redirecting to dashboard...", "success");

    const user = data.user || {};
    const role = (user.role || currentRole).toLowerCase();
    const token = data.access_token || "";

    localStorage.setItem("auth_token", token);
    localStorage.setItem("auth_role", role);

    if (role === "student") {
      // Map identifier or entity to anonymous student id
      let stuId = "STU-807";
      const rawEntity = (user.entity_id || identifier || "").toUpperCase();
      const rawUser = (user.user_id || "").toUpperCase();

      if (rawEntity.includes("818") || rawUser.includes("818") || identifier.toLowerCase().includes("atrisk")) {
        stuId = "STU-818";
      } else if (rawEntity.includes("842") || rawUser.includes("842")) {
        stuId = "STU-842";
      }

      localStorage.setItem("active_student_id", stuId);
      localStorage.setItem("auth_user", JSON.stringify({
        ...user,
        display_name: `Student Profile (${stuId})`
      }));

      setTimeout(() => {
        window.location.href = "student.html";
      }, 500);

    } else {
      // Faculty / Admin
      let facId = user.entity_id || "FAC_AIML_01";
      localStorage.setItem("active_faculty_id", facId);
      localStorage.setItem("auth_user", JSON.stringify({
        ...user,
        display_name: `Faculty Advisor (${facId})`
      }));

      setTimeout(() => {
        window.location.href = "faculty.html";
      }, 500);
    }

  } catch (err) {
    console.error("Login fetch error:", err);
    showAlert("Could not connect to FastAPI server (port 8002). Check connection status.", "error");
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnHtml;
    }
  }
}

/**
 * 1-Click Quick Demo Login (Anonymized)
 */
function quickDemoLogin(role, identifier, password, optionalEntityId) {
  switchRole(role);

  const idInput = document.getElementById("identifier-input");
  const pwdInput = document.getElementById("password-input");

  if (idInput) idInput.value = identifier;
  if (pwdInput) pwdInput.value = password;

  if (optionalEntityId) {
    if (role === "student") {
      localStorage.setItem("active_student_id", optionalEntityId);
    } else {
      localStorage.setItem("active_faculty_id", optionalEntityId);
    }
  }

  // Trigger login directly
  handleLogin();
}

/**
 * Toggle Password Visibility
 */
function togglePasswordVisibility() {
  const pwdInput = document.getElementById("password-input");
  const eyeIcon = document.getElementById("eye-icon");
  if (!pwdInput) return;

  if (pwdInput.type === "password") {
    pwdInput.type = "text";
    if (eyeIcon) {
      // Show eye slash
      eyeIcon.innerHTML = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24M1 1l22 22"/>`;
    }
  } else {
    pwdInput.type = "password";
    if (eyeIcon) {
      // Show open eye
      eyeIcon.innerHTML = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>`;
    }
  }
}

/**
 * Show alert banner inside card
 */
function showAlert(message, type = "error") {
  const alertEl = document.getElementById("login-alert");
  if (!alertEl) return;

  alertEl.textContent = message;
  alertEl.className = type === "error" ? "auth-alert alert-error" : "auth-alert alert-success";
}

/**
 * Hide alert banner
 */
function hideAlert() {
  const alertEl = document.getElementById("login-alert");
  if (alertEl) {
    alertEl.style.display = "none";
  }
}

/**
 * Check if a valid session already exists in localStorage
 */
function checkActiveSession() {
  const token = localStorage.getItem("auth_token");
  const role = localStorage.getItem("auth_role");
  const sessionBanner = document.getElementById("active-session-banner");
  const sessionText = document.getElementById("active-session-text");

  if (token && role && sessionBanner) {
    const isStudent = role.toLowerCase() === "student";
    const entityId = isStudent 
      ? (localStorage.getItem("active_student_id") || "STU-807")
      : (localStorage.getItem("active_faculty_id") || "FAC_AIML_01");

    if (sessionText) {
      sessionText.innerHTML = `
        Active session detected: <strong>${isStudent ? "Student Profile" : "Faculty Advisor"} (${entityId})</strong>.
      `;
    }
    sessionBanner.classList.add("visible");
  }
}

/**
 * Resume detected active session
 */
function resumeActiveSession() {
  const role = localStorage.getItem("auth_role");
  if (role && role.toLowerCase() === "faculty") {
    window.location.href = "faculty.html";
  } else {
    window.location.href = "student.html";
  }
}

/**
 * Clear session and switch accounts
 */
function clearActiveSession() {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("auth_role");
  localStorage.removeItem("auth_user");
  const sessionBanner = document.getElementById("active-session-banner");
  if (sessionBanner) {
    sessionBanner.classList.remove("visible");
  }
  showAlert("Previous session cleared. You can now sign in with a different account.", "success");
}

/**
 * Check health status of FastAPI engine
 */
async function checkSystemHealth() {
  const statusPill = document.getElementById("nav-system-status");
  if (!statusPill) return;

  try {
    const res = await fetch(`${API_BASE}/`, { method: "GET" });
    if (res.ok) {
      statusPill.innerHTML = `
        <span class="pulse-dot"></span>
        <span>FastAPI 8002 &amp; ChromaDB Active</span>
      `;
    }
  } catch (err) {
    statusPill.innerHTML = `
      <span class="pulse-dot" style="background: #f59e0b;"></span>
      <span>FastAPI 8002 Connecting...</span>
    `;
  }
}
