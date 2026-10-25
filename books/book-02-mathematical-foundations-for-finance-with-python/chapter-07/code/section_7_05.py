"""Section 7.5: exponential limits and continuous compounding."""
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

def periodic_factor(nominal_rate, periods_per_year, years):
    j = finite(nominal_rate, "nominal_rate")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    if type(periods_per_year) is not int:
        raise TypeError("periods_per_year must be an integer")
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    if 1+j/periods_per_year <= 0:
        raise ValueError("periodic base must be positive")
    value = math.exp(periods_per_year*t*math.log1p(j/periods_per_year))
    if not math.isfinite(value):
        raise OverflowError("periodic accumulation overflow")
    return value

def continuous_factor(continuous_rate, years):
    delta = finite(continuous_rate, "continuous_rate")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    value = math.exp(delta*t)
    if not math.isfinite(value):
        raise OverflowError("continuous accumulation overflow")
    return value

def effective_from_continuous(continuous_rate):
    delta = finite(continuous_rate, "continuous_rate")
    result = math.expm1(delta)
    if not math.isfinite(result):
        raise OverflowError("effective rate overflow")
    return result

def continuous_from_effective(effective_rate):
    rate = finite(effective_rate, "effective_rate")
    if rate <= -1:
        raise ValueError("effective rate must exceed -1")
    return math.log1p(rate)

def continuous_discount(continuous_rate, years):
    delta = finite(continuous_rate, "continuous_rate")
    t = finite(years, "years")
    if t < 0:
        raise ValueError("years must be nonnegative")
    value = math.exp(-delta*t)
    if not math.isfinite(value):
        raise OverflowError("discount factor overflow")
    return value

def present_value(amount, continuous_rate, years):
    amount = finite(amount, "amount")
    result = amount*continuous_discount(continuous_rate, years)
    if not math.isfinite(result):
        raise OverflowError("present value overflow")
    return result

def relative_error(nominal_rate, periods_per_year, years):
    discrete = periodic_factor(nominal_rate, periods_per_year, years)
    continuous = continuous_factor(nominal_rate, years)
    return abs(discrete/continuous-1)

if __name__ == "__main__":
    for m in (1, 2, 4, 12, 365, 10000):
        print(f"m={m:5d} factor={periodic_factor(0.06,m,2):.12f} error={relative_error(0.06,m,2):.3e}")
    print("continuous value:", 1000*continuous_factor(0.06, 2))
    print("effective annual rate:", effective_from_continuous(0.06))
    print("discounted 500:", present_value(500, 0.03, 2))
