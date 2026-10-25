"""Reference checks for Section 6.6."""
import math
from section_6_06 import (
    finite, periods, level_perpetuity, growing_perpetuity,
    deferred_level, deferred_growing, level_tail, growing_tail,
    finite_level_pv, finite_growing_pv)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    close(level_perpetuity(100, 0.05), 2000)
    close(level_perpetuity(100, 0.05, "begin"), 2100)
    close(deferred_level(100, 0.05, 0), 2000)
    close(deferred_level(100, 0.05, 3), 2000 / 1.05**3)
    close(level_tail(100, 0.05, 10), 2000 / 1.05**10)
    close(growing_perpetuity(100, 0.02, 0.05), 100 / 0.03)
    close(deferred_growing(100, 0.02, 0.05, 3),
          (100 / 0.03) / 1.05**3)
    close(growing_tail(100, 0.02, 0.05, 5),
          (100 / 0.03) * (1.02 / 1.05)**5)
    for n in (0, 1, 3, 10, 25):
        close(finite_level_pv(100, 0.05, n) +
              level_tail(100, 0.05, n),
              level_perpetuity(100, 0.05))
        close(finite_growing_pv(100, 0.02, 0.05, n) +
              growing_tail(100, 0.02, 0.05, n),
              growing_perpetuity(100, 0.02, 0.05))
    close(growing_perpetuity(0, 0.05, 0.05), 0)
    rejects(ValueError, level_perpetuity, 100, 0)
    rejects(ValueError, level_perpetuity, 100, 0.05, "bad")
    rejects(ValueError, growing_perpetuity, 100, 0.05, 0.05)
    rejects(ValueError, growing_perpetuity, 100, 0.06, 0.05)
    rejects(ValueError, growing_perpetuity, 100, -1, 0.05)
    rejects(ValueError, periods, -1)
    rejects(TypeError, periods, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 6.6 reference checks")

if __name__ == "__main__":
    run()
