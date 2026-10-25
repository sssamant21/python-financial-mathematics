"""Section 9.5: Taylor remainder and guaranteed rate-shock bounds."""
import math

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def validated_flows(flows):
    items = list(flows)
    if not items:
        raise ValueError("at least one cash flow required")
    result = []
    for c,t in items:
        c,t = finite(c,"cash"),finite(t,"years")
        if c <= 0 or t < 0:
            raise ValueError("cash must be positive and years nonnegative")
        result.append((c,t))
    return result

def portfolio_report(flows, rate, shock):
    items = validated_flows(flows)
    r,h = finite(rate,"rate"),finite(shock,"shock")
    rmin = min(r,r+h)
    v = d1 = d2 = m2 = m3 = exact = 0.0
    for c,t in items:
        baseline = c*math.exp(-r*t)
        worst = c*math.exp(-rmin*t)
        v += baseline
        d1 -= t*baseline
        d2 += t*t*baseline
        m2 += t*t*worst
        m3 += t*t*t*worst
        exact += baseline*math.expm1(-t*h)
    first = d1*h
    second = first+0.5*d2*h*h
    bound1 = 0.5*m2*h*h
    bound2 = m3*abs(h)**3/6
    values = (v,d1,d2,m2,m3,exact,first,second,bound1,bound2)
    if not all(math.isfinite(z) for z in values) or v <= 0:
        raise ValueError("nonfinite calculation or nonpositive valuation")
    return {"baseline_value":v,"first_derivative":d1,
            "second_derivative":d2,"exact_change":exact,
            "linear_change":first,"quadratic_change":second,
            "linear_error":exact-first,"quadratic_error":exact-second,
            "linear_bound":bound1,"quadratic_bound":bound2,
            "linear_bound_utilization":None if bound1==0 else abs(exact-first)/bound1,
            "quadratic_bound_utilization":None if bound2==0 else abs(exact-second)/bound2}

def single_report(cash, years, rate, shock):
    return portfolio_report([(cash,years)],rate,shock)

def polynomial_example(shock):
    h = finite(shock,"shock")
    exact = (2+h)**3
    linear = 8+12*h
    quadratic = linear+6*h*h
    return {"exact":exact,"linear":linear,"quadratic":quadratic,
            "quadratic_remainder":h**3,
            "quadratic_bound":abs(h)**3}

if __name__ == "__main__":
    import json
    report = {
        "polynomial":polynomial_example(0.1),
        "single_10bp":single_report(10000,5,0.04,0.001),
        "single_minus_10bp":single_report(10000,5,0.04,-0.001),
        "portfolio_50bp":portfolio_report([(100,1),(1100,2)],0.04,0.005)}
    print(json.dumps(report,indent=2,allow_nan=False))
