"""Book 02 Section 9.3: first-order Taylor approximation."""
import math
from fractions import Fraction
from decimal import Decimal, Context, localcontext

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

def _report_fraction(exact):
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("Taylor report outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("Taylor report outside finite float range")
    return result

def linear_taylor(value, derivative, shock):
    v, d, h = finite(value,"value"), finite(derivative,"derivative"), finite(shock,"shock")
    exact = Fraction(v)+Fraction(d)*Fraction(h)
    if exact == 0:
        return v+d*h
    return _report_fraction(exact)

def compare_change(function, derivative, baseline, shock):
    if not callable(function) or not callable(derivative):
        raise TypeError("function and derivative must be callable")
    x, h = finite(baseline,"baseline"), finite(shock,"shock")
    point = x+h
    if not math.isfinite(point):
        raise ValueError("shocked point must be finite")
    v0 = finite(function(x),"baseline value")
    v1 = finite(function(point),"shocked value")
    slope = finite(derivative(x),"derivative")
    V,W,D,H = map(Fraction,(v0,v1,slope,h))
    exact, approx = W-V, D*H
    error = exact-approx
    return {"baseline_value":v0, "exact_change":_report_fraction(exact),
            "linear_change":_report_fraction(approx), "linear_value":_report_fraction(V+approx),
            "signed_error":_report_fraction(error), "absolute_error":_report_fraction(abs(error)),
            "relative_change_error":None if exact == 0 else _report_fraction(abs(error)/abs(exact))}

def discount_value(cash_flow, years, rate):
    c, t, r = finite(cash_flow,"cash_flow"), finite(years,"years"), finite(rate,"rate")
    if c <= 0 or t < 0:
        raise ValueError("cash_flow must be positive and years nonnegative")
    if t == 0:
        return c
    exponent = -Fraction(t)*Fraction(r)
    # A finite binary64 coefficient cannot rescue these exponent bounds.
    if exponent > 10000:
        raise ValueError("discounted value outside finite float range")
    if exponent < -10000:
        return 0.0
    with localcontext(Context(prec=1300)):
        power = Decimal(exponent.numerator)/Decimal(exponent.denominator)
        result = float(Decimal(c)*power.exp())
    if not math.isfinite(result):
        raise ValueError("discounted value outside finite float range")
    return result

def discount_shock(cash_flow, years, rate, shock):
    c, t, r, h = (finite(v,n) for v,n in
                  ((cash_flow,"cash_flow"),(years,"years"),
                   (rate,"rate"),(shock,"shock")))
    v0 = discount_value(c,t,r)
    C,T,R,H = map(Fraction,(c,t,r,h))
    power, z = -T*R, -T*H
    if z == 0:
        zero = -t*0.0*h
        return {"baseline_value":v0, "exact_change":zero,
                "linear_change":zero, "linear_value":v0+zero,
                "signed_error":0.0, "absolute_error":0.0,
                "relative_change_error":None}
    with localcontext(Context(prec=1700)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        def report(value):
            result = float(value)
            if not math.isfinite(result):
                raise ValueError("shock report outside finite float range")
            return result
        def amount(coefficient, exponent):
            if coefficient == 0:
                return float(coefficient)
            if exponent > 10000:
                raise ValueError("shock report outside finite float range")
            if exponent < -10000:
                return -0.0 if coefficient < 0 else 0.0
            return report(coefficient*dec(exponent).exp())
        dc, dz = Decimal(c), dec(z)
        # B*(exp(z)-1) and B*(exp(z)-1-z),scaled before float reporting.
        if z > 0:
            damp = Decimal(0) if z > 10000 else (-dz).exp()
            delta_factor = 1-damp
            error_factor = 1-(1+dz)*damp
            exact = amount(dc*delta_factor,power+z)
            error = amount(dc*error_factor,power+z)
        else:
            w = -dz
            damp = Decimal(0) if -z > 10000 else (-w).exp()
            delta_factor = 1-damp
            error_factor = w-delta_factor
            exact = amount(-dc*delta_factor,power)
            error = amount(dc*error_factor,power)
        approx = amount(dc*dz,power)
        linear = amount(dc*(1+dz),power)
        relative = report(error_factor/delta_factor)
    return {"baseline_value":v0, "exact_change":exact,
            "linear_change":approx, "linear_value":linear,
            "signed_error":error, "absolute_error":abs(error),
            "relative_change_error":relative}

def discount_step_ladder(cash_flow, years, rate, steps):
    return [{"shock":finite(h,"shock"),
             **discount_shock(cash_flow,years,rate,h)} for h in steps]

def revenue(quantity):
    q = finite(quantity,"quantity")
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return 40*q-0.1*q*q

def revenue_derivative(quantity):
    q = finite(quantity,"quantity")
    if q < 0:
        raise ValueError("quantity must be nonnegative")
    return 40-0.2*q

if __name__ == "__main__":
    import json
    report = {
        "quadratic":compare_change(lambda x:x*x,lambda x:2*x,3,0.2),
        "discount_10bp":discount_shock(10000,5,0.04,0.001),
        "discount_ladder":discount_step_ladder(10000,5,0.04,
                                             (0.01,0.005,0.001,0.0001)),
        "revenue":compare_change(revenue,revenue_derivative,100,5)}
    print(json.dumps(report,indent=2,allow_nan=False))
