import numpy as np
import pytest
from dependent_bootstrap import bootstrap_horizon_losses, bootstrap_var_cvar


def test_seed_reproducible_and_horizon_compounding():
    r = np.full(60, 0.01)
    a = bootstrap_horizon_losses(r, horizon=13, block_length=4, draws=200)
    b = bootstrap_horizon_losses(r, horizon=13, block_length=4, draws=200)
    np.testing.assert_array_equal(a, b)
    np.testing.assert_allclose(a, 1 - 1.01**13, atol=1e-14)


def test_single_week_bootstrap_is_empirical():
    r = np.linspace(-0.08, 0.08, 60)
    losses = bootstrap_horizon_losses(r, horizon=1, block_length=3, draws=300)
    assert all(np.any(np.isclose(v, -r)) for v in losses)


def test_bootstrap_tail_order():
    r = np.random.default_rng(1).normal(0, 0.02, 100)
    losses = bootstrap_horizon_losses(r, 4, draws=1000)
    var, cvar = bootstrap_var_cvar(losses)
    assert 0 <= var <= cvar


def test_training_only_isolation():
    r = np.linspace(-0.05, 0.05, 120)
    a = bootstrap_horizon_losses(r[:80], 4)
    r[80:] = -0.9
    b = bootstrap_horizon_losses(r[:80], 4)
    np.testing.assert_array_equal(a, b)


@pytest.mark.parametrize('kwargs', [{'horizon': 0}, {'horizon': True}, {'horizon': 4, 'block_length': 0}, {'horizon': 4, 'draws': 3}, {'horizon': 4, 'seed': -1}])
def test_invalid_config(kwargs):
    with pytest.raises(ValueError):
        bootstrap_horizon_losses(np.zeros(50), **kwargs)


def test_invalid_return_and_loss_inputs():
    with pytest.raises(ValueError):
        bootstrap_horizon_losses(np.full(40, -1.0), 4)
    with pytest.raises(ValueError):
        bootstrap_var_cvar(np.ones(99))
