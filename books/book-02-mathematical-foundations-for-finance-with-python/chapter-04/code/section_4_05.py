"""Section 4.5 — Solving for time and growth rate.

Educational floating-point implementation; no settlement-grade rounding.
"""
import math

def real(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be an int or float (not bool)")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} cannot be represented as a finite float") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def positive(value, name):
    result = real(value, name)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result

def log_ratio(initial, final):
    initial = positive(initial, "initial")
    final = positive(final, "final")
    delta = (final - initial) / initial
    if math.isfinite(delta) and delta > -1:
        return math.log1p(delta)
    return math.log(final) - math.log(initial)

def periods_to_target(initial, target, periodic_rate):
    rate = real(periodic_rate, "periodic_rate")
    if rate <= -1 or rate == 0:
        raise ValueError("require periodic rate > -1 and nonzero")
    numerator = log_ratio(initial, target)
    periods = numerator / math.log1p(rate)
    if not math.isfinite(periods) or periods < 0:
        raise ValueError("target is unreachable in nonnegative time")
    return periods

def periodic_rate_from_values(initial, final, periods):
    n = positive(periods, "periods")
    return math.expm1(log_ratio(initial, final) / n)

def nominal_rate_from_values(initial, final, periods, frequency):
    if type(frequency) is not int:
        raise TypeError("frequency must be an integer")
    if frequency < 1:
        raise ValueError("frequency must be positive")
    return frequency * periodic_rate_from_values(initial, final, periods)

def continuous_time_to_target(initial, target, rate):
    rate = real(rate, "rate")
    if rate == 0:
        raise ValueError("zero rate does not identify a unique time")
    time = log_ratio(initial, target) / rate
    if not math.isfinite(time) or time < 0:
        raise ValueError("target is unreachable in nonnegative time")
    return time

def continuous_rate_from_values(initial, final, years):
    time = positive(years, "years")
    return log_ratio(initial, final) / time

def first_period_at_least(initial, target, periodic_rate):
    """First completed period for strictly positive growth and target >= initial.

    Checks adjacent integer candidates using logs to avoid overflow in powers.
    """
    initial = positive(initial, "initial")
    target = positive(target, "target")
    rate = real(periodic_rate, "periodic_rate")
    if rate <= 0:
        raise ValueError("requires positive periodic growth")
    if target < initial:
        raise ValueError("target must be at least initial")
    if target == initial:
        return 0
    step = math.log1p(rate)
    threshold = log_ratio(initial, target)
    guess = math.ceil(threshold / step)
    if guess < 0 or guess > 10**12:
        raise ValueError("period count exceeds supported numerical range")
    # Check neighboring candidates against the log threshold.
    while guess > 0 and (guess - 1) * step >= threshold:
        guess -= 1
    while guess * step < threshold:
        guess += 1
        if guess > 10**12:
            raise ValueError("period count exceeds supported numerical range")
    return guess

if __name__ == "__main__":
    print("Doubling time at 5%:", periods_to_target(1000, 2000, 0.05))
    print("First completed period:", first_period_at_least(1000, 2000, 0.05))
    print("Continuous rate over 5 years:", continuous_rate_from_values(100, 150, 5))
