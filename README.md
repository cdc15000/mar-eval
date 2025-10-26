# mar-eval
**Toolkit for the Objective Evaluation of Metal Artifact Reduction (MAR) in CT Imaging**

[![mar-eval CI](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml/badge.svg)](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml)
[![PyPI version](https://img.shields.io/pypi/v/mar-eval.svg)](https://pypi.org/project/mar-eval/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this?

`mar-eval` is an open-source Python toolkit that implements the analysis framework described in **Annex GG** of the proposed IEC 60601-2-44 Ed. 4.  
It enables objective evaluation of **Metal Artifact Reduction (MAR)** in CT imaging using the **Channelized Hotelling Observer (CHO)**, **AUC-based detectability metrics**, and **bias assessment** between MAR and Filtered-Back Projection (FBP) reconstructions.

> The toolkit supports the **type test** use case — premarket evaluation on representative CT systems or realistic simulation outputs.

---

## Example Notebook

A full Annex GG demo is provided at:

notebooks/annex_gg_full_demo.ipynb

This notebook runs the entire workflow end-to-end: from synthetic image generation and ROI extraction to CHO analysis, AUC computation, paired t-tests, and bias evaluation. 

---

## Install

```bash
pip install mar-eval
# for notebook demo & plots:
pip install matplotlib jupyterlab pyyaml
```

Python ≥ 3.9 is supported.  
GitHub Actions tests run on 3.9 – 3.12.

---

## Quick Start (synthetic)

```python
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

train_imgs = [images[(0,0,0,'FBP','absent')], images[(2,2,0,'MAR','present')]]
train_rois = batch_extract_rois(train_imgs, centers, roi_size)
U = build_pca_channels(train_rois, n_channels=8)

pos = [extract_roi(images[(0,0,r,'FBP','present')], centers[0], roi_size).ravel() for r in range(cfg['realizations'])]
neg = [extract_roi(images[(0,0,r,'FBP','absent')], centers[0], roi_size).ravel() for r in range(cfg['realizations'])]

import numpy as np
pos = np.asarray(pos); neg = np.asarray(neg)
ch_pos = (pos - pos.mean(0)) @ U
ch_neg = (neg - neg.mean(0)) @ U
w = cho_template(ch_pos, ch_neg, lambda_reg=1e-3)

s = np.concatenate([ch_pos @ w, ch_neg @ w])
y = np.array([1]*len(ch_pos) + [0]*len(ch_neg))
res = compute_auc_ci(s, y, n_bootstrap=1000)
print(res)
```

---

## Annex GG “adult chest / spinal rod” example

- Config: `configs/adult_chest_spinal_rod.yaml`  
- Notebook: `notebooks/annex_gg_full_demo.ipynb`

The notebook executes the full flow:

1. **Load config** and generate synthetic images approximating an adult chest with a **titanium spinal rod** and an adjacent low-contrast lesion.  
2. **Preview** example slices and ROI placement.  
3. **ROI extraction** and **channel learning** (PCA).  
4. **CHO template** and **AUC computation** for each `(dose, contrast)` cell, both FBP and MAR.  
5. **Paired one-tailed t-test** and **ΔAUC bias assessment**.  
6. **Detectability curves** for AUC vs Dose and AUC vs Contrast.  
7. **CSV output tables** in `outputs/`.

> The synthetic generator produces realistic streak-like artifacts and dose-dependent noise; MAR reduces streak amplitude and adds mild smoothing.

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
  - `compute_auc(values, labels)`  
  - `compute_auc_ci(values, labels, n_bootstrap=2000)`  
  - `paired_ttest_one_tailed(a, b)`  
  - `delta_auc_bias_assessment(auc_fb, auc_mar)`
- **Simulator flow**
  - `generate_synthetic_study(cfg_dict)`
  - `extract_roi(img, center, size)` / `batch_extract_rois([...], centers, size)`
  - `make_parameter_grid(...)`
  - `save_auc_table_csv(...)`, `save_delta_auc_table_csv(...)`

---

## Citation

If you use `mar-eval` in your research, please cite:

> C.D. Cocchiaraley, *Annex GG — Objective evaluation of Metal Artifact Reduction algorithms in CT imaging*, Proposed addition to IEC 60601-2-44 Ed. 4 (2025).

---

## Versioning

- **v0.3.0** introduces the simulator workflow, unified Annex GG notebook, and detectability-curve outputs.  
- Version tags align releases with document snapshots (e.g., Annex GG draft refs).

---

## License

MIT
