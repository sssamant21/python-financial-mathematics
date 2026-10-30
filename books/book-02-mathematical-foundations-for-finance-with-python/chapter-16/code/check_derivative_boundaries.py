"""Selected exact-polynomial and finite-step contracts for Sections 16.2-16.4.

Run from chapter-16/code; no third-party dependencies. These checks establish
selected arithmetic contracts, not accuracy for arbitrary callbacks or steps.
"""
from fractions import Fraction
import math

from section_16_02 import centered_difference
from section_16_03 import centered_second_difference as second_03
from section_16_04 import centered_second_difference as second_04


def rejected(call, exception=ValueError):
    try:
        call()
    except exception:
        return
    raise AssertionError(f"expected {exception.__name__}")


def check():
    # Guard cases run first so the original silent collapse is a retained failure.
    guards = 0
    for helper in (centered_difference, second_03, second_04):
        for x, h in ((1.0, 1e-20), (1e308, 1e308), (0.0, 1e308)):
            calls = []
            def constant(t):
                calls.append(t)
                return 1.0
            rejected(lambda: helper(constant, x, h))
            assert calls == [], "invalid stencil must be rejected before callbacks"
            guards += 1
        for h in (0.0, -1.0, math.inf, math.nan):
            rejected(lambda: helper(lambda t: t, 0.0, h))
            guards += 1
        rejected(lambda: helper(lambda t: t, 0.0, True), TypeError)
        guards += 1
        for output in (math.inf, math.nan, True):
            rejected(lambda: helper(lambda t: output, 0.0, 0.125),
                     TypeError if output is True else ValueError)
            guards += 1
    for helper in (second_03, second_04):
        rejected(lambda: helper(lambda t: 1.0, 0.0, 1e-200))
        guards += 1

    # Exact dyadic cubic: D_h x^3 = 3*x^2 + h^2. Quartic:
    # D_h^2 x^4 = 12*x^2 + 2*h^2. All operations here fit exactly.
    references = 0
    x = Fraction(1, 2)
    for power in (6, 7, 8):
        h = Fraction(1, 2**power)
        first = centered_difference(lambda t: t*t*t, float(x), float(h))
        assert Fraction(first) == 3*x*x + h*h
        references += 1
        for helper in (second_03, second_04):
            second = helper(lambda t: t**4, float(x), float(h))
            assert Fraction(second) == 12*x*x + 2*h*h
            references += 1
    # Positive h may produce distinct but unequal represented offsets. The API
    # still divides by requested 2*h, not the actual endpoint distance.
    h = 3 * 2.0**-53
    xp, xm = 1.0+h, 1.0-h
    assert xp-1.0 != 1.0-xm
    assert centered_difference(lambda t: t, 1.0, h) == (xp-xm)/(2*h)
    # Endpoint arithmetic can be valid while the callback-derived result is not.
    rejected(lambda: centered_difference(lambda t: math.copysign(1e308,t), 0.0, 0.5))
    for helper in (second_03, second_04):
        rejected(lambda: helper(lambda t: -1e308 if t == 0 else 1e308, 0.0, 0.5))
    return {"guard_cases": guards, "exact_polynomial_pairs": references,
            "unequal_offset_cases": 1, "nonfinite_result_cases": 3}


if __name__ == "__main__":
    print(check())
