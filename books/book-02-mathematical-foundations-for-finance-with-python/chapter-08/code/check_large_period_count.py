"""Independent count-conversion and complete-power references, Section 8.4.

Optional directory argument selects the exact original section_8_04.py.
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
    if not (directory/"section_8_04.py").is_file():
        raise SystemExit("requested source module is missing")
    sys.path.insert(0,str(directory))
m=importlib.import_module("section_8_04")
M,T=sys.float_info.max,math.ulp(0.0)
rows=[]

def base_reference(n,z):
    # Decimal conversion independently models the existing float denominator
    # rounding; use the exact count only beyond its conversion range.
    with localcontext() as ctx:
        ctx.prec=2500
        scaled=float(Decimal.from_float(.001)*Decimal.from_float(float(z)))
        rate=float(Decimal.from_float(.04)+Decimal.from_float(scaled))
        converted=float(Decimal(n))
        denominator=Decimal.from_float(converted) if math.isfinite(converted) else Decimal(n)
        ratio=float(Decimal.from_float(rate)/denominator)
        return float(Decimal(1)+Decimal.from_float(ratio))

def reference(p,n,t,z,derivative=False,precision=1600):
    p,t=float(p),float(t)
    b=base_reference(n,z)
    if b<=0:return "ValueError"
    if p==0 or t==0:return p*t*.001 if derivative else p
    coefficient=Fraction(p)*(Fraction(t)*Fraction(.001) if derivative else 1)
    exponent=Fraction(n)*Fraction(t)-(1 if derivative else 0)
    if b==1 or exponent==0:
        value=coefficient
    elif exponent>10**100:
        # Any binary64 b different from one has |ln(b)| > 2^-54.
        # This dominates all finite coefficient logs in these interfaces.
        return "ValueError" if b>1 else 0.0
    else:
        with localcontext() as ctx:
            ctx.prec=precision
            power=Decimal(exponent.numerator)/Decimal(exponent.denominator)
            value=(Decimal(coefficient.numerator)/Decimal(coefficient.denominator))*Decimal.from_float(b)**power
    try:result=float(value)
    except OverflowError:return "ValueError"
    return result if math.isfinite(result) else "ValueError"

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

# Midpoint above maximum finite: conversion rounds to the overflowing endpoint.
H=2**1024-2**970
factor=(math.nextafter(1.0,math.inf)-.04)/.001
points=[
    (1.,10**400,1.,0.),(0.,10**400,1.,0.),(M,10**400,1.,0.),
    (-0.,10**400,1.,M),(1.,10**400,M,0.),
    (1.,10**310,1e-308,M),(1.,10**310,1e-308,-M),
    (1.,H-1,1e-308,M),(1.,H,1e-308,M),(1.,H+1,1e-308,M),
    (1.,int(M),T,M),(1.,H,0.,M),(M,H,-0.,M),
    (1.,2**53+1,1.,factor),(1.,2**53+1,.5,factor),
    (1.,10**400,1.,M),(1.,10**310,1.,M),(1.,10**310,1.,-M),
]
for i,args in enumerate(points):
    for derivative in (False,True):
        expected=reference(*args,derivative=derivative)
        assert expected==reference(*args,derivative=derivative,precision=2200)
        fn=m.discrete_future_value_derivative if derivative else m.discrete_future_value
        observe(("sensitivity" if derivative else "value")+str(i),
                lambda f=fn,a=args:f(*a),expected)
    _,n,_,z=args
    observe("base"+str(i),lambda n=n,z=z:m._discrete_inputs(1.,n,1.,z)[2],base_reference(n,z))
for fn in (m.discrete_future_value,m.discrete_future_value_derivative):
    for label,args,expected in [
        ("negative count",(1,-1,1,0),"ValueError"),
        ("zero count",(1,0,1,0),"ValueError"),
        ("bool count",(1,True,1,0),"ValueError"),
        ("float count",(1,1.,1,0),"ValueError"),
        ("text count",(1,"10",1,0),"ValueError"),
        ("negative principal",(-1,10**400,1,0),"ValueError"),
        ("negative horizon",(1,10**400,-1,0),"ValueError"),
        ("bool factor",(1,10**400,1,True),"TypeError"),
        ("nonfinite factor",(1,10**400,1,math.nan),"ValueError"),
        ("zero principal invalid factor",(0,10**400,1,math.nan),"ValueError"),
        ("zero horizon invalid count",(1,True,0,0),"ValueError"),
        ("zero principal invalid base",(0,1,1,-2000),"ValueError"),
    ]:
        observe(fn.__name__+" "+label,lambda f=fn,a=args:f(*a),expected)
print(json.dumps(rows,allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
