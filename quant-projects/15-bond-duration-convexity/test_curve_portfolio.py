import pytest
from curve_portfolio import Bond, bond_value, key_rate_dv01, portfolio_value, scenario, shift, spot

CURVE=((1,.03),(3,.04),(5,.05),(10,.06))
BONDS=(Bond(1000,.04,3,2),Bond(1000,.05,7))

def test_interpolation():
    assert spot(CURVE,2)==pytest.approx(.035)
    assert spot(CURVE,3)==pytest.approx(.04)

def test_zero_coupon():
    assert bond_value(Bond(1000,0,5),CURVE)==pytest.approx(1000/1.05**5)

def test_additivity_and_units():
    assert portfolio_value(BONDS,CURVE)==pytest.approx(sum(bond_value(b,CURVE) for b in BONDS))
    assert bond_value(Bond(1000,.04,3,2),CURVE)==pytest.approx(2*bond_value(Bond(1000,.04,3),CURVE))

def test_zero_shock():
    r=scenario(BONDS,CURVE,(0,0,0,0))
    assert r["exact_change"]==pytest.approx(0)
    assert r["linear_change"]==pytest.approx(0)

def test_parallel_rise():
    assert scenario(BONDS,CURVE,(100,)*4)["exact_change"]<0

def test_key_rate_dv01_independent_finite_difference():
    _,dv=key_rate_dv01(BONDS,CURVE)
    for i,value in enumerate(dv):
        plus=[0]*4; minus=[0]*4
        plus[i]=1; minus[i]=-1
        expected=(portfolio_value(BONDS,shift(CURVE,minus))-portfolio_value(BONDS,shift(CURVE,plus)))/2
        assert value==pytest.approx(expected)

def test_small_shock_linearization():
    assert abs(scenario(BONDS,CURVE,(.01,-.01,.01,-.01))["approximation_error"])<.0001

def test_bump_normalization():
    _,a=key_rate_dv01(BONDS,CURVE,1)
    _,b=key_rate_dv01(BONDS,CURVE,.5)
    assert b==pytest.approx(a,rel=1e-6)

@pytest.mark.parametrize("curve",[
    ((2,.03),(5,.04)),((1,.03),(1,.04)),((1,-.999),(3,-1)),
    ((1,.03),),((1,float("nan")),(3,.04))])
def test_invalid_curves(curve):
    with pytest.raises(ValueError):
        portfolio_value(BONDS,curve)

@pytest.mark.parametrize("bond",[Bond(1000,.04,11),Bond(1000,.04,3,0)])
def test_invalid_portfolios(bond):
    with pytest.raises(ValueError):
        portfolio_value((bond,),CURVE)

def test_invalid_bond():
    with pytest.raises(ValueError):
        Bond(-100,.04,5)
    with pytest.raises(ValueError):
        Bond(1000,.04,True)

def test_invalid_shocks_and_bump():
    with pytest.raises(ValueError):
        shift(CURVE,(0,0))
    with pytest.raises(ValueError):
        shift(CURVE,(0,0,float("nan"),0))
    with pytest.raises(ValueError):
        key_rate_dv01(BONDS,CURVE,0)
