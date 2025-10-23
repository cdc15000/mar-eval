# mar-eval 🩻  
**Objective Evaluation Toolkit for Metal Artifact Reduction (MAR) Algorithms in CT Imaging**

[![mar-eval CI](https://github.com/cdc15000/mar-eval/actions/workflows/tests.yml/badge.svg)](https://github.com/cdc15000/mar-eval/actions)

`mar-eval` is an open-source Python toolkit that implements the analysis framework described in **Annex GG** of the proposed IEC 60601-2-44 Ed. 4.  
It enables objective evaluation of **Metal Artifact Reduction (MAR)** algorithms in CT imaging using the **Channelized Hotelling Observer (CHO)**, **AUC-based detectability metrics**, and **bias assessment** between MAR and non-MAR reconstructions.

---

## 🔍 Purpose

`mar-eval` supports regulatory, clinical, and technical validation of MAR performance by providing reproducible, quantitative methods for:
- Computing **Area Under the ROC Curve (AUC)** using CHO-derived decision variables  
- Performing **paired statistical comparison** of MAR vs. non-MAR detectability  
- Estimating **confidence intervals** and **ΔAUC bias**  
- Enabling interoperability across CT simulators, physical phantoms, and regulatory test environments

---

## 📘 Example Notebook

A runnable Jupyter Notebook, [`examples/mar_eval_demo.ipynb`](examples/mar_eval_demo.ipynb), walks through the full workflow described in **Annex GG**:

1. **GG.2 – Model Observer Task**  
   Simulates lesion-present and lesion-absent image sets using Gaussian statistics.  
2. **GG.3 – Data Evaluation**  
   Computes CHO decision values, ROC curves, and AUC estimates.  
3. **GG.4 – Statistical Comparison**  
   Uses a one-tailed paired t-test to detect significant improvements in detectability.  
4. **GG.5 – Bias Assessment**  
   Quantifies ΔAUC and confidence intervals to evaluate MAR-related bias.

---

## ⚙️ Installation

Install directly from [PyPI](https://pypi.org/project/mar-eval/):

```bash
pip install mar-eval
```

Or, for the latest development version:

```bash
pip install git+https://github.com/cdc15000/mar-eval.git
```

---

## 🧪 Running the Example

```bash
# Clone the repository
git clone https://github.com/cdc15000/mar-eval.git
cd mar-eval

# Install dependencies
pip install -r requirements.txt

# Launch JupyterLab
jupyter lab

# Open and run the example notebook
examples/mar_eval_demo.ipynb
```

---

## 📊 Output Example

The notebook produces AUC estimates and statistical comparison similar to:

```
AUC (no MAR): 0.484  CI: (0.423, 0.538)
AUC (with MAR): 0.504  CI: (0.445, 0.558)
ΔAUC = 0.020, p = 0.0005
```

---

## 🧩 Package Structure

```
mareval/
├── __init__.py
├── cho.py           # CHO computation routines
├── stats.py         # AUC, bias, and statistical testing
├── utils.py         # Helper utilities
examples/
└── mar_eval_demo.ipynb
tests/
└── test_mareval_basic.py
```

---

## 🧾 Citation

If you use `mar-eval` in your research, please cite:

> C.D. Cocchiaraley, *Annex GG — Objective evaluation of Metal Artifact Reduction algorithms in CT imaging*,  
> Proposed addition to IEC 60601-2-44 Ed. 4 (2025).

---

## 🪪 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions, issue reports, and pull requests are welcome.  
Please open an [issue](https://github.com/cdc15000/mar-eval/issues) or submit a PR with your proposed improvements.

---

© 2025 Christopher D. Cocchiaraley. All rights reserved.
