"""Actual callback traces and rational sampled-value references for Section 8.1."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv)==2:
    sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import section_8_01 as lab


def check():
    rows=[]
    M=sys.float_info.max
    u=math.ulp(0.)
    def exercise(name,method,x,h,callback,expected,calls_expected):
        calls=[]
        def observed(point):
            calls.append(point if math.isfinite(point) else repr(point))
            return callback(point)
        try:
            actual=method(observed,x,h)
            if not math.isfinite(actual):
                actual=repr(actual)
        except Exception as exc:
            actual=type(exc).__name__
        passed=actual==expected and calls==calls_expected
        rows.append(dict(case=name,expected=expected,actual=actual,
                         expected_calls=calls_expected,actual_calls=calls,passed=passed))
    for method in (lab.forward_difference,lab.centered_difference):
        label=method.__name__
        centered=method is lab.centered_difference
        for name,x,h in [("collapsed",1.,1e-30),("zero",1.,0.),
                         ("overflowed perturbation",M,M)]:
            exercise(label+" "+name,method,x,h,lambda x:x,"ValueError",[])
        for h in (.25,-.25):
            x=2.
            points=[x+h,x-h] if centered else [x+h,x]
            values=[p*p for p in points]
            expected=float((Q(values[0])-Q(values[1]))/(Q(h)*(2 if centered else 1)))
            exercise(label+" signed quadratic "+str(h),method,x,h,
                     lambda p:p*p,expected,points)
        h=M if centered else 2.
        points=[h,-h] if centered else [h,0.]
        vals=[M,-M]
        expected=float((Q(vals[0])-Q(vals[1]))/(Q(h)*(2 if centered else 1)))
        exercise(label+" complete large difference",method,0.,h,
                 lambda p:M if p>0 else -M,expected,points)
        h=.25
        points=[h,-h] if centered else [h,0.]
        exercise(label+" genuine result overflow",method,0.,h,
                 lambda p:M if p>0 else -M,"ValueError",points)
        exercise(label+" callback NaN",method,0.,1.,lambda p:math.nan,
                 "ValueError",[1.])
        exercise(label+" callback bool",method,0.,1.,lambda p:True,
                 "TypeError",[1.])
    exercise("centered denominator alone exceeds float",lab.centered_difference,0.,M,
             lambda p:1. if p>0 else 0.,float(Q(1)/(2*Q(M))),[M,-M])
    exercise("forward complete quotient after subtraction overflow",lab.forward_difference,0.,M,
             lambda p:M if p>0 else -M,2.,[M,0.])
    exercise("centered least-step sampled identity",lab.centered_difference,0.,u,
             lambda p:p,1.,[u,-u])
    exercise("forward least-step sampled identity",lab.forward_difference,0.,u,
             lambda p:p,1.,[u,0.])
    # Represented grid points are deliberately asymmetric around x, and the
    # specified denominator is retained. This is a sampled stencil, not a proof
    # that a chosen step estimates the derivative accurately.
    x=1.
    h=math.ulp(x)
    pts=[x+h,x-h]
    vals=[p*p for p in pts]
    expect=float((Q(vals[0])-Q(vals[1]))/(2*Q(h)))
    exercise("rounded sampled grid",lab.centered_difference,x,h,lambda p:p*p,expect,pts)
    for method in (lab.forward_difference,lab.centered_difference):
        try: method(None,0.,1.)
        except Exception as exc: actual=type(exc).__name__
        else: actual="returned"
        rows.append(dict(case=method.__name__+" noncallable",expected="TypeError",
                         actual=actual,passed=actual=="TypeError"))
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
