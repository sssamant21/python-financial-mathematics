"""Section 4.8: conditioning, sensitivity, and model limitations."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float (not bool)")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def positive(value, name):
    result = finite(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result

def continuous_future_value(principal, rate, years):
    p = positive(principal, "principal")
    r = finite(rate, "rate")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    return p * math.exp(r * t)

def relative_fv_sensitivity_to_rate(years):
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    return t

def periodic_relative_fv_sensitivity(periodic_rate, periods):
    rate = finite(periodic_rate, "periodic_rate")
    if rate <= -1:
        raise ValueError("periodic factor must be positive")
    if type(periods) is not int or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    return periods / (1 + rate)

def implied_continuous_rate(initial, final, years):
    p = positive(initial, "initial")
    f = positive(final, "final")
    t = positive(years, "years")
    change = (f - p) / p
    log_ratio = math.log1p(change) if math.isfinite(change) and change > -1 else math.log(f) - math.log(p)
    return log_ratio / t

def implied_rate_sensitivity_to_final(final, years):
    f = positive(final, "final")
    t = positive(years, "years")
    return 1 / (t * f)

def implied_time(initial, final, rate):
    p = positive(initial, "initial")
    f = positive(final, "final")
    r = finite(rate, "rate")
    if r == 0:
        raise ValueError("zero rate cannot identify a unique time")
    change = (f - p) / p
    log_ratio = math.log1p(change) if math.isfinite(change) and change > -1 else math.log(f) - math.log(p)
    t = log_ratio / r
    if not math.isfinite(t) or t < 0:
        raise ValueError("target unreachable at nonnegative time")
    return t

def time_sensitivity_to_rate(initial, final, rate):
    t = implied_time(initial, final, rate)
    return -t / rate

def central_difference(function, x, step):
    x = finite(x, "x")
    h = positive(step, "step")
    if x + h == x or x - h == x:
        raise ValueError("step too small to perturb x")
    result = (function(x + h) - function(x - h)) / (2 * h)
    if not math.isfinite(result):
        raise OverflowError("finite difference is not finite")
    return result

if __name__ == "__main__":
    print("Rate sensitivity over 30 years:",
          relative_fv_sensitivity_to_rate(30))
    print("Implied continuous rate:",
          implied_continuous_rate(100, 150, 5))
    print("Time sensitivity:",
          time_sensitivity_to_rate(100, 150, 0.08))
