"""Section 4.4: periodic and continuous compounding.

Floating-point educational calculations; periodic time is a whole number of
completed compounding periods, not a fractional posting convention.
"""
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

def positive_frequency(value):
    if type(value) is not int:
        raise TypeError("frequency must be a positive integer")
    if value < 1:
        raise ValueError("frequency must be positive")
    return value

def periods_count(value):
    if type(value) is not int:
        raise TypeError("periods must be a nonnegative integer")
    if value < 0:
        raise ValueError("periods must be nonnegative")
    return value

def periodic_factor(nominal_rate, frequency, periods):
    rate = finite(nominal_rate, "nominal_rate")
    m = positive_frequency(frequency)
    n = periods_count(periods)
    periodic_rate = rate / m
    if periodic_rate <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    return math.exp(n * math.log1p(periodic_rate))

def periodic_future_value(principal, nominal_rate, frequency, periods):
    principal = finite(principal, "principal")
    if principal < 0:
        raise ValueError("principal must be nonnegative")
    return principal * periodic_factor(nominal_rate, frequency, periods)

def periodic_present_value(future, nominal_rate, frequency, periods):
    future = finite(future, "future")
    if future < 0:
        raise ValueError("future must be nonnegative")
    return future / periodic_factor(nominal_rate, frequency, periods)

def effective_annual_rate(nominal_rate, frequency):
    rate = finite(nominal_rate, "nominal_rate")
    m = positive_frequency(frequency)
    if rate / m <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    return math.expm1(m * math.log1p(rate / m))

def nominal_from_effective(effective_rate, frequency):
    rate = finite(effective_rate, "effective_rate")
    m = positive_frequency(frequency)
    if rate <= -1:
        raise ValueError("effective rate must exceed -1")
    return m * math.expm1(math.log1p(rate) / m)

def continuous_future_value(principal, continuous_rate, years):
    principal, rate, time = (finite(principal, "principal"),
                             finite(continuous_rate, "continuous_rate"),
                             finite(years, "years"))
    if principal < 0 or time < 0:
        raise ValueError("principal and years must be nonnegative")
    return principal * math.exp(rate * time)

def continuous_present_value(future, continuous_rate, years):
    future, rate, time = (finite(future, "future"),
                         finite(continuous_rate, "continuous_rate"),
                         finite(years, "years"))
    if future < 0 or time < 0:
        raise ValueError("future and years must be nonnegative")
    return future * math.exp(-rate * time)

def continuous_from_effective(effective_rate):
    rate = finite(effective_rate, "effective_rate")
    if rate <= -1:
        raise ValueError("effective rate must exceed -1")
    return math.log1p(rate)

def effective_from_continuous(continuous_rate):
    return math.expm1(finite(continuous_rate, "continuous_rate"))

def continuous_from_nominal(nominal_rate, frequency):
    rate = finite(nominal_rate, "nominal_rate")
    m = positive_frequency(frequency)
    if rate / m <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    return m * math.log1p(rate / m)

if __name__ == "__main__":
    for m in (1, 2, 4, 12):
        print(f"m={m:2d}, EAR={effective_annual_rate(0.12, m):.8%}")
    print("Continuous EAR:", f"{effective_from_continuous(0.12):.8%}")
    print("PV at 10% EAR:", continuous_present_value(1210, math.log1p(0.1), 2))
