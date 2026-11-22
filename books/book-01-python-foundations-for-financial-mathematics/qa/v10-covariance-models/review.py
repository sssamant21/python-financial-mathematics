"""Covariance pairing, nonlinear dependence and inconsistent pairwise matrices."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
import re,sys,json,subprocess,tempfile,importlib.util,hashlib,platform,math,itertools
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='83322aff81c8a0fa62a1cd0787e6cad96acf56e0';source_path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.05-covariance.md';raw=subprocess.check_output(['git','show',pin+':'+source_path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];pairings=[]
def ck(name,got,want,kind,close=False):rows.append(dict(name=name,actual=str(got),expected=str(want),passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if close else got==want,kind=kind))
def cov(x,y,ddof):return (sum(a*b for a,b in zip(x,y))-sum(x)*sum(y)/len(x))/(len(x)-ddof)
def sqrt(x):
 with localcontext() as c:c.prec=100;return float((D(x.numerator)/D(x.denominator)).sqrt())
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'covariance.py';p.write_text(listing);spec=importlib.util.spec_from_file_location('covariance_lab',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 X=[F(v,100) for v in [-2,-1,0,1,2]];Y=[F(v*v,100) for v in [-2,-1,0,1,2]];x=list(map(float,X));y=list(map(float,Y));values=[]
 for i,ys in enumerate(sorted(set(itertools.permutations(Y)))):
  v=list(map(float,ys));matrix=m.covariance_matrix([x,v]);vx,vy=cov(X,X,1),cov(ys,ys,1);c=cov(X,ys,1)
  for ddof in [0,1]:ck(f'pairing{i} cov ddof{ddof}',m.covariance(x,v,ddof),cov(X,ys,ddof),'independent raw cross-product oracle',True)
  ck(f'pairing{i} correlation',m.correlation(x,v),float(c)/sqrt(vx*vy),'native normalized covariance vs raw-product reference',True)
  for w in [F(1,2),F(3,2)]:
   portfolio=[w*a+(1-w)*b for a,b in zip(X,ys)];ck(f'pairing{i} portfolio w{w}',m.two_asset_variance(x,v,float(w)),cov(portfolio,portfolio,1),'direct portfolio observations vs covariance expansion,including signed weights',True)
  for a,b,want in [(0,0,vx),(0,1,c),(1,0,c),(1,1,vy)]:ck(f'pairing{i} matrix{a}{b}',matrix[a][b],want,'native common-row matrix vs raw-moment oracle',True)
  values.append(c);pairings.append(dict(y=list(map(str,ys)),sample_covariance=str(c)))
 ck('same marginals pairing min',min(values),F(-11,40000),'marginal order statistics do not fix covariance');ck('same marginals pairing max',max(values),F(11,40000),'different positional joint pairing')
 ck('nonlinear paired covariance',m.covariance(x,y),0.,'Y=100X² under finite joint law')
 ck('nonlinear paired correlation',m.correlation(x,y),0.,'uncorrelated does not establish independent')
 p_a=F(sum(v<F(-1,100) for v in X),5);p_b=F(sum(v>F(3,100) for v in Y),5);joint=F(sum(a<F(-1,100) and b>F(3,100) for a,b in zip(X,Y)),5)
 ck('specified joint event probability',joint,F(1,5),'external finite law,not native prediction')
 ck('independence product differs',joint!=p_a*p_b,True,'joint.2 versus marginal product.08')
 # Each pair uses its own disjoint observation dates;native scalars are valid.
 ab=m.covariance([-1,1],[-1,1]);ac=m.covariance([-1,1],[-1,1]);bc=m.covariance([-1,1],[1,-1]);external=[[2,ab,ac],[ab,2,bc],[ac,bc,2]];w=[-1,1,1]
 for name,got,want in [('AB',ab,2),('AC',ac,2),('BC',bc,-2)]:ck('pairwise-subset '+name,got,want,'source scalar covariance on different two-row subsets')
 quadratic=sum(F(str(external[i][j]))*w[i]*w[j] for i in range(3) for j in range(3));ck('external inconsistent matrix quadratic',quadratic,-6,'external pairwise assembly is indefinite,no source matrix validation claim')
 common=m.covariance_matrix([[-1,1],[-1,1],[-1,1]]);q=sum(F(str(common[i][j]))*w[i]*w[j] for i in range(3) for j in range(3));ck('native common-row matrix quadratic',q,2,'same complete rows preserve this nonnegative quadratic form')
 prior=json.loads((here.parent/'chapter-15-covariance-review/results.json').read_text());ck('prior whole source identity',hashlib.sha256(raw).hexdigest(),prior['source_sha256'],'F131 prior failures/44 predicates retained');ck('prior listing identity',hashlib.sha256(listing.encode()).hexdigest(),prior['listing_sha256'],'no source change')
r=dict(pin=pin,source_path=source_path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),rows=rows,commands=commands,pairings=pairings,external_pairwise_matrix=external,external_subset_dates=dict(AB=[1,2],AC=[3,4],BC=[5,6]),nonlinear_joint=dict(X=list(map(str,X)),Y=list(map(str,Y)),probability='1/5 per pair',joint_event=str(joint),product=str(p_a*p_b)),executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Selected positional/joint-law/missing-pair assumptions;no real date alignment,independence,PSD/model/platform/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
