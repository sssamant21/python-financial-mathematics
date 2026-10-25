"""Book 02 Section 9.3: first-order Taylor approximation."""
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

def linear_taylor(value, derivative, shock):
    v, d, h = finite(value,"value"), finite(derivative,"derivative"), finite(shock,"shock")
    return v+d*h

def compare_change(function, derivative, baseline, shock):
    if not callable(function) or not callable(derivative):
        raise TypeError("function and derivative must be callable")
    x, h = finite(baseline,"baseline"), finite(shock,"shock")
    v0 = finite(function(x),"baseline value")
    v1 = finite(function(x+h),"shocked value")
    slope = finite(derivative(x),"derivative")
    exact = v1-v0
    approx = slope*h
    error = exact-approx
    return {"baseline_value":v0, "exact_change":exact,
            "linear_change":approx, "linear_value":linear_taylor(v0,slope,h),
            "signed_error":error, "absolute_error":abs(error),
            "relative_change_error":None if exact == 0 else abs(error)/abs(exact)}

def discount_value(cash_flow, years, rate):
    c, t, r = finite(cash_flow,"cash_flow"), finite(years,"years"), finite(rate,"rate")
    if c <= 0 or t < 0:
        raise ValueError("cash_flow must be positive and years nonnegative")
    return c*math.exp(-t*r)

def discount_shock(cash_flow, years, rate, shock):
    c, t, r, h = (finite(v,n) for v,n in
                  ((cash_flow,"cash_flow"),(years,"years"),
                   (rate,"rate"),(shock,"shock")))
    v0 = discount_value(c,t,r)
    exact = v0*math.expm1(-t*h)
    approx = -t*v0*h
    error = exact-approx
    return {"baseline_value":v0, "exact_change":exact,
            "linear_change":approx, "linear_value":v0+approx,
            "signed_error":error, "absolute_error":abs(error),
            "relative_change_error":None if exact == 0 else abs(error)/abs(exact)}

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
