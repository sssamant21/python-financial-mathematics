import numpy as np
import pytest
from walkforward import walkforward


def fixture():
    return np.random.default_rng(7).normal(.001, .02, 180)


def test_alignment_and_no_overlap():
    x = walkforward(fixture(), train=60, horizon=20, blocks=(2, 4), simulations=20)
    assert len(x['rows']) == 12
    assert [r['origin'] for r in x['rows'] if r['block'] == 2] == [60, 80, 100, 120, 140, 160]
    assert all(r['train_start'] + 60 == r['origin'] and r['test_end_exclusive'] == r['origin'] + 20 for r in x['rows'])


def test_deterministic():
    assert walkforward(fixture(), train=60, horizon=20, simulations=20) == walkforward(fixture(), train=60, horizon=20, simulations=20)


def test_future_mutation_isolation():
    r = fixture()
    a = walkforward(r, train=60, horizon=20, simulations=20)['rows'][0]
    r[81:] = .9
    b = walkforward(r, train=60, horizon=20, simulations=20)['rows'][0]
    assert a == b


def test_forecast_ignores_held_out_returns():
    r = fixture()
    a = walkforward(r, train=60, horizon=20, simulations=20)['rows'][0]
    r[60:80] = -.1
    b = walkforward(r, train=60, horizon=20, simulations=20)['rows'][0]
    assert a['forecast_p95'] == b['forecast_p95']
    assert a['realized_max_drawdown'] != b['realized_max_drawdown']


def test_flat_returns():
    x = walkforward(np.zeros(100), train=60, horizon=20, simulations=20)
    assert all(row['forecast_p95'] == row['realized_max_drawdown'] == 0 for row in x['rows'])


def test_invalid_parameters():
    for kw in ({'train': 10}, {'horizon': 1}, {'step': 5}, {'blocks': (100,)},
               {'blocks': ()}, {'blocks': (2, 2)}, {'simulations': 1}, {'train': True}):
        with pytest.raises(ValueError):
            walkforward(fixture(), **dict({'train': 60, 'horizon': 20, 'simulations': 20}, **kw))


def test_insufficient_data():
    with pytest.raises(ValueError):
        walkforward(np.zeros(50), train=40, horizon=20)


def test_no_input_mutation():
    x = fixture()
    y = x.copy()
    walkforward(x, train=60, horizon=20, simulations=20)
    np.testing.assert_array_equal(x, y)


def test_summary_consistency():
    x = walkforward(fixture(), train=60, horizon=20, simulations=20)
    for s in x['summary']:
        rows = [r for r in x['rows'] if r['block'] == s['block']]
        assert s['scored_periods'] == len(rows)
        assert s['p95_exceedances'] == sum(r['exceeded_p95'] for r in rows)
