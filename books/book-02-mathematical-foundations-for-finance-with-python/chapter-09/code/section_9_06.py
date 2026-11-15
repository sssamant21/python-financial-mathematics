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
    """Complete latent change/error report;full baseline eligibility retained.

    The baseline prerequisite includes per-cash derivatives even though this
    API returns only change fields. It is a documented range restriction.
    """
    items = validate_flows(flows)
    r,h = finite(rate,"rate"),finite(shock,"shock")
    portfolio_sensitivity(items,r)
    R,H = map(Fraction,(r,h))
    with localcontext(Context(prec=1700)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        def amount(C,exponent):
            if exponent > 10000:
                raise ValueError("parallel report outside finite float range")
            return Decimal(0) if exponent < -10000 else dec(C)*dec(exponent).exp()
        exact = first = second = Decimal(0)
        for c,t in items:
            C,T = map(Fraction,(c,t));baseline = amount(C,-T*R)
            endpoint = amount(C,-T*(R+H));TT = dec(T)
            exact += endpoint-baseline;first -= TT*baseline;second += TT*TT*baseline
        HH = dec(H);linear = first*HH;quadratic = linear+second*HH*HH/2
        return {"shock":h,"exact_change":_sensitivity_float(exact),
                "linear_change":_sensitivity_float(linear),
                "quadratic_change":_sensitivity_float(quadratic),
                "linear_error":_sensitivity_float(exact-linear),
                "quadratic_error":_sensitivity_float(exact-quadratic)}

def spot_curve_sensitivity(flows, spot_rates):
    """Finite positive value, per-spot derivatives and finite aggregate first.

    Form complete cash-weighted terms before float conversion; a bare
    discount factor need not fit float because it is not a returned field.
    """
    items = validate_flows(flows)
    rates = [finite(x,"spot_rate") for x in spot_rates]
    if len(items)!=len(rates):
        raise ValueError("one spot rate is required per cash flow")
    with localcontext(Context(prec=1500)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        value = Decimal(0); derivatives = []
        for (c,t),z in zip(items,rates):
            C,T,Z = map(Fraction,(c,t,z));exponent = -Z*T
            if exponent > 10000:
                raise ValueError("spot report outside finite float range")
            amount = Decimal(0) if exponent < -10000 else dec(C)*dec(exponent).exp()
            value += amount;derivatives.append(-dec(T)*amount)
        reported_value = _sensitivity_float(value)
        if reported_value <= 0:
            raise ValueError("valuation must report positive")
        return {"value":reported_value,
                "spot_derivatives":[_sensitivity_float(x) for x in derivatives],
                "parallel_first":_sensitivity_float(sum(derivatives,Decimal(0)))}

def spot_shock(flows, spot_rates, shocks):
    """Complete latent change/error report, retaining spot-curve eligibility."""
    items = validate_flows(flows)
    rates = [finite(z,"spot_rate") for z in spot_rates]
    bumps = [finite(h,"shock") for h in shocks]
    if len(items)!=len(rates) or len(items)!=len(bumps):
        raise ValueError("rates and shocks must match cash-flow count")
    spot_curve_sensitivity(items,rates)
    with localcontext(Context(prec=1700)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        def amount(C,exponent):
            if exponent > 10000:
                raise ValueError("spot shock outside finite float range")
            return Decimal(0) if exponent < -10000 else dec(C)*dec(exponent).exp()
        exact = linear = Decimal(0)
        for (c,t),z,h in zip(items,rates,bumps):
            C,T,Z,H = map(Fraction,(c,t,z,h))
            baseline = amount(C,-Z*T);endpoint = amount(C,-T*(Z+H))
            exact += endpoint-baseline;linear -= dec(T)*baseline*dec(H)
        return {"exact_change":_sensitivity_float(exact),
                "linear_change":_sensitivity_float(linear),
                "linear_error":_sensitivity_float(exact-linear)}

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
