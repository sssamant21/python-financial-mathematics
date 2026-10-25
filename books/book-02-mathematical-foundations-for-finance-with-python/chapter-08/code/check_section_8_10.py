"""Independent acceptance checks for Chapter 08, Section 8.10."""
import math
from section_8_10 import (
    finite, profit, marginal_profit, present_value, pv_rate_derivatives,
    pv_rate_shock, log_return, break_even_quantity, break_even_derivative,
    bond_yield_from_price, bond_yield_price_derivative, centered_first,
    centered_second, chapter_report)

def close(actual, expected, rel_tol=1e-8, abs_tol=1e-8):
    assert math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol), (actual, expected)

def rejects(exc, function, *args):
    try:
        function(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    close(marginal_profit(125), 0)
    assert profit(125) > profit(100)
    assert profit(125) > profit(150)
    pv, first, second = pv_rate_derivatives(10000, 0.04, 5)
    close(pv, 10000*math.exp(-0.2))
    close(first, -5*pv)
    close(second, 25*pv)
    shock = pv_rate_shock(10000, 0.04, 5, 0.001)
    close(shock["first_order"], -0.005*pv)
    close(shock["second_order"], (-0.005+0.5*0.005**2)*pv)
    close(shock["exact"], pv*math.expm1(-0.005))
    assert abs(shock["second_order"]-shock["exact"]) < abs(shock["first_order"]-shock["exact"])
    close(log_return(80, 84), math.log(1.05))
    close(break_even_quantity(45, 15, 900), 30)
    close(break_even_derivative(45, 15, 900), -1)
    close(bond_yield_from_price(110, 100), 0.1)
    close(bond_yield_price_derivative(110, 100), -0.011)
    close(centered_first(lambda x:x**3, 2, 0.1), 12.01)
    close(centered_second(lambda x:x*x, 2, 0.1), 2)
    for r in (-0.01, 0, 0.04, 0.1):
        f = lambda z:present_value(10000, z, 5)
        _, d1, d2 = pv_rate_derivatives(10000, r, 5)
        close(centered_first(f, r, 1e-4), d1, rel_tol=1e-7)
        close(centered_second(f, r, 1e-3), d2, rel_tol=1e-6)
    assert len(chapter_report()) == 12
    rejects(ValueError, profit, 201)
    rejects(ValueError, present_value, -1, 0.04, 5)
    rejects(ValueError, log_return, 0, 84)
    rejects(ValueError, break_even_quantity, 15, 15, 900)
    rejects(ValueError, bond_yield_from_price, 110, 0)
    rejects(ValueError, centered_first, lambda x:x*x, 2, 0)
    rejects(ValueError, centered_second, lambda x:x*x, 2, 1e-20)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.10 Chapter 08 acceptance checks")

if __name__ == "__main__":
    run()
