"""mar-eval: Task-based evaluation toolkit for MAR in CT (Annex GG).

Exports:
- CHO pipeline utilities (channel building, decision values)
- AUC computation with bootstrap CI
- Paired one-tailed t-test and ΔAUC bias assessment
- Simulation IO helpers, ROI tools, grid helpers, reporting, visualization
"""
from .cho import (
    build_pca_channels,
    apply_channels,
    cho_template,
    cho_decision_values,
)
from .stats import (
    compute_auc,
    compute_auc_ci,
    paired_ttest_one_tailed,
    delta_auc_bias_assessment,
)
from .io_sim import (
    generate_synthetic_study,
)
from .roi import (
    extract_roi,
    batch_extract_rois,
)
from .grid import (
    make_parameter_grid,
    grid_to_index,
)
from .reporting import (
    save_auc_table_csv,
    save_delta_auc_table_csv,
)
from .viz import (
    plot_auc_heatmap,
    plot_delta_auc_heatmap,
)

__all__ = [
    # cho
    "build_pca_channels", "apply_channels", "cho_template", "cho_decision_values",
    # stats
    "compute_auc", "compute_auc_ci", "paired_ttest_one_tailed", "delta_auc_bias_assessment",
    # io / roi / grid
    "generate_synthetic_study", "extract_roi", "batch_extract_rois",
    "make_parameter_grid", "grid_to_index",
    # reporting / viz
    "save_auc_table_csv", "save_delta_auc_table_csv",
    "plot_auc_heatmap", "plot_delta_auc_heatmap",
]
