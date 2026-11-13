# PACD-RAG: System Architecture & Workflow Specification
## AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
**A Compound AI Framework: Machine Learning + Explainable AI (XAI) + Prerequisite DAG + RAG + Multi-Agent Orchestration**

---

### Meta-Information & Academic Registry
* **Lead Investigator / Student:** Sumith U (SRN: `R24EA807`)
* **Degree & Department:** B.Tech in Computer Science and Engineering (Artificial Intelligence & Machine Learning)
* **Semester & Section:** 7th Semester, Section B
* **Institution:** School of Computing & Information Technology, REVA University, Bengaluru, India
* **Supervisor / Guide:** Department Project Evaluation Committee
* **Implementation Status:** Fully Implemented, Deployed, and Verified (53/53 Automated Tests Passing)

---

## 1. Executive Problem Statement & Compound AI Solution

### 1.1 The Triad of Deficits in Conventional Academic Systems
Modern Higher Educational Institutions (HEIs) rely on Learning Management Systems (e.g., Moodle, Canvas, Blackboard) and enterprise ERPs that exhibit three critical structural flaws:
1. **The Descriptive Trap:** Current portals function as retrospective scorecards. They display historical marks and static bar charts after semester completion, providing zero predictive foresight when interventions could still prevent failure (Susnjak et al., 2022).
2. **The "Coarse-Grained" Assessment Deficit:** Continuous Internal Evaluation (CIE) marks are aggregated into a single coarse scalar (e.g., scoring $24/40$ on Internal Assessment 1). The student and mentor receive no granular visibility into which specific topic, concept, or Course Outcome (CO) caused the mark loss.
3. **The Semester End Exam (SEE) Uncertainty Barrier:** Students enter final examinations without algorithmic guidance on the exact mathematical threshold required to pass, clear backlogs, or achieve a target CGPA given their accumulated CIE marks.

### 1.2 The Compound AI Architectural Solution (PACD-RAG)
To resolve these systemic flaws, this platform transitions academic monitoring from a passive recording system into an **active, cognitive, agentic navigator** through an 8-layer Compound AI architecture:

```mermaid
flowchart TD
    subgraph UI["1. Executive Monochrome Presentation Layer (Port 8000)"]
        UI_F["Faculty Console<br/>(Cohort Trajectories & Privileged CRUD)"]
        UI_S["Student SRL Dashboard<br/>(CIE Ledger & Shortage Alert)"]
        UI_RAG["PACD-RAG Assistant<br/>(Cognitive Prerequisite Flow)"]
    end

    subgraph API["2. Role-Separated REST API Layer (FastAPI Port 8002)"]
        API_STU["/api/student/*<br/>(Profile, Records, Diagnostics, Drills)"]
        API_FAC["/api/faculty/*<br/>(Mentees, Roster, 403 Privilege Check)"]
        API_AUTH["RBAC Allocation Guard<br/>(Advisor & Instructor Verification)"]
    end

    subgraph REASONING["3. Cognitive Diagnosis & Reasoning Engine"]
        DAG["Part 4: Prerequisite Knowledge Graph<br/>(17 Concepts &bull; 21 Edges &bull; NetworkX DAG)"]
        ML["Part 2: Predictive Risk Pipeline<br/>(Calibrated Threshold &tau;=0.42 &bull; 86.10% Acc)"]
        XAI["Part 3: TreeSHAP Attribution<br/>(&sum;&phi;i + &phi;0 = f(x) &bull; DiCE Counterfactuals)"]
    end

    subgraph HYBRID_DB["4. Hybrid Storage & AI Gateway Layer"]
        CHROMA[("ChromaDB Vector Store<br/>Docker Port 8001<br/>all-MiniLM-L6-v2 Embeddings")]
        FLUX_DB[("Fluxbase Cloud PostgreSQL<br/>fluxbasedb.me &bull; Project: 1e6db5b86dd04e11<br/>10 Relational Tables")]
        FLUX_AI["Flux AI Reasoning Gateway<br/>flux-flash &bull; Cloud LLM Completions"]
        MYSQL[("MySQL Relational DB<br/>Docker Port 3307 &bull; smart_campus_db")]
    end

    UI --> API
    API --> API_AUTH
    API_AUTH --> REASONING
    REASONING --> HYBRID_DB
```

---

## 2. End-to-End System Architecture (8 Operational Layers)

### Layer 1: Multi-Modal Ingestion & Anti-Leakage Data Pipeline
* **Corpus Ingested:** UCI Machine Learning Student Performance & Dropout dataset (ID: 697; 4,424 student cohorts, 37 demographic, socio-economic, and academic features).
* **Anti-Leakage Protocol:** An 80/20 stratified split is executed strictly *before* any feature transformation (3,539 Train / 885 Test).
* **Transformation:** A production Scikit-Learn `ColumnTransformer` handles standard scaling for continuous features and one-hot encoding for categorical descriptors, generating a 236-dimensional feature space (`preprocessor.joblib`).
* **Target Isolation:** Binary and 3-class target attributes (`Target_Dropout`, `Target_Graduate`) are completely removed from the feature matrix $X$ prior to fitting to eliminate look-ahead leakage.

### Layer 2: Calibrated Student Risk Modeling Benchmark
* **Benchmarked Architectures:** Evaluated 4 algorithmic paradigms: L2-regularized Logistic Regression, Random Forest, CatBoost, and XGBoost.
* **Production Model:** Calibrated Logistic Regression / CatBoost ensemble achieving:
  $$\text{Accuracy} = 86.10\%, \quad \text{Dropout Recall} = 81.69\%, \quad \text{ROC-AUC} = 0.9133$$
* **Threshold Tuning:** A tuned decision boundary ($\tau = 0.42$) optimizes sensitivity to at-risk indicators, providing a 4.2-week lead time before midterms.

### Layer 3: Explainable AI (TreeSHAP & DiCE Counterfactuals)
* **Local & Global Attributions:** Implements Lundberg's TreeSHAP algorithm to compute signed Shapley values $\phi_i(x)$.
* **Mathematical Axiom Compliance:** Every individual prediction strictly adheres to the Efficiency and Additivity Axiom:
  $$\sum_{i=1}^{M} \phi_i(x) + \phi_0 = f(x)$$
* **DiCE Counterfactual Engine:** Formulates minimal-distance optimization problems to compute feasible interventions:
  $$c^* = \arg\min_{c} \text{dist}(x, c) + \lambda \left( f(c) - y^* \right)^2$$
  *Example Output:* "Increasing weekly VLE self-study hours from 2.5h to 6.2h shifts student risk from High ($78\%$) to Safe ($32\%$)".

### Layer 4: Curriculum Prerequisite Knowledge Graph & Deficit Tracing
* **Graph Topology:** Ingests 17 foundational curriculum concepts across Mathematics, Optimization, and Machine Learning, connected by 21 directed prerequisite edges into a NetworkX DiGraph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$.
* **DAG Integrity:** Cycle detection proves $0$ directed cycles; topological sorting establishes the cognitive learning hierarchy.
* **Canonical Verified Pathway:**
  $$\text{Partial Derivatives} \longrightarrow \text{Chain Rule} \longrightarrow \text{Backpropagation} \longrightarrow \text{Neural Network Training}$$
* **Cognitive Deficit Isolation:** Formative assessment quiz scores are mapped to target concepts. Scores below mastery threshold ($\tau = 0.60$) trigger backward traversal through ancestral closures:
  $$\text{Ancestors}(v) = \{ u \in \mathcal{V} \mid u \rightsquigarrow v \}$$
  This isolates the exact foundational prerequisite deficit causing the assessment failure.

### Layer 5: Hybrid Vector & Cloud Relational Infrastructure
* **Dense Vector Embeddings (Local Docker ChromaDB - Port 8001):**
  - Runs inside Docker container `rio_chromadb` with persistent storage volume `rio_chroma_data`.
  - Partitioned into 3 academic collections: `syllabus_collection`, `lecture_notes_collection`, and `question_bank_collection`.
  - Embeddings generated via ONNX-accelerated `all-MiniLM-L6-v2` ($384$ dense dimensions).
* **Cloud Relational Database (Fluxbase AWS PostgreSQL):**
  - Connected to `https://fluxbasedb.me` using Project ID `1e6db5b86dd04e11`.
  - Maintains 10 university-grade relational schema tables.
* **Cloud AI Reasoning Gateway:**
  - Directly routes cognitive reasoning requests to `flux-flash` via `https://fluxbasedb.me/api/v1/chat/completions`.

### Layer 6: Subject-Scoped Intelligent PACD-RAG Engine
* **Subject Partitioning:** Every document chunk and query is strictly partitioned by `course_id` (e.g. `AIML-401`, `AIML-402`). Vector retrieval queries are constrained by metadata filters (`where={"course_id": course_id}`).
* **Dual-Stage Prerequisite Retrieval:**
  1. *Stage 1 (Graph Expansion):* The student's query is resolved against the Part 4 DAG to identify the target concept and its immediate prerequisite ancestors.
  2. *Stage 2 (Hybrid Semantic Search):* The prerequisite definitions are injected into ChromaDB vector retrieval, ensuring the returned context includes both foundational math and advanced slide excerpts.
  3. *Stage 3 (Scaffolded Generation):* Flux AI synthesizes pedagogical explanations adhering strictly to university syllabus boundaries.

### Layer 7: Role-Separated REST API Server with Privileged Security (FastAPI)
* Running on port `8002` (Swagger UI at `/docs`):
  - **Student Router (`/api/student/*`):** Profile, standing, enrolled courses, Continuous Internal Evaluation (CIE) marks breakdown, diagnostic deficit tracing, subject RAG queries, and adaptive drills.
  - **Faculty Router (`/api/faculty/*`):** Mentee rosters, cohort at-risk monitoring, course blueprints, material uploads, and privileged grade updates.
  - **Role-Based Access Control (RBAC):** Privileged grade and attendance updates (`POST /api/faculty/{faculty_id}/grades/update`) strictly enforce:
    $$\text{Authorized} \iff \text{faculty\_id} == \text{assigned\_advisor\_id} \quad \lor \quad \text{faculty\_id} == \text{instructor\_faculty\_id}$$
    Unauthorized faculty requests receive an immediate **HTTP 403 Forbidden**.
  - **Automated Early-Warning Trigger:**
    $$\text{Attendance} < 75.0\% \quad \lor \quad \text{Grade} \in \{\text{'D'}, \text{'F'}\} \implies \text{risk\_level} = \text{'HIGH'}, \; \text{dropout\_probability} = 0.78$$

### Layer 8: Executive Monochrome Presentation Dashboard
* Served locally on port `8000` (`http://localhost:8000/index.html`).
* Strict minimalist monochrome design system: Pure White background (`#FFFFFF`), solid black buttons (`#000000`), and soft grey cards (`#F3F4F6`). Zero unauthorized accent colors.
* Features active faculty switching, interactive CIE marks and attendance tables with `SHORTAGE (< 75%)` badges, DiCE "What-If" sliders, and the Subject RAG Copilot.

---

## 3. Core System Workflows

### Workflow A: Cognitive Deficit Diagnosis & Adaptive Remediation
Demonstrates how a student's formative quiz failure triggers cognitive diagnosis, prerequisite graph traversal, and RAG-grounded remediation:

```mermaid
sequenceDiagram
    autonumber
    actor Student
    participant UI as Student SRL Dashboard (Port 8000)
    participant API as FastAPI Server (Port 8002)
    participant PKG as Prerequisite DAG (Part 4)
    participant Chroma as Docker ChromaDB (Port 8001)
    participant FluxAI as Flux AI Gateway (fluxbasedb.me)

    Student->>UI: Submits Formative Quiz for AIML-401
    UI->>API: POST /api/student/{srn}/courses/AIML-401/submit-drill
    API->>PKG: Map question to Concept (DL_BACKPROP) & Score (0.40)
    PKG->>PKG: Check threshold &tau;=0.60 &rarr; Deficit Detected!
    PKG->>PKG: Compute Ancestral Closure: Partial Derivatives &rarr; Chain Rule
    PKG-->>API: Return Root-Cause Gap: MATH_CHAIN_RULE
    API->>Chroma: Query chunks for MATH_CHAIN_RULE + DL_BACKPROP (course_id=AIML-401)
    Chroma-->>API: Top-3 Grounded Slide Chunks
    API->>FluxAI: Generate Scaffolded Remediation with Prerequisite Chain
    FluxAI-->>API: Pedagogical Explanation + Remedial Question
    API-->>UI: Return Diagnostic JSON
    UI->>Student: Display Prerequisite Flowchart + Scaffolded Lesson + Drill
```

---

### Workflow B: Privileged Grade & Attendance CRUD with RBAC Security
Illustrates institutional security enforcement when faculty members record marks or attendance:

```mermaid
sequenceDiagram
    autonumber
    actor Faculty as Acting Faculty
    participant UI as Faculty Console (Port 8000)
    participant API as FastAPI REST Server (Port 8002)
    participant FluxDB as Fluxbase AWS DB (fluxbasedb.me)

    Faculty->>UI: Selects Student (R24EA807) & Clicks "Marks & Attd"
    UI->>UI: Opens Grade & Attendance Modal
    Faculty->>UI: Enters IA-1 (20), IA-2 (20), Attendance (58.5%) & Clicks Commit
    UI->>API: POST /api/faculty/{faculty_id}/grades/update
    
    API->>FluxDB: SELECT assigned_advisor_id, instructor_faculty_id
    FluxDB-->>API: Return Allocations (Advisor: FAC_AIML_01, Instructor: FAC_AIML_01)
    
    alt Acting Faculty is Unallocated (e.g. FAC_AIML_02)
        API-->>UI: HTTP 403 Forbidden ("Access Denied: Unallocated Faculty")
        UI->>Faculty: Displays High-Contrast Monochrome Security Alert Box
    else Acting Faculty is Authorized (FAC_AIML_01)
        API->>FluxDB: UPSERT course_enrollments (ia1, ia2, attd, overall_grade='F')
        API->>API: Check Early Warning Rule: Attendance 58.5% < 75%
        API->>FluxDB: UPDATE students SET risk_level='HIGH', dropout_probability=0.78
        API-->>UI: HTTP 200 OK (Record Committed & Synced)
        UI->>UI: Re-render Roster Table & Trigger Risk Escalation Alert
    end
```

---

### Workflow C: Subject-Scoped Material Ingestion & Partitioned RAG Search
Demonstrates how course documents are uploaded, chunked, indexed, and retrieved without cross-subject contamination:

```mermaid
flowchart TD
    subgraph Ingestion["Faculty Course Material Ingestion"]
        DOC["Course Document<br/>(PDF Syllabus, PPTX Slides, DOCX Notes)"]
        META["Subject Scope: course_id = 'AIML-401'<br/>Category: 'lecture_notes'"]
        CHUNK["Recursive Character Text Splitter<br/>Chunk Size: 500 &bull; Overlap: 50"]
        EMBED["ONNX all-MiniLM-L6-v2<br/>Dense Embedding Vector (384-d)"]
        DOC --> META --> CHUNK --> EMBED
    end

    subgraph Storage["Partitioned Dual Persistence"]
        EMBED -->|Vector + course_id metadata| CHROMA_STORE[("ChromaDB Collection<br/>course_learning_materials")]
        META -->|Master Record Metadata| FLUX_MAT[("Fluxbase Table<br/>learning_materials")]
    end

    subgraph Retrieval["Prerequisite-Aware Query Flow"]
        STU_Q["Student Query: 'Explain Backpropagation Through Time'"]
        RESOLVE["Part 4 DAG Concept Resolution<br/>Identified: DL_BACKPROP &bull; Ancestor: MATH_CHAIN_RULE"]
        FILTER["ChromaDB Scoped Vector Query<br/>where={'course_id': 'AIML-401'} &bull; top_k=3"]
        SYNTH["Flux AI Pedagogical Reasoning<br/>flux-flash Cloud Gateway"]
        RESP["Student Output:<br/>Prerequisite DAG Chain + Grounded Explanation + Citations"]

        STU_Q --> RESOLVE --> FILTER
        CHROMA_STORE -.->|Cosine Distance Similarity| FILTER
        FILTER --> SYNTH --> RESP
    end
```

---

## 4. University Relational Database Schema (Fluxbase AWS PostgreSQL)

The platform operates on a 10-table schema deployed on Fluxbase AWS PostgreSQL:

```mermaid
erDiagram
    DEPARTMENTS ||--o{ FACULTY : employs
    DEPARTMENTS ||--o{ COURSES : offers
    FACULTY ||--o{ COURSES : instructs
    FACULTY ||--o{ STUDENTS : advises
    STUDENTS ||--o{ COURSE_ENROLLMENTS : enrolls
    COURSES ||--o{ COURSE_ENROLLMENTS : contains
    COURSES ||--o{ CURRICULUM_CONCEPTS : defines
    CURRICULUM_CONCEPTS ||--o{ CONCEPT_PREREQUISITES : depends_on
    COURSES ||--o{ LEARNING_MATERIALS : provides
    STUDENTS ||--o{ STUDENT_ASSESSMENT_RECORDS : completes
    CURRICULUM_CONCEPTS ||--o{ STUDENT_ASSESSMENT_RECORDS : evaluated_by
    STUDENTS ||--o{ FACULTY_INTERVENTIONS : receives
    FACULTY ||--o{ FACULTY_INTERVENTIONS : logs

    DEPARTMENTS {
        string department_id PK
        string department_name
        string school_name
        string building_location
    }

    FACULTY {
        string faculty_id PK
        string department_id FK
        string name
        string email
        string designation
        string specialization
    }

    COURSES {
        string course_id PK
        string department_id FK
        string instructor_faculty_id FK
        string course_title
        int credits
        int semester
    }

    STUDENTS {
        string srn PK
        string department_id FK
        string assigned_advisor_id FK
        string student_name
        string email
        int semester
        string section
        string risk_level
        float dropout_probability
        float attendance_rate
    }

    COURSE_ENROLLMENTS {
        int enrollment_id PK
        string srn FK
        string course_id FK
        int semester
        float ia1_score
        float ia2_score
        float assignment_score
        float exam_score
        float attendance_pct
        string overall_grade
    }

    CURRICULUM_CONCEPTS {
        string concept_id PK
        string course_id FK
        string concept_name
        int unit_number
        string bloom_taxonomy_level
    }

    CONCEPT_PREREQUISITES {
        int prerequisite_id PK
        string concept_id FK
        string prerequisite_concept_id FK
        string relationship_type
    }

    LEARNING_MATERIALS {
        string material_id PK
        string course_id FK
        string title
        string category
        string chroma_collection_name
    }

    STUDENT_ASSESSMENT_RECORDS {
        int assessment_id PK
        string srn FK
        string concept_id FK
        float score_obtained
        boolean is_concept_mastered
    }

    FACULTY_INTERVENTIONS {
        int intervention_id PK
        string srn FK
        string faculty_id FK
        string intervention_type
        string action_notes
        string follow_up_status
    }
```

---

## 5. Verification Matrix (53/53 Automated Tests Passing)

| Test Suite File | Component Validated | Tests | Status | Key Metrics Verified |
| :--- | :--- | :---: | :---: | :--- |
| [`run_step1_tests.py`](file:///c:/Users/sumit/Downloads/rio/student_success_platform/run_step1_tests.py) | UCI Dataset Ingestion & Anti-Leakage Split | 7 / 7 | **PASS** | 4,424 records, zero nulls, 80/20 stratified partition, 236 transformed dimensions |
| [`run_part2_tests.py`](file:///c:/Users/sumit/Downloads/rio/student_success_platform/run_part2_tests.py) | Risk Modeling Benchmark & Calibration | 6 / 6 | **PASS** | Accuracy: 86.10%, Recall: 81.69%, ROC-AUC: 0.9133, Threshold: $\tau = 0.42$ |
| [`run_part3_tests.py`](file:///c:/Users/sumit/Downloads/rio/student_success_platform/run_part3_tests.py) | TreeSHAP Explainability & Axioms | 5 / 5 | **PASS** | Exact Shapley values, Efficiency Axiom $\sum \phi_i + \phi_0 = f(x)$ verified |
| [`run_part4_tests.py`](file:///c:/Users/sumit/Downloads/rio/student_success_platform/run_part4_tests.py) | Prerequisite Knowledge Graph & Deficits | 8 / 8 | **PASS** | 17 concepts, 21 edges, 0 cycles, topological sort, deficit threshold $\tau = 0.60$ |
| [`run_db_tests.py`](file:///c:/Users/sumit/Downloads/rio/student_success_platform/run_db_tests.py) | Docker ChromaDB & Fluxbase AWS DB + AI | 14 / 14 | **PASS** | Local ChromaDB port 8001, Fluxbase AWS schema, Cloud LLM completions on `flux-flash` |
| [`test_api_endpoints.py`](file:///c:/Users/sumit/Downloads/rio/student_success_platform/tests/test_api_endpoints.py) | Role-Separated REST API & RBAC Security | 13 / 13 | **PASS** | 13 endpoints, HTTP 403 Forbidden enforcement on unallocated faculty, 200 OK sync |
| **TOTAL** | **Full Platform End-to-End Verification** | **53 / 53** | **100%** | **All Layers Tested, Operational, and Synchronized** |

---

## 6. Execution Command Summary

To execute and verify all running services locally:

```powershell
# 1. Start Local Web Frontend Server (Port 8000)
python -m http.server 8000 --directory c:\Users\sumit\Downloads\rio

# 2. Start FastAPI REST API Server (Port 8002)
$env:PYTHONPATH="."; python student_success_platform/src/api_server.py

# 3. Verify Local Docker ChromaDB Vector Store (Port 8001)
docker ps --filter "name=rio_chromadb"

# 4. Run All 53 Automated Tests
python student_success_platform/run_step1_tests.py
python student_success_platform/run_part2_tests.py
python student_success_platform/run_part3_tests.py
python student_success_platform/run_part4_tests.py
python student_success_platform/run_db_tests.py
python -m unittest student_success_platform/tests/test_api_endpoints.py
```
