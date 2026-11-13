"""
Cold-Start Student Bootstrapper & Prior Risk Estimator (PACD-RAG)
=================================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Provides Bayesian cohort transfer learning and KNN peer clustering for newly enrolled
students who lack semester academic and attendance histories (Weeks 1 to 3).
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional

class ColdStartBootstrapper:
    def __init__(self, k_neighbors: int = 7):
        self.k_neighbors = k_neighbors
        self.historical_cohort = self._initialize_historical_cohort()

    def _initialize_historical_cohort(self) -> pd.DataFrame:
        """Seeds historical student pre-enrollment profiles and their realized Week-16 outcomes."""
        np.random.seed(101)
        n = 300
        
        twelfth_pct = np.random.normal(loc=76.0, scale=10.0, size=n)
        twelfth_pct = np.clip(twelfth_pct, 45.0, 98.0)
        
        entrance_percentile = np.random.normal(loc=72.0, scale=14.0, size=n)
        entrance_percentile = np.clip(entrance_percentile, 25.0, 99.5)
        
        math_proficiency_score = np.clip(
            (0.6 * twelfth_pct + 0.4 * entrance_percentile) + np.random.normal(0, 5, size=n), 
            30.0, 100.0
        )
        
        # Realized semester 1 SGPA and dropout risk
        realized_sgpa = (
            0.045 * twelfth_pct +
            0.035 * entrance_percentile +
            0.02 * math_proficiency_score - 1.2 +
            np.random.normal(0, 0.4, size=n)
        )
        realized_sgpa = np.clip(realized_sgpa, 3.5, 9.8)
        
        # Binary realized risk (1 = struggled or dropped out)
        realized_at_risk = (realized_sgpa < 6.75).astype(int)

        return pd.DataFrame({
            "twelfth_pct": twelfth_pct,
            "entrance_percentile": entrance_percentile,
            "math_proficiency": math_proficiency_score,
            "realized_sgpa": realized_sgpa,
            "realized_at_risk": realized_at_risk
        })

    def predict_new_student_prior(
        self,
        student_srn: str,
        student_name: str,
        twelfth_marks_pct: float,
        entrance_exam_percentile: float,
        math_proficiency_score: float,
        admission_stream: str = "CSE (AI & ML)"
    ) -> Dict[str, Any]:
        """
        Calculates cold-start risk prior using similarity-weighted nearest neighbor transfer.
        """
        # Feature normalization
        query_vec = np.array([twelfth_marks_pct, entrance_exam_percentile, math_proficiency_score])
        
        matrix = self.historical_cohort[["twelfth_pct", "entrance_percentile", "math_proficiency"]].values
        
        # Normalization scalers
        means = matrix.mean(axis=0)
        stds = matrix.std(axis=0)
        
        norm_matrix = (matrix - means) / stds
        norm_query = (query_vec - means) / stds
        
        # Euclidean distances in normalized pre-admission feature space
        dists = np.linalg.norm(norm_matrix - norm_query, axis=1)
        nearest_indices = np.argsort(dists)[:self.k_neighbors]
        
        neighbors = self.historical_cohort.iloc[nearest_indices]
        neighbor_dists = dists[nearest_indices]
        
        # Inverse distance weights
        weights = 1.0 / (neighbor_dists + 1e-4)
        weights /= weights.sum()

        weighted_prior_risk = float(np.sum(neighbors["realized_at_risk"].values * weights))
        expected_sgpa_mean = float(np.sum(neighbors["realized_sgpa"].values * weights))
        expected_sgpa_std = float(np.std(neighbors["realized_sgpa"].values))

        # Risk classification for onboarding
        if weighted_prior_risk >= 0.50:
            category = "PRIOR_HIGH_RISK_ONBOARDING_BRIDGE_REQUIRED"
            onboarding_advice = "Assign Foundation Math and Coding Bridge Course during Orientation Week."
        elif weighted_prior_risk >= 0.30:
            category = "PRIOR_MODERATE_MONITOR"
            onboarding_advice = "Assign Peer Mentor and conduct Week-3 check-in."
        else:
            category = "PRIOR_LOW_RISK_ON_TRACK"
            onboarding_advice = "Eligible for Advanced Honors / Research Track Orientation."

        return {
            "student_srn": student_srn,
            "student_name": student_name,
            "admission_stream": admission_stream,
            "assessment_phase": "COLD_START_ONBOARDING (WEEKS 1-3)",
            "pre_admission_metrics": {
                "twelfth_board_pct": twelfth_marks_pct,
                "entrance_percentile": entrance_exam_percentile,
                "math_proficiency": math_proficiency_score
            },
            "bayesian_prior_risk": round(weighted_prior_risk, 4),
            "expected_sgpa_range": {
                "mean": round(expected_sgpa_mean, 2),
                "lower_bound_95ci": round(max(3.0, expected_sgpa_mean - 1.96 * expected_sgpa_std), 2),
                "upper_bound_95ci": round(min(10.0, expected_sgpa_mean + 1.96 * expected_sgpa_std), 2)
            },
            "confidence_tier": "BOOTSTRAP_PEER_TRANSFER (k=7)",
            "onboarding_classification": category,
            "actionable_onboarding_recommendation": onboarding_advice,
            "historical_peers_summary": {
                "peer_count": self.k_neighbors,
                "historical_dropout_rate_in_peer_cluster": f"{round(weighted_prior_risk * 100, 1)}%",
                "avg_realized_sgpa_in_cluster": round(expected_sgpa_mean, 2)
            }
        }

if __name__ == "__main__":
    bootstrapper = ColdStartBootstrapper()
    # Test for a newly registered student with low math entrance marks
    new_student_res = bootstrapper.predict_new_student_prior(
        student_srn="R24EA999",
        student_name="Rahul Verma (Freshman)",
        twelfth_marks_pct=58.0,
        entrance_exam_percentile=42.0,
        math_proficiency_score=48.0
    )
    import json
    print(json.dumps(new_student_res, indent=2))

