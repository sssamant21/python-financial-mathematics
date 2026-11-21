"""Installed schema/time boundary versus explicit hypothetical caller model parameters."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone,timedelta
import financial_toolkit.validation as validation
import financial_toolkit.simulation as simulation
import financial_toolkit.statistics as statistics
import json,sys,math,hashlib,platform
rows=[];models=[];observations=[]
def ck(name,actual,want):
 ok=actual==want if isinstance(want,(bool,str)) else math.isclose(float(actual),float(want),rel_tol=5e-13,abs_tol=0)
 rows.append(dict(name=name,actual=actual,expected=str(want),passed=ok))
for m in [validation,simulation,statistics]:assert Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
t0=datetime(2026,1,1,tzinfo=timezone.utc);t1=t0+timedelta(days=1);cutoff=t1+timedelta(days=1)
def record(price,when,source):return dict(instrument='XYZ',currency='USD',price=price,observed_at=when,available_at=when,source=source)
first=record(100.,t0,'source-A');second=record(125.,t1,'source-B')
original_first=first.copy();original_second=second.copy()
ret=validation.validated_price_return(first,second,cutoff);ck('eligible price return',ret,F(1,4))
obs=validation.validate_price_record(second,cutoff);ck('source label preserved',obs.source,'source-B');ck('instrument preserved',obs.instrument,'XYZ');ck('currency preserved',obs.currency,'USD');ck('caller dictionaries unchanged',first==original_first and second==original_second,True)
# Different source labels are explicitly permitted; neither label is authenticated.
second_same=record(125.,t1,'source-A');ck('same price different source remains eligible',validation.validated_price_return(first,second_same,cutoff),ret)
for label,changes in [('future availability',dict(available_at=cutoff+timedelta(seconds=1))),('currency mismatch',dict(currency='EUR')),('instrument mismatch',dict(instrument='OTHER'))]:
 altered=second.copy();altered.update(changes)
 try:validation.validated_price_return(first,altered,cutoff);actual='returned'
 except Exception as e:actual=type(e).__name__
 ck(label+' rejected',actual,'ValueError')
for probability in [.25,.75]:
 # Explicit caller choice: no calibration or one-day-to-one-year transformation.
 result=simulation.simulate_two_outcome(100.,.25,-.25,probability,4,42)
 summary=statistics.summarize_sample(result.terminal_values);up=sum(x==125. for x in result.terminal_values);mean=F(75)+F(50*up,4);variance=(F(up)*(125-mean)**2+F(4-up)*(75-mean)**2)/3
 ck('p'+str(probability)+' source observation unchanged',validation.validated_price_return(first,second,cutoff),ret)
 ck('p'+str(probability)+' native probability retained',result.up_probability,probability)
 ck('p'+str(probability)+' empirical mean',summary.mean,mean)
 ck('p'+str(probability)+' empirical variance',summary.sample_variance,variance)
 ck('p'+str(probability)+' empirical SD',summary.sample_stddev,math.sqrt(float(variance)))
 ck('p'+str(probability)+' support',all(x in (75.,125.) for x in result.terminal_values),True)
 model_mean=F(100)*(1+F(probability)*F(1,4)+(1-F(probability))*F(-1,4))
 models.append(dict(probability=probability,caller_model_mean=str(model_mean),native_values=result.terminal_values,native_summary=dict(count=summary.count,mean=summary.mean,variance=summary.sample_variance,SD=summary.sample_stddev),provenance=dict(instrument='XYZ',currency='USD',price_observation_days=1,source_labels=['source-A','source-B'],decision_cutoff=cutoff.isoformat(),model_horizon='hypothetical one-period choice; not inferred from price dates',measure='hypothetical caller Bernoulli law; not market/risk-neutral calibration',seed=42,scenarios=4)))
ck('same eligible data permits different stated model means',models[0]['caller_model_mean']!=models[1]['caller_model_mean'],True)
observations.append(dict(scope='Conceptual/design disposition, not a new predicate/API',statement='No native price-to-probability/return calibration adapter exists. Eligibility of a historical price return does not establish predictive horizon, probability measure, independence, freshness, adjustment basis or model suitability.'))
observations.append(dict(scope='External record, not ScenarioResult durability',statement='Instrument/currency/source/decision cutoff/model horizon/measure are caller provenance; ScenarioResult stores numeric parameters/seed/values but does not authenticate or durably retain this context.'))
result=dict(python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,observations=observations,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),installed_modules={m.__name__:dict(path=m.__file__,sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for m in [validation,simulation,statistics]},scope='Selected native price validation, explicit caller model alternatives and empirical summaries; no calibration adapter or model acceptance')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
