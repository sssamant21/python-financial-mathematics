import numpy as np
from stock_monte_carlo import simulate, statistics

def test_paths_are_positive_and_reproducible():
    x=simulate(seed=42,days=20,paths=100)
    assert x.shape == (21,100)
    assert np.all(x > 0)
    assert np.array_equal(x,simulate(seed=42,days=20,paths=100))

def test_constant_price_with_no_drift_or_volatility():
    x=simulate(days=20,paths=100,drift=0,volatility=0)
    assert np.allclose(x,100)

def test_probability_and_tail_statistics():
    x=simulate(days=30,paths=1000)
    r=statistics(x[-1])
    assert 0 <= r["loss_probability"] <= 1
    assert r["p05_price"] <= r["median_price"] <= r["p95_price"]
    assert r["cvar95_per_share"] >= r["var95_per_share"]
