"""Reference checks for Section 6.3."""
import math
from section_6_03 import (
    finite, nonnegative_int, geometric_partial, geometric_infinite,
    geometric_remainder, perpetuity, perpetuity_tail)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(geometric_infinite(0.6), 2.5)
    close(geometric_infinite(0.8), 5)
    close(geometric_partial(0.8, 4), 2.952)
    close(geometric_remainder(0.8, 4), 2.048)
    close(geometric_partial(0.8, 4) +
          geometric_remainder(0.8, 4), geometric_infinite(0.8))
    close(geometric_infinite(-0.5), 2/3)
    close(geometric_remainder(-0.5, 3), -0.5**3 / 1.5)
    close(geometric_infinite(2, 0), 0)
    close(geometric_partial(1, 0), 0)
    close(geometric_partial(1, 4), 4)
    close(perpetuity(100, 0.05), 2000)
    close(perpetuity(100, 0.05, "begin"), 2100)
    close(perpetuity_tail(100, 0.05, 0), 2000)
    close(perpetuity_tail(100, 0.05, 10), 2000/(1.05**10))
    close(perpetuity(100, 0.05) - perpetuity_tail(100, 0.05, 10),
          100 * (1 - (1.05**-10)) / 0.05)
    rejects(ValueError, geometric_infinite, 1)
    rejects(ValueError, geometric_infinite, -1)
    rejects(ValueError, geometric_infinite, 1.01)
    rejects(ValueError, perpetuity, 100, 0)
    rejects(ValueError, perpetuity, 100, -0.01)
    rejects(ValueError, perpetuity, 100, 0.05, "bad")
    rejects(TypeError, nonnegative_int, True, "terms")
    rejects(ValueError, nonnegative_int, -1, "terms")
    rejects(TypeError, finite, True, "value")
    rejects(ValueError, finite, float("nan"), "value")
    print("PASS: Section 6.3 reference checks")

if __name__ == "__main__":
    run()
