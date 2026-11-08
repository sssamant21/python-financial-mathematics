import numpy as np
import pandas as pd
import pytest
from multi_horizon import synthetic_prices,portfolio_returns,horizon_risk,summarize

def test_seed_and_portfolio_math():
    a=synthetic_prices(200)
    pd.testing.assert_frame_equal(a,synthetic_prices(200))
    r=portfolio_returns(a)
    expected=a[['TECH','BANK','HEALTH']].pct_change(fill_method=None).iloc[1:].to_numpy()@[.4,.3,.3]
    assert np.allclose(r.Return,expected)

@pytest.mark.parametrize("h",[1,4,13])
def test_nonoverlap_and_tail_order(h):
    s=horizon_risk(portfolio_returns(synthetic_prices(260)),horizon=h)
    assert len(s)==(259-104)//h
    assert (s.TrainingEnd<s.OutcomeStart).all()
    assert (s.HistoricalCVaR95>=s.HistoricalVaR95-1e-12).all()
    for i in range(1,len(s)): assert s.OutcomeStart.iloc[i]>s.OutcomeEnd.iloc[i-1]

def test_exact_compounded_loss():
    r=np.full(65,.01);r[60:64]=[-.1,.05,-.02,.03]
    x=pd.DataFrame({"Date":pd.date_range("2020-01-03",periods=65,freq="W-FRI"),"Return":r})
    s=horizon_risk(x,horizon=4,lookback=60)
    assert np.isclose(s.RealizedLoss.iloc[0],1-np.prod(1+r[60:64]))
    assert s.HistoricalVaR95.iloc[0]==0
    assert s.HistoricalBreach.iloc[0]==1

def test_no_future_leakage():
    r=portfolio_returns(synthetic_prices(240))
    a=horizon_risk(r,horizon=4)
    b=r.copy();b.loc[b.index>=200,'Return']=-.2
    c=horizon_risk(b,horizon=4)
    pd.testing.assert_frame_equal(a.iloc[:20].reset_index(drop=True),c.iloc[:20].reset_index(drop=True))

def test_current_outcome_excluded_from_forecast():
    r=portfolio_returns(synthetic_prices(200))
    a=horizon_risk(r,horizon=4)
    b=r.copy();b.loc[b.index[104:108],'Return']=-.5
    c=horizon_risk(b,horizon=4)
    assert a.HistoricalVaR95.iloc[0]==c.HistoricalVaR95.iloc[0]
    assert a.NormalVaR95.iloc[0]==c.NormalVaR95.iloc[0]
    assert a.RealizedLoss.iloc[0]!=c.RealizedLoss.iloc[0]

@pytest.mark.parametrize("h,lookback",[(0,104),(4,10),(100,104)])
def test_invalid_horizon(h,lookback):
    with pytest.raises(ValueError):
        horizon_risk(portfolio_returns(synthetic_prices(180)),h,lookback)

def test_invalid_weights_and_prices():
    p=synthetic_prices(90)
    with pytest.raises(ValueError): portfolio_returns(p,weights=[.5,.5,.5])
    p.loc[10,'TECH']=0
    with pytest.raises(ValueError): portfolio_returns(p)

def test_summary():
    s=horizon_risk(portfolio_returns(synthetic_prices(200)),horizon=4)
    x=summarize(s)
    assert x['scored_periods']==len(s)
    assert 0<=x['historical_breach_rate']<=1
