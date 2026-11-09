import math
import pytest
from bond_lab import cashflows, price, sensitivities, shock_table


def test_par_coupon_equals_yield():
    assert price(1000, 0.05, 5, 0.05) == pytest.approx(1000)


def test_zero_coupon_price_and_duration():
    result = sensitivities(1000, 0, 4, 0.05)
    assert result["price"] == pytest.approx(1000 / 1.05**4)
    assert result["macaulay_duration"] == pytest.approx(4)
    assert result["modified_duration"] == pytest.approx(4 / 1.05)


def test_cashflows_include_principal_only_at_maturity():
    assert cashflows(100, 0.03, 3) == [(1, 3), (2, 3), (3, 103)]


def test_yield_increase_lowers_price():
    assert price(1000, .04, 5, .06) < price(1000, .04, 5, .04)


def test_duration_matches_finite_difference():
    y = .05
    h = 1e-5
    p = price(1000, .04, 5, y)
    derivative = (price(1000, .04, 5, y + h) - price(1000, .04, 5, y - h)) / (2*h)
    assert -derivative / p == pytest.approx(sensitivities(1000, .04, 5, y)["modified_duration"], rel=1e-7)


def test_convexity_improves_approximation_for_moderate_shock():
    _, rows = shock_table(1000, .04, 5, .05, (100,))
    r = rows[0]
    assert abs(r["approximation_error"]) < abs(r["duration_return"] - r["exact_return"])


def test_shock_zero_returns_zero():
    _, rows = shock_table(1000, .04, 5, .05, (0,))
    assert rows[0]["exact_return"] == pytest.approx(0)


@pytest.mark.parametrize("face,coupon,years,y", [(0,.04,5,.05), (100,-.01,5,.05), (100,.04,0,.05),
                                                  (100,.04,True,.05), (100,.04,5,-1),
                                                  (100,.04,5,float("nan"))])
def test_invalid_inputs(face,coupon,years,y):
    with pytest.raises(ValueError):
        price(face,coupon,years,y)


def test_invalid_shock():
    with pytest.raises(ValueError):
        shock_table(100,.04,5,.05,(float("inf"),))
