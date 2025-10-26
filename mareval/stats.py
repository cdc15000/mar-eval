import numpy as np
from sklearn.metrics import roc_auc_score
from scipy import stats as spstats

def compute_auc(decision_values, labels, n_bootstrap: int = 0, random_state: int = 42):
    """Compute ROC AUC. If n_bootstrap>0, return dict with CI; else float."""
    y = np.asarray(labels)
    s = np.asarray(decision_values)
    auc = float(roc_auc_score(y, s))
    if n_bootstrap and n_bootstrap > 0:
        return compute_auc_ci(s, y, n_bootstrap=n_bootstrap, random_state=random_state)
    return auc

def compute_auc_ci(decision_values, labels, n_bootstrap: int = 2000, random_state: int = 42):
    """Return dict: {'auc': float, 'ci': (lo, hi), 'n_bootstrap': int}"""
    y = np.asarray(labels)
    s = np.asarray(decision_values)
    rng = np.random.default_rng(random_state)
    auc = float(roc_auc_score(y, s))

    boot = []
    n = len(y)
    for _ in range(n_bootstrap):
        idx = rng.integers(0, n, n)
        yy = y[idx]
        ss = s[idx]
        # Only compute when both classes present
        if yy.min() != yy.max():
            try:
                boot.append(float(roc_auc_score(yy, ss)))
            except Exception:
                continue
    if len(boot) == 0:
        lo = hi = auc
    else:
        lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"auc": auc, "ci": (float(lo), float(hi)), "n_bootstrap": n_bootstrap}

def paired_ttest_one_tailed(values_a, values_b):
    """Paired one-tailed t-test: H1: mean(b - a) > 0. Returns (delta_mean, p)."""
    a = np.asarray(values_a, dtype=float)
    b = np.asarray(values_b, dtype=float)
    diffs = b - a
    t_stat, p_two = spstats.ttest_rel(b, a, nan_policy='omit')
    # one-tailed p (improvement)
    p_one = p_two / 2.0 if t_stat > 0 else 1.0 - (p_two / 2.0)
    return float(diffs.mean()), float(p_one)

def delta_auc_bias_assessment(auc_fb, auc_mar):
    """Compute ΔAUC and label bias status for scalar or array inputs."""
    auc_fb = np.asarray(auc_fb)
    auc_mar = np.asarray(auc_mar)
    delta = np.mean(auc_mar - auc_fb)
    status = "improved" if delta > 0 else ("worse" if delta < 0 else "no_change")
    return {"delta_auc": float(delta), "status": status}

