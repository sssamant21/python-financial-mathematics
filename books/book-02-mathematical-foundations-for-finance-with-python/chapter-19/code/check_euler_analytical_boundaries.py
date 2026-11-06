"""Independent Euler factor, strict stability and assessment checks."""
import json
import math
import sys
from decimal import Decimal, localcontext

from section_19_05 import (assessment, euler, exact_account,
                          linear_amplification, stable_linear_decay)


def outcome(fn, *args):
    try:
        return fn(*args)
    except (ValueError, TypeError, OverflowError) as exc:
        return type(exc).__name__


def integrate(a, r, u, t):
    with localcontext() as ctx:
        ctx.prec = 100
        a, r, u, t = map(Decimal,(a,r,u,t))
        g = (r*t).exp()
        return float(a*g+u*(g-1)/r)


def main():
    q, d, m = 2.**-52, math.ulp(0.), sys.float_info.max
    rows = []
    def check(name, expected, actual):
        rows.append(dict(case=name, expected=expected, actual=actual,
                         passed=repr(expected)==repr(actual)))

    # Expand (1-q)(1+q)=1-q²; strict tests use exact factors even
    # where the expected float display is exactly a stability boundary.
    for name, r, h, display, stable in [
        ("inside_minus_one_rounded", -2*(1-q), 1+q, -1., True),
        ("inside_plus_one_rounded", -d, d, 1., True),
        ("near_zero_cancellation", -(1-q), 1+q, q*q, True),
        ("exact_minus_one", -2., 1., -1., False),
        ("adjacent_inside", -2., math.nextafter(1.,0.), -1+q, True),
        ("adjacent_outside", -2., 1+q, -1-2*q, False),
        ("exact_zero_factor", -2., .5, 0., True),
        ("huge_unstable", -m, 2., "ValueError", False),
    ]:
        check(name+"_factor",display,outcome(linear_amplification,r,h))
        check(name+"_stable",stable,outcome(stable_linear_decay,r,h))
    check("zero_rate_factor", 1., outcome(linear_amplification,0.,1.))
    check("zero_rate_not_decay", "ValueError", outcome(stable_linear_decay,0.,1.))
    check("invalid_step", "ValueError", outcome(stable_linear_decay,-1.,0.))
    check("bool_step", "TypeError", outcome(linear_amplification,-1.,True))

    # On these two grids rounded iterates stay at unit magnitude.
    # Mathematical contraction need not yield representable decay.
    for name,r,h,expected in [
        ("rounded_alternation", -2*(1-q), 1+q, [1.,-1.,1.]),
        ("rounded_neutral", -d, d, [1.,1.,1.]),
        ("resolved_cancellation", -(1-q), 1+q, [1.,q*q]),
    ]:
        seen=[]
        def rhs(t,y):
            seen.append(y)
            return r*y
        n=len(expected)-1
        result=euler(rhs,1.,n*h,n)
        check(name,expected,[*seen,result["final_state"]])

    for name,args,expected in [
        ("account_equilibrium",(6.,800.,-4800.,1.),6.),
        ("account_scaled_withdrawal",(0.,720.,-d,1.),integrate(0.,720.,-d,1.)),
        ("account_zero_rate_cancellation",(-m,0.,m,2.),m),
        ("account_signed_underflow",(0.,0.,-d,.125),-0.),
        ("account_overflow",(m,0.,m,1.),"ValueError"),
    ]:
        check(name,expected,outcome(exact_account,*args))
    report=assessment()
    for name,args in [("growth_reference",(1000,.05,0,2)),("account_reference",(1000,.04,200,5))]:
        ref=integrate(*args)
        check(name,True,abs(report[name]-ref)<=math.ulp(ref))
    for name,factor in [("h025",.5),("h075",-.5),("h125",-1.5)]:
        check("report_"+name,factor,report["decay_amplification_"+name])
    check("review_flags",[False,False],[report["runtime_certified"],report["independent_review_completed"]])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
