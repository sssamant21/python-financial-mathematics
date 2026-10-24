"""Section 4.7 — stable numerical evaluation for financial growth."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def log_change(simple_return):
    r = finite(simple_return, "simple_return")
    if r <= -1:
        raise ValueError("simple return must exceed -1")
    return math.log1p(r)

def simple_change(log_return):
    return math.expm1(finite(log_return, "log_return"))

def cumulative_log_change(returns):
    return math.fsum(log_change(r) for r in returns)

def cumulative_simple_change(returns):
    return math.expm1(cumulative_log_change(returns))

def log_periodic_factor(nominal_rate, frequency, periods):
    rate = finite(nominal_rate, "nominal_rate")
    if type(frequency) is not int or frequency < 1:
        raise ValueError("frequency must be a positive integer")
    if type(periods) is not int or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    periodic_rate = rate / frequency
    if periodic_rate <= -1:
        raise ValueError("periodic factor must be positive")
    result = periods * math.log1p(periodic_rate)
    if not math.isfinite(result):
        raise OverflowError("log accumulation exceeds float range")
    return result

def effective_annual_rate(nominal_rate, frequency):
    return math.expm1(log_periodic_factor(nominal_rate, frequency, frequency))

def periodic_factor(nominal_rate, frequency, periods):
    return math.exp(log_periodic_factor(nominal_rate, frequency, periods))

def continuous_ear(rate):
    return math.expm1(finite(rate, "rate"))

def continuous_from_ear(ear):
    return log_change(ear)

if __name__ == "__main__":
    small = 1e-16
    print("Naive log:", math.log(1 + small))
    print("Stable log:", log_change(small))
    print("Monthly EAR at 12% nominal:", effective_annual_rate(0.12, 12))
    print("Cumulative return (+100%, -50%):",
          cumulative_simple_change((1.0, -0.5)))
