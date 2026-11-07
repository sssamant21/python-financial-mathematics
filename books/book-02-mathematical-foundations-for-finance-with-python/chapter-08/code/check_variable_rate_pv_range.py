"""Independent log-scale references for Section 8.4 variable-rate PV.

Optional argument: directory with the exact original section_8_04.py.
"""
from decimal import Decimal, localcontext
import importlib
import json
import math
from pathlib import Path
import sys

if len(sys.argv) > 1:
    directory = Path(sys.argv[1]).resolve()
    if not (directory / "section_8_04.py").is_file():
        raise SystemExit("requested source module is missing")
    sys.path.insert(0, str(directory))
m = importlib.import_module("section_8_04")
M, T = sys.float_info.max, math.ulp(0.0)
rows = []

def rounded_rate(z):
    # Independently round each represented affine operation.
    with localcontext() as ctx:
        ctx.prec = 2500
        scaled = float(Decimal.from_float(.002)*Decimal.from_float(float(z)))
        return float(Decimal.from_float(.03)+Decimal.from_float(scaled))

def reference(c, t, z, derivative=False, precision=1800):
    c,t = float(c),float(t)
    if c == 0 or t == 0:
        return -t*c*.002 if derivative else c
    rate = rounded_rate(z)
    with localcontext() as ctx:
        ctx.prec = precision
        dc,dt,dr = map(Decimal.from_float,(c,t,rate))
        exponent = -dt*dr
        # Bounds far beyond all possible log coefficients in this interface.
        if exponent < -100000:
            return -0.0 if derivative else 0.0
        if exponent > 100000:
            return "ValueError"
        log_value = dc.ln()+exponent
        if derivative:
            log_value += dt.ln()+Decimal.from_float(.002).ln()
        value = float(log_value.exp())
        if not math.isfinite(value):
            return "ValueError"
        return -value if derivative else value

def observe(name, fn, expected):
    try:
        actual = fn()
        passed = not isinstance(expected,str) and actual == expected
        if isinstance(expected,float) and expected == 0 and actual == 0:
            passed = passed and math.copysign(1,actual)==math.copysign(1,expected)
    except Exception as exc:
        actual = type(exc).__name__
        passed = actual == expected
    if isinstance(actual,float) and not math.isfinite(actual):
        actual = repr(actual)
    rows.append(dict(case=name,expected=expected,actual=actual,passed=passed))

near_zero = math.nextafter(-15.0,math.inf)
points = [
    (M,1000.0,485.0),(T,1000.0,-515.0),
    (0.0,M,-M),(-0.0,M,-M),(M,0.0,M),(M,-0.0,M),
    (1.0,M,-15.0),(M,M,-15.0),(1e-100,M,-15.0),
    (T,T,-15.0),(M,T,485.0),(1.0,M,M),(1.0,M,-M),
    (T,1e-300,-5e305),(1.0,750.0/rounded_rate(near_zero),near_zero),
    (1000.0,4.0,1.0),(1000.0,4.0,-5.0),(1.0,1.0,485.0),
]
for index,args in enumerate(points):
    for derivative in (False,True):
        expected = reference(*args,derivative=derivative)
        assert expected == reference(*args,derivative=derivative,precision=2400)
        fn = m.variable_rate_pv_derivative if derivative else m.variable_rate_pv
        observe(("sensitivity" if derivative else "PV")+str(index),
                lambda f=fn,a=args:f(*a),expected)

for index,z in enumerate([-M,-515.0,-15.0,near_zero,485.0,M]):
    observe("rate rounding "+str(index),lambda z=z:m.rate_from_factor(z),rounded_rate(z))
for fn in (m.variable_rate_pv,m.variable_rate_pv_derivative):
    for label,args,expected in [
        ("negative amount",(-1,1,0),"ValueError"),
        ("negative horizon",(1,-1,0),"ValueError"),
        ("bool amount",(True,1,0),"TypeError"),
        ("bool horizon",(1,True,0),"TypeError"),
        ("bool factor",(1,1,True),"TypeError"),
        ("nonfinite amount",(math.inf,1,0),"ValueError"),
        ("nonfinite horizon",(1,math.nan,0),"ValueError"),
        ("nonfinite factor",(1,1,math.inf),"ValueError"),
        ("zero amount invalid factor",(0,1,math.nan),"ValueError"),
        ("zero horizon invalid factor",(1,0,math.nan),"ValueError"),
    ]:
        observe(fn.__name__+" "+label,lambda f=fn,a=args:f(*a),expected)
observe("derivative horizon validation priority",
        lambda:m.variable_rate_pv_derivative(math.nan,True,0),"TypeError")
print(json.dumps(rows,allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
