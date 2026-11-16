"""Independent textbook capstone references;shared integration distinguished."""
from fractions import Fraction as F
from datetime import datetime,timezone
from pathlib import Path
import sys,math,json
import financial_toolkit as m
assert Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
rows=[]
def check(case,actual,expected,tol,units,kind='independent numerical'):
 ok=actual==expected if isinstance(expected,(str,bool,tuple)) else math.isclose(actual,float(expected),rel_tol=0.,abs_tol=tol)
 rows.append(dict(case=case,actual=repr(actual),expected=repr(expected),absolute_tolerance=tol,relative_tolerance=0.,units=units,kind=kind,passed=ok))
check('FV100at10pct2periods',m.future_value(100.,.1,2),F(100)*(1+F(1,10))**2,1e-10,'amount')
check('PV110at10pct1period',m.present_value(110.,.1,1),F(110)/(1+F(1,10)),1e-10,'amount')
check('time-zero NPV',m.net_present_value([-100.,110.],.1),-F(100)+F(110)/(1+F(1,10)),1e-10,'amount')
check('one payment annuity',m.level_payment(1000.,.1,1),F(1000)/(1/(1+F(1,10))),1e-9,'amount per period')
check('bond direct two-payment discount sum',m.fixed_coupon_bond_price(100.,.05,.05,2),F(5)/(1+F(1,20))+F(105)/(1+F(1,20))**2,1e-10,'amount')
check('linked exact factor product',m.linked_return([.1,-.1]),(1+F(1,10))*(1-F(1,10))-1,1e-12,'return fraction')
check('portfolio rational weighting',m.portfolio_return([.6,.4],[.1,-.05]),F(3,5)*F(1,10)+F(2,5)*F(-1,20),1e-12,'return fraction')
a=m.summarize_sample([1.,2.,3.]);values=[F(1),F(2),F(3)];mean=sum(values)/3;var=sum((values[i]-values[j])**2 for i in range(3) for j in range(i+1,3))/(3*2)
check('sample independent mean',a.mean,mean,0.,'sample units');check('sample pairwise-gap variance',a.sample_variance,var,0.,'sample units squared')
run=m.simulate_two_outcome(100.,.1,0.,0.,3,42);check('probability-zero endpoint',run.terminal_values,(100.,100.,100.),0.,'amount tuple','deterministic boundary,not RNG distribution')
u=timezone.utc;t1=datetime(2025,1,2,16,tzinfo=u);t2=datetime(2025,1,3,16,tzinfo=u);cut=datetime(2025,1,3,18,tzinfo=u)
def rec(p,t):return dict(instrument='X',currency='USD',price=p,observed_at=t,available_at=t,source='synthetic')
a=m.validated_price_return(rec(100.,t1),rec(110.,t2),cut);check('validated independent ratio',a,(F(110)-100)/100,1e-12,'return fraction');check('shared lower-return integration',a==m.simple_price_return(100.,110.),True,0.,'boolean','shared implementation,not independent oracle')
for label,fn in [('invalid discount rate',lambda:m.present_value(100.,-1.,1)),('invalid weight sum',lambda:m.portfolio_return([.4,.4],[.1,.2]))]:
 try:fn();actual='returned'
 except Exception as e:actual=type(e).__name__
 check(label,actual,'ValueError',0.,'exception category','invalid contract')
d=dict(predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Independent exact textbook rational benchmarks and two invalid contracts;shared return comparison separate. No complete mathematical/data/model/platform/release/independent reviewer approval.')
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
