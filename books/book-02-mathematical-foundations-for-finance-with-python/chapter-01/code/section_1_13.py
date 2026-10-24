"""Check exact growth candidates and explicitly bounded float comparisons."""
import math
from section_1_12 import compound_balance, periodic_rate, rational


def audit_growth(*, principal, period_rate, periods, candidate):
    formula = compound_balance(principal=principal, period_rate=period_rate,
                               periods=periods)
    p = rational(principal)
    rate = periodic_rate(period_rate)
    observed = rational(candidate)
    reference = p
    for _ in range(periods):
        reference = reference + reference * rate
    recovered = observed / (1 + rate) ** periods
    direction_ok = observed >= p if rate >= 0 else observed <= p
    checks = {
        "formula_agreement": observed == formula,
        "recurrence_agreement": observed == reference,
        "round_trip": recovered == p,
        "nonnegative": observed >= 0,
        "direction_bound": direction_ok,
    }
    return {"candidate": observed, "reference": reference,
            "discrepancy": observed - reference, "checks": checks,
            "passed": all(checks.values())}


def finite_float(value):
    if type(value) not in (int, float):
        raise TypeError("use built-in int or float, excluding bool")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError("value exceeds the float interface") from exc
    if not math.isfinite(number):
        raise ValueError("comparison requires finite values")
    return number


def compare_finite(actual, reference, *, rel_tol, abs_tol):
    a, b = finite_float(actual), finite_float(reference)
    relative, absolute = finite_float(rel_tol), finite_float(abs_tol)
    if not 0 <= relative < 1 or absolute < 0:
        raise ValueError("require 0 <= rel_tol < 1 and abs_tol >= 0")
    return math.isclose(a, b, rel_tol=relative, abs_tol=absolute)


def main():
    inputs = dict(principal=100, period_rate="0.10", periods=2)
    good = audit_growth(candidate=121, **inputs)
    bad = audit_growth(candidate=110, **inputs)
    print(f"Correct candidate passed: {good['passed']}")
    print(f"Missing-period candidate passed: {bad['passed']}")
    print(f"Missing-period discrepancy: {bad['discrepancy']}")
    print(f"Weak bounds passed: {bad['checks']['nonnegative']} and "
          f"{bad['checks']['direction_bound']}")
    print("Float equality:", 0.1 + 0.2 == 0.3)
    print("Explicit close comparison:", compare_finite(
        0.1 + 0.2, 0.3, rel_tol=1e-12, abs_tol=0))
    print("Near zero, relative only:", compare_finite(
        1e-12, 0, rel_tol=1e-9, abs_tol=0))
    print("Near zero, absolute tolerance:", compare_finite(
        1e-12, 0, rel_tol=1e-9, abs_tol=1e-12))


if __name__ == "__main__":
    main()
