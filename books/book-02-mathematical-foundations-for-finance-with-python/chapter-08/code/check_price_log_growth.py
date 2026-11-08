"""Independent represented-base price and log-growth checks, Section 8.4.

Optional directory argument selects the exact original section_8_04.py.
"""
from decimal import Decimal, localcontext
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
M=sys.float_info.max
rows=[]

def base_reference(t):
    with localcontext() as ctx:
        ctx.prec=2500
        product=float(Decimal.from_float(.02)*Decimal.from_float(float(t)))
        return float(Decimal(1)+Decimal.from_float(product))

def price_reference(t):
    base=base_reference(t)
    with localcontext() as ctx:
        ctx.prec=2500
        b=Decimal.from_float(base)
        # Exact complete Decimal monomials; production uses rational power.
        value=float(Decimal(100)*b*b*b)
    return value if math.isfinite(value) else "OverflowError"

def growth_reference(t):
    return float(Fraction(.06)/Fraction(base_reference(t)))

def from_bits(bits):
    return struct.unpack(">d",bits.to_bytes(8,"big"))[0]

# Rounded multiplication/addition and positive cubic are monotone for t>=0.
low,high=0,0x7fefffffffffffff
assert price_reference(0.)==100. and price_reference(M)=="OverflowError"
while high-low>1:
    middle=(low+high)//2
    if price_reference(from_bits(middle))=="OverflowError":high=middle
    else:low=middle
last_finite,first_overflow=from_bits(low),from_bits(high)
minimum_time=math.nextafter(-50.,math.inf)
minimum_base=base_reference(minimum_time)
maximum_base=base_reference(M)
assert minimum_base==2.**-53 and 0<maximum_base<M
bounds=dict(minimum_base=minimum_base,maximum_base=maximum_base,
            minimum_growth=growth_reference(M),maximum_growth=growth_reference(minimum_time))

def observe(name,fn,expected):
    try:
        actual=fn()
        passed=not isinstance(expected,str) and actual==expected
    except Exception as exc:
        actual=type(exc).__name__;passed=actual==expected
    if isinstance(actual,float) and not math.isfinite(actual):actual=repr(actual)
    rows.append(dict(case=name,expected=expected,actual=actual,passed=passed))

points=[minimum_time,math.nextafter(minimum_time,math.inf),-49.,-1.,-0.,0.,
        math.ulp(0.),sys.float_info.min,1.,3.,1e103,1e104,M]
rng=random.Random(111)
points.extend(math.ldexp(rng.uniform(.5,2),rng.choice([-1000,0,10,100,300])) for _ in range(8))
points.extend(from_bits(bits) for bits in [low-1,low,high])
for i,t in enumerate(points):
    observe("price "+str(i),lambda t=t:m.price(t),price_reference(t))
    observe("log growth "+str(i),lambda t=t:m.log_price_growth(t),growth_reference(t))
for fn in (m.price,m.log_price_growth):
    for label,t,expected in [
        ("domain boundary",-50.,"ValueError"),
        ("below domain",math.nextafter(-50.,-math.inf),"ValueError"),
        ("bool",True,"TypeError"),("text","3","TypeError"),
        ("nan",math.nan,"ValueError"),("infinite",math.inf,"ValueError"),
        ("huge integer",10**400,"ValueError"),
    ]:
        observe(fn.__name__+" "+label,lambda f=fn,t=t:f(t),expected)
print(json.dumps(dict(boundary=dict(last_finite_time=last_finite,
                                  first_overflow_time=first_overflow,
                                  adjacent_bits=high-low),
                      finite_growth_bounds=bounds,observations=rows),allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
