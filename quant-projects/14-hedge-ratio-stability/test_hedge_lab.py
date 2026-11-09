import numpy as np
import pytest
from hedge_lab import hedge_ratio, walk_forward, synthetic

def test_known_beta():
    x = np.linspace(-.04, .04, 40)
    assert hedge_ratio(1.5*x, x) == pytest.approx(1.5)

def test_cap_and_negative_beta():
    x = np.linspace(-.04, .04, 40)
    assert hedge_ratio(-3*x, x, max_abs=2) == pytest.approx(-2)

def test_zero_hedge_variance_rejected():
    with pytest.raises(ValueError):
        hedge_ratio(np.arange(20), np.ones(20))

def test_nonoverlap_and_finite():
    a,b = synthetic()
    rows = walk_forward(a,b)
    assert np.all(np.diff([x["origin"] for x in rows]) == 13)
    assert all(np.isfinite(x["net_arithmetic_pnl"]) for x in rows)

def test_future_isolation():
    a,b = synthetic()
    x = walk_forward(a,b)[0]["ratio"]
    a2,b2 = a.copy(),b.copy()
    a2[52:] *= .4
    b2[52:] *= 1.3
    assert walk_forward(a2,b2)[0]["ratio"] == x

def test_cost_monotonicity():
    a,b=synthetic()
    low=walk_forward(a,b,cost_bps=0)
    high=walk_forward(a,b,cost_bps=100)
    assert all(y["net_arithmetic_pnl"] <= x["net_arithmetic_pnl"] for x,y in zip(low,high))

def test_reproducible():
    assert [(r["ratio"],r["net_arithmetic_pnl"]) for r in walk_forward(*synthetic())] == [(r["ratio"],r["net_arithmetic_pnl"]) for r in walk_forward(*synthetic())]

@pytest.mark.parametrize("bad", [dict(lookback=4),dict(horizon=0),dict(cost_bps=-1),dict(max_abs=0)])
def test_bad_controls(bad):
    with pytest.raises(ValueError):
        walk_forward(*synthetic(), **bad)

def test_bad_returns():
    a,b=synthetic()
    a[0]=np.nan
    with pytest.raises(ValueError):
        walk_forward(a,b)

def test_insufficient_history():
    with pytest.raises(ValueError):
        walk_forward(np.ones(30)*.01,np.ones(30)*.02)
