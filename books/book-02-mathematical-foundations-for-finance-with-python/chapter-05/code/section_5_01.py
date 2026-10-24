"""Section 5.1: sequence indexing, time grids, and cash-flow timing."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number

def count(value):
    if type(value) is not int:
        raise TypeError("period count must be an integer")
    if value < 0:
        raise ValueError("period count must be nonnegative")
    return value

def time_grid(periods, years_per_period):
    n = count(periods)
    step = finite(years_per_period, "years_per_period")
    if step <= 0:
        raise ValueError("years_per_period must be positive")
    return [k * step for k in range(n + 1)]

def payment_for_period(payments, period):
    if type(period) is not int or period < 1:
        raise ValueError("payment period must be a positive integer")
    values = tuple(payments)
    if period > len(values):
        raise IndexError("payment period exceeds schedule")
    return finite(values[period - 1], f"payment[{period}]")

def balance_path(initial, periodic_rate, payments, timing="end"):
    initial = finite(initial, "initial")
    rate = finite(periodic_rate, "periodic_rate")
    if rate <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    values = tuple(finite(x, "payment") for x in payments)
    balances = [initial]
    for payment in values:
        previous = balances[-1]
        current = ((1 + rate) * previous + payment
                   if timing == "end"
                   else (previous + payment) * (1 + rate))
        if not math.isfinite(current):
            raise OverflowError("balance is outside finite float range")
        balances.append(current)
    return balances

def present_value_end_payments(payments, periodic_rate):
    rate = finite(periodic_rate, "periodic_rate")
    if rate <= -1:
        raise ValueError("periodic accumulation factor must be positive")
    values = tuple(finite(x, "payment") for x in payments)
    return math.fsum(payment / ((1 + rate) ** n)
                     for n, payment in enumerate(values, start=1))

if __name__ == "__main__":
    print("Monthly time grid:", time_grid(12, 1/12))
    print("End-of-period balances:", balance_path(1000, 0.01, (100, 100)))
    print("Beginning-of-period balances:",
          balance_path(1000, 0.01, (100, 100), timing="begin"))
