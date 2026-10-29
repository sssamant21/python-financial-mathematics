"""Section 8.9: analytic versus numerical derivative comparator."""
import json
import math

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
    forward = (fp-f0)/h
    backward = (f0-fm)/h
    centered = (fp-fm)/(2*h)
    half_centered = (fhp-fhm)/h
    richardson = (4*half_centered-centered)/3
    methods = {}
    for name, approx in (("forward",forward),("backward",backward),
                         ("centered",centered),("richardson",richardson)):
        approx = finite(approx, "derivative estimate")
        error = finite(approx-analytic_first, "signed derivative error")
        methods[name] = {"estimate":approx,"signed_error":error,
                         "absolute_error":abs(error),
                         "pass":abs(error) <= a+r*abs(analytic_first)}
    result = {"x":x,"step":h,"analytic_first":analytic_first,
              "abs_tol":a,"rel_tol":r,
              "comparison_rule":"abs(error) <= abs_tol + rel_tol*abs(analytic)",
              "first_derivatives":methods}
    if second is not None:
        analytic_second = evaluated(second, x)
        estimate = finite((fp-2*f0+fm)/(h*h), "second derivative estimate")
        error = finite(estimate-analytic_second, "signed second derivative error")
        result["second_derivative"] = {
            "analytic":analytic_second,"estimate":estimate,
            "signed_error":error,"absolute_error":abs(error),
            "pass":abs(error) <= a+r*abs(analytic_second)}
    return result

def step_ladder(function, first, x, steps, second=None,
                abs_tol=1e-5, rel_tol=1e-5):
    return [compare_derivatives(function, first, x, step, second,
                                abs_tol, rel_tol) for step in steps]

def accumulation_model():
    p, rate = 1000.0, 0.04
    f = lambda t:p*math.exp(rate*t)
    d1 = lambda t:rate*f(t)
    d2 = lambda t:rate*rate*f(t)
    return f, d1, d2, 5.0, "years"

def discounted_cash_flow_model():
    cash, years = 5000.0, 4.0
    f = lambda rate:cash*math.exp(-rate*years)
    d1 = lambda rate:-years*f(rate)
    d2 = lambda rate:years*years*f(rate)
    return f, d1, d2, 0.03, "decimal rate"

def profit_model():
    def check(q):
        if not 0 <= q <= 500:
            raise ValueError("quantity must be in [0,500]")
    def f(q):
        check(q)
        return -1000+80*q-0.25*q*q
    def d1(q):
        check(q)
        return 80-0.5*q
    def d2(q):
        check(q)
        return -0.5
    return f, d1, d2, 160.0, "units"

def ratio_model():
    def check(x):
        if x <= 0:
            raise ValueError("x must be positive")
    def f(x):
        check(x)
        return (100+8*x)/(50+3*x)
    def d1(x):
        check(x)
        return 100/(50+3*x)**2
    def d2(x):
        check(x)
        return -600/(50+3*x)**3
    return f, d1, d2, 2.0, "time units"

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
