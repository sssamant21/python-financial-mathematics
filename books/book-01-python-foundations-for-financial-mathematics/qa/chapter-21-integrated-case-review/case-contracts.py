"""Actual installed-toolkit case,independent references and controlled boundaries."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,Context,localcontext
from datetime import timedelta
import json,sys,math,hashlib,importlib.util
import financial_toolkit as toolkit
assert Path(toolkit.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
p=Path(sys.argv[1]);spec=importlib.util.spec_from_file_location('case_probe',p);case=importlib.util.module_from_spec(spec);spec.loader.exec_module(case);rows=[]
def add(name,actual,want,tol=0.,kind='contract'):
 ok=actual==want if isinstance(want,(str,bool,tuple,list)) else math.isclose(actual,float(want),rel_tol=0.,abs_tol=tol)
 rows.append(dict(case=name,actual=repr(actual),expected=repr(want),absolute_tolerance=tol,relative_tolerance=0.,kind=kind,passed=ok))
a=case.build_case();ra=F(110,100)-1;rb=F(95,100)-1;mean=(ra+rb)/2;var=(ra-rb)**2/2
with localcontext(Context(prec=100)):sd=float((Decimal(var.numerator)/Decimal(var.denominator)).sqrt())
for k,w in [('asset_a_return',ra),('asset_b_return',rb),('portfolio_return',F(3,5)*ra+F(2,5)*rb),('cross_section_mean',mean),('cross_section_variance',var),('cross_section_stddev',sd),('present_value',F(110)/(1+F(1,10))),('cashflow_npv',-100+F(110)/(1+F(1,10))),('loan_payment',F(1000)/(1/(1+F(1,10)))),('bond_price',F(5)/(1+F(1,20))+F(105)/(1+F(1,20))**2)]:add(k,a[k],w,1e-9 if k=='loan_payment' else 1e-12 if 'return'in k or k.startswith('cross_') else 1e-10,'independent rational/Decimal benchmark')
add('schema',sorted(a),sorted(['asset_a_return','asset_b_return','portfolio_return','cross_section_mean','cross_section_variance','cross_section_stddev','present_value','cashflow_npv','loan_payment','bond_price','simulation_mean','simulation_values','simulation_seed','simulation_count']));add('simulation count',a['simulation_count'],20);add('simulation seed',a['simulation_seed'],42);values=a['simulation_values'];add('simulation tuple/count',type(values)is tuple and len(values)==20,True);add('native outcome support',all(any(math.isclose(x,w,rel_tol=0.,abs_tol=1e-10) for w in (90.,110.))for x in values),True)
up=sum(math.isclose(x,110.,rel_tol=0.,abs_tol=1e-10) for x in values);down=len(values)-up;empirical=sum(map(F,values))/len(values);add('count-derived native mean',a['simulation_mean'],empirical,1e-10,'observed-sample reference,not model expectation');add('same environment replay',case.build_case()['simulation_values'],values)
# Trace actual pair,weight and sample contracts without changing their values.
trace=[];v0=case.validated_price_return;p0=case.portfolio_return;s0=case.summarize_sample
try:
 def validated(x,y,cut):trace.append(('pair',x['instrument'],y['instrument'],x['currency'],y['currency'],x['price'],y['price'],x['observed_at'].isoformat(),y['observed_at'].isoformat(),cut.isoformat(),x['available_at'].isoformat(),y['available_at'].isoformat(),x['source'],y['source']));return v0(x,y,cut)
 def portfolio(w,r):trace.append(('weights',list(w),list(r)));return p0(w,r)
 def summary(v):trace.append(('sample size',len(v)));return s0(v)
 case.validated_price_return=validated;case.portfolio_return=portfolio;case.summarize_sample=summary;b=case.build_case()
 add('validated pair identities',[x[1:3] for x in trace if x[0]=='pair'],[('A','A'),('B','B')]);add('pair currencies',[x[3:5] for x in trace if x[0]=='pair'],[('USD','USD'),('USD','USD')]);add('case prices',[x[5:7] for x in trace if x[0]=='pair'],[(100.,110.),(100.,95.)]);add('time/cutoff',[x[7:10] for x in trace if x[0]=='pair'],[('2025-01-02T16:00:00+00:00','2025-01-03T16:00:00+00:00','2025-01-03T18:00:00+00:00')]*2);add('weights/order',next(x[1] for x in trace if x[0]=='weights'),[.6,.4]);add('returns/order',next(x[2] for x in trace if x[0]=='weights'),[b['asset_a_return'],b['asset_b_return']]);add('distinct descriptive samples',[x[1] for x in trace if x[0]=='sample size'],[2,20])
 add('availability timeline',[x[10:12] for x in trace if x[0]=='pair'],[('2025-01-02T16:00:00+00:00','2025-01-03T16:00:00+00:00')]*2);add('source labels',[x[12:14] for x in trace if x[0]=='pair'],[('synthetic','synthetic')]*2)
finally:case.validated_price_return=v0;case.portfolio_return=p0;case.summarize_sample=s0
# Controlled unavailable data must stop before the portfolio boundary.
calls=[]
try:
 def unavailable(x,y,cut):y=dict(y);y['available_at']=cut+timedelta(seconds=1);return v0(x,y,cut)
 def watched(w,r):calls.append('portfolio');return p0(w,r)
 case.validated_price_return=unavailable;case.portfolio_return=watched
 try:case.build_case();kind='returned'
 except Exception as e:kind=type(e).__name__
 add('controlled future availability',kind,'ValueError',kind='controlled boundary,not source defect');add('rejection before portfolio',calls,[])
finally:case.validated_price_return=v0;case.portfolio_return=p0
# The fixed order supplies alignment;it doesnot enforce arbitrary caller mapping.
try:
 case.portfolio_return=lambda w,r:p0(w,list(reversed(r)));wrong=case.build_case()['portfolio_return'];add('controlled misalignment differs',not math.isclose(wrong,a['portfolio_return'],rel_tol=0.,abs_tol=1e-12),True,kind='controlled variant,not source defect')
finally:case.portfolio_return=p0
import financial_toolkit.simulation as sm
factory=sm.random.Random
try:
 class Fixed:
  def __init__(self,seed):self.draws=iter([.25,.75]*10)
  def random(self):return next(self.draws)
 sm.random.Random=Fixed;c=case.build_case();add('controlled simulation support',all(math.isclose(x,110. if i%2==0 else 90.,rel_tol=0.,abs_tol=1e-10)for i,x in enumerate(c['simulation_values'])),True,kind='controlled RNG branch,not distribution approval');add('controlled sample mean',c['simulation_mean'],F(100),1e-10,'controlled sample reference,not native balance requirement')
finally:sm.random.Random=factory
add('restored native behavior',case.build_case()['simulation_values'],values)
d=dict(predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),native_simulation=dict(up=up,down=down,actual_mean=a['simulation_mean'],count_reference=float(empirical),nominal_model_mean=100.,seed=42,scenarios=20),actual_case=a,trace=trace,case_file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),toolkit_file=toolkit.__file__,prefix=sys.prefix,source_path_injection=False,limits='Exact-source external case consumes installed toolkit;example isnot a wheel member. Controlled wrappers/RNG restored;not realdata provenance,vintage,basis,model/forecast/RNG/platform/release/independent approval. BroadF32 remainsopen.')
Path(sys.argv[2]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
