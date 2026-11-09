import numpy as np
import pytest
from stability import sample_covariance, shrink_to_diagonal, finite_difference_marginal
from risk_attribution import contributions


def test_sample_covariance_closed_form():
    assert np.allclose(sample_covariance([[1,2], [2,4], [3,6]]), [[1,2],[2,4]])


def test_single_asset_shape():
    assert sample_covariance([[1],[2],[3]]).shape == (1,1)


def test_shrinkage_endpoints():
    c = np.array([[4.,1.],[1.,9.]])
    assert np.allclose(shrink_to_diagonal(c,0), c)
    assert np.allclose(shrink_to_diagonal(c,1), np.diag([4.,9.]))
    assert np.allclose(np.diag(shrink_to_diagonal(c,.5)), np.diag(c))


def test_gradient_matches_euler():
    w = np.array([.5,.3,.2])
    c = np.array([[.04,.01,-.002],[.01,.03,.004],[-.002,.004,.01]])
    _, marginal, component = contributions(w,c)
    assert np.allclose(finite_difference_marginal(w,c), marginal, rtol=1e-7, atol=1e-8)
    assert np.isclose(component.sum(), np.sqrt(w@c@w))


def test_hedge_gradient_negative():
    assert finite_difference_marginal([.2,.8], [[.01,-.04],[-.04,.25]])[0] < 0


@pytest.mark.parametrize("bad", [[[1,2]], [[1,float("nan")],[2,3]], [1,2,3]])
def test_invalid_returns(bad):
    with pytest.raises(ValueError): sample_covariance(bad)


@pytest.mark.parametrize("c,a", [([[1,0],[0,1]],-.1), ([[1,0],[0,1]],1.1),
                                ([[1,2],[2,1]],.5), ([[1,2],[0,1]],.5)])
def test_invalid_shrinkage(c,a):
    with pytest.raises(ValueError): shrink_to_diagonal(c,a)


def test_invalid_step():
    with pytest.raises(ValueError): finite_difference_marginal([1.], [[.04]], step=0)
