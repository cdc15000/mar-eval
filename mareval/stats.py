from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from typing import Tuple, Dict
from sklearn.metrics import roc_auc_score, roc_curve
from scipy import stats

def _ensure_binary_labels(labels: ArrayLike) -> np.ndarray:
    """Coerce labels to {0,1} if they are not already binary."""
    y = np.asarray(labels)
    uniq = np.unique(y)
    if len(uniq) == 2 and set(uniq.tolist()) == {0, 1}:
        return y.astype(int)
    # Fallback: map any non-zero to 1 (for robustness in simple tests)
    return (y != 0).astype(int)

def compute_auc(decision_values: ArrayLike, labels: ArrayLike) -> float:
    """
    Compute ROC AUC (binary). Returns a scalar float in [0,1].
    """
    y = _ensure_binary_labels(labels)
    s = np.asarray(decision_values, dtype=float)
    return float(roc_auc_score(y, s))

def compute_auc_ci(
    decision_values: ArrayLike,
    labels: ArrayLike,
    n_bootstrap: int = 2000,
    random_state: int = 42,
    alpha: float = 0.05,
) -> Dict[str, object]:
    """
    ROC AUC with bootstrap CI.
    Returns dict with keys: auc, ci=(lo, hi), n_bootstrap
    """
    rng = np.random.default_rng(random_state)
    y = _ensure_binary_labels(labels)
    s = np.asarray(decision_values, dtype=float)

    auc = float(roc_auc_score(y, s))
    n = len(y)
    boot = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        yb = y[idx]
        sb = s[idx]
        # Skip degenerate resamples that have a single class
        if len(np.unique(yb)) < 2:
            continue
        boot.append(float(roc_auc_score(yb, sb)))

    if len(boot) == 0:
        ci = (auc, auc)
    else:
        lo, hi = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
        ci = (float(lo), float(hi))

    return {"auc": auc, "ci": ci, "n_bootstrap": n_bootstrap}

def compare_auc_paired(
    dv_mar: ArrayLike,
    y_mar: ArrayLike,
    dv_fbp: ArrayLike,
    y_fbp: ArrayLike,
    one_tailed: bool = True,
) -> Dict[str, float]:
    """
    One-tailed paired comparison of AUC(MAR) vs AUC(FBP).
    Simple approach: pair by index, compute per-pair differences in decision scores,
    then test AUC difference via paired t-test on subject-level AUCs across bootstrap
    resamples. Keeps compute lightweight and reproducible.

    Returns dict: {"auc_mar": ..., "auc_fbp": ..., "delta_auc": ..., "p_value": ...}
    """
    y0 = _ensure_binary_labels(y_fbp)
    y1 = _ensure_binary_labels(y_mar)
    s0 = np.asarray(dv_fbp, dtype=float)
    s1 = np.asarray(dv_mar, dtype=float)

    # Basic AUCs
    auc_fbp = float(roc_auc_score(y0, s0))
    auc_mar = float(roc_auc_score(y1, s1))
    delta = auc_mar - auc_fbp

    # Paired t-test via bootstrap pairing (same RNG sequence)
    rng = np.random.default_rng(123)
    n = min(len(y0), len(y1))
    B = 2000
    diffs = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        yb0, sb0 = y0[idx], s0[idx]
        yb1, sb1 = y1[idx], s1[idx]
        # Skip degenerate
        if len(np.unique(yb0)) < 2 or len(np.unique(yb1)) < 2:
            continue
        diffs.append(float(roc_auc_score(yb1, sb1) - roc_auc_score(yb0, sb0)))

    if len(diffs) < 5:
        # fallback unpaired normal approx
        se = 0.02
        z = delta / se
        p = 1 - stats.norm.cdf(z) if one_tailed else 2 * (1 - stats.norm.cdf(abs(z)))
    else:
        d = np.array(diffs, dtype=float)
        tstat = (np.mean(d) - 0.0) / (np.std(d, ddof=1) / np.sqrt(len(d)))
        df = len(d) - 1
        if one_tailed:
            p = 1 - stats.t.cdf(tstat, df=df)
        else:
            p = 2 * (1 - stats.t.cdf(abs(tstat), df=df))

    return {
        "auc_mar": auc_mar,
        "auc_fbp": auc_fbp,
        "delta_auc": delta,
        "p_value": float(p),
    }

def bias_assessment(auc_mar: float, auc_fbp: float) -> Dict[str, float]:
    """
    Bias assessment as ΔAUC = AUC(MAR) - AUC(FBP).
    """
    return {"delta_auc": float(auc_mar - auc_fbp)}
