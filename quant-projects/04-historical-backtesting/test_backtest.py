"""Synthetic-fixture tests; no third-party market data required."""
import numpy as np
import pandas as pd
from backtest import TICKERS, LOOKBACK, STRATEGIES, estimate, optimal_weights, backtest, kupiec_pvalue

def fixture(n=120):
 rng=np.random.default_rng(2026)
 shocks=rng.normal(0.001,0.015,(n,len(TICKERS)))
 p=100*np.exp(np.cumsum(shocks,axis=0))
 return pd.DataFrame(p,columns=TICKERS,index=pd.date_range("2020-01-03",periods=n,freq="W-FRI"))

def test_optimizer_and_covariance():
 p=fixture()
 mu,cov,_=estimate(p.pct_change(fill_method=None).iloc[1:53])
 assert np.min(np.linalg.eigvalsh(cov))>0
 weights,_=optimal_weights(mu,cov)
 assert set(weights)==set(STRATEGIES)
 for w in weights.values():
  assert np.isclose(w.sum(),1,atol=1e-6)
  assert np.min(w)>=-1e-6 and np.max(w)<=0.40001

def test_no_lookahead_when_future_prices_change():
 p=fixture()
 a,wa,_=backtest(p.iloc[:110])
 q=p.copy()
 q.iloc[110:]=q.iloc[110:]*1.25
 b,wb,_=backtest(q)
 pd.testing.assert_frame_equal(a.reset_index(drop=True),b[b.Date<=a.Date.max()].reset_index(drop=True),atol=1e-8,rtol=1e-8)
 assert len(a)==(110-(LOOKBACK+1))*len(STRATEGIES)

def test_kupiec_p_value_range():
 assert 0 <= kupiec_pvalue(334,23) <= 1
