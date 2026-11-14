"""Section 8.9: analytic versus numerical derivative comparator."""
import json
import math
from fractions import Fraction
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

def evaluated(function, x):
    if not callable(function):
        raise TypeError("function must be callable")
    return finite(function(x), "function result")

def _report(exact, zero=0.0):
    if exact == 0:
        return zero
    try:
        return finite(float(exact), "derivative estimate")
    except OverflowError as exc:
        raise ValueError("derivative estimate outside finite float range") from exc

def _within_tolerance(error, absolute, relative, analytic):
    # Exact threshold for the represented finite report fields and controls.
    return abs(Fraction(error)) <= Fraction(absolute)+Fraction(relative)*abs(Fraction(analytic))

def compare_derivatives(function, first, x, step, second=None,
                        abs_tol=1e-5, rel_tol=1e-5):
    if not callable(first):
        raise TypeError("first derivative must be callable")
    if second is not None and not callable(second):
        raise TypeError("second derivative must be callable")
    x, h = finite(x, "x"), finite(step, "step")
    a, r = finite(abs_tol, "abs_tol"), finite(rel_tol, "rel_tol")
    if h <= 0 or a < 0 or r < 0:
        raise ValueError("step must be positive and tolerances nonnegative")
    if x+h == x or x-h == x or x+h/2 == x or x-h/2 == x:
        raise ValueError("step is too small to perturb x")
    if not math.isfinite(x+h) or not math.isfinite(x-h) or not math.isfinite(2*h):
        raise ValueError("perturbations and denominator must be finite")
    if second is not None and (h*h==0 or not math.isfinite(h*h)):
        raise ValueError("squared step must be finite and nonzero")
    f0, fp, fm = (evaluated(function, z) for z in (x, x+h, x-h))
    fhp, fhm = (evaluated(function, z) for z in (x+h/2, x-h/2))
    analytic_first = evaluated(first, x)
    F0, FP, FM, FHP, FHM = map(Fraction, (f0,fp,fm,fhp,fhm))
    H = Fraction(h)
    coarse, fine = (FP-FM)/(2*H), (FHP-FHM)/H
    forward = _report((FP-F0)/H, fp-f0 if fp == f0 else 0.0)
    backward = _report((F0-FM)/H, f0-fm if f0 == fm else 0.0)
    centered = _report(coarse, fp-fm if fp == fm else 0.0)
    richardson_zero = ((4*((fhp-fhm)/h)-(fp-fm)/(2*h))/3
                       if coarse == 0 and fine == 0 else 0.0)
    richardson = _report((4*fine-coarse)/3, richardson_zero)
    methods = {}
    for name, approx in (("forward",forward),("backward",backward),
                         ("centered",centered),("richardson",richardson)):
        approx = finite(approx, "derivative estimate")
        error = finite(approx-analytic_first, "signed derivative error")
        methods[name] = {"estimate":approx,"signed_error":error,
                         "absolute_error":abs(error),
                         "pass":_within_tolerance(error,a,r,analytic_first)}
    result = {"x":x,"step":h,"analytic_first":analytic_first,
              "abs_tol":a,"rel_tol":r,
              "comparison_rule":"abs(error) <= abs_tol + rel_tol*abs(analytic)",
              "first_derivatives":methods}
    if second is not None:
        analytic_second = evaluated(second, x)
        second_zero = (fp-2*f0+fm)/(h*h) if fp == f0 == fm == 0 else 0.0
        estimate = _report((FP-2*F0+FM)/(H*H),second_zero)
        error = finite(estimate-analytic_second, "signed second derivative error")
        result["second_derivative"] = {
            "analytic":analytic_second,"estimate":estimate,
            "signed_error":error,"absolute_error":abs(error),
            "pass":_within_tolerance(error,a,r,analytic_second)}
    return result

def step_ladder(function, first, x, steps, second=None,
                abs_tol=1e-5, rel_tol=1e-5):
    return [compare_derivatives(function, first, x, step, second,
                                abs_tol, rel_tol) for step in steps]

def accumulation_model():
    principal, rate = Fraction(1000), Fraction(0.04)
    def expression(t, order):
        t = finite(t, "years")
        return _scaled_pv(principal*rate**order,rate*Fraction(t))
    return (lambda t:expression(t,0),lambda t:expression(t,1),
            lambda t:expression(t,2),5.0,"years")

def discounted_cash_flow_model():
    def expression(rate, order):
        rate = finite(rate, "rate")
        return _scaled_pv(Fraction(5000)*Fraction(-4)**order,-4*Fraction(rate))
    return (lambda rate:expression(rate,0),lambda rate:expression(rate,1),
            lambda rate:expression(rate,2),0.03,"decimal rate")

def profit_model():
    def quantity(q):
        q = finite(q, "quantity")
        if not 0 <= q <= 500:
            raise ValueError("quantity must be in [0,500]")
        return Fraction(q)
    def f(q):
        q = quantity(q)
        return _report(-1000+80*q-q*q/4)
    def d1(q):
        return _report(80-quantity(q)/2)
    def d2(q):
        quantity(q)
        return -0.5
    return f,d1,d2,160.0,"units"

def ratio_model():
    def denominator(x):
        x = finite(x, "x")
        if x <= 0:
            raise ValueError("x must be positive")
        return Fraction(50)+3*Fraction(x)
    def f(x):
        d = denominator(x)
        # x=(d-50)/3; evaluate the complete rational expression.
        return _report((100+8*(d-50)/3)/d)
    def d1(x):
        return _report(Fraction(100)/denominator(x)**2)
    def d2(x):
        return _report(Fraction(-600)/denominator(x)**3)
    return f,d1,d2,2.0,"time units"

def run_demo():
    models = {
        "accumulation":accumulation_model(),
        "discounted_cash_flow":discounted_cash_flow_model(),
        "profit":profit_model(),
        "ratio":ratio_model()}
    report = {}
    for name, (f, d1, d2, x, unit) in models.items():
        report[name] = {"variable_unit":unit,
                        "comparisons":step_ladder(f,d1,x,
                          (1e-2,1e-3,1e-4,1e-5),d2)}
    return report

if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, allow_nan=False))
