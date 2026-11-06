"""Scoped replication oracle: exact pivoted elimination on represented inputs."""
import json
import math
import sys
from fractions import Fraction as Q

import section_21_05 as lab
import section_21_09 as integrated


def oracle(matrix, target, threshold=1e-12):
    rows = [[Q(float(x)) for x in row] + [Q(float(y))]
            for row, y in zip(matrix, target)]
    scale = max(abs(x) for row in rows for x in row[:2])
    if not scale:
        raise ValueError
    first, second = sorted(rows, key=lambda row: abs(row[0]), reverse=True)
    if not first[0]:
        raise ValueError
    reduced = [b - (second[0] / first[0]) * a for a, b in zip(first, second)]
    screen = first[0] * reduced[1] / scale**2
    if first is rows[1]:
        screen = -screen
    if abs(screen) <= Q(threshold):
        raise ValueError
    second_holding = reduced[2] / reduced[1]
    holdings = (float((first[2] - first[1] * second_holding) / first[0]),
                float(second_holding))
    residuals = [float(sum(x * Q(h) for x, h in zip(row[:2], holdings)) - row[2])
                 for row in rows]
    return dict(solution=holdings, residual=tuple(residuals),
                normalized_determinant=float(screen), screening_threshold=threshold)


def outcome(fn):
    try:
        return fn()
    except (ValueError, TypeError, OverflowError) as exc:
        return {"error": type(exc).__name__}


def main():
    largest = sys.float_info.max
    tiny = math.ulp(0.0)
    p = math.nextafter(.5, 1)
    q = math.nextafter(p, 1)
    cases = [
        ("screen_equal", [[1, 0], [0, .125]], [3, .25], .125),
        ("screen_below", [[1, 0], [0, .125]], [3, .25], math.nextafter(.125, 0)),
        ("screen_above", [[1, 0], [0, .125]], [3, .25], math.nextafter(.125, 1)),
        ("pivot_and_sign", [[0, .125], [1, 0]], [.25, 3], 0),
        ("screen_rounded_zero", [[largest, 0], [0, tiny]], [largest, tiny], 0),
        ("near_dependence", [[.5, p], [p, q]], [p, q], 0),
        ("singular", [[.5, p], [1, 2*p]], [p, 2*p], 0),
        ("large_canceling_products", [[largest, largest], [largest, largest/2]],
         [0, largest], .01),
        ("exact_rounded_residual", [[3, 1], [1, 2]], [1, 0], 0),
        ("scaled_target_overflow", [[.5, .5], [.5, -.5]], [largest, 0], 0),
        ("true_holding_overflow", [[tiny, 0], [0, tiny]], [largest, 0], 0),
        ("tiny_system", [[2*tiny, tiny], [tiny, 3*tiny]], [3*tiny, 4*tiny], .01),
    ]
    rows = []
    def record(name, expected, actual):
        rows.append(dict(case=name, expected=expected, actual=actual, passed=expected == actual))
    for name, matrix, target, threshold in cases:
        record(name, outcome(lambda: oracle(matrix, target, threshold)),
               outcome(lambda: lab.solve_2x2(matrix, target, threshold=threshold)))
    report = integrated.build_report()
    record("integrated_replication", dict(inputs=dict(matrix=[[1, 1], [1, 2]], target=[3, 5]),
                                         **oracle([[1, 1], [1, 2]], [3, 5])),
           report["replication"])
    record("report_path_and_status", (True, "not run", "pending", "pending"),
           (integrated.solve_2x2 is lab.solve_2x2, report["validation_execution"],
            report["independent_review"], report["approval"]))
    print(json.dumps(rows, allow_nan=False, indent=2))
    assert all(row["passed"] for row in rows)


if __name__ == "__main__":
    main()
