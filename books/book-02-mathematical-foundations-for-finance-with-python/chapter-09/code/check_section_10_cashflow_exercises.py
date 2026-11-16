"""Exercises 14–16/22: actual Section 9.6 outputs vs rational exponential series.
Run with assertions enabled; optional JSON output path. No certification.
"""
import importlib.util, math, sys, json
from pathlib import Path
from fractions import Fraction as F
if not __debug__:
    raise RuntimeError("exercise checks require assertions enabled")
spec=importlib.util.spec_from_file_location("exercise_sensitivity",Path(__file__).with_name("section_9_06.py"))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
records=[]
def check(name,actual,expected,kind="direct helper",atol=0.):
    target=float(expected)
    ok=math.isclose(actual,target,rel_tol=5e-14,abs_tol=atol)
    records.append(dict(name=name,kind=kind,actual=actual,expected=target,expected_fraction=str(expected),relative_tolerance=5e-14,absolute_tolerance=atol,passed=ok))
    assert ok,name

def exponential(x):
    # Independent 100-term rational Maclaurin sum. Used only |x|<=1/2.
    assert abs(x)<=F(1,2)
    term=total=F(1)
    for k in range(1,101):
        term=term*x/k;total+=term
    # Lagrange tail <= exp(1/2)*(1/2)^101/101! < 2*(1/2)^101/101!.
    return total

def reference(flows,rates,bumps=None):
    amounts=[F(float(c))*exponential(-F(float(t))*F(float(z))) for (c,t),z in zip(flows,rates)]
    v=sum(amounts,F(0));first=-sum((F(float(t))*a for (_,t),a in zip(flows,amounts)),F(0));second=sum((F(float(t))**2*a for (_,t),a in zip(flows,amounts)),F(0))
    ref=dict(value=v,first=first,second=second,duration=-first/v,convexity=second/v,cash_flow_derivatives=[exponential(-F(float(t))*F(float(z))) for (_,t),z in zip(flows,rates)],value_weights=[a/v for a in amounts])
    if bumps is not None:
        # Complete exponent uses exact represented z+h, not a rounded float sum.
        endpoint=sum((F(float(c))*exponential(-F(float(t))*(F(float(z))+F(float(h)))) for (c,t),z,h in zip(flows,rates,bumps)),F(0))
        linear=-sum((F(float(t))*a*F(float(h)) for (_,t),a,h in zip(flows,amounts,bumps)),F(0))
        ref.update(exact_change=endpoint-v,linear_change=linear,linear_error=endpoint-v-linear)
    return ref

for label,flows,rate in [("E14",[(100,1),(1100,2)],.04),("equal times",[(25,2),(75,2)],.04),("time zero",[(100,0),(1100,0)],.04),("single",[(10000,5)],.04)]:
    ref=reference(flows,[rate]*len(flows));actual=m.portfolio_sensitivity(flows,rate)
    assert set(actual)==set(ref)
    for key,value in ref.items():
        if isinstance(value,list):
            assert len(actual[key])==len(value)
            for i,x in enumerate(value):check(f"{label} {key}[{i}]",actual[key][i],x)
        else:check(f"{label} {key}",actual[key],value)
    # This is a caller-side comparison of returned fields, not a helper theorem prover.
    variance=sum((w*(F(float(t))-ref['duration'])**2 for (_,t),w in zip(flows,ref['value_weights'])),F(0))
    check(f"{label} E15 weighted variance",actual['convexity']-actual['duration']**2,variance,"caller composition",1e-14)
    check(f"{label} E16 weight sum",sum(actual['value_weights']),F(1),"caller composition")

flows=[(100,1),(1100,2)];rates=[.035,.04]
ref=reference(flows,rates);a=m.spot_curve_sensitivity(flows,rates)
assert set(a)=={'value','spot_derivatives','parallel_first'}
check('E22 spot value',a['value'],ref['value'])
expected_derivatives=[-F(t)*F(c)*exponential(-F(t)*F(z)) for (c,t),z in zip(flows,rates)]
for i,d in enumerate(expected_derivatives):check(f'E22 spot derivative[{i}]',a['spot_derivatives'][i],d)
check('E22 aggregate first',a['parallel_first'],sum(expected_derivatives,F(0)))
for label,bumps in [('mixed',[.001,-.002]),('zero',[0.,0.]),('parallel',[.001,.001])]:
    ref=reference(flows,rates,bumps);a=m.spot_shock(flows,rates,bumps)
    assert set(a)=={'exact_change','linear_change','linear_error'}
    for key in a:check(f'E22 {label} {key}',a[key],ref[key],atol=1e-14)
# Direct cash-amount perturbation; exact linearity in C is tested separately from derivative formula.
base=m.portfolio_sensitivity(flows,.04)
for i in range(2):
    altered=list(flows);altered[i]=(altered[i][0]+1,altered[i][1])
    delta=m.portfolio_sensitivity(altered,.04)['value']-base['value']
    check(f'E16 one-unit payment {i}',delta,reference(flows,[.04,.04])['cash_flow_derivatives'][i],"caller composition",3e-13)
# Rejections delimit these exercises' positive-fixed-flow model; no signed-flow theorem claim.
for name,fn,exc in [('negative payment',lambda:m.portfolio_sensitivity([(-1,1)],.04),ValueError),('zero payment',lambda:m.portfolio_sensitivity([(0,1)],.04),ValueError),('spot length',lambda:m.spot_shock(flows,rates,[.001]),ValueError),('bool cash',lambda:m.portfolio_sensitivity([(True,1)],.04),TypeError)]:
    try:fn()
    except exc:records.append(dict(name=name,kind='direct rejection',passed=True,exception=exc.__name__))
    else:raise AssertionError(name)
# Supplemental negative controls demonstrate that weighting/sign/market-factor substitutions are distinguishable.
for name,bad,good in [('unweighted duration',1.5,base['duration']),('derivative sign',-base['cash_flow_derivatives'][0],base['cash_flow_derivatives'][0]),('replace nonparallel with average bump',base['first']*(-.0005),float(reference(flows,rates,[.001,-.002])['linear_change']))]:
    ok=not math.isclose(bad,good,rel_tol=5e-14,abs_tol=1e-12);assert ok
    records.append(dict(name=name,kind='supplemental wrong-formula control',wrong=bad,reference=good,passed=ok))
result=dict(records=records,passed=sum(x['passed'] for x in records),failed=sum(not x['passed'] for x in records),oracle='100-term exact rational exponential series; |exponent|<=1/2; tail <2*(1/2)^101/101!',limits='Selected direct helper outputs, caller compositions and supplemental controls kept distinct. E15 proof reviewed separately. No market key-rate, signed-flow, model, resource, platform or independent acceptance.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print('PASS',result['passed'],'exercise predicates')
