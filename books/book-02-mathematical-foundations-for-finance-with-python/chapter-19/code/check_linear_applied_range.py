"""Independent Section 19.3 range and assessment checks."""
from decimal import Decimal as D, localcontext
import json
import math
import sys

from section_19_03 import (account, assessment, depletion_time, euler_account,
                           piecewise_account, variable_rate_no_flow)


def outcome(f,*args):
    try:
        x=f(*args)
        return "infinity" if x is not None and math.isinf(x) else x
    except (ValueError,TypeError,OverflowError) as exc:
        return type(exc).__name__


def balance(a,r,u,t):
    a,r,u,t=map(D,(a,r,u,t))
    if not r:
        return a+u*t
    w=(r*t).exp()
    return a*w+u*(w-1)/r


def main():
    rows=[]
    def check(name,want,got,ulps=0):
        if isinstance(want,float) and isinstance(got,float):
            ok=abs(want-got)<=ulps*math.ulp(want) and (want==0 or got!=0)
            if want==0 and got==0:
                ok=math.copysign(1.,want)==math.copysign(1.,got)
        else:
            ok=want==got
        rows.append(dict(case=name,expected=want,actual=got,passed=ok))

    m,d=sys.float_info.max,math.ulp(0.)
    q=2.**-52
    with localcontext() as ctx:
        ctx.prec=2000
        for name,f,args,expected in [
            ("integral_cancellation",variable_rate_no_flow,(7.,-m,m,2.),7.),
            ("scaled_variable_growth",variable_rate_no_flow,(d,0.,500.,2.),float(D(d)*D(1000).exp())),
            ("variable_signed_underflow",variable_rate_no_flow,(-1.,-m,0.,2.),-0.),
            ("variable_zero_state",variable_rate_no_flow,(0.,m,m,m),0.),
            ("variable_final_overflow",variable_rate_no_flow,(1.,m,m,1.),"ValueError"),
            ("zero_rate_cancellation",account,(-m,0.,m,2.),m),
            ("scaled_continuous_decay",account,(m,-1000.,0.,1.),float(D(m)*D(-1000).exp())),
            ("account_zero_time",account,(-0.,m,m,0.),-0.),
            ("continuous_overflow",account,(m,0.,m,1.),"ValueError"),
            ("piecewise_extreme",piecewise_account,(-m,0.,[(m,2.),(-m,1.)]),0.),
            ("piecewise_keeps_state_boundary",piecewise_account,(m,0.,[(m,1.),(-m,1.)]),"ValueError"),
            ("piecewise_reverse_order",piecewise_account,(-m,0.,[(-m,1.),(m,2.)]),"ValueError"),
            ("whole_euler_update",euler_account,(-m,-2.,-m,1.,1),0.),
            ("tiny_euler_width",euler_account,(0.,0.,m,3*d,2),float(D(m)*D(3*d))),
            ("euler_zero_time",euler_account,(m,m,m,0.,2),m),
            ("euler_overflow",euler_account,(m,0.,m,1.,1),"ValueError"),
            ("euler_invalid_steps",euler_account,(1.,0.,1.,1.,True),"ValueError"),
            ("depletion_threshold",depletion_time,(1+q,1-q,1.),float(-(D(q)**2).ln()/D(1-q))),
            ("depletion_equal_threshold",depletion_time,(2.,.5,1.),None),
            ("depletion_final_overflow",depletion_time,(m,0.,d),"ValueError"),
            ("depletion_negative_rate",depletion_time,(1.,-1.,1.),"ValueError"),
        ]:
            check(name,expected,outcome(f,*args))
        report=assessment()
        check("report_flow",float(balance(1000,.04,200,5)),report["constant_flow_balance"],1)
        first=float(balance(1000,.04,100,2))
        check("report_piecewise",float(balance(first,.04,200,3)),report["piecewise_balance"],1)
        check("report_variable",float(D(1000)*(D(.03)*5+D(.002)*25/2).exp()),report["time_varying_rate_balance"],1)
        h=D(5)/40
        g=1+D(.04)*h
        exact_discrete=1000*g**40+200*h*sum(g**j for j in range(40))
        check("report_euler_40",float(exact_discrete),report["euler_40"],8)
        check("report_depletion",float((D(100)/(100-D(.04)*1000)).ln()/D(.04)),report["depletion_time"],2)
        check("report_review",[False,False],
              [report["runtime_certified"],report["independent_review_completed"]])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
