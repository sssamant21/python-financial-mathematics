"""Section 19.6 account and assessment checks against independent integration."""
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
import sys

from section_19_06 import assessment, exact_account
from section_19_08 import continuous_contributions


def outcome(fn, *args):
    try:
        return fn(*args)
    except (ValueError, OverflowError, TypeError) as exc:
        return type(exc).__name__


def integrated(a, r, u, t):
    # Integrating-factor form, with separate initial and flow terms.
    # This is used only on selected moderate exponents.
    with localcontext() as ctx:
        ctx.prec = 2600
        a, r, u, t = map(Decimal, (a, r, u, t))
        if not r:
            return float(a+u*t)
        e = (r*t).exp()
        return float(a*e+u*(e-1)/r)


def main():
    m, d = sys.float_info.max, math.ulp(0.)
    rows = []

    def check(case, expected, actual, *, tolerance=0):
        passed = (abs(expected-actual)<=tolerance
                  if isinstance(expected,float) and isinstance(actual,float) and tolerance
                  else repr(expected)==repr(actual))
        rows.append(dict(case=case,expected=expected,actual=actual,passed=passed))

    for name, args, expected in [
        ("equilibrium", (3.,900.,-2700.,1.), 3.),
        ("zero_rate_cancellation", (-m/2,0.,m/2,3.), m),
        ("scaled_initial", (d,735.,0.,1.), integrated(d,735.,0.,1.)),
        ("scaled_flow", (0.,730.,d,1.), integrated(0.,730.,d,1.)),
        ("zero_horizon", (-0.,m,3.,0.), -0.),
        ("zero_account", (0.,m,0.,m), 0.),
        ("equilibrium_exponent_overflow", (1.,m,-m,2.), 1.),
        ("true_zero_rate_overflow", (m,0.,m,1.), "ValueError"),
        ("true_growth_overflow", (1.,m,0.,2.), "ValueError"),
        ("zero_horizon_keeps_subnormal", (d,0.,0.,0.), d),
        ("zero_rate_negative_underflow", (0.,0.,-d,.25), -0.),
        ("strong_decay_negative_zero", (-1.,-m,0.,2.), -0.),
        ("deep_midpoint_up", (d,-2.,d,1900.), d),
        ("deep_midpoint_down", (0.,-2.,d,1900.), 0.),
        ("limit_midpoint_up", (d,-2.,d,1e300), d),
        ("limit_midpoint_down", (0.,-2.,d,1e300), 0.),
        ("negative_limit_midpoint_away", (-d,-2.,-d,1e300), -d),
        ("negative_years", (1.,.1,0.,-1.), "ValueError"),
        ("bool_input", (True,.1,0.,1.), "TypeError"),
    ]:
        check(name, expected, outcome(exact_account,*args))
    check("sister_rejects_nonzero_underflow", "ValueError",
          outcome(continuous_contributions,0.,-2.,d,1e300))
    check("sister_keeps_finite_subnormal", d, outcome(continuous_contributions,d,-2.,d,1900.))

    report = assessment()
    for name,args in [("growth_reference",(1000,.05,0,2)),
                      ("account_reference",(1000,.04,200,5))]:
        reference=integrated(*args)
        check(name,reference,report[name],tolerance=math.ulp(reference))
    ref=integrated(1000,.05,0,2)
    for name,row in [*report["fixed_rk4"].items(),("adaptive",report["adaptive_growth"])]:
        error=float(abs(Fraction(row["final_state"])-Fraction(ref)))
        check("reported_error_"+name,error,row["absolute_error"],tolerance=math.ulp(ref))
    check("assessment_validation_flags",[False,False],
          [report["runtime_certified"],report["independent_review_completed"]])
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    main()
