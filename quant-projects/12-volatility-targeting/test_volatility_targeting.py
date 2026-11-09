import numpy as np
import pytest
from volatility_targeting import run_strategy, synthetic


def test_deterministic():
    assert run_strategy(synthetic()) == run_strategy(synthetic())


def test_future_mutation_isolation():
    r = synthetic()
    original = run_strategy(r)
    r[30:] *= 2
    changed = run_strategy(r)
    assert original[0] == changed[0]
    assert original[10]["weight"] == changed[10]["weight"]


def test_nonoverlap_and_caps():
    rows = run_strategy(synthetic(), window=30, max_leverage=1.2)
    assert len(rows) == 330
    assert all(z["training_end_exclusive"] == z["index"] for z in rows)
    assert all(0 <= z["weight"] <= 1.2 for z in rows)


def test_cost_accounting():
    rows = run_strategy(synthetic(), cost_bps=25)
    assert all(z["net_return"] == pytest.approx(z["gross_return"] - z["cost"]) for z in rows)
    assert rows[0]["turnover"] == pytest.approx(rows[0]["weight"])
    assert rows[0]["cost"] == pytest.approx(rows[0]["weight"] * .0025)


def test_zero_volatility_stays_in_cash():
    rows = run_strategy(np.zeros(40))
    assert all(z["weight"] == 0 and z["net_return"] == 0 for z in rows)


@pytest.mark.parametrize("kwargs", [
    {"window": 2}, {"window": True}, {"target_vol": 0},
    {"max_leverage": -1}, {"cost_bps": -1}, {"periods_per_year": 0},
    {"cost_bps": float("nan")}
])
def test_invalid_settings(kwargs):
    with pytest.raises(ValueError):
        run_strategy(synthetic(), **kwargs)


def test_bad_returns():
    for data in ([0, 1], [0.0] * 40 + [np.nan], [0.0] * 40 + [-1.0]):
        with pytest.raises(ValueError):
            run_strategy(data)
