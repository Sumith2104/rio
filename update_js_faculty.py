with open(r"js\faculty.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update checkFacultyAuth
old_auth = """function checkFacultyAuth() {
  // Direct frictionless access: No OTP gating
  sessionStorage.setItem("faculty_authenticated", "true");
  if (!sessionStorage.getItem("active_faculty_id")) {
    sessionStorage.setItem("active_faculty_id", "FAC_AIML_01");
  }
  const loginView = document.getElementById("faculty-login-view");
  const dashView = document.getElementById("faculty-dashboard-view");

  if (loginView) loginView.style.display = "none";
  if (dashView) dashView.style.display = "block";
  activeFacultyId = sessionStorage.getItem("active_faculty_id") || "FAC_AIML_01";
  updateFacultyHeaderUI();
  initFacultyConsole();
  if (typeof loadFacultyUploadedMaterials === "function") {
    loadFacultyUploadedMaterials();
  }
}"""

new_auth = """function checkFacultyAuth() {
  const isAuth = sessionStorage.getItem("faculty_authenticated") === "true";
  const loginView = document.getElementById("faculty-login-view");
  const dashView = document.getElementById("faculty-dashboard-view");

  if (isAuth) {
    if (loginView) loginView.style.display = "none";
    if (dashView) dashView.style.display = "block";
    activeFacultyId = sessionStorage.getItem("active_faculty_id") || "FAC_AIML_01";
    updateFacultyHeaderUI();
    initFacultyConsole();
    if (typeof loadFacultyUploadedMaterials === "function") {
      loadFacultyUploadedMaterials();
    }
  } else {
    if (loginView) loginView.style.display = "flex";
    if (dashView) dashView.style.display = "none";
  }
}"""

js = js.replace(old_auth, new_auth)

# 2. Update handleFacultyPasswordLogin
old_fac_login = """async function handleFacultyPasswordLogin(event) {
  if (event) event.preventDefault();

  const idInput = document.getElementById("fac-login-id");
  const fid = idInput.value.trim() || "FAC_AIML_01";"""

new_fac_login = """async function handleFacultyPasswordLogin(event) {
  if (event) event.preventDefault();

  const idInput = document.getElementById("fac-login-id");
  const pwdInput = document.getElementById("fac-login-pwd");
  const errEl = document.getElementById("faculty-login-error");

  const identifier = (idInput ? idInput.value.trim() : "");
  const password = (pwdInput ? pwdInput.value : "");

  if (!identifier || !password) {
    if (errEl) {
      errEl.textContent = "Please enter both Faculty ID / Email and password.";
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
        role: "faculty"
      })
    });

    const data = await res.json();
    if (!res.ok || !data.authenticated) {
      const msg = data.detail || data.message || "Invalid credentials. Please verify your Faculty ID or password.";
      if (errEl) {
        errEl.textContent = msg;
        errEl.style.display = "block";
      } else {
        alert(msg);
      }
      return;
    }

    sessionStorage.setItem("faculty_authenticated", "true");
    sessionStorage.setItem("faculty_auth_token", data.access_token);
    sessionStorage.setItem("faculty_profile", JSON.stringify(data.user));
    const fid = data.user.entity_id || data.user.user_id || identifier;
    sessionStorage.setItem("active_faculty_id", fid);
    activeFacultyId = fid;

    if (errEl) errEl.style.display = "none";
    checkFacultyAuth();
    return;
  } catch (err) {
    if (errEl) {
      errEl.textContent = "Error connecting to faculty authentication service.";
      errEl.style.display = "block";
    }
    return;
  }

  const fid = identifier;"""

js = js.replace(old_fac_login, new_fac_login)

# 3. Update facultySignOut to actually clear session and return to login view
old_fac_signout = """function facultySignOut() {
  const newFid = prompt("Switch Faculty Profile (Enter Faculty ID or Email):", activeFacultyId === "FAC_AIML_01" ? "FAC_AIML_02" : "FAC_AIML_01");
  if (newFid && newFid.trim()) {
    activeFacultyId = newFid.trim();
    sessionStorage.setItem("active_faculty_id", activeFacultyId);
    updateFacultyHeaderUI();
    initFacultyConsole();
    if (typeof loadFacultyUploadedMaterials === "function") {
      loadFacultyUploadedMaterials();
    }
  }
}"""

new_fac_signout = """function facultySignOut() {
  sessionStorage.removeItem("faculty_authenticated");
  sessionStorage.removeItem("faculty_auth_token");
  sessionStorage.removeItem("faculty_profile");
  sessionStorage.removeItem("active_faculty_id");

  try {
    fetch(`${API_BASE}/api/auth/logout?actor_id=${activeFacultyId}&actor_role=faculty`, { method: "POST" });
  } catch (_) {}

  const pwdInput = document.getElementById("fac-login-pwd");
  if (pwdInput) pwdInput.value = "";
  const errEl = document.getElementById("faculty-login-error");
  if (errEl) errEl.style.display = "none";

  checkFacultyAuth();
}"""

js = js.replace(old_fac_signout, new_fac_signout)

# 4. Replace mock cohort and weak topics functions with live database calls
old_render_cohort = """function renderCohortTable(filterQuery = "") {
  const tbody = document.getElementById("cohort-table-body");
  if (!tbody) return;

  const q = filterQuery.toLowerCase();
  const filtered = ANONYMIZED_COHORT.filter(s => 
    s.id.toLowerCase().includes(q) || s.risk.toLowerCase().includes(q)
  );

  tbody.innerHTML = filtered.map(s => {
    const isCritical = s.risk === "CRITICAL";
    const isMod = s.risk === "MODERATE";
    
    // Monochrome badges with high contrast for white background
    const badgeBg = isCritical ? "#000000" : (isMod ? "#27272a" : "#f4f4f5");
    const badgeText = isCritical ? "#ffffff" : (isMod ? "#ffffff" : "#09090b");
    const badgeBorder = isCritical ? "#000000" : (isMod ? "#27272a" : "#71717a");
    const attStyle = s.att < 75.0 ? "color: #000000; font-weight: 800; text-decoration: underline;" : "color: #09090b; font-weight: 700;";

    return `
      <tr>
        <td><strong style="color: #000000; font-family: monospace; font-size: 13.5px; font-weight: 800;">${s.id}</strong></td>
        <td><span style="${attStyle}">${s.att.toFixed(1)}%</span></td>
        <td style="color: #09090b; font-weight: 700; font-size: 13px;">${s.ia1.toFixed(1)} / 30</td>
        <td style="color: #09090b; font-weight: 700; font-size: 13px;">${s.ia2.toFixed(1)} / 30</td>
        <td style="color: #000000; font-weight: 700; font-size: 13px;">${((1.0 - s.prob) * 100).toFixed(1)}%</td>
        <td>
          <span style="display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; background: ${badgeBg}; color: ${badgeText}; border: 1px solid ${badgeBorder};">
            ${s.risk} (${(s.prob*100).toFixed(1)}%)
          </span>
        </td>
        <td>
          <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <button class="btn-outline" style="font-size: 11px; font-weight: 600; padding: 5px 10px; color: #000000; border-color: #71717a;" onclick="openGradeModal('${s.id}')">Manual Override</button>
            <button class="btn-black" style="font-size: 11px; font-weight: 600; padding: 5px 10px;" onclick="openInterventionModal('${s.id}')">Advising Notes</button>
            <button class="btn-black" style="font-size: 11px; font-weight: 600; padding: 5px 10px; background: ${s.att < 75 ? '#dc2626' : '#0f172a'}; border-color: ${s.att < 75 ? '#dc2626' : '#0f172a'};" onclick="dispatchStudentAttendanceAlert('${s.id}', ${s.att.toFixed(1)})" title="Dispatch SMTP Attendance Alert">✉️ Notify</button>
          </div>
        </td>
      </tr>
    `;
  }).join("");
}"""

new_render_cohort = """async function renderCohortTable(filterQuery = "") {
  const tbody = document.getElementById("cohort-table-body");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/faculty/cohort/students`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const students = data.cohort || [];

    const q = (filterQuery || "").toLowerCase();
    const filtered = students.filter(s => 
      s.id.toLowerCase().includes(q) || (s.name && s.name.toLowerCase().includes(q)) || (s.risk && s.risk.toLowerCase().includes(q))
    );

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No student records found in database.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(s => {
      const isCritical = s.risk === "HIGH" || s.prob > 0.6;
      const isMod = s.risk === "MEDIUM" || (s.prob >= 0.3 && s.prob <= 0.6);
      
      const badgeBg = isCritical ? "#dc2626" : (isMod ? "#d97706" : "#16a34a");
      const attStyle = s.att < 75.0 ? "color: #dc2626; font-weight: 800; text-decoration: underline;" : "color: #09090b; font-weight: 700;";

      return `
        <tr>
          <td>
            <strong style="color: #000000; font-family: monospace; font-size: 13.5px; font-weight: 800;">${s.id}</strong>
            <div style="font-size: 11px; color: #71717a;">${s.name || 'Enrolled Student'}</div>
          </td>
          <td><span style="${attStyle}">${s.att.toFixed(1)}%</span></td>
          <td style="color: #09090b; font-weight: 700; font-size: 13px;">${s.ia1.toFixed(1)} / 30</td>
          <td style="color: #09090b; font-weight: 700; font-size: 13px;">${s.ia2.toFixed(1)} / 30</td>
          <td style="color: #000000; font-weight: 700; font-size: 13px;">${((1.0 - s.prob) * 100).toFixed(1)}%</td>
          <td>
            <span style="display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; background: ${badgeBg}; color: #ffffff;">
              ${s.risk} (${(s.prob*100).toFixed(1)}%)
            </span>
          </td>
          <td>
            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
              <button class="btn-outline" style="font-size: 11px; font-weight: 600; padding: 5px 10px;" onclick="openGradeModal('${s.id}')">Override</button>
              <button class="btn-black" style="font-size: 11px; font-weight: 600; padding: 5px 10px;" onclick="openInterventionModal('${s.id}')">Advising</button>
              <button class="btn-black" style="font-size: 11px; font-weight: 600; padding: 5px 10px; background: ${s.att < 75 ? '#dc2626' : '#0f172a'}; border-color: ${s.att < 75 ? '#dc2626' : '#0f172a'};" onclick="dispatchStudentAttendanceAlert('${s.id}', ${s.att.toFixed(1)})" title="Dispatch SMTP Attendance Alert">✉️ Alert</button>
            </div>
          </td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    console.warn("Failed to load cohort table from database", err);
  }
}"""

js = js.replace(old_render_cohort, new_render_cohort)

old_render_weak = """function renderWeakTopicsTable() {
  const tbody = document.getElementById("weak-topics-table-body");
  if (!tbody) return;

  tbody.innerHTML = CURRICULUM_CONCEPTS.map(c => `
    <tr>
      <td><span class="badge-tag" style="background: #000000; color: #ffffff; border-color: #000000; font-weight: 700;">${c.id}</span></td>
      <td><strong style="color: #09090b; font-size: 13px;">${c.name}</strong><div style="font-size: 11px; color: #52525b; font-weight: 500;">${c.domain}</div></td>
      <td style="color: #09090b; font-weight: 700; font-size: 13px;">${c.struggling} Students</td>
      <td style="color: #27272a; font-weight: 600;">${c.attempts} Total</td>
      <td><span style="font-weight: 700; color: #000000; font-size: 13px;">${c.failureRate}</span></td>
      <td style="color: #09090b; font-size: 12px; font-weight: 500;">${c.prereq}</td>
      <td><span class="badge-tag" style="background: #ffffff; color: #09090b; border-color: #71717a; font-weight: 600;">${c.remedial}</span></td>
    </tr>
  `).join("");
}"""

new_render_weak = """async function renderWeakTopicsTable() {
  const tbody = document.getElementById("weak-topics-table-body");
  if (!tbody) return;

  try {
    const res = await fetch(`${API_BASE}/api/faculty/courses/AIML-401/class-weak-topics`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const topics = data.class_weakness_distribution || [];

    if (topics.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No diagnostic records found.</td></tr>`;
      return;
    }

    tbody.innerHTML = topics.map(t => `
      <tr>
        <td><span class="badge-tag" style="background: #000000; color: #ffffff; border-color: #000000; font-weight: 700;">${t.topic_id}</span></td>
        <td><strong style="color: #09090b; font-size: 13px;">${t.topic_title}</strong></td>
        <td style="color: #09090b; font-weight: 700; font-size: 13px;">${t.students_struggling} Students</td>
        <td style="color: #27272a; font-weight: 600;">${t.total_students} Total</td>
        <td><span style="font-weight: 700; color: ${t.struggle_rate_pct > 50 ? '#dc2626' : '#09090b'}; font-size: 13px;">${t.struggle_rate_pct.toFixed(1)}%</span></td>
        <td style="color: #09090b; font-size: 12px; font-weight: 500;">Avg Mark: ${t.avg_marks}</td>
        <td><span class="badge-tag" style="background: ${t.priority === 'HIGH' ? '#dc2626' : '#27272a'}; color: #ffffff; font-weight: 600;">${t.priority} PRIORITY</span></td>
      </tr>
    `).join("");
  } catch (err) {
    console.warn("Failed to load class weak topics from database", err);
  }
}"""

js = js.replace(old_render_weak, new_render_weak)

with open(r"js\faculty.js", "w", encoding="utf-8") as f:
    f.write(js)

print("js/faculty.js updated successfully with real authentication & live database records!")

