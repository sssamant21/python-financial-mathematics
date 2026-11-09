import numpy as np
import pytest
from oos_covariance import walk_forward_covariance, summarize

def fixture():
    return np.random.default_rng(23).normal(0, .01, (45, 2))

def test_manual_training_only():
    x = fixture()
    r = walk_forward_covariance(x, [.6,.4], train=20, horizon=5, step=5, shrinkages=(0.,))[0]
    w = np.array([.6,.4])
    assert r[:4] == (20,0,25,0.)
    assert r[4] == pytest.approx(w @ np.cov(x[:20], rowvar=False, ddof=1) @ w)
    assert r[5] == pytest.approx(np.mean((x[20:25] @ w)**2))

def test_future_mutation_isolation():
    x = fixture()
    original = walk_forward_covariance(x, [.5,.5], train=20, horizon=5, step=5)
    y = x.copy()
    y[20:] *= 100
    changed = walk_forward_covariance(y, [.5,.5], train=20, horizon=5, step=5)
    assert [r[4] for r in original[:3]] == [r[4] for r in changed[:3]]
    assert any(a[5] != b[5] for a,b in zip(original[:3], changed[:3]))

def test_nonoverlapping_and_summary():
    rows = walk_forward_covariance(fixture(), [.5,.5], train=20, horizon=4, step=4)
    origins = [r for r in rows if r[3] == 0.]
    assert all(a[2] <= b[0] for a,b in zip(origins, origins[1:]))
    assert summarize(rows)[0.]['origins'] == len(origins)
    assert all(v['variance_mse'] >= 0 for v in summarize(rows).values())

def test_deterministic():
    x = fixture()
    assert walk_forward_covariance(x,[.5,.5],train=20) == walk_forward_covariance(x,[.5,.5],train=20)

@pytest.mark.parametrize("kwargs", [dict(train=2),dict(horizon=0),dict(step=1),dict(shrinkages=(-.1,)),dict(shrinkages=(float('nan'),)),dict(train=50)])
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        walk_forward_covariance(fixture(), [.5,.5], **kwargs)

def test_invalid_data_and_weights():
    x = fixture()
    for weights in ([.5,.3],[.5,.5,.0]):
        with pytest.raises(ValueError):
            walk_forward_covariance(x, weights)
    x[0,0] = np.nan
    with pytest.raises(ValueError):
        walk_forward_covariance(x, [.5,.5])
