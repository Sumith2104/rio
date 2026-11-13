# Student Feature Documentation & Temporal Leakage Audit

**Project:** AI-Powered Agentic Smart Campus Intelligence & Student Success Platform  
**Author:** Sumith U (SRN: R24EA807) | REVA University  
**Dataset:** Predict Students' Dropout and Academic Success (UCI Repository ID: 697)  
**Standard:** Part 1 Student Data Workflow Specification  

---

## 1. Feature Availability & Temporal Classification Matrix

To prevent **temporal data leakage** (using future information to predict an earlier state), every feature is classified by its real-world availability timeline:

| Feature Name | Type | Description | Available at Admission? | Available after Sem 1? | Temporal Leakage Risk if Predicting Early |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `Marital Status` | Categorical | Legal marital status of student | **Yes** | **Yes** | None (Pre-existing demographic) |
| `Application mode` | Categorical | Method of application (general contest, special, etc.) | **Yes** | **Yes** | None (Admission metadata) |
| `Application order` | Numerical | Choice preference (1st choice, 2nd choice, etc.) | **Yes** | **Yes** | None (Admission metadata) |
| `Course` | Categorical | Degree program enrolled in | **Yes** | **Yes** | None (Admission metadata) |
| `Daytime/evening attendance` | Binary | Day shift (1) or evening shift (0) | **Yes** | **Yes** | None (Admission metadata) |
| `Previous qualification` | Categorical | Prior secondary school degree | **Yes** | **Yes** | None (Prior academic record) |
| `Previous qualification (grade)` | Numerical | High school grade (0–200 scale) | **Yes** | **Yes** | None (Prior academic record) |
| `Nacionality` | Categorical | Country of origin | **Yes** | **Yes** | None (Demographic) |
| `Mother's qualification` | Categorical | Highest educational level of mother | **Yes** | **Yes** | None (Socioeconomic context) |
| `Father's qualification` | Categorical | Highest educational level of father | **Yes** | **Yes** | None (Socioeconomic context) |
| `Mother's occupation` | Categorical | Employment sector of mother | **Yes** | **Yes** | None (Socioeconomic context) |
| `Father's occupation` | Categorical | Employment sector of father | **Yes** | **Yes** | None (Socioeconomic context) |
| `Admission grade` | Numerical | Standardized entrance score (0–200 scale) | **Yes** | **Yes** | None (Admission examination) |
| `Displaced` | Binary | Relocated from home to attend university | **Yes** | **Yes** | None (Demographic) |
| `Educational special needs` | Binary | Registered disability or accommodation | **Yes** | **Yes** | None (Institutional support) |
| `Debtor` | Binary | Outstanding financial balance at enrollment | **Yes** | **Yes** | None (Financial registration) |
| `Tuition fees up to date` | Binary | Semester fee payments verified | **Yes** | **Yes** | None (Financial registration) |
| `Gender` | Binary | Gender identity (1=Male, 0=Female) | **Yes** | **Yes** | None (Demographic) |
| `Scholarship holder` | Binary | Awarded financial grant / scholarship | **Yes** | **Yes** | None (Financial aid status) |
| `Age at enrollment` | Numerical | Student age at matriculation (years) | **Yes** | **Yes** | None (Demographic) |
| `International` | Binary | Foreign national status | **Yes** | **Yes** | None (Demographic) |
| `Curricular units 1st sem (credited)` | Numerical | Approved transferred course units | No | **Yes** | Low (Available at end of Sem 1) |
| `Curricular units 1st sem (enrolled)` | Numerical | Number of units enrolled in Sem 1 | No | **Yes** | Low (Available during Sem 1) |
| `Curricular units 1st sem (evaluations)`| Numerical | Number of exams / assessments taken in Sem 1 | No | **Yes** | Low (Available at end of Sem 1) |
| `Curricular units 1st sem (approved)` | Numerical | Number of units passed in Sem 1 | No | **Yes** | **Critical Feature** (End of Sem 1) |
| `Curricular units 1st sem (grade)` | Numerical | Grade point average for Sem 1 (0–20) | No | **Yes** | **Critical Feature** (End of Sem 1) |
| `Curricular units 1st sem (without eval)`| Numerical | Units enrolled with zero exam attempts | No | **Yes** | Low (Available at end of Sem 1) |
| `Curricular units 2nd sem (credited)` | Numerical | Approved transferred course units | No | No | **HIGH LEAKAGE** for early warning |
| `Curricular units 2nd sem (enrolled)` | Numerical | Number of units enrolled in Sem 2 | No | No | **HIGH LEAKAGE** for early warning |
| `Curricular units 2nd sem (evaluations)`| Numerical | Number of exams taken in Sem 2 | No | No | **HIGH LEAKAGE** for early warning |
| `Curricular units 2nd sem (approved)` | Numerical | Number of units passed in Sem 2 | No | No | **CRITICAL LEAKAGE** for early warning |
| `Curricular units 2nd sem (grade)` | Numerical | Grade point average for Sem 2 (0–20) | No | No | **CRITICAL LEAKAGE** for early warning |
| `Curricular units 2nd sem (without eval)`| Numerical | Units enrolled with zero exam attempts | No | No | **HIGH LEAKAGE** for early warning |
| `Unemployment rate` | Numerical | Regional macroeconomic indicator | **Yes** | **Yes** | None (Macroeconomic context) |
| `Inflation rate` | Numerical | Regional inflation indicator | **Yes** | **Yes** | None (Macroeconomic context) |
| `GDP` | Numerical | Regional gross domestic product rate | **Yes** | **Yes** | None (Macroeconomic context) |

---

## 2. Preventing Temporal Data Leakage in Part 2 ML Modeling

### A. The Week-6 Early Warning Dilemma
* If an AI system claims to predict student dropout at **Week 6 of the academic year**, it **MUST NOT** include `Curricular units 2nd sem (grade)` or `Curricular units 2nd sem (approved)`.
* Doing so would introduce **hindsight leakage**, creating artificially inflated test accuracy (>99%) that catastrophically fails in real-world deployment when 2nd-semester grades do not yet exist.

### B. Valid Experimental Setups for Part 2:
1. **Experiment 1 (Admission-Stage Prediction):**
   * Uses only the 21 admission, demographic, and macroeconomic indicators.
   * Tests baseline risk before classes commence.
2. **Experiment 2 (First-Semester Early Warning):**
   * Incorporates admission features + 1st Semester academic outcomes (27 features).
   * Models actionable intervention at the start of Semester 2.
3. **Experiment 3 (Full Academic Trajectory):**
   * Uses all 36 features across Year 1 to benchmark institutional graduation vs dropout rates.

---
*Documented in accordance with REVA University Capstone Quality Guidelines.*

