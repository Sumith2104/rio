"""
Module: evaluation.py
Project: AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Part: 2 — Student Risk Modeling
Author: Sumith U (SRN: R24EA807) | REVA University

Purpose:
    Provides rigorous, audit-grade evaluation utilities:
    - Confusion matrices and error breakdown (False Positives, False Negatives).
    - Per-class Precision, Recall, F1-score, Macro-F1, and Weighted-F1.
    - Dropout-specific sensitivity and specificity.
    - ROC-AUC and PR-AUC computation.
    - Publication-grade figure plotting for test set evaluation.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    average_precision_score,
    classification_report
)


def evaluate_model_performance(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
    is_binary: bool = True,
    target_names: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Compute comprehensive classification metrics for model evaluation.
    
    Args:
        y_true: Ground truth target labels.
        y_pred: Predicted class labels.
        y_proba: Predicted probability distribution.
        is_binary: True if binary (Dropout vs Not Dropout), False if 3-class.
        target_names: Optional class label names for display.
        
    Returns:
        dict: Detailed dictionary of computed metrics and per-class reports.
    """
    acc = float(accuracy_score(y_true, y_pred))
    
    # Macro and Weighted metrics
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true, y_pred, average="weighted", zero_division=0
    )

    # Per-class breakdown
    p_class, r_class, f1_class, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, zero_division=0
    )

    cm = confusion_matrix(y_true, y_pred).tolist()

    metrics = {
        "accuracy": round(acc, 4),
        "macro_precision": round(float(p_macro), 4),
        "macro_recall": round(float(r_macro), 4),
        "macro_f1": round(float(f1_macro), 4),
        "weighted_f1": round(float(f1_weighted), 4),
        "confusion_matrix": cm,
        "per_class": {}
    }

    labels = target_names or [f"Class_{i}" for i in range(len(p_class))]
    for i, label in enumerate(labels):
        metrics["per_class"][label] = {
            "precision": round(float(p_class[i]), 4),
            "recall": round(float(r_class[i]), 4),
            "f1": round(float(f1_class[i]), 4),
            "support": int(support[i])
        }

    # Binary specific metrics (Focusing on Dropout = Class 1)
    if is_binary and y_proba is not None:
        # y_proba for positive class (Dropout = 1)
        prob_pos = y_proba[:, 1] if y_proba.ndim > 1 else y_proba
        try:
            auc_roc = float(roc_auc_score(y_true, prob_pos))
            auc_pr = float(average_precision_score(y_true, prob_pos))
        except Exception:
            auc_roc, auc_pr = 0.0, 0.0

        # Detailed error breakdown
        # cm = [[TN, FP], [FN, TP]]
        tn, fp = cm[0][0], cm[0][1]
        fn, tp = cm[1][0], cm[1][1]

        metrics["roc_auc"] = round(auc_roc, 4)
        metrics["pr_auc"] = round(auc_pr, 4)
        metrics["dropout_recall"] = round(tp / (tp + fn) if (tp + fn) > 0 else 0.0, 4)
        metrics["dropout_precision"] = round(tp / (tp + fp) if (tp + fp) > 0 else 0.0, 4)
        metrics["false_negatives_count"] = int(fn)
        metrics["false_positives_count"] = int(fp)
        metrics["false_negative_rate"] = round(fn / (tp + fn) if (tp + fn) > 0 else 0.0, 4)
        metrics["false_positive_rate"] = round(fp / (tn + fp) if (tn + fp) > 0 else 0.0, 4)

    return metrics


def plot_all_confusion_matrices(
    models_results: Dict[str, Dict[str, Any]],
    output_path: Path,
    labels: List[str]
) -> None:
    """
    Generate side-by-side confusion matrix heatmaps for all candidate models.
    """
    n_models = len(models_results)
    fig, axes = plt.subplots(1, n_models, figsize=(5.5 * n_models, 4.5))
    if n_models == 1:
        axes = [axes]

    for ax, (model_name, res) in zip(axes, models_results.items()):
        cm = np.array(res["confusion_matrix"])
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            xticklabels=labels,
            yticklabels=labels,
            ax=ax,
            annot_kws={"size": 11, "weight": "bold"}
        )
        ax.set_title(f"{model_name}\nAcc: {res['accuracy']:.1%} | F1: {res['macro_f1']:.3f}", fontsize=11, fontweight="bold", pad=8)
        ax.set_xlabel("Predicted Outcome", fontsize=9, fontweight="bold")
        ax.set_ylabel("True Outcome", fontsize=9, fontweight="bold")

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_model_comparison_bar(
    comparison_df: pd.DataFrame,
    output_path: Path
) -> None:
    """
    Generate grouped bar charts comparing candidate model metrics.
    """
    fig, ax = plt.subplots(figsize=(10, 5.5))
    
    metrics = ["Accuracy", "Dropout Recall", "Macro F1", "ROC-AUC"]
    valid_metrics = [m for m in metrics if m in comparison_df.columns]
    
    plot_df = comparison_df.melt(id_vars=["Model"], value_vars=valid_metrics, var_name="Metric", value_name="Score")
    
    palette = ["#6366F1", "#F43F5E", "#10B981", "#06B6D4"]
    sns.barplot(data=plot_df, x="Model", y="Score", hue="Metric", palette=palette, ax=ax, edgecolor="black", linewidth=0.8)
    
    ax.set_title("Candidate Algorithm Performance Comparison on Untouched Holdout Test Set", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylim(0.5, 1.0)
    ax.set_ylabel("Score (0.0 to 1.0)", fontsize=10, fontweight="bold")
    ax.set_xlabel("Candidate Algorithm", fontsize=10, fontweight="bold")
    ax.legend(loc="lower right", framealpha=0.95)
    
    # Annotate values on bars
    for p in ax.patches:
        height = p.get_height()
        if height > 0.01:
            ax.annotate(f"{height:.2f}",
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8, rotation=0, xytext=(0, 2),
                        textcoords='offset points')

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_roc_comparison(
    models_proba: Dict[str, np.ndarray],
    y_test: np.ndarray,
    output_path: Path
) -> None:
    """
    Generate superimposed ROC curves for all candidate models on the holdout test set.
    """
    fig, ax = plt.subplots(figsize=(7.5, 6))
    
    colors = ["#6366F1", "#F59E0B", "#10B981", "#06B6D4"]
    
    for (name, proba), color in zip(models_proba.items(), colors):
        prob_pos = proba[:, 1] if proba.ndim > 1 else proba
        fpr, tpr, _ = roc_curve(y_test, prob_pos)
        auc = roc_auc_score(y_test, prob_pos)
        ax.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})", color=color, linewidth=2.2)

    ax.plot([0, 1], [0, 1], "k--", label="Random Chance Baseline (AUC = 0.500)", alpha=0.5)
    ax.set_title("ROC Curves — Binary Student Dropout Early Warning", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=10, fontweight="bold")
    ax.set_ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=10, fontweight="bold")
    ax.legend(loc="lower right", framealpha=0.95)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

