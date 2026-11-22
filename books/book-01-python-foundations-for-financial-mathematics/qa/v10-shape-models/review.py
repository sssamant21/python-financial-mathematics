"""Matching finite empirical moments do not identify distribution or tail events."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='3c23b8721b0e2fa5a936438fd9cb0fa1aa4e0fbe';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.04-skewness-and-kurtosis.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def sqrt(x):
 with localcontext() as c:c.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
def oracle(x):
 n=len(x);rawmom=[sum((v**k for v in x),F(0))/n for k in [1,2,3,4]];a,b,c,d=rawmom;m2=b-a*a;m3=c-3*a*b+2*a**3;m4=d-4*a*c+6*a*a*b-3*a**4;skew=sqrt(m3*m3/m2**3)*(1 if m3>=0 else -1);kurt=m4/m2**2
 return dict(n=n,mean=a,m2=m2,skewness=skew,kurtosis=kurt,excess_kurtosis=kurt-3),rawmom
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'skewness_kurtosis.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('shape_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 first=([0]*6+[-1]*2+[1]*2+[-2,2])*6;second=[0]*16+[-1]*27+[1]*27+[-3,3];assert len(first)==len(second)==72
 data={'bounded2':[F(v,100) for v in first],'rare3':[F(v,100) for v in second]};reports={};raws={}
 for name,x in data.items():
  expected,rawmom=oracle(x);actual=m.standardized_moments(list(map(float,x)));reports[name]=actual;raws[name]=rawmom
  for k,want in expected.items():ck(name+' '+k,actual[k],want,'raw-power expansion of central moments,not native centered sums',True)
  ck(name+' adjusted skew',m.adjusted_sample_skewness(list(map(float,x))),0.,'symmetric finite law')
  ck(name+' adjusted excess',m.adjusted_sample_excess_kurtosis(list(map(float,x))),F(6*71,70*69),'n72,g2=0 implies positive finite-sample correction',True)
  tail=m.downside_frequency(list(map(float,x)),-.02);ck(name+' strict below−2%',tail,F(0) if name=='bounded2' else F(1,72),'exact weighted finite-law tail event',True)
  models.append(dict(name=name,observations=list(map(str,x)),weight='1/72',raw_moments=list(map(str,rawmom)),native_report=actual,strict_below_minus_2_percent=str(tail),scope='deterministic multiset encoding a finite law,not72 IID draws or a fitted market model'))
 ck('same first four raw moments',raws['bounded2'],raws['rare3'],'same mean,variance,third and fourth moment')
 ck('same full native shape report',reports['bounded2'],reports['rare3'],'same n72 and shape statistics,but distinct tail distributions')
 ck('same normal-reference excess value',reports['bounded2']['excess_kurtosis'],0.,'excess0 does not identify a Gaussian distribution')
 original=[F(-4,100),F(-1,100),F(0),F(2,100),F(8,100)]
 for label,x in [('project',original),('positive stress',original[:-1]+[F(28,100)]),('negative stress',[F(-24,100)]+original[1:]),('caller removed zero',data['rare3'][1:])]:
  # Last fixture is a disclosed deletion of a zero;record exactly what changed.
  want,_=oracle(x);got=m.standardized_moments(list(map(float,x)))
  for k,v in want.items():ck(label+' '+k,got[k],v,'native source vs independent raw-moment expansion',True)
 for label,scale,shift in [('units',F(100),F(0)),('loss reflection',F(-1),F(0)),('shift',F(1),F(1,20))]:
  transformed=[scale*v+shift for v in original];want,_=oracle(transformed);got=m.standardized_moments(list(map(float,transformed)))
  for k,v in want.items():ck(label+' '+k,got[k],v,'affine measurement transform with declared decimal values',True)
 prior=json.loads((here.parent/'chapter-15-shape-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'prior F130 evidence retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,models=models,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Finite moment-matching/shape/selection measurements,not tail calibration,Gaussian identification,model/platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
