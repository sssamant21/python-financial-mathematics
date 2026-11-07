"""Section 8.4 actual callback and sampled-quotient contract checks.

Run normally, or pass a directory containing the exact baseline section_8_04.py.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
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

def observe(name, fn, expected):
    try:
        actual = fn()
        passed = not isinstance(expected, str) and actual == expected
        if isinstance(expected, float) and expected == 0 and actual == 0:
            passed = passed and math.copysign(1, actual) == math.copysign(1, expected)
    except Exception as exc:
        actual = type(exc).__name__
        passed = actual == expected
    if isinstance(actual, float) and not math.isfinite(actual):
        actual = repr(actual)
    rows.append(dict(case=name, expected=expected, actual=actual, passed=passed))

def product_reference(a, b):
    # Exact represented operands, high-precision independent Decimal product.
    with localcontext() as ctx:
        ctx.prec = 2500
        value = float(Decimal.from_float(a)*Decimal.from_float(b))
    return value if math.isfinite(value) else "ValueError"

pairs = [(M, 2.0), (-M, 2.0), (M, -2.0), (M, .5),
         (M, 0.0), (-M, 0.0), (T, .5), (-T, .5),
         (T, 1.0), (1.5, 4.0), (-0.0, 1.0), (0.0, -1.0)]
for index, (a, b) in enumerate(pairs):
    observe("chain product "+str(index),
            lambda a=a,b=b:m.chain_derivative(lambda _:a, lambda x:x, lambda _:b, 3.0),
            product_reference(a,b))

trace = []
def inner(x):
    trace.append(["inner", x])
    return x+1
def outer(x):
    trace.append(["outer", x])
    return 3.0
def derivative(x):
    trace.append(["derivative", x])
    return 4.0
observe("ordinary chain", lambda:m.chain_derivative(outer,inner,derivative,2), 12.0)
observe("chain order arguments", lambda:trace, [["inner",2.0],["outer",3.0],["derivative",2.0]])

class MarkerError(Exception):
    pass
marker = MarkerError("callback marker")
for where in ("inner", "outer", "derivative"):
    seen = []
    def callback(name, result):
        def fn(x):
            seen.append(name)
            if name == where:
                raise marker
            return result
        return fn
    def run():
        try:
            m.chain_derivative(callback("outer",3.0),callback("inner",2.0),
                               callback("derivative",4.0),1.0)
        except MarkerError as exc:
            return exc is marker
        return False
    observe("exception identity "+where, run, True)
    order = ["inner","outer","derivative"]
    observe("exception short circuit "+where, lambda:seen, order[:order.index(where)+1])

for where in ("inner","outer","derivative"):
    seen=[]
    def callback(name, result):
        def fn(x):
            seen.append(name)
            return math.nan if name == where else result
        return fn
    observe("nonfinite "+where,
            lambda:m.chain_derivative(callback("outer",3.0),callback("inner",2.0),
                                       callback("derivative",4.0),1.0), "ValueError")
    order=["inner","outer","derivative"]
    observe("nonfinite short circuit "+where, lambda:seen, order[:order.index(where)+1])

for name, fn, expected in [
    ("chain callable preflight",lambda:m.chain_derivative(None,inner,derivative,math.nan),"TypeError"),
    ("chain bool control",lambda:m.chain_derivative(outer,inner,derivative,True),"TypeError"),
    ("chain nonfinite control",lambda:m.chain_derivative(outer,inner,derivative,math.inf),"ValueError"),
    ("center callable priority",lambda:m.centered_difference(None,math.nan,0),"TypeError"),
    ("center zero step",lambda:m.centered_difference(lambda x:x,0,0),"ValueError"),
    ("center bool step",lambda:m.centered_difference(lambda x:x,0,True),"TypeError"),
]:
    observe(name,fn,expected)

# Sampled quotients use exact rational references for represented sample values.
for index,(first,second,h) in enumerate([
    (M,-M,M),(-M,M,-M),(T,-T,T),(M,M,M),(3.0,1.0,.5),
    (M,-M,T),(-M,M,T),
]):
    try:
        expected=float((Fraction(first)-Fraction(second))/(2*Fraction(h)))
    except OverflowError:
        expected="ValueError"
    samples=[]
    def function(x):
        samples.append(x)
        return first if len(samples)==1 else second
    observe("sampled quotient "+str(index),lambda:m.centered_difference(function,0.0,h),expected)
    observe("sampled argument order "+str(index),lambda:samples,[h,-h])

for label,x,h in [("collapsed",M,1.0),("overflowed points",M,M)]:
    samples=[]
    def function(z):
        samples.append(z)
        return z
    observe(label,lambda:m.centered_difference(function,x,h),"ValueError")
    observe(label+" callback count",lambda:len(samples),0)

samples=[]
def identity(x):
    samples.append(x)
    return x
observe("default step value",lambda:m.centered_difference(identity,0.0),1.0)
observe("default step arguments",lambda:samples,[1e-4,-1e-4])
observe("center bool callback",lambda:m.centered_difference(lambda _:True,0,1),"TypeError")
observe("center nonfinite callback",lambda:m.centered_difference(lambda _:math.inf,0,1),"ValueError")
def raising(_):
    raise marker
def exception_identity():
    try:
        m.centered_difference(raising,0,1)
    except MarkerError as exc:
        return exc is marker
    return False
observe("center exception identity",exception_identity,True)

print(json.dumps(rows,allow_nan=False))
assert all(row["passed"] for row in rows),[row for row in rows if not row["passed"]]
