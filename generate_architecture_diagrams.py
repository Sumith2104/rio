"""
generate_architecture_diagrams.py
---------------------------------
Generates 3 publication-quality architecture diagrams for PACD-RAG:
1. Current Phase-1 End-to-End System Architecture
2. Root-Cause Diagnostic Traversal Walkthrough (Sneha Patel 2.5/10 Case Study)
3. Future Phase-2 & Phase-3 Expansion Roadmap
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = r"C:\Users\sumit\Downloads\rio\assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set high DPI and aesthetic styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# ==============================================================================
# DIAGRAM 1: Current Phase-1 Architecture
# ==============================================================================
def create_current_architecture():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=150)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Main Title
    ax.text(50, 96, "PACD-RAG: Current Phase-1 System Architecture", 
            fontsize=16, fontweight='bold', ha='center', color='#0F172A')
    ax.text(50, 93, "Predictive Academic & Conceptual Diagnostic System with Hybrid RAG & Ontological Knowledge Graph", 
            fontsize=10, ha='center', color='#475569', fontstyle='italic')

    # Box styling helper
    def draw_box(x, y, w, h, bg_color, border_color, title, subtitle="", items=None, title_color="#0F172A"):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
                                     linewidth=1.5, edgecolor=border_color, facecolor=bg_color)
        ax.add_patch(rect)
        if title:
            ax.text(x + w/2, y + h - 3, title, fontsize=10.5, fontweight='bold', ha='center', color=title_color)
        if subtitle:
            ax.text(x + w/2, y + h - 5.5, subtitle, fontsize=8.5, ha='center', color='#64748B', fontstyle='italic')
        if items:
            curr_y = y + h - 8.5
            for it in items:
                ax.text(x + 2, curr_y, f"• {it}", fontsize=8.2, color='#1E293B', va='center')
                curr_y -= 3.2

    # LAYER 1: DATA INGESTION LAYER
    draw_box(4, 58, 26, 30, '#EFF6FF', '#3B82F6', "1. Data Ingestion Layer", 
             "Batch & Raw Campus Records",
             ["IA-1 & IA-2 Question-Wise Marks", "Student Midterm & Attendance Data", 
              "Course Syllabus (68 AI/ML Concepts)", "Faculty Lecture Slides (PDF/PPT)", 
              "Structured CSV Section Uploader"])

    # LAYER 2A: 4-TIER RISK ENSEMBLE
    draw_box(37, 72, 27, 16, '#FEF3C7', '#D97706', "2A. Predictive Risk Engine", 
             "Early At-Risk Classification",
             ["CatBoost + XGBoost + LightGBM + RF", "5-Fold Cross Validation (94.2% AUC)", 
              "F1-Score: 92.5% | Low False Negatives"])

    # LAYER 2B: 68-CONCEPT OKF DAG
    draw_box(37, 49, 27, 20, '#F0FDF4', '#16A34A', "2B. 68-Concept OKF DAG", 
             "Ontological Knowledge Framework",
             ["NetworkX Directed Acyclic Graph", "Prerequisite Dependency Tree", 
              "Bloom's Taxonomy Cognitive Mapping", "Upstream Deficit Root-Cause Traversal"])

    # LAYER 2C: HYBRID RAG ENGINE
    draw_box(37, 24, 27, 22, '#FAF5FF', '#9333EA', "2C. Hybrid RAG Search Engine", 
             "Zero-Hallucination Grounding",
             ["BM25 Lexical Keyword Search", "FAISS Dense Vector Embeddings (MiniLM)", 
              "Reciprocal Rank Fusion (RRF, k=60)", "Cross-Encoder Re-Ranker (MS-MARCO)", 
              "Direct Faculty Slide Citing (<200ms)"])

    # LAYER 3: SYNTHESIS & REMEDIATION
    draw_box(71, 49, 25, 39, '#FDF2F8', '#DB2777', "3. Generative Synthesis", 
             "Actionable Student Remediation",
             ["LLM Inference (Gemini / DeepSeek)", "Personalized 5-Day Recovery Plan", 
              "Direct Slide Citation Anchor", "Pre-requisite Gap Explanations", 
              "Targeted Self-Check Quiz Questions"])

    # LAYER 4: DUAL USER DASHBOARDS
    draw_box(15, 4, 70, 16, '#F1F5F9', '#475569', "4. Dual Interactive Presentation Portals (Glassmorphic Web UI)", 
             "Flask REST API + Dynamic High-Contrast Frontends",
             ["STUDENT PORTAL: IA Performance Diagnostics, Upstream Gap Modal, 5-Day Remedial Plan, Attendance Gauge",
              "FACULTY PORTAL: Section Batch Marks Ingestion, Real-Time Pipeline Telemetry, At-Risk Student Cohort Filter",
              "TECH FOUNDATION: Python Flask API, Vanilla JavaScript, Responsive Glassmorphic CSS3, Chart.js Metrics"])

    # Connective Arrows
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#334155", lw=1.5, mutation_scale=12))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 1, label, fontsize=7.5, ha='center', color='#0284C7', fontweight='bold')

    draw_arrow(30, 78, 37, 78, "Marks Data")
    draw_arrow(30, 60, 37, 60, "Syllabus")
    draw_arrow(30, 36, 37, 36, "Slide Decks")
    
    draw_arrow(50, 72, 50, 69, "At-Risk Flag")
    draw_arrow(64, 59, 71, 59, "Root Deficit")
    draw_arrow(64, 35, 71, 52, "Ranked Slides")

    draw_arrow(50, 49, 50, 46, "Prerequisite Context")
    draw_arrow(83, 49, 78, 20, "5-Day Remedial Plan")
    draw_arrow(50, 24, 50, 20, "Real-time Telemetry")

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "arch_fig1_current_system.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()
    print("Generated:", out_path)

# ==============================================================================
# DIAGRAM 2: Diagnostic Root-Cause Traversal Flow (Sneha Patel Example)
# ==============================================================================
def create_diagnostic_walkthrough():
    fig, ax = plt.subplots(figsize=(10, 6.0), dpi=150)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(50, 96, "Diagnostic Root-Cause Traversal Walkthrough: Sneha Patel (R24EA895)", 
            fontsize=15, fontweight='bold', ha='center', color='#0F172A')
    ax.text(50, 93, "How PACD-RAG goes beyond marks to uncover hidden prerequisite gaps and generate verified study plans", 
            fontsize=9.5, ha='center', color='#475569', fontstyle='italic')

    # Steps in horizontal chain
    steps = [
        {"x": 3, "y": 55, "w": 20, "h": 32, "bg": "#EFF6FF", "bc": "#3B82F6",
         "step": "STEP 1: IA-1 TEST MARKS", "title": "Question Deficit Detected",
         "lines": ["Student: Sneha Patel", "Course: AI & Deep Learning", "IA-1 Question 2: Backprop",
                   "Max: 10.0 | Scored: 2.5", "Deficit Threshold: < 4.0/10", "STATUS: DEFICIT (75% Loss)"]},
        
        {"x": 27, "y": 55, "w": 21, "h": 32, "bg": "#FEF3C7", "bc": "#D97706",
         "step": "STEP 2: OKF DAG TRAVERSAL", "title": "Upstream Dependency Walk",
         "lines": ["Concept: Backpropagation", "DAG Upstream Parents:", "  1. Gradient Descent",
                   "  2. Matrix Multiplication", "  3. Chain Rule of Diff.", "ROOT CAUSE: Chain Rule",
                   "Upstream Deficit Identified!"]},
        
        {"x": 52, "y": 55, "w": 21, "h": 32, "bg": "#FAF5FF", "bc": "#9333EA",
         "step": "STEP 3: HYBRID RAG SEARCH", "title": "Faculty Slide Retrieval",
         "lines": ["BM25 Keyword + FAISS Dense", "RRF Fusion Ranking (k=60)", "Re-Ranker: MS-MARCO",
                   "Retrieved Faculty Decks:", "  • Module 3: Slide 14 (Chain Rule)",
                   "  • Module 3: Slide 18 (Gradients)", "Score: 0.94 Match"]},
        
        {"x": 76, "y": 55, "w": 21, "h": 32, "bg": "#F0FDF4", "bc": "#16A34A",
         "step": "STEP 4: ACTIONABLE RECOVERY", "title": "Personalized 5-Day Plan",
         "lines": ["Day 1: Review Slide 14 & Diff.", "Day 2: Partial Deriv. Gradients",
                   "Day 3: Manual 2-Layer Backprop", "Day 4: Python Numpy Code Exercise",
                   "Day 5: 3 Self-Assessment Tests", "OUTCOME: 8.5/10 on Re-Test!"]}
    ]

    for s in steps:
        rect = patches.FancyBboxPatch((s["x"], s["y"]), s["w"], s["h"], boxstyle="round,pad=0.6,rounding_size=1.2",
                                     linewidth=1.5, edgecolor=s["bc"], facecolor=s["bg"])
        ax.add_patch(rect)
        ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 2.8, s["step"], fontsize=8, fontweight='bold', ha='center', color=s["bc"])
        ax.text(s["x"] + s["w"]/2, s["y"] + s["h"] - 5.5, s["title"], fontsize=9.5, fontweight='bold', ha='center', color='#0F172A')
        cy = s["y"] + s["h"] - 8.5
        for line in s["lines"]:
            ax.text(s["x"] + 1.2, cy, line, fontsize=7.8, color='#1E293B')
            cy -= 3.3

    # Connective arrows
    ax.annotate('', xy=(27, 71), xytext=(23, 71),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=2.5, mutation_scale=15))
    ax.annotate('', xy=(52, 71), xytext=(48, 71),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=2.5, mutation_scale=15))
    ax.annotate('', xy=(76, 71), xytext=(73, 71),
                arrowprops=dict(arrowstyle="->", color="#0284C7", lw=2.5, mutation_scale=15))

    # BOTTOM CALLOUT: THE CRITICAL DIFFERENCE
    c_box = patches.FancyBboxPatch((5, 10), 90, 36, boxstyle="round,pad=0.8,rounding_size=1.5",
                                  linewidth=1.5, edgecolor='#475569', facecolor='#F8FAFC')
    ax.add_patch(c_box)

    ax.text(50, 42, "Why PACD-RAG Outperforms Traditional College Assessment Systems", 
            fontsize=11.5, fontweight='bold', ha='center', color='#0F172A')

    # Left vs Right Comparison Box
    ax.text(26, 37, "Traditional Campus Workflow (Reactive)", fontsize=9.5, fontweight='bold', color='#DC2626', ha='center')
    trad_lines = [
        "• Faculty records aggregate score: 'Sneha scored 14/30 in Midterm'",
        "• Student is told: 'Study hard for semester exams or you will fail'",
        "• Root cause is completely invisible to both teacher and student",
        "• Student re-reads random YouTube tutorials or whole textbook",
        "• Result: High backlog rate (15-20%) and exam anxiety"
    ]
    ty = 33
    for tl in trad_lines:
        ax.text(7, ty, tl, fontsize=8.2, color='#450A0A')
        ty -= 3.3

    ax.text(74, 37, "PACD-RAG Autonomous Workflow (Diagnostic)", fontsize=9.5, fontweight='bold', color='#16A34A', ha='center')
    pacd_lines = [
        "• System analyzes question-wise breakdown: Q2 Backprop = 2.5/10",
        "• Knowledge Graph maps exact root cause: Chain Rule prerequisite gap",
        "• Hybrid RAG extracts exact slides (Slide 14) from course teacher's deck",
        "• Personalized 5-day structured micro-curriculum generated immediately",
        "• Result: 94.2% prediction accuracy and 88.3% RAGAS quality score"
    ]
    py = 33
    for pl in pacd_lines:
        ax.text(54, py, pl, fontsize=8.2, color='#052E16')
        py -= 3.3

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "arch_fig2_diagnostic_traversal.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()
    print("Generated:", out_path)

# ==============================================================================
# DIAGRAM 3: Future Phase-2 & Phase-3 Roadmap Architecture
# ==============================================================================
def create_future_roadmap():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=150)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Main Title
    ax.text(50, 96, "PACD-RAG: Future Evolution & Innovation Roadmap (Phase 2 & Phase 3)", 
            fontsize=15, fontweight='bold', ha='center', color='#0F172A')
    ax.text(50, 93, "Scaling from a Capstone Pilot to an Autonomous, Enterprise-Grade University Intelligence Platform", 
            fontsize=9.5, ha='center', color='#475569', fontstyle='italic')

    # 5 Pillars of Future Expansion
    pillars = [
        {"x": 4, "y": 48, "w": 28, "h": 41, "bg": "#EFF6FF", "bc": "#2563EB",
         "num": "PILLAR 1", "title": "Automated LMS & ERP Event Bus",
         "phase": "Phase 2 (Immediate Extension)",
         "items": ["Direct Webhooks for Canvas, Moodle, Blackboard",
                   "Real-Time Event Streaming (Apache Kafka / Redis)",
                   "Auto-trigger diagnostic on assignment submit",
                   "Zero manual CSV marks upload required",
                   "Bi-directional gradebook sync with university ERP"]},
        
        {"x": 36, "y": 48, "w": 28, "h": 41, "bg": "#F5F3FF", "bc": "#7C3AED",
         "num": "PILLAR 2", "title": "Domain-Tuned SLM (Local QLoRA)",
         "phase": "Phase 2 (High Privacy & Low Latency)",
         "items": ["Fine-tune LLaMA-3-8B / Mistral-7B on syllabus",
                   "Quantized Low-Rank Adaptation (QLoRA 4-bit)",
                   "Zero external Cloud API costs (100% On-Premise)",
                   "Complete student data privacy (FERPA compliant)",
                   "Sub-200ms generation on campus workstation GPUs"]},
        
        {"x": 68, "y": 48, "w": 28, "h": 41, "bg": "#ECFDF5", "bc": "#059669",
         "num": "PILLAR 3", "title": "Cross-Platform Mobile App",
         "phase": "Phase 2 (Student Ubiquity)",
         "items": ["Flutter iOS & Android unified client",
                   "Push notification alerts for upcoming test deficits",
                   "Daily 5-minute micro-quizzes on DAG gaps",
                   "Offline PDF slide & remedial deck viewer",
                   "Gamified streak counters & mastery badges"]},
        
        {"x": 18, "y": 4, "w": 30, "h": 39, "bg": "#FFFBEB", "bc": "#D97706",
         "num": "PILLAR 4", "title": "Voice Socratic AI Tutor",
         "phase": "Phase 3 (Next-Gen Interaction)",
         "items": ["Speech-to-Speech via Whisper & FastPitch",
                   "Multilingual tutoring: English, Kannada, Hindi",
                   "Socratic questioning: Guides student step-by-step",
                   "Never gives raw answers; prompts thought process",
                   "Hands-free audio revision while commuting"]},
        
        {"x": 52, "y": 4, "w": 30, "h": 39, "bg": "#FDF2F8", "bc": "#DB2777",
         "num": "PILLAR 5", "title": "Faculty Counterfactual XAI Simulator",
         "phase": "Phase 3 (Institutional Analytics)",
         "items": ["SHAP & LIME 'What-If' scenario modeling",
                   "Simulate: 'If Sneha gets 7/10 in re-test, pass % = ?'",
                   "Department-level curriculum gap heatmaps",
                   "Automated Mentor Assignment & Alert Dispatch",
                   "Cross-subject DAG linking (Math -> ML -> Robotics)"]}
    ]

    for p in pillars:
        rect = patches.FancyBboxPatch((p["x"], p["y"]), p["w"], p["h"], boxstyle="round,pad=0.8,rounding_size=1.5",
                                     linewidth=1.5, edgecolor=p["bc"], facecolor=p["bg"])
        ax.add_patch(rect)
        ax.text(p["x"] + p["w"]/2, p["y"] + p["h"] - 3, p["num"], fontsize=8.5, fontweight='bold', ha='center', color=p["bc"])
        ax.text(p["x"] + p["w"]/2, p["y"] + p["h"] - 6.5, p["title"], fontsize=10, fontweight='bold', ha='center', color='#0F172A')
        ax.text(p["x"] + p["w"]/2, p["y"] + p["h"] - 9.5, p["phase"], fontsize=8, ha='center', color='#64748B', fontstyle='italic')
        cy = p["y"] + p["h"] - 13.5
        for it in p["items"]:
            ax.text(p["x"] + 1.8, cy, f"• {it}", fontsize=7.8, color='#1E293B')
            cy -= 4.2

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "arch_fig3_future_roadmap.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=150)
    plt.close()
    print("Generated:", out_path)

if __name__ == "__main__":
    create_current_architecture()
    create_diagnostic_walkthrough()
    create_future_roadmap()
    print("All 3 architectural diagrams generated successfully!")
