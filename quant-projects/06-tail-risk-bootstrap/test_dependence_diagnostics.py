import numpy as np
import pandas as pd
import pytest
from dependence_diagnostics import block_indices,block_var_interval,conditional_coverage,evaluate

def fixture(n=85):
    return pd.DataFrame({'Date':pd.date_range('2020-01-03',periods=n,freq='W-FRI'),
        'Return':np.random.default_rng(19).normal(0,.015,n)})

def test_contiguous_blocks():
    a=block_indices(30,4,10,np.random.default_rng(8))
    assert a.shape==(10,30)
    for i in range(0,28,4):assert np.all((a[:,i+1:i+4]-a[:,i:i+3])%30==1)

def test_block_one_equals_iid():
    assert np.array_equal(block_indices(30,1,12,np.random.default_rng(2)),
                          np.random.default_rng(2).integers(0,30,size=(12,30)))

def test_reproducible_interval():
    x=fixture().Return.to_numpy()
    a=block_var_interval(x,samples=120)
    assert a==block_var_interval(x,samples=120) and 0<=a[0]<=a[1]

def test_transition_counts():
    r=conditional_coverage(np.array([0,0,1,1,0,1,0]))
    assert (r['n00'],r['n01'],r['n10'],r['n11'])==(1,2,2,1)
    assert 0<=r['p_cc']<=1

def test_degenerate_breaches():
    r=conditional_coverage(np.zeros(80,dtype=int))
    assert not r['independence_identifiable'] and r['p_cc'] is None

def test_future_return_not_used_in_forecast():
    a=fixture();a.loc[a.index[-1],'Return']=.10
    b=a.copy();b.loc[b.index[-1],'Return']=-.50
    x,_=evaluate(a,samples=100);y,_=evaluate(b,samples=100)
    pd.testing.assert_frame_equal(x.iloc[:-1],y.iloc[:-1])
    assert x.iloc[-1]['VaR']==y.iloc[-1]['VaR']
    assert x.iloc[-1]['BlockBootstrapLower']==y.iloc[-1]['BlockBootstrapLower']
    assert x.iloc[-1]['Breach']!=y.iloc[-1]['Breach']

def test_reject_invalid_inputs():
    with pytest.raises(ValueError):block_indices(19,4,10,np.random.default_rng(1))
    with pytest.raises(ValueError):block_var_interval(np.zeros(30),block=31)
    with pytest.raises(ValueError):conditional_coverage([0,2,1])
    x=fixture();x.loc[1,'Date']=x.loc[0,'Date']
    with pytest.raises(ValueError):evaluate(x,samples=100)
