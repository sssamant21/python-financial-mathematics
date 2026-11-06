"""Selected end-period boundary checks against explicitly timed payments."""
from decimal import Context, Decimal as D, localcontext
import json
import math
import sys

from section_19_08 import end_period_contributions as end


def rounded(ref):
    value = float(ref)
    return "result range" if not math.isfinite(value) or (ref and not value) else value


def explicit_sum(args):
    a, r, u, t, n = args
    with localcontext(Context(prec=3400)):
        a, r, u, t = map(D, (a, r, u, t))
        h = t/n
        return rounded(a*(r*t).exp() + sum(
            (u*h*(r*h*j).exp() for j in range(n)), D(0)))


def observe(name, args, expected):
    try:
        actual = end(*args)
    except ValueError as error:
        message = str(error)
        actual = ("evaluation limit" if "supported evaluation range" in message
                  else "result range" if "outside floating-point range" in message
                  else "invalid input")
    return dict(case=name, inputs=[*args[:-1], repr(args[-1])], expected=expected,
                actual=actual, passed=actual == expected)


def main():
    tiny = math.ulp(0.0)
    maxval = sys.float_info.max
    direct = [
        ("negative_one_payment", (1., -4001., 2., 1., 1)),
        ("negative_two_payments", (1., -4001., 2., 1., 2)),
        ("positive_one_payment", (0., 4001., 2., 1., 1)),
        ("positive_one_payment_overflow", (1., 4001., 2., 1., 1)),
        ("positive_two_payments_overflow", (0., 4001., 2., 1., 2)),
        ("negative_midpoint_up", (0., -5000., tiny, 1., 2)),
        ("negative_midpoint_down", (-1., -5000., tiny, .5, 1)),
        ("negative_midpoint_down_single", (-1., -10000., tiny, .5, 1)),
        ("negative_midpoint_up_single", (1., -10000., tiny, .5, 1)),
        ("negative_final_underflow", (0., -5000., tiny, 1., 4)),
        ("old_boundary_decay", (1., -4000., tiny, .5, 1)),
        ("ordinary_signed_flow", (75., .125, -12., 2., 7)),
        ("no_flow_contract", (1., -4001., 0., 1., 1)),
        ("payment_out_of_range", (0., -2500., maxval, 2., 1)),
    ]
    rows = [observe(name, args, explicit_sum(args)) for name, args in direct]
    # For a=1, u=-r, t=1, write the balance as
    # 1 + (1 - z/expm1(z))*(exp(x)-1), z=x/n. For 0<z<1/2,
    # z/4 < 1 - z/expm1(z) < z follows by bounding the exponential series.
    # At x=4001 and 5000, exp(x) lies between 10**1737 and
    # 10**2172, so n=10**2500 rounds to 1 and n=10**1200 overflows.
    rows.append(observe("published_fine_checkpoint", (1., 4001., -4001., 1., 10**2000), 1.))
    for x in (4001., 5000.):
        rows.append(observe(f"equilibrium_fine_{x}", (1., x, -x, 1., 10**2500), 1.))
        rows.append(observe(f"equilibrium_overflow_{x}", (1., x, -x, 1., 10**1200),
                            "result range"))
    rows.extend([
        observe("new_positive_limit", (1., 5001., -5001., 1., 10**2500), "evaluation limit"),
        observe("new_negative_limit", (1., -5001., 2., 1., 2), "evaluation limit"),
        observe("zero_state_bypasses_limit", (0., maxval, 0., maxval, 2), 0.),
        observe("boolean_period_rejected", (1., .25, 2., 1., True), "invalid input"),
    ])
    print(json.dumps(rows, indent=2, allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__ == "__main__":
    main()
