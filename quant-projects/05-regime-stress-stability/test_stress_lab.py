import numpy as np
import pandas as pd
import pytest
from stress_lab import (ASSETS,LOOKBACK,synthetic_prices,validate_prices,
                        forecast_cov,weights,stress_cov,walk_forward,run_study)

@pytest.fixture(scope="module")
def prices():
    return synthetic_prices()

def test_reproducible_fixture(prices):
    pd.testing.assert_frame_equal(prices,synthetic_prices())
    assert (prices>0).all().all()

def test_missing_data_rejected(prices):
    p=prices.copy()
    p.iloc[5,1]=np.nan
    with pytest.raises(ValueError):
        validate_prices(p)

def test_optimizer_constraints(prices):
    cov=forecast_cov(prices.pct_change(fill_method=None).iloc[1:LOOKBACK+1].to_numpy())
    w=weights(cov)
    assert np.isclose(w.sum(),1)
    assert w.min()>=-1e-7 and w.max()<=.4000001

def test_stress_covariance_psd(prices):
    cov=forecast_cov(prices.pct_change(fill_method=None).iloc[1:LOOKBACK+1].to_numpy())
    stressed=stress_cov(cov,.5,2)
    assert np.linalg.eigvalsh(stressed).min()>=-1e-9
    w=np.full(5,.2)
    assert w@stressed@w>=w@cov@w

def test_future_changes_cannot_change_past(prices):
    before,_=walk_forward(prices.iloc[:130])
    changed=prices.copy()
    changed.iloc[130:]*=2
    after,_=walk_forward(changed)
    pd.testing.assert_frame_equal(before.reset_index(drop=True),
                                  after.iloc[:len(before)].reset_index(drop=True),
                                  rtol=1e-11,atol=1e-11)

def test_cost_and_forecast_only_stresses(prices):
    zero,_=walk_forward(prices,cost_bps=0)
    high,_=walk_forward(prices,cost_bps=25)
    base,_=walk_forward(prices)
    stressed,_=walk_forward(prices,correlation_shift=.5,vol_multiplier=2)
    assert high.Equity.iloc[-1]<zero.Equity.iloc[-1]
    np.testing.assert_allclose(base.NetReturn,stressed.NetReturn)
    assert (stressed.ForecastAnnualVol>=base.ForecastAnnualVol-1e-10).all()

def test_scenarios_and_shrinkage(prices):
    summary,regimes,ts,alloc=run_study(prices)
    assert len(summary)==6 and len(regimes)==12
    assert (summary.Weeks>100).all()
    assert set(regimes.Status)=={"DATE_WINDOW_ONLY"}
    assert np.isfinite(summary.EndingWealthPerDollar).all()
    assert summary.ForecastVolStd.gt(0).all()
    base=alloc[alloc.Scenario=="baseline"][list(ASSETS)].to_numpy()
    shrink=alloc[alloc.Scenario=="shrinkage_50pct"][list(ASSETS)].to_numpy()
    assert np.max(np.abs(base-shrink))>1e-5
