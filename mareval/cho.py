from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from typing import Optional, Tuple

def _pooled_covariance(X0: np.ndarray, X1: np.ndarray) -> np.ndarray:
    """Pooled (within-class) covariance."""
    X0c = X0 - X0.mean(axis=0, keepdims=True)
    X1c = X1 - X1.mean(axis=0, keepdims=True)
    n0 = max(1, X0.shape[0] - 1)
    n1 = max(1, X1.shape[0] - 1)
    S0 = (X0c.T @ X0c) / n0
    S1 = (X1c.T @ X1c) / n1
    return 0.5 * (S0 + S1)

def _reg_inv(S: np.ndarray, reg: float) -> np.ndarray:
    """Tikhonov-regularized inverse."""
    d = S.shape[0]
    return np.linalg.pinv(S + reg * np.eye(d, dtype=S.dtype))

def fit_channels_pca(roi_stack: ArrayLike, n_components: int) -> np.ndarray:
    """
    Learn a channel bank (U) via PCA on vectorized ROIs.
    Parameters
    ----------
    roi_stack : array, shape (N, q)
        N vectorized ROIs of length q.
    n_components : int
        Number of PCA components (channels).
    Returns
    -------
    U : array, shape (q, n_components)
        Orthonormal channel basis.
    """
    X = np.asarray(roi_stack, dtype=float)
    Xc = X - X.mean(axis=0, keepdims=True)
    # Economy SVD
    Ux, Sx, Vt = np.linalg.svd(Xc, full_matrices=False)
    # Principal directions are columns of V (rows of Vt)
    V = Vt.T  # shape (q, min(N,q))
    U = V[:, :n_components].copy()
    return U

def cho_decision_values(
    g0: ArrayLike,
    g1: ArrayLike,
    channels: Optional[np.ndarray] = None,
    n_pca: Optional[int] = None,
    reg: float = 1e-3,
) -> Tuple[np.ndarray, np.ndarray, dict]:
    """
    Compute CHO decision values for lesion-absent (g0) and lesion-present (g1) ROI vectors.
    This builds a channelized Hotelling template using pooled covariance and Tikhonov regularization.

    Parameters
    ----------
    g0 : array, shape (N0, q)
        Lesion-absent vectorized ROIs.
    g1 : array, shape (N1, q)
        Lesion-present vectorized ROIs.
    channels : array, shape (q, k), optional
        Channel bank (columns). If None and n_pca is given, learns channels via PCA.
        If both None, identity channels are used (k = q).
    n_pca : int, optional
        Number of PCA channels to learn if `channels` is None.
    reg : float, default 1e-3
        Tikhonov regularization parameter for pooled covariance inverse.

    Returns
    -------
    dv0 : array, shape (N0,)
        Decision values for lesion-absent samples.
    dv1 : array, shape (N1,)
        Decision values for lesion-present samples.
    info : dict
        {"w": template vector in channel space,
         "mu0": class mean in channel space,
         "mu1": class mean in channel space,
         "U": channels used, shape (q, k)}
    """
    G0 = np.asarray(g0, dtype=float)
    G1 = np.asarray(g1, dtype=float)
    N0, q = G0.shape
    N1, q1 = G1.shape
    if q1 != q:
        raise ValueError("g0 and g1 must have the same feature length.")

    if channels is None:
        if n_pca is not None:
            U = fit_channels_pca(np.vstack([G0, G1]), n_pca)
        else:
            U = np.eye(q)
    else:
        U = np.asarray(channels, dtype=float)
        if U.shape[0] != q:
            raise ValueError("channels.shape[0] must equal ROI vector length q.")

    # Project into channel space
    Z0 = G0 @ U   # (N0, k)
    Z1 = G1 @ U   # (N1, k)

    # Means
    mu0 = Z0.mean(axis=0)
    mu1 = Z1.mean(axis=0)
    delta = mu1 - mu0

    # Pooled covariance in channel space
    S = _pooled_covariance(Z0, Z1)  # (k, k)
    S_inv = _reg_inv(S, reg)

    # CHO template (Hotelling observer)
    w = S_inv @ delta  # (k,)

    # Decision values (linear template)
    dv0 = Z0 @ w
    dv1 = Z1 @ w

    info = {"w": w, "mu0": mu0, "mu1": mu1, "U": U}
    return dv0, dv1, info
