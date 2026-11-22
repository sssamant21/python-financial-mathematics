"""Regression omitted-variable, influence, pairing and raw/excess-return boundaries."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='5da9c8d7875acd64ab532feed63537cbe63749c6';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.10-linear-regression.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind,approx=False):
 ok=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want
 rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=ok))
def oracle(x,y):
 n=len(x);sx=sum(x);sy=sum(y);sxx=sum(v*v for v in x);sxy=sum(a*b for a,b in zip(x,y));det=n*sxx-sx*sx;b=F(n*sxy-sx*sy,det);a=F(sy-b*sx,n);fit=[a+b*v for v in x];e=[v-w for v,w in zip(y,fit)];sse=sum(v*v for v in e);sst=sum((v-F(sy,n))**2 for v in y);sigma=sse/F(n-2);xx=sxx-F(sx*sx,n)
 return dict(intercept=a,slope=b,fitted=fit,residuals=e,sse=sse,sst=sst,r_squared=1-sse/sst if sst else F(1),residual_variance=sigma,slope_se_square=sigma/xx)
def sqrt(x):
 with localcontext() as c:c.prec=100;return (D(x.numerator)/D(x.denominator)).sqrt()
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'linear_regression.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('regression_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 def fit(name,x,y):
  # Interpret float fixtures by displayed decimal, matching the declared source policy.
  X=[F(str(v)) for v in x];Y=[F(str(v)) for v in y];got=m.ols_simple(x,y);want=oracle(X,Y)
  for k in ['intercept','slope','sse','sst','r_squared','residual_variance']:ck(name+' '+k,got[k],want[k],'native field vs independent exact determinant equations',True)
  for k in ['intercept','slope']:ck(name+' ratio '+k,F(got['coefficient_ratios'][k]),want[k],'native coefficient ratios vs independent determinant')
  for k in ['fitted','residuals']:
   for i,v in enumerate(want[k]):ck(name+' '+k+str(i),got[k][i],v,'native projection field vs independent equations',True)
  ck(name+' slope SE',got['slope_standard_error'],sqrt(want['slope_se_square']),'native classical formula arithmetic only',True)
  return got,want
 x=[-3,-1,1,3];slopes=[]
 for i,u in enumerate(itertools.product([-1,1],repeat=4)):
  z=[a+b for a,b in zip(x,u)];y=[1+2*a+3*b for a,b in zip(x,z)];got,want=fit('omitted variable '+str(i),x,y);beta=F(got['coefficient_ratios']['slope']);slopes.append(beta)
  structural_error=[3*v for v in z]
  ck('omitted '+str(i)+' projection bias',beta-2,sum(F(a)*b for a,b in zip(x,structural_error))/20,'native slope vs known structural error projection')
  ck('omitted '+str(i)+' fitted residual orthogonality',sum(F(a)*F(b) for a,b in zip(x,got['residuals'])),0,'OLS residual identity does not prove exogeneity',True)
  models.append(dict(name='omitted variable path'+str(i),x=x,z=z,y=y,source_fit=got,scope='Hypothetical structural equation y=1+2x+3z with z=x+u. Structural coefficient2 is specified, not identified by native simple OLS.'))
 ck('omitted variable exact law mean fitted slope',sum(slopes)/16,F(5),'exact independent u signs, omitted term conditional mean3x')
 ck('omitted exact law mean slope bias',sum(slopes)/16-2,F(3),'specified structural contrast, not causal discovery')
 base,_=fit('influence base',[-1,0,1],[-1,0,1]);X=[-1,0,1,10];Y=[-1,0,1,100];full,ref=fit('influence full',X,Y);leave=[]
 for i in range(4):g,w=fit('influence delete'+str(i),X[:i]+X[i+1:],Y[:i]+Y[i+1:]);leave.append(g)
 mean=F(sum(X),4);xx=sum((F(a)-mean)**2 for a in X);leverage=[F(1,4)+(F(a)-mean)**2/xx for a in X]
 ck('max leverage appended observation',leverage.index(max(leverage)),3,'supplemental exact hat diagonal')
 ck('hat diagonals sum parameter count',sum(leverage),F(2),'supplemental design identity')
 ck('delete appended point restores base coefficients',leave[3]['coefficient_ratios'],base['coefficient_ratios'],'native leave-one-out fit, no influence API')
 models.append(dict(name='explicit leverage sensitivity',full=full,leave_one_out=leave,hat_diagonals=list(map(str,leverage)),scope='Caller deletion/design calculations, not robust regression or automatic outlier rejection'))
 raw_x=[1,2,3,4];raw_y=[3,5,7,9];raw_model,_=fit('raw returns',raw_x,raw_y);fixed_rf=[1]*4;varying_rf=[0,1,0,2]
 fixed,_=fit('constant benchmark excess',[a-b for a,b in zip(raw_x,fixed_rf)],[a-b for a,b in zip(raw_y,fixed_rf)]);varying,_=fit('varying benchmark excess',[a-b for a,b in zip(raw_x,varying_rf)],[a-b for a,b in zip(raw_y,varying_rf)])
 ck('constant benchmark slope invariant',fixed['slope'],raw_model['slope'],'native fixed-benchmark transformation')
 ck('constant benchmark intercept transformation',F(fixed['coefficient_ratios']['intercept']),F(raw_model['coefficient_ratios']['intercept'])+(F(raw_model['coefficient_ratios']['slope'])-1),'exact response/predictor common shift')
 ck('varying benchmark slope differs',varying['slope']!=raw_model['slope'],True,'raw and excess models can have different slopes')
 mispaired,_=fit('reversed response positional input',raw_x,list(reversed(raw_y)))
 ck('mispaired slope sign',mispaired['slope'],-2,'native positional pairing accepts equal-length reordered observations')
 models.append(dict(name='pairing and benchmark boundary',raw=raw_model,constant_benchmark_excess=fixed,varying_benchmark_excess=varying,mispaired=mispaired,declared_units='hypothetical percentage points per common period, no market dates or real risk-free curve',scope='Native API has no timestamp/currency/frequency/availability guards or CAPM calibration adapter. Caller transformations, no authenticity/point-in-time claim.'))
 # Prescribed project fixture: prove what the caller-selected training slice uses,
 # while preserving the fact that the source API cannot enforce the split.
 market=[.01,.02,.03,.04,.01,.02,.03,.04,.05,.06];asset=[.02,.04,.05,.09,.03,.03,.07,.08,.11,.10]
 train,ref=fit('prescribed project training',market[:8],asset[:8]);changed=asset[:8]+[-999,999];train2=m.ols_simple(market[:8],changed[:8]);ck('caller training slice excludes altered holdout outcomes',train2,train,'caller slice behavior, not a native leakage detector')
 fixture_sha=hashlib.sha256(json.dumps([market,asset]).encode()).hexdigest();prior=json.loads((here.parent/'chapter-15-regression-review/results.json').read_text());ck('prior prescribed fixture identity',fixture_sha,prior['project_report']['fixture_sha256'],'source-prescribed synthetic fixture hash')
 ck('training first eight labels',len(market[:8]),8,'caller explicit training bound')
 models.append(dict(name='prescribed project lineage',fixture_sha256=fixture_sha,period_labels=list(range(1,11)),training_labels=list(range(1,9)),holdout_labels=[9,10],calendar_dates=None,return_basis='raw daily decimal simple returns, no risk-free adjustment',source_train=train,mutated_holdout=changed[8:],scope='Caller provenance/split, not native date availability or source authenticity checks'))
prior=json.loads((here.parent/'chapter-15-regression-review/results.json').read_text());assert hashlib.sha256(raw).hexdigest()==prior['source_sha256'];assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Omitted-variable finite fixture, leverage/deletion sensitivity, positional/raw-excess and caller project lineage; no causality/HAC/calendar/model/independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
