"""Adaptive RK4 clock checks with a prescribed proposal and real RHS stages."""
import json
import math
from unittest.mock import patch

import section_19_06 as lab


def main():
    rows = []
    u = math.ulp(1.)
    def check(name, expected, actual):
        rows.append(dict(case=name, expected=expected, actual=actual, passed=expected==actual))

    # The first trial integrates y'=1 over [0,1], giving y(1)=0.
    # Only the controller proposal is patched. Every derivative and RK stage is real.
    for name, proposal, horizon_ticks, endpoint_ticks, midpoint_ticks, status in [
        ("no_progress", .25, 4, 0, None, "step_too_small"),
        ("collapsed_midpoint", .75, 4, 0, None, "step_too_small"),
        ("rounded_advance", 1.75, 4, 2, 1, "attempt_budget_exhausted"),
        ("odd_interval", 2.75, 4, 3, 2, "attempt_budget_exhausted"),
        ("clipped_final_interval", 5., 3, 3, 2, "completed"),
    ]:
        seen = []
        def rhs(t, y):
            seen.append((t,y))
            return 1.
        with patch.object(lab, "_step_factor", return_value=proposal*u):
            r = lab.adaptive_rk4(rhs,-1.,1.+horizon_ticks*u,initial_step=1.,
                                 min_step=u/8,max_attempts=2)
        n = 1 if midpoint_ticks is None else 2
        endpoint = 1.+endpoint_ticks*u
        # y'=1 has exact state t-1 at the accepted endpoint.
        check(name+"_report", [status, endpoint, endpoint_ticks*u, n, 0, 12*n],
              [r[k] for k in ("status","final_time","final_state","accepted_steps",
                              "rejected_steps","evaluations")])
        check(name+"_callbacks", 12*n, len(seen))
        if midpoint_ticks is not None:
            check(name+"_shared_endpoint", [endpoint,endpoint], [seen[15][0],seen[23][0]])
            m = 1.+midpoint_ticks*u
            check(name+"_shared_midpoint", [m,m,m,m], [seen[i][0] for i in (13,14,19,20)])
            check(name+"_stages_within_trial", True,
                  all(1. <= t <= endpoint for t,_ in seen[12:]))

    # y'=t on [0,1] integrates to 1/2. Verify normal final clipping without
    # a controller patch and confirm the two terminal callback paths land at 1.
    seen = []
    def linear(t, y):
        seen.append(t)
        return t
    r = lab.adaptive_rk4(linear,0.,1.,initial_step=.25)
    check("linear_integral", ["completed",1.,.5,2,0,24],
          [r[k] for k in ("status","final_time","final_state","accepted_steps",
                          "rejected_steps","evaluations")])
    check("linear_shared_endpoint", [1.,1.], [seen[-9],seen[-1]])
    print(json.dumps(rows,indent=2))
    assert all(r["passed"] for r in rows)


if __name__=="__main__":
    main()
