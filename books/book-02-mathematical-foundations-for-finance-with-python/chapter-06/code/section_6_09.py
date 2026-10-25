"""Chapter 6 project: finite cash-flow valuation and independent verification."""
import math

def number(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def inputs(first_payment, growth, rate, periods, timing, kind):
    c, g, r = number(first_payment, "first_payment"), number(growth, "growth"), number(rate, "rate")
    if g <= -1 or r <= -1:
        raise ValueError("growth and discount rates must exceed -1")
    if type(periods) is not int:
        raise TypeError("periods must be an integer")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    if timing not in ("end", "begin") or kind not in ("pv", "fv"):
        raise ValueError("invalid valuation convention")
    return c, g, r, periods

def closed_form(first_payment, growth, rate, periods, kind="pv", timing="end"):
    c, g, r, n = inputs(first_payment, growth, rate, periods, timing, kind)
    if n == 0 or c == 0:
        return 0.0
    x = math.log1p(g) - math.log1p(r)
    factor = float(n) if x == 0 else math.expm1(n*x) / math.expm1(x)
    pv = c / (1+r) * factor
    result = pv if kind == "pv" else pv * math.exp(n*math.log1p(r))
    if timing == "begin":
        result *= 1+r
    if not math.isfinite(result):
        raise OverflowError("closed form overflowed")
    return result

def direct_sum(first_payment, growth, rate, periods, kind="pv", timing="end"):
    c, g, r, n = inputs(first_payment, growth, rate, periods, timing, kind)
    logg, logr = math.log1p(g), math.log1p(r)
    values = []
    for k in range(n):
        t = k + (1 if timing == "end" else 0)
        exponent = k*logg + ((-t) if kind == "pv" else (n-t))*logr
        values.append(c*math.exp(exponent))
    result = math.fsum(values)
    if not math.isfinite(result):
        raise OverflowError("direct sum overflowed")
    return result

def verify(first_payment, growth, rate, periods, timing="end", rel_tol=1e-10, abs_tol=1e-9):
    r = number(rate, "rate")
    results = {}
    for kind in ("pv", "fv"):
        analytic = closed_form(first_payment, growth, r, periods, kind, timing)
        enumerated = direct_sum(first_payment, growth, r, periods, kind, timing)
        if not math.isclose(analytic, enumerated, rel_tol=rel_tol, abs_tol=abs_tol):
            raise AssertionError(f"{kind} formula and cash flows differ: {analytic}, {enumerated}")
        results[kind] = analytic
    expected_fv = results["pv"] * math.exp(periods*math.log1p(r))
    if not math.isclose(results["fv"], expected_fv, rel_tol=rel_tol, abs_tol=abs_tol):
        raise AssertionError("PV/FV reconciliation failed")
    return results

def perpetuity(first_payment, growth, rate):
    c, g, r, _ = inputs(first_payment, growth, rate, 0, "end", "pv")
    if c == 0:
        return 0.0
    if r <= g:
        raise ValueError("nonzero perpetuity requires discount rate > growth")
    value = c/(r-g)
    if not math.isfinite(value):
        raise OverflowError("perpetuity overflowed")
    return value

def tail(first_payment, growth, rate, completed_periods):
    c, g, r, n = inputs(first_payment, growth, rate, completed_periods, "end", "pv")
    total = perpetuity(c, g, r)
    value = total*math.exp(n*(math.log1p(g)-math.log1p(r)))
    if not math.isfinite(value):
        raise OverflowError("tail overflowed")
    return value

def sample_report():
    for timing in ("end", "begin"):
        for growth, rate in ((0, 0), (0, 0.05), (0.02, 0.05), (0.05, 0.05)):
            results = verify(100, growth, rate, 5, timing)
            print(f"timing={timing} growth={growth} rate={rate} n=5 PV={results['pv']:.8f} FV={results['fv']:.8f} PASS")
    total = perpetuity(100, 0.02, 0.05)
    first_five = closed_form(100, 0.02, 0.05, 5)
    remainder = tail(100, 0.02, 0.05, 5)
    assert math.isclose(first_five+remainder, total, rel_tol=1e-11)
    print(f"growing perpetuity: total={total:.8f}, first5={first_five:.8f}, tail={remainder:.8f} PASS")

if __name__ == "__main__":
    sample_report()
