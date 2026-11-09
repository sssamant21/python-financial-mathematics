import numpy as np
import pytest
from factor_lab import rolling_exposures, synthetic


def test_recover_known_coefficients():
    rng = np.random.default_rng(4)
    x = rng.normal(size=(120, 2))
    y = .01 + 1.5*x[:, 0] - .4*x[:, 1]
    rows = rolling_exposures(x, y, window=60, horizon=20)
    assert len(rows) == 3
    assert rows[0]['intercept'] == pytest.approx(.01, abs=1e-12)
    assert rows[0]['betas'] == pytest.approx([1.5, -.4], abs=1e-12)
    assert rows[0]['heldout_mse'] < 1e-20


def test_nonoverlap_and_future_isolation():
    x, y = synthetic()
    a = rolling_exposures(x, y)
    changed = y.copy()
    changed[100:] += .1
    b = rolling_exposures(x, changed)
    assert a[0]['betas'] == b[0]['betas']
    assert a[0]['intercept'] == b[0]['intercept']
    assert all(a[i]['test_end_exclusive'] == a[i+1]['origin_index'] for i in range(len(a)-1))


def test_reproducible():
    assert rolling_exposures(*synthetic()) == rolling_exposures(*synthetic())


def test_rank_deficiency_and_ridge():
    x = np.ones((120, 2))
    y = np.arange(120)/1000
    with pytest.raises(ValueError, match='rank'):
        rolling_exposures(x, y)
    assert len(rolling_exposures(x, y, ridge=1.0)) > 0


@pytest.mark.parametrize('kwargs', [{'window': 3}, {'horizon': 0}, {'ridge': -1}, {'window': True}])
def test_invalid_settings(kwargs):
    with pytest.raises(ValueError):
        rolling_exposures(*synthetic(), **kwargs)


def test_nonfinite_and_shape():
    x, y = synthetic()
    with pytest.raises(ValueError):
        rolling_exposures(x, y[:-1])
    x[0, 0] = np.nan
    with pytest.raises(ValueError):
        rolling_exposures(x, y)
