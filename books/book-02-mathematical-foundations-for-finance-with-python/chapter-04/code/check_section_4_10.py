"""Reference checks for Chapter 04 integrated assessment."""
import math
from section_4_10 import (
    finite, periodic_future_value, effective_annual_rate,
    continuous_from_effective, continuous_future_value, doubling_periods,
    cumulative_log_return, cumulative_simple_return,
    implied_continuous_rate, relative_fv_change, answers)

def close(a, b, rel=1e-11, absolute=1e-10):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=absolute), (a, b)

def rejects(error, fn, *args):
    try:
        fn(*args)
    except error:
        return
    raise AssertionError("expected " + error.__name__)

def run():
    a = answers()
    close(a["quarterly_future_value"], 5000 * 1.02**12)
    close(a["quarterly_ear"], 1.02**4 - 1)
    close(a["present_value_at_10pct_ear"], 1000)
    close(a["continuous_rate_from_7pct_ear"], math.log1p(0.07))
    close(a["doubling_periods_at_6pct"], math.log(2)/math.log1p(0.06))
    assert math.ceil(a["doubling_periods_at_6pct"]) == 12
    close(a["implied_continuous_rate"], math.log(1.25)/4)
    close(a["three_period_simple_return"], 1.15 * 0.9 * 1.05 - 1)
    close(a["loss_recovery_return"], 1/0.7 - 1)
    close(a["sensitivity_exact_20yr_15bp"], math.expm1(0.03))
    close(cumulative_log_return((0.15, -0.1, 0.05)),
          math.log(1.15*0.9*1.05))
    close(cumulative_simple_return((-0.3, 1/0.7 - 1)), 0)
    close(periodic_future_value(1000, 0, 12, 36), 1000)
    close(continuous_future_value(1000, 0, 3), 1000)
    for ear in (-0.2, 0, 0.01, 0.07):
        rate = continuous_from_effective(ear)
        close(continuous_future_value(100, rate, 1), 100*(1+ear))
    close(effective_annual_rate(0.06, 12),
          math.expm1(12*math.log1p(0.06/12)))
    rejects(ValueError, periodic_future_value, 100, -1, 1, 1)
    rejects(ValueError, periodic_future_value, 100, 0.1, 0, 1)
    rejects(ValueError, periodic_future_value, 100, 0.1, 12, -1)
    rejects(ValueError, periodic_future_value, -100, 0.1, 12, 1)
    rejects(ValueError, continuous_from_effective, -1)
    rejects(ValueError, doubling_periods, 0)
    rejects(ValueError, cumulative_log_return, (-1,))
    rejects(ValueError, implied_continuous_rate, 100, 120, 0)
    rejects(ValueError, relative_fv_change, 0.01, -1)
    rejects(TypeError, finite, True, "x")
    rejects(ValueError, finite, float("nan"), "x")
    print("PASS: Section 4.10 integrated reference checks")

if __name__ == "__main__":
    run()
