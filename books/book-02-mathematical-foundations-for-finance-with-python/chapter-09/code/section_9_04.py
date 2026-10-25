"""Section 9.4: second-order Taylor approximation and rate convexity."""
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

def taylor_change(first, second, shock, order=2):
    d1, d2, h = finite(first,"first"), finite(second,"second"), finite(shock,"shock")
    if order not in (1,2):
        raise ValueError("order must be 1 or 2")
    return d1*h+(0.5*d2*h*h if order==2 else 0.0)

def single_cash_flow(cash, years, rate):
    c, t, r = finite(cash,"cash"), finite(years,"years"), finite(rate,"rate")
    if c <= 0 or t < 0:
        raise ValueError("cash must be positive and years nonnegative")
    v = c*math.exp(-r*t)
    if not math.isfinite(v) or v == 0:
        raise ValueError("discounted value must be finite and positive")
    return {"value":v,"first":-t*v,"second":t*t*v,"duration":t,"convexity":t*t}

def cash_flow_portfolio(cash_flows, rate):
    r = finite(rate,"rate")
    flows = list(cash_flows)
    if not flows:
        raise ValueError("at least one cash flow is required")
    v = first = second = 0.0
    for cash, years in flows:
        item = single_cash_flow(cash,years,r)
        v += item["value"]
        first += item["first"]
        second += item["second"]
    if not math.isfinite(v) or v <= 0:
        raise ValueError("portfolio value must be finite and positive")
    return {"value":v,"first":first,"second":second,
            "duration":-first/v,"convexity":second/v}

def single_shock(cash, years, rate, shock):
    h = finite(shock,"shock")
    base = single_cash_flow(cash,years,rate)
    v, d1, d2 = base["value"], base["first"], base["second"]
    exact = v*math.expm1(-finite(years,"years")*h)
    linear = taylor_change(d1,d2,h,1)
    quadratic = taylor_change(d1,d2,h,2)
    return {"shock":h,"exact_change":exact,"linear_change":linear,
            "quadratic_change":quadratic,"linear_error":exact-linear,
            "quadratic_error":exact-quadratic}

def portfolio_shock(cash_flows, rate, shock):
    h, r = finite(shock,"shock"), finite(rate,"rate")
    flows = list(cash_flows)
    base = cash_flow_portfolio(flows,r)
    exact = sum(single_cash_flow(c,t,r)["value"]*math.expm1(-t*h)
                for c,t in flows)
    linear = taylor_change(base["first"],base["second"],h,1)
    quadratic = taylor_change(base["first"],base["second"],h,2)
    return {"shock":h,"exact_change":exact,"linear_change":linear,
            "quadratic_change":quadratic,"linear_error":exact-linear,
            "quadratic_error":exact-quadratic}

if __name__ == "__main__":
    import json
    flows = [(100,1),(1100,2)]
    report = {"single":single_cash_flow(10000,5,0.04),
              "single_shocks":[single_shock(10000,5,0.04,h)
                               for h in (-0.01,-0.005,-0.001,0.001,0.005,0.01)],
              "portfolio":cash_flow_portfolio(flows,0.04),
              "portfolio_50bp":portfolio_shock(flows,0.04,0.005)}
    print(json.dumps(report,indent=2,allow_nan=False))
