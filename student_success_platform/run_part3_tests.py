"""
Part 3: Automated End-to-End Verification Test Runner
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807) | REVA University

Usage:
    cd student_success_platform
    python run_part3_tests.py
"""

import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

base_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(base_dir))

from src.explain_model import (
    compute_shap_explanations,
    explain_single_raw_student,
    load_model_and_test_data
)
from src.data_loader import load_student_data


class TestPart3ModelExplainabilitySHAP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 75)
        print("  PART 3 END-TO-END VERIFICATION TEST SUITE: SHAP EXPLAINABILITY")
        print("  Evaluating: Global Attribution, Local Waterfalls, and Axiom Verification")
        print("=" * 75)

    def test_01_shap_values_computation(self):
        """Test 1: Verify SHAP values compute successfully with correct dimensions."""
        shap_values, explainer, y_proba, high_idx, low_idx = compute_shap_explanations(sample_size=50)
        self.assertEqual(shap_values.shape, (50, 236), "SHAP matrix must match sample size and feature dimensions.")
        self.assertIsNotNone(explainer.expected_value, "Explainer must have valid expected baseline value.")
        self.assertEqual(len(y_proba), 50, "Probabilities array must match sample size.")
        print(f"  [PASS] Test 1: SHAP matrix computed with shape {shap_values.shape} and baseline={explainer.expected_value:.4f}.")

    def test_02_additivity_property_verification(self):
        """Test 2: Verify the Shapley Efficiency / Additivity Axiom: sum(phi_i) + phi_0 == f(x)."""
        full_pipeline, classifier, X_train_df, X_test_df, clean_cols = load_model_and_test_data()
        
        # Test on 5 samples
        test_sample = X_test_df.iloc[:5]
        masker = joblib.load(base_dir / "models" / "selected_model_pipeline.joblib")
        
        import shap
        bg = X_train_df.iloc[:100]
        explainer = shap.LinearExplainer(classifier, shap.maskers.Independent(bg, max_samples=100))
        shap_res = explainer(test_sample)
        
        # Raw model decision function outputs (log-odds)
        decision_outputs = classifier.decision_function(test_sample)
        
        # Sum of SHAP values + base value
        reconstructed = shap_res.values.sum(axis=1) + explainer.expected_value
        
        np.testing.assert_allclose(
            reconstructed,
            decision_outputs,
            atol=1e-3,
            err_msg="Shapley additivity axiom violated: sum(phi_i) + base must equal f(x)."
        )
        print("  [PASS] Test 2: Shapley Efficiency/Additivity Axiom confirmed: sum(phi) + base_value == model_output.")

    def test_03_figures_exist_and_non_empty(self):
        """Test 3: Verify all 4 required SHAP figures exist and are non-empty."""
        fig_dir = base_dir / "reports" / "figures"
        required_figs = [
            "shap_global_summary.png",
            "shap_global_importance.png",
            "shap_student_case_waterfall.png",
            "shap_persistent_student_waterfall.png"
        ]
        for f in required_figs:
            p = fig_dir / f
            self.assertTrue(p.exists(), f"Figure {f} must exist.")
            self.assertGreater(p.stat().st_size, 10000, f"Figure {f} must have non-zero content.")
            
        print("  [PASS] Test 3: All 4 SHAP figures verified: Summary, Importance, and Case Waterfalls.")

    def test_04_programmatic_single_student_explainer(self):
        """Test 4: Verify real-time advisor utility returns valid positive/negative risk factors."""
        raw_df = load_student_data().drop(columns=["Target"])
        sample = raw_df.iloc[[0]]
        
        res = explain_single_raw_student(sample)
        self.assertIn("predicted_dropout_probability", res)
        self.assertIn("risk_tier", res)
        self.assertIn("top_5_positive_risk_drivers", res)
        self.assertIn("top_5_protective_factors", res)
        self.assertLessEqual(len(res["top_5_positive_risk_drivers"]), 5)
        self.assertLessEqual(len(res["top_5_protective_factors"]), 5)
        
        print(f"  [PASS] Test 4: Single student explanation verified: {res['risk_tier']} ({res['predicted_dropout_probability']}%) with top risk & protective drivers.")

    def test_05_explanation_report_integrity(self):
        """Test 5: Verify shap_explanation_report.md exists and contains ethical guidelines."""
        rep_path = base_dir / "reports" / "shap_explanation_report.md"
        self.assertTrue(rep_path.exists(), "reports/shap_explanation_report.md must exist.")
        
        with open(rep_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("Curricular units 2nd sem (approved)", content)
        self.assertIn("Attribution, NOT Causation", content)
        self.assertIn("Supportive vs Punitive Action", content)
        print("  [PASS] Test 5: SHAP report validated with responsible AI and non-causal attribution boundaries.")


if __name__ == "__main__":
    unittest.main()

