"""Section 7.1: limits, removable holes, and stable zero-rate factors."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def removable(x):
    """(x*x - 4)/(x-2), evaluated by its simplified form for x != 2."""
    x = finite(x, "x")
    if x == 2:
        raise ValueError("original rational function is undefined at x=2")
    return x + 2

def modified(x):
    """Function value 100 at x=2; nearby values approach 4."""
    x = finite(x, "x")
    return 100.0 if x == 2 else x + 2

def approach_table(center, steps=(0.1, 0.01, 0.001)):
    a = finite(center, "center")
    rows = []
    for step in steps:
        h = finite(step, "step")
        if h <= 0:
            raise ValueError("steps must be positive")
        left, right = a-h, a+h
        if left == a or right == a:
            raise ValueError("step too small to represent a distinct float")
        rows.append((left, left+2, right, right+2))
    return rows

def annuity_factor(rate, periods):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("effective rate must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    if periods == 0:
        return 0.0
    if r == 0:
        return float(periods)
    result = math.expm1(periods * math.log1p(r)) / r
    if not math.isfinite(result):
        raise OverflowError("annuity factor overflow")
    return result

def direct_factor(rate, periods):
    r = finite(rate, "rate")
    if r <= -1:
        raise ValueError("effective rate must exceed -1")
    if type(periods) is not int or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    return math.fsum((1+r)**k for k in range(periods))

if __name__ == "__main__":
    for left, fl, right, fr in approach_table(2):
        print(f"left {left:.6f}: {fl:.6f} | right {right:.6f}: {fr:.6f}")
    print("Modified function at x=2:", modified(2))
    for r in (0.05, 1e-4, 1e-8, 0):
        print(f"r={r:.8g}, A_5={annuity_factor(r, 5):.12f}")
