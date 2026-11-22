"""Fixed-design finite regression laws, classical-SE limits and selection counterexamples."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import datetime,timezone
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools,math
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='1d5215359aa0b0897cd05778a48ec136a48f50ea';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.10-linear-regression.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
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
 x=[-3,-1,1,3];xx=F(20);laws=[('IID unit Rademacher',[list(z) for z in itertools.product([-1,1],repeat=4)],[1,1,1,1]),('independent heteroskedastic',[[a*b for a,b in zip(z,[1,1,1,4])] for z in itertools.product([-1,1],repeat=4)],[1,1,1,16]),('dependent slope shock',[[s*v for v in x] for s in [-1,1]],None)]
 for name,errors,variances in laws:
  fits=[]
  for i,e in enumerate(errors):
   y=[1+2*v+w for v,w in zip(x,e)];got=m.ols_simple(x,y);want=oracle(x,y);fits.append(got)
   for k in ['intercept','slope','sse','sst','r_squared','residual_variance']:ck(f'{name} path{i} {k}',got[k],want[k],'native field vs exact uncentered normal equations',True)
   for k in ['intercept','slope']:ck(f'{name} path{i} ratio {k}',F(got['coefficient_ratios'][k]),want[k],'native exact coefficient vs independent determinant solution')
   for k in ['fitted','residuals']:
    for j,v in enumerate(want[k]):ck(f'{name} path{i} {k}{j}',got[k][j],v,'native field vs exact projection',True)
   ck(f'{name} path{i} slope SE',got['slope_standard_error'],sqrt(want['slope_se_square']),'native classical formula vs exact expectation, NOT sampling calibration',True)
   ck(f'{name} path{i} residual sum',sum(map(F,got['residuals'])),F(0),'native residual normal equation',True)
   ck(f'{name} path{i} residual orthogonality',sum(F(a)*F(b) for a,b in zip(x,got['residuals'])),F(0),'native residual normal equation',True)
  n=len(fits);mean=sum(F(z['coefficient_ratios']['slope']) for z in fits)/n;actual_variance=sum((F(z['coefficient_ratios']['slope'])-mean)**2 for z in fits)/n;mean_estimated_square=sum(F(z['slope_standard_error'])**2 for z in fits)/n
  true_variance=sum(F(v)*a*a for v,a in zip(variances,x))/(xx*xx) if variances else F(1)
  expected_estimated=sum((1-F(1,4)-F(a*a,20))*v for a,v in zip(x,variances))/2/xx if variances else F(0)
  ck(name+' mean slope',mean,F(2),'native coefficients averaged over exact finite law')
  ck(name+' actual slope sampling variance',actual_variance,true_variance,'native weighted coefficient variation vs covariance formula')
  ck(name+' expected classical estimated variance',mean_estimated_square,expected_estimated,'native SE squared averaged vs residual-projection trace',True)
  models.append(dict(name=name,paths=n,weight=str(F(1,n)),mean_slope=str(mean),true_slope_variance=str(actual_variance),mean_native_classical_SE_squared=str(float(mean_estimated_square)),exact_expected_classical_estimated_variance=str(expected_estimated),scope='Fixed design; hypothetical finite zero-mean errors, not real data or Student-t reference law',native_fits=fits))
 # Conditional on nonconstant response only: usual R2 defined. Constants handled
 # separately by existing source convention, not counted as explained variance.
 x2=[-1,3,-3,1];fixed=[];selected=[]
 for i,y in enumerate(itertools.product([-1,1],repeat=4)):
  if len(set(y))==1:continue
  a=m.ols_simple(x,list(y));b=m.ols_simple(x2,list(y));wa=oracle(x,list(y));wb=oracle(x2,list(y));fa=wa['r_squared'];fb=wb['r_squared']
  ck(f'selection response{i} first R2',a['r_squared'],fa,'native predefined fit vs exact null projection',True)
  ck(f'selection response{i} second R2',b['r_squared'],fb,'native alternative fit vs exact null projection',True)
  ck(f'selection response{i} selected R2',max(a['r_squared'],b['r_squared']),max(fa,fb),'caller same-sample selection, not independent predictive test',True)
  fixed.append(fa);selected.append(max(fa,fb))
 ck('selection raises average same-sample R2',sum(selected)>sum(fixed),True,'exact selected null-law comparison')
 models.append(dict(name='same-sample selection',conditional_nonconstant_paths=len(fixed),mean_predeclared_R2=str(sum(fixed)/len(fixed)),mean_selected_R2=str(sum(selected)/len(selected)),scope='Caller chooses greater of two training R2 values; no inference p-value or holdout acceptance'))
 train=m.ols_simple(x,[1+2*v for v in x]);holdx=[-1,1];holdy=[1-2*v for v in holdx];pred=[m.predict(train,v) for v in holdx];base=[1,1]
 ck('regime-change training R2',train['r_squared'],1,'native in-sample perfect fit')
 ck('regime-change training SE',train['slope_standard_error'],0,'zero estimated variance is not inference validity')
 ck('regime-change holdout predictions',pred,[-1.,3.],'native predictions fixed before holdout evaluation')
 ck('regime-change holdout RMSE',m.rmse(holdy,pred),4,'native holdout metric vs exact errors')
 ck('regime-change training-mean baseline RMSE',m.rmse(holdy,base),2,'native baseline metric vs exact errors')
 models.append(dict(name='explicit hypothetical slope reversal',training_predictors=x,holdout_predictors=holdx,holdout_actual=holdy,holdout_predictions=pred,scope='Caller chronology/regime fixture; native API has no date/timestamp guard and no detected-real-break claim'))
prior=json.loads((here.parent/'chapter-15-regression-review/results.json').read_text())
assert hashlib.sha256(raw).hexdigest()==prior['source_sha256']
assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256']
identity=dict(prior_source_sha256=prior['source_sha256'],prior_listing_sha256=prior['listing_sha256'],identities_match=True,scope='Earlier F136 twelve baseline failures/61 corrected predicates retained, not recounted. Whole-source and exact listing identities match prior corrected evidence.')
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence=identity,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Fixed-design finite error laws and caller selection/regime counterexamples; no robust/HAC API, t-reference calibration, real market model or independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);print([(x.get('name'),x.get('true_slope_variance'),x.get('exact_expected_classical_estimated_variance'),x.get('mean_selected_R2')) for x in models]);assert result['failed']==0
