"""Exact polynomial-quotient references for Section 8.3 financial examples."""
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv)==2:
    sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import section_8_03 as lab


def rounded(value):
    try: return float(value)
    except OverflowError: return "ValueError"


def oracle(name,x):
    x=Q(x)
    if name.startswith("average_cost"):
        if x<=0: return "ValueError"
        cost=500+10*x+Q(.1)*x*x
        marginal=10+2*Q(.1)*x
        answer=cost/x if name=="average_cost" else (marginal*x-cost)/(x*x)
    else:
        assets,liabilities=100+8*x,50+3*x
        if not liabilities: return "ValueError"
        answer=assets/liabilities if name=="coverage_ratio" else (8*liabilities-3*assets)/(liabilities*liabilities)
    return rounded(answer)


def check():
    rows=[]
    def observe(name,x,expected=None,label="numeric"):
        if expected is None: expected=oracle(name,x)
        try:
            actual=getattr(lab,name)(x)
            if not math.isfinite(actual): actual=repr(actual)
        except Exception as exc:
            actual=type(exc).__name__
        passed=actual==expected
        if isinstance(expected,float) and expected==0:
            passed=passed and isinstance(actual,float) and math.copysign(1,actual)==math.copysign(1,expected)
        rows.append(dict(helper=name,input=x if type(x) is bool or math.isfinite(x) else repr(x),
                         control=label,expected=expected,actual=actual,passed=passed))
    M=sys.float_info.max
    u=math.ulp(0.)
    for fn in ("average_cost","average_cost_derivative"):
        for x in (M,1e200,1e154,1e-154,u,100.,0.,-1.):
            observe(fn,x)
    pole=-50./3.
    for fn in ("coverage_ratio","coverage_ratio_derivative"):
        for x in (M,-M,1e154,1e100,0.,pole,math.nextafter(pole,math.inf),
                  math.nextafter(pole,-math.inf)):
            observe(fn,x)
    for fn in ("average_cost","average_cost_derivative","coverage_ratio","coverage_ratio_derivative"):
        observe(fn,True,"TypeError","bool")
        observe(fn,math.inf,"ValueError","nonfinite")
    # Distinguish exact represented denominator from its rounded evaluation.
    exact=50+3*Q(pole)
    rows.append(dict(helper="near-pole interpretation",expected=[True,True],actual=[exact!=0,50+3*pole==0],
                     passed=exact!=0 and 50+3*pole==0))
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
