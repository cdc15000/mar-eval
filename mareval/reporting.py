from __future__ import annotations
from typing import Dict, Any, List
import json

def make_results_report(
    auc_mar: float,
    auc_fbp: float,
    delta_auc: float,
    p_value: float,
    meta: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Produce a JSON-friendly results record for Annex GG-style reporting.
    """
    return {
        "analysis": {
            "auc_mar": float(auc_mar),
            "auc_fbp": float(auc_fbp),
            "delta_auc": float(delta_auc),
            "p_value_one_tailed": float(p_value),
        },
        "metadata": dict(meta),
    }

def dump_report_json(path: str, report: Dict[str, Any]) -> None:
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
