"""Independent log-scale oracle for Section 8.5 exponential derivative.

Optional directory argument selects the exact original section_8_05.py.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import importlib
import json
import math
from pathlib import Path
import sys
if len(sys.argv)>1:
    directory=Path(sys.argv[1]).resolve()
    if not (directory/"section_8_05.py").is_file():
        raise SystemExit("requested source module is missing")
    sys.path.insert(0,str(directory))
m=importlib.import_module("section_8_05")
M,T=sys.float_info.max,math.ulp(0.0)
rows=[]

def reference(x,a,k,precision=1600):
    x,a,k=map(float,(x,a,k))
    if a==0 or k==0:return a*k
    if x==0:
        try:return float(Fraction(a)*Fraction(k))
        except OverflowError:return "ValueError"
    negative=(a<0)!=(k<0)
    with localcontext() as ctx:
        ctx.prec=precision
        dx,da,dk=map(Decimal.from_float,(x,a,k))
        exponent=dk*dx
        if exponent>100000:return "ValueError"
        if exponent< -100000:return -0.0 if negative else 0.0
        # Independent log amplitude, not production's coefficient times exp.
        magnitude=float((abs(da).ln()+abs(dk).ln()+exponent).exp())
    if not math.isfinite(magnitude):return "ValueError"
    return -magnitude if negative else magnitude

def observe(name,fn,expected):
    try:
        actual=fn()
        passed=not isinstance(expected,str) and actual==expected
        if isinstance(expected,float) and expected==0 and actual==0:
            passed=passed and math.copysign(1,actual)==math.copysign(1,expected)
    except Exception as exc:
        actual=type(exc).__name__;passed=actual==expected
    if isinstance(actual,float) and not math.isfinite(actual):actual=repr(actual)
    rows.append(dict(case=name,expected=expected,actual=actual,passed=passed))

points=[
    (-500.,M,2.),(1000.,T,1.),(M,0.,M),(-500.,-M,2.),
    (M,-0.,M),(M,M,0.),(M,M,-0.),(0.,M,M),
    (1e303,T,1e-300),(1000.,-T,1.),(-1000.,T,-1.),(500.,M,-2.),
    (1.,M,T),(1.,T,T),(1.,-T,T),(M,M,M),(M,M,-M),(-M,M,M),
    (1.,7.,3.),(-2.,7.,3.),(0.,2.,3.),(.3,1.,1.),(1.3,-1.1,2.3),
]
for i,args in enumerate(points):
    expected=reference(*args)
    assert expected==reference(*args,precision=2200)
    observe("complete expression "+str(i),lambda a=args:m.exponential_derivative(*a),expected)
observe("retained defaults",lambda:m.exponential_derivative(1.),reference(1.,1.,1.))
for label,args,expected in [
    ("bool x",(True,1,1),"TypeError"),("bool scale",(1,True,1),"TypeError"),
    ("bool growth",(1,1,True),"TypeError"),("nan x",(math.nan,1,1),"ValueError"),
    ("infinite scale",(1,math.inf,1),"ValueError"),
    ("infinite growth",(1,1,math.inf),"ValueError"),
    ("zero scale invalid x",(math.nan,0,1),"ValueError"),
    ("zero growth invalid scale",(1,math.inf,0),"ValueError"),
    ("huge integer",(10**400,1,1),"ValueError"),
    ("text scale",(1,"2",1),"TypeError"),
]:
    observe(label,lambda a=args:m.exponential_derivative(*a),expected)
print(json.dumps(rows,allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
