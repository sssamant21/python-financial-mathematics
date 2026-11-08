"""Independent Section 8.5 accumulation references; prints evidence before asserting."""
import json
import math
import sys
from functools import lru_cache
from decimal import Decimal, localcontext
import section_8_05 as subject

FUNCTIONS = ("accumulation", "accumulation_time_derivative", "accumulation_rate_derivative")
T, M = math.ulp(0.), sys.float_info.max

def signzero(x):
    return int(math.copysign(1, x)) if x == 0 else None

@lru_cache(maxsize=None)
def oracle_log(value, precision):
    with localcontext() as ctx:
        ctx.prec = precision
        return Decimal.from_float(value).ln()

def reference(args, kind, precision):
    p, r, t = map(float, args)
    factor = (1., r, t)[kind]
    negative = (math.copysign(1, p) < 0) != (math.copysign(1, factor) < 0)
    if p == 0 or factor == 0:
        return -0. if negative else 0.
    with localcontext() as ctx:
        ctx.prec = precision
        dp, dr, dt, df = map(Decimal.from_float, (p, r, t, abs(factor)))
        # Independent log-amplitude oracle; implementation uses rational coefficients/direct exp.
        amplitude = oracle_log(abs(p), precision) + oracle_log(abs(factor), precision) + dr*dt
        if amplitude > 1000:
            return "ValueError"
        if amplitude < -1000:
            return -0. if negative else 0.
        value = float(amplitude.exp())
        if not math.isfinite(value):
            return "ValueError"
        return -value if negative else value

def observe(fn, args):
    try:
        value = fn(*args)
        return (value if math.isfinite(value) else repr(value)), signzero(value), None
    except Exception as exc:
        return type(exc).__name__, None, str(exc)

def token(x):
    return repr(x) if type(x) is float and not math.isfinite(x) else x

def run():
    cases = [
        (T, 1., 1000.), (1., -1., 750.), (M, T, M), (0., M, M),
        (-0., M, M), (0., -M, M), (-0., -M, M),
        (1., -M, M), (M, -M, M), (T, M, M),
        (1., 0., M), (M, -0., M), (M, M, 0.), (M, -M, -0.),
        (T, 0., T), (T, -T, T), (T, T, M), (M, -T, M),
        (1000., .04, 5.), (1000., -.04, 5.), (1., 1., 709.),
        (1., 1., 710.), (1., -1., 744.), (1., -1., 745.),
        (M, -1., 1000.), (T, 1., 1450.), (T, 1., 1500.),
        (T, -1., 0.), (M, -1., 0.), (1., .1, 10.),
        (2., math.nextafter(.1, 0.), 10.)]
    rows = []
    for i, args in enumerate(cases):
        for kind, name in enumerate(FUNCTIONS):
            expected = reference(args, kind, 1600)
            repeated = reference(args, kind, 2200)
            assert expected == repeated and (
                isinstance(expected, str) or signzero(expected) == signzero(repeated))
            actual, zs, message = observe(getattr(subject, name), args)
            passed = actual == expected if isinstance(expected, str) else (
                type(actual) in (int, float) and
                math.isclose(actual, expected, rel_tol=4e-15, abs_tol=0.) and
                zs == signzero(expected))
            rows.append(dict(case=i, function=name, args=list(args),
                expected=expected, expected_zero_sign=None if isinstance(expected,str) else signzero(expected),
                actual=actual, actual_zero_sign=zs, exception_message=message, passed=passed))
    guards = [
        ((True,.1,1.),"TypeError","principal"), ((1.,True,1.),"TypeError","rate"),
        ((1.,.1,True),"TypeError","years"),
        ((-1.,.1,1.),"ValueError","principal and years"),
        ((1.,.1,-1.),"ValueError","principal and years"),
        ((math.inf,.1,1.),"ValueError","principal"),
        ((1.,math.nan,1.),"ValueError","rate"),
        ((1.,.1,math.inf),"ValueError","years"),
        ((10**400,.1,1.),"ValueError","principal"),
        ((1.,10**400,1.),"ValueError","rate"),
        ((1.,.1,10**400),"ValueError","years"),
        ((0.,"bad",1.),"TypeError","rate"),
        ((0.,.1,-1.),"ValueError","principal and years")]
    for args, expected, prefix in guards:
        for name in FUNCTIONS:
            actual,zs,message=observe(getattr(subject,name),args)
            rows.append(dict(function=name,args=[token(x) for x in args],expected=expected,
                expected_message_prefix=prefix,actual=actual,exception_message=message,
                passed=actual==expected and message.startswith(prefix)))
    for name,prefix in zip(FUNCTIONS,("principal","rate","years")):
        args=("bad",True,"bad")
        actual,zs,message=observe(getattr(subject,name),args)
        rows.append(dict(function=name,args=list(args),expected="TypeError",
            expected_message_prefix=prefix,actual=actual,exception_message=message,
            passed=actual=="TypeError" and message.startswith(prefix)))
    original=subject.accumulation
    def forbidden(*args):
        raise AssertionError("sensitivity called rounded accumulation")
    subject.accumulation=forbidden
    try:
        for kind,name in enumerate(FUNCTIONS[1:],1):
            args=(2.,.125,4.)
            expected=reference(args,kind,1600)
            actual,zs,message=observe(getattr(subject,name),args)
            rows.append(dict(function=name,contract="independent complete expression",
                expected=expected,actual=actual,exception_message=message,
                passed=type(actual) is float and math.isclose(actual,expected,rel_tol=4e-15)))
    finally:
        subject.accumulation=original
    print(json.dumps(dict(reference="Decimal log-amplitude at 1600/2200 digits and signed-zero identities",
        tolerance="4e-15 relative, no absolute floor; exact zero signs and error types",
        observations=rows),indent=2,allow_nan=False))
    assert all(r["passed"] for r in rows), str(sum(not r["passed"] for r in rows))+" mismatches"

if __name__=="__main__":
    run()
