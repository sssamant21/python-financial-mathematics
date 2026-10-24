"""Reference checks for Section 5.5."""
import math
from section_5_05 import (
    finite, periods_value, equilibrium, deviation_balance, iterative_balance)

def close(a, b, rel=1e-11, absolute=1e-9):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=absolute), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    stable = equilibrium(-0.1, 50)
    assert stable["kind"] == "unique" and stable["stability"] == "attracting"
    close(stable["balance"], 500)
    unstable = equilibrium(0.02, -100)
    assert unstable["kind"] == "unique" and unstable["stability"] == "repelling"
    close(unstable["balance"], 5000)
    close(deviation_balance(5000, 0.02, -100, 20), 5000)
    close(deviation_balance(4000, 0.02, -100, 4), 3917.56784)
    close(deviation_balance(100, -0.1, 50, 4), 500-400*0.9**4)
    close(equilibrium(0.02, -100, "begin")["balance"], 5100)
    assert equilibrium(0, 0)["kind"] == "all_balances"
    assert equilibrium(0, 50)["kind"] == "none"
    close(deviation_balance(1000, 0, 0, 20), 1000)
    close(deviation_balance(1000, 0, 50, 20), 2000)
    for rate in (-0.3, -0.05, 0, 0.01, 0.2):
        for timing in ("end", "begin"):
            for n in (0, 1, 2, 5, 15):
                close(deviation_balance(800, rate, 30, n, timing),
                      iterative_balance(800, rate, 30, n, timing))
    rejects(ValueError, equilibrium, -1, 50)
    rejects(ValueError, equilibrium, 0.1, 50, "invalid")
    rejects(ValueError, deviation_balance, 1000, 0.1, 50, -1)
    rejects(TypeError, periods_value, True)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 5.5 reference checks")

if __name__ == "__main__":
    run()
