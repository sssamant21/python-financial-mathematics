import ast,contextlib,hashlib,io,json,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from decimal import Decimal as D,Inexact,ROUND_DOWN,getcontext,localcontext
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]

def run():
 checks=[];mods={};codes={};sources=[];runs=[]
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,expected,call):
  try:call();actual='none'
  except Exception as e:actual=type(e).__name__
  ck(id,'exception',actual,expected)
 for n in (10,11,12,13):
  p=next((BOOK/'chapter-03').glob(f'3.{n}-*.md'));s=p.read_text();a=re.search(r'^## .*Hands-On Lab.*$',s,re.M).start();e=s.find('\n## ',a+1);code=re.findall(r'^```python\n(.*?)^```',s[a:e],re.M|re.S)[0];codes[n]=code;sources.append(dict(path=str(p.relative_to(BOOK)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code.encode()).hexdigest()))
  if n<13:
   m=types.ModuleType('lab'+str(n));exec(compile(code,str(p),'exec'),m.__dict__);mods[n]=m
 r,c,f=mods[10],mods[11],mods[12]
 q=r.periodic_rate_from_nominal(D('.08'),periods_per_year=4);ck('3.10-E1','quarterly nominal',q,D('.02'));ck('3.10-E2','annual rational',F(r.effective_annual_rate(q,periods_per_year=4)),F(51,50)**4-1);ck('3.10-E3','discount factor',r.discount_factor(D('.25'),periods=1),D('.8'));ck('3.10-E4','negative factor',r.discount_factor(D('-.1'),periods=1)>1,True)
 err('3.10-E5','TypeError',lambda:r.accumulation_factor(D('.05'),periods=True));err('3.10-E5','TypeError',lambda:r.periodic_rate_from_nominal(D('.08'),periods_per_year=4.5));err('3.10-E5','ValueError',lambda:r.discount_factor(D('Infinity'),periods=1))
 with localcontext() as x:
  x.prec=3;direct=D(2)/D(3);staged=D(2)*(D(1)/D(3));ck('3.10-E7','low precision staging differs',direct==staged,False)
 before=getcontext().copy()
 with localcontext() as x:
  x.prec=2;x.traps[Inexact]=True;err('3.10-E9','Inexact',lambda:r.accumulation_factor(D('.05'),periods=2))
 ck('3.10-E9','precision and traps restored',(getcontext().prec,dict(getcontext().traps),dict(getcontext().flags)),(before.prec,dict(before.traps),dict(before.flags)))
 nested=c.apply_factor(D('104.04'),factor=c.discount_factor(c.periodic_rate_from_nominal(D('.08'),periods_per_year=4),periods=2));wrapped=c.present_value_from_nominal(D('104.04'),nominal_annual_rate=D('.08'),periods_per_year=4,periods=2)
 ck('3.11-E1','nested/staged bound',abs(nested-wrapped)<=D('1e-24'),True);ck('3.11-E2','quarterly known value',wrapped,D(100));ck('3.11-E3','nominal annual misused monthly',(D('1.12')**12)==D('1.01')**12,False)
 for amount,freq,n,expected in [(D('Infinity'),12,1,'ValueError'),(D(100),12.5,1,'TypeError'),(D(100),12,-1,'ValueError')]:err('3.11-E4',expected,lambda amount=amount,freq=freq,n=n:c.present_value_from_nominal(amount,nominal_annual_rate=D('.12'),periods_per_year=freq,periods=n))
 ck('3.11-E5','negative nominal raises PV',c.present_value_from_nominal(D(100),nominal_annual_rate=D('-.12'),periods_per_year=12,periods=1)>D(100),True)
 ck('3.11-E6','early cents affect doubling',(D('1.005')*2)==D('1.005').quantize(D('.01'))*2,False)
 def prints():print('100')
 with contextlib.redirect_stdout(io.StringIO()):err('3.11-E9','TypeError',lambda:D(1)+prints())
 market={'rate':D('.05')}
 def ambient(p):return p*(1+market['rate'])
 first=ambient(D(100));market['rate']=D('.1');ck('3.12-E1','hidden global changes result',first==ambient(D(100)),False)
 with contextlib.redirect_stdout(io.StringIO()):ck('3.12-E2','printing return',prints(),None)
 def snapshot(x):return (x.prec,x.rounding,x.Emin,x.Emax,x.capitals,x.clamp,dict(x.flags),dict(x.traps))
 reference=f.fixed_present_value(D(125),periodic_rate=D('.25'),periods=1)
 with localcontext() as x:
  x.prec=6;x.rounding=ROUND_DOWN;x.flags[Inexact]=True;original=snapshot(x)
  ck('3.12-E3','fixed result',f.fixed_present_value(D(125),periodic_rate=D('.25'),periods=1),reference);ck('3.12-E3','settings preserved',snapshot(x),original)
  err('3.12-E4','ValueError',lambda:f.fixed_present_value(D(125),periodic_rate=D('NaN'),periods=0));ck('3.12-E4','failure preserves context',snapshot(x),original)
 policy_variant=types.ModuleType('policy_variant');assert codes[12].count('prec=40')==1
 exec(compile(codes[12].replace('prec=40','prec=6'),'policy_variant','exec'),policy_variant.__dict__)
 ck('3.12-E5','changed precision alters selected value',policy_variant.fixed_present_value(D('1234.56'),periodic_rate=D('.037'),periods=17)==f.fixed_present_value(D('1234.56'),periodic_rate=D('.037'),periods=17),False)
 values=[]
 def alias(items):items.append(1)
 alias(values);ck('3.12-E8','alias mutation',values,[1])
 ck('3.13-E1','known144 PV',f.fixed_present_value(D(144),periodic_rate=D('.2'),periods=2),D(100));ck('3.13-E3','near-minus-one scale',f.fixed_present_value(D(1),periodic_rate=D('-.99'),periods=2),D(10000));ck('3.13-E6','actual Decimal return type',type(reference).__name__,'Decimal')
 with tempfile.TemporaryDirectory() as tmp:
  tmp=Path(tmp);(tmp/'reproducibility_lab.py').write_text(codes[12]);(tmp/'test_financial_functions.py').write_text(codes[13])
  tree=ast.parse(codes[13]);names=[method.name for cls in tree.body if isinstance(cls,ast.ClassDef) for method in cls.body if isinstance(method,ast.FunctionDef) and method.name.startswith('test_')];assert len(names)==12
  for name in names:
   p=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_financial_functions.TestPresentValue.'+name],cwd=tmp,text=True,capture_output=True,timeout=15);runs.append(dict(method=name,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr));ck('3.13-E7','individual '+name,p.returncode,0)
  assert codes[12].count('** periods')>=1
  mutant=codes[12].replace('** periods','** (periods + 1)',1);(tmp/'reproducibility_lab.py').write_text(mutant)
  p=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_financial_functions.TestPresentValue.test_known_values'],cwd=tmp,text=True,capture_output=True,timeout=15);runs.append(dict(method='wrong-horizon mutation',exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr));ck('3.13-E4','wrong horizon detected',p.returncode,1)
 out=dict(python=sys.version,platform=platform.platform(),exercise_records=36,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),sources=sources,individual_and_mutant_runs=runs,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('sources','individual_and_mutant_runs','checks')},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
