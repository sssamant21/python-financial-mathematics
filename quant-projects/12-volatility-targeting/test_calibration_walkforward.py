"""Synthetic deterministic regression checks; no downloaded market data."""
import numpy as np
import pytest
from calibration_walkforward import evaluate, sensitivity


def fixture():
    return np.r_[np.linspace(-.012, .014, 80), np.linspace(-.04, .035, 80)]


def test_nonoverlap_and_training_cutoff():
    rows = evaluate(fixture(), window=20, horizon=10)
    assert rows
    assert all(x["train_end_exclusive"] == x["origin"] for x in rows)
    assert all(a["test_end_exclusive"] == b["origin"] for a,b in zip(rows, rows[1:]))


def test_future_mutation_cannot_change_first_forecast():
    r = fixture()
    baseline = evaluate(r, window=20, horizon=10)[0]
    r[20:] *= 2
    altered = evaluate(r, window=20, horizon=10)[0]
    assert altered["weight"] == baseline["weight"]
    assert altered["forecast_vol"] == baseline["forecast_vol"]


def test_zero_volatility_goes_to_cash():
    r = np.r_[np.zeros(25), np.linspace(-.01, .01, 40)]
    row = evaluate(r, window=20, horizon=5)[0]
    assert row["weight"] == row["forecast_vol"] == row["realized_vol"] == 0


def test_cost_changes_cost_not_risk_forecast():
    a = evaluate(fixture(), cost_bps=0)[0]
    b = evaluate(fixture(), cost_bps=25)[0]
    assert a["forecast_vol"] == b["forecast_vol"]
    assert b["entry_cost"] > a["entry_cost"]


def test_caps_and_seeded_determinism():
    r = fixture()
    low = evaluate(r, max_leverage=.5)
    high = evaluate(r, max_leverage=2.0)
    assert all(x["weight"] <= .5 for x in low)
    assert low == evaluate(r, max_leverage=.5)
    assert all(x["weight"] <= 2 for x in high)


def test_reject_bad_horizon_and_grid():
    with pytest.raises(ValueError):
        evaluate(fixture(), horizon=1)
    with pytest.raises(ValueError):
        evaluate(fixture(), horizon=True)
    with pytest.raises(ValueError):
        sensitivity(fixture(), leverage_caps=())


def test_sensitivity_fixed_grid():
    rows = sensitivity(fixture(), leverage_caps=(.5, 1.0), costs_bps=(0, 25))
    assert len(rows) == 4
    assert all(x["windows"] > 0 for x in rows)
