"""Section 9.9: chapter project for fixed-cash-flow valuation sensitivity."""
import json
import math
from fractions import Fraction
from decimal import Decimal, Context, localcontext

def finite(value, name):
    if type(value) not in (int, float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside finite float range") from exc
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
        clean.append((c, t))
    return clean

def baseline(flows, rate):
    items = validate_flows(flows)
    r = finite(rate, "rate")
    R = Fraction(r)
    with localcontext(Context(prec=1500)):
        def dec(value):
            return Decimal(value.numerator) / Decimal(value.denominator)
        def reported(value):
            result = float(value)
            if not math.isfinite(result):
                raise ValueError("baseline report outside finite float range")
            return result
        value = first = second = Decimal(0)
        amounts = []
        for cash, years in items:
            C, T = map(Fraction, (cash, years))
            exponent = -R * T
            if exponent > 10000:
                raise ValueError("baseline report outside finite float range")
            amount = Decimal(0) if exponent < -10000 else dec(C) * dec(exponent).exp()
            TT = dec(T)
            value += amount
            first -= TT * amount
            second += TT * TT * amount
            amounts.append(amount)
        v = reported(value)
        if v <= 0:
            raise ValueError("baseline value must report positive")
        return {"value": v, "first": reported(first), "second": reported(second),
                "duration": reported(-first / value),
                "convexity": reported(second / value),
                "terms": [reported(x) for x in amounts]}

def scenario(flows, rate, shock_bp):
    items = validate_flows(flows)
    r = finite(rate, "rate")
    bp = finite(shock_bp, "shock_bp")
    h = bp / 10000.0
    shifted_rate = finite(r + h, "shifted rate")
    base = baseline(items, r)
    # Keep the finite reported shifted-rate gate above, but form the
    # mathematical endpoint and bounds from exact represented R + H.
    R, H = map(Fraction, (r, h))
    with localcontext(Context(prec=1700)):
        def dec(value):
            return Decimal(value.numerator) / Decimal(value.denominator)
        def amount(C, exponent):
            if exponent > 10000:
                raise ValueError("scenario report outside finite float range")
            return Decimal(0) if exponent < -10000 else dec(C) * dec(exponent).exp()
        def reported(value):
            result = float(value)
            if not math.isfinite(result):
                raise ValueError("scenario report outside finite float range")
            return result
        value = shifted = first = second = bound1 = bound2 = Decimal(0)
        HH = dec(H)
        low = min(R, R + H)
        for cash, years in items:
            C, T = map(Fraction, (cash, years))
            TT = dec(T)
            v = amount(C, -R * T)
            value += v
            shifted += amount(C, -(R + H) * T)
            first -= TT * v
            second += TT * TT * v
            worst = amount(C, -low * T)
            bound1 += TT * TT * worst * HH * HH / 2
            bound2 += TT * TT * TT * worst * abs(HH) ** 3 / 6
        exact = shifted - value
        linear = first * HH
        quadratic = linear + second * HH * HH / 2
        error1, error2 = exact - linear, exact - quadratic
        data = {"shock_bp": bp, "shock_decimal": h,
                "exact_change": reported(exact),
                "linear_change": reported(linear),
                "quadratic_change": reported(quadratic),
                "exact_value": reported(shifted),
                "linear_error": reported(error1),
                "quadratic_error": reported(error2),
                "absolute_linear_error": reported(abs(error1)),
                "absolute_quadratic_error": reported(abs(error2)),
                "linear_bound": reported(bound1),
                "quadratic_bound": reported(bound2)}
    # Retain the existing reported-error/bound allowance policy; this is
    # not certification of a latent mathematical bound or floating error.
    allowance = 1e-12 * max(1.0, abs(base["value"]))
    data["linear_bound_pass"] = data["absolute_linear_error"] <= data["linear_bound"] + allowance
    data["quadratic_bound_pass"] = data["absolute_quadratic_error"] <= data["quadratic_bound"] + allowance
    return data

def project_report(flows, rate, shock_grid_bp):
    items = validate_flows(flows)
    r = finite(rate, "rate")
    grid = [finite(bp, "shock_bp") for bp in shock_grid_bp]
    if not grid or 0.0 not in grid or not any(bp < 0 for bp in grid) or not any(bp > 0 for bp in grid):
        raise ValueError("grid must include zero, negative, and positive shocks")
    base = baseline(items, r)
    rows = [scenario(items, r, bp) for bp in grid]
    passed = all(row["linear_bound_pass"] and row["quadratic_bound_pass"]
                 for row in rows)
    return {"model": "positive fixed cash flows",
            "rate_convention": "decimal annual continuously compounded",
            "baseline_rate": r,
            "cash_flows": [{"cash": c, "years": t} for c, t in items],
            "baseline_value": base["value"],
            "first_derivative": base["first"],
            "second_derivative": base["second"],
            "duration": base["duration"],
            "convexity": base["convexity"],
            "scenarios": rows,
            "validation": {"in_model_bound_checks_pass": passed,
                           "runtime_certified": False,
                           "independent_review_completed": False},
            "limitations": [
                "Fixed positive cash flows; no optionality or credit effects",
                "Flat continuously compounded annual discount rate",
                "Floating-point rounding not included in mathematical Taylor bounds",
                "Educational model; not production pricing software"]}

if __name__ == "__main__":
    sample = [(120, 0.5), (120, 1), (120, 2), (1120, 3)]
    report = project_report(sample, 0.04,
                            [-100, -50, -25, -10, 0, 10, 25, 50, 100])
    print(json.dumps(report, indent=2, allow_nan=False))
