import numpy as np
import matplotlib.pyplot as plt

def _prep_axes():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    return fig, ax

def plot_auc_heatmap(auc_grid: np.ndarray, dose_levels, contrast_levels, title: str = "AUC Heatmap"):
    fig, ax = _prep_axes()
    im = ax.imshow(auc_grid, aspect="auto")
    ax.set_title(title)
    ax.set_xlabel("contrast index (low→high)")
    ax.set_ylabel("dose index (low→high)")
    ax.set_yticks(range(len(dose_levels)))
    ax.set_xticks(range(len(contrast_levels)))
    return fig, ax

def plot_delta_auc_heatmap(delta_grid: np.ndarray, dose_levels, contrast_levels, title: str = "ΔAUC Heatmap"):
    fig, ax = _prep_axes()
    im = ax.imshow(delta_grid, aspect="auto")
    ax.set_title(title)
    ax.set_xlabel("contrast index (low→high)")
    ax.set_ylabel("dose index (low→high)")
    ax.set_yticks(range(len(dose_levels)))
    ax.set_xticks(range(len(contrast_levels)))
    return fig, ax
