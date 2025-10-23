# mar-eval

![CI](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml/badge.svg)

**mar-eval** is a Python toolkit for evaluating Metal Artifact Reduction (MAR) performance in computed tomography (CT) imaging.
It implements key components described in *Annex GG* of IEC 60601-2-44 (Ed. 4 draft), including Channelized Hotelling Observer (CHO) analysis, AUC computation, statistical comparison, and bias assessment.

---

## 🚀 Installation

You can install the latest release from PyPI (or Test PyPI for experimental builds):

```bash
pip install mar-eval
```

To install the latest development version from GitHub:

```bash
pip install git+https://github.com/cdc15000/mar-eval.git
```

---

## 🧠 Overview

**mar-eval** provides utilities to support both digital and quantitative physical approaches to MAR evaluation as described in IEC 60601-2-44 Annex GG.

Core modules include:
- `mareval.cho` — Channelized Hotelling Observer analysis and model observer simulation.
- `mareval.stats` — AUC computation, ΔAUC bias, and statistical comparison.
- `mareval.utils` — Helper functions for image simulation, ROI extraction, and data organization.

---

## 📘 Examples

The `examples/` directory includes ready-to-run Jupyter notebooks demonstrating how to use **mar-eval** for Metal Artifact Reduction (MAR) performance analysis in accordance with *Annex GG* of IEC 60601-2-44 (Ed. 4 draft).  

Each notebook generates synthetic data and performs **CHO analysis**, **AUC computation**, and **ΔAUC bias assessment** using `scikit-learn` ROC utilities.

| Notebook | Description |
|-----------|--------------|
| [1_intro_to_mar_eval.ipynb](examples/1_intro_to_mar_eval.ipynb) | Quick start example — simulate images, compute AUC, visualize ROC curves |
| [2_cho_auc_analysis.ipynb](examples/2_cho_auc_analysis.ipynb) | Detailed workflow — perform CHO analysis, derive AUC distributions, and assess detectability |
| [3_bias_and_statistical_comparison.ipynb](examples/3_bias_and_statistical_comparison.ipynb) | Statistical comparison — compute ΔAUC bias and perform one-tailed significance testing |

To run them locally:

```bash
pip install jupyterlab mar-eval
jupyter lab
```

Then open any notebook from the `examples/` folder.

> 💡 You can view the notebooks online in GitHub’s built-in Jupyter viewer.

---

## 🧩 Versioning and Releases

Version tags correspond to formal document references (e.g., *Annex GG v0.1.0*).
Each release is listed in the [CHANGELOG.md](CHANGELOG.md).

---

## 🧾 Citation

If you use **mar-eval** in your research or regulatory documentation, please cite:

> Cocchiaraley, C.D. (2025). *mar-eval: Annex GG Toolkit for MAR Performance Evaluation.*  
> GitHub Repository: https://github.com/cdc15000/mar-eval

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
