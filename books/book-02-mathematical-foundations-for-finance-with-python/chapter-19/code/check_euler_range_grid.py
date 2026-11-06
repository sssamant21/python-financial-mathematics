"""Independent complete-update and represented-grid checks for Section 19.5."""
from fractions import Fraction as Q
import json
import math
import sys

from section_19_05 import assessment, euler


def outcome(fn, *args):
    try:
        return fn(*args)
    except (ValueError, TypeError) as exc:
        return type(exc).__name__


def main():
    m, d = sys.float_info.max, math.ulp(0.)
    rows = []
    def check(name, expected, actual):
        rows.append(dict(case=name, expected=expected, actual=actual, passed=expected==actual))
    def report(y, horizon, steps, nominal, smallest, largest):
        return dict(final_state=y, final_time=horizon, steps=steps, step_size=nominal,
                    min_step_size=smallest, max_step_size=largest, status="completed")

    check("complete_cancellation", report(m,2.,1,2.,2.,2.),
          outcome(euler,lambda t,y:m,-m,2.,1))
    check("genuine_overflow", "ValueError", outcome(euler,lambda t,y:m,m,2.,1))
    check("invalid_derivative", "ValueError", outcome(euler,lambda t,y:math.nan,0.,1.,1))
    check("invalid_step_type", "ValueError", outcome(euler,lambda t,y:1.,0.,1.,True))

    for ticks,n,starts,short,long in [
        (3,2,[0,2],1,2),
        (5,4,[0,1,2,4],1,2),
        (4,2,[0,2],2,2),
    ]:
        seen=[]
        def constant(t,y):
            seen.append(t)
            return m
        horizon=ticks*d
        want=float(Q(m)*Q(horizon))
        check(f"constant_balance_{ticks}", want,
              euler(constant,0.,horizon,n)["final_state"])
        check(f"left_endpoints_{ticks}", [k*d for k in starts], seen)
        check(f"grid_report_{ticks}", report(want,horizon,n,horizon/n,short*d,long*d),
              euler(lambda t,y:m,0.,horizon,n))

    # On [0,2d,3d], slopes 0 and M/2 act over 2d and d, respectively.
    check("time_dependent_left_rule", float(Q(m)*Q(d)/2),
          euler(lambda t,y:(t/d)*(m/4),0.,3*d,2)["final_state"])
    seen=[]
    def traced(t,y):
        seen.append(t)
        return 0.
    check("collapsed_grid", "ValueError", outcome(euler,traced,0.,2*d,3))
    check("collapsed_grid_no_callbacks", [], seen)
    seen=[]
    check("zero_horizon", report(5.,0.,0,0.,0.,0.), euler(traced,5.,0.,3))
    check("zero_horizon_no_callbacks", [], seen)
    # Left rectangle rule at t=i/10 with slope t has exact mathematical sum .45.
    ordinary=euler(lambda t,y:t,0.,1.,10)
    check("ordinary_linear_left_rule", True, abs(ordinary["final_state"]-.45)<=math.ulp(.45))
    a=assessment()["growth_euler"]
    check("assessment_convergence", True, a["40"]["absolute_error"]<a["20"]["absolute_error"]<a["10"]["absolute_error"])
    check("assessment_horizons", [2.,2.,2.], [a[k].get("final_time") for k in ("10","20","40")])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
