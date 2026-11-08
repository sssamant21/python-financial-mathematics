"""Independent expanded-polynomial oracle for Section 8.4 nested derivative.

Optional directory argument selects the exact baseline section_8_04.py.
"""
from fractions import Fraction
import importlib
import json
import math
from pathlib import Path
import random
import struct
import sys
if len(sys.argv)>1:
    directory=Path(sys.argv[1]).resolve()
    if not (directory/"section_8_04.py").is_file():
        raise SystemExit("requested source module is missing")
    sys.path.insert(0,str(directory))
m=importlib.import_module("section_8_04")
M,T=sys.float_info.max,math.ulp(0.0)
rows=[]

def reference(x):
    x=float(x)
    if x==0:return x
    q=Fraction(x)
    # Algebraic expansion independent of the production factored form.
    result=648*q**7+1296*q**5+864*q**3+192*q
    try:return float(result)
    except OverflowError:return "OverflowError"

def from_bits(bits):
    return struct.unpack(">d",bits.to_bytes(8,"big"))[0]

# Positive coefficients make the expanded polynomial strictly increasing for x>=0.
low,high=0,0x7fefffffffffffff
assert reference(from_bits(low))==0.0 and reference(from_bits(high))=="OverflowError"
while high-low>1:
    middle=(low+high)//2
    if reference(from_bits(middle))=="OverflowError":high=middle
    else:low=middle
last_finite,first_overflow=from_bits(low),from_bits(high)

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

points=[0.,-0.,T,-T,sys.float_info.min,-sys.float_info.min,1e-100,-1e-100,
        -3.,-1.,1.,2.,5.,4e43,-4e43,4.5e43,-4.5e43,1e100,-1e100,M,-M]
rng=random.Random(110)
points.extend(math.ldexp(rng.uniform(-2,2),rng.choice([-1000,-500,-50,10,50,100,140]))
              for _ in range(12))
for bits in [low-1,low,high]:
    points.extend([from_bits(bits),-from_bits(bits)])
for i,x in enumerate(points):
    observe("expanded polynomial "+str(i),lambda x=x:m.nested_power_derivative(x),reference(x))
for name,x,expected in [
    ("bool",True,"TypeError"),("text","2","TypeError"),
    ("complex",1+0j,"TypeError"),("nan",math.nan,"ValueError"),
    ("infinite",math.inf,"ValueError"),("huge integer",10**400,"ValueError"),
]:
    observe(name,lambda x=x:m.nested_power_derivative(x),expected)
print(json.dumps(dict(boundary=dict(last_finite_input=last_finite,
                                  first_overflow_input=first_overflow,
                                  adjacent_bits=high-low),
                      observations=rows),allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
