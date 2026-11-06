"""Section 19.7 terminal, nonterminal and interpolation boundary oracle."""
from decimal import Decimal, localcontext
import json
import math
import sys

from section_19_07 import account, linear_crossing, simulate_jumps


def outcome(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except (ValueError, OverflowError, TypeError) as exc:
        return type(exc).__name__


def result(t,b,depleted=False):
    return dict(status="depleted" if depleted else "completed",
                final_time=t, final_balance=b, event_time=t if depleted else None)


def main():
    rows=[]
    def check(case,expected,actual):
        rows.append(dict(case=case,expected=expected,actual=actual,passed=expected==actual))
    m=sys.float_info.max
    for name,args,expected in [
        ("symmetric_extreme",(-m,m,m,-m),0.),
        ("asymmetric_extreme",(-m,m,1.,-3.),-m/2),
        ("zero_right_endpoint",(0.,m,m,0.),m),
        ("ordinary_crossing",(2.,8.,2.,-4.),4.),
        ("invalid_sign",(0.,1.,1.,1.),"ValueError"),
        ("invalid_times",(1.,1.,1.,0.),"ValueError"),
    ]:
        check(name,expected,outcome(linear_crossing,*args))

    # A(t)=5 exp(-t/4)-4. The displayed crossing rounds upward.
    t=.8925742052568391
    before=math.nextafter(t,0.)
    with localcontext() as ctx:
        ctx.prec=150
        a=lambda x: 5*(-Decimal(x)/4).exp()-4
        assert a(before)>0>a(t)
        before_b=float(a(before))
        later_b=float(a(t))
    check("later_deposit_cannot_rescue",result(t,0.,True),
          outcome(simulate_jumps,1.,-.25,1.,t,[(t,1.)]))
    check("earlier_deposit_rescues",result(before,before_b+1.),
          outcome(simulate_jumps,1.,-.25,1.,before,[(before,1.)]))
    check("nonterminal_applies_later_deposit",result(t,later_b+1.),
          outcome(simulate_jumps,1.,-.25,1.,t,[(t,1.)],stop_at_depletion=False))
    check("exact_tie_allows_rescue",result(1.,1.),
          outcome(simulate_jumps,1.,0.,1.,1.,[(1.,1.)]))
    check("exact_tie_without_rescue",result(1.,0.,True),
          outcome(simulate_jumps,1.,0.,1.,1.,[(1.,0.)]))
    check("initial_jump_rescues",result(0.,2.),
          outcome(simulate_jumps,0.,0.,1.,0.,[(0.,2.)]))
    check("signed_continuation",result(2.,-1.),
          outcome(simulate_jumps,1.,0.,1.,2.,[],stop_at_depletion=False))
    # Keep the represented width after a tiny initial interval.
    e=2.**-54
    check("exact_elapsed_width",result(1.,e),
          outcome(simulate_jumps,1.,0.,1.,1.,[(e,0.)]))
    # Exact positive equilibrium, even though exp(800) itself overflows.
    check("equilibrium_balance",6.,outcome(account,6.,800.,4800.,1.))
    # A positive quarter-subnormal is not a terminal crossing.
    d=math.ulp(0.)
    check("terminal_underflow_is_range_error","ValueError",
          outcome(simulate_jumps,d,0.,d,.75,[]))
    check("nonterminal_underflow_rounds_to_zero",result(.75,0.),
          outcome(simulate_jumps,d,0.,d,.75,[],stop_at_depletion=False))
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
