import numpy as np
import matplotlib.pyplot as plt

def _prep_axes():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    return fig, ax

def plot_auc_heatmap(auc, dose_levels=None, contrast_levels=None, title="AUC Heatmap"):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4))
    im = ax.imshow(auc, origin='lower', cmap='viridis', vmin=0.5, vmax=1.0)
    ax.set_xlabel('Contrast level')
    ax.set_ylabel('Dose level')
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label='AUC')
    plt.show()

