# Changelog

All notable changes to **mar-eval** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)  
and the project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.1] – 2025-10-23

### Added
- Unified **Annex GG Jupyter notebook** for end-to-end CHO/AUC workflows.
- **Bootstrap CI** and **bias analysis** utilities for AUC computation.
- Added **PyPI packaging support** (`pyproject.toml`, `setup.cfg`, `twine` upload ready).
- Continuous Integration (CI) via **GitHub Actions** across Python 3.9–3.12.
- **PyPI badge** added to README.
- Support for **TestPyPI** and real **PyPI** releases.

### Fixed
- CI workflow syntax and dependency issues.
- Unit test type errors in `test_mareval_basic.py`.
- Corrected import paths for `compute_auc` and `cho_decision_values`.

### Changed
- Simplified repo structure:
  - Consolidated all examples into `/examples/mar_eval_annexGG.ipynb`.
  - Updated README to reflect single unified workflow.

---

## [0.1.0] – 2025-10-21

### Added
- Initial release of **mar-eval**, the open-source toolkit for objective evaluation of **Metal Artifact Reduction (MAR)** algorithms in CT imaging.
- Core modules:
  - `cho.py` – Channelized Hotelling Observer (CHO) decision simulation.
  - `stats.py` – ROC AUC computation, confidence intervals, and bias comparison.
  - `utils.py` – Supporting math and image handling utilities.
- Example script: `/examples/synthetic_demo.py`
- Automated test suite with `pytest`.

---

**Upcoming**
- Cross-scanner validation utilities.
- Integration with DICOM MAR metadata extensions.
- Expanded model-observer templates (non-Gaussian, ROI-based).

