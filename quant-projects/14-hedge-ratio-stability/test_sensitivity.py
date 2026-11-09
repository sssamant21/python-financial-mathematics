import numpy as np
import pytest
from hedge_lab import synthetic
from sensitivity import sensitivity


def test_common_origins_and_nonoverlap():
    rows = sensitivity(*synthetic())
    origins = sorted(set(r["origin"] for r in rows))
    assert origins[0] == 78
    assert np.all(np.diff(origins) == 13)
    assert len(rows) == len(origins)*9


def test_no_future_leakage():
    a,b = synthetic()
    original = [r for r in sensitivity(a,b) if r["origin"] == 78]
    a[78:] *= 0.3
    b[78:] *= 1.4
    changed = [r for r in sensitivity(a,b) if r["origin"] == 78]
    assert [r["ratio"] for r in original] == [r["ratio"] for r in changed]


def test_full_shrinkage_zero_hedge():
    assert all(r["ratio"] == 0 for r in sensitivity(*synthetic(), shrinkages=(1.0,)))


def test_zero_shrinkage_analytic_beta():
    b = np.linspace(-0.04,0.04,120)
    a = 1.3*b
    rows = sensitivity(a,b,windows=(26,),shrinkages=(0.0,),horizon=13)
    assert all(r["ratio"] == pytest.approx(1.3) for r in rows)


def test_reproducible_and_finite():
    x = sensitivity(*synthetic())
    assert x == sensitivity(*synthetic())
    assert all(np.isfinite(r["hedged_variance"]) for r in x)


@pytest.mark.parametrize("kwargs", [
    {"windows":(4,)}, {"windows":()}, {"shrinkages":(-0.1,)},
    {"shrinkages":(1.1,)}, {"shrinkages":()}, {"horizon":1},
    {"max_abs":0}, {"windows":(500,)},
])
def test_bad_parameters(kwargs):
    with pytest.raises(ValueError):
        sensitivity(*synthetic(), **kwargs)


def test_nonfinite_rejected():
    a,b = synthetic()
    a[0] = np.nan
    with pytest.raises(ValueError):
        sensitivity(a,b)


def test_regime_labels():
    rows = sensitivity(*synthetic())
    assert {"early","late"} == {r["regime"] for r in rows}
