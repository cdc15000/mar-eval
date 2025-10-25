from mareval import compute_auc


def test_auc_range():
    """Test that compute_auc returns a valid AUC (and optional CI)."""
    labels = [0, 1, 0, 1]
    decision_values = [0.1, 0.9, 0.4, 0.8]
    result = compute_auc(decision_values, labels)

    # Support both dictionary or float return types
    if isinstance(result, dict):
        auc = result.get("auc", None)
        ci = result.get("ci", None)
    else:
        auc = result
        ci = None

    # Validate AUC range
    assert auc is not None, "AUC value should not be None"
    assert 0.0 <= auc <= 1.0, f"AUC out of range: {auc}"

    # If CI is returned, ensure it’s a tuple of two floats
    if ci is not None:
        assert isinstance(ci, tuple), "CI should be a tuple"
        assert len(ci) == 2, "CI should have two elements"
        assert all(isinstance(x, (float, int)) for x in ci), "CI values must be numeric"
