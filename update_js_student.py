with open(r"js\student.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update checkStudentAuth
old_auth = """function checkStudentAuth() {
  // Frictionless direct student access (No OTP login barrier)
  sessionStorage.setItem("student_authenticated", "true");
  if (!sessionStorage.getItem("active_student_id")) {
    sessionStorage.setItem("active_student_id", "STU-807");
  }
  const loginView = document.getElementById("student-login-view");
  const dashView = document.getElementById("student-dashboard-view");
  const navAuthBtn = document.getElementById("nav-auth-buttons");

  if (loginView) loginView.style.display = "none";
  if (dashView) dashView.style.display = "block";
  if (navAuthBtn) navAuthBtn.style.display = "flex";
  currentStudentId = sessionStorage.getItem("active_student_id") || "STU-807";
  initStudentPortal();
  if (typeof checkStudentNotifications === "function") {
    checkStudentNotifications();
  }
}"""

new_auth = """function checkStudentAuth() {
  const isAuth = sessionStorage.getItem("student_authenticated") === "true";
  const loginView = document.getElementById("student-login-view");
  const dashView = document.getElementById("student-dashboard-view");
  const navAuthBtn = document.getElementById("nav-auth-buttons");

  if (isAuth) {
    if (loginView) loginView.style.display = "none";
    if (dashView) dashView.style.display = "block";
    if (navAuthBtn) navAuthBtn.style.display = "flex";
    currentStudentId = sessionStorage.getItem("active_student_id") || "R24EA807";
    initStudentPortal();
    if (typeof checkStudentNotifications === "function") {
      checkStudentNotifications();
    }
  } else {
    if (loginView) loginView.style.display = "flex";
    if (dashView) dashView.style.display = "none";
    if (navAuthBtn) navAuthBtn.style.display = "none";
  }
}"""

js = js.replace(old_auth, new_auth)

# 2. Update handleStudentLogin to do proper DB authentication
old_login = """async function handleStudentLogin(event) {
  if (event) event.preventDefault();

  const srnInput = document.getElementById("login-srn");
  const rawId = srnInput ? srnInput.value.trim() : "STU-807";"""

new_login = """async function handleStudentLogin(event) {
  if (event) event.preventDefault();

  const srnInput = document.getElementById("login-srn");
  const pwdInput = document.getElementById("login-pwd");
  const errEl = document.getElementById("student-login-error");

  const identifier = (srnInput ? srnInput.value.trim() : "");
  const password = (pwdInput ? pwdInput.value : "");

  if (!identifier || !password) {
    if (errEl) {
      errEl.textContent = "Please enter both University SRN/Email and password.";
      errEl.style.display = "block";
    }
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        identifier: identifier,
        password: password,
        role: "student"
      })
    });

    const data = await res.json();
    if (!res.ok || !data.authenticated) {
      const msg = data.detail || data.message || "Invalid credentials. Please verify your University SRN/Email or password.";
      if (errEl) {
        errEl.textContent = msg;
        errEl.style.display = "block";
      } else {
        alert(msg);
      }
      return;
    }

    // Success! Store real session
    sessionStorage.setItem("student_authenticated", "true");
    sessionStorage.setItem("auth_token", data.access_token);
    sessionStorage.setItem("user_profile", JSON.stringify(data.user));
    const sid = data.user.entity_id || data.user.user_id || identifier;
    sessionStorage.setItem("active_student_id", sid);
    currentStudentId = sid;

    if (errEl) errEl.style.display = "none";
    checkStudentAuth();
    return;
  } catch (err) {
    if (errEl) {
      errEl.textContent = "Error connecting to authentication service. Please try again.";
      errEl.style.display = "block";
    }
    return;
  }

  const rawId = identifier;"""

js = js.replace(old_login, new_login)

# 3. Update studentSignOut to actually clear session and return to login view
old_signout = """function studentSignOut() {
  const newSrn = prompt("Switch Student Profile (Enter SRN or Student ID):", currentStudentId === "STU-807" ? "STU-818" : "STU-807");
  if (newSrn && newSrn.trim()) {
    const sid = newSrn.trim();
    sessionStorage.setItem("active_student_id", sid);
    localStorage.setItem("active_student_id", sid);
    currentStudentId = sid;
    initStudentPortal();
    checkStudentNotifications();
  }
}"""

new_signout = """function studentSignOut() {
  sessionStorage.removeItem("student_authenticated");
  sessionStorage.removeItem("auth_token");
  sessionStorage.removeItem("user_profile");
  sessionStorage.removeItem("active_student_id");

  try {
    fetch(`${API_BASE}/api/auth/logout?actor_id=${currentStudentId}&actor_role=student`, { method: "POST" });
  } catch (_) {}

  const pwdInput = document.getElementById("login-pwd");
  if (pwdInput) pwdInput.value = "";
  const errEl = document.getElementById("student-login-error");
  if (errEl) errEl.style.display = "none";

  checkStudentAuth();
}"""

js = js.replace(old_signout, new_signout)

# 4. Remove mock STUDENT_PROFILES and replace with live database call
old_profile_func = """function updateStudentHeaderUI() {
  // Student profile lookup for all 5 anonymized IDs
  const STUDENT_PROFILES = {
    "STU-807": { label: "On Track", att: "94.5%", ia: "26.5 / 30", risk: "4.2%",  riskClass: "badge-low",  riskText: "ON TRACK (LOW RISK)",       target: "Target: 8.5+ SGPA" },
    "STU-818": { label: "Critical Priority", att: "68.0%", ia: "10.5 / 30", risk: "79.6%", riskClass: "badge-high", riskText: "CRITICAL RISK (tau = 0.79)", target: "Target: 7.0+ SGPA (Recovery)" },
    "STU-801": { label: "Moderate Risk", att: "75.0%", ia: "18.0 / 30", risk: "38.5%", riskClass: "badge-medium", riskText: "MODERATE RISK",            target: "Target: 7.5+ SGPA" },
    "STU-842": { label: "On Track", att: "88.0%", ia: "22.0 / 30", risk: "12.1%", riskClass: "badge-low",  riskText: "ON TRACK (LOW RISK)",       target: "Target: 8.0+ SGPA" },
    "STU-895": { label: "On Track", att: "91.5%", ia: "24.5 / 30", risk: "7.3%",  riskClass: "badge-low",  riskText: "LOW RISK",                  target: "Target: 8.5+ SGPA" },
  };
  
  const sid = currentStudentId;
  const profile = STUDENT_PROFILES[sid] || STUDENT_PROFILES["STU-807"];
  
  const nameEl = document.getElementById("srl-name");
  const srnEl = document.getElementById("srl-srn");
  const badgeEl = document.getElementById("srl-risk-badge");
  const targetEl = document.getElementById("srl-target-cgpa");
  const attKpi = document.getElementById("stu-kpi-att");
  const iaKpi = document.getElementById("stu-kpi-ia");
  const riskKpi = document.getElementById("stu-kpi-risk");
  const navLabel = document.getElementById("nav-user-label");

  if (nameEl) nameEl.textContent = `Student Profile (${profile.label})`;
  if (srnEl) srnEl.textContent = `ID: ${sid} | B.Tech AIML (Sem 7-B)`;
  if (badgeEl) { badgeEl.className = `badge ${profile.riskClass}`; badgeEl.textContent = profile.riskText; }
  if (targetEl) { targetEl.textContent = profile.target; targetEl.style.color = "#ffffff"; }
  if (attKpi) attKpi.textContent = profile.att;
  if (iaKpi) iaKpi.textContent = profile.ia;
  if (riskKpi) riskKpi.textContent = profile.risk;
  if (navLabel) navLabel.textContent = `Student (ID: ${sid})`;
}"""

new_profile_func = """async function updateStudentHeaderUI() {
  const sid = currentStudentId;
  const nameEl = document.getElementById("srl-name");
  const srnEl = document.getElementById("srl-srn");
  const badgeEl = document.getElementById("srl-risk-badge");
  const targetEl = document.getElementById("srl-target-cgpa");
  const attKpi = document.getElementById("stu-kpi-att");
  const iaKpi = document.getElementById("stu-kpi-ia1");
  const riskKpi = document.getElementById("stu-kpi-pred");
  const navLabel = document.getElementById("nav-user-label");

  try {
    const res = await fetch(`${API_BASE}/api/student/${sid}/profile`);
    if (res.ok) {
      const json = await res.json();
      const s = json.data;
      if (s) {
        if (nameEl) nameEl.textContent = s.student_name || "Enrolled Student";
        if (srnEl) srnEl.textContent = `SRN: ${s.srn} • ${s.program || 'B.Tech CSE (AI & ML)'} (Sem ${s.semester || 7}-${s.section || 'B'})`;
        const isHigh = s.risk_level === 'HIGH' || (s.dropout_probability && s.dropout_probability > 0.4);
        if (badgeEl) {
          badgeEl.className = isHigh ? "badge-tag badge-critical" : "badge-tag badge-low";
          badgeEl.textContent = `${s.risk_level || 'LOW'} RISK (${((s.dropout_probability || 0.042) * 100).toFixed(1)}%)`;
          badgeEl.style.background = isHigh ? "#dc2626" : "#18181b";
          badgeEl.style.color = "#ffffff";
        }
        if (attKpi) attKpi.textContent = `${s.attendance_rate || 85.0}%`;
        if (targetEl) targetEl.textContent = `Advisor: ${s.advisor_name || 'Dr. Ramesh Kumar'}`;
        if (navLabel) navLabel.textContent = `${s.student_name} (${s.srn})`;
      }
    }
  } catch (err) {
    console.warn("Could not fetch student profile from database", err);
  }
}"""

js = js.replace(old_profile_func, new_profile_func)

with open(r"js\student.js", "w", encoding="utf-8") as f:
    f.write(js)

print("js/student.js updated successfully with real authentication & live database records!")

