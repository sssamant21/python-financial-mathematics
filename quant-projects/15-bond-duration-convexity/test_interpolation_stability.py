import math
import pytest
from curve_portfolio import Bond, portfolio_value
from interpolation_stability import discount_factor, value, diagnostics

CURVE=((1,.035),(3,.04),(5,.043),(10,.047))
BONDS=(Bond(1000,.04,3,2),Bond(1000,.05,7),Bond(1000,.03,10))

def test_knot_agreement():
    for t,r in CURVE:
        for method in ("rate_linear","log_discount"):
            assert discount_factor(CURVE,t,method)==pytest.approx((1+r)**(-t))

def test_rate_linear_matches_baseline():
    assert value(BONDS,CURVE,"rate_linear")==pytest.approx(portfolio_value(BONDS,CURVE))

def test_log_df_midpoint():
    assert discount_factor(CURVE,2,"log_discount")==pytest.approx(math.sqrt((1.035)**(-1)*(1.04)**(-3)))

def test_zero_coupon_at_knot():
    bonds=(Bond(1000,0,5),)
    assert value(bonds,CURVE,"log_discount")==pytest.approx(value(bonds,CURVE,"rate_linear"))

def test_parallel_up_decreases_both():
    d=diagnostics(BONDS,CURVE,(100,)*4)
    assert all(d[m]["exact_change"]<0 for m in ("rate_linear","log_discount"))

def test_zero_shock():
    d=diagnostics(BONDS,CURVE,(0,)*4)
    assert all(d[m]["exact_change"]==pytest.approx(0) for m in ("rate_linear","log_discount"))

def test_small_shock_linearization():
    d=diagnostics(BONDS,CURVE,(.01,-.01,.01,-.01))
    assert all(abs(d[m]["linear_error"])<.0001 for m in ("rate_linear","log_discount"))

def test_dv01_bump_stability():
    a=diagnostics(BONDS,CURVE,(0,)*4,1)
    b=diagnostics(BONDS,CURVE,(0,)*4,.5)
    for m in ("rate_linear","log_discount"):
        assert a[m]["dv01"]==pytest.approx(b[m]["dv01"],rel=1e-6)

def test_dv01_parallel_additivity():
    d=diagnostics(BONDS,CURVE,(.01,)*4)
    for m in ("rate_linear","log_discount"):
        assert d[m]["linear_change"]==pytest.approx(-.01*sum(d[m]["dv01"]))

@pytest.mark.parametrize("bad",[0,-1,11,True,2.5])
def test_invalid_year(bad):
    with pytest.raises(ValueError): discount_factor(CURVE,bad)

@pytest.mark.parametrize("bad",["cubic","",None])
def test_invalid_method(bad):
    with pytest.raises(ValueError): value(BONDS,CURVE,bad)

def test_invalid_bump():
    with pytest.raises(ValueError): diagnostics(BONDS,CURVE,(0,)*4,0)

def test_invalid_maturity():
    with pytest.raises(ValueError): value((Bond(1000,.04,11),),CURVE)

def test_invalid_shocks():
    with pytest.raises(ValueError): diagnostics(BONDS,CURVE,(100,))

def test_no_input_mutation():
    original=tuple(CURVE)
    diagnostics(BONDS,CURVE,(100,0,0,0))
    assert CURVE==original
