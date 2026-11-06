"""Independent fixed RK4 horizon, callback grid, and convergence checks."""
from fractions import Fraction as Q
import json
import math
import sys

from section_19_06 import fixed_rk4

D = math.ulp(0.)
M = sys.float_info.max


def outcome(fn):
    try:
        return fn()
    except ValueError as e:
        return str(e)


def main():
    rows = []
    def check(name, expected, actual, *, passed=None):
        rows.append(dict(case=name, expected=repr(expected), actual=repr(actual),
                         passed=expected == actual if passed is None else passed))

    # The grids are manually derived by rounding exact tick indices to even.
    # For the second case the exact ideal ticks are 0, 1.25, 2.5, 3.75, 5.
    for ticks, count, endpoints, midpoints in [
        (3, 2, (0, 2, 3), (1, 2)),
        (5, 4, (0, 1, 2, 4, 5), (0, 2, 3, 4)),
        (4, 2, (0, 2, 4), (1, 3)),
    ]:
        seen = []
        def constant(t, y):
            seen.append(t)
            return M
        horizon = ticks*D
        result = outcome(lambda: fixed_rk4(constant, 0., horizon, count))
        expected = dict(final_state=float(Q(M)*Q(horizon)), final_time=horizon,
                        steps=count, evaluations=4*count, status="completed")
        check(f"constant_report_{ticks}_{count}", expected, result)
        times = [i*D for l, m, r in zip(endpoints, midpoints, endpoints[1:])
                 for i in (l, m, m, r)]
        check(f"callback_times_{ticks}_{count}", times, seen)

    # Rounded endpoints can collapse even if a naive repeated step is nonzero.
    for ticks, count in [(2, 3), (1, 3)]:
        seen = []
        result = outcome(lambda: fixed_rk4(constant, 0., ticks*D, count))
        check(f"collapsed_grid_{ticks}", "fixed RK4 grid has non-increasing endpoints", result)
        check(f"collapsed_grid_no_callbacks_{ticks}", [], seen)

    seen = []
    result = fixed_rk4(constant, 7., 0., 3)
    check("zero_horizon", dict(final_state=7., final_time=0., steps=0,
                               evaluations=0, status="completed"), result)
    check("zero_horizon_no_callbacks", [], seen)
    check("bool_step_count", "invalid horizon or step count",
          outcome(lambda: fixed_rk4(constant, 0., 1., True)))
    check("negative_horizon", "invalid horizon or step count",
          outcome(lambda: fixed_rk4(constant, 0., -1., 3)))

    # State-independent y'=t^2 integrates to 1/3. At dyadic callback times
    # Simpson quadrature is exact apart from per-step state rounding.
    out = fixed_rk4(lambda t, y: t*t, 0., 1., 4)
    check("time_polynomial", 1./3., out["final_state"],
          passed=abs(out["final_state"]-1./3.) <= math.ulp(1./3.))
    # Ordinary non-dyadic grid: each step must end exactly where the next starts.
    seen = []
    def time_slope(t, y):
        seen.append(t)
        return t
    out = fixed_rk4(time_slope, 0., 1., 10)
    check("non_dyadic_contiguous_grid", [i/10 for i in range(1, 11)], seen[3::4])
    check("non_dyadic_shared_endpoints", seen[3:-1:4], seen[4::4])
    check("non_dyadic_terminal_time", (1., 1., 40),
          (seen[-1], out["final_time"], out["evaluations"]))
    check("non_dyadic_linear_integral", .5, out["final_state"],
          passed=abs(out["final_state"]-.5) <= math.ulp(.5))
    print(json.dumps(rows, indent=2))
    assert all(row["passed"] for row in rows)


if __name__ == "__main__":
    main()
