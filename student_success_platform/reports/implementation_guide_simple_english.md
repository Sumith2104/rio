# PACD-RAG: Complete Project Implementation & Tools Guide
## Written in Simple Indian English for Project Review & Viva Preparation
**Lead Investigator:** Sumith U (SRN: `R24EA807`)  
**Department:** B.Tech in CSE (AI & ML), 7th Semester, Section B  
**Institution:** School of Computing & Information Technology, REVA University, Bengaluru  
**Status:** Fully Implemented & Tested (53/53 Unit Tests Passing - 100%)

---

### 1. What Is This Project in Simple Words? (The Big Picture)

In our colleges, the current student portal or LMS (like Moodle, Canvas, or SLCM) only shows marks and attendance **after** exams are already over.
* If a student gets $24/40$ in Internal Assessment 1 (IA-1), nobody tells them *which specific chapter or topic they were weak in*.
* If attendance drops below $75\%$, students only find out at the end when their hall tickets are blocked. By then, it is already too late to improve.

To solve this, we built **PACD-RAG**. It is an intelligent smart campus system that does 5 things automatically:
1. **Predicts Failure 4 to 6 Weeks Early:** Uses Machine Learning to identify struggling students before midterms happen.
2. **Explains the Exact Reasons (XAI):** Uses TreeSHAP to show a signed breakdown of why a student is at risk (e.g., $+38\%$ risk from attendance shortage, $-18\%$ protection from good lab marks).
3. **Finds the Foundational Concept Gap:** Uses a Prerequisite Knowledge Graph to see if the student failed because they missed an earlier basic topic (like failing Backpropagation because of weak Chain Rule).
4. **Subject-Locked AI Assistant (RAG):** Allows students to ask doubts strictly from their own subject's syllabus and lecture slides using local Docker ChromaDB vector search and cloud AI.
5. **College Mark & Attendance Entry with Privilege Security:** Students can check their IA-1, IA-2, assignment, and attendance marks with shortage alerts. Only the allocated mentor or subject teacher can add/change marks; unauthorized teachers get an immediate **HTTP 403 Forbidden** security block.

---

### 2. Step-by-Step Implementation Breakdown (What We Did)

#### Step 1: Data Preparation & Anti-Leakage Split (Part 1)
* **What We Did:** Ingested 4,424 student records from the standard UCI Educational dataset (37 columns). Cleaned missing values and duplicates.
* **Anti-Leakage Rule:** Executed an 80/20 stratified train/test split (3,539 Train / 885 Test) **before** applying any transformers. Completely removed the Target column (Dropout/Graduate) from the feature matrix so future exam outcomes do not leak into model training.
* **Tools & Libraries:** Python, `pandas`, `numpy`, `scikit-learn` (`ColumnTransformer`, `StandardScaler`, `OneHotEncoder`), `joblib`.
* **Verification:** `python student_success_platform/run_step1_tests.py` (7/7 tests passed).

#### Step 2: Student Risk Prediction Model (Part 2)
* **What We Did:** Benchmarked 4 machine learning algorithms: Logistic Regression, Random Forest, CatBoost, and XGBoost.
* **Production Model:** Calibrated Logistic Regression / CatBoost ensemble achieving **86.10% accuracy**, **81.69% dropout recall**, and a **0.9133 ROC-AUC score**.
* **Threshold Calibration:** Tuned the decision boundary to $\tau = 0.42$ to maximize sensitivity to at-risk students 4.2 weeks before midterms.
* **Tools & Libraries:** `scikit-learn`, `catboost`, `xgboost`, `matplotlib`, `seaborn`.
* **Verification:** `python student_success_platform/run_part2_tests.py` (6/6 tests passed).

#### Step 3: Explainable AI with TreeSHAP & DiCE Counterfactuals (Part 3)
* **What We Did:** Implemented TreeSHAP to compute signed feature attributions $\phi_i$ for every student prediction.
* **Math Axiom Proved:** Verified the Shapley Additivity rule: $\sum \phi_i + \phi_0 = f(x)$ (all individual feature contributions plus baseline equal the final prediction).
* **DiCE Counterfactuals:** Generated actionable "what-if" guidance (e.g., "Increasing weekly VLE study from 2.5h to 6.2h reduces failure probability from 78% to 32%").
* **Tools & Libraries:** `shap`, `dice-ml`, `matplotlib`.
* **Verification:** `python student_success_platform/run_part3_tests.py` (5/5 tests passed).

#### Step 4: Curriculum Prerequisite Knowledge Graph & Deficit Tracing (Part 4)
* **What We Did:** Built a curriculum map of 17 computer science and math concepts with 21 directed prerequisite connections in `concept_prerequisites.json`.
* **DAG Proof:** Validated that the graph has 0 cycles using NetworkX (strictly valid Directed Acyclic Graph). Verified canonical pathway: `Partial Derivatives` $\to$ `Chain Rule` $\to$ `Backpropagation` $\to$ `Neural Network Training`.
* **Cognitive Deficit Isolation:** When a student scores below mastery threshold ($\tau = 0.60$) on a quiz, code traces backwards through ancestral closures to pinpoint the root-cause foundational weakness.
* **Tools & Libraries:** `networkx`, `json`, Python collections.
* **Verification:** `python student_success_platform/run_part4_tests.py` (8/8 tests passed).

#### Step 5: Database Setup - Local Docker & Cloud PostgreSQL
* **Local Docker ChromaDB (Port 8001):** Runs `rio_chromadb` with 3 collections (`syllabus_collection`, `lecture_notes_collection`, `question_bank_collection`) with ONNX `all-MiniLM-L6-v2` embeddings.
* **Local MySQL (Port 3307):** Runs `rio_mysql` container for local structured relational data.
* **Cloud Database (`fluxbasedb.me`):** Connected to AWS PostgreSQL using API key and Project ID `1e6db5b86dd04e11`. Deployed a 10-table schema covering departments, faculty, courses, students, enrollments, marks, concepts, prerequisites, materials, and advising interventions.
* **Tools & Libraries:** `docker`, `docker-compose`, `chromadb`, `pymysql`, `requests`.
* **Verification:** `python student_success_platform/run_db_tests.py` (14/14 tests passed).

#### Step 6: Cloud AI Reasoning Model Integration
* **What We Did:** Integrated cloud AI models (`flux-flash` and `flux`) via `https://fluxbasedb.me/api/v1/chat/completions`.
* **Role:** Synthesizes clear, textbook-grounded pedagogical guidance and generates dynamic adaptive MCQs for weak concepts without hallucination.
* **Tools & Libraries:** `requests`, OpenAI-compatible JSON payload, Flux AI Gateway.
* **Verification:** Tested via `test_flux_ai.py` (passed).

#### Step 7: Subject-Scoped Intelligent PACD-RAG Engine
* **What We Did:** Built `subject_rag_engine.py`. When a student asks a doubt, vector retrieval is strictly locked to that subject (`course_id = 'AIML-401'`).
* **Dual-Stage Retrieval:** Checks the Part 4 DAG first to find prerequisite ancestor concepts, fetches top lecture slide chunks from ChromaDB, and uses Flux AI to generate a grounded explanation.
* **Tools & Libraries:** `chromadb`, ONNX MiniLM, `flux-flash`, Python.
* **Verification:** `test_api_endpoints.py` (passed).

#### Step 8: FastAPI REST Server with Role-Based Security
* **What We Did:** Built 13 REST API endpoints on port `8002`. Kept separate paths: `/api/student/*` for students and `/api/faculty/*` for teachers.
* **Privilege Security:** In `POST /api/faculty/{faculty_id}/grades/update`, only the assigned advisor or course instructor can edit marks or attendance. Unallocated teachers receive **HTTP 403 Forbidden**.
* **Automated Early Warning:** If attendance is $< 75\%$ or grade is D/F, backend automatically escalates student status to `risk_level: HIGH` and `dropout_probability: 0.78` in the database.
* **Tools & Libraries:** `fastapi`, `uvicorn`, `pydantic`.
* **Verification:** `python -m unittest student_success_platform/tests/test_api_endpoints.py` (13/13 tests passed).

#### Step 9: Minimalist Monochrome Web Dashboard
* **What We Did:** Built a responsive single-page web app on port `8000` using strictly White (`#FFFFFF`) background, Black (`#000000`) buttons, and Grey (`#F3F4F6`) cards (zero colors).
* **Features:** Faculty Console with teacher switcher and marks entry modal; Student SRL View with Continuous Internal Evaluation (CIE) ledger table (IA1, IA2, assignment, exam, grade, attendance %, shortage alerts), and interactive PACD-RAG Copilot.
* **Tools & Libraries:** HTML5, CSS3, Vanilla JavaScript, Chart.js, Fetch API.
* **Verification:** Running live on `http://localhost:8000/index.html`.

---

### 3. Master Summary of All Tools, Frameworks & Libraries Used

| Category | Tool / Library Name | Source / Version | Exact Role in Our Smart Campus Platform |
| :--- | :--- | :--- | :--- |
| **Data Science** | `pandas` & `numpy` | Python 3.12 | Loading datasets, handling data frames, matrix calculations, array manipulation. |
| **Machine Learning** | `scikit-learn` | v1.4+ | Preprocessing (`ColumnTransformer`), Logistic Regression, stratified train/test split, metrics. |
| **Machine Learning** | `catboost` & `xgboost` | Official PyPI | Gradient boosting tree algorithms benchmarked for early student attrition prediction. |
| **Explainable AI** | `shap` (TreeSHAP) | PyPI | Computes exact signed Shapley feature values explaining why a student is at risk. |
| **Explainable AI** | `dice-ml` | PyPI | Generates counterfactual "what-if" recommendations for students to reduce risk. |
| **Knowledge Graph** | `networkx` | v3.x | Builds Curriculum Directed Acyclic Graph (DAG), validates 0 cycles, traces ancestor deficits. |
| **Vector Database** | `chromadb` | Docker Port 8001 | Stores dense vector embeddings of syllabus, lecture notes, and question bank. |
| **Dense Embeddings** | `all-MiniLM-L6-v2` | ONNX Engine | Converts text into 384-dimensional dense semantic vectors with fast CPU inference. |
| **Local Relational DB**| `MySQL 8.0` | Docker Port 3307 | Runs `smart_campus_db` container for structured local relational data. |
| **Cloud Database** | `Fluxbase PostgreSQL`| `fluxbasedb.me` | Stores 10 university schema tables (faculty, students, enrollments, marks, advising logs). |
| **Cloud AI Gateway** | `Flux AI (flux-flash)`| `fluxbasedb.me` | Cloud LLM used to generate student learning guidance and dynamic practice MCQs. |
| **Backend Framework** | `fastapi` & `uvicorn` | ASGI Server | High-speed REST API server running on port 8002 with 13 role-separated endpoints. |
| **Data Validation** | `pydantic` | v2.x | Validates request body schemas for grade updates, RAG queries, and user logins. |
| **Frontend Stack** | `HTML5 + CSS3 + JS` | Native / Vanilla | Executive monochrome UI (White/Black/Grey), modal dialogs, and responsive layout. |
| **Data Visualization**| `chart.js` | CDN v4.x | Renders week-wise risk trajectories, SAL&EC matrices, and radar skill charts. |
| **PDF Generation** | `reportlab` | v5.0 | Compiles publication-grade technical specifications and PDF summary reports. |
| **Unit Testing** | Python `unittest` | Built-in | Executes all 53 automated tests covering data, ML, XAI, DAG, databases, and APIs. |

---

### 4. How to Run and Demo Everything (Commands for Viva / Review)

To demo your working project to your guide or external examiner, run these in PowerShell:
```powershell
# 1. Open Web Frontend Dashboard in Browser (Port 8000)
python -m http.server 8000 --directory c:\Users\sumit\Downloads\rio
# Open in browser: http://localhost:8000/index.html

# 2. Start FastAPI REST Backend Server (Port 8002)
$env:PYTHONPATH="."; python student_success_platform/src/api_server.py
# Open Swagger documentation: http://localhost:8002/docs

# 3. Run All 53 Automated Tests (100% Passing Proof)
python student_success_platform/run_step1_tests.py                 # Part 1: 7/7 Pass
python student_success_platform/run_part2_tests.py                 # Part 2: 6/6 Pass
python student_success_platform/run_part3_tests.py                 # Part 3: 5/5 Pass
python student_success_platform/run_part4_tests.py                 # Part 4: 8/8 Pass
python student_success_platform/run_db_tests.py                    # Databases & AI: 14/14 Pass
python -m unittest student_success_platform/tests/test_api_endpoints.py # REST APIs: 13/13 Pass
```

---

### 5. Ready Viva Questions & Simple Indian English Answers

* **Q1: What is the main innovation over standard LMS like Moodle or SLCM?**  
  *Answer:* Standard college LMS only shows marks after students have already written exams. Our PACD-RAG platform predicts failure 4 to 6 weeks early, explains the exact reason using TreeSHAP, traces foundational concept gaps using a Prerequisite Knowledge Graph, and gives targeted help using Subject-Scoped RAG.

* **Q2: What is Data Leakage and how did you prevent it in Part 1?**  
  *Answer:* Data leakage happens when information from the test set or final exam leaks into model training. We prevented this by doing an 80/20 stratified split FIRST, completely removing the Target column before scaling, and fitting our Scikit-Learn `ColumnTransformer` strictly on the training set.

* **Q3: Why did you use both ChromaDB in Docker and Fluxbase in the Cloud?**  
  *Answer:* This is a hybrid architecture. Heavy vector embeddings of lecture notes and syllabi need fast local search with zero cloud cost, so we run ChromaDB in Docker on port 8001. Relational data like student names, IA marks, attendance, and faculty mentorship logs need real database ACID rules and remote access, which our AWS PostgreSQL database on `fluxbasedb.me` provides.

* **Q4: How does your Role-Based Security work for faculty mark entry?**  
  *Answer:* When a teacher tries to update marks or attendance, our FastAPI server checks if the faculty is either the student's assigned mentor or the subject instructor in the database. If an unallocated teacher tries to edit marks, the server immediately rejects the request with **HTTP 403 Forbidden**. This ensures complete academic security.

* **Q5: How does Subject-Scoped RAG prevent hallucinations?**  
  *Answer:* Many AI chatbots mix up different subjects. In our system, every document chunk and vector query is strictly locked with `course_id` (like `AIML-401`). When a student asks a doubt, ChromaDB only retrieves slides from that specific subject, and our Cloud AI (`flux-flash`) answers strictly using those lecture notes.

* **Q6: What is a Prerequisite Knowledge Graph (DAG) and why is it useful?**  
  *Answer:* In engineering, topics build on top of each other. You cannot understand Backpropagation without knowing the Chain Rule, and you cannot understand the Chain Rule without Partial Derivatives. Our NetworkX DAG maps these 17 concepts with 0 cycles. When a student fails a quiz, it walks backwards up the graph to find their real weakness.

* **Q7: How does this platform support NBA / NAAC accreditation and Outcome-Based Education (OBE)?**  
  *Answer:* Accreditation bodies require proof of continuous Course Outcome (CO) attainment and remedial actions for weak students. Our platform provides automated logging of faculty counseling interventions, attendance shortage warnings, and individualized student improvement tracking throughout the semester.

* **Q8: What happens when a student's attendance drops below 75%?**  
  *Answer:* In our university regulations, 75% attendance is compulsory for writing Semester End Exams (SEE). In our platform, the moment faculty enters attendance below 75%, the student is automatically flagged with a black **SHORTAGE (< 75%)** warning badge, and their risk status in the database is automatically escalated to **HIGH RISK**.

