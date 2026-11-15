"""Section 9.6: discounted-value sensitivity under continuous compounding."""
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

def validate_flows(flows):
    items = list(flows)
    if not items:
        raise ValueError("at least one cash flow is required")
    clean = []
    for cash, years in items:
        c, t = finite(cash, "cash"), finite(years, "years")
        if c <= 0 or t < 0:
            raise ValueError("cash must be positive and years nonnegative")
        clean.append((c,t))
    return clean

def _sensitivity_float(value):
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("sensitivity report outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("sensitivity report outside finite float range")
    return result

def portfolio_sensitivity(flows, rate):
    """Complete baseline report;all scalar/list fields finite,total positive.

    Normalize latent derivatives/amounts,not separately rounded floats.
    Per-cash derivatives can impose a stricter range than total value alone.
    """
    r = finite(rate,"rate")
    items = validate_flows(flows)
    R = Fraction(r)
    with localcontext(Context(prec=1500)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        terms = [];cash_derivatives = [];value = first = second = Decimal(0)
        for c,t in items:
            C,T = map(Fraction,(c,t));exponent = -R*T
            if exponent > 10000:
                raise ValueError("sensitivity report outside finite float range")
            factor = Decimal(0) if exponent < -10000 else dec(exponent).exp()
            amount = dec(C)*factor;TT = dec(T)
            terms.append(amount);cash_derivatives.append(factor)
            value += amount;first -= TT*amount;second += TT*TT*amount
        reported_value = _sensitivity_float(value)
        if reported_value <= 0:
            raise ValueError("valuation must report positive")
        return {"value":reported_value,"first":_sensitivity_float(first),
                "second":_sensitivity_float(second),
                "duration":_sensitivity_float(-first/value),
                "convexity":_sensitivity_float(second/value),
                "cash_flow_derivatives":[_sensitivity_float(x) for x in cash_derivatives],
                "value_weights":[_sensitivity_float(x/value) for x in terms]}

def parallel_shock(flows, rate, shock):
    items = validate_flows(flows)
    r,h = finite(rate,"rate"),finite(shock,"shock")
    base = portfolio_sensitivity(items,r)
    terms = [c*math.exp(-r*t) for c,t in items]
    exact = math.fsum(v*math.expm1(-t*h) for (_,t),v in zip(items,terms))
    linear = base["first"]*h
    quadratic = linear+0.5*base["second"]*h*h
    if not all(math.isfinite(z) for z in (exact,linear,quadratic)):
        raise ValueError("nonfinite shock result")
    return {"shock":h,"exact_change":exact,"linear_change":linear,
            "quadratic_change":quadratic,
            "linear_error":exact-linear,"quadratic_error":exact-quadratic}

def spot_curve_sensitivity(flows, spot_rates):
    items = validate_flows(flows)
    rates = [finite(x,"spot_rate") for x in spot_rates]
    if len(items)!=len(rates):
        raise ValueError("one spot rate is required per cash flow")
    terms = [c*math.exp(-z*t) for (c,t),z in zip(items,rates)]
    value = math.fsum(terms)
    derivatives = [-t*v for (_,t),v in zip(items,terms)]
    if not all(math.isfinite(x) for x in [value,*derivatives]) or value <= 0:
        raise ValueError("nonfinite spot valuation")
    return {"value":value,"spot_derivatives":derivatives,
            "parallel_first":math.fsum(derivatives)}

def spot_shock(flows, spot_rates, shocks):
    items = validate_flows(flows)
    rates = [finite(z,"spot_rate") for z in spot_rates]
    bumps = [finite(h,"shock") for h in shocks]
    if len(items)!=len(rates) or len(items)!=len(bumps):
        raise ValueError("rates and shocks must match cash-flow count")
    base = spot_curve_sensitivity(items,rates)
    exact = math.fsum(c*math.exp(-z*t)*math.expm1(-t*h)
                      for (c,t),z,h in zip(items,rates,bumps))
    linear = math.fsum(d*h for d,h in zip(base["spot_derivatives"],bumps))
    if not math.isfinite(exact) or not math.isfinite(linear):
        raise ValueError("nonfinite spot shock")
    return {"exact_change":exact,"linear_change":linear,
            "linear_error":exact-linear}

if __name__ == "__main__":
    import json
    flows=[(100,1),(1100,2)]
    report={"single":portfolio_sensitivity([(10000,5)],0.04),
            "single_10bp":parallel_shock([(10000,5)],0.04,0.001),
            "portfolio":portfolio_sensitivity(flows,0.04),
            "parallel_50bp":parallel_shock(flows,0.04,0.005),
            "spot_curve":spot_curve_sensitivity(flows,[0.035,0.04]),
            "nonparallel":spot_shock(flows,[0.035,0.04],[0.001,-0.002])}
    print(json.dumps(report,indent=2,allow_nan=False))
