"""Independent Decimal references for Section 8.2 cost and marginal cost.

Optional positional argument: directory containing the baseline Section 8.2
module. Emits JSON observations and exits nonzero when a contract fails.
"""
from decimal import Decimal, localcontext
import importlib
import json
import math
from pathlib import Path
import sys

if len(sys.argv) > 1:
    directory = Path(sys.argv[1]).resolve()
    if not (directory / "section_8_02.py").is_file():
        raise SystemExit("requested source module is missing")
    sys.path.insert(0, str(directory))
m = importlib.import_module("section_8_02")
rows = []

def reference(q, derivative=False):
    # Separate monomials, distinct from the production rational Horner method.
    with localcontext() as ctx:
        ctx.prec = 2500
        x = Decimal.from_float(float(q))
        a = Decimal.from_float(0.05)
        result = Decimal(20)+2*a*x if derivative else Decimal(1000)+20*x+a*x*x
        value = float(result)
        return value if math.isfinite(value) else "OverflowError"

def observe(name, fn, expected):
    try:
        actual = fn()
        passed = not isinstance(expected, str) and actual == expected
    except Exception as exc:
        actual = type(exc).__name__
        passed = actual == expected
    if isinstance(actual, float) and not math.isfinite(actual):
        actual = repr(actual)
    rows.append(dict(case=name, expected=expected, actual=actual, passed=passed))

with localcontext() as ctx:
    ctx.prec = 120
    a = Decimal.from_float(0.05)
    boundary = float((-20+(Decimal(400)-4*a*(1000-Decimal.from_float(sys.float_info.max))).sqrt())/(2*a))

points = [0.0, -0.0, math.ulp(0.0), sys.float_info.min, 1.0, 3.0,
          100.0, 500.0, 1e10, 1e100, 5e154, boundary,
          math.nextafter(boundary, 0), math.nextafter(boundary, math.inf),
          1e155, sys.float_info.max]
for index, q in enumerate(points):
    for derivative in (False, True):
        fn = m.marginal_cost if derivative else m.cost
        name = ("marginal" if derivative else "cost")+str(index)
        observe(name, lambda f=fn, x=q: f(x), reference(q, derivative))

for fn in (m.cost, m.marginal_cost):
    for label, value, expected in [
        ("negative", -1.0, "ValueError"),
        ("nan", math.nan, "ValueError"),
        ("infinity", math.inf, "ValueError"),
        ("bool", True, "TypeError"),
        ("text", "10", "TypeError"),
        ("huge integer", 10**400, "ValueError"),
    ]:
        observe(fn.__name__+" "+label, lambda f=fn, q=value: f(q), expected)

# The all-finite [0,500] composed interfaces keep their exact call relationship.
for q in (0.0, 100.0, 500.0):
    observe("profit composition "+str(q), lambda x=q: m.profit(x),
            m.revenue(q)-m.cost(q))
    observe("marginal composition "+str(q), lambda x=q: m.marginal_profit(x),
            m.marginal_revenue(q)-m.marginal_cost(q))

print(json.dumps(rows, allow_nan=False))
assert all(row["passed"] for row in rows), [row for row in rows if not row["passed"]]
