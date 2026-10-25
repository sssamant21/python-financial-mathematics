"""Section 7.2: one-sided limits and threshold behavior."""
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

def step(x):
    x = finite(x, "x")
    return 2.0 if x < 5 else 7.0

def matching_piecewise(x):
    x = finite(x, "x")
    return x + 1 if x < 2 else 3*x - 3

def threshold_fee(amount):
    a = finite(amount, "amount")
    if a < 0:
        raise ValueError("transaction amount must be nonnegative")
    return 5.0 if a < 1000 else 10.0

def removable(x):
    x = finite(x, "x")
    if x == 3:
        raise ValueError("original expression undefined at x=3")
    return x + 3

def approach(function, point, steps=(0.1, 0.01, 0.001)):
    a = finite(point, "point")
    rows = []
    for step_size in steps:
        h = finite(step_size, "step")
        if h <= 0:
            raise ValueError("steps must be positive")
        left, right = a-h, a+h
        if left == a or right == a:
            raise ValueError("step too small to represent distinct inputs")
        rows.append((left, function(left), right, function(right)))
    return rows

if __name__ == "__main__":
    for label, fn, point in (
        ("step", step, 5),
        ("matching", matching_piecewise, 2),
        ("fee", threshold_fee, 1000),
        ("removable", removable, 3),
    ):
        print(label, "at", point)
        for left, fl, right, fr in approach(fn, point):
            print(f"  left {left:.6f}: {fl:.6f}; right {right:.6f}: {fr:.6f}")
