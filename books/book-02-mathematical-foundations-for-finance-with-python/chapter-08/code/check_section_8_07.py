"""Reference checks for Section 8.7."""
import math
from section_8_07 import (
    finite, circle_upper, circle_slope, break_even_quantity,
    break_even_sensitivity, bond_price, bond_price_derivative,
    yield_price_sensitivity, exposure_slope, centered_difference)

def close(a, b, rel_tol=1e-7, abs_tol=1e-8):
    assert math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol), (a, b)

def rejects(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)

def run():
    close(circle_upper(3), 4)
    close(circle_slope(3, 4), -0.75)
    for x in (-3, -1, 0, 1, 3):
        y = circle_upper(x)
        close(centered_difference(circle_upper, x), circle_slope(x, y))
    for p in (30, 40, 50, 80):
        q = break_even_quantity(p, 20, 1200)
        close((p-20)*q, 1200)
        close(break_even_sensitivity(p, 20, 1200), -1200/(p-20)**2)
        close(centered_difference(lambda v:break_even_quantity(v, 20, 1200), p),
              break_even_sensitivity(p, 20, 1200))
    close(bond_price((105,), 0.05), 100)
    close(bond_price_derivative((105,), 0.05), -105/1.05**2)
    close(yield_price_sensitivity((105,), 0.05), -0.0105)
    for flows in ((105,), (4, 4, 104), (10, 20, 30, 100)):
        for y in (0, 0.03, 0.1):
            dp = bond_price_derivative(flows, y)
            assert dp < 0
            close(centered_difference(lambda z:bond_price(flows, z), y), dp)
            close(yield_price_sensitivity(flows, y)*dp, 1)
    close(exposure_slope(3, 4, 1, 1), -0.75)
    rejects(ValueError, circle_slope, 5, 0)
    rejects(ValueError, circle_upper, 6, 5)
    rejects(ValueError, break_even_quantity, 20, 20, 1200)
    rejects(ValueError, break_even_quantity, 50, 20, 0)
    rejects(ValueError, bond_price, (105,), -1)
    rejects(ValueError, bond_price, (), 0.05)
    rejects(ValueError, exposure_slope, 1, 0, 1, 1)
    rejects(ValueError, centered_difference, lambda x:x*x, 1, 0)
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 8.7 reference checks")

if __name__ == "__main__":
    run()
