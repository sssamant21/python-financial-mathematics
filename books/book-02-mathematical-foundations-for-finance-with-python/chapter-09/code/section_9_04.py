"""Section 9.4: second-order Taylor approximation and rate convexity."""
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

def taylor_change(first, second, shock, order=2):
    d1, d2, h = finite(first,"first"), finite(second,"second"), finite(shock,"shock")
    if type(order) is not int:
        raise TypeError("order must be a built-in integer")
    if order not in (1,2):
        raise ValueError("order must be 1 or 2")
    A,B,H = map(Fraction,(d1,d2,h))
    exact = A*H+(B*H*H/2 if order==2 else 0)
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("Taylor change outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("Taylor change outside finite float range")
    return result

def _single_report(exact):
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError("single-flow report outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError("single-flow report outside finite float range")
    return result

def _single_amount(coefficient, exponent, zero=0.0):
    if coefficient == 0:
        return zero
    if exponent > 10000:
        raise ValueError("single-flow report outside finite float range")
    if exponent < -10000:
        return -0.0 if coefficient < 0 else 0.0
    if exponent == 0:
        return _single_report(coefficient)
    with localcontext(Context(prec=1300)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        return _single_report(dec(coefficient)*dec(exponent).exp())

def single_cash_flow(cash, years, rate):
    c, t, r = finite(cash,"cash"), finite(years,"years"), finite(rate,"rate")
    if c <= 0 or t < 0:
        raise ValueError("cash must be positive and years nonnegative")
    C,T,R = map(Fraction,(c,t,r))
    exponent = -R*T
    v = _single_amount(C,exponent)
    if v == 0:
        raise ValueError("discounted value must be finite and positive")
    first = _single_amount(-T*C,exponent,zero=-t*0.0)
    second = _single_amount(T*T*C,exponent)
    convexity = _single_report(T*T)
    return {"value":v,"first":first,"second":second,"duration":t,"convexity":convexity}

def cash_flow_portfolio(cash_flows, rate):
    """Report complete positive-flow sums; per-leg normalized fields are unused.

    All five final fields must be finite and the rounded total value positive.
    A leg whose value rounds to zero is eligible if the complete total qualifies.
    """
    r = finite(rate,"rate")
    flows = list(cash_flows)
    if not flows:
        raise ValueError("at least one cash flow is required")
    with localcontext(Context(prec=1300)):
        def dec(x):
            q = Fraction(x)
            return Decimal(q.numerator)/Decimal(q.denominator)
        v = first = second = Decimal(0)
        for cash, years in flows:
            c, t = finite(cash,"cash"), finite(years,"years")
            if c <= 0 or t < 0:
                raise ValueError("cash must be positive and years nonnegative")
            C,T,R = map(Fraction,(c,t,r))
            exponent = -T*R
            # Positive cash/derivative magnitudes cannot cancel. These bounds
            # exceed every finite binary64 coefficient C, TC and T^2 C.
            if exponent > 10000:
                raise ValueError("portfolio report outside finite float range")
            if exponent < -10000:
                continue
            amount = dec(C)*dec(exponent).exp()
            horizon = dec(T)
            v += amount
            first -= horizon*amount
            second += horizon*horizon*amount
        value = _single_report(v)
        if value <= 0:
            raise ValueError("portfolio value must be finite and positive")
        return {"value":value,"first":_single_report(first),
                "second":_single_report(second),
                "duration":_single_report(-first/v),
                "convexity":_single_report(second/v)}

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
