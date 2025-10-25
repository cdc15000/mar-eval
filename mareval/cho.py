import numpy as np

def build_pca_channels(rois: np.ndarray, n_channels: int = 16, whiten: bool = True, random_state: int = 0):
    """Learn a simple PCA-like channel bank from training ROIs.
    rois: shape (n_samples, q) where q is flattened ROI dimension.
    Returns U with shape (q, n_channels).
    """
    rng = np.random.default_rng(random_state)
    X = rois - rois.mean(axis=0, keepdims=True)
    # SVD for PCA
    U_svd, S, Vt = np.linalg.svd(X, full_matrices=False)
    # principal directions are Vt[:n_channels].T
    U = Vt[:n_channels].T
    if whiten:
        # scale columns by 1/sqrt(variance) ~ 1/S
        scales = (S[:n_channels] + 1e-8)
        U = U / scales
    # Orthonormalize (Gram-Schmidt-ish via QR)
    U, _ = np.linalg.qr(U)
    return U

def apply_channels(rois: np.ndarray, U: np.ndarray) -> np.ndarray:
    """Project flattened ROIs onto channel bank U (q, k) -> (n, k)."""
    return rois @ U

def cho_template(ch_pos: np.ndarray, ch_neg: np.ndarray, lambda_reg: float = 1e-3):
    """Compute CHO template using pooled covariance with Tikhonov regularization.
    ch_pos: (n_pos, k), ch_neg: (n_neg, k)
    Returns w (k,).
    """
    mu1 = ch_pos.mean(axis=0)
    mu0 = ch_neg.mean(axis=0)
    k = ch_pos.shape[1]
    X = np.vstack([ch_pos - mu1, ch_neg - mu0])
    Sigma = (X.T @ X) / max(1, (X.shape[0]-1))
    Sigma_reg = Sigma + lambda_reg * np.eye(k)
    w = np.linalg.solve(Sigma_reg, (mu1 - mu0))
    return w

def cho_decision_values(ch_samples: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Compute CHO decision values for channelized samples.
    ch_samples: (n, k), w: (k,)
    Returns: (n,)
    """
    return ch_samples @ w
