"""Check the final sum of represented cash-flow terms, independently of PV."""
from fractions import Fraction
from itertools import permutations
import json
import math
import sys
import section_20_06 as lab


def reference(values):
    dyadics=[v.as_integer_ratio() for v in map(float,values)]
    scale=max((d for _,d in dyadics),default=1)
    numerator=sum(n*(scale//d) for n,d in dyadics)
    try:
        return float(Fraction(numerator,scale))
    except OverflowError:
        return 'OverflowError'


def observe(flows,rate,expected,label=None):
    try:
        actual=lab.portfolio(flows,rate)
    except (TypeError,ValueError,OverflowError) as exc:
        actual=type(exc).__name__
    return dict(helper='portfolio',inputs=label or repr((flows,rate)),expected=expected,
                actual=actual,passed=type(actual) is type(expected) and actual==expected)


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    half=math.ulp(m)/2
    values=[*sorted(set(permutations((m,m,-m)))),
            *sorted(set(permutations((-m,-m,m)))),
            (m,m,-m,-m,s),(-m,-m,m,m,-s),(m,m,-m,-m),
            (m,m),(m,half),(m,math.nextafter(half,0)),
            (1,2**-53,s),(1,2**-53,-s),(s,s,-s),(),(0,-0.)]
    rows=[observe([(a,0) for a in v],0,reference(v)) for v in values]
    rows.extend([
        observe(iter([(80,1),(40,2)]),math.log(2),50.,'one-shot iterable at log(2)'),
        observe([(80,1),(20,2),(-60,1)],math.log(2),15.),
        observe([],float('nan'),'ValueError'),
        observe([],True,'TypeError'),
        observe([(1,-1)],0,'ValueError'),
        observe([(True,0)],0,'TypeError'),
        observe([(0,2)],m,'OverflowError'),
        observe([(m,1),(-m,1)],-1,'OverflowError'),
    ])
    calls=[]
    terms=iter((m,m,-m,s))
    old=lab.pv
    def observed(a,r,t):
        calls.append((a,r,t))
        return next(terms)
    lab.pv=observed
    try:
        rows.append(observe(iter([(1,0),(2,1),(3,2),(4,3)]),.125,m,'observed rounded terms'))
    finally:
        lab.pv=old
    expected_calls=[(1,.125,0),(2,.125,1),(3,.125,2),(4,.125,3)]
    rows.append(dict(helper='portfolio.pv calls',inputs='observed rounded terms',
                     expected=expected_calls,actual=calls,passed=calls==expected_calls))
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
