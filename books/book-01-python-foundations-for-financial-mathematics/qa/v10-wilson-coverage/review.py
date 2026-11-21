"""Exact binomial coverage ofnativeWilson intervals atselectedfixedN/p;notnominalcertification."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import subprocess,json,re,tempfile,importlib.util,math,sys,platform,hashlib
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='51991b60a598dd4167a26cfcc245821655fd8621';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.10-confidence-and-simulation-error.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(listing)==1;rows=[];commands=[];intervals=[];coverage=[];Z=F(49,25)
def check(name,got,want,kind='source Wilson endpoint'):
 ok=got==want if type(want)is bool else math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-12);rows.append(dict(name=name,actual=str(got) if isinstance(got,F) else got,expected=str(want),kind=kind,passed=ok))
def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
def reference(k,n):
 # Independently solve score-test quadratic A*p²-B*p+C<=0.
 A=F(n)*(n+Z*Z);B=F(n)*(2*k+Z*Z);C=F(k*k)
 with localcontext() as c:
  c.prec=160;rad=dec(B*B-4*A*C).sqrt();return (dec(B)-rad)/(2*dec(A)),(dec(B)+rad)/(2*dec(A))
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'simulation_error.py';p.write_text(listing[0]);spec=importlib.util.spec_from_file_location('error_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  r=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0
 for n in [10,20]:
  actual=[m.wilson_interval(k,n) for k in range(n+1)]
  for k,(lo,hi) in enumerate(actual):
   wantlo,wanthi=reference(k,n);check(str((n,k))+' lower',lo,wantlo);check(str((n,k))+' upper',hi,wanthi);intervals.append(dict(trials=n,events=k,native=[lo,hi],reference=[str(wantlo),str(wanthi)]))
  byp={}
  for P in [F(0),F(1,100),F(1,10),F(1,4),F(1,2),F(3,4),F(9,10),F(99,100),F(1)]:
   mass=covered=F(0);decisions=[]
   for k,(lo,hi) in enumerate(actual):
    probability=math.comb(n,k)*P**k*(1-P)**(n-k);score=F(n)*(P-F(k,n))**2<=Z*Z*P*(1-P);contains=F.from_float(lo)<=P<=F.from_float(hi);check(str((n,str(P),k))+' score containment',contains,score,'native interval vs exact score decision');mass+=probability;covered+=probability*score;decisions.append(score)
   check(str((n,str(P)))+' binomial mass',mass,F(1),'exact model aggregate');byp[P]=covered;coverage.append(dict(trials=n,true_probability=str(P),coverage=str(covered),coverage_decimal=float(covered),zero_event_probability=str((1-P)**n),covered_event_counts=[k for k,yes in enumerate(decisions) if yes]))
  for P in [F(0),F(1,100),F(1,10),F(1,4)]:check(str((n,str(P)))+' complement coverage',byp[P],byp[1-P],'exact symmetry aggregate')
result=dict(pin=pin,source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing[0].encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),commands=commands,rows=rows,intervals=intervals,coverage=coverage,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='fixedN independentBernoulli model;coverage diagnostic,notsampler/independence/sequential/95%approval')
(here/((sys.argv[1] if len(sys.argv)>1 else 'first')+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],failed=result['failed'],selected_coverage=[(x['trials'],x['true_probability'],x['coverage_decimal']) for x in coverage if x['true_probability'] in ['1/100','1/2']])));assert result['failed']==0
