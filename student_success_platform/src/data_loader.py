"""
Module: data_loader.py
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807) | REVA University

Purpose:
    Provides reliable, robust functions to load the official UCI student dataset:
    "Predict Students' Dropout and Academic Success" (UCI ML Repository ID: 697).
    Ensures column names are cleaned, separator/encoding is verified, and summary
    statistics are generated without altering the raw dataset.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd


def get_default_data_path() -> Path:
    """Returns the default path to the raw student dataset."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / "data" / "raw" / "data.csv"


def load_student_data(filepath: Optional[Path] = None, delimiter: str = ";") -> pd.DataFrame:
    """
    Load the raw student dataset from disk into a Pandas DataFrame.
    
    Args:
        filepath: Optional path to the CSV file. Defaults to data/raw/data.csv.
        delimiter: CSV separator. Defaults to semicolon ';' as formatted by UCI.
        
    Returns:
        pd.DataFrame: Cleanly loaded DataFrame with whitespace-stripped column headers.
        
    Raises:
        FileNotFoundError: If the data file does not exist at the specified path.
        ValueError: If the file is empty or cannot be parsed.
    """
    path = filepath or get_default_data_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {path}. "
            "Please ensure data/raw/data.csv is present or run data retrieval."
        )

    # Read with UTF-8 encoding
    df = pd.read_csv(path, sep=delimiter, encoding="utf-8")

    # Clean any accidental trailing tabs or whitespace in column names
    # (The raw UCI dataset contains a trailing tab in 'Daytime/evening attendance\t')
    df.columns = [col.strip() for col in df.columns]

    return df


def get_dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate an executive structural summary of the loaded student dataset.
    
    Args:
        df: The student DataFrame.
        
    Returns:
        dict: Summary containing shape, column types, target distributions, and memory usage.
    """
    target_counts = df["Target"].value_counts().to_dict() if "Target" in df.columns else {}
    target_pct = (
        (df["Target"].value_counts(normalize=True) * 100).round(2).to_dict()
        if "Target" in df.columns
        else {}
    )

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "str"]).columns.tolist()

    return {
        "num_rows": len(df),
        "num_cols": len(df.columns),
        "column_names": list(df.columns),
        "numeric_feature_count": len(numeric_cols),
        "categorical_feature_count": len(categorical_cols),
        "target_counts": target_counts,
        "target_percentages": target_pct,
        "missing_values_total": int(df.isnull().sum().sum()),
        "duplicate_rows_total": int(df.duplicated().sum()),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
    }


if __name__ == "__main__":
    # Self-test demonstration
    data = load_student_data()
    summary = get_dataset_summary(data)
    print("=== DATASET LOADING VERIFICATION ===")
    print(f"Total Student Records: {summary['num_rows']}")
    print(f"Total Features + Target: {summary['num_cols']}")
    print(f"Target Distribution: {summary['target_counts']}")
    print(f"Target Percentages:  {summary['target_percentages']}")
    print(f"Missing Values:      {summary['missing_values_total']}")
    print(f"Duplicate Rows:      {summary['duplicate_rows_total']}")
    print(f"Memory Footprint:    {summary['memory_usage_mb']} MB")

