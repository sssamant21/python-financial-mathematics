"""Reference checks for Section 3.4."""
from fractions import Fraction as F
from section_3_04 import (rational, affine_inverse, profit, quantity_from_profit,
                          present_value, rate_from_present_value,
                          restricted_square, inverse_restricted_square)


def rejects(error, function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def run():
    assert affine_inverse(13, slope=2, intercept=3) == {"kind": "unique", "x": F(5)}
    assert affine_inverse(5, slope=0, intercept=5)["kind"] == "all"
    assert affine_inverse(4, slope=0, intercept=5)["kind"] == "none"
    m = dict(price=20, unit_cost=10, fixed_cost=100)
    assert quantity_from_profit(80, **m) == {"kind": "unique", "quantity": F(18)}
    assert quantity_from_profit(85, **m)["kind"] == "not_in_range"
    assert quantity_from_profit(85, whole_units=False, **m)["quantity"] == F(37, 2)
    assert quantity_from_profit(-110, **m)["kind"] == "outside_domain"
    assert quantity_from_profit(0, price=10, unit_cost=10,
                                fixed_cost=100)["kind"] == "none"
    assert quantity_from_profit(-100, price=10, unit_cost=10,
                                fixed_cost=100)["kind"] == "all"
    for n in (0, 1, 5, 18, 100):
        assert quantity_from_profit(profit(n, **m), **m)["quantity"] == n
    assert present_value(110, "1/10") == 100
    assert rate_from_present_value(110, 100) == F(1, 10)
    for rate in ("-1/2", "0", "1/10", "2"):
        assert rate_from_present_value(110, present_value(110, rate)) == F(rate)
    assert inverse_restricted_square("9/4") == {"kind": "unique", "x": F(3, 2)}
    assert inverse_restricted_square(2)["kind"] == "irrational_or_unrepresented"
    assert restricted_square(inverse_restricted_square("9/4")["x"]) == F(9, 4)
    rejects(ValueError, present_value, 110, -1)
    rejects(ValueError, rate_from_present_value, 110, 0)
    rejects(ValueError, inverse_restricted_square, -1)
    rejects(ValueError, restricted_square, -2)
    rejects(TypeError, rational, True)
    rejects(TypeError, rational, 0.1)
    print("PASS: Section 3.4 reference checks")


if __name__ == "__main__":
    run()
