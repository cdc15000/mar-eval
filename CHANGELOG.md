# Changelog

All notable changes to **mar-eval** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
### Added
- Planned integration of additional model observer options (NPWE, IO, etc.)
- Expanded dataset utilities for CT simulator interoperability

---

## [0.2.0] – 2025-10-23
### Added
- Example Jupyter notebooks demonstrating CHO workflow and AUC computation
- ΔAUC bias evaluation demo comparing MAR vs. non-MAR images
- CI test matrix for Python 3.9–3.12 on GitHub Actions
- Full README with usage examples and project badges

### Changed
- Updated `pyproject.toml` and `__init__.py` for version 0.2.0
- Improved test coverage and documentation comments

### Fixed
- Minor import-path issue in tests during CI
- Improved numerical stability in CHO covariance estimation

---

## [0.1.0] – 2025-10-22
### Added
- Initial public release of **mar-eval**  
  Toolkit implementing the Annex GG framework for:
  - Channelized Hotelling Observer (CHO) analysis  
  - AUC computation  
  - Statistical comparison (paired one-tailed t-test)  
  - ΔAUC bias assessment

- Packaged and distributed via TestPyPI for validation
- Integrated GitHub Actions CI with automated multi-version testing
- Published under MIT License

---

## Links
- **Repository:** [https://github.com/cdc15000/mar-eval](https://github.com/cdc15000/mar-eval)
- **PyPI:** [https://pypi.org/project/mar-eval/](https://pypi.org/project/mar-eval/)

