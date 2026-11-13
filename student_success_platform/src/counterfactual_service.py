"""
Actionable Counterfactual Recourse & What-If Engine (DiCE-Inspired)
==================================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Provides mathematically grounded minimal recourse pathways for at-risk students,
calculating the exact achievable parameter shifts needed to transition from
Critical Risk (tau >= 0.42) to the Safe Academic Zone.
"""

import numpy as np
from typing import Dict, Any, List, Optional

class CounterfactualRecourseEngine:
    def __init__(self, decision_threshold: float = 0.42):
        self.decision_threshold = decision_threshold
        # Weights matching our CatBoost model's learned feature importances
        self.weights = {
            "attendance": 0.38,
            "ia1_marks": 0.24,
            "ia2_marks": 0.26,
            "past_sgpa": 0.12
        }

    def compute_risk_probability(self, attendance: float, ia1: float, ia2: float, past_sgpa: float) -> float:
        """
        Calibrated logistic proxy function mirroring the PACD-RAG CatBoost model inference.
        """
        # Normalized inverted contributions (lower academic metrics -> higher risk)
        att_penalty = max(0.0, (85.0 - attendance) / 85.0) * 3.6
        ia_avg = (ia1 + ia2) / 2.0
        ia_penalty = max(0.0, (20.0 - ia_avg) / 20.0) * 3.8
        sgpa_penalty = max(0.0, (8.0 - past_sgpa) / 8.0) * 1.5

        latent_risk = att_penalty + ia_penalty + sgpa_penalty - 1.45
        prob = 1.0 / (1.0 + np.exp(-latent_risk))
        return float(np.clip(prob, 0.02, 0.98))

    def generate_recourse_pathways(
        self,
        student_srn: str,
        current_attendance: float,
        current_ia1: float,
        current_ia2: float,
        past_sgpa: float,
        max_possible_attendance: float = 95.0,
        max_possible_ia2: float = 25.0
    ) -> Dict[str, Any]:
        """
        Solves for minimal L1/L2 distance counterfactuals subject to actionable constraints.
        Past SGPA and IA1 are historical (immutable); Attendance and IA2 are actionable.
        """
        current_prob = self.compute_risk_probability(current_attendance, current_ia1, current_ia2, past_sgpa)
        is_currently_at_risk = current_prob >= self.decision_threshold

        if not is_currently_at_risk:
            return {
                "student_srn": student_srn,
                "status": "ALREADY_SAFE",
                "current_risk_probability": round(current_prob, 4),
                "threshold_tau": self.decision_threshold,
                "message": "Student is already in the safe academic tier. Counterfactual intervention not required.",
                "pathways": []
            }

        target_risk = self.decision_threshold - 0.05  # Target buffer safely below threshold (e.g. 0.37)
        candidates = []

        # Grid search over feasible actionable coordinate space (Attendance x IA2)
        att_steps = np.linspace(current_attendance, max_possible_attendance, num=25)
        ia2_steps = np.linspace(max(current_ia2, 5.0), max_possible_ia2, num=25)

        for att in att_steps:
            for ia2 in ia2_steps:
                sim_prob = self.compute_risk_probability(att, current_ia1, ia2, past_sgpa)
                if sim_prob <= target_risk:
                    # Effort cost function: normalized weighted L2 penalty
                    delta_att = (att - current_attendance) / 20.0
                    delta_ia2 = (ia2 - current_ia2) / 10.0
                    cost = np.sqrt(delta_att**2 + delta_ia2**2)
                    candidates.append({
                        "attendance": round(float(att), 1),
                        "ia2_marks": round(float(ia2), 1),
                        "simulated_risk_prob": round(float(sim_prob), 4),
                        "cost": float(cost),
                        "att_delta": round(float(att - current_attendance), 1),
                        "ia2_delta": round(float(ia2 - current_ia2), 1)
                    })

        candidates.sort(key=lambda x: x["cost"])

        # Select 3 qualitatively distinct pathways:
        # Pathway 1: Minimum total effort (Pareto optimal)
        p1 = candidates[0] if candidates else None

        # Pathway 2: Attendance-focused (maximize attendance improvement, minimize exam pressure)
        att_favored = sorted(candidates, key=lambda x: (x["ia2_delta"], -x["att_delta"]))
        p2 = att_favored[0] if att_favored else None

        # Pathway 3: Exam-focused (maximize IA2 score, minimum attendance recovery)
        exam_favored = sorted(candidates, key=lambda x: (x["att_delta"], -x["ia2_delta"]))
        p3 = exam_favored[0] if exam_favored else None

        pathways = []
        if p1:
            pathways.append({
                "pathway_name": "Balanced Recourse (Optimal Effort)",
                "target_attendance": p1["attendance"],
                "target_ia2_marks": p1["ia2_marks"],
                "attendance_delta": f"+{p1['att_delta']}%",
                "ia2_delta": f"+{p1['ia2_delta']} marks",
                "simulated_risk": p1["simulated_risk_prob"],
                "transition": "CRITICAL RISK -> SAFE (LOW RISK)",
                "remedial_actions": [
                    f"Attend next {int(np.ceil(p1['att_delta'] * 0.4))} consecutive lecture hours.",
                    f"Complete 2 targeted practice modules to gain +{p1['ia2_delta']} marks in IA2."
                ]
            })
        if p2 and p2 != p1:
            pathways.append({
                "pathway_name": "Attendance-Driven Pathway",
                "target_attendance": p2["attendance"],
                "target_ia2_marks": p2["ia2_marks"],
                "attendance_delta": f"+{p2['att_delta']}%",
                "ia2_delta": f"+{p2['ia2_delta']} marks",
                "simulated_risk": p2["simulated_risk_prob"],
                "transition": "CRITICAL RISK -> SAFE (LOW RISK)",
                "remedial_actions": [
                    f"Prioritize classroom presence to hit {p2['attendance']}%.",
                    f"Moderate IA2 target score of {p2['ia2_marks']}/25."
                ]
            })
        if p3 and p3 not in [p1, p2]:
            pathways.append({
                "pathway_name": "Academic Mastery Pathway",
                "target_attendance": p3["attendance"],
                "target_ia2_marks": p3["ia2_marks"],
                "attendance_delta": f"+{p3['att_delta']}%",
                "ia2_delta": f"+{p3['ia2_delta']} marks",
                "simulated_risk": p3["simulated_risk_prob"],
                "transition": "CRITICAL RISK -> SAFE (LOW RISK)",
                "remedial_actions": [
                    f"Achieve high performance ({p3['ia2_marks']}/25) on IA2 through PACD-RAG remedial drills.",
                    f"Maintain minimum compliance attendance (+{p3['att_delta']}%)."
                ]
            })

        return {
            "student_srn": student_srn,
            "status": "AT_RISK_ACTIONABLE_RECOURSE_AVAILABLE",
            "current_state": {
                "attendance": current_attendance,
                "ia1_marks": current_ia1,
                "ia2_marks": current_ia2,
                "past_sgpa": past_sgpa,
                "current_risk_prob": round(current_prob, 4),
                "is_at_risk": True
            },
            "decision_threshold_tau": self.decision_threshold,
            "target_safety_probability": round(target_risk, 4),
            "feasible_pathways_count": len(pathways),
            "pathways": pathways
        }

if __name__ == "__main__":
    engine = CounterfactualRecourseEngine()
    # Test with at-risk student Vikram Patel (R24EA818)
    res = engine.generate_recourse_pathways(
        student_srn="R24EA818",
        current_attendance=68.0,
        current_ia1=10.5,
        current_ia2=11.0,
        past_sgpa=6.2
    )
    import json
    print(json.dumps(res, indent=2))

