"""Independent complete-power references for Section 8.4 discrete FV.

Optional directory argument selects the exact baseline section_8_04.py.
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
    with localcontext() as ctx:
        ctx.prec=2500
        scaled=float(Decimal.from_float(.001)*Decimal.from_float(float(z)))
        rate=float(Decimal.from_float(.04)+Decimal.from_float(scaled))
        divided=float(Decimal.from_float(rate)/Decimal(n))
        return float(Decimal(1)+Decimal.from_float(divided))

def reference(p,n,t,z,derivative=False,precision=1600):
    p,t=float(p),float(t)
    b=base_reference(n,z)
    if b<=0:
        return "ValueError"
    if p==0 or t==0:
        return p*t*.001 if derivative else p
    exponent=Fraction(n)*Fraction(t)-(1 if derivative else 0)
    coefficient=Fraction(p)*(Fraction(t)*Fraction(.001) if derivative else 1)
    # Exact rational powers are an independent oracle for selected integer powers.
    if b==1 or exponent==0:
        value=coefficient
    elif exponent.denominator==1 and abs(exponent.numerator)<=2000:
        value=coefficient*Fraction(b)**exponent.numerator
    else:
        with localcontext() as ctx:
            ctx.prec=precision
            power=Decimal(exponent.numerator)/Decimal(exponent.denominator)
            db=Decimal.from_float(b)
            # Here selected noninteger exponents are bounded; huge test exponents
            # use b=1 or b>=2, whose overflow is immediate by monotonicity.
            if power>100000 and b>=2:
                return "ValueError"
            value=(Decimal(coefficient.numerator)/Decimal(coefficient.denominator))*db**power
    try:
        result=float(value)
    except OverflowError:
        return "ValueError"
    return result if math.isfinite(result) else "ValueError"

def observe(name,fn,expected):
    try:
        actual=fn()
        passed=not isinstance(expected,str) and actual==expected
        if isinstance(expected,float) and expected==0 and actual==0:
            passed=passed and math.copysign(1,actual)==math.copysign(1,expected)
    except Exception as exc:
        actual=type(exc).__name__
        passed=actual==expected
    if isinstance(actual,float) and not math.isfinite(actual):
        actual=repr(actual)
    rows.append(dict(case=name,expected=expected,actual=actual,passed=passed))

decay=(math.exp(-1)-1-.04)/.001
growth=(math.exp(1)-1-.04)/.001
points=[
    (M,1,1000.,decay),(T,1,1000.,growth),(0.,1,1000.,M),
    (-0.,1,1000.,M),(M,1,0.,M),(M,1,-0.,M),
    (2000.,12,2.,1.),(1.,12,.125,0.),(M,1,1.,growth),
    (T,1,1000.,decay),(M,1,.25,decay),(T,1,.25,growth),
    (1.,2**53+1,1.,0.),(M,10**300,1.,0.),
    (1.,1,M,1000.),(1e-100,1,1.,-40.),
    (M,1,1.,-40.),(M,1,2.,-40.),
    (1.,1,T,growth),(T,1,T,-40.),
    (1.,2**53+1,1.,1960.),(1.,2**53+1,.5,1960.),
]
for i,args in enumerate(points):
    for derivative in (False,True):
        expected=reference(*args,derivative=derivative)
        assert expected==reference(*args,derivative=derivative,precision=2200)
        fn=m.discrete_future_value_derivative if derivative else m.discrete_future_value
        observe(("sensitivity" if derivative else "value")+str(i),
                lambda f=fn,a=args:f(*a),expected)

for i,(n,z) in enumerate([(1,decay),(1,growth),(12,1.),(2**53+1,0.),(10**300,0.),(2**53+1,1960.)]):
    observe("rounded base "+str(i),lambda n=n,z=z:1+m.nominal_rate(z)/n,base_reference(n,z))
for fn in (m.discrete_future_value,m.discrete_future_value_derivative):
    for label,args,expected in [
        ("negative principal",(-1,1,1,0),"ValueError"),
        ("negative horizon",(1,1,-1,0),"ValueError"),
        ("zero periods",(1,0,1,0),"ValueError"),
        ("bool periods",(1,True,1,0),"ValueError"),
        ("float periods",(1,1.,1,0),"ValueError"),
        ("negative base",(1,1,1,-2000),"ValueError"),
        ("zero principal invalid base",(0,1,1,-2000),"ValueError"),
        ("zero horizon invalid base",(1,1,0,-2000),"ValueError"),
        ("bool principal",(True,1,1,0),"TypeError"),
        ("bool horizon",(1,1,True,0),"TypeError"),
        ("nonfinite factor",(1,1,1,math.nan),"ValueError"),
        ("nonfinite horizon",(1,1,math.inf,0),"ValueError"),
    ]:
        observe(fn.__name__+" "+label,lambda f=fn,a=args:f(*a),expected)
print(json.dumps(rows,allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
