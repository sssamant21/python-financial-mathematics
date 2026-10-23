"""Exact fee bounds, slack, sign rules, and deviation-band checks."""
from fractions import Fraction as Q
import json
from section_1_07 import rational,maximum_transaction_amount,transaction_report,weight_band_member

names=[]
def check(name,condition):
    assert condition,name
    names.append(name)
policy=dict(fixed_fee=5,fee_rate='0.01',fee_budget=15,amount_cap=800)
check('exact quoted fee rate',rational('0.01')==Q(1,100))
check('cap binds',maximum_transaction_amount(**policy)==800)
r=transaction_report(amount=800,**policy)
check('cap-bound fee and feasibility',r['fee']==13 and r['feasible'])
check('cap-bound slacks',r['slacks']=={'fee_budget':Q(2),'amount_cap':Q(0)})
r=transaction_report(amount=900,**policy)
check('infeasible proposal despite fee pass',r['checks']=={'fee_budget':True,'amount_cap':False} and not r['feasible'])
check('violating-cap slack',r['slacks']['amount_cap']==-100)
loose=policy|{'amount_cap':2000}
check('fee binds with loose cap',maximum_transaction_amount(**loose)==1000)
check('fee boundary included',transaction_report(amount=1000,**loose)['feasible'])
check('no rounding of fee violation',not transaction_report(amount='1000.01',**loose)['feasible'])
check('fixed fee exceeds budget',maximum_transaction_amount(**(policy|{'fixed_fee':16})) is None)
check('zero rate affordable',maximum_transaction_amount(**(policy|{'fee_rate':0}))==800)
check('zero rate equal budget',maximum_transaction_amount(**(policy|{'fee_rate':0,'fixed_fee':15}))==800)
check('zero rate infeasible',maximum_transaction_amount(**(policy|{'fee_rate':0,'fixed_fee':16})) is None)
check('only zero feasible',maximum_transaction_amount(**(policy|{'fixed_fee':15}))==0)
check('zero maximum distinct from None',maximum_transaction_amount(**(policy|{'amount_cap':0}))==0)
check('zero proposal at exhausted budget',transaction_report(amount=0,**(policy|{'fixed_fee':15}))['feasible'])
check('positive proposal at exhausted budget',not transaction_report(amount='0.001',**(policy|{'fixed_fee':15}))['feasible'])
check('band upper included',weight_band_member(weight='0.6',target='0.5',half_width='0.1'))
check('band lower included',weight_band_member(weight='0.4',target='0.5',half_width='0.1'))
check('just outside band',not weight_band_member(weight='0.6001',target='0.5',half_width='0.1'))
check('long-only intersection',not weight_band_member(weight='1.05',target='0.95',half_width='0.1'))
check('long-only upper accepted',weight_band_member(weight=1,target='0.95',half_width='0.1'))
check('zero-width singleton',weight_band_member(weight='0.5',target='0.5',half_width=0))
exercise=dict(fixed_fee=4,fee_rate='0.02',fee_budget=14,amount_cap=400)
check('exercise maximum',maximum_transaction_amount(**exercise)==400)
check('exercise slacks',transaction_report(amount=400,**exercise)['slacks']=={'fee_budget':Q(2),'amount_cap':Q(0)})
check('strict-boundary exclusion',not (5+Q('0.01')*1000<15))
check('band-cap conflict',max(Q(0),Q('0.4'))>min(Q(1),Q('0.6'),Q('0.3')))
# Derivation cross-check: direct inequalities versus independently computed maximum.
policy_cases=0
proposal_cases=0
for F in range(4):
    for k in [Q(0),Q(1,10),Q(1)]:
        for B in range(5):
            for M in [Q(0),Q(2),Q(5)]:
                p=dict(fixed_fee=F,fee_rate=k,fee_budget=B,amount_cap=M)
                maximum=maximum_transaction_amount(**p)
                if F>B:
                    assert maximum is None
                else:
                    assert maximum is not None and 0<=maximum<=M
                    assert F+k*maximum<=B
                    assert not (maximum+Q(1,100)<=M and F+k*(maximum+Q(1,100))<=B)
                for x in [Q(0),Q(1,2),Q(1),Q(2),Q(5),Q(6)]:
                    direct=(F+k*x<=B and x<=M)
                    result=transaction_report(amount=x,**p)
                    assert result['feasible']==direct
                    assert result['slacks']['fee_budget']==B-(F+k*x)
                    assert result['slacks']['amount_cap']==M-x
                    assert direct==(maximum is not None and x<=maximum)
                    proposal_cases+=1
                policy_cases+=1
# Absolute-value policy versus interval intersection with exact rationals.
band_cases=0
for target in [Q(0),Q(1,4),Q(1,2),Q(19,20),Q(1)]:
    for epsilon in [Q(0),Q(1,10),Q(1,4)]:
        lower,upper=max(Q(0),target-epsilon),min(Q(1),target+epsilon)
        for w in [Q(-1,10),Q(0),Q(1,4),Q(2,5),Q(1,2),Q(3,5),Q(17,20),Q(19,20),Q(1),Q(21,20)]:
            assert weight_band_member(weight=w,target=target,half_width=epsilon)==(lower<=w<=upper)
            band_cases+=1
# Test sign-sensitive rearrangements including the zero-coefficient branch.
sign_cases=0
for a in [-3,-1,0,1,3]:
    for b in [-2,0,2]:
        for B in [-1,0,1]:
            for x in [-3,-1,0,1,3]:
                direct=a*x+b<=B
                if a>0: transformed=x<=Q(B-b,a)
                elif a<0: transformed=x>=Q(B-b,a)
                else: transformed=b<=B
                assert direct==transformed
                sign_cases+=1
invalid=[(lambda:rational(True),TypeError),(lambda:rational(.01),TypeError),
 (lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
 (lambda:rational('Infinity'),ValueError),(lambda:rational('1/0'),ValueError),
 (lambda:maximum_transaction_amount(**(policy|{'fixed_fee':-1})),ValueError),
 (lambda:maximum_transaction_amount(**(policy|{'fee_rate':'-0.01'})),ValueError),
 (lambda:maximum_transaction_amount(**(policy|{'fee_budget':-1})),ValueError),
 (lambda:maximum_transaction_amount(**(policy|{'amount_cap':-1})),ValueError),
 (lambda:transaction_report(amount=-1,**policy),ValueError),
 (lambda:transaction_report(amount=True,**policy),TypeError),
 (lambda:weight_band_member(weight='0.5',target='1.1',half_width='.1'),ValueError),
 (lambda:weight_band_member(weight='0.5',target='-.1',half_width='.1'),ValueError),
 (lambda:weight_band_member(weight='0.5',target='.5',half_width='-.1'),ValueError),
 (lambda:weight_band_member(weight=.5,target='.5',half_width='.1'),TypeError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError(f'expected {error.__name__}')
print('PASS: '+json.dumps({'reference_checks':len(names),'policy_cases':policy_cases,
 'proposal_cases':proposal_cases,'band_cases':band_cases,'sign_cases':sign_cases,
 'invalid_input_cases':len(invalid)},sort_keys=True))
