"""Independent finite cash-flow sums and half-period identity for Section 18.2."""
from decimal import Decimal as D, localcontext
import json
import math
import section_18_02 as lab


def check():
    tiny = math.ulp(0.0)
    cases = [
        (100, .05, 12), (100, -.05, 12), (100, 0, 12),
        (1e-300, 1e-100, 12), (1e-300, -1e-100, 12),
        (1e308, 1e-100, tiny), (1e308, -1e-100, tiny),
        (1e-300, -.5, 2000), (1e308, -.5, .5),
        (1e308, .05, 2), (1e308, 0, 2), (tiny, 1, 1),
        (tiny, 1, .5), (tiny, 0, .5),
        (0, -.5, 2000), (1e308, -.5, 0),
        (100, -tiny, .5), (100, tiny, .5),
        (1e308, 1e308, 1), (1e308, 1e308, 2),
        (1, -.5, 1e308), (1, 1, 1e308),
    ]
    rows = []
    with localcontext() as ctx:
        ctx.prec = 1200
        for c,r,n in cases:
            dc, dr, dn = D(c), D(r), D(n)
            if not c or not n or not r:
                reference = dc*dn
            elif n == .5:
                root = (1+dr).sqrt()
                reference = dc/(root*(root+1))
            elif n == tiny:
                # Correction to n*log1p(r)/r is < 10^-400 in these fixtures.
                reference = dc*dn*(1+dr).ln()/dr
            elif n > 2000:
                # At rate +1 the finite geometric sum differs from 1 by 2^-n;
                # at rate -1/2 even the 2000th payment alone exceeds float range.
                reference = D(1) if r > 0 else D(2)**2000
            else:
                step = 1/(1+dr)
                term = dc
                reference = D(0)
                for _ in range(n):
                    term *= step
                    reference += term
            expected = float(reference)
            try:
                actual = lab.annuity_present_value(c,r,n)
            except (ValueError, OverflowError) as exc:
                actual = type(exc).__name__
            if not math.isfinite(expected) or (reference and expected==0):
                ok = actual == 'ValueError'
            else:
                ok = (isinstance(actual,float) and math.isfinite(actual)
                      and (actual==0)==(expected==0)
                      and abs(D(actual)-D(expected))<=2*D(math.ulp(expected)))
            rows.append({'payment':c,'rate':r,'periods':n,'actual':str(actual),
                         'rounded_reference':str(expected),'pass':ok})
    invalid = []
    for args,error in [((0,-1,2),ValueError),((0,.1,-1),ValueError),
                       ((-1,0,0),ValueError),((True,0,0),TypeError),
                       ((0,float('inf'),0),ValueError)]:
        try:
            lab.annuity_present_value(*args)
            ok = False
        except (TypeError, ValueError) as exc:
            ok = type(exc) is error
        invalid.append(ok)
    print(json.dumps({'cases':rows,'invalid_inputs':invalid},indent=2,allow_nan=False))
    assert all(row['pass'] for row in rows) and all(invalid)


if __name__ == '__main__':
    check()
