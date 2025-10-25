from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike
from typing import List, Tuple

def extract_rois(
    img: np.ndarray,
    centers: List[Tuple[int, int]],
    size: int,
) -> np.ndarray:
    """
    Extract square ROIs from a 2D image.

    Parameters
    ----------
    img : array, shape (H, W)
    centers : list of (row, col)
    size : int, ROI size (pixels). Must be odd preferred.

    Returns
    -------
    rois : array, shape (len(centers), size*size)
        Flattened ROIs (row-major).
    """
    H, W = img.shape
    r = size // 2
    out = []
    for (cy, cx) in centers:
        y0, y1 = max(0, cy - r), min(H, cy + r + 1)
        x0, x1 = max(0, cx - r), min(W, cx + r + 1)
        patch = np.zeros((size, size), dtype=float)
        sy = y1 - y0
        sx = x1 - x0
        patch[(r - (cy - y0)):(r - (cy - y0) + sy), (r - (cx - x0)):(r - (cx - x0) + sx)] = img[y0:y1, x0:x1]
        out.append(patch.reshape(-1))
    return np.stack(out, axis=0)

def extract_rois_batch(
    images: np.ndarray,
    centers: List[Tuple[int, int]],
    size: int,
) -> np.ndarray:
    """
    Extract ROIs for a batch of images.

    Parameters
    ----------
    images : array, shape (N, H, W)
    centers : list of (row, col)
    size : int

    Returns
    -------
    rois : array, shape (N*len(centers), size*size)
    """
    batches = [extract_rois(img, centers, size) for img in images]
    return np.vstack(batches)
