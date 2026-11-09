"""Section 8.8: numerical derivatives and step-size selection."""
import math
import sys
from fractions import Fraction
from decimal import Context, Decimal, localcontext
from section_8_01 import _scaled_pv

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

def _difference_report(exact, zero=0.0):
    if exact == 0:
        return zero
    try:
        return finite(float(exact), "difference estimate")
    except OverflowError as exc:
        raise ValueError("difference estimate outside finite float range") from exc

def _pair_samples(function, first_x, last_x, denominator):
    first = finite(function(first_x), "first sample")
    last = finite(function(last_x), "last sample")
    exact = (Fraction(first)-Fraction(last))/denominator
    zero = first-last if first == last else 0.0
    return exact, zero

def forward_difference(function, x, step):
    x, h = validated_step(x, step)
    exact, zero = _pair_samples(function,x+h,x,Fraction(h))
    return _difference_report(exact,zero)

def backward_difference(function, x, step):
    x, h = validated_step(x, step)
    exact, zero = _pair_samples(function,x,x-h,Fraction(h))
    return _difference_report(exact,zero)

def centered_difference(function, x, step):
    x, h = validated_step(x, step)
    exact, zero = _pair_samples(function,x+h,x-h,2*Fraction(h))
    return _difference_report(exact,zero)

def second_difference(function, x, step):
    x, h = validated_step(x, step)
    samples = [Fraction(finite(function(z), "second-difference sample"))
               for z in (x+h,x,x-h)]
    return _difference_report((samples[0]-2*samples[1]+samples[2])/Fraction(h)**2)

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
    coarse, _ = _pair_samples(function,x+h,x-h,2*Fraction(h))
    # Preserve half-step validation after the two coarse samples.
    x, half = validated_step(x,h/2)
    fine, _ = _pair_samples(function,x+half,x-half,2*Fraction(half))
    return _difference_report((4*fine-coarse)/3)

def discounted_price(cash_flow, years, rate):
    c, t, r = finite(cash_flow, "cash_flow"), finite(years, "years"), finite(rate, "rate")
    if c <= 0 or t < 0:
        raise ValueError("cash_flow must be positive and years nonnegative")
    if t == 0:
        return c
    return _scaled_pv(Fraction(c), -Fraction(r)*Fraction(t))

def _normalized_report(value, name):
    try:
        return finite(float(value), name)
    except OverflowError as exc:
        raise ValueError(name+" outside finite float range") from exc

def rate_sensitivity(cash_flow, years, rate, step):
    p = discounted_price(cash_flow, years, rate)
    if p == 0:
        raise ValueError("positive representable price required for normalized sensitivities")
    r, h = validated_step(rate, step)
    t = finite(years, "years")
    analytic_convexity = _difference_report(Fraction(t)**2)
    if t == 0:
        return {"price":p,"duration":-0.0,"convexity":0.0,
                "analytic_duration":t,"analytic_convexity":analytic_convexity}
    # Model-normalized prices cancel the positive cash scale exactly.
    up_gap = -Fraction(t)*(Fraction(r+h)-Fraction(r))
    down_gap = -Fraction(t)*(Fraction(r-h)-Fraction(r))
    if down_gap > 10000:
        raise ValueError("normalized sensitivity outside finite float range")
    with localcontext(Context(prec=1600)):
        def dec(value):return Decimal(value.numerator)/Decimal(value.denominator)
        up = Decimal(0) if up_gap < -10000 else dec(up_gap).exp()
        down = dec(down_gap).exp()
        H = dec(Fraction(h))
        duration = _normalized_report(-(up-down)/(2*H), "duration")
        convexity = _normalized_report((up-2+down)/(H*H), "convexity")
    return {"price":p,"duration":duration,"convexity":convexity,
            "analytic_duration":t,"analytic_convexity":analytic_convexity}

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
