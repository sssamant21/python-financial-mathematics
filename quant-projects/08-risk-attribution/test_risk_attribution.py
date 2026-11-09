import numpy as np
import pytest
from risk_attribution import contributions, normal_var_contributions


def test_euler_additivity():
    w = np.array([.6, .4])
    cov = np.array([[.04, .01], [.01, .09]])
    vol, marginal, component = contributions(w, cov)
    assert np.isclose(vol, np.sqrt(w @ cov @ w))
    assert np.isclose(component.sum(), vol)
    assert np.allclose(component, w * marginal)


def test_independent_assets_closed_form():
    vol, marginal, comp = contributions([.5, .5], [[.04, 0], [0, .04]])
    assert np.isclose(vol, np.sqrt(.02))
    assert np.allclose(comp, [vol/2, vol/2])


def test_normal_var_additivity_and_horizon():
    w = [.7, .3]
    cov = [[.04, .002], [.002, .01]]
    var1, _, parts1 = normal_var_contributions(w, cov)
    var4, _, parts4 = normal_var_contributions(w, cov, horizon=4)
    assert np.isclose(parts1.sum(), var1)
    assert np.isclose(parts4.sum(), var4)
    assert np.isclose(var4, 2*var1)


def test_negative_hedge_contribution_is_allowed():
    vol, _, comp = contributions([.2, .8], [[.01, -.04], [-.04, .25]])
    assert comp[0] < 0
    assert np.isclose(comp.sum(), vol)


@pytest.mark.parametrize('w,c', [([.3,.3], [[1,0],[0,1]]), ([1.], [[-1.]]), ([1.], [[0.]]), ([1.,0.], [[1.,2.],[0.,1.]]), ([float('nan')], [[1.]])])
def test_invalid_inputs(w,c):
    with pytest.raises(ValueError):
        contributions(w,c)


def test_invalid_horizon():
    with pytest.raises(ValueError):
        normal_var_contributions([1.], [[.04]], horizon=0)
