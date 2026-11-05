"""Exact reciprocal-state oracle for quadratic growth and its singularity."""
from fractions import Fraction as F
import json
import math
import sys
import section_19_02 as lab


def check():
    tiny=math.ulp(0.0);big=sys.float_info.max
    cases=[(100,.001,0),(100,.001,5),(100,.001,10),
           (big,big,0),(tiny,tiny,big),(1,tiny,big),
           (big,tiny,1),(1e-308,1e308,.5),(1e308,1e-308,.5),
           (1,1,math.nextafter(1,0)),(1,1,1),(1,1,math.nextafter(1,2)),
           (1,big,tiny),(tiny,big,1),(big,big,tiny),
           (2,.125,2),(2,.125,4),(2,.125,5)]
    rows=[]
    for a,k,t in cases:
        inverse=1/F(a)-F(k)*F(t)
        if inverse<=0:
            expected='ValueError'
        else:
            try:
                expected=float(1/inverse)
                if not math.isfinite(expected) or expected==0:
                    expected='ValueError'
            except OverflowError:
                expected='ValueError'
        try:
            actual=lab.quadratic_growth(a,k,t)
        except (ValueError,OverflowError,ZeroDivisionError) as exc:
            actual=type(exc).__name__
        rows.append(dict(initial=repr(a),coefficient=repr(k),years=repr(t),
                         expected=repr(expected),actual=repr(actual),passed=actual==expected))
    for args,error in [((0,1,0),'ValueError'),((1,0,0),'ValueError'),
                       ((1,1,-1),'ValueError'),((True,1,0),'TypeError')]:
        try:
            lab.quadratic_growth(*args)
            actual='accepted'
        except (ValueError,TypeError) as exc:
            actual=type(exc).__name__
        rows.append(dict(invalid=repr(args),expected=error,actual=actual,passed=actual==error))
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
