# mar-eval

Task-based evaluation toolkit for **Metal Artifact Reduction (MAR)** in CT imaging, aligned with the **Annex GG** framework.

[![CI](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml/badge.svg)](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/mar-eval.svg)](https://pypi.org/project/mar-eval/)

---

## What is this?

**mar-eval** implements a pragmatic, reproducible pipeline for MAR performance assessment using a **Channelized Hotelling Observer (CHO)**, **AUC** computation (with bootstrap CI), **one‑tailed paired t‑tests**, and **ΔAUC bias assessment**. It supports:

- **Simulator-driven inputs** (e.g., DukeSim) via a YAML config + loader that organizes the (dose, contrast, realization, recon, class) grid prescribed in Annex GG.
- **ROI‑based CHO** with PCA-derived channels and pooled covariance (with small Tikhonov regularization).
- Clean **reporting helpers** (CSV tables) and **matplotlib** visualizations (AUC and ΔAUC heatmaps).
- A runnable **unified notebook** that mirrors Annex GG end‑to‑end for the **adult chest with titanium spinal rod** example.

> The toolkit focuses on the **type test** use case, i.e., premarket evaluation on representative systems and validated phantoms or realistic simulation outputs.

---

## Install

```bash
pip install mar-eval
# for notebook demo & plots you may also want:
pip install matplotlib jupyterlab pyyaml
```

Python ≥ 3.9 is supported.

---

## Quick start (synthetic)

```python
import numpy as np
from mareval import (
    generate_synthetic_study, extract_roi, batch_extract_rois,
    build_pca_channels, cho_template, cho_decision_values,
    compute_auc_ci
)

cfg = dict(image_shape=(64,64), doses=3, contrasts=3, realizations=4, rng_seed=0)
study = generate_synthetic_study(cfg)
images = study["images"]
centers = [(32, 24)]
roi_size = (17,17)

# simple training set for channels
train_imgs = [images[(0,0,0,'FBP','absent')], images[(2,2,0,'MAR','present')]]
train_rois = batch_extract_rois(train_imgs, centers, roi_size)
U = build_pca_channels(train_rois, n_channels=8)

# one cell AUC (FBP)
pos = []; neg = []
for r in range(cfg['realizations']):
    pos.append(extract_roi(images[(0,0,r,'FBP','present')], centers[0], roi_size).ravel())
    neg.append(extract_roi(images[(0,0,r,'FBP','absent')], centers[0], roi_size).ravel())

import numpy as np
pos = np.asarray(pos); neg = np.asarray(neg)
ch_pos = (pos - pos.mean(0)) @ U
ch_neg = (neg - neg.mean(0)) @ U
w = cho_template(ch_pos, ch_neg, lambda_reg=1e-3)

s = np.concatenate([ch_pos @ w, ch_neg @ w])
y = np.array([1]*len(ch_pos) + [0]*len(ch_neg))
res = compute_auc_ci(s, y, n_bootstrap=1000)
print(res)  # {'auc': ..., 'ci': (..., ...), 'n_bootstrap': 1000}
```

---

## Annex GG “adult chest / spinal rod” example

- Config: `configs/adult_chest_spinal_rod.yaml`
- Notebook: `notebooks/annex_gg_full_demo.ipynb`

The notebook executes the full flow:

1. **Load config** and generate synthetic images approximating an adult chest with a **6 mm titanium rod** and a **5 mm lesion** adjacent to the rod centerline.
2. **Preview** grid counts and an example slice.
3. **ROI extraction** and **channel learning** (PCA).
4. **CHO template** + **AUC per (dose, contrast)** for both **FBP** and **MAR**.
5. **Paired one‑tailed t‑test** and **ΔAUC bias assessment**.
6. **Heatmaps** for AUC and ΔAUC.
7. **CSV tables** (Annex‑GG‑style) in `outputs/`.

> The synthetic generator produces realistic streak‑like artifacts and dose‑dependent noise; MAR reduces streak amplitude and introduces mild smoothing.

---

## API Highlights

```python
from mareval import (
  build_pca_channels, cho_template, cho_decision_values,
  compute_auc, compute_auc_ci, paired_ttest_one_tailed, delta_auc_bias_assessment,
  generate_synthetic_study, extract_roi, batch_extract_rois,
  make_parameter_grid, save_auc_table_csv, save_delta_auc_table_csv
)
```

- **CHO**
  - `build_pca_channels(rois, n_channels=16, whiten=True)`
  - `cho_template(ch_pos, ch_neg, lambda_reg=1e-3)`
  - `cho_decision_values(ch_samples, w)`
- **AUC & Stats**
  - `compute_auc(values, labels) -> float`
  - `compute_auc_ci(values, labels, n_bootstrap=2000) -> dict`
  - `paired_ttest_one_tailed(a, b) -> (delta_mean, p_one)`
  - `delta_auc_bias_assessment(auc_fb, auc_mar) -> dict`
- **Simulator flow**
  - `generate_synthetic_study(cfg_dict)`
  - `extract_roi(img, center, size)` / `batch_extract_rois([...], centers, size)`
  - `make_parameter_grid(...)`
  - `save_auc_table_csv(...)`, `save_delta_auc_table_csv(...)`

---

## Tests / CI

A light **smoke test** covers the end‑to‑end pipeline on a tiny synthetic set:

```
pytest -q
```

GitHub Actions runs the tests across 3.9–3.12.

---

## Versioning

- This update introduces **v0.3.0** with simulator workflow, unified Annex‑GG notebook, and reporting/visualization helpers.
- Version tags are used to align releases with document snapshots (e.g., Annex‑GG draft refs).

---

## License

MIT
