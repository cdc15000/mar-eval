from __future__ import annotations
from typing import Iterable, Dict, Iterator

def iter_param_grid(
    doses: Iterable[int],
    contrasts: Iterable[float],
    recon_types: Iterable[str],
    classes: Iterable[str],
) -> Iterator[Dict[str, object]]:
    """
    Iterate over a factorial grid of simulation parameters.

    Yields dicts like:
        {"dose": d, "contrast": c, "recon": r, "class": cls}
    """
    for d in doses:
        for c in contrasts:
            for r in recon_types:
                for cls in classes:
                    yield {"dose": d, "contrast": c, "recon": r, "class": cls}
