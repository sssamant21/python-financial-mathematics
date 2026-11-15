"""Section 9.5: Taylor remainder and guaranteed rate-shock bounds."""
import math
from fractions import Fraction
from decimal import Decimal, Context, localcontext

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

def _report_float(value):
    try:
        out = float(value)
    except OverflowError as exc:
        raise ValueError("report outside finite float range") from exc
    if not math.isfinite(out):
        raise ValueError("report outside finite float range")
    return out

def portfolio_report(flows, rate, shock):
    """Complete latent report;positive rounded baseline and finite final fields.

    Internal derivative maxima need not themselves fit float. Utilization
    uses latent error/bound;if the reported bound is zero,it remains None.
    """
    items = validated_flows(flows)
    r,h = finite(rate,"rate"),finite(shock,"shock")
    R,H = map(Fraction,(r,h))
    with localcontext(Context(prec=1700)):
        def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
        def amount(C,exponent):
            if exponent > 10000:
                raise ValueError("report outside finite float range")
            return Decimal(0) if exponent < -10000 else dec(C)*dec(exponent).exp()
        v = d1 = d2 = m2 = m3 = exact = Decimal(0)
        for c,t in items:
            C,T = map(Fraction,(c,t));baseline = amount(C,-R*T)
            endpoint = amount(C,-(R+H)*T)
            worst = amount(C,-min(R,R+H)*T)
            TT = dec(T)
            v += baseline;d1 -= TT*baseline;d2 += TT*TT*baseline
            m2 += TT*TT*worst;m3 += TT*TT*TT*worst
            exact += endpoint-baseline
        HH = dec(H);first = d1*HH;second = first+d2*HH*HH/2
        bound1 = m2*HH*HH/2;bound2 = m3*abs(HH)**3/6
        linear_error,quadratic_error = exact-first,exact-second
        values = (v,d1,d2,exact,first,second,linear_error,quadratic_error,bound1,bound2)
        out = [_report_float(x) for x in values]
        if out[0] <= 0:
            raise ValueError("nonpositive reported valuation")
        keys = ("baseline_value","first_derivative","second_derivative","exact_change",
                "linear_change","quadratic_change","linear_error","quadratic_error",
                "linear_bound","quadratic_bound")
        result = dict(zip(keys,out))
        result["linear_bound_utilization"] = None if out[8]==0 else _report_float(abs(linear_error)/bound1)
        result["quadratic_bound_utilization"] = None if out[9]==0 else _report_float(abs(quadratic_error)/bound2)
        return result

def single_report(cash, years, rate, shock):
    return portfolio_report([(cash,years)],rate,shock)

def polynomial_example(shock):
    """Round each complete represented-input expression once.

    All five fields must be finite;true range overflow raises ValueError.
    Exactly zero expressions report positive zero;nonzero underflow may
    retain a negative zero. Analytic remainder is not display subtraction.
    """
    h = finite(shock,"shock")
    H = Fraction(h)
    return {"exact":_report_float((2+H)**3),
            "linear":_report_float(8+12*H),
            "quadratic":_report_float(8+12*H+6*H*H),
            "quadratic_remainder":_report_float(H**3),
            "quadratic_bound":_report_float(abs(H)**3)}

if __name__ == "__main__":
    import json
    report = {
        "polynomial":polynomial_example(0.1),
        "single_10bp":single_report(10000,5,0.04,0.001),
        "single_minus_10bp":single_report(10000,5,0.04,-0.001),
        "portfolio_50bp":portfolio_report([(100,1),(1100,2)],0.04,0.005)}
    print(json.dumps(report,indent=2,allow_nan=False))
