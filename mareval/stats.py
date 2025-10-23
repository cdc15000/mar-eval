import numpy as np
from sklearn.metrics import roc_auc_score
import warnings

def compute_auc(decision_values, labels, n_bootstrap: int = 2000, random_state: int = 42):
    """
    Compute the Area Under the ROC Curve (AUC) with 95% confidence interval.
    """
    decision_values = np.asarray(decision_values)
    labels = np.asarray(labels)

    rng = np.random.default_rng(random_state)
    auc = roc_auc_score(labels, decision_values)

    boot = []
    n = len(labels)
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        sample_labels = labels[idx]
        sample_values = decision_values[idx]

        # Skip resamples that contain only one class
        if len(np.unique(sample_labels)) < 2:
            continue

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            try:
                boot_auc = roc_auc_score(sample_labels, sample_values)
                boot.append(boot_auc)
            except ValueError:
                continue

    ci = (np.percentile(boot, 2.5), np.percentile(boot, 97.5)) if boot else (auc, auc)
    return {"auc": auc, "ci": ci, "n_bootstrap": len(boot)}


def compare_auc(decision_values_mar, decision_values_nomar, labels):
    """
    Compare AUC values (with vs without MAR) and compute ΔAUC and one-tailed paired t-test.

    Parameters
    ----------
    decision_values_mar : np.ndarray
        Decision values from MAR-processed images.
    decision_values_nomar : np.ndarray
        Decision values from non-MAR images.
    labels : np.ndarray
        Binary lesion labels (same for both sets).

    Returns
    -------
    comparison : dict
        {
          "auc_mar": float,
          "auc_nomar": float,
          "delta_auc": float,
          "p_value": float
        }
    """
    auc_mar = roc_auc_score(labels, decision_values_mar)
    auc_nomar = roc_auc_score(labels, decision_values_nomar)
    delta_auc = auc_mar - auc_nomar

    # Compute paired one-tailed t-test across image-pair AUC estimates
    diffs = decision_values_mar - decision_values_nomar
    t_stat, p_two = stats.ttest_rel(decision_values_mar, decision_values_nomar)
    p_one = p_two / 2 if t_stat > 0 else 1 - (p_two / 2)

    return {
        "auc_mar": auc_mar,
        "auc_nomar": auc_nomar,
        "delta_auc": delta_auc,
        "p_value": p_one
    }
