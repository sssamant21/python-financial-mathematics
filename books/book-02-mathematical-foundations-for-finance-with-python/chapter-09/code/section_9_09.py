"""Section 9.9: chapter project for fixed-cash-flow valuation sensitivity."""
import json
import math

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
    terms = [c * math.exp(-r * t) for c, t in items]
    value = math.fsum(terms)
    first = -math.fsum(t * v for (_, t), v in zip(items, terms))
    second = math.fsum(t * t * v for (_, t), v in zip(items, terms))
    if not all(math.isfinite(x) for x in (value, first, second)) or value <= 0:
        raise ValueError("nonfinite valuation or derivatives")
    return {"value": value, "first": first, "second": second,
            "duration": -first / value, "convexity": second / value,
            "terms": terms}

def scenario(flows, rate, shock_bp):
    items = validate_flows(flows)
    r = finite(rate, "rate")
    bp = finite(shock_bp, "shock_bp")
    h = bp / 10000.0
    shifted_rate = finite(r + h, "shifted rate")
    base = baseline(items, r)
    terms = base["terms"]
    exact = math.fsum(v * math.expm1(-t * h)
                      for (_, t), v in zip(items, terms))
    linear = base["first"] * h
    quadratic = linear + 0.5 * base["second"] * h * h
    # Revalue directly: baseline + change can cancel a representable small PV.
    exact_value = finite(math.fsum(c * math.exp(-shifted_rate * t)
                                  for c, t in items), "exact value")
    low_rate = min(r, shifted_rate)
    worst = [c * math.exp(-low_rate * t) for c, t in items]
    m2 = math.fsum(t * t * v for (_, t), v in zip(items, worst))
    m3 = math.fsum(t * t * t * v for (_, t), v in zip(items, worst))
    b1 = 0.5 * m2 * h * h
    b2 = m3 * abs(h) ** 3 / 6.0
    e1, e2 = exact - linear, exact - quadratic
    values = (exact, linear, quadratic, b1, b2, e1, e2)
    if not all(math.isfinite(x) for x in values):
        raise ValueError("nonfinite scenario output")
    allowance = 1e-12 * max(1.0, abs(base["value"]))
    return {"shock_bp": bp, "shock_decimal": h,
            "exact_change": exact, "linear_change": linear,
            "quadratic_change": quadratic,
            "exact_value": exact_value,
            "linear_error": e1, "quadratic_error": e2,
            "absolute_linear_error": abs(e1),
            "absolute_quadratic_error": abs(e2),
            "linear_bound": b1, "quadratic_bound": b2,
            "linear_bound_pass": abs(e1) <= b1 + allowance,
            "quadratic_bound_pass": abs(e2) <= b2 + allowance}

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
