"""Deterministic, point-in-time tests for integrated bootstrap scoring."""
import numpy as np
import pandas as pd
import pytest

from bootstrap_walkforward import score_bootstrap
from multi_horizon import horizon_risk, portfolio_returns, synthetic_prices


@pytest.fixture(scope="module")
def weekly():
    return portfolio_returns(synthetic_prices(175))


@pytest.mark.parametrize("horizon", [1, 4, 13])
def test_alignment_nonoverlap_and_tail_order(weekly, horizon):
    scored = score_bootstrap(weekly, horizon=horizon, draws=100, seed=5)
    baseline = horizon_risk(weekly, horizon=horizon)
    pd.testing.assert_frame_equal(
        scored[baseline.columns], baseline)
    assert (scored.BootstrapCVaR95 >= scored.BootstrapVaR95).all()
    assert scored.BootstrapBreach.isin([0, 1]).all()
    for i in range(1, len(scored)):
        assert scored.OutcomeStart.iloc[i] > scored.OutcomeEnd.iloc[i-1]


def test_determinism(weekly):
    a = score_bootstrap(weekly, horizon=4, draws=100)
    b = score_bootstrap(weekly, horizon=4, draws=100)
    pd.testing.assert_frame_equal(a, b)


def test_no_future_data_in_first_forecast(weekly):
    a = score_bootstrap(weekly, horizon=4, draws=100)
    changed = weekly.copy()
    changed.loc[changed.index[104:108], "Return"] = -0.5
    b = score_bootstrap(changed, horizon=4, draws=100)
    assert a.BootstrapVaR95.iloc[0] == b.BootstrapVaR95.iloc[0]
    assert a.BootstrapCVaR95.iloc[0] == b.BootstrapCVaR95.iloc[0]
    assert a.RealizedLoss.iloc[0] != b.RealizedLoss.iloc[0]


def test_training_window_rolls(weekly):
    a = score_bootstrap(weekly, horizon=4, draws=100)
    changed = weekly.copy()
    changed.loc[changed.index[0], "Return"] = -0.6
    b = score_bootstrap(changed, horizon=4, draws=100)
    assert a.BootstrapVaR95.iloc[0] != b.BootstrapVaR95.iloc[0]
    # The first training observation has rolled out by the second origin.
    # By origin t=108 it is absent, so the second forecast must match.
    assert a.BootstrapVaR95.iloc[1] == b.BootstrapVaR95.iloc[1]


@pytest.mark.parametrize("kwargs", [
    {"block_length": 0}, {"block_length": 105}, {"draws": 99},
    {"seed": -1}, {"alpha": 0}, {"horizon": 0}])
def test_invalid_parameters(weekly, kwargs):
    with pytest.raises(ValueError):
        score_bootstrap(weekly, **kwargs)
