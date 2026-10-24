"""Reference checks for Section 4.1."""
from fractions import Fraction as F
from section_4_01 import (rational, future_value, cumulative_change,
                          linear_value, implied_rate)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    assert future_value(100, "1/10", 0) == 100
    assert future_value(100, "1/10", 1) == 110
    assert future_value(100, "1/10", 2) == 121
    assert future_value(1000, "1/20", 3) == F(9261,8)
    assert future_value(500, "-1/5", 3) == 256
    assert cumulative_change("1/20", 3) == F(1261,8000)
    assert cumulative_change("-1/5", 3) == F(-61,125)
    assert linear_value(100, 10, 2) == 120
    assert future_value(0, "1/10", 3) == 0
    assert implied_rate(100, 121, 2) == {"kind": "exact", "rate": F(1,10)}
    assert implied_rate(100, 200, 2)["kind"] == "not_rational"
    assert implied_rate(100, 81, 2) == {"kind": "exact", "rate": F(-1,10)}
    assert implied_rate(100, 100, 7) == {"kind": "exact", "rate": F(0)}
    for rate in ("-1/2", "-1/10", 0, "1/10", 2):
        for n in (1,2,3):
            final = future_value(100, rate, n)
            assert implied_rate(100, final, n)["rate"] == F(rate)
    rejects(ValueError, future_value, 100, -1, 2)
    rejects(ValueError, future_value, 100, 0, -1)
    rejects(ValueError, future_value, 100, 0, "1/2")
    rejects(ValueError, future_value, -1, 0, 2)
    rejects(ValueError, implied_rate, 0, 100, 2)
    rejects(ValueError, implied_rate, 100, 100, 0)
    rejects(TypeError, rational, 0.1)
    rejects(TypeError, rational, True)
    print("PASS: Section 4.1 reference checks")

if __name__ == "__main__":
    run()
