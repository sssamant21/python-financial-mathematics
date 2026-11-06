"""Scoped allocation oracle via Decimal projection and represented-weight checks."""
import json
import math
import sys
from decimal import Decimal as D, localcontext

import section_21_06 as lab
import section_21_09 as integrated


def objective(w1, w2, a, b):
    exact = (D(w1) - D(a))**2 + (D(w2) - D(b))**2
    result = float(exact)
    if not math.isfinite(result):
        raise OverflowError
    return result


def diagnostics(w1, w2, tolerance):
    excess = D(w1) + D(w2) - 1
    violation = max(0., -w1, -w2)
    if not math.isfinite(float(excess)):
        raise OverflowError
    return dict(equality_residual=float(excess), long_only_violation=violation,
                tolerance=tolerance, feasible=abs(excess) <= D(tolerance)
                and violation <= tolerance)


def solve(a, b, tolerance=1e-12):
    # Orthogonal projection onto the line moves both coordinates equally.
    # If the resulting point is outside the segment, use the nearest endpoint.
    shift = (1 - D(a) - D(b)) / 2
    first, second = D(a) + shift, D(b) + shift
    weights = (0., 1.) if first <= 0 else (1., 0.) if second <= 0 else (
        float(first), float(second))
    return dict(weights=weights, objective=objective(*weights, a, b),
                diagnostics=diagnostics(*weights, tolerance),
                method="analytic solution for two-weight quadratic")


def outcome(fn):
    try:
        return fn()
    except (ValueError, TypeError, OverflowError) as exc:
        return {"error": type(exc).__name__}


def main():
    largest = sys.float_info.max
    near = math.nextafter(1., 0.)
    small = math.ldexp(1.25, -538)
    rows = []

    def record(name, expected, actual):
        rows.append(dict(case=name, expected=expected, actual=actual, passed=expected == actual))

    # Binary64 inputs, differences and squares fit in 2500 decimal digits.
    with localcontext() as ctx:
        ctx.prec = 2500
        for name, a, b, tol in [
            ("equal_large", 2.**100, 2.**100, 1e-12),
            ("equal_negative_large", -2.**100, -2.**100, 1e-12),
            ("small_second_weight", near, 0., 0.),
            ("small_first_weight", 0., near, 0.),
            ("upper_endpoint", 1., 0., 0.),
            ("lower_endpoint", 0., 1., 0.),
            ("above_upper_endpoint", math.nextafter(1., 2.), 0., 0.),
            ("below_lower_endpoint", 0., math.nextafter(1., 2.), 0.),
            ("true_objective_overflow", largest, -largest, 0.),
            ("ordinary_asymmetric", -.123, .643, 1e-12),
        ]:
            record(name, outcome(lambda: solve(a, b, tol)),
                   outcome(lambda: lab.solve(a, b, tol)))
        for name, args in [
            ("sum_recovers_subnormal", (0., 0., small, small)),
            ("objective_large_finite", (0., 0., 2.**511, 2.**511)),
            ("objective_true_overflow", (largest, 0., -largest, 0.)),
        ]:
            record(name, outcome(lambda: objective(*args)), outcome(lambda: lab.objective(*args)))
        for name, args in [
            ("positive_tolerance_rounding", (2., 2.**-54, 1.)),
            ("negative_tolerance_rounding", (0., -2.**-54, 1.)),
            ("exact_tolerance_equality", (1.25, -.125, .125)),
            ("large_opposite_weights", (largest, -largest, largest)),
            ("true_residual_overflow", (largest, largest, 1.)),
        ]:
            record(name, outcome(lambda: diagnostics(*args)), outcome(lambda: lab.diagnostics(*args)))
        report = integrated.build_report()
        record("integrated_allocation", dict(inputs=dict(target_a=.7, target_b=.2,
                    constraints="long-only; weights sum to one"), **solve(.7, .2)), report["allocation"])
        record("report_path_and_status", (True, "not run", "pending", "pending"),
               (integrated.solve is lab.solve, report["validation_execution"],
                report["independent_review"], report["approval"]))
    print(json.dumps(rows, allow_nan=False, indent=2))
    assert all(row["passed"] for row in rows)


if __name__ == "__main__":
    main()
