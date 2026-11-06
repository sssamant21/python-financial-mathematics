"""Section 19.9 event decisions against exact and Decimal balance references."""
from decimal import Decimal, localcontext
import json
import math
import sys

from section_19_09 import simulate


def snapshot(*args):
    try:
        r=simulate(*args)
    except (ValueError, OverflowError) as exc:
        return type(exc).__name__
    return {k:r[k] for k in ("status","final_time","final_balance","depletion_time",
                              "applied_jumps","events")}


def completed(t,b,events):
    return dict(status="completed",final_time=t,final_balance=b,depletion_time=None,
                applied_jumps=len(events),events=events)


def depleted(t):
    return dict(status="depleted",final_time=t,final_balance=0.,depletion_time=t,
                applied_jumps=0,events=[dict(type="depletion",time=t)])


def jump(t,b,amount=1.):
    return dict(type="jump",time=t,amount=amount,balance=b)


def main():
    rows=[]
    def check(case,expected,actual):
        rows.append(dict(case=case,expected=expected,actual=actual,passed=expected==actual))

    q=2.**-52
    t=1.+q
    # Affine residual is q², so the deposit precedes crossing even
    # though the crossing's float display equals the deposit time.
    check("linear_rounded_tie", completed(t,1.,[jump(t,1.)]),
          snapshot(1.,0.,-(1-q),t,[(t,1.)]))
    check("linear_horizon_before_crossing", completed(t,q*q,[]),
          snapshot(1.,0.,-(1-q),t))
    check("linear_exact_tie", depleted(1.),snapshot(1.,0.,-1.,1.,[(1.,1.)]))
    check("linear_later_jump", depleted(1.),snapshot(1.,0.,-1.,t,[(t,1.)]))

    # Independent integrating-factor solution A(t)=2-exp(t/2).
    t=1.3862943611198906
    with localcontext() as ctx:
        ctx.prec=150
        a=2-(Decimal(t)/2).exp()
        assert a>0
        b=float(a+1)
    check("nonzero_rounded_tie",completed(t,b,[jump(t,b)]),
          snapshot(1.,.5,-1.,t,[(t,1.)]))
    check("nonzero_horizon_before_crossing",completed(t,float(a),[]),
          snapshot(1.,.5,-1.,t))
    later=math.nextafter(t,math.inf)
    check("nonzero_later_jump",depleted(t),snapshot(1.,.5,-1.,later,[(later,1.)]))

    # After the zero transfer, the represented state is 1. The exact
    # interval width is 1-e, so the terminal balance is e, not zero.
    e=2.**-54
    check("exact_elapsed_difference",completed(1.,e,[jump(e,1.,0.)]),
          snapshot(1.,0.,-1.,1.,[(e,0.)]))
    check("initial_rescue",completed(0.,1.,[jump(0.,1.)]),
          snapshot(0.,0.,-1.,0.,[(0.,1.)]))
    m,d=sys.float_info.max,math.ulp(0.)
    check("crossing_beyond_float_range",completed(1.,m,[]),snapshot(m,0.,-d,1.))
    check("crossing_rounds_to_zero",depleted(0.),snapshot(d,0.,-m,1.))

    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
