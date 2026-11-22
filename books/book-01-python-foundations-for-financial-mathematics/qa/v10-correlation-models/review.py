"""Correlation under outcome selection,aggregation and tied-rank pairing."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='d70076db68175154442acfeb934c721bd438d6ab';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.06-correlation.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];records=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def oracle(x,y):
 a=list(map(F,x));b=list(map(F,y));n=len(a);cross=sum(u*v for u,v in zip(a,b))-sum(a)*sum(b)/n;xx=sum(v*v for v in a)-sum(a)**2/n;yy=sum(v*v for v in b)-sum(b)**2/n
 with localcontext() as ctx:ctx.prec=100;return float((D(abs(cross).numerator)/D(abs(cross).denominator))/(D((xx*yy).numerator)/D((xx*yy).denominator)).sqrt())*(1 if cross>=0 else -1)
def ranks(x):return [sum(v<z for v in x)+F(sum(v==z for v in x)+1,2) for z in x]
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'correlation.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('correlation_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 pairs=list(itertools.product([-1,1],repeat=2))
 for label,selected,want in [('unselected',pairs,0),('agreements',[v for v in pairs if v[0]==v[1]],1),('disagreements',[v for v in pairs if v[0]!=v[1]],-1)]:
  a,b=map(list,zip(*selected));ck(label+' Pearson',m.pearson(a,b),want,'native source on exact caller-selected finite pairs',True);ck(label+' Spearman',m.spearman(a,b),want,'same declared conditional empirical law',True);records.append(dict(name=label,pairs=selected,retention=str(F(len(selected),4)),scope='caller outcome selection,not a native independence or p-value API'))
 groups=[([1,2,3],[3,2,1]),([5,6,7],[7,6,5])];X=sum((x for x,y in groups),[]);Y=sum((y for x,y in groups),[])
 for i,(x,y) in enumerate(groups):ck('within group'+str(i),m.pearson(x,y),-1.,'each group has a descending straight relation')
 ck('pooled Pearson',m.pearson(X,Y),F(5,7),'raw covariance20,raw variances28;aggregation reversal',True);ck('pooled Spearman',m.spearman(X,Y),F(19,35),'exact no-tie rank squares',True)
 x=[1,2,3,4]
 for i,y in enumerate(sorted(set(itertools.permutations([2,2,5,7])))):
  ck(f'tied pairing{i} ranks',m.average_tie_ranks(list(y)),list(map(float,ranks(y))),'independent less-than/equal counting rank oracle')
  ck(f'tied pairing{i} Pearson',m.pearson(x,list(y)),oracle(x,y),'raw cross-sum correlation reference',True)
  ck(f'tied pairing{i} Spearman',m.spearman(x,list(y)),oracle(ranks(x),ranks(y)),'independent counted ranks plus raw-sum oracle',True)
  for j,value in enumerate(m.rolling_pearson(x,list(y),3)):ck(f'tied pairing{i} rolling{j}',value,oracle(x[j:j+3],y[j:j+3]),'selected trailing positional windows,not availability timestamps',True)
  matrix=m.correlation_matrix([x,list(y)])
  for a,b,want in [(0,0,1),(1,1,1),(0,1,oracle(x,y)),(1,0,oracle(x,y))]:ck(f'tied pairing{i} matrix{a}{b}',matrix[a][b],want,'native matrix on common complete rows',True)
 monotone=[1,8,27,64];ck('strict monotone ranks',m.spearman(x,monotone),1.,'ordering is preserved despite nonlinear response')
 ck('strict monotone Pearson differs',m.pearson(x,monotone)!=1.,True,'rank-perfect need not mean linear-perfect')
 collapsed=[1,1,2,2];ck('tie creation changes rank correlation',m.spearman(x,collapsed),oracle(ranks(x),ranks(collapsed)),'non-strict transformation creates ties;strict-monotone invariance does not apply',True)
 prior=json.loads((here.parent/'chapter-15-correlation-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F132 prior failures/50 predicates retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,selection_models=records,pooled_groups=groups,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected correlation/selection/aggregation/rank assumptions;no independence,causality,real timing/model/platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
