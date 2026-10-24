"""Section 5.4: closed forms for first-order balance recurrences."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds finite float range") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be finite")
    return number

def periods_value(value):
    if type(value) is not int:
        raise TypeError("periods must be an integer")
    if value < 0:
        raise ValueError("periods must be nonnegative")
    return value

def annuity_factor(rate, periods):
    i = finite(rate, "rate")
    n = periods_value(periods)
    if i <= -1:
        raise ValueError("periodic factor must be positive")
    if n == 0:
        return 0.0
    if i == 0:
        return float(n)
    return math.expm1(n * math.log1p(i)) / i

def closed_balance(initial, rate, payment, periods, timing="end"):
    b = finite(initial, "initial")
    i = finite(rate, "rate")
    c = finite(payment, "payment")
    n = periods_value(periods)
    if i <= -1:
        raise ValueError("periodic factor must be positive")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    growth = math.exp(n * math.log1p(i))
    factor = annuity_factor(i, n)
    result = b * growth + c * factor * (1 if timing == "end" else 1+i)
    if not math.isfinite(result):
        raise OverflowError("balance exceeds finite float range")
    return result

def iterative_balance(initial, rates, payments, timing="end"):
    b = finite(initial, "initial")
    rate_values = tuple(finite(x, "rate") for x in rates)
    cash_flows = tuple(finite(x, "payment") for x in payments)
    if len(rate_values) != len(cash_flows):
        raise ValueError("rates and payments must have equal lengths")
    if timing not in ("end", "begin"):
        raise ValueError("timing must be 'end' or 'begin'")
    for i, c in zip(rate_values, cash_flows):
        if i <= -1:
            raise ValueError("periodic factor must be positive")
        b = (1+i)*b+c if timing == "end" else (b+c)*(1+i)
        if not math.isfinite(b):
            raise OverflowError("balance exceeds finite float range")
    return b

def variable_closed_balance(initial, rates, payments):
    """Independent product/sum representation for end-of-period cash flows."""
    b = finite(initial, "initial")
    rate_values = tuple(finite(x, "rate") for x in rates)
    cash_flows = tuple(finite(x, "payment") for x in payments)
    if len(rate_values) != len(cash_flows):
        raise ValueError("rates and payments must have equal lengths")
    if any(i <= -1 for i in rate_values):
        raise ValueError("periodic factor must be positive")
    factors = tuple(1+i for i in rate_values)
    total = b * math.prod(factors)
    for k, payment in enumerate(cash_flows):
        total += payment * math.prod(factors[k+1:])
    if not math.isfinite(total):
        raise OverflowError("balance exceeds finite float range")
    return total

if __name__ == "__main__":
    print("End-of-period closed form:", closed_balance(1000, 0.02, 100, 3))
    print("Beginning-of-period closed form:",
          closed_balance(1000, 0.02, 100, 3, timing="begin"))
    print("Iterative baseline:",
          iterative_balance(1000, (0.02,)*3, (100,)*3))
