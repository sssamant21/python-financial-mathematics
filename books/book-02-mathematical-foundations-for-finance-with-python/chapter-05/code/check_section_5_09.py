"""Reference checks for Section 5.9."""
import math
from section_5_09 import (
    Period, finite, run_engine, reconcile, closed_form_reference)

def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-11, abs_tol=1e-10), (a, b)

def rejects(error, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    scenario = (Period(0.02, 100), Period(-0.01, -50), Period(0.03, 0))
    result = run_engine(1000, scenario, allow_negative=False)
    close(result.closing, 1090.564)
    assert result.first_rejected is None
    close(*reconcile(result))
    close(closed_form_reference(1000, scenario), result.closing)
    begin = run_engine(1000, scenario, "begin")
    close(begin.closing, 1093.1184)
    close(closed_form_reference(1000, scenario, "begin"), begin.closing)
    close(*reconcile(begin))
    withdrawals = (Period(0.01, -200),)*3
    rejected = run_engine(500, withdrawals, allow_negative=False)
    assert rejected.first_rejected == 3
    assert len(rejected.ledger) == 3
    close(rejected.closing, 109.1305)
    assert rejected.ledger[-1]["applied"] == 0
    assert not rejected.ledger[-1]["accepted"]
    close(*reconcile(rejected))
    end = run_engine(100, (Period(0.1, -105),), allow_negative=False)
    start = run_engine(100, (Period(0.1, -105),), "begin", False)
    close(end.closing, 5)
    assert end.first_rejected is None
    assert start.first_rejected == 1
    close(start.closing, 100)
    close(*reconcile(start))
    exact = run_engine(1000, (Period(0, -250),)*4, allow_negative=False)
    close(exact.closing, 0)
    assert exact.first_rejected is None
    empty = run_engine(100, ())
    close(empty.closing, 100)
    close(closed_form_reference(100, ()), 100)
    for timing in ("end", "begin"):
        for n in range(6):
            periods = tuple(Period(0.02, 20) for _ in range(n))
            calculated = run_engine(100, periods, timing)
            close(calculated.closing, closed_form_reference(100, periods, timing))
            close(*reconcile(calculated))
    rejects(ValueError, run_engine, -1, (), "end", False)
    rejects(ValueError, run_engine, 100, (Period(-1, 0),))
    rejects(ValueError, run_engine, 100, (), "bad")
    rejects(TypeError, run_engine, 100, (), "end", 1)
    rejects(TypeError, run_engine, 100, (object(),))
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 5.9 reference checks")

if __name__ == "__main__":
    run()
