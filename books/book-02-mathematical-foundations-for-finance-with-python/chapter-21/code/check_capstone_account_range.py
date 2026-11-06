"""Selected independent integrating-factor and exact limit checks."""
import json
import math
import sys
from decimal import Context, Decimal as D, localcontext
from unittest.mock import patch

import section_21_07 as lab
import section_21_09 as integrated


def oracle(initial, rate, flow, years):
    # Integrating factor: exp(rt) A(0) + u integral_0^t exp(rs) ds.
    # Exact float-to-Decimal conversion and enough precision for the
    # selected fixtures (including the smallest represented r*t).
    with localcontext(Context(prec=2700)):
        a, r, u, t = map(D, (initial, rate, flow, years))
        if not r:
            value = a + u*t
        else:
            g = (r*t).exp()
            value = a*g + u*(g-1)/r
        answer = float(value)
        if not math.isfinite(answer):
            return "OverflowError"
        return answer


def observe(args):
    try:
        return lab.transition(*args)
    except (OverflowError, ValueError, TypeError) as exc:
        return type(exc).__name__


def main():
    M = sys.float_info.max
    s = math.ulp(0.0)
    rows = []

    def record(case, expected, actual, inputs=None):
        same = expected == actual
        if same and isinstance(expected, float) and expected == 0:
            same = math.copysign(1., expected) == math.copysign(1., actual)
        rows.append(dict(case=case, inputs=inputs, expected=expected, actual=actual, passed=same))

    for name, args, expected in [
        ("zero_rate_cancel", (-M, 0., M, 2.), M),
        ("exact_equilibrium", (1., 1024., -1024., 1.), 1.),
        ("negative_exponent_product_overflow", (1., -M, M, 2.), 1.),
        ("zero_state_large_exponent", (0., M, 0., 2.), 0.),
        ("negative_limit_without_equilibrium", (0., -M, M, 2.), 1.),
        ("positive_exponent_product_overflow", (1., M, 0., 2.), "OverflowError"),
        # e^-6000 changes which side of the half-subnormal tie is reached.
        ("approach_half_from_above", (1., -2., s, 3000.), s),
        ("approach_half_from_below", (0., -2., s, 3000.), 0.),
        ("approach_negative_half", (-1., -2., -s, 3000.), -s),
        ("negative_underflow", (-1., -4., 0., 1500.), -0.),
        ("zero_time_preserves_sign", (-0., M, M, 0.), -0.),
        ("invalid_horizon", (1., .1, 0., -1.), "ValueError"),
        ("boolean_flow", (1., .1, True, 1.), "TypeError"),
    ]:
        record(name, expected, observe(args), args)
    for name, args in [
        ("small_initial_large_growth", (s, 750., 0., 1.)),
        ("small_flow_large_growth", (0., 760., s, 1.)),
        ("large_initial_tiny_growth", (M, -760., 0., 1.)),
        ("large_factor_finite_flow", (0., 0.5, s, 1420.)),
        ("drift_cancellation", (1e307, 1., math.nextafter(-1e307, 0.), 25.)),
        ("tiny_exponent_rounded_zero", (0., s, M, .25)),
        ("zero_rate_round_once", (-1., 0., math.nextafter(1., 2.), math.nextafter(1., 0.))),
        ("zero_rate_tie", (0., 0., s, .5)),
        ("true_zero_rate_overflow", (M, 0., M, 1.)),
        ("true_positive_overflow", (1., 800., 0., 1.)),
        ("ordinary_unconstrained", (100., .125, -40., 4.)),
        ("large_negative_flow_factor", (0., -1., -M, M)),
        ("moderate_exponent_negative_underflow", (-s, -2., 0., 1.)),
    ]:
        record(name, oracle(*args), observe(args), args)

    account = integrated.build_report()["account"]
    expected = {
        "model": "constant-coefficient unconstrained account",
        "inputs": {"initial": 1000, "rate": 0, "flow": 200, "years": 3},
        "units": {"initial": "currency", "rate": "per year", "flow": "currency per year",
                  "years": "years"},
        "ending_balance": oracle(1000, 0, 200, 3),
        "boundary_policy": "unconstrained; negative balances allowed",
        "validation_execution": "not run", "independent_review": "pending", "approval": "pending",
    }
    record("integrated_account_field", expected, account)
    record("integrated_callable", True, integrated.scenario_report is lab.scenario_report)
    with patch.object(lab, "transition", side_effect=OverflowError("account failure")):
        try:
            integrated.build_report()
        except OverflowError as exc:
            actual = str(exc)
        else:
            actual = "returned a report"
    record("account_failure_propagates", "account failure", actual)
    print(json.dumps(rows, allow_nan=False, indent=2))
    assert all(row["passed"] for row in rows)


if __name__ == "__main__":
    main()
