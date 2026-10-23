"""Endpoint, set, product-domain, and coupled-feasibility checks."""
from fractions import Fraction
from math import inf,nextafter
import json
from section_1_04 import (finite_float,interval_contains,discount_rate_member,
                         growth_domain_member,long_only_pair_member)

names=[]
def check(name,condition):
    assert condition,name
    names.append(name)

A,B,U={'USD','EUR'},{'EUR','JPY'},{'USD','EUR','JPY'}
check('intersection',A&B=={'EUR'})
check('union',A|B==U)
check('difference',A-B=={'USD'})
check('relative complement',U-A=={'JPY'})
check('repetition does not change set',{1,2,2}=={2,1})
check('closed endpoints',interval_contains(0,0,1) and interval_contains(1,0,1))
check('open endpoints',not interval_contains(0,0,1,left_closed=False) and not interval_contains(1,0,1,right_closed=False))
check('closed singleton',interval_contains(1,1,1))
check('half-open singleton empty',not interval_contains(1,1,1,left_closed=False) and not interval_contains(1,1,1,right_closed=False))
check('excluded rate boundary',not discount_rate_member(-1))
check('adjacent rate inside',discount_rate_member(nextafter(-1,inf)))
check('adjacent rate outside',not discount_rate_member(nextafter(-1,-inf)))
check('negative rate inside',discount_rate_member(-.05))
check('adjacent weight outside',not interval_contains(nextafter(0,-inf),0,1))
check('adjacent weight inside',interval_contains(nextafter(0,inf),0,1))
check('adjacent upper outside',not interval_contains(nextafter(1,inf),0,1))
check('valid pair endpoints',long_only_pair_member(0,1) and long_only_pair_member(1,0))
check('bounds not enough',not long_only_pair_member(.8,.8))
check('sum not enough',not long_only_pair_member(1.1,-.1))
check('strict component bounds despite tolerance',not long_only_pair_member(-1e-15,1))
check('approximate budget accepted',long_only_pair_member(.5,.5000000000005))
check('zero-tolerance budget rejects discrepancy',not long_only_pair_member(.5,.5000000000005,budget_tol=0))
check('valid negative rate growth triple',growth_domain_member(1000,-.05,2))
check('zero principal still validates rate',not growth_domain_member(0,-1,2))
check('complete-loss simple return', (0-100)/100==-1 and not discount_rate_member(-1))
check('nonfinite observations excluded',all(finite_float(x) is None for x in [float('nan'),inf,-inf]))
check('unsupported observation types excluded',all(finite_float(x) is None for x in [True,False,None,'0.5',complex(1),Fraction(1,2)]))
check('huge integer conversion excluded',finite_float(10**1000) is None)
check('documented float conversion limitation',interval_contains(2**53+1,2**53,2**53))
# Independent exact rational membership for four endpoint conventions.
interval_cases=0
for left_closed in [False,True]:
    for right_closed in [False,True]:
        for x in [-.1,0.,.25,.5,.75,1.,1.1]:
            exact=Fraction(x)
            expected=(0<exact<1 or exact==0 and left_closed or exact==1 and right_closed)
            assert interval_contains(x,0,1,left_closed=left_closed,right_closed=right_closed)==expected
            interval_cases+=1
        for x in [.5,1.,1.5]:
            expected=x==1 and left_closed and right_closed
            assert interval_contains(x,1,1,left_closed=left_closed,right_closed=right_closed)==expected
            interval_cases+=1
# Product domain evaluated against explicitly listed admitted coordinate values.
growth_cases=0
for principal in [-1,0,1000]:
    for rate in [-1,-.1,0,.05]:
        for periods in [-1,0,2,2.0,True]:
            expected=(principal in [0,1000] and rate in [-.1,0,.05]
                      and type(periods) is int and periods in [0,2])
            assert growth_domain_member(principal,rate,periods)==expected
            growth_cases+=1
# Exact tenth-weight grid provides an independent finite feasibility benchmark.
pair_cases=0
for i in range(-2,13):
    for j in range(-2,13):
        expected=(0<=i<=10 and 0<=j<=10 and Fraction(i,10)+Fraction(j,10)==1)
        assert long_only_pair_member(i/10,j/10)==expected,(i,j)
        pair_cases+=1
invalid_config=[(lambda:interval_contains(.5,1,0),ValueError),
 (lambda:interval_contains(.5,-inf,1),ValueError),
 (lambda:interval_contains(.5,0,inf),ValueError),
 (lambda:interval_contains(.5,float('nan'),1),ValueError),
 (lambda:interval_contains(.5,False,1),ValueError),
 (lambda:interval_contains(.5,0,1,left_closed=1),TypeError),
 (lambda:interval_contains(.5,0,1,right_closed='yes'),TypeError),
 (lambda:long_only_pair_member(.5,.5,budget_tol=-1),ValueError),
 (lambda:long_only_pair_member(.5,.5,budget_tol=float('nan')),ValueError),
 (lambda:long_only_pair_member(.5,.5,budget_tol=inf),ValueError),
 (lambda:long_only_pair_member(.5,.5,budget_tol=True),ValueError)]
for operation,error in invalid_config:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
# Worked examples with exact rationals instead of binary comparison thresholds.
check('policy intersection lower exclusion',not (-1>-1) and -.5>-1 and -.5<=.15)
check('singleton practice',{x for x in [1,2,3] if x>=2 and x<=2}=={2})
check('empty practice',{x for x in [0,1,2,3] if x>=2 and x<=1}==set())
summary={'reference_checks':len(names),'interval_cases':interval_cases,
         'growth_domain_cases':growth_cases,'coupled_weight_cases':pair_cases,
         'invalid_configuration_cases':len(invalid_config)}
print('PASS: '+json.dumps(summary,sort_keys=True))
