import numpy as np
import pytest
from erc import estimate_covariance, erc_weights, risk_contributions, walk_forward_stability

def sample():
    rng = np.random.default_rng(14)
    return rng.normal(size=(160,3)) @ np.array([[.01,.003,0],[0,.02,.003],[0,0,.03]])

def test_equal_contribution():
    c = estimate_covariance(sample()[:52])
    w = erc_weights(c)
    assert np.all(w > 0) and np.isclose(w.sum(),1)
    assert np.allclose(risk_contributions(w,c), np.ones(3)/3, atol=1e-8)

def test_diagonal():
    assert np.allclose(erc_weights(np.diag([.01,.04,.09])), np.array([6,3,2])/11, atol=1e-8)

def test_correlations_matter():
    c = np.array([[.01,.008,0],[.008,.04,0],[0,0,.09]])
    assert not np.allclose(erc_weights(c), erc_weights(np.diag(np.diag(c))))

def test_future_isolation():
    r = sample()
    a = walk_forward_stability(r)
    changed = r.copy()
    changed[60:] *= 2
    b = walk_forward_stability(changed)
    assert np.allclose(a[0][1],b[0][1])
    assert np.allclose(a[0][2],b[0][2])

def test_nonoverlap():
    records = walk_forward_stability(sample())
    assert np.all(np.diff([v[0] for v in records]) == 13)
    assert all(np.isclose(v[3].sum(),1) for v in records)

def test_determinism():
    a,b = walk_forward_stability(sample()),walk_forward_stability(sample())
    assert all(np.array_equal(x[1],y[1]) for x,y in zip(a,b))

@pytest.mark.parametrize("cov",[np.array([[1,2],[2,1]]),np.array([[1,np.nan],[np.nan,1]]),np.eye(1)])
def test_bad_cov(cov):
    with pytest.raises(ValueError):
        erc_weights(cov)

def test_zero_variance():
    with pytest.raises(ValueError):
        estimate_covariance(np.ones((12,3)))

def test_bad_window():
    with pytest.raises(ValueError):
        walk_forward_stability(sample(),horizon=1)

def test_bad_shrinkage():
    with pytest.raises(ValueError):
        estimate_covariance(sample(),shrinkage=1.1)
