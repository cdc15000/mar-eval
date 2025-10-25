import numpy as np
from typing import Tuple, List

def extract_roi(image: np.ndarray, center: Tuple[int, int], size: Tuple[int, int]) -> np.ndarray:
    """Extract ROI (h, w) from image at center (y, x). Pads with edge values if needed."""
    h, w = size
    cy, cx = center
    y0 = max(0, cy - h//2); y1 = min(image.shape[0], y0 + h)
    x0 = max(0, cx - w//2); x1 = min(image.shape[1], x0 + w)
    roi = np.empty((h, w), dtype=image.dtype)
    roi.fill(float(image[cy, cx]))
    roi[0:(y1-y0), 0:(x1-x0)] = image[y0:y1, x0:x1]
    return roi

def batch_extract_rois(images: List[np.ndarray], centers: List[Tuple[int,int]], size: Tuple[int,int]):
    """Extract all ROIs for a list of images; returns ROIs flattened to (n, q)."""
    rois = []
    for img in images:
        for c in centers:
            r = extract_roi(img, c, size)
            rois.append(r.ravel())
    return np.asarray(rois)
