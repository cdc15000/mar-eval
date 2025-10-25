from typing import Dict, List, Tuple

def make_parameter_grid(dose_levels: List[int], contrast_levels: List[float], realizations: int,
                        recon_types: Tuple[str, ...], classes: Tuple[str, ...]) -> List[Dict]:
    grid = []
    for d in dose_levels:
        for j, _ in enumerate(contrast_levels):
            for r in range(realizations):
                for recon in recon_types:
                    for cls in classes:
                        grid.append({"dose": d, "contrast_idx": j, "realization": r, "recon": recon, "cls": cls})
    return grid

def grid_to_index(item: Dict) -> Tuple:
    return (item["dose"], item["contrast_idx"], item["realization"], item["recon"], item["cls"])