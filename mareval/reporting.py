import csv
from typing import List

def save_auc_table_csv(path: str, dose_levels: List[int], contrast_levels: List[float], auc_grid_mar, auc_grid_fbp):
    """Write CSV table with AUC per (dose, contrast) for MAR and FBP."""
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        header = ["dose \\ contrast"] + [f"c{j}" for j in range(len(contrast_levels))]
        w.writerow(header)
        for i, d in enumerate(dose_levels):
            row = [f"d{d}"]
            for j in range(len(contrast_levels)):
                row.append(f"MAR={auc_grid_mar[i,j]:.3f};FBP={auc_grid_fbp[i,j]:.3f}")
            w.writerow(row)

def save_delta_auc_table_csv(path: str, dose_levels: List[int], contrast_levels: List[float], delta_auc_grid):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        header = ["dose \\ contrast"] + [f"c{j}" for j in range(len(contrast_levels))]
        w.writerow(header)
        for i, d in enumerate(dose_levels):
            row = [f"d{d}"]
            for j in range(len(contrast_levels)):
                row.append(f"{delta_auc_grid[i,j]:.3f}")
            w.writerow(row)
