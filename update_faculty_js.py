with open("js/faculty.js", "r", encoding="utf-8") as f:
    js_code = f.read()

qp_and_batch_js = '''
// =============================================================================
// FLOW 1: UPLOAD IA QUESTION PAPER & SECTION BLUEPRINT
// =============================================================================
function openUploadQPModal() {
  const modal = document.getElementById("upload-qp-modal");
  if (modal) {
    modal.style.display = "flex";
    populateDefaultQPBlueprint();
  }
}

function closeUploadQPModal() {
  const modal = document.getElementById("upload-qp-modal");
  if (modal) modal.style.display = "none";
}

function populateDefaultQPBlueprint() {
  const iaSelect = document.getElementById("qp-ia-number");
  const iaNum = parseInt(iaSelect ? iaSelect.value : "1", 10);
  const titleInput = document.getElementById("qp-title");
  const unitInput = document.getElementById("qp-unit-name");
  const fileInput = document.getElementById("qp-file-name");
  const tbody = document.getElementById("qp-sections-table-body");

  if (iaNum === 1) {
    if (titleInput) titleInput.value = "IA-1 Question Paper & Section Blueprint: Deep Learning";
    if (unitInput) unitInput.value = "Unit 1 & Unit 2: Differential Optimization & Computational Graphs";
    if (fileInput) fileInput.value = "IA1_Question_Paper_AIML401.pdf";
    if (tbody) {
      tbody.innerHTML = `
        <tr style="border-bottom: 1px solid rgba(0,0,0,0.05);">
          <td style="padding: 6px; font-weight: 600;">Question 1 (Sec A)</td>
          <td style="padding: 6px;"><span class="badge badge-gray">MATH_PARTIAL_DERIV</span></td>
          <td style="padding: 6px;">Multivariable Calculus: Partial Derivatives</td>
          <td style="padding: 6px; text-align: right; font-weight: 700;">10.0 pts</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(0,0,0,0.05);">
          <td style="padding: 6px; font-weight: 600;">Question 2 (Sec B)</td>
          <td style="padding: 6px;"><span class="badge badge-gray">MATH_CHAIN_RULE</span></td>
          <td style="padding: 6px;">Multivariate Chain Rule & Graph Propagation</td>
          <td style="padding: 6px; text-align: right; font-weight: 700;">10.0 pts</td>
        </tr>
        <tr>
          <td style="padding: 6px; font-weight: 600;">Question 3 (Sec C)</td>
          <td style="padding: 6px;"><span class="badge badge-gray">DL_BACKPROP</span></td>
          <td style="padding: 6px;">Reverse-Mode Autodiff & Backpropagation</td>
          <td style="padding: 6px; text-align: right; font-weight: 700;">10.0 pts</td>
        </tr>
      `;
    }
  } else {
    if (titleInput) titleInput.value = "IA-2 Question Paper & Section Blueprint: Deep Neural Architectures";
    if (unitInput) unitInput.value = "Unit 3 & Unit 4: CNNs, Sequence Modeling & Optimizers";
    if (fileInput) fileInput.value = "IA2_Question_Paper_AIML401.pdf";
    if (tbody) {
      tbody.innerHTML = `
        <tr style="border-bottom: 1px solid rgba(0,0,0,0.05);">
          <td style="padding: 6px; font-weight: 600;">Question 1 (Sec A)</td>
          <td style="padding: 6px;"><span class="badge badge-gray">DL_CNN_CONV</span></td>
          <td style="padding: 6px;">CNN Spatial Convolutions & Receptive Fields</td>
          <td style="padding: 6px; text-align: right; font-weight: 700;">10.0 pts</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(0,0,0,0.05);">
          <td style="padding: 6px; font-weight: 600;">Question 2 (Sec B)</td>
          <td style="padding: 6px;"><span class="badge badge-gray">DL_RNN_LSTM</span></td>
          <td style="padding: 6px;">Recurrent Networks & LSTM Gating Mechanics</td>
          <td style="padding: 6px; text-align: right; font-weight: 700;">10.0 pts</td>
        </tr>
        <tr>
          <td style="padding: 6px; font-weight: 600;">Question 3 (Sec C)</td>
          <td style="padding: 6px;"><span class="badge badge-gray">DL_OPTIM_ADAM</span></td>
          <td style="padding: 6px;">Optimization Dynamics: SGD, RMSprop & Adam</td>
          <td style="padding: 6px; text-align: right; font-weight: 700;">10.0 pts</td>
        </tr>
      `;
    }
  }
}

async function handleUploadQPSubmit(e) {
  if (e) e.preventDefault();
  const btn = document.getElementById("btn-submit-upload-qp");
  const iaNum = parseInt(document.getElementById("qp-ia-number").value || "1", 10);
  const title = document.getElementById("qp-title").value.trim();
  const unit = document.getElementById("qp-unit-name").value.trim();
  const file = document.getElementById("qp-file-name").value.trim();

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span>Indexing in ChromaDB...</span>`;
  }

  try {
    const payload = {
      ia_number: iaNum,
      title: title,
      unit_name: unit,
      file_name: file,
      faculty_id: activeFacultyId || "FAC_AIML_01"
    };

    const res = await fetch(`${API_BASE}/api/faculty/courses/AIML-401/upload-qp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok && data.status === "success") {
      alert(`Success! IA-${iaNum} Question Paper & Blueprint registered in PostgreSQL and indexed in ChromaDB.\\nMaterial ID: ${data.material_id}\\n\\nNodemailer SMTP notification dispatched to enrolled student email: sumithu.dev@gmail.com.`);
      closeUploadQPModal();
      if (typeof loadFacultyUploadedMaterials === "function") {
        loadFacultyUploadedMaterials();
      }
    } else {
      alert("Failed to upload Question Paper: " + (data.detail || data.message || "Unknown error"));
    }
  } catch (err) {
    alert("Connection error uploading Question Paper: " + err.message);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `Upload Question Paper &amp; Register Blueprint`;
    }
  }
}

// =============================================================================
// FLOW 2: BATCH IA MARKS INGESTION BY SECTION
// =============================================================================
const BATCH_STUDENTS_DEFAULT = [
  { srn: "R24EA895", name: "Sneha Patel", att: 51.0, q1: 4.0, q2: 2.5, q3: 2.5 },
  { srn: "R24EA818", name: "Rohan Verma", att: 64.0, q1: 6.5, q2: 3.0, q3: 3.5 },
  { srn: "R24EA842", name: "Priya Nair", att: 72.0, q1: 8.0, q2: 6.5, q3: 4.5 },
  { srn: "R24EA801", name: "Aarav Sharma", att: 91.0, q1: 9.0, q2: 8.5, q3: 8.5 },
  { srn: "R24EA807", name: "Sumith U", att: 94.5, q1: 9.5, q2: 10.0, q3: 10.0 }
];

function openBatchIAMarksModal() {
  const modal = document.getElementById("batch-ia-marks-modal");
  if (modal) {
    modal.style.display = "flex";
    renderBatchMarksGrid();
  }
}

function closeBatchIAMarksModal() {
  const modal = document.getElementById("batch-ia-marks-modal");
  if (modal) modal.style.display = "none";
}

function renderBatchMarksGrid() {
  const iaNum = parseInt(document.getElementById("batch-ia-num").value || "1", 10);
  const tbody = document.getElementById("batch-ia-table-body");
  const thQ1 = document.getElementById("th-batch-q1");
  const thQ2 = document.getElementById("th-batch-q2");
  const thQ3 = document.getElementById("th-batch-q3");

  if (iaNum === 1) {
    if (thQ1) thQ1.textContent = "Q1: Partial Deriv (/10)";
    if (thQ2) thQ2.textContent = "Q2: Chain Rule (/10)";
    if (thQ3) thQ3.textContent = "Q3: Backpropagation (/10)";
  } else {
    if (thQ1) thQ1.textContent = "Q1: CNN Convolutions (/10)";
    if (thQ2) thQ2.textContent = "Q2: LSTM Mechanics (/10)";
    if (thQ3) thQ3.textContent = "Q3: Adam Optimizer (/10)";
  }

  if (!tbody) return;
  tbody.innerHTML = BATCH_STUDENTS_DEFAULT.map((s, idx) => {
    const total = (s.q1 + s.q2 + s.q3).toFixed(1);
    const riskTier = total < 15.0 || s.att < 75.0 ? (total < 12.0 || s.att < 65.0 ? "HIGH" : "MEDIUM") : "LOW";
    const riskBadge = riskTier === "HIGH" ? `<span class="badge badge-red">HIGH RISK</span>` : (riskTier === "MEDIUM" ? `<span class="badge badge-yellow">MEDIUM</span>` : `<span class="badge badge-green">LOW RISK</span>`);

    return `
      <tr>
        <td style="font-weight: 700; font-family: monospace;">${s.srn}</td>
        <td>${s.name}</td>
        <td>
          <input type="number" step="0.5" min="0" max="10" value="${s.q1}" id="batch-q1-${idx}" class="form-control" style="width: 80px; padding: 4px 8px; font-size: 12.5px;" onchange="updateBatchRowTotal(${idx})">
        </td>
        <td>
          <input type="number" step="0.5" min="0" max="10" value="${s.q2}" id="batch-q2-${idx}" class="form-control" style="width: 80px; padding: 4px 8px; font-size: 12.5px;" onchange="updateBatchRowTotal(${idx})">
        </td>
        <td>
          <input type="number" step="0.5" min="0" max="10" value="${s.q3}" id="batch-q3-${idx}" class="form-control" style="width: 80px; padding: 4px 8px; font-size: 12.5px;" onchange="updateBatchRowTotal(${idx})">
        </td>
        <td style="font-weight: 800; font-size: 13px;" id="batch-total-${idx}">${total} / 30</td>
        <td id="batch-risk-${idx}">${riskBadge}</td>
      </tr>
    `;
  }).join("");
}

function updateBatchRowTotal(idx) {
  const q1 = parseFloat(document.getElementById(`batch-q1-${idx}`).value || 0);
  const q2 = parseFloat(document.getElementById(`batch-q2-${idx}`).value || 0);
  const q3 = parseFloat(document.getElementById(`batch-q3-${idx}`).value || 0);
  const total = (q1 + q2 + q3).toFixed(1);
  const totalEl = document.getElementById(`batch-total-${idx}`);
  if (totalEl) totalEl.textContent = `${total} / 30`;

  const s = BATCH_STUDENTS_DEFAULT[idx];
  const riskTier = total < 15.0 || s.att < 75.0 ? (total < 12.0 || s.att < 65.0 ? "HIGH" : "MEDIUM") : "LOW";
  const riskBadge = riskTier === "HIGH" ? `<span class="badge badge-red">HIGH RISK</span>` : (riskTier === "MEDIUM" ? `<span class="badge badge-yellow">MEDIUM</span>` : `<span class="badge badge-green">LOW RISK</span>`);
  const riskEl = document.getElementById(`batch-risk-${idx}`);
  if (riskEl) riskEl.innerHTML = riskBadge;
}

async function handleBatchIAMarksSubmit(e) {
  if (e) e.preventDefault();
  const btn = document.getElementById("btn-submit-batch-pipeline");
  const iaNum = parseInt(document.getElementById("batch-ia-num").value || "1", 10);
  const telemEl = document.getElementById("batch-pipeline-telemetry");

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<span>Executing 6-Stage Pipeline...</span>`;
  }
  if (telemEl) {
    telemEl.style.display = "block";
    telemEl.textContent = "Stage 1: Connecting to Fluxbase PostgreSQL...\\nStage 2: Validating section scores against [0.0 - 10.0] bounds...";
  }

  try {
    const q1Topic = iaNum === 1 ? { id: "MATH_PARTIAL_DERIV", title: "Multivariable Calculus: Partial Derivatives" } : { id: "DL_CNN_CONV", title: "CNN Spatial Convolutions & Receptive Fields" };
    const q2Topic = iaNum === 1 ? { id: "MATH_CHAIN_RULE", title: "Multivariate Chain Rule & Graph Propagation" } : { id: "DL_RNN_LSTM", title: "Recurrent Networks & LSTM Gating Mechanics" };
    const q3Topic = iaNum === 1 ? { id: "DL_BACKPROP", title: "Reverse-Mode Autodiff & Backpropagation" } : { id: "DL_OPTIM_ADAM", title: "Optimization Dynamics: SGD, RMSprop & Adam" };

    const records = BATCH_STUDENTS_DEFAULT.map((s, idx) => {
      const q1Val = parseFloat(document.getElementById(`batch-q1-${idx}`).value || s.q1);
      const q2Val = parseFloat(document.getElementById(`batch-q2-${idx}`).value || s.q2);
      const q3Val = parseFloat(document.getElementById(`batch-q3-${idx}`).value || s.q3);
      return {
        srn: s.srn,
        attendance_pct: s.att,
        questions: [
          { question_no: "Q1", topic_id: q1Topic.id, topic_title: q1Topic.title, marks_obtained: q1Val, max_marks: 10.0 },
          { question_no: "Q2", topic_id: q2Topic.id, topic_title: q2Topic.title, marks_obtained: q2Val, max_marks: 10.0 },
          { question_no: "Q3", topic_id: q3Topic.id, topic_title: q3Topic.title, marks_obtained: q3Val, max_marks: 10.0 }
        ]
      };
    });

    const payload = {
      course_id: "AIML-401",
      semester: 7,
      ia_number: iaNum,
      faculty_id: activeFacultyId || "FAC_AIML_01",
      records: records
    };

    const res = await fetch(`${API_BASE}/api/pipeline/ingest-ia-marks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      if (telemEl) {
        telemEl.innerHTML = `
[SUCCESS] Pipeline Batch: ${data.batch_id}
[+] Students Processed: ${data.students_processed}
[+] Question Scores Persisted: ${data.questions_persisted}
[+] ML Risk Evaluated (tau=0.42): ${data.at_risk_students_flagged} At-Risk Students Flagged
[+] WeakTopicRAGEngine: ${data.remedial_plans_synthesized} Remedial Study Plans Synthesized in student_study_plans
[+] Faculty Interventions: ${data.mentor_alerts_triggered} Automated Early Warning Directives Raised
[+] Pipeline Latency: ${data.execution_latency_ms} ms
        `.trim();
      }

      setTimeout(() => {
        alert(`Automated Batch Ingestion Complete!\\n\\nPersisted ${data.questions_persisted} section scores for IA-${iaNum}.\\nRecalibrated ML dropout tiers and synthesized personalized remedial study plans.`);
        closeBatchIAMarksModal();
        renderCohortTable();
        loadCohortRiskAnalysis();
        renderWeakTopicsTable(activeAssessmentFilter);
      }, 1500);
    } else {
      alert("Pipeline Error: " + (data.detail || "Failed to execute batch ingestion."));
    }
  } catch (err) {
    alert("Connection Error executing pipeline: " + err.message);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `Execute Automated Ingestion Pipeline`;
    }
  }
}
'''

# Replace runAutomatedBatchPipeline with openBatchIAMarksModal
if "function runAutomatedBatchPipeline" in js_code:
    # Replace runAutomatedBatchPipeline function
    import re
    js_code = re.sub(r'async function runAutomatedBatchPipeline\(\) \{.*?alert\([^)]+\);\s*\}, 1200\);\s*\}', 'function runAutomatedBatchPipeline() { openBatchIAMarksModal(); }', js_code, flags=re.DOTALL)
    print("Replaced runAutomatedBatchPipeline placeholder.")

# Append qp_and_batch_js to js/faculty.js if not already present
if "function openUploadQPModal" not in js_code:
    js_code += "\n" + qp_and_batch_js
    print("Appended openUploadQPModal and batch ingestion logic to faculty.js.")

with open("js/faculty.js", "w", encoding="utf-8") as f:
    f.write(js_code)
print("js/faculty.js updated.")

