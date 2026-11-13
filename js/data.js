/**
 * AI-Powered Smart Campus Intelligence & Student Success Platform
 * Data Store & Paper Citations
 * Author: Student 807 (SRN: STU-807) - REVA University
 * Based on Project Task-2 Literature Survey & Synthesis
 */

const PLATFORM_CONFIG = {
  institution: "REVA University",
  school: "School of Computing & Information Technology",
  project: "AI-Powered Smart Campus Intelligence & Student Success Platform",
  developer: {
    name: "Lead Researcher",
    srn: "STU-807",
    program: "B.Tech in Computer Science and Engineering (AI & ML)",
    semester: "7th Semester / Section B"
  },
  aiEngine: {
    version: "v2.4-Hybrid",
    activeModels: ["Conv-LSTM (Temporal)", "CatBoost (Tree-Ensemble)", "SAL&EC-BP (Context-Aware)", "DiCE (Counterfactuals)"],
    leadTimeWeeks: 4.2,
    accuracy: 94.6,
    aucScore: 0.965
  }
};

const RESEARCH_PAPERS = [
  {
    id: "01",
    citeKey: "s10758-023-09650-0",
    title: "Informative Feedback and Explainable AI-Based Recommendations to Support Students' Self-regulation",
    authors: "Muhammad Afzaal, Aayesha Zia, Jalal Nouri, Uno Fors",
    journal: "Technology, Knowledge and Learning (Springer)",
    year: "2024",
    doi: "10.1007/s10758-023-09650-0",
    link: "https://doi.org/10.1007/s10758-023-09650-0",
    methodology: "Random Forest & ANN (~88% accuracy), SMOTE balancing, DiCE Counterfactual Explanations",
    dataset: "446 students in university programming course, Moodle activity logs",
    platformRole: "Powers the Student SRL Dashboard and the Counterfactual 'What-If' prescriptive recommendation generator."
  },
  {
    id: "02",
    citeKey: "s40593-023-00331-8",
    title: "Interpretable Dropout Prediction: Towards XAI-Based Personalized Intervention",
    authors: "Marcell Nagy, Roland Molontay",
    journal: "International Journal of Artificial Intelligence in Education (Springer)",
    year: "2024",
    doi: "10.1007/s40593-023-00331-8",
    link: "https://doi.org/10.1007/s40593-023-00331-8",
    methodology: "CatBoost (AP: 0.847, AUC: 0.774) with Permutation Importance, PDP, LIME, and TreeSHAP",
    dataset: "Large university STEM cohort at Budapest University of Technology and Economics (BME)",
    platformRole: "Drives the Dropout Risk Scoring module and the SHAP local/global feature attribution waterfalls."
  },
  {
    id: "03",
    citeKey: "Early_Warning_Subjective_Objective",
    title: "Early Warning of Student Performance With Integration of Subjective and Objective Elements",
    authors: "K. Qin, et al.",
    journal: "IEEE Access, Vol. 11",
    year: "2023",
    doi: "10.1109/ACCESS.2023.3295580",
    link: "https://doi.org/10.1109/ACCESS.2023.3295580",
    methodology: "SAL&EC-BP Framework (Validation Acc: 94.09%, Macro-F1: 0.822, AUC: 0.965)",
    dataset: "Longitudinal weekly university institutional data tracking academic & environmental changes",
    platformRole: "Underpins the Dual-Factor Risk Matrix (Student Academic Level vs. External Characteristics/Environment)."
  },
  {
    id: "04",
    citeKey: "s41239-021-00313-7",
    title: "Learning Analytics Dashboard: A Tool for Providing Actionable Insights to Learners",
    authors: "Teo Susnjak, Gomathy Suganya Ramaswami, Anuradha Mathrani",
    journal: "Intl. Journal of Educational Technology in Higher Education",
    year: "2022",
    doi: "10.1186/s41239-021-00313-7",
    link: "https://doi.org/10.1186/s41239-021-00313-7",
    methodology: "PRISMA systematic review (17 included empirical dashboards) + 3-tier Analytics Architecture",
    dataset: "Comprehensive systematic synthesis of 2,680 higher-ed learning analytics papers",
    platformRole: "Guides the three-tier dashboard architecture: Descriptive (status) -> Predictive (risk) -> Prescriptive (actions)."
  },
  {
    id: "05",
    citeKey: "applsci-12-01885-v2",
    title: "Week-Wise Student Performance Early Prediction in Virtual Learning Environment Using Deep XAI",
    authors: "Hsing-Chung Chen, et al.",
    journal: "Applied Sciences (MDPI), Vol. 12",
    year: "2022",
    doi: "10.3390/app12041885",
    link: "https://doi.org/10.3390/app12041885",
    methodology: "Conv-LSTM & CNN-LSTM (Week 6 Recall: 0.91, Week 16 Accuracy: >0.950) with temporal clickstream attention",
    dataset: "977 students with >202,000 Moodle VLE activity logs across 16 weeks",
    platformRole: "Powers the Temporal Week-Wise Risk Trajectory tracker and clickstream sequence anomaly detector."
  }
];

const STUDENTS_DATABASE = [
  {
    id: "STU-807",
    anonymizedId: "ANON-8807",
    name: "Lead Researcher",
    srn: "STU-807",
    program: "B.Tech in CSE (AI & ML)",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Low",
    riskScore: 4,
    dropoutProb: 4,
    academicWarning: "Exemplary Standing",
    salScore: 96,
    ecScore: 94,
    cgpa: 9.42,
    midtermScore: 95,
    attendanceRate: 98,
    vleStudyHoursWeekly: 14.5,
    quizCompletionRate: 100,
    forumPosts: 28,
    assignmentLatenessDays: 0,
    lastActiveDate: "Today",
    primaryRiskFactor: "Optimal Mastery (No Risk Factors Detected)",
    assignedAdvisorId: "FAC_AIML_01",
    assignedAdvisorName: "Faculty Advisor 01",
    trajectory: [8, 7, 6, 5, 5, 4, 4],
    shapAttribution: [
      { feature: "Consistent LMS Engagement (>14h/wk)", impact: -38, type: "positive" },
      { feature: "High Internal Assessment (98%)", impact: -32, type: "positive" },
      { feature: "Foundational Math Mastery", impact: -24, type: "positive" },
      { feature: "100% Lab Practical Completion", impact: -18, type: "positive" }
    ],
    counterfactuals: [
      { action: "Maintain current SRL pace; proceed with Advanced Transformer research", targetRisk: 3, icon: "check" }
    ],
    radar: { vleHours: 95, quizScore: 98, attendance: 98, forumActivity: 92, onTimeSubmissions: 100, labPerformance: 96 }
  },
  {
    id: "STU-801",
    anonymizedId: "ANON-8801",
    name: "Student 801",
    srn: "STU-801",
    program: "B.Tech in CSE (AI & ML)",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Low",
    riskScore: 8,
    dropoutProb: 8,
    academicWarning: "On Track",
    salScore: 88,
    ecScore: 86,
    cgpa: 8.65,
    midtermScore: 86,
    attendanceRate: 91,
    vleStudyHoursWeekly: 9.8,
    quizCompletionRate: 92,
    forumPosts: 12,
    assignmentLatenessDays: 0.5,
    lastActiveDate: "Yesterday",
    primaryRiskFactor: "Occasional minor quiz delay (protective factors high)",
    assignedAdvisorId: "FAC_AIML_02",
    assignedAdvisorName: "Faculty Advisor 02",
    trajectory: [14, 12, 11, 10, 9, 8, 8],
    shapAttribution: [
      { feature: "Strong Exam Performance (86%)", impact: -25, type: "positive" },
      { feature: "Regular Attendance (91%)", impact: -22, type: "positive" },
      { feature: "Slight Quiz Delay (+0.5d)", impact: 8, type: "negative" }
    ],
    counterfactuals: [
      { action: "Submit quizzes 24 hours prior to deadline", targetRisk: 5, icon: "calendar" }
    ],
    radar: { vleHours: 85, quizScore: 88, attendance: 91, forumActivity: 75, onTimeSubmissions: 90, labPerformance: 88 }
  },
  {
    id: "STU-818",
    anonymizedId: "ANON-8818",
    name: "Student 818",
    srn: "STU-818",
    program: "B.Tech in CSE (AI & ML)",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
    riskCategory: "High",
    riskScore: 78,
    dropoutProb: 79,
    academicWarning: "Critical Shortage Alert",
    salScore: 48,
    ecScore: 42,
    cgpa: 5.62,
    midtermScore: 45,
    attendanceRate: 58.5,
    vleStudyHoursWeekly: 2.5,
    quizCompletionRate: 46,
    forumPosts: 2,
    assignmentLatenessDays: 4.8,
    lastActiveDate: "5 days ago",
    primaryRiskFactor: "Attendance Shortage (58.5% < 75%) & IA-1 Score Deficit",
    assignedAdvisorId: "FAC_AIML_03",
    assignedAdvisorName: "Dr. Rajesh V",
    trajectory: [35, 45, 55, 65, 72, 76, 78],
    shapAttribution: [
      { feature: "Severe Attendance Shortage (58.5%)", impact: 38, type: "negative" },
      { feature: "Low VLE Study Hours (2.5h/wk)", impact: 29, type: "negative" },
      { feature: "IA-1 Score Deficit (12/30)", impact: 24, type: "negative" },
      { feature: "Foundational Math Credits", impact: -12, type: "positive" }
    ],
    counterfactuals: [
      { action: "Attend remedial classes to lift attendance above 75%", targetRisk: 44, icon: "check" },
      { action: "Complete PACD-RAG prerequisite drill on Chain Rule", targetRisk: 52, icon: "book" }
    ],
    radar: { vleHours: 35, quizScore: 46, attendance: 58, forumActivity: 20, onTimeSubmissions: 40, labPerformance: 52 }
  },
  {
    id: "STU-842",
    anonymizedId: "ANON-8842",
    name: "Student 842",
    srn: "STU-842",
    program: "B.Tech in CSE (AI & ML)",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Medium",
    riskScore: 42,
    dropoutProb: 43,
    academicWarning: "Attendance Warning",
    salScore: 66,
    ecScore: 68,
    cgpa: 6.95,
    midtermScore: 62,
    attendanceRate: 72.0,
    vleStudyHoursWeekly: 5.2,
    quizCompletionRate: 68,
    forumPosts: 5,
    assignmentLatenessDays: 1.8,
    lastActiveDate: "2 days ago",
    primaryRiskFactor: "Borderline Attendance (72% < 75%) & Unit-2 Concept Gaps",
    assignedAdvisorId: "FAC_AIML_02",
    assignedAdvisorName: "Faculty Advisor 02",
    trajectory: [24, 28, 32, 38, 41, 42, 42],
    shapAttribution: [
      { feature: "Borderline Attendance (72%)", impact: 26, type: "negative" },
      { feature: "Unit 2 Partial Derivatives Deficit", impact: 19, type: "negative" },
      { feature: "Steady Lab Submissions", impact: -18, type: "positive" }
    ],
    counterfactuals: [
      { action: "Increase attendance by attending next 4 lectures", targetRisk: 28, icon: "calendar" }
    ],
    radar: { vleHours: 60, quizScore: 68, attendance: 72, forumActivity: 50, onTimeSubmissions: 70, labPerformance: 75 }
  },
  {
    id: "STU-895",
    anonymizedId: "ANON-8895",
    name: "Student 895",
    srn: "STU-895",
    program: "B.Tech in CSE (AI & ML)",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
    riskCategory: "High",
    riskScore: 84,
    dropoutProb: 84,
    academicWarning: "Institutional Disqualification Warning",
    salScore: 40,
    ecScore: 34,
    cgpa: 4.88,
    midtermScore: 38,
    attendanceRate: 51.0,
    vleStudyHoursWeekly: 1.8,
    quizCompletionRate: 35,
    forumPosts: 0,
    assignmentLatenessDays: 6.2,
    lastActiveDate: "6 days ago",
    primaryRiskFactor: "Critical Attendance Shortage (51%) & Multiple IA Deficits",
    assignedAdvisorId: "FAC_AIML_03",
    assignedAdvisorName: "Dr. Rajesh V",
    trajectory: [42, 52, 64, 72, 78, 82, 84],
    shapAttribution: [
      { feature: "Severe Attendance Shortage (51%)", impact: 44, type: "negative" },
      { feature: "IA Score Deficit (<10/30)", impact: 31, type: "negative" },
      { feature: "VLE Inactivity (>6 days)", impact: 22, type: "negative" }
    ],
    counterfactuals: [
      { action: "Immediate mentor counseling with Dr. Rajesh V", targetRisk: 58, icon: "user" },
      { action: "Enroll in PACD-RAG Remedial Intensive Track", targetRisk: 62, icon: "book" }
    ],
    radar: { vleHours: 25, quizScore: 35, attendance: 51, forumActivity: 10, onTimeSubmissions: 30, labPerformance: 42 }
  },
  {
    id: "STU-1001",
    anonymizedId: "ANON-8821",
    name: "Student 801",
    srn: "R21EA102",
    program: "B.Tech AIML",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
    riskCategory: "High",
    riskScore: 89,
    dropoutProb: 84,
    academicWarning: "Critical Alert",
    salScore: 42, // Student Academic Level (Qin et al.)
    ecScore: 35,  // External Characteristics
    cgpa: 5.84,
    midtermScore: 41,
    attendanceRate: 64,
    vleStudyHoursWeekly: 2.1,
    quizCompletionRate: 38,
    forumPosts: 1,
    assignmentLatenessDays: 3.5,
    lastActiveDate: "4 days ago",
    primaryRiskFactor: "Severe drop in LMS engagement & quiz incompletion",
    trajectory: [28, 35, 42, 58, 72, 81, 89], // Week 1 to 7 Conv-LSTM trend
    shapAttribution: [
      { feature: "Quiz Completion (<40%)", impact: 34, type: "negative" },
      { feature: "VLE Study Hours (2.1h/wk)", impact: 29, type: "negative" },
      { feature: "Assignment Delays (+3.5d)", impact: 21, type: "negative" },
      { feature: "Low Midterm (41%)", impact: 18, type: "negative" },
      { feature: "Foundational Math Credits", impact: -13, type: "positive" }
    ],
    counterfactuals: [
      { action: "Increase weekly VLE study time from 2.1h to 6.5h", targetRisk: 52, icon: "clock" },
      { action: "Submit remedial quiz on Deep Learning Module 3", targetRisk: 41, icon: "check-circle" },
      { action: "Attend 2 mentor tutoring sessions in Section B", targetRisk: 24, icon: "users" }
    ],
    interventionStatus: "Intervention Scheduled",
    mentorAssigned: "Dr. Ramesh Babu (SCIT)",
    interventionLog: [
      { date: "Oct 19, 2026", note: "Early-warning trigger: 3 consecutive missed quizzes.", author: "Automated Conv-LSTM Alert" },
      { date: "Oct 21, 2026", note: "Faculty mentor scheduled 1-on-1 counseling session for Oct 24.", author: "Dr. Ramesh Babu" }
    ]
  },
  {
    id: "STU-1002",
    anonymizedId: "ANON-4190",
    name: "Pooja Hegde",
    srn: "R21EA145",
    program: "B.Tech AIML",
    department: "AI & ML",
    semester: 7,
    section: "A",
    avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80",
    riskCategory: "High",
    riskScore: 78,
    dropoutProb: 72,
    academicWarning: "High Risk",
    salScore: 48,
    ecScore: 40,
    cgpa: 6.12,
    midtermScore: 52,
    attendanceRate: 71,
    vleStudyHoursWeekly: 3.4,
    quizCompletionRate: 50,
    forumPosts: 2,
    assignmentLatenessDays: 2.1,
    lastActiveDate: "2 days ago",
    primaryRiskFactor: "Commute distance & irregular video lecture viewing",
    trajectory: [30, 38, 45, 60, 68, 74, 78],
    shapAttribution: [
      { feature: "Video Lecture Completion (<45%)", impact: 31, type: "negative" },
      { feature: "Attendance Falling (<75%)", impact: 26, type: "negative" },
      { feature: "Quiz Performance Drop", impact: 19, type: "negative" },
      { feature: "Prior CGPA Stability", impact: -14, type: "positive" },
      { feature: "Lab Work Punctuality", impact: -8, type: "positive" }
    ],
    counterfactuals: [
      { action: "Stream offline module recordings (raise to 80%)", targetRisk: 46, icon: "video" },
      { action: "Maintain 80%+ classroom attendance next 3 weeks", targetRisk: 32, icon: "calendar" }
    ],
    interventionStatus: "Pending Action",
    mentorAssigned: "Prof. Ananya Rao",
    interventionLog: [
      { date: "Oct 20, 2026", note: "Automated notification: Attendance dropped below 75% threshold.", author: "System Monitor" }
    ]
  },
  {
    id: "STU-1003",
    anonymizedId: "ANON-7312",
    name: "Karan Verma",
    srn: "R22CS304",
    program: "B.Tech CSE",
    department: "Computer Science",
    semester: 5,
    section: "C",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Medium",
    riskScore: 61,
    dropoutProb: 49,
    academicWarning: "Moderate Watchlist",
    salScore: 62,
    ecScore: 55,
    cgpa: 6.95,
    midtermScore: 64,
    attendanceRate: 79,
    vleStudyHoursWeekly: 5.2,
    quizCompletionRate: 68,
    forumPosts: 4,
    assignmentLatenessDays: 0.8,
    lastActiveDate: "Yesterday",
    primaryRiskFactor: "Declining trend in weekly code submissions",
    trajectory: [20, 25, 34, 46, 52, 59, 61],
    shapAttribution: [
      { feature: "Code Lab Git Activity Decline", impact: 27, type: "negative" },
      { feature: "Quiz 3 & 4 Score Drop", impact: 22, type: "negative" },
      { feature: "Good Lecture Attendance (79%)", impact: -18, type: "positive" },
      { feature: "Consistent Resource Downloads", impact: -12, type: "positive" }
    ],
    counterfactuals: [
      { action: "Complete Git repo lab exercises for Algorithms", targetRisk: 34, icon: "code" },
      { action: "Post 2 questions in Technical Discussion Forum", targetRisk: 28, icon: "message-square" }
    ],
    interventionStatus: "Intervention In-Progress",
    mentorAssigned: "Dr. S. K. Murthy",
    interventionLog: [
      { date: "Oct 15, 2026", note: "Advisor suggested attending weekend peer-assisted coding circle.", author: "Dr. S. K. Murthy" },
      { date: "Oct 18, 2026", note: "Student attended coding session; progress registered.", author: "Peer Lead" }
    ]
  },
  {
    id: "STU-1004",
    anonymizedId: "ANON-9011",
    name: "Meera Nair",
    srn: "R22CS215",
    program: "B.Tech CSE",
    department: "Computer Science",
    semester: 5,
    section: "A",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Medium",
    riskScore: 54,
    dropoutProb: 38,
    academicWarning: "Moderate Watchlist",
    salScore: 66,
    ecScore: 62,
    cgpa: 7.30,
    midtermScore: 69,
    attendanceRate: 83,
    vleStudyHoursWeekly: 6.0,
    quizCompletionRate: 72,
    forumPosts: 5,
    assignmentLatenessDays: 0.0,
    lastActiveDate: "3 hours ago",
    primaryRiskFactor: "Sub-optimal forum participation & exam anxiety indicators",
    trajectory: [22, 26, 31, 40, 48, 51, 54],
    shapAttribution: [
      { feature: "Midterm Score Below Historical Avg", impact: 24, type: "negative" },
      { feature: "Low Discussion Board Interaction", impact: 18, type: "negative" },
      { feature: "High Assignment Punctuality (0.0d)", impact: -22, type: "positive" },
      { feature: "Good Classroom Attendance (83%)", impact: -20, type: "positive" }
    ],
    counterfactuals: [
      { action: "Participate in weekly collaborative study groups", targetRisk: 29, icon: "users" },
      { action: "Review AI diagnostic quizzes in discrete mathematics", targetRisk: 21, icon: "book-open" }
    ],
    interventionStatus: "Resolved / Stabilized",
    mentorAssigned: "Prof. Divya K.",
    interventionLog: [
      { date: "Oct 12, 2026", note: "Sent personalized feedback based on counterfactual recommendations.", author: "Prof. Divya K." },
      { date: "Oct 20, 2026", note: "Student scored 84% on follow-up checkpoint. Risk normalized.", author: "System Monitor" }
    ]
  },
  {
    id: "STU-1005",
    anonymizedId: "ANON-5561",
    name: "Rohan Kulkarni",
    srn: "R23DS110",
    program: "B.Tech Data Science",
    department: "Data Science",
    semester: 3,
    section: "A",
    avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
    riskCategory: "High",
    riskScore: 82,
    dropoutProb: 79,
    academicWarning: "Critical Alert",
    salScore: 44,
    ecScore: 38,
    cgpa: 5.90,
    midtermScore: 46,
    attendanceRate: 68,
    vleStudyHoursWeekly: 2.8,
    quizCompletionRate: 42,
    forumPosts: 0,
    assignmentLatenessDays: 4.0,
    lastActiveDate: "5 days ago",
    primaryRiskFactor: "High assignment lateness & zero discussion activity",
    trajectory: [35, 44, 52, 65, 74, 80, 82],
    shapAttribution: [
      { feature: "Assignment Delays (+4.0d)", impact: 33, type: "negative" },
      { feature: "Zero Forum Participation", impact: 28, type: "negative" },
      { feature: "VLE Engagement Hours (<3h/wk)", impact: 24, type: "negative" },
      { feature: "Basic Programming Prerequisite Pass", impact: -11, type: "positive" }
    ],
    counterfactuals: [
      { action: "Clear overdue Assignment 2 & 3 within 72 hrs", targetRisk: 48, icon: "upload" },
      { action: "Engage in data structures discussion forum", targetRisk: 36, icon: "message-circle" }
    ],
    interventionStatus: "Pending Action",
    mentorAssigned: "Dr. Preethi Shenoy",
    interventionLog: [
      { date: "Oct 21, 2026", note: "CatBoost dropout risk crossed 75% cutoff threshold.", author: "AI Risk Engine" }
    ]
  },
  {
    id: "STU-1006",
    anonymizedId: "ANON-3204",
    name: "Ananya Deshmukh",
    srn: "R21EA189",
    program: "B.Tech AIML",
    department: "AI & ML",
    semester: 7,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Low",
    riskScore: 16,
    dropoutProb: 8,
    academicWarning: "Safe / High Achiever",
    salScore: 92,
    ecScore: 89,
    cgpa: 9.35,
    midtermScore: 94,
    attendanceRate: 96,
    vleStudyHoursWeekly: 11.5,
    quizCompletionRate: 98,
    forumPosts: 16,
    assignmentLatenessDays: -1.8,
    lastActiveDate: "30 mins ago",
    primaryRiskFactor: "None (High SRL & Consistent Leader)",
    trajectory: [12, 14, 15, 14, 17, 15, 16],
    shapAttribution: [
      { feature: "High Quiz Mastery (98%)", impact: -38, type: "positive" },
      { feature: "VLE Study Hours (11.5h/wk)", impact: -32, type: "positive" },
      { feature: "Early Submissions (-1.8d)", impact: -25, type: "positive" },
      { feature: "Active Forum Contributor", impact: -19, type: "positive" },
      { feature: "Course Workload Surge", impact: 8, type: "negative" }
    ],
    counterfactuals: [
      { action: "Eligible for Peer Mentorship Fellowship", targetRisk: 10, icon: "award" },
      { action: "Recommend advanced research publication track", targetRisk: 8, icon: "file-text" }
    ],
    interventionStatus: "Resolved / Stabilized",
    mentorAssigned: "Dr. Ramesh Babu (SCIT)",
    interventionLog: [
      { date: "Oct 05, 2026", note: "Nominated as Peer Tutor for Deep Learning course.", author: "Dept Chair" }
    ]
  },
  {
    id: "STU-1007",
    anonymizedId: "ANON-6022",
    name: "Aditya Roy",
    srn: "R21EC112",
    program: "B.Tech ECE",
    department: "Electronics & Comm",
    semester: 7,
    section: "A",
    avatar: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Medium",
    riskScore: 58,
    dropoutProb: 44,
    academicWarning: "Moderate Watchlist",
    salScore: 61,
    ecScore: 59,
    cgpa: 6.82,
    midtermScore: 63,
    attendanceRate: 77,
    vleStudyHoursWeekly: 4.8,
    quizCompletionRate: 64,
    forumPosts: 3,
    assignmentLatenessDays: 1.2,
    lastActiveDate: "1 day ago",
    primaryRiskFactor: "Inconsistent weekly study cadence in signal processing",
    trajectory: [24, 29, 36, 47, 53, 56, 58],
    shapAttribution: [
      { feature: "Signal Processing Simulation Lab Lags", impact: 26, type: "negative" },
      { feature: "Irregular Weekly Study Bursts", impact: 21, type: "negative" },
      { feature: "Good Math Foundations", impact: -16, type: "positive" },
      { feature: "Satisfactory Attendance (77%)", impact: -14, type: "positive" }
    ],
    counterfactuals: [
      { action: "Stabilize weekly study schedule to >6h/week", targetRisk: 31, icon: "clock" },
      { action: "Complete MATLAB simulation checkpoint 3", targetRisk: 25, icon: "cpu" }
    ],
    interventionStatus: "Intervention Scheduled",
    mentorAssigned: "Prof. Vinay Kumar",
    interventionLog: [
      { date: "Oct 18, 2026", note: "Scheduled check-in on MATLAB lab submissions.", author: "Prof. Vinay Kumar" }
    ]
  },
  {
    id: "STU-1008",
    anonymizedId: "ANON-1198",
    name: "Tanvi Sen",
    srn: "R22DS208",
    program: "B.Tech Data Science",
    department: "Data Science",
    semester: 5,
    section: "B",
    avatar: "https://images.unsplash.com/photo-1534751516642-a171ed296a2d?w=150&auto=format&fit=crop&q=80",
    riskCategory: "Low",
    riskScore: 22,
    dropoutProb: 12,
    academicWarning: "On Track",
    salScore: 86,
    ecScore: 82,
    cgpa: 8.74,
    midtermScore: 88,
    attendanceRate: 92,
    vleStudyHoursWeekly: 9.6,
    quizCompletionRate: 94,
    forumPosts: 11,
    assignmentLatenessDays: -0.9,
    lastActiveDate: "45 mins ago",
    primaryRiskFactor: "None (High Consistency)",
    trajectory: [18, 19, 21, 20, 24, 21, 22],
    shapAttribution: [
      { feature: "Consistent Assignment Turn-in", impact: -31, type: "positive" },
      { feature: "High Quiz Accuracy", impact: -28, type: "positive" },
      { feature: "Active Discussion Contributor", impact: -20, type: "positive" },
      { feature: "Minor Elective Workload", impact: 6, type: "negative" }
    ],
    counterfactuals: [
      { action: "Explore advanced Kaggle competitive track", targetRisk: 15, icon: "trending-up" }
    ],
    interventionStatus: "Resolved / Stabilized",
    mentorAssigned: "Dr. Preethi Shenoy",
    interventionLog: [
      { date: "Sept 30, 2026", note: "Semester initial review: exemplary self-regulated learning.", author: "Dr. Preethi Shenoy" }
    ]
  }
];

const CAMPUS_ANALYTICS = {
  totalStudents: 1420,
  highRiskCount: 68,
  mediumRiskCount: 184,
  lowRiskCount: 1168,
  activeInterventions: 42,
  resolvedInterventionsThisMonth: 86,
  interventionsSuccessRate: 91.8,
  averageLeadTimeWeeks: 4.2,
  departmentBreakdown: [
    { department: "B.Tech AI & ML", total: 420, high: 21, medium: 52, low: 347, avgRisk: 28.4 },
    { department: "B.Tech CSE", total: 540, high: 24, medium: 72, low: 444, avgRisk: 27.2 },
    { department: "B.Tech Data Science", total: 260, high: 14, medium: 36, low: 210, avgRisk: 29.8 },
    { department: "B.Tech ECE", total: 200, high: 9, medium: 24, low: 167, avgRisk: 26.5 }
  ],
  weeklyTemporalTrend: {
    weeks: ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12", "W13", "W14", "W15", "W16"],
    convLstmAccuracy: [68.2, 73.1, 79.4, 84.6, 88.2, 91.0, 92.5, 93.8, 94.2, 94.8, 95.1, 95.3, 95.4, 95.6, 95.7, 95.8],
    convLstmRecall: [61.0, 67.5, 74.2, 81.3, 86.4, 90.8, 92.0, 93.1, 93.7, 94.2, 94.6, 94.8, 95.0, 95.2, 95.3, 95.5],
    atRiskPopulationIdentified: [18, 29, 44, 58, 65, 68, 68, 67, 66, 64, 62, 60, 59, 58, 57, 56]
  },
  modelBenchmark: [
    { model: "Conv-LSTM Deep XAI (Chen et al. 2022)", acc: "95.8%", recall: "91.0% (W6) / 95.5% (W16)", auc: "0.962", xai: "Temporal Heatmaps" },
    { model: "SAL&EC-BP Context Network (Qin et al. 2023)", acc: "94.09%", recall: "92.4%", auc: "0.965", xai: "Dual-Factor SAL-EC" },
    { model: "CatBoost Gradient Boosting (Nagy & Molontay 2024)", acc: "91.5%", recall: "88.2%", auc: "0.774 / AP 0.847", xai: "TreeSHAP & LIME" },
    { model: "Random Forest + DiCE (Afzaal et al. 2024)", acc: "88.2%", recall: "86.5%", auc: "0.912", xai: "Counterfactual Recs" }
  ]
};
