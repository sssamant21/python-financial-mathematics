"""Reference checks for Section 6.7."""
import math
from section_6_07 import (
    finite, periods, infinite_value, partial_value, exact_tail,
    relative_error, minimum_terms_relative, perpetuity_tail,
    minimum_perpetuity_terms)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(infinite_value(1, 0.8), 5)
    close(partial_value(1, 0.8, 4), 2.952)
    close(exact_tail(1, 0.8, 4), 2.048)
    close(relative_error(0.8, 4), 0.4096)
    close(partial_value(1, 0.8, 4) + exact_tail(1, 0.8, 4),
          infinite_value(1, 0.8))
    for q in (-0.8, -0.5, 0, 0.1, 0.8, 0.95):
        for n in (0, 1, 2, 5, 20):
            close(partial_value(100, q, n) + exact_tail(100, q, n),
                  infinite_value(100, q))
    assert minimum_terms_relative(0, 0.01) == 1
    assert minimum_terms_relative(0.8, 0.01) == 21
    assert minimum_perpetuity_terms(0.05, 0.01) == 95
    close(perpetuity_tail(100, 0.05, 10), 2000 / 1.05**10)
    for q in (0.1, 0.5, 0.8, 0.99):
        for tolerance in (0.1, 0.01, 1e-6):
            n = minimum_terms_relative(q, tolerance)
            assert q**n <= tolerance * (1 + 1e-12)
            if n > 0:
                assert q**(n-1) > tolerance * (1 - 1e-12)
    rejects(ValueError, infinite_value, 1, 1)
    rejects(ValueError, infinite_value, 1, -1)
    rejects(ValueError, minimum_terms_relative, 0.8, 0)
    rejects(ValueError, minimum_terms_relative, 0.8, 1)
    rejects(ValueError, perpetuity_tail, 100, 0, 3)
    rejects(ValueError, periods, -1)
    rejects(TypeError, periods, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 6.7 reference checks")

if __name__ == "__main__":
    run()
