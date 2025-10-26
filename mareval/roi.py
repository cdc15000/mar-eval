import numpy as np

def extract_roi(image, center, size):
    h, w = size
    cy, cx = center
    y0 = max(0, cy - h // 2)
    x0 = max(0, cx - w // 2)
    y1 = y0 + h
    x1 = x0 + w
    return image[y0:y1, x0:x1]

def batch_extract_rois(images, centers, size):
    """Extract ROIs from a list or dict of images, returning stacked array."""
    rois = []
    # Allow both dicts and lists of images
    if isinstance(images, dict):
        images_iter = images.values()
    else:
        images_iter = images
    for img in images_iter:
        for c in centers:
            roi = extract_roi(img, c, size)
            rois.append(roi.ravel())
    return np.asarray(rois)
