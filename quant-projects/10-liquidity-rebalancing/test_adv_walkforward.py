import importlib.util
from pathlib import Path
import numpy as np
import pytest

spec = importlib.util.spec_from_file_location("adv_walkforward", Path(__file__).with_name("adv_walkforward.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    return np.full((30, 2), [10., 20.]), np.full((30, 2), [100., 100.])


def test_nonoverlap():
    p, v = fixture()
    rows = m.evaluate(p, v, [100, -100], 10, 5, stress_factors=(1,))
    assert [(r["origin_index"], r["test_end_exclusive"]) for r in rows] == [(10, 15), (15, 20), (20, 25), (25, 30)]


def test_train_only_future_mutation():
    p, v = fixture()
    first = m.evaluate(p, v, [100, -100], 10, 5, stress_factors=(1,))[0]
    v[10:] *= .1
    changed = m.evaluate(p, v, [100, -100], 10, 5, stress_factors=(1,))[0]
    assert first["forecast_adv_dollars"] == changed["forecast_adv_dollars"]
    assert first["realized_adv_dollars"] != changed["realized_adv_dollars"]


def test_lag_and_arithmetic():
    p, v = fixture()
    v[9] = [200, 200]
    row = m.evaluate(p, v, [100, -100], 10, 5, stress_factors=(1,))[0]
    assert row["forecast_adv_dollars"] == pytest.approx([1100, 2200])
    assert row["forecast_max_days"] == pytest.approx(100 / 110)


def test_stress_monotone():
    p, v = fixture()
    rows = m.evaluate(p, v, [100, -100], 10, 5, stress_factors=(1, .5, .25))[:3]
    assert [r["forecast_max_days"] for r in rows] == pytest.approx([1, 2, 4])


def test_shock_flags_underestimate():
    p, v = fixture()
    v[10:15] *= .1
    assert m.evaluate(p, v, [100, -100], 10, 5, stress_factors=(1,))[0]["underestimated_capacity_days"]


def test_zero_trade():
    p, v = fixture()
    assert m.evaluate(p, v, [0, 0], 10, 5)[0]["forecast_max_days"] == 0


def test_deterministic_demo():
    assert m.demo() == m.demo()


@pytest.mark.parametrize("change", [
    lambda p,v,q,k: (p[:10],v[:10],q,k),
    lambda p,v,q,k: (p,v[:,:1],q,k),
    lambda p,v,q,k: (p,v,[1],k),
    lambda p,v,q,k: (p,v*0,q,k),
    lambda p,v,q,k: (p*np.nan,v,q,k),
    lambda p,v,q,k: (p,v,[np.inf,1],k),
    lambda p,v,q,k: (p,v,q,0),
    lambda p,v,q,k: (p,v,q,True),
])
def test_invalid(change):
    p, v = fixture()
    p, v, q, k = change(p, v, [100, -100], 10)
    with pytest.raises(ValueError):
        m.evaluate(p, v, q, window=k)


def test_invalid_stress():
    p, v = fixture()
    for f in [(0,), (1.1,), (np.nan,), ()]:
        with pytest.raises(ValueError):
            m.evaluate(p, v, [100, -100], stress_factors=f)
