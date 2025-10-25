"""
mar-eval: Metal Artifact Reduction evaluation toolkit (Annex GG oriented)

Public API
----------
Core CHO / AUC / stats:
    - cho_decision_values
    - fit_channels_pca
    - compute_auc
    - compute_auc_ci
    - compare_auc_paired
    - bias_assessment

ROI & data I/O:
    - extract_rois
    - extract_rois_batch
    - load_simulation_manifest
    - iter_param_grid

Visualization & reporting:
    - plot_roc
    - plot_score_hist
    - make_results_report
"""

from .cho import (
    cho_decision_values,
    fit_channels_pca,
)

from .stats import (
    compute_auc,
    compute_auc_ci,
    compare_auc_paired,
    bias_assessment,
)

from .roi import (
    extract_rois,
    extract_rois_batch,
)

from .io_sim import (
    load_simulation_manifest,
)

from .grid import (
    iter_param_grid,
)

from .viz import (
    plot_roc,
    plot_score_hist,
)

from .reporting import (
    make_results_report,
)

__all__ = [
    # CHO
    "cho_decision_values",
    "fit_channels_pca",
    # Stats
    "compute_auc",
    "compute_auc_ci",
    "compare_auc_paired",
    "bias_assessment",
    # ROI / I/O / grid
    "extract_rois",
    "extract_rois_batch",
    "load_simulation_manifest",
    "iter_param_grid",
    # Viz / reporting
    "plot_roc",
    "plot_score_hist",
    "make_results_report",
]
