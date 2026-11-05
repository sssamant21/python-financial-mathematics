"""Independent power and half-period boundary checks for Section 18.2."""
import json
import math
import sys
from fractions import Fraction as F

import section_18_02 as lab


def rounded(q):
    try:
        x = float(q)
    except OverflowError:
        return "ValueError"
    return "ValueError" if q and not x else x


def check():
    rows = []
    helpers = (lab.growth_factor, lab.growth_increment, lab.discount_change)

    def compare(fn, r, n, expected):
        try:
            actual = fn(r, n)
        except (ValueError, OverflowError, TypeError) as exc:
            actual = type(exc).__name__
        rows.append(dict(helper=fn.__name__, rate=repr(r), periods=repr(n),
                         expected=repr(expected), actual=repr(actual),
                         passed=actual == expected))

    tiny = math.ulp(0.0)
    for r,n in [(1,1023),(1,1024),(-.5,1074),(-.5,1075),
                (-.5,54),(-.5,55),(1,54),(1,55),(tiny,2),
                (-tiny,2),(sys.float_info.max,1),(0,100),(1,0),
                (2**-54,4),(.125,17),(-.125,17)]:
        p = (1+F(r))**n
        for fn,q in zip(helpers,(p,p-1,1/p-1)):
            compare(fn,r,n,rounded(q))
    # sqrt(1+r)-1 = r/(sqrt(1+r)+1); its magnitude is on
    # opposite sides of tiny/2 for the two signs. The inverse
    # change has the extra factor 1/sqrt(1+r), reinforcing this.
    for r,expected in [(tiny,(1.,'ValueError','ValueError')),
                       (-tiny,(1.,-tiny,tiny)),
                       (3,(2.,1.,-.5)),
                       (-.75,(.5,-.5,1.)),
                       (1,( 'ValueError','ValueError',-1.)),
                       (-.5,('ValueError',-1.,'ValueError'))]:
        n = 1e308 if r in (1,-.5) else .5
        for fn,x in zip(helpers,expected):
            compare(fn,r,n,x)
    for fn in helpers:
        compare(fn,-1,0,'ValueError')
        compare(fn,0,-1,'ValueError')
        compare(fn,True,1,'TypeError')
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
