"""Reference checks for Section 5.6."""
import math
from section_5_06 import (
    finite, nonnegative_int, classify, equilibrium, deviation,
    periods_to_tolerance, half_life, shock_effect)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    assert classify(0.9, 50) == "attracting"
    assert classify(1.1, -100) == "repelling"
    assert classify(-1, 50) == "oscillatory_neutral"
    assert classify(1, 0) == "neutral"
    assert classify(1, 50) == "no_fixed_point"
    close(equilibrium(0.9, 50), 500)
    close(equilibrium(1.02, -100), 5000)
    assert equilibrium(1, 50) is None
    close(deviation(0.9, -400, 3), -400*0.9**3)
    close(deviation(0.8, 20, 5), 6.5536)
    assert periods_to_tolerance(0.9, -400, 10) == 36
    assert periods_to_tolerance(0.8, 10, 10) == 0
    assert periods_to_tolerance(0, 10, 1) == 1
    assert periods_to_tolerance(0.5, 8, 1) == 3
    close(half_life(0.9), math.log(0.5)/math.log(0.9))
    close(shock_effect(1.02, 100, 2, 5), 106.1208)
    close(shock_effect(1.02, 100, 2, 1), 0)
    close(shock_effect(1.02, 100, 2, 2), 100)
    rejects(ValueError, periods_to_tolerance, 1, 10, 1)
    rejects(ValueError, periods_to_tolerance, 0.5, 10, 0)
    rejects(ValueError, half_life, 1)
    rejects(ValueError, shock_effect, 1.02, 100, 0, 5)
    rejects(TypeError, nonnegative_int, True, "periods")
    rejects(TypeError, finite, True, "q")
    rejects(ValueError, finite, float("nan"), "q")
    print("PASS: Section 5.6 reference checks")

if __name__ == "__main__":
    run()
