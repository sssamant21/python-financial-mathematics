import numpy as np
import pytest
from compare import compare, synthetic

def test_methods_and_nonoverlap():
    rows = compare(synthetic())
    assert {r["method"] for r in rows} == {"inverse_vol","erc"}
    assert np.all(np.diff([r["origin"] for r in rows if r["method"]=="erc"]) == 13)

def test_matched_constraints():
    for row in compare(synthetic()):
        assert np.all(row["weights"] > 0)
        assert np.isclose(row["weights"].sum(), 1)

def test_future_isolation_of_first_weights():
    r = synthetic()
    altered = r.copy()
    altered[52:] *= 1.8
    a, b = compare(r), compare(altered)
    for i in range(2):
        assert np.array_equal(a[i]["weights"], b[i]["weights"])

def test_initial_turnover_and_cost():
    a = compare(synthetic(), cost_bps=0)
    b = compare(synthetic(), cost_bps=100)
    for i in range(2):
        assert np.isclose(a[i]["turnover"],1)
        assert np.isclose(b[i]["net_return"]+1,(a[i]["gross_return"]+1)*.99)
    for method in ("erc","inverse_vol"):
        assert [x for x in b if x["method"]==method][-1]["wealth"] <= [x for x in a if x["method"]==method][-1]["wealth"]

def test_buy_and_hold_compounding():
    r = np.tile([[.01,.02],[-.005,.015],[.02,-.01],[.005,.025]], (10,1))
    rows = compare(r, lookback=12, horizon=4, shrinkage=1., cost_bps=0)
    w = rows[0]["weights"]
    expected = float(w @ np.prod(1+r[12:16],axis=0))
    assert np.isclose(rows[0]["wealth"],expected)

def test_determinism():
    a,b=compare(synthetic()),compare(synthetic())
    assert [(x["wealth"],x["turnover"]) for x in a] == [(x["wealth"],x["turnover"]) for x in b]

@pytest.mark.parametrize("kwargs", [{"lookback":3},{"horizon":0},{"cost_bps":-1},{"shrinkage":1.2}])
def test_bad_controls(kwargs):
    with pytest.raises(ValueError):
        compare(synthetic(), **kwargs)

def test_bad_returns():
    for r in (np.ones((4,2)), np.array([[0.,float("nan")]]*100), np.array([[-1.,.01]]*100)):
        with pytest.raises(ValueError):
            compare(r)
