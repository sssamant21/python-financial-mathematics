"""Exact weighted nested-prefix study,not an independence or asymptotic certificate."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import subprocess,json,re,tempfile,importlib.util,itertools,math,sys,platform,hashlib
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='63984650b354db8b361106303bc5d2317a314e71';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.09-convergence.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(listing)==1;rows=[];cases=[];commands=[]
def check(name,got,want,kind='source summary'):
 ok=got==want if type(want)is bool else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=str(got) if isinstance(got,F) else got,expected=str(want),kind=kind,passed=ok))
def oracle(vals):
 n=len(vals);mean=sum(vals)/n;var=sum((x-mean)**2 for x in vals)/(n-1)
 with localcontext() as ctx:ctx.prec=120;se=(Decimal(var.numerator)/Decimal(var.denominator)/n).sqrt()
 return dict(count=n,mean=mean,estimated_se=se,absolute_error=abs(mean-100)),var/n
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'monte_carlo_convergence.py';p.write_text(listing[0]);spec=importlib.util.spec_from_file_location('convergence_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  r=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0
 weight={80:F(1,4),100:F(1,2),120:F(1,4)};agg={key:F(0) for key in ['mass','mean2','mean4','mse2','mse4','covariance','difference_variance','estimated_variance2','estimated_variance4','worsens']}
 for seq in itertools.product([80,100,120],repeat=4):
  vals=list(map(F,seq));prob=math.prod(weight[x] for x in seq);actual=m.prefix_study(list(seq),[2,4],100);refs=[];varest=[]
  for i,n in enumerate([2,4]):
   ref,var=oracle(vals[:n]);refs.append(ref);varest.append(var)
   for field,want in ref.items():check(str(seq)+' N'+str(n)+' '+field,actual[i][field],want)
  worse=refs[1]['absolute_error']>refs[0]['absolute_error'];check(str(seq)+' observed error increases',actual[1]['absolute_error']>actual[0]['absolute_error'],worse,'native vs exact decision')
  a=refs[0]['mean']-100;b=refs[1]['mean']-100
  for key,value in [('mass',1),('mean2',a),('mean4',b),('mse2',a*a),('mse4',b*b),('covariance',a*b),('difference_variance',(b-a)**2),('estimated_variance2',varest[0]),('estimated_variance4',varest[1]),('worsens',worse)]:agg[key]+=prob*value
  cases.append(dict(observations=seq,probability=str(prob),native_prefixes=actual,larger_prefix_error_worse=worse))
 for key,want in [('mass',1),('mean2',0),('mean4',0),('mse2',100),('mse4',50),('covariance',50),('difference_variance',50),('estimated_variance2',100),('estimated_variance4',50)]:check(key,agg[key],want,'exact finite-model aggregate')
result=dict(pin=pin,source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing[0].encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,cases=cases,commands=commands,aggregates={k:str(v) for k,v in agg.items()},passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='IID finite-model algebra andactualprefix summaries,not LLN/CLT/platform/model approval')
(here/((sys.argv[1] if len(sys.argv)>1 else 'first')+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],failed=result['failed'],worsening_probability=str(agg['worsens']))));assert result['failed']==0
