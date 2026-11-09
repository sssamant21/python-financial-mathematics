import numpy as np
import pytest
from risk_parity import weights_from_history, walk_forward, demo

def fixture():
    rng = np.random.default_rng(4)
    return rng.normal(0, [0.01, 0.02, 0.03], size=(130, 3))

def test_weights_sum_and_cap():
    w = weights_from_history(fixture()[:52])
    assert np.isclose(w.sum(), 1)
    assert np.all((w >= 0) & (w <= .7 + 1e-12))

def test_lower_vol_gets_higher_weight():
    w = weights_from_history(fixture()[:52])
    assert w[0] > w[1] > w[2]

def test_future_mutation_isolation():
    x = fixture()
    a = walk_forward(x)
    x[90:] *= 3
    b = walk_forward(x)
    assert np.allclose(a[0], b[0])

def test_cost_reduces_returns():
    x = fixture()
    a = walk_forward(x, cost_bps=0)
    b = walk_forward(x, cost_bps=100)
    assert np.all(b[:, 2] <= a[:, 2] + 1e-12)

def test_nonoverlapping_origins():
    out = walk_forward(fixture(), horizon=13)
    assert np.all(np.diff(out[:, 0]) == 13)

def test_seeded_demo():
    assert np.array_equal(demo(13), demo(13))

@pytest.mark.parametrize("bad", [np.ones((2,3)), np.array([[np.nan, 1]] * 5)])
def test_invalid_history(bad):
    with pytest.raises(ValueError):
        weights_from_history(bad)

def test_infeasible_cap():
    with pytest.raises(ValueError):
        weights_from_history(fixture(), cap=.2)

def test_bad_returns():
    x = fixture()
    x[0,0] = -1
    with pytest.raises(ValueError):
        walk_forward(x)
