# Changelog

All notable changes to **mar-eval** will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)  
and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] – 2025-10-25
### Added
- **Simulator workflow** for evaluating Metal Artifact Reduction (MAR) using realistic dose/contrast grids.
- **Unified Annex GG demonstration notebook** (`notebooks/annex_gg_full_demo.ipynb`) illustrating the full evaluation pipeline for the *adult chest with titanium spinal rod* scenario.
- **New modules**:
  - `io_sim.py` – handles loading and organization of simulator-generated image sets (e.g., DukeSim).
  - `roi.py` – extraction utilities for lesion-present and lesion-absent regions of interest.
  - `grid.py` – parameter grid builder for dose/contrast/realization/reconstruction/class combinations.
  - `reporting.py` – structured export of AUC, ΔAUC, and bias-assessment tables.
  - `viz.py` – plotting utilities for AUC and ΔAUC heatmaps.
- **Configuration system** (`configs/adult_chest_spinal_rod.yaml`) to define test scenarios.
- **Smoke-test coverage** (`tests/test_pipeline_smoke.py`) verifying pipeline functionality with synthetic data.
- CI now runs across **Python 3.9–3.12** on GitHub Actions.

### Changed
- Refactored core modules (`cho.py`, `stats.py`) for clarity and extensibility.
- Extended README to document the simulator-based evaluation workflow and unified Annex GG notebook.
- Updated project metadata (`pyproject.toml`) to explicitly package only the `mareval` module.

### Fixed
- Stabilized AUC and CI computation for reproducible statistical comparisons.
- Corrected import paths to prevent namespace conflicts.

---

## [0.2.0] – 2025-10-20
### Added
- Initial public release of **mar-eval** on PyPI.
- Implemented core CHO and AUC analysis for Annex GG framework.
- Added automated CI testing across Python 3.9–3.12.
- Published example notebooks and documentation.

---

## [0.1.0] – 2025-10-18
### Added
- Prototype toolkit implementing CHO, AUC computation, and statistical comparison for MAR algorithms.

---

**Author:** Christopher D. Cocchiaraley  
**License:** MIT  
**Repository:** [https://github.com/cdc15000/mar-eval](https://github.com/cdc15000/mar-eval)
