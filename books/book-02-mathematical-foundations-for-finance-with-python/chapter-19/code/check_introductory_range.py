"""Range and assessment checks for the actual Section 19.1 implementation."""
import json
import math
from decimal import Context, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import sys

if len(sys.argv) == 2:  # Replay against the Section 19.1 module in an older checkout.
    sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import section_19_01 as lab


def run():
    rows = []
    def check(name, expected, operation, *, exact=False):
        try:
            actual = operation()
        except Exception as error:
            actual = type(error).__name__
            detail = str(error)
        else:
            detail = None
            if isinstance(actual, float) and not math.isfinite(actual):
                actual = repr(actual)
        if type(expected) is float:
            passed = type(actual) is float and (
                actual == expected and (expected != 0 or
                    math.copysign(1, actual) == math.copysign(1, expected))
                if exact or expected == 0 else math.isclose(actual, expected, rel_tol=2e-13)
            )
        else:
            passed = type(actual) is type(expected) and actual == expected
        rows.append(dict(case=name, expected=expected, actual=actual, passed=passed, exception=detail))

    least = math.ulp(0.0)
    largest = sys.float_info.max
    with localcontext(Context(prec=850)):
        D = Decimal
        check("growth: finite after scaling", float(D(least)*D(800).exp()),
              lambda: lab.growth(least, 800., 1.))
        check("growth: zero at huge exponent", -0.0,
              lambda: lab.growth(-0., largest, largest))
        check("growth: retain a subnormal", float(D(largest)*D(-1450).exp()),
              lambda: lab.growth(largest, -1450., 1.), exact=True)
        check("growth: signed underflow", -0.0, lambda: lab.growth(-1., -1000., 1.))
        check("growth: true overflow", "ValueError", lambda: lab.growth(1., 800., 1.))
        check("account: exact equilibrium", 1., lambda: lab.account(1., 800., -800., 1.))
        check("account: zero-rate cancellation", largest,
              lambda: lab.account(-largest, 0., largest, 2.))
        check("account: zero horizon", -0., lambda: lab.account(-0., largest, largest, 0.))
        check("account: signed underflow", -0., lambda: lab.account(-1., -1000., 0., 1.))
        check("account: true overflow", "ValueError", lambda: lab.account(2., 800., -800., 1.))
        r = Fraction(1e308)
        check("Euler: finite whole step", float(2+r/2),
              lambda: lab.euler_account(2., 1e308, -1e308, .5, 1), exact=True)
        check("Euler: exact width below least float", float(Fraction(largest)*Fraction(least)),
              lambda: lab.euler_account(0., 0., largest, least, 2))
        check("Euler: zero horizon", -0., lambda: lab.euler_account(-0., largest, largest, 0., 2))
        check("Euler: true overflow", "ValueError",
              lambda: lab.euler_account(largest, 1., 0., 1., 1))
        check("Euler: bool is not a step count", "ValueError",
              lambda: lab.euler_account(1., 0., 1., 1., True))
        edge = math.nextafter(-1., 0.)
        check("rate: nearest valid effective", float((1+D(edge)).ln()),
              lambda: lab.continuous_from_effective(edge))
        check("rate: nearest valid effective round trip", edge,
              lambda: lab.effective_from_continuous(lab.continuous_from_effective(edge)), exact=True)
        check("rate: negative but distinguishable", float(D(-37).exp()-1),
              lambda: lab.effective_from_continuous(-37.), exact=True)
        assert float(D(-38).exp()-1) == -1.
        check("rate: rounded excluded endpoint", "ValueError",
              lambda: lab.effective_from_continuous(-38.))
        check("rate: extreme negative endpoint", "ValueError",
              lambda: lab.effective_from_continuous(-1000.))
        check("rate: true overflow", "ValueError", lambda: lab.effective_from_continuous(800.))
        check("rate: least positive continuous", least,
              lambda: lab.effective_from_continuous(least), exact=True)
        check("rate: inverse rejects endpoint", "ValueError", lambda: lab.continuous_from_effective(-1.))
        report = lab.assessment()
        r = D(.05)
        exact_growth = D(1000)*(2*r).exp()
        check("assessment: exact growth", float(exact_growth), lambda: report["growth_2_years"])
        for n in (10,20,40):
            geometric = D(1000)*(1+2*r/n)**n
            check(f"assessment: Euler {n}", float(geometric), lambda: report[f"growth_euler_{n}"])
            # This error is against the unrounded geometric and analytic values.
            # The reported simulation rounds at every step, so allow its accumulated ulps.
            check(f"assessment: error {n}", True,
                  lambda: math.isclose(report[f"growth_euler_absolute_error_{n}"],
                                       float(abs(geometric-exact_growth)), abs_tol=2e-11, rel_tol=0.))
            check(f"assessment: error from displayed balances {n}", True,
                  lambda: report[f"growth_euler_absolute_error_{n}"] ==
                          abs(report[f"growth_euler_{n}"]-report["growth_2_years"]))
        flow_r = D(.04)
        check("assessment: constant flow", float((D(1000)+200/flow_r)*(5*flow_r).exp()-200/flow_r),
              lambda: report["account_with_flow"])
        check("assessment: zero rate", 2000, lambda: int(report["zero_rate_account"])
              if report["zero_rate_account"] == 2000 else None)
        check("assessment: depletion", 10, lambda: report["depletion_years"])
        check("assessment: effective", float(r.exp()-1), lambda: report["annual_effective_equivalent"])
        for flag in ("runtime_certified", "independent_review_completed"):
            check("assessment: "+flag, False, lambda: report[flag])
    print(json.dumps(rows, allow_nan=False))
    return all(row["passed"] for row in rows)


if __name__ == "__main__":
    raise SystemExit(0 if run() else 1)
