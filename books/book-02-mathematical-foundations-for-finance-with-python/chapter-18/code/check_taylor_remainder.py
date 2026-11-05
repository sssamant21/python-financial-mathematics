"""Compare the observed approximation report to analytic remainder bounds."""
from decimal import Decimal as D, localcontext
import json
import math
import section_18_01 as lab


def check():
    rows = []
    with localcontext() as ctx:
        ctx.prec = 120
        for x in (0.0, .1, -.1, .5, -.5, .01, -.01, 2**-20, -2**-20,
                  2**-40, -2**-40):
            dx = D(x)
            leading = dx*dx/2
            # For positive x, consecutive tail terms after x²/2 have
            # ratio <= x/3. For negative x use the alternating-series bound.
            lo = leading if dx >= 0 else leading-abs(dx)**3/6
            hi = leading/(1-dx/3) if dx >= 0 else leading
            reference = dx.exp()-1-dx
            assert lo <= reference <= hi
            result = lab.exponential_approximation(x)
            exact, linear = result['exact'], result['first_order']
            assert abs(D(exact)-dx.exp()) <= D(math.ulp(exact))
            assert linear == float(1+dx)
            # This field compares the rounded operands; the exact remainder
            # has a separate reference, including when rounding hides it.
            observed = result['error']['absolute']
            assert observed == abs(exact-linear)
            allowance = D(math.ulp(exact))+D(math.ulp(linear))+D(math.ulp(observed))
            assert abs(D(observed)-reference) <= allowance
            assert abs(D(result['error']['relative'])-reference/dx.exp()) <= 4*allowance
            if abs(x) >= .01:
                assert lo <= D(observed)+allowance and D(observed)-allowance <= hi
            rows.append({'x':x,'leading':str(leading),'lower':str(lo),'upper':str(hi),
                         'reference':str(reference),'reported':observed})
        hidden = [row for row in rows if row['x'] and row['reported']==0]
        assert len(hidden)==2
    print(json.dumps({'cases':rows,'rounding_hidden_remainders':len(hidden)},indent=2))


if __name__ == '__main__':
    check()
