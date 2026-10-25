"""Independent reference checks for Book 02 Section 9.1."""
import math
from section_9_01 import (
    finite, discounted_value, discounted_sensitivity, discounted_shock,
    demand_quantity, demand_sensitivity, portfolio_sensitivity)

def close(actual, expected, rel_tol=1e-9, abs_tol=1e-9):
    assert math.isclose(actual, expected, rel_tol=rel_tol, abs_tol=abs_tol), (actual, expected)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    for rate in (-0.02, 0.0, 0.04, 0.12):
        for years in (0, 1, 5, 10):
            v = 10000*math.exp(-rate*years)
            result = discounted_sensitivity(10000, rate, years)
            close(result["value"], v)
            close(result["absolute"], -years*v)
            close(result["normalized_rate"], years)
            close(result["elasticity"], -rate*years)
            shock = discounted_shock(10000, rate, years, 0.0001)
            close(shock["exact"], discounted_value(10000, rate+0.0001, years)-v,
                  rel_tol=1e-6, abs_tol=1e-8)
            close(shock["first_order"], -years*v*0.0001)
    d = demand_sensitivity(20)
    close(d["quantity"], 400*20**-1.5)
    close(d["absolute"], -600*20**-2.5)
    close(d["elasticity"], -1.5)
    for price in (1, 10, 20, 100):
        close(demand_sensitivity(price)["elasticity"], -1.5)
    p = portfolio_sensitivity(20, 50, 1000)
    close(p["value"], 2000)
    close(p["absolute"], 20)
    close(p["elasticity"], 0.5)
    rejects(ValueError, discounted_value, 0, 0.04, 5)
    rejects(ValueError, discounted_value, 1000, 0.04, -1)
    rejects(ValueError, demand_quantity, 0)
    rejects(ValueError, portfolio_sensitivity, 0, 50, 0)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 9.1 reference checks")

if __name__ == "__main__":
    run()
