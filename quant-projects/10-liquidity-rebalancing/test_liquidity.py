import importlib.util
from pathlib import Path
import numpy as np
import pytest

spec = importlib.util.spec_from_file_location("liquidity", Path(__file__).with_name("liquidity.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def run(**kwargs):
    args = dict(holdings=[60000, 40000], target_weights=[.4, .6],
                prices=[100, 50], daily_volume=[10000, 20000], equity=100000)
    args.update(kwargs)
    return module.estimate(**args)


def test_self_financing():
    assert sum(run()["trade_dollars"]) == pytest.approx(0)


def test_turnover():
    assert run()["turnover_fraction"] == pytest.approx(.2)


def test_capacity():
    assert run()["max_execution_days"] == pytest.approx(.2)


def test_stress():
    base = run()
    stressed = run(stress_volume_factor=.25)
    assert stressed["max_execution_days"] == pytest.approx(4 * base["max_execution_days"])
    assert stressed["estimated_cost_dollars"] > base["estimated_cost_dollars"]


def test_no_trade():
    assert run(target_weights=[.6, .4])["estimated_cost_dollars"] == 0


@pytest.mark.parametrize("bad", [
    {"participation": 0}, {"participation": 1.1},
    {"stress_volume_factor": 0}, {"spread_bps": -1},
    {"equity": 200000}, {"target_weights": [.2, .2]},
    {"daily_volume": [0, 10]}, {"prices": [np.nan, 50]},
    {"holdings": [60000]}, {"target_weights": [.4, -.6]},
])
def test_invalid(bad):
    with pytest.raises(ValueError):
        run(**bad)
