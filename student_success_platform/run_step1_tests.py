"""
Step 1: Automated End-to-End Verification Test Runner
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807) | REVA University

Usage:
    cd student_success_platform
    python run_step1_tests.py
"""

import sys
import unittest
from pathlib import Path
import pandas as pd
import joblib

# Add src to path
base_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(base_dir))

from src.data_loader import load_student_data, get_dataset_summary
from src.data_validation import DataValidator
from src.preprocessing import run_preprocessing_pipeline


class TestStep1EndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 75)
        print("  PART 1 END-TO-END VERIFICATION TEST SUITE")
        print("  AI-Powered Smart Campus Intelligence Platform (UCI Dataset ID: 697)")
        print("=" * 75)

    def test_01_dataset_loading_and_shape(self):
        """Test 1: Verify data.csv loads with exact expected shape and cleaned headers."""
        df = load_student_data()
        self.assertEqual(df.shape[0], 4424, "Dataset must have exactly 4,424 rows.")
        self.assertEqual(df.shape[1], 37, "Dataset must have exactly 37 columns (36 features + 1 target).")
        self.assertIn("Target", df.columns, "Target column must exist.")
        self.assertNotIn("Daytime/evening attendance\t", df.columns, "Trailing tab in column name must be stripped.")
        self.assertIn("Daytime/evening attendance", df.columns, "Cleaned column name must exist.")
        print("  [PASS] Test 1: Raw dataset loaded cleanly with shape (4,424, 37).")

    def test_02_target_distribution(self):
        """Test 2: Verify the exact distribution of Graduate, Dropout, and Enrolled classes."""
        df = load_student_data()
        summary = get_dataset_summary(df)
        counts = summary["target_counts"]
        self.assertEqual(counts["Graduate"], 2209, "Graduate count must be 2,209.")
        self.assertEqual(counts["Dropout"], 1421, "Dropout count must be 1,421.")
        self.assertEqual(counts["Enrolled"], 794, "Enrolled count must be 794.")
        print(f"  [PASS] Test 2: Target classes verified: Graduate={counts['Graduate']}, Dropout={counts['Dropout']}, Enrolled={counts['Enrolled']}.")

    def test_03_data_validation_integrity(self):
        """Test 3: Verify zero missing values, zero duplicates, and strict domain bounds."""
        df = load_student_data()
        validator = DataValidator(df)
        results = validator.run_all_validations()
        self.assertTrue(results["overall_passed"], "All validation checks must pass.")
        self.assertEqual(results["missing_values"]["total_nulls"], 0, "Missing values must be 0.")
        self.assertEqual(results["duplicate_rows"]["duplicate_count"], 0, "Duplicate rows must be 0.")
        self.assertTrue(results["age_bounds"]["passed"], "Age must fall within standard university range.")
        print("  [PASS] Test 3: Zero nulls, zero duplicates, and domain constraints fully validated.")

    def test_04_processed_splits_exist_and_match(self):
        """Test 4: Verify train/test processed matrices match 80/20 stratified proportions."""
        processed_dir = base_dir / "data" / "processed"
        x_train = pd.read_csv(processed_dir / "X_train.csv")
        x_test = pd.read_csv(processed_dir / "X_test.csv")
        
        self.assertEqual(len(x_train), 3539, "X_train must have exactly 3,539 rows (80%).")
        self.assertEqual(len(x_test), 885, "X_test must have exactly 885 rows (20%).")
        self.assertEqual(len(x_train) + len(x_test), 4424, "Total rows must equal 4,424.")
        self.assertEqual(x_train.shape[1], 236, "Processed feature dimensions must equal 236.")
        print(f"  [PASS] Test 4: 80/20 Stratified split confirmed: Train={len(x_train)}, Test={len(x_test)}, Features={x_train.shape[1]}.")

    def test_05_anti_leakage_isolation(self):
        """Test 5: Verify strict separation between X (features) and y (target)."""
        processed_dir = base_dir / "data" / "processed"
        x_train = pd.read_csv(processed_dir / "X_train.csv")
        x_test = pd.read_csv(processed_dir / "X_test.csv")

        # Ensure Target column is strictly absent from X
        self.assertNotIn("Target", x_train.columns, "Target must not leak into X_train.")
        self.assertNotIn("Target", x_test.columns, "Target must not leak into X_test.")

        # Ensure no NaN values exist in transformed matrices
        self.assertEqual(x_train.isnull().sum().sum(), 0, "Processed X_train must contain zero NaNs.")
        self.assertEqual(x_test.isnull().sum().sum(), 0, "Processed X_test must contain zero NaNs.")
        print("  [PASS] Test 5: Anti-leakage isolation verified: Target strictly excluded from feature space.")

    def test_06_target_splits_validity(self):
        """Test 6: Verify Experiment A (3-class) and Experiment B (binary) targets."""
        processed_dir = base_dir / "data" / "processed"
        y_train_3c = pd.read_csv(processed_dir / "y_train_3class.csv").squeeze("columns")
        y_test_3c = pd.read_csv(processed_dir / "y_test_3class.csv").squeeze("columns")
        y_train_bin = pd.read_csv(processed_dir / "y_train_binary.csv").squeeze("columns")
        y_test_bin = pd.read_csv(processed_dir / "y_test_binary.csv").squeeze("columns")

        # 3-class check
        self.assertEqual(set(y_train_3c.unique()), {"Graduate", "Dropout", "Enrolled"})
        self.assertEqual(set(y_test_3c.unique()), {"Graduate", "Dropout", "Enrolled"})

        # Binary check (Dropout = 1, Not Dropout = 0)
        self.assertEqual(set(y_train_bin.unique()), {0, 1})
        self.assertEqual(set(y_test_bin.unique()), {0, 1})

        # Stratification consistency check
        train_dropout_pct = (y_train_bin == 1).mean() * 100
        test_dropout_pct = (y_test_bin == 1).mean() * 100
        self.assertAlmostEqual(train_dropout_pct, test_dropout_pct, delta=0.5)
        print(f"  [PASS] Test 6: Both targets verified: 3-Class & Binary (Train Attrition: {train_dropout_pct:.2f}%, Test Attrition: {test_dropout_pct:.2f}%).")

    def test_07_preprocessor_pipeline_serialization(self):
        """Test 7: Verify serialized preprocessor pipeline can be deserialized and run inference."""
        processed_dir = base_dir / "data" / "processed"
        pipeline_path = processed_dir / "preprocessor.joblib"
        self.assertTrue(pipeline_path.exists(), "preprocessor.joblib must exist.")
        
        preprocessor = joblib.load(pipeline_path)
        df_raw = load_student_data()
        sample = df_raw.drop(columns=["Target"]).iloc[:5]
        transformed = preprocessor.transform(sample)
        
        self.assertEqual(transformed.shape, (5, 236), "Fitted pipeline must transform new samples to (5, 236).")
        print("  [PASS] Test 7: Serialized ColumnTransformer loaded and successfully transformed test sample.")


if __name__ == "__main__":
    unittest.main()

