"""Section 8.8: numerical derivatives and step-size selection."""
import math
import sys

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def validated_step(x, step):
    x, h = finite(x, "x"), finite(step, "step")
    if h <= 0:
        raise ValueError("step must be positive")
    if x+h == x or x-h == x:
        raise ValueError("step is too small to perturb x in floating point")
    if not math.isfinite(x+h) or not math.isfinite(x-h):
        raise ValueError("step must produce finite perturbations")
    return x, h

def forward_difference(function, x, step):
    x, h = validated_step(x, step)
    return (finite(function(x+h), "f(x+h)")-finite(function(x), "f(x)"))/h

def backward_difference(function, x, step):
    x, h = validated_step(x, step)
    return (finite(function(x), "f(x)")-finite(function(x-h), "f(x-h)"))/h

def centered_difference(function, x, step):
    x, h = validated_step(x, step)
    if not math.isfinite(2*h):
        raise ValueError("central-difference denominator must be finite")
    return (finite(function(x+h), "f(x+h)")-finite(function(x-h), "f(x-h)"))/(2*h)

def second_difference(function, x, step):
    x, h = validated_step(x, step)
    if h*h==0 or not math.isfinite(h*h):
        raise ValueError("squared step must be finite and nonzero")
    return (finite(function(x+h), "f(x+h)")-2*finite(function(x), "f(x)")
            +finite(function(x-h), "f(x-h)"))/(h*h)

def suggested_step(x, derivative_order=1, scale=None):
    x = finite(x, "x")
    if type(derivative_order) is not int or derivative_order not in (1, 2):
        raise ValueError("derivative_order must be 1 or 2")
    s = max(1.0, abs(x)) if scale is None else finite(scale, "scale")
    if s <= 0:
        raise ValueError("scale must be positive")
    exponent = 1/3 if derivative_order == 1 else 1/4
    h = s*sys.float_info.epsilon**exponent
    validated_step(x, h)
    return h

def richardson_first(function, x, step):
    x, h = validated_step(x, step)
    coarse = centered_difference(function, x, h)
    fine = centered_difference(function, x, h/2)
    return (4*fine-coarse)/3

def discounted_price(cash_flow, years, rate):
    c, t, r = finite(cash_flow, "cash_flow"), finite(years, "years"), finite(rate, "rate")
    if c <= 0 or t < 0:
        raise ValueError("cash_flow must be positive and years nonnegative")
    return c*math.exp(-r*t)

def rate_sensitivity(cash_flow, years, rate, step):
    p = discounted_price(cash_flow, years, rate)
    function = lambda r: discounted_price(cash_flow, years, r)
    d1 = centered_difference(function, rate, step)
    d2 = second_difference(function, rate, step)
    return {"price": p, "duration": -d1/p, "convexity": d2/p,
            "analytic_duration": float(years),
            "analytic_convexity": float(years)**2}

if __name__ == "__main__":
    x, h = 2, 0.1
    f = lambda z:z**3
    print("Forward x^3:", forward_difference(f, x, h))
    print("Backward x^3:", backward_difference(f, x, h))
    print("Centered x^3:", centered_difference(f, x, h))
    print("Richardson x^3:", richardson_first(f, x, h))
    print("Suggested first step:", suggested_step(0.04, 1))
    print("Suggested second step:", suggested_step(0.04, 2))
    print("Rate sensitivities:", rate_sensitivity(1000, 5, 0.04, 1e-3))
