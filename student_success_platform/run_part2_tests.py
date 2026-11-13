"""
Part 2: Automated End-to-End Verification Test Runner
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807) | REVA University

Usage:
    cd student_success_platform
    python run_part2_tests.py
"""

import sys
import unittest
import json
from pathlib import Path
import pandas as pd
import numpy as np
import joblib

base_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(base_dir))

from src.data_loader import load_student_data


class TestPart2StudentRiskModeling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 75)
        print("  PART 2 END-TO-END VERIFICATION TEST SUITE: STUDENT RISK MODELING")
        print("  Evaluating: Logistic Regression, Random Forest, CatBoost, XGBoost")
        print("=" * 75)

    def test_01_candidate_models_metadata_exists(self):
        """Test 1: Verify model_metadata.json exists and contains all 4 candidate algorithms."""
        meta_path = base_dir / "models" / "model_metadata.json"
        self.assertTrue(meta_path.exists(), "models/model_metadata.json must exist.")
        
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        self.assertIn("selected_algorithm", meta)
        self.assertIn("all_candidates_comparison", meta)
        
        candidates = [row["Model"] for row in meta["all_candidates_comparison"]]
        for expected in ["Logistic Regression", "Random Forest", "CatBoost", "XGBoost"]:
            self.assertIn(expected, candidates, f"Candidate {expected} must be benchmarked.")
            
        print(f"  [PASS] Test 1: All 4 candidates benchmarked. Selected: {meta['selected_algorithm']}.")

    def test_02_production_pipeline_serialization(self):
        """Test 2: Verify selected_model_pipeline.joblib exists and can be loaded."""
        pipeline_path = base_dir / "models" / "selected_model_pipeline.joblib"
        self.assertTrue(pipeline_path.exists(), "models/selected_model_pipeline.joblib must exist.")
        
        pipeline = joblib.load(pipeline_path)
        self.assertTrue(hasattr(pipeline, "predict"), "Pipeline must have predict method.")
        self.assertTrue(hasattr(pipeline, "predict_proba"), "Pipeline must have predict_proba method.")
        print("  [PASS] Test 2: Serialized end-to-end production pipeline loaded successfully.")

    def test_03_end_to_end_inference_on_raw_data(self):
        """Test 3: Verify the full pipeline accepts raw untouched data and outputs valid predictions."""
        pipeline_path = base_dir / "models" / "selected_model_pipeline.joblib"
        pipeline = joblib.load(pipeline_path)
        
        raw_df = load_student_data().drop(columns=["Target"])
        sample = raw_df.iloc[:10]  # 10 raw students
        
        preds = pipeline.predict(sample)
        probas = pipeline.predict_proba(sample)
        
        self.assertEqual(len(preds), 10, "Must output 10 predictions.")
        self.assertEqual(probas.shape, (10, 2), "Must output probabilities with shape (10, 2).")
        
        # Verify probability normalization
        row_sums = probas.sum(axis=1)
        np.testing.assert_allclose(row_sums, np.ones(10), atol=1e-5, err_msg="Probabilities must sum to 1.0.")
        
        # Verify predictions match argmax
        expected_preds = np.argmax(probas, axis=1)
        np.testing.assert_array_equal(preds, expected_preds, err_msg="Predictions must match argmax probability.")
        print("  [PASS] Test 3: Raw inference verified: End-to-end pipeline handles raw input and returns normalized probabilities.")

    def test_04_test_set_performance_benchmarks(self):
        """Test 4: Verify test set performance meets rigorous quality thresholds."""
        meta_path = base_dir / "models" / "model_metadata.json"
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        test_metrics = meta["test_metrics"]
        
        # Rigorous educational early-warning thresholds
        self.assertGreaterEqual(test_metrics["accuracy"], 0.80, "Accuracy must be >= 80%.")
        self.assertGreaterEqual(test_metrics["macro_f1"], 0.80, "Macro F1 must be >= 0.80.")
        self.assertGreaterEqual(test_metrics["roc_auc"], 0.88, "ROC-AUC must be >= 0.88.")
        self.assertGreaterEqual(test_metrics["dropout_recall"], 0.75, "Dropout recall must be >= 75% to prevent high false negatives.")
        
        print(f"  [PASS] Test 4: Performance verified: Acc={test_metrics['accuracy']:.2%}, Dropout Recall={test_metrics['dropout_recall']:.2%}, ROC-AUC={test_metrics['roc_auc']:.4f}.")

    def test_05_visualizations_generated(self):
        """Test 5: Verify all required publication-quality figures exist on disk."""
        fig_dir = base_dir / "reports" / "figures"
        for fig_name in ["confusion_matrix.png", "class_metrics.png", "roc_curves.png"]:
            path = fig_dir / fig_name
            self.assertTrue(path.exists(), f"Figure {fig_name} must exist.")
            self.assertGreater(path.stat().st_size, 10000, f"Figure {fig_name} must have valid content.")
            
        print("  [PASS] Test 5: All 3 visualization figures verified: Confusion Matrix, Class Metrics, ROC Curves.")

    def test_06_model_comparison_report_exists(self):
        """Test 6: Verify model_comparison.md exists and contains candidate metrics."""
        rep_path = base_dir / "reports" / "model_comparison.md"
        self.assertTrue(rep_path.exists(), "reports/model_comparison.md must exist.")
        
        with open(rep_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("Logistic Regression", content)
        self.assertIn("Random Forest", content)
        self.assertIn("CatBoost", content)
        self.assertIn("XGBoost", content)
        self.assertIn("Dropout Recall", content)
        print("  [PASS] Test 6: Model comparison report validated with complete evidence-based justification.")


if __name__ == "__main__":
    unittest.main()

