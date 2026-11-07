"""Independent exact power-sum references and Section 8.2 contract checks.

Run without arguments for corrected source, or pass a directory containing the
baseline section_8_02.py. JSON observations are emitted even on failure.
"""
from fractions import Fraction
import importlib
import json
import math
from pathlib import Path
import random
import sys

if len(sys.argv) > 1:
    directory = Path(sys.argv[1]).resolve()
    if not (directory / "section_8_02.py").is_file():
        raise SystemExit("requested source module is missing")
    sys.path.insert(0, str(directory))
module = importlib.import_module("section_8_02")
M = sys.float_info.max
T = math.ulp(0.0)
rows = []

def observe(name, fn, expected):
    try:
        actual = fn()
        passed = type(expected) is not str and actual == expected
        if isinstance(actual, float) and actual == 0 and expected == 0:
            passed = passed and math.copysign(1, actual) == math.copysign(1, expected)
    except Exception as exc:
        actual = type(exc).__name__
        passed = actual == expected
    rows.append(dict(case=name, expected=expected, actual=actual, passed=passed))

def reference(coeffs, x, derivative=False):
    # Direct monomial sum, deliberately not the implementation's Horner recurrence.
    a, point = tuple(map(Fraction, coeffs)), Fraction(x)
    terms = [i*a[i]*point**(i-1) for i in range(1, len(a))] if derivative else [
        a[i]*point**i for i in range(len(a))]
    try:
        return float(sum(terms, Fraction(0)))
    except OverflowError:
        return "OverflowError"

vectors = [
    ([-M, M], 2.0), ([M, M], -2.0),
    ([0, M, -M], 2.0), ([0, -M, M], -2.0),
    ([0, T, T], 0.5), ([0, -T, -T], 0.5),
    ([M, 0, M], 2.0), ([0, 0, M], 0.0),
    ([0, 0, M], 0.25), ([M, -M, M], 1.0),
    ([T, 0, T], -0.5), ([12], M),
]
rng = random.Random(802)
for _ in range(12):
    vectors.append(([rng.choice([-M, M, T, -T, 0.0, 1.0, -1.0])
                     for _ in range(rng.randint(2, 7))],
                    rng.choice([-2.0, -0.5, 0.0, 0.5, 2.0])))
for i, (values, point) in enumerate(vectors):
    for derivative in (False, True):
        function = module.polynomial_derivative if derivative else module.polynomial
        observe(("derivative" if derivative else "polynomial")+str(i),
                lambda f=function, a=values, x=point: f(a, x),
                reference(values, point, derivative))

observe("coefficient overflow", lambda: module.derivative_coefficients([0, 0, M]), "OverflowError")
observe("constant coefficients", lambda: module.derivative_coefficients([M]), (0.0,))
observe("ordinary coefficients", lambda: module.derivative_coefficients([12, -9, 5, -3, 7]),
        (-9.0, 10.0, -9.0, 28.0))
for name, function, args, expected in [
    ("empty", module.polynomial, ([], 0), "ValueError"),
    ("noniterable", module.polynomial, (None, 0), "TypeError"),
    ("bool coefficient", module.polynomial, ([True], 0), "TypeError"),
    ("nan coefficient", module.polynomial, ([math.nan], 0), "ValueError"),
    ("infinite point", module.polynomial_derivative, ([1], math.inf), "ValueError"),
    ("bool point", module.polynomial_derivative, ([1], True), "TypeError"),
]:
    observe(name, lambda f=function, a=args: f(*a), expected)

calls = []
def callback(x):
    calls.append(x)
    return x
observe("collapsed step", lambda: module.centered_difference(callback, M, 1), "ValueError")
observe("preflight no callbacks", lambda: len(calls), 0)
observe("sample overflow", lambda: module.centered_difference(lambda x: x, M, M), "ValueError")
observe("complete sampled quotient", lambda: module.centered_difference(lambda x: x, 0, M), 1.0)
observe("nonfinite result", lambda: module.centered_difference(lambda x: M if x > 0 else -M, 0, T),
        "ValueError")
observe("signed step", lambda: module.centered_difference(lambda x: x*x, 2, -0.5), 4.0)
observe("callback nan", lambda: module.centered_difference(lambda x: math.nan, 0, 1), "ValueError")

def serializable(value):
    if isinstance(value, float) and not math.isfinite(value):
        return repr(value)
    if isinstance(value, (tuple, list)):
        return [serializable(item) for item in value]
    if isinstance(value, dict):
        return {key: serializable(item) for key, item in value.items()}
    return value

print(json.dumps(serializable(rows), allow_nan=False))
assert all(row["passed"] for row in rows), [row for row in rows if not row["passed"]]
