"""Educational continuous-discount sensitivity calculations."""
import math
from numbers import Real

def finite(x, name):
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError(f"{name} must be real, excluding bool")
    try: x = float(x)
    except OverflowError as exc: raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(x): raise ValueError(f"{name} must be finite")
    return x

def inputs(amount, rate, years):
    amount, rate, years = finite(amount, "amount"), finite(rate, "rate"), finite(years, "years")
    if years < 0: raise ValueError("years must be nonnegative")
    return amount, rate, years

def checked(x):
    if not math.isfinite(x): raise OverflowError("result exceeds float range")
    return x

def pv(amount, rate, years):
    amount, rate, years = inputs(amount, rate, years)
    try: result = amount * math.exp(-rate * years)
    except OverflowError as exc: raise OverflowError("discount factor exceeds float range") from exc
    return checked(result)

def derivatives(amount, rate, years):
    amount, rate, years = inputs(amount, rate, years)
    p = pv(amount, rate, years)
    first = checked(-years * p)
    second = checked(-years * first)
    return first, second

def central_difference(amount, rate, years, step):
    amount, rate, years = inputs(amount, rate, years)
    step = finite(step, "step")
    if step <= 0: raise ValueError("step must be positive")
    up, down = rate + step, rate - step
    if not math.isfinite(up) or not math.isfinite(down) or up == rate or down == rate:
        raise ValueError("step does not produce finite distinct perturbations")
    return checked((pv(amount, up, years) - pv(amount, down, years)) / (2 * step))

def approximations(amount, rate, years, change):
    change = finite(change, "change")
    base = pv(amount, rate, years)
    first, second = derivatives(amount, rate, years)
    linear = checked(base + first * change)
    quadratic = checked(linear + .5 * second * change * change)
    return linear, quadratic

if __name__ == "__main__":
    print("First and second derivatives:", derivatives(100, 0, 2))
    print("Approximations:", approximations(100, 0, 2, .01))
    print("Central difference:", central_difference(100, 0, 2, 1e-5))
