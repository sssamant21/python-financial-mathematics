"""Deterministic synthetic regression checks for prequential calibration."""
import numpy as np
import pytest
from calibration import calibrate


def fixture():
    prices = np.full((90, 2), [100., 50.])
    volumes = np.full((90, 2), [10000., 20000.])
    volumes[55:] *= 0.3
    return prices, volumes, [20000., -20000.]


def test_warmup_and_nonoverlap():
    rows = calibrate(*fixture(), window=10, horizon=5, min_history=3)
    assert len(rows) == 16
    assert [r["covered"] for r in rows[:3]] == [None] * 3
    assert all(r["origin_index"] == 10 + i*5 for i, r in enumerate(rows))
    assert all(r["test_end_exclusive"] == r["origin_index"] + 5 for r in rows)


def test_future_mutation_does_not_change_earlier_forecasts():
    p, v, q = fixture()
    a = calibrate(p, v, q, window=10, horizon=5)
    changed = v.copy()
    changed[60:] *= 0.01
    b = calibrate(p, changed, q, window=10, horizon=5)
    assert a[:10] == b[:10]


def test_constant_volume_exact_coverage():
    p, v, q = fixture()
    v[:] = 10000.
    rows = calibrate(p, v, q, window=10, horizon=5)
    assert all(r["covered"] is True for r in rows[3:])
    assert all(r["upper_multiplier"] == pytest.approx(1) for r in rows[3:])


@pytest.mark.parametrize("alpha,min_history", [(0, 3), (1, 3), (float("nan"), 3),
                                                  (0.1, 1), (0.1, True)])
def test_reject_bad_configuration(alpha, min_history):
    with pytest.raises(ValueError):
        calibrate(*fixture(), alpha=alpha, min_history=min_history)


def test_reject_zero_trade():
    p, v, _ = fixture()
    with pytest.raises(ValueError):
        calibrate(p, v, [0., 0.])


def test_determinism():
    assert calibrate(*fixture()) == calibrate(*fixture())
