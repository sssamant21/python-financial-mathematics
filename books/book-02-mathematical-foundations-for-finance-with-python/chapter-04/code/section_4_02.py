"""Section 4.2: natural exponential and logarithm in financial models.

Uses finite IEEE-754 floats; outputs are approximations, not exact fractions.
"""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be a real int or float (not bool)")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is too large for finite float conversion") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def continuous_value(initial, rate, time):
    initial, rate, time = (finite(initial, "initial"),
                           finite(rate, "rate"), finite(time, "time"))
    if initial < 0 or time < 0:
        raise ValueError("initial and time must be nonnegative")
    return initial * math.exp(rate * time)

def continuous_present_value(future, rate, time):
    future, rate, time = (finite(future, "future"),
                         finite(rate, "rate"), finite(time, "time"))
    if future < 0 or time < 0:
        raise ValueError("future and time must be nonnegative")
    return future * math.exp(-rate * time)

def continuous_rate(initial, final, time):
    initial, final, time = (finite(initial, "initial"),
                           finite(final, "final"), finite(time, "time"))
    if initial <= 0 or final <= 0 or time <= 0:
        raise ValueError("initial, final, and time must be positive")
    return math.log(final / initial) / time

def time_to_target(initial, target, rate):
    initial, target, rate = (finite(initial, "initial"),
                            finite(target, "target"), finite(rate, "rate"))
    if initial <= 0 or target <= 0:
        raise ValueError("initial and target must be positive")
    if rate == 0:
        raise ValueError("zero rate: no unique finite target time")
    time = math.log(target / initial) / rate
    if time < 0:
        raise ValueError("target is unreachable in nonnegative time at this rate")
    return time

def effective_rate(continuous_rate_per_period):
    rate = finite(continuous_rate_per_period, "continuous_rate_per_period")
    return math.expm1(rate)

def continuous_rate_from_effective(effective_rate_per_period):
    rate = finite(effective_rate_per_period, "effective_rate_per_period")
    if rate <= -1:
        raise ValueError("effective rate must exceed -1")
    return math.log1p(rate)

def main():
    print("Doubling time at 6%:", time_to_target(100, 200, 0.06))
    print("PV of 1000 in 3 years:", continuous_present_value(1000, 0.05, 3))
    print("Continuous rate equivalent to 10% effective:",
          continuous_rate_from_effective(0.10))

if __name__ == "__main__":
    main()
