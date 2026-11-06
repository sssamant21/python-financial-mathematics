"""Independent Section 19.4 transition and assessment range checks."""
from decimal import Decimal as D, localcontext
import json
import math
import sys

from section_19_04 import assessment, half_life, logistic, mean_reversion


def outcome(f,*args):
    try:
        x=f(*args)
        return "infinity" if math.isinf(x) else x
    except (ValueError,TypeError,OverflowError) as exc:
        return type(exc).__name__


def affine(a,b,k,t):
    with localcontext() as ctx:
        ctx.prec=2200
        a,b,k,t=map(D,(a,b,k,t))
        w=(-k*t).exp()
        return float(a*w+b*(1-w))


def reciprocal(a,r,k,t):
    with localcontext() as ctx:
        ctx.prec=2200
        a,r,k,t=map(D,(a,r,k,t))
        w=(-r*t).exp()
        return float(1/(1/k+(1/a-1/k)*w))


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
    for name,args,expected in [
        ("affine_zero_time",(m,-m,1.,0.),m),
        ("affine_opposite_targets",(m,-m,1.,.5),affine(m,-m,1.,.5)),
        ("affine_scaled_decay",(m,0.,1000.,1.),affine(m,0.,1000.,1.)),
        ("affine_tiny_drift",(0.,m,d,.125),affine(0.,m,d,.125)),
        ("affine_equilibrium",(m,m,m,m),m),
        ("affine_signed_underflow",(-1.,0.,m,m),-0.),
        ("affine_invalid_speed",(1.,2.,0.,0.),"ValueError"),
        ("affine_invalid_time",(1.,2.,1.,-1.),"ValueError"),
    ]:
        check(name,expected,outcome(mean_reversion,*args),1 if name in
              ("affine_opposite_targets","affine_scaled_decay","affine_tiny_drift") else 0)
    for name,args,expected in [
        ("logistic_zero_time",(d,1.,m,0.),d),
        ("logistic_scaled_growth",(d,1.,m,1000.),reciprocal(d,1.,m,1000.)),
        ("logistic_above_capacity",(m,1.,d,.125),reciprocal(m,1.,d,.125)),
        ("logistic_equilibrium",(m,m,m,m),m),
        ("logistic_zero",(0.,m,m,m),0.),
        ("logistic_saturation",(d,m,m,m),m),
        ("logistic_invalid_rate",(1.,0.,2.,0.),"ValueError"),
    ]:
        check(name,expected,outcome(logistic,*args),1 if name in
              ("logistic_scaled_growth","logistic_above_capacity") else 0)
    with localcontext() as ctx:
        ctx.prec=100
        for name,k,expected in [
            ("half_life_overflow",d,"ValueError"),
            ("half_life_subnormal",m,float(D(2).ln()/D(m))),
            ("half_life_invalid",0.,"ValueError"),
        ]:
            check(name,expected,outcome(half_life,k),1 if name=="half_life_subnormal" else 0)
        h=float(D(2).ln()/D(.5))
    report=assessment()
    check("assessment_mean_reversion",affine(1200,1000,.5,2),report["mean_reverting_balance"],1)
    check("assessment_logistic",reciprocal(200,.4,1000,5),report["logistic_balance"],1)
    check("assessment_half_life",h,report["mean_reversion_half_life"],1)
    check("assessment_review",[False,False],
          [report["runtime_certified"],report["independent_review_completed"]])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
