from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from typing import Optional, Tuple
from sklearn.metrics import roc_curve, roc_auc_score

def _import_mpl():
    import matplotlib.pyplot as plt  # lazy import
    return plt

def plot_roc(
    decision_values: ArrayLike,
    labels: ArrayLike,
    ax=None,
    label: Optional[str] = None,
):
    """
    Plot ROC curve for binary labels.
    """
    plt = _import_mpl()
    y = np.asarray(labels)
    s = np.asarray(decision_values, dtype=float)
    fpr, tpr, _ = roc_curve(y, s)
    auc = roc_auc_score(y, s)
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(fpr, tpr, lw=2, label=(label or "ROC") + f" (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], lw=1, linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC")
    ax.legend()
    return ax

def plot_score_hist(
    scores0: ArrayLike,
    scores1: ArrayLike,
    bins: int = 30,
    ax=None,
    labels: Tuple[str, str] = ("Absent", "Present"),
):
    """
    Histogram of decision values for absent/present classes.
    """
    plt = _import_mpl()
    s0 = np.asarray(scores0, dtype=float)
    s1 = np.asarray(scores1, dtype=float)
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist(s0, bins=bins, alpha=0.6, density=True, label=labels[0])
    ax.hist(s1, bins=bins, alpha=0.6, density=True, label=labels[1])
    ax.set_xlabel("Decision value")
    ax.set_ylabel("Density")
    ax.set_title("CHO decision distributions")
    ax.legend()
    return ax
