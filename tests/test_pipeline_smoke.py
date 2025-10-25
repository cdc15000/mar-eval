import numpy as np
from mareval import (
    generate_synthetic_study, extract_roi, batch_extract_rois,
    build_pca_channels, cho_template, cho_decision_values,
    compute_auc
)

def test_pipeline_smoke():
    # Tiny config to keep CI fast
    cfg = dict(
        image_shape=(32,32),
        lesion_radius_px=2,
        doses=2,
        contrasts=2,
        realizations=3,
        recon_types=["FBP","MAR"],
        classes=["absent","present"],
        base_bg_mean=1000.0,
        base_bg_std=5.0,
        dose_noise_scale=1.0,
        contrast_min=1.00,
        contrast_max=1.04,
        rng_seed=1,
    )
    study = generate_synthetic_study(cfg)
    images = study['images']
    centers = [(16, 12)]
    roi_size = (9,9)

    # small train set
    train_imgs = [images[(0,0,0,'FBP','absent')], images[(1,1,1,'MAR','present')]]
    train_rois = batch_extract_rois(train_imgs, centers, roi_size)
    U = build_pca_channels(train_rois, n_channels=4, whiten=True, random_state=0)

    # one cell, FBP present/absent
    pos = []; neg = []
    for r in range(3):
        pos.append(extract_roi(images[(0,0,r,'FBP','present')], centers[0], roi_size).ravel())
        neg.append(extract_roi(images[(0,0,r,'FBP','absent')], centers[0], roi_size).ravel())
    pos = np.asarray(pos); neg = np.asarray(neg)
    ch_pos = (pos - pos.mean(0)) @ U
    ch_neg = (neg - neg.mean(0)) @ U
    w = cho_template(ch_pos, ch_neg, lambda_reg=1e-3)
    s = np.concatenate([ch_pos @ w, ch_neg @ w])
    y = np.array([1]*len(ch_pos) + [0]*len(ch_neg))
    auc = compute_auc(s, y)
    assert 0.0 <= auc <= 1.0
