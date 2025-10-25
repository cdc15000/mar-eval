from __future__ import annotations
import os
import csv
from typing import Dict, Iterator, Optional, List

def load_simulation_manifest(
    root: str,
    manifest_csv: str = "manifest.csv",
) -> Iterator[Dict[str, str]]:
    """
    Iterate over simulation entries described by a CSV manifest.
    The CSV should include columns like:
        path, dose, contrast, recon, class, roi_x, roi_y, roi_size, meta...
    Yields dict rows with absolute paths.

    Parameters
    ----------
    root : str
        Root directory containing the images and the manifest.
    manifest_csv : str
        CSV file name inside root.

    Yields
    ------
    row : dict
        Each row of the CSV with 'path' resolved to an absolute path.
    """
    csv_path = os.path.join(root, manifest_csv)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Manifest not found: {csv_path}")

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "path" not in row:
                raise ValueError("Manifest must contain a 'path' column.")
            row["path"] = os.path.join(root, row["path"])
            yield row
