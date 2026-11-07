"""Exact local power-series references and callback traces for Section 8.3."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv)==2:
    sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import section_8_03 as lab


def reference(kind,values):
    a,b,c,d=map(Q,values)
    if kind=="product":
        # Coefficient of z in (a+b*z)*(c+d*z).
        coefficients=[Q(0)]*3
        for i,u in enumerate((a,b)):
            for j,v in enumerate((c,d)):
                coefficients[i+j]+=u*v
        exact=coefficients[1]
    else:
        if not c:
            return "ValueError"
        # Solve coefficients of (c+d*z)*(q0+q1*z+...) = a+b*z.
        q0=a/c
        exact=(b-d*q0)/c
    try: return float(exact)
    except OverflowError: return "ValueError"


def check():
    rows=[]
    names=("u","du","v","dv")
    def observe(kind,values,x=0.,bad=None,expected=None):
        order=["du","v","u","dv"] if kind=="product" else ["v","du","u","dv"]
        if kind=="quotient" and values[2]==0:
            order=["v"]
        if bad:
            order=order[:order.index(bad[0])+1]
        if isinstance(x,bool) or not math.isfinite(x):
            order=[]
        calls=[]
        def callback(name,value):
            def run(point):
                calls.append([name,point])
                return bad[1] if bad and bad[0]==name else value
            return run
        callbacks=[callback(name,value) for name,value in zip(names,values)]
        fn=lab.product_derivative if kind=="product" else lab.quotient_derivative
        if expected is None:
            expected=reference(kind,values)
        try:
            actual=fn(*callbacks,x)
            if not math.isfinite(actual): actual=repr(actual)
        except Exception as exc:
            actual=type(exc).__name__
        zero_sign=(not isinstance(expected,float) or expected!=0 or
                   (type(actual) is float and math.copysign(1,actual)==math.copysign(1,expected)))
        want_calls=[[name,x] for name in order]
        rows.append(dict(helper=kind,inputs=list(values),control=bad[0] if bad else "numeric",
                         expected=expected,actual=actual,expected_calls=want_calls,actual_calls=calls,
                         passed=actual==expected and calls==want_calls and zero_sign))
    M=sys.float_info.max
    u=math.ulp(0.)
    for values in [(1.,M,2.,-M),(M,M,1.,-1.),(u,u,.5,.5),(-u,-u,.5,.5),
                   (M,1.,1.,M),(1.,1e-300,1e-300,0.),(3.,2.,4.,-1.)]:
        observe("product",values)
    for values in [(M,M,M,M),(M,M,M,0.),(0.,u,u,0.),(u,u,u,u),(1.,0.,M,1.),
                   (M,M,-M,M),(M,0.,u,1.),(1.,1.,0.,1.),(1.,1.,-0.,1.)]:
        observe("quotient",values)
    for kind in ("product","quotient"):
        for name in names:
            for bad_value,error in [(True,"TypeError"),(math.nan,"ValueError")]:
                observe(kind,(1.,2.,3.,4.),bad=(name,bad_value),expected=error)
        observe(kind,(1.,2.,3.,4.),x=True,expected="TypeError")
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
