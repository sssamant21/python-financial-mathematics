"""Section 7.6: stable small-change limits and financial approximations."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def log_quotient(h):
    h = finite(h, "h")
    if h <= -1:
        raise ValueError("h must exceed -1")
    return 1.0 if h == 0 else math.log1p(h)/h

def exp_quotient(h):
    h = finite(h, "h")
    if h == 0:
        return 1.0
    value = math.expm1(h)/h
    if not math.isfinite(value):
        raise OverflowError("exponential quotient overflow")
    return value

def power_quotient(h, exponent):
    h = finite(h, "h")
    a = finite(exponent, "exponent")
    if h <= -1:
        raise ValueError("h must exceed -1")
    if h == 0:
        return a
    logarithm = math.log1p(h)
    argument = a*logarithm
    # Factor the quotient into continuous near-zero ratios so a*h rounding
    # to zero does not erase a nonzero limiting exponent.
    exponential_ratio = 1.0 if argument == 0 else math.expm1(argument)/argument
    value = a*(logarithm/h)*exponential_ratio
    if not math.isfinite(value):
        raise OverflowError("power quotient overflow")
    return value

def sin_quotient(h):
    h = finite(h, "h")
    return 1.0 if h == 0 else math.sin(h)/h

def log_return(simple_return):
    r = finite(simple_return, "simple_return")
    if r <= -1:
        raise ValueError("simple return must exceed -1")
    return math.log1p(r)

def discount_relative_change(rate_shock, years):
    h = finite(rate_shock, "rate_shock")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    value = math.expm1(-h*t)
    if not math.isfinite(value):
        raise OverflowError("discount change overflow")
    return value

def discount_linear_approximation(rate_shock, years):
    h = finite(rate_shock, "rate_shock")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    return -h*t

def annuity_factor(rate, periods):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("rate must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    if periods == 0:
        return 0.0
    if r == 0:
        return float(periods)
    value = math.expm1(periods*math.log1p(r))/r
    if not math.isfinite(value):
        raise OverflowError("annuity factor overflow")
    return value

if __name__ == "__main__":
    for h in (0.1, 0.01, 1e-4, 1e-8, 0):
        print(f"h={h:.8g} log/h={log_quotient(h):.12f} exp/h={exp_quotient(h):.12f} power7/h={power_quotient(h,7):.12f}")
    print("log return at -2%:", log_return(-0.02))
    print("discount exact:", discount_relative_change(0.001, 5))
    print("discount linear:", discount_linear_approximation(0.001, 5))
    print("annuity zero-rate limit:", annuity_factor(0, 12))
