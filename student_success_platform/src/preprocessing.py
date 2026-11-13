"""
Module: preprocessing.py
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807) | REVA University

Purpose:
    Implements an anti-leakage data preprocessing pipeline using Scikit-Learn
    ColumnTransformer, Pipeline, StandardScaler, OneHotEncoder, and SimpleImputer.
    Prepares training and testing matrices for Experiment A (3-class) and
    Experiment B (binary dropout) models.
"""

from pathlib import Path
from typing import Tuple, Dict, Any
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data_loader import load_student_data


# Explicit Categorization of All 36 Input Features
CATEGORICAL_NOMINAL_COLS = [
    "Marital Status",
    "Application mode",
    "Course",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation"
]

BINARY_COLS = [
    "Daytime/evening attendance",
    "Displaced",
    "Educational special needs",
    "Debtor",
    "Tuition fees up to date",
    "Gender",
    "Scholarship holder",
    "International"
]

NUMERICAL_COLS = [
    "Application order",
    "Previous qualification (grade)",
    "Admission grade",
    "Age at enrollment",
    "Curricular units 1st sem (credited)",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (evaluations)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (without evaluations)",
    "Curricular units 2nd sem (credited)",
    "Curricular units 2nd sem (enrolled)",
    "Curricular units 2nd sem (evaluations)",
    "Curricular units 2nd sem (approved)",
    "Curricular units 2nd sem (grade)",
    "Curricular units 2nd sem (without evaluations)",
    "Unemployment rate",
    "Inflation rate",
    "GDP"
]


def build_preprocessor_pipeline() -> ColumnTransformer:
    """
    Constructs an isolated Scikit-Learn ColumnTransformer.
    - Numerical features: Mean imputation + StandardScaler (zero mean, unit variance).
    - Categorical features: Most frequent imputation + OneHotEncoder (handle_unknown='ignore').
    - Binary features: Most frequent imputation + Passthrough (already 0/1 integers).
    """
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    binary_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("passthrough", "passthrough")
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERICAL_COLS),
            ("cat", categorical_pipeline, CATEGORICAL_NOMINAL_COLS),
            ("bin", binary_pipeline, BINARY_COLS)
        ],
        remainder="drop"
    )

    return preprocessor


def create_target_splits(y_series: pd.Series) -> Tuple[pd.Series, pd.Series]:
    """
    Construct two prediction target vectors:
    - Experiment A (3-class): 'Graduate', 'Dropout', 'Enrolled' preserved as discrete classes.
    - Experiment B (Binary): 'Dropout' = 1 (Attrition), 'Enrolled'/'Graduate' = 0 (Persistent).
    """
    y_3class = y_series.copy()
    y_binary = (y_series == "Dropout").astype(int)
    return y_3class, y_binary


def run_preprocessing_pipeline(
    test_size: float = 0.20,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Executes the full anti-leakage preprocessing workflow:
    1. Loads data.csv
    2. Separates X and y
    3. Creates 80/20 stratified train/test split on raw data
    4. Fits ColumnTransformer strictly on X_train
    5. Transforms X_train and X_test
    6. Saves all processed artifacts to data/processed/
    """
    base_dir = Path(__file__).resolve().parent.parent
    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    df = load_student_data()

    # 2. Separate X and y
    X_raw = df.drop(columns=["Target"])
    y_raw = df["Target"]

    y_3class, y_binary = create_target_splits(y_raw)

    # 3. 80/20 Stratified Split
    X_train_raw, X_test_raw, y_train_3c, y_test_3c, y_train_bin, y_test_bin = train_test_split(
        X_raw,
        y_3class,
        y_binary,
        test_size=test_size,
        random_state=random_state,
        stratify=y_3class
    )

    # 4. Build and Fit Preprocessor ONLY on X_train (ANTI-LEAKAGE RULE)
    preprocessor = build_preprocessor_pipeline()
    preprocessor.fit(X_train_raw)

    # 5. Transform Train and Test splits
    X_train_proc = preprocessor.transform(X_train_raw)
    X_test_proc = preprocessor.transform(X_test_raw)

    # Retrieve transformed feature names
    feature_names = preprocessor.get_feature_names_out()

    X_train_df = pd.DataFrame(X_train_proc, columns=feature_names, index=X_train_raw.index)
    X_test_df = pd.DataFrame(X_test_proc, columns=feature_names, index=X_test_raw.index)

    # 6. Save Processed Artifacts
    X_train_df.to_csv(processed_dir / "X_train.csv", index=False)
    X_test_df.to_csv(processed_dir / "X_test.csv", index=False)
    y_train_3c.to_csv(processed_dir / "y_train_3class.csv", index=False)
    y_test_3c.to_csv(processed_dir / "y_test_3class.csv", index=False)
    y_train_bin.to_csv(processed_dir / "y_train_binary.csv", index=False)
    y_test_bin.to_csv(processed_dir / "y_test_binary.csv", index=False)

    # Save fitted preprocessor pipeline
    joblib.dump(preprocessor, processed_dir / "preprocessor.joblib")

    # Save metadata dictionary
    metadata = {
        "dataset_name": "Predict Students' Dropout and Academic Success (UCI ID: 697)",
        "total_raw_records": len(df),
        "train_records": len(X_train_df),
        "test_records": len(X_test_df),
        "raw_features_count": X_raw.shape[1],
        "processed_features_count": len(feature_names),
        "stratification_key": "Target (3-class)",
        "train_test_split_ratio": f"{int((1 - test_size) * 100)}/{int(test_size * 100)}",
        "random_state": random_state,
        "feature_names": list(feature_names),
        "class_counts_train_3class": y_train_3c.value_counts().to_dict(),
        "class_counts_test_3class": y_test_3c.value_counts().to_dict(),
        "binary_dropout_train_pct": round(float(y_train_bin.mean() * 100), 2),
        "binary_dropout_test_pct": round(float(y_test_bin.mean() * 100), 2)
    }

    with open(processed_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return metadata


if __name__ == "__main__":
    print("Running Student Data Preprocessing Pipeline...")
    meta = run_preprocessing_pipeline()
    print("=== PREPROCESSING SUCCESSFUL ===")
    print(f"Train Shape:        ({meta['train_records']}, {meta['processed_features_count']})")
    print(f"Test Shape:         ({meta['test_records']}, {meta['processed_features_count']})")
    print(f"Train 3-Class Dist: {meta['class_counts_train_3class']}")
    print(f"Test 3-Class Dist:  {meta['class_counts_test_3class']}")
    print(f"Binary Dropout %:   Train={meta['binary_dropout_train_pct']}%, Test={meta['binary_dropout_test_pct']}%")

