"""Section 7.3: continuity and discontinuity examples."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def removable(x, extended=False):
    x = finite(x, "x")
    if type(extended) is not bool:
        raise TypeError("extended must be bool")
    if x == 3 and not extended:
        raise ValueError("original expression undefined at x=3")
    return x + 3

def jump(x):
    x = finite(x, "x")
    return 2.0 if x < 5 else 7.0

def reciprocal(x):
    x = finite(x, "x")
    if x == 2:
        raise ValueError("reciprocal undefined at x=2")
    return 1/(x-2)

def oscillating(x):
    x = finite(x, "x")
    if x == 0:
        raise ValueError("sin(1/x) undefined at x=0")
    return math.sin(1/x)

def threshold_fee(amount):
    amount = finite(amount, "amount")
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    return 5.0 if amount < 1000 else 10.0

def continuous_kink(amount):
    amount = finite(amount, "amount")
    if amount < 0:
        raise ValueError("amount must be nonnegative")
    return 0.01*max(amount-1000, 0)

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

def approach(function, point, steps=(0.1, 0.01, 0.001)):
    a = finite(point, "point")
    rows = []
    for step in steps:
        h = finite(step, "step")
        if h <= 0:
            raise ValueError("step must be positive")
        left, right = a-h, a+h
        if left == a or right == a:
            raise ValueError("step too small to represent distinct inputs")
        rows.append((left, function(left), right, function(right)))
    return rows

if __name__ == "__main__":
    for label, function, point in (
        ("removable", removable, 3),
        ("jump", jump, 5),
        ("infinite", reciprocal, 2),
        ("fee", threshold_fee, 1000),
        ("kink", continuous_kink, 1000),
    ):
        print(label)
        for row in approach(function, point):
            print(" ", row)
    print("annuity-factor zero-rate extension:", annuity_factor(0, 5))
