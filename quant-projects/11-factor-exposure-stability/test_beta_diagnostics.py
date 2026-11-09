import numpy as np
import pytest
from factor_lab import synthetic
from beta_diagnostics import beta_diagnostics


def test_lag_and_nonoverlap():
    rows = beta_diagnostics(*synthetic())
    assert rows and rows[0]["training_end_exclusive"] == rows[0]["origin_index"] - 2
    assert all(a["test_end_exclusive"] == b["origin_index"] for a, b in zip(rows, rows[1:]))


def test_future_mutation_cannot_change_first_estimate():
    x, y = synthetic()
    original = beta_diagnostics(x, y)
    x2, y2 = x.copy(), y.copy()
    x2[original[0]["training_end_exclusive"]:] += 100
    y2[original[0]["training_end_exclusive"]:] += 100
    changed = beta_diagnostics(x2, y2)
    for field in ("betas", "bootstrap_lower", "bootstrap_upper"):
        assert original[0][field] == changed[0][field]


def test_seeded_reproducibility():
    assert beta_diagnostics(*synthetic()) == beta_diagnostics(*synthetic())


def test_known_coefficients_and_intervals():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(180, 2))
    y = .01 + 1.2 * x[:, 0] - .4 * x[:, 1]
    row = beta_diagnostics(x, y, window=80)[0]
    assert row["betas"] == pytest.approx([1.2, -.4], abs=1e-10)
    assert row["bootstrap_lower"] == pytest.approx([1.2, -.4], abs=1e-10)
    assert row["bootstrap_upper"] == pytest.approx([1.2, -.4], abs=1e-10)


def test_drift_and_regularized_collinearity():
    x, y = synthetic()
    rows = beta_diagnostics(x, y)
    assert rows[0]["beta_drift_l2"] is None
    assert all(row["beta_drift_l2"] >= 0 for row in rows[1:])
    z = np.ones((180, 2))
    with pytest.raises(ValueError, match="rank"):
        beta_diagnostics(z, np.arange(180) / 1000)
    assert beta_diagnostics(z, np.arange(180) / 1000, ridge=1.0)


@pytest.mark.parametrize("settings", [
    {"window": 3}, {"horizon": 0}, {"release_lag": -1},
    {"draws": 2}, {"ridge": -1}, {"release_lag": True}
])
def test_invalid_settings(settings):
    with pytest.raises(ValueError):
        beta_diagnostics(*synthetic(), **settings)


def test_nonfinite_and_short_sample():
    x, y = synthetic()
    with pytest.raises(ValueError):
        beta_diagnostics(x[:20], y[:20])
    x[0, 0] = np.nan
    with pytest.raises(ValueError):
        beta_diagnostics(x, y)
