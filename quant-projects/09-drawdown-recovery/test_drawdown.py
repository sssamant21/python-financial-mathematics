import numpy as np
import pytest
from drawdown import analyze, bootstrap_risk


def test_flat():
    a = analyze([0, 0, 0])
    assert a["max_drawdown"] == 0 and a["longest_underwater_periods"] == 0


def test_recovery():
    a = analyze([.2, -.5, 1.1, .01])
    assert a["peak_index"] == 1 and a["trough_index"] == 2 and a["recovery_index"] == 3
    assert a["max_drawdown"] == pytest.approx(.5)


def test_unrecovered():
    assert analyze([-.1, -.1])["recovery_index"] is None


def test_reproducible():
    r = np.linspace(-.03, .04, 90)
    assert bootstrap_risk(r, simulations=30, seed=3) == bootstrap_risk(r, simulations=30, seed=3)


def test_zero_returns():
    b = bootstrap_risk(np.zeros(20), horizon=12, simulations=20)
    assert b["p95_max_drawdown"] == 0


def test_invalid_returns():
    for x in ([.1], [0, -1], [0, np.nan], [[0, .1], [0, .2]]):
        with pytest.raises(ValueError):
            analyze(x)


def test_invalid_parameters():
    for opts in ({"block": 99}, {"horizon": 1}, {"simulations": 1}):
        with pytest.raises(ValueError):
            bootstrap_risk(np.zeros(10), **opts)


def test_no_input_mutation():
    x = np.linspace(-.02, .02, 30)
    y = x.copy()
    bootstrap_risk(x, simulations=20)
    np.testing.assert_array_equal(x, y)
