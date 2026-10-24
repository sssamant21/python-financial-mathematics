"""Reference checks for Section 3.3."""
from fractions import Fraction as F
from section_3_03 import (q, gross_after_fee, discount, net_present_value,
                          discounted_gross_minus_fee, compose, affine)


def must_raise(error, function, *args):
    try:
        function(*args)
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def run():
    assert gross_after_fee(110, 10) == 100
    assert discount(100, "0.10") == F(1000, 11)
    assert net_present_value(110, 10, "0.10") == F(1000, 11)
    assert discounted_gross_minus_fee(110, 10, "0.10") == 90
    assert net_present_value(110, 10, 0) == 100
    assert discounted_gross_minus_fee(110, 10, 0) == 100
    assert net_present_value(110, 0, "0.10") == 100
    f, g = affine(2, 3), affine(4, 5)
    assert compose(f, g)(1) == 21
    assert compose(g, f)(1) == 25
    assert compose(f, g)(F(1, 2)) == 17
    h = affine(3, -1)
    for x in (0, 1, F(5, 2)):
        assert compose(f, compose(g, h))(x) == compose(compose(f, g), h)(x)
    must_raise(ValueError, gross_after_fee, 10, 11)
    must_raise(ValueError, gross_after_fee, -1, 0)
    must_raise(ValueError, net_present_value, 100, 20, -1)
    must_raise(ValueError, net_present_value, 100, 20, -2)
    must_raise(TypeError, q, True)
    must_raise(TypeError, q, 0.1)
    print("PASS: Section 3.3 reference checks")


if __name__ == "__main__":
    run()
