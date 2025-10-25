"""
mareval.stats
Statistical utilities for CHO and AUC analysis in MAR-Eval.

Implements:
- compute_auc():      Compute AUC with bootstrap confidence intervals
- compare_auc_paired(): Paired comparison of AUCs (e.g., MAR vs. FBP)
- bias_assessment():  Quantify bias between two AUC distributions

References:
- Vaishnav et al. (2020), Med Phys 47(8): “CT metal artifact reduction algorithms: Toward a framework for objective performance assessment.”
- Annex GG (IEC 60601-2-44 Ed.4 Draft): Task-based assessment of MAR algorithms
"""

import numpy as np
from sklearn.metrics import roc_auc_score
from scipy import stats


# -------------------------------------------------------------------------
# Compute AUC with bootstrap CI
# -------------------------------------------------------------------------
def compute_auc(decision_values, labels, n_bootstrap: int = 2000, random_state: int = 42):
    """
    Compute the Area Under the ROC Curve (AUC) with 95% bootstrap confidence interval.

    Parameters
    ----------
    decision_values : array-like
        Decision statistic values (e.g., CHO scores).
    labels : array-like
        Ground truth binary labels (0 = lesion-absent, 1 = lesion-present).
    n_bootstrap : int, optional
        Number of bootstrap iterations for CI estimation.
    random_state : int, optional
        Random-number seed for reproducibility.

    Returns
    -------
    dict
        {
          "auc": float,
          "ci": (float, float),
          "n_bootstrap": int
        }
    """
    labels = np.asarray(labels)
    decision_values = np.asarray(decision_values)
    rng = np.random.default_rng(random_state)

    try:
        auc = roc_auc_score(labels, decision_values)
    except ValueError:
        return {"auc": np.nan, "ci": (np.nan, np.nan), "n_bootstrap": n_bootstrap}

    # Bootstrap 95% CI
    boot = []
    n = len(labels)
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        try:
            boot_auc = roc_auc_score(labels[idx], decision_values[idx])
            boot.append(boot_auc)
        except ValueError:
            continue

    if boot:
        ci = (np.percentile(boot, 2.5), np.percentile(boot, 97.5))
    else:
        ci = (auc, auc)

    return {"auc": float(auc), "ci": tuple(map(float, ci)), "n_bootstrap": n_bootstrap}


# -------------------------------------------------------------------------
# Paired AUC comparison (MAR vs. FBP)
# -------------------------------------------------------------------------
def compare_auc_paired(auc1, auc2):
    """
    Perform paired comparison of AUCs using a one-tailed paired t-test.

    Parameters
    ----------
    auc1 : array-like
        AUC values for condition 1 (e.g., FBP).
    auc2 : array-like
        AUC values for condition 2 (e.g., MAR).

    Returns
    -------
    dict
        {
          "delta_auc": float,
          "p_value": float,
          "mean_auc1": float,
          "mean_auc2": float
        }
    """
    auc1 = np.asarray(auc1)
    auc2 = np.asarray(auc2)
    delta = auc2 - auc1
    t_stat, p_value = stats.ttest_rel(auc2, auc1, alternative="greater")

    return {
        "delta_auc": float(np.mean(delta)),
        "p_value": float(p_value),
        "mean_auc1": float(np.mean(auc1)),
        "mean_auc2": float(np.mean(auc2)),
    }


# -------------------------------------------------------------------------
# Bias assessment
# -------------------------------------------------------------------------
def bias_assessment(auc_nominal, auc_reference):
    """
    Assess bias between MAR and reference AUC values.

    Parameters
    ----------
    auc_nominal : array-like
        AUCs from MAR condition.
    auc_reference : array-like
        AUCs from FBP (reference) condition.

    Returns
    -------
    dict
        {
          "bias_mean": float,
          "bias_std": float,
          "bias_percent": float
        }
    """
    auc_nominal = np.asarray(auc_nominal)
    auc_reference = np.asarray(auc_reference)
    bias = auc_nominal - auc_reference

    bias_mean = np.mean(bias)
    bias_std = np.std(bias)
    bias_percent = 100.0 * bias_mean / np.mean(auc_reference)

    return {
        "bias_mean": float(bias_mean),
        "bias_std": float(bias_std),
        "bias_percent": float(bias_percent),
    }
