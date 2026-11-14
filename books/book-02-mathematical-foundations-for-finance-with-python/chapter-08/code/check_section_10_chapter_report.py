"""Full fixed report oracle/CLI serialization and selected validation priorities."""
import json,math,subprocess,sys
from pathlib import Path
from decimal import Decimal,Context,localcontext
import section_8_10 as source

def observations():
 rows=[]
 def check(name,actual,want,rtol=0):
  ok=math.isfinite(actual) and math.isclose(actual,want,rel_tol=rtol,abs_tol=0) if rtol else actual==want
  rows.append(dict(name=name,actual=repr(actual),expected=repr(want),passed=ok))
 refs=[]
 for precision in (150,250):
  with localcontext(Context(prec=precision)):
   C=Decimal(10000);R=Decimal(.04);T=Decimal(5);H=Decimal(.001);P=C*(-R*T).exp();gap=T*H
   expected={'profit_maximizer':125.,'marginal_profit_at_maximizer':0.,'pv':float(P),'pv_rate_first':float(-T*P),'pv_rate_second':float(T*T*P),'pv_shock_10bp':{'first_order':float(-gap*P),'second_order':float(P*(-gap+gap*gap/2)),'exact':float(P*((-gap).exp()-1))},'log_return_80_to_84':float((Decimal(84)/80).ln()),'break_even_quantity':30.,'break_even_derivative':-1.,'bond_yield':.1,'bond_yield_price_derivative':-.011}
   # Rounded callback samples are the stencil's inputs,not analytic derivatives.
   h=Decimal(.1);up=Decimal((2+.1)**3);down=Decimal((2-.1)**3);expected['cubic_centered_first']=float((up-down)/(2*h))
   up=Decimal((2+.1)**2);mid=Decimal(4);down=Decimal((2-.1)**2);expected['quadratic_centered_second']=float((up-2*mid+down)/(h*h));refs.append(expected)
 assert refs[0]==refs[1]
 expected=refs[0];report=source.chapter_report();check('top-level exact keys/order',list(report),list(expected));check('nested exact keys/order',list(report['pv_shock_10bp']),list(expected['pv_shock_10bp']))
 def leaves(d,prefix=''):
  for k,x in d.items():
   if isinstance(x,dict):yield from leaves(x,prefix+k+'.')
   else:yield prefix+k,x
 actual=dict(leaves(report));wanted=dict(leaves(expected));check('leaf count',len(actual),15);check('all leaves finite plain floats',all(type(x) is float and math.isfinite(x) for x in actual.values()),True)
 for key,value in actual.items():check('independent report '+key,value,wanted[key],rtol=4e-14 if wanted[key] else 0)
 encoded=json.dumps(report,allow_nan=False,separators=(',',':'));check('strict JSON roundtrip',json.loads(encoded),report);check('selected compact JSON budget <=4096 bytes',len(encoded.encode())<=4096,True)
 again=source.chapter_report();check('fresh top-level dictionary',again is not report,True);check('fresh nested dictionary',again['pv_shock_10bp'] is not report['pv_shock_10bp'],True);check('deterministic full report',again,report)
 report['pv_shock_10bp']['exact']=123;check('caller mutation isolation',source.chapter_report(),again)
 cli=subprocess.run([sys.executable,str(Path(source.__file__))],capture_output=True,text=True);check('CLI exit',cli.returncode,0);check('CLI stderr empty',cli.stderr,'');payload=json.loads(cli.stdout,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)));check('CLI whole stdout is strict report JSON',payload,again)
 # Current named diagnostics establish observed priority,not stable public wording.
 controls=[('PV amount first',lambda:source.present_value(False,math.nan,True),'TypeError','payment'),('derivatives years first',lambda:source.pv_rate_derivatives('x',math.nan,True),'TypeError','years'),('shock first',lambda:source.pv_rate_shock('x',math.nan,False,True),'TypeError','shock'),('log start first',lambda:source.log_return(False,math.nan),'TypeError','start'),('break price first',lambda:source.break_even_quantity(False,math.nan,0),'TypeError','price'),('bond payment first',lambda:source.bond_yield_from_price(False,math.nan),'TypeError','payment'),('first callable first',lambda:source.centered_first(None,math.nan,True),'TypeError','callable'),('second callable first',lambda:source.centered_second(None,math.nan,True),'TypeError','callable'),('profit bool',lambda:source.profit(False),'TypeError','quantity'),('marginal NaN',lambda:source.marginal_profit(math.nan),'ValueError','quantity')]
 for label,fn,kind,token in controls:
  try:fn();observed=('none','')
  except Exception as e:observed=(type(e).__name__,str(e))
  check('priority '+label,(observed[0],token in observed[1]),(kind,True))
 return dict(predicates=rows,report=again,expected_report=expected,compact_json_bytes=len(encoded.encode()),cli=dict(returncode=cli.returncode,stdout=cli.stdout,stderr=cli.stderr),limits='One fixed report and selected priority pairs;JSON byte budget is QA-only,not a product cap. No independent/model/platform/release acceptance.')
if __name__=='__main__':
 d=observations();print(json.dumps(d,indent=2,allow_nan=False));print(len(d['predicates']),'report predicates;',sum(not x['passed'] for x in d['predicates']),'failed');assert all(x['passed'] for x in d['predicates'])
