"""Known values, fixed-input comparisons, identifiability, and interface checks."""
from fractions import Fraction
from math import isclose
import json
from section_1_03 import annual_value,rate_scenarios,BASIS_POINTS_PER_UNIT

names=[]
def check(name,condition):
    assert condition,name
    names.append(name)
def close(a,b):
    return isclose(a,b,rel_tol=1e-12,abs_tol=1e-10)

assumptions={'principal':1000.,'years':2}
snapshot=assumptions.copy()
rates=[0.,.03,.05]
rows=rate_scenarios(**assumptions,rates=rates)
check('known rate table',len(rows)==3 and all(close(v,e) for (_,v),e in zip(rows,[1000,1060.9,1102.5])))
check('fixed assumptions preserved',assumptions==snapshot)
check('input rate list preserved',rates==[0,.03,.05])
check('rate labels aligned',tuple(r for r,v in rows)==tuple(rates))
check('empty scenarios',rate_scenarios(principal=1000,years=2,rates=[])==())
# Empty lists do not trigger row-level parameter validation, as documented.
check('empty-list validation scope',rate_scenarios(principal=-1,years=-1,rates=[])==())
duplicates=rate_scenarios(**assumptions,rates=[.05,0,.05])
check('duplicates and order retained',tuple(r for r,v in duplicates)==(.05,0,.05) and close(duplicates[0][1],duplicates[2][1]))
generated=rate_scenarios(**assumptions,rates=(r for r in [.05,0]))
check('finite iterator accepted',len(generated)==2 and generated[0][0]==.05)
check('negative rate example',close(annual_value(principal=1000,annual_effective_rate=-.02,years=2),960.4))
check('principal exercise',all(close(annual_value(principal=p,annual_effective_rate=.05,years=2),e) for p,e in [(500,551.25),(1000,1102.5),(2000,2205)]))
check('time exercise',all(close(annual_value(principal=1000,annual_effective_rate=.05,years=n),e) for n,e in [(0,1000),(1,1050),(2,1102.5),(3,1157.625)]))
check('basis-point conversion',BASIS_POINTS_PER_UNIT==10000 and 50/BASIS_POINTS_PER_UNIT==.005)
check('one-year implied rate',close(110/100-1,.1))
check('target principal',close(1210/(1.1**2),1000))
check('exercise finite change',close(annual_value(principal=500,annual_effective_rate=.045,years=2)-annual_value(principal=500,annual_effective_rate=.04,years=2),5.2125))
# Exact rational arithmetic supplies an independent benchmark for the finite change.
P,r,h=Fraction(500),Fraction('0.04'),Fraction('0.005')
check('independent exact difference',P*((1+r+h)**2-(1+r)**2)==Fraction('5.2125'))
old=annual_value(principal=1000,annual_effective_rate=.05,years=2)
new=annual_value(principal=2000,annual_effective_rate=.06,years=2)
p_first=annual_value(principal=2000,annual_effective_rate=.05,years=2)
r_first=annual_value(principal=1000,annual_effective_rate=.06,years=2)
check('joint move total',close(new-old,1144.7))
check('principal-first contributions',close(p_first-old,1102.5) and close(new-p_first,42.2))
check('rate-first contributions',close(r_first-old,21.1) and close(new-r_first,1123.6))
check('both paths reconcile',close((p_first-old)+(new-p_first),(r_first-old)+(new-r_first)))
# Independent recurrence, linear scaling, and zero-principal/horizon information.
scenarios=0
for principal in [0.,1.,500.,1000.]:
    for rate in [-.2,0.,.04,.1]:
        for years in [0,1,2,5]:
            value=annual_value(principal=principal,annual_effective_rate=rate,years=years)
            iterative=principal
            for _ in range(years): iterative*=1+rate
            assert close(value,iterative)
            doubled=annual_value(principal=2*principal,annual_effective_rate=rate,years=years)
            assert close(doubled,2*value)
            scenarios+=1
check('zero principal cannot identify rate',all(annual_value(principal=0,annual_effective_rate=r,years=2)==0 for r in [-.2,0,.1]))
check('zero horizon cannot identify rate',all(annual_value(principal=1000,annual_effective_rate=r,years=0)==1000 for r in [-.2,0,.1]))
finite_moves=0
for principal in [100,500,1000]:
    for rate in [-.02,0,.04,.1]:
        for h in [-.01,.005,.01]:
            base=annual_value(principal=principal,annual_effective_rate=rate,years=2)
            moved=annual_value(principal=principal,annual_effective_rate=rate+h,years=2)
            assert close(moved-base,principal*(2*(1+rate)*h+h*h))
            finite_moves+=1
invalid=[({'principal':-1,'annual_effective_rate':.05,'years':2},ValueError),
         ({'principal':100,'annual_effective_rate':-1,'years':2},ValueError),
         ({'principal':100,'annual_effective_rate':.05,'years':-1},ValueError),
         ({'principal':True,'annual_effective_rate':.05,'years':2},TypeError),
         ({'principal':100,'annual_effective_rate':True,'years':2},TypeError),
         ({'principal':100,'annual_effective_rate':.05,'years':True},TypeError),
         ({'principal':100,'annual_effective_rate':.05,'years':1.5},TypeError),
         ({'principal':100,'annual_effective_rate':float('nan'),'years':2},ValueError),
         ({'principal':float('inf'),'annual_effective_rate':.05,'years':2},ValueError),
         ({'principal':100,'annual_effective_rate':'0.05','years':2},TypeError)]
for args,error in invalid:
    try: annual_value(**args)
    except error: pass
    else: raise AssertionError(f'expected {error.__name__} for {args}')
try:
    rate_scenarios(**assumptions,rates=[.05,-1])
except ValueError:
    pass
else:
    raise AssertionError('invalid mixed rate list returned a report')
try:
    annual_value(1000,.05,2)
except TypeError:
    pass
else:
    raise AssertionError('positional arguments accepted')
summary={'reference_checks':len(names),'recurrence_and_scaling_scenarios':scenarios,
         'exact_finite_change_scenarios':finite_moves,'invalid_input_cases':len(invalid)+2}
print('PASS: '+json.dumps(summary,sort_keys=True))
