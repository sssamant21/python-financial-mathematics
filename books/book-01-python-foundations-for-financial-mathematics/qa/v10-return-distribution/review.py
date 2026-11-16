"""Pinned18.5 return-model assumptions;controlledtwo-pointlaw vsnormal moment formula.
Usage: python THIS first|replay
"""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from decimal import Decimal,localcontext
from fractions import Fraction as F
here=Path(__file__).resolve().parent;root=here.parents[3];pin='4251353f502d823654eb7920618e545903f37f7e';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.05-return-simulations.md';stem=sys.argv[1];raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(fences)==1;rows=[];commands=[];cases=[]
def check(name,got,want,kind='source numeric'):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,kind=kind,actual=got,independent_expected=str(want),passed=ok));assert ok,name
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);p=t/'return_simulations.py';p.write_text(fences[0])
 for argv in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(argv,cwd=t,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 spec=importlib.util.spec_from_file_location('return_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);Original=m.random.Random
 for mean,sd in [(0.,.2),(.04,.2),(.04,.4),(.04,0.)]:
  seen=[]
  class Controlled:
   def __init__(self,seed):self.values=iter([-1.,1.])
   def normalvariate(self,mu,sigma):seen.append((mu,sigma));return next(self.values)
  m.random.Random=Controlled
  try:logs=m.simulate_log_returns(mean,sd,2,7)
  finally:m.random.Random=Original
  label=str((mean,sd));M,S=F(str(mean)),F(str(sd));expected_logs=[M-S,M+S]
  for i,want in enumerate(expected_logs):check(label+' log'+str(i),logs[i],want)
  ok=seen==[(0,1),(0,1)] and m.random.Random is Original;rows.append(dict(name=label+' controlled standard draw/restoration',kind='observer contract',passed=ok));assert ok
  values=m.terminal_values(100,logs);summary=m.summarize(values,100)
  with localcontext() as ctx:
   ctx.prec=120;D=Decimal;DM=D(str(mean));DS=D(str(sd));targets=[D(100)*(DM-DS).exp(),D(100)*(DM+DS).exp()];pair_mean=sum(targets)/2;geometric=D(100)*DM.exp();gaussian=D(100)*(DM+DS*DS/2).exp()
  for i,want in enumerate(targets):check(label+' terminal'+str(i),values[i],want)
  A,B=map(lambda x:F(str(x)),values);average=(A+B)/2;var=(A-B)**2/2
  with localcontext() as ctx:ctx.prec=120;se=(Decimal(var.numerator)/Decimal(var.denominator)/2).sqrt()
  refs=dict(count=2,mean_terminal=average,mean_simple_return=(average-100)/100,standard_error_terminal=se,loss_frequency=F(sum(x<100 for x in (A,B)),2))
  for key,want in refs.items():check(label+' summary '+key,summary[key],want,'summary from supplied observations')
  normal=m.expected_terminal(100,mean,sd);check(label+' normal analytic mean API',normal,gaussian)
  check(label+' controlled pair mean',summary['mean_terminal'],pair_mean,'supplemental two-point law')
  check(label+' caller geometric mean',math.sqrt(values[0]*values[1]),geometric,'caller composition')
  differs=pair_mean<gaussian if sd>0 else pair_mean==gaussian;rows.append(dict(name=label+' same log moments do not fix exp mean',kind='supplemental distribution assumption',passed=differs));assert differs
  cases.append(dict(mean_log=mean,sd_log=sd,controlled_standard_draws=[-1,1],source_log_returns=logs,source_terminal_values=values,source_summary=summary,two_point_expected_terminal=str(pair_mean),normal_expected_terminal=str(gaussian),geometric_center=str(geometric),population_log_mean=str(M),population_log_variance=str(S*S),normal_formula_applies_to_controlled_law=sd==0))
 assert p.read_text()==fences[0]
result=dict(source_revision=pin,source_path=path,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=hashlib.sha256(fences[0].encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,rows=rows,passed=len(rows),failed=0,cases=cases,limits='Controlledstandarddraws[-1,+1]formtwo-pointlaw,notnormalgeneratorvalidation. Source summarySEfieldisconditionalarithmetic,not validuncertaintyforthefixedpairedquadrature. SharedDecimalexp backend;no normalCDF/tailF165orfinancialmeasure/platform/independentacceptance.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(len(rows),'predicates;',len(cases),'distribution cases')
