"""Section 18.1 binary64 range checks against exact rational references."""
from fractions import Fraction as F
import json
import math
import sys
import section_18_01 as lab


def rounded(q):
    try:
        x = float(q)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if q and not x else x


def check():
    tiny, largest = math.ulp(0.0), sys.float_info.max
    rows = []

    def compare(label, call, expected):
        try:
            actual = call()
        except (ValueError, OverflowError, ZeroDivisionError, TypeError) as exc:
            actual = type(exc).__name__
        rows.append(dict(case=label, expected=repr(expected), actual=repr(actual),
                         passed=actual == expected))

    for c,r,n in [(largest,1,1024),(tiny,-.5,1075),(1,1,1075),
                  (largest,-.5,1),(tiny,1,1),(0,-.5,5000),
                  (1,.5,0),(1000,.05,2),(1,2**-54,4),
                  (largest,1,2098),(largest,1,2099)]:
        ref = F(c)/(1+F(r))**n
        compare(repr((c,r,n)),lambda:lab.present_value(c,r,n),rounded(ref))
    compare('half-period sqrt(4)',lambda:lab.present_value(10,3,.5),5.)
    compare('discount saturation',lambda:lab.present_value(largest,1,1e308),'ValueError')
    compare('discount growth',lambda:lab.present_value(tiny,-.5,1e308),'ValueError')
    compare('zero still validates rate',lambda:lab.present_value(0,-1,0),'ValueError')
    compare('boolean payment',lambda:lab.present_value(True,0,1),'TypeError')

    for y,z in [(largest,-largest),(tiny,largest),(largest,tiny),
                (3,4),(0,largest),(tiny,0),(largest,math.nextafter(largest,0)),
                (0,0),(tiny,2*tiny),(-3,4)]:
        delta=abs(F(z)-F(y))
        a=rounded(delta)
        b=rounded(delta/abs(F(y))) if y else None
        expected='ValueError' if 'ValueError' in (a,b) else dict(absolute=a,relative=b)
        compare(repr(('errors',y,z)),lambda:lab.errors(y,z),expected)
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
