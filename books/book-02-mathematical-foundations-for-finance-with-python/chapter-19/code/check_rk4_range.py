"""RK4 range checks with exact stage identities and controlled controller inputs."""
from fractions import Fraction as Q
import json
import math
import sys
from unittest.mock import patch

import section_19_06 as lab


M = sys.float_info.max
TINY = math.ulp(0.0)
H = 2.0**-1022


def outcome(fn):
    try:
        return fn()
    except (ValueError, TypeError, OverflowError, RuntimeError) as exc:
        return type(exc).__name__


def main():
    rows = []

    def record(name, expected, actual):
        # Retain the old infinity seen by the callback as valid JSON evidence.
        rows.append(dict(case=name, expected=repr(expected), actual=repr(actual),
                         passed=expected == actual))

    def constant(t, y):
        return M

    # A constant derivative integrates exactly; this oracle does not sum RK weights.
    exact = float(Q(M)*Q(H))
    record("finite_scaled_increment", exact,
           outcome(lambda: lab.rk4_step(constant, 0., 0., H)))
    record("published_scaled_increment", float(Q(M)*Q(H)/2),
           outcome(lambda: lab.rk4_step(constant, 0., 0., H/2)))
    fixed = {"final_state": exact, "final_time": H, "steps": 2,
             "evaluations": 8, "status": "completed"}
    record("fixed_consumer", fixed, outcome(lambda: lab.fixed_rk4(constant, 0., H, 2)))

    def metrics(report):
        return (report["status"], report["final_state"], report["final_time"],
                report["accepted_steps"], report["rejected_steps"], report["evaluations"])

    record("adaptive_consumer", ("completed", exact, H, 1, 0, 12),
           outcome(lambda: metrics(lab.adaptive_rk4(
               constant, 0., H, initial_step=H, min_step=TINY))))

    seen = []
    def symmetric(t, y):
        seen.append((t,y))
        return {0.: M, 1.: 0., 2.: -M}[t]
    # The endpoint slopes cancel; only the first midpoint carries a nonzero state.
    record("canceling_increment", 0., outcome(lambda: lab.rk4_step(symmetric, 0., 0., 2.)))
    record("finite_midpoint_state", [(0.,0.), (1.,M), (1.,0.), (2.,0.)], seen)

    seen = []
    def middle_pair(t, y):
        seen.append((t, y))
        return next(slopes)
    slopes = iter((0., M, -M, 0.))
    record("opposite_middle_slopes", 0., outcome(lambda: lab.rk4_step(middle_pair, 0., 0., 1.)))
    record("middle_pair_stages", [(0.,0.), (.5,0.), (.5,M/2), (1.,-M)], seen)

    seen = []
    def trace(t, y):
        seen.append((t, y))
        return M
    record("invalid_stage_state", "ValueError", outcome(lambda: lab.rk4_step(trace, 0., 0., 4.)))
    record("invalid_stage_no_callback", [(0.,0.)], seen)
    seen = []
    record("invalid_stage_time", "ValueError", outcome(lambda: lab.rk4_step(trace, M, 0., M)))
    record("invalid_time_no_callback", [(M,0.)], seen)

    # All intermediate stage states are finite; the final weighted state is not.
    slopes = iter((M, M, M/2, M))
    record("final_state_overflow", "ValueError",
           outcome(lambda: lab.rk4_step(lambda t,y:next(slopes), 0., M/2, 1.)))
    record("boolean_derivative", "TypeError", outcome(lambda: lab.rk4_step(lambda t,y:True, 0, 0, 1)))
    record("nonfinite_derivative", "ValueError",
           outcome(lambda: lab.rk4_step(lambda t,y:math.inf, 0, 0, 1)))
    def bad_callback(t, y):
        raise RuntimeError("from callback")
    record("callback_exception_propagates", "RuntimeError",
           outcome(lambda: lab.rk4_step(bad_callback, 0, 0, 1)))

    # These deliberately injected, finite step results isolate adaptive arithmetic.
    # The error from opposite extreme states is 2*M/15, smaller than atol=M.
    with patch.object(lab, "_rk4_interval", side_effect=(-M, 0., M)):
        record("adaptive_difference_range", ("completed", M, 1., 1, 0, 12),
               outcome(lambda: metrics(lab.adaptive_rk4(
                   constant, 0., 1., atol=M, rtol=0., initial_step=1., max_attempts=1))))
    # With a zero full estimate, error=M/15; scale=M+2*M. Even though
    # scale itself exceeds float range, its ratio is finite (45).
    # The next step is .9 * 45**.2, below the upper clamp and horizon.
    with patch.object(lab, "_rk4_interval", side_effect=(0., 0., M, M, M, M)) as step:
        result = lab.adaptive_rk4(constant, 0., 10., atol=M, rtol=2.,
                                  initial_step=1., max_attempts=2)
        h2 = .9 * 45**.2
        record("adaptive_scale_range", ("attempt_budget_exhausted", M, 1.+h2, 2, 0, 24),
               metrics(result))
        record("adaptive_scale_retry_size", Q(1.+h2)-1, step.call_args_list[3].args[3])

    seen = []
    record("unrepresentable_half_step", ("step_too_small", 0., 0., 0, 0, 0),
           outcome(lambda: metrics(lab.adaptive_rk4(
               trace, 0., TINY, initial_step=TINY, min_step=TINY))))
    record("unrepresentable_half_no_callback", [], seen)
    seen = []
    record("inexact_equal_split", ("step_too_small", 0., 0., 0, 0, 0),
           outcome(lambda: metrics(lab.adaptive_rk4(
               trace, 0., 3*TINY, initial_step=3*TINY, min_step=TINY))))
    record("inexact_equal_split_no_callback", [], seen)
    print(json.dumps(rows, indent=2))
    assert all(row["passed"] for row in rows)


if __name__ == "__main__":
    main()
