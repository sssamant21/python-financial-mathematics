"""Independent reciprocal oracle and retained rounded-domain gate, Section 8.5.

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

def rounded_argument(x,a,b):
    with localcontext() as ctx:
        ctx.prec=3000
        product=float(Decimal.from_float(b)*Decimal.from_float(x))
        return float(Decimal.from_float(a)+Decimal.from_float(product))

def reference(x,a,b):
    x,a,b=map(float,(x,a,b))
    if rounded_argument(x,a,b)<=0:return "ValueError"
    if b==0:return b
    # Algebraically independent form: b/(a+b*x) = 1/(x+a/b).
    reciprocal_denominator=Fraction(x)+Fraction(a)/Fraction(b)
    try:return float(1/reciprocal_denominator)
    except OverflowError:return "ValueError"

def observe(name,fn,expected):
    try:
        actual=fn()
        passed=not isinstance(expected,str) and actual==expected
        es=int(math.copysign(1,expected)) if isinstance(expected,float) and expected==0 else None
        xs=int(math.copysign(1,actual)) if isinstance(actual,float) and actual==0 else None
        if es is not None and xs is not None:passed=passed and es==xs
    except Exception as exc:
        actual=type(exc).__name__;passed=actual==expected
        es=int(math.copysign(1,expected)) if isinstance(expected,float) and expected==0 else None
        xs=None
    if isinstance(actual,float) and not math.isfinite(actual):actual=repr(actual)
    rows.append(dict(case=name,expected=expected,actual=actual,
                     expected_zero_sign=es,actual_zero_sign=xs,passed=passed))

points=[
    (M,1.,M),(math.nextafter(1.,math.inf),-M,M),(10.,-1.,.1),(-M,1.,-M),
    (0.,T,1.),(0.,T,-1.),(1.,M,T),(1.,M,-T),(M,1.,0.),(M,1.,-0.),
    (0.,0.,1.),(-1.,1.,1.),(-2.,1.,1.),
    (math.nextafter(-.5,math.inf),1.,2.),(-.5,1.,2.),
    (1.,1.,2.),(.5,1.,2.),(0.,1.,2.),(5.,1.,2.),
    (1.,M,M),(-1.,M,-M),(M,M,-M),
]
for i,args in enumerate(points):
    observe("complete reciprocal "+str(i),lambda a=args:m.logarithm_derivative(*a),reference(*args))
observe("retained defaults",lambda:m.logarithm_derivative(1.),reference(1.,1.,2.))
for label,args,expected in [
    ("bool x",(True,1,2),"TypeError"),("bool offset",(1,True,2),"TypeError"),
    ("bool slope",(1,1,True),"TypeError"),("nan x",(math.nan,1,2),"ValueError"),
    ("infinite offset",(1,math.inf,2),"ValueError"),
    ("infinite slope",(1,1,math.inf),"ValueError"),
    ("zero slope invalid x",(math.nan,1,0),"ValueError"),
    ("zero slope invalid argument",(1,-1,0),"ValueError"),
    ("huge integer",(10**400,1,2),"ValueError"),("text offset",(1,"2",2),"TypeError"),
]:
    observe(label,lambda a=args:m.logarithm_derivative(*a),expected)

# Explicit retained policy: exact argument positive does not widen the old gate.
argument=Fraction(-1)+Fraction(.1)*10
assert argument>0 and rounded_argument(10.,-1.,.1)==0.
print(json.dumps(dict(domain_policy=dict(probe_exact_argument_positive=argument>0,
                                       probe_rounded_argument_zero=True,
                                       retained_rejection="ValueError"),
                      observations=rows),allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
