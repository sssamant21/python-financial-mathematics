"""Classical implication and explicit finite input-check schemas."""
import math


def implies(p, q):
    if type(p) is not bool or type(q) is not bool:
        raise TypeError("implication requires two Boolean values")
    return (not p) or q


def supported_finite(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def review_checks(checks, *, required):
    if type(required) not in (tuple, list) or not required:
        raise ValueError("declare a nonempty list or tuple of required names")
    if any(type(name) is not str or not name for name in required):
        raise ValueError("required names must be nonempty strings")
    if len(set(required)) != len(required):
        raise ValueError("required names must be unique")
    if type(checks) is not dict:
        raise TypeError("checks must be a dictionary")
    if set(checks) != set(required):
        raise ValueError("check names must exactly match the schema")
    if any(type(checks[name]) is not bool for name in required):
        raise TypeError("check results must be Boolean values")
    return {
        "passed": all(checks[name] for name in required),
        "failed": tuple(name for name in required if not checks[name]),
    }


def growth_inputs_report(*, principal, period_rate, periods):
    conditions = {
        "principal_domain": supported_finite(principal) and principal >= 0,
        "rate_domain": supported_finite(period_rate) and period_rate > -1,
        "period_domain": type(periods) is int and periods >= 0,
    }
    report = review_checks(
        conditions,
        required=("principal_domain", "rate_domain", "period_domain"),
    )
    return {"conditions": conditions, **report}


def main():
    for p, q in [(True, True), (True, False), (False, True), (False, False)]:
        print(f"{p} -> {q}: {implies(p, q)}")
    valid = growth_inputs_report(principal=1000, period_rate=0.04, periods=3)
    invalid = growth_inputs_report(principal=1000, period_rate=-1, periods=3)
    print(f"Valid inputs: {valid['passed']}")
    print(f"Invalid inputs accepted: {invalid['passed']}")
    print(f"Failed conditions: {invalid['failed']}")
    print(f"all([]): {all([])}")


if __name__ == "__main__":
    main()
