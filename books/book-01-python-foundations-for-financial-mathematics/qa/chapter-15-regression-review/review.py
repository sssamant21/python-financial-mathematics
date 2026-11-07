"""Section 15.10 exact regression lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.10-linear-regression.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1510-') as tmp:
        Path(tmp,'linear_regression.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['linear_regression.py']),('isolated import',['-c','import linear_regression']),('exact compilation',['-m','compileall','-q','linear_regression.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['linear_regression.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('regression_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    def oracle(x,y):
        a=[F(str(v)) for v in x];b=[F(str(v)) for v in y];n=len(a)
        # Solve the 2x2 normal equations using uncentered rational sums.
        sx=sum(a);sy=sum(b);sxx=sum(v*v for v in a);sxy=sum(u*v for u,v in zip(a,b))
        det=n*sxx-sx*sx;beta=(n*sxy-sx*sy)/det;alpha=(sy-beta*sx)/n
        fitted=[alpha+beta*u for u in a];res=[v-p for v,p in zip(b,fitted)]
        sse=sum(e*e for e in res);sst=sum(v*v for v in b)-sy*sy/n
        return dict(intercept=alpha,slope=beta,sse=sse,sst=sst,r_squared=1-sse/sst if sst else 1,
            residual_variance=sse/(n-2),slope_standard_error=root(sse/(n-2)/(sxx-sx*sx/n))),fitted,res
    x=[1,2,3,4];y=[3,5,7,9];base=m.ols_simple(x,y)
    for key,want in [('slope',2),('intercept',1),('sse',0),('sst',20),('r_squared',1),('residual_variance',0),('slope_standard_error',0)]:close('E6-E15 perfect '+key,base[key],want,atol=0)
    num('E8 prediction',lambda:m.predict(base,5),11)
    num('E16 RMSE',lambda:m.rmse([1,-1,1,-1],[0,0,0,0]),1)
    num('E18 response shift',lambda:m.ols_simple(x,[v+10 for v in y])['intercept'],11)
    num('E19 predictor scale',lambda:m.ols_simple([2*v for v in x],y)['slope'],1)
    # Fully specified financial lab: 8 training periods in two 4-period windows, then two holdout periods.
    market=[.01,.02,.03,.04,.01,.02,.03,.04,.05,.06]
    asset=[.02,.04,.05,.09,.03,.03,.07,.08,.11,.10]
    train=m.ols_simple(market[:8],asset[:8]);want,fit,res=oracle(market[:8],asset[:8])
    for k,v in want.items():close('project train '+k,train[k],v,atol=0)
    for i in range(8):
        close('project fitted '+str(i),train['fitted'][i],fit[i],atol=0)
        close('project residual '+str(i),train['residuals'][i],res[i],atol=1e-17)
    close('project training RMSE',m.rmse(asset[:8],train['fitted']),root(want['sse']/8),atol=0)
    windows=[]
    for lo in [0,4]:
        actual=m.ols_simple(market[lo:lo+4],asset[lo:lo+4]);w,_,_=oracle(market[lo:lo+4],asset[lo:lo+4])
        for k in ['intercept','slope']:close('project window '+str(lo)+' '+k,actual[k],w[k],atol=1e-17)
        windows.append(actual)
    predicted=[m.predict(train,v) for v in market[8:]]
    expected_pred=[want['intercept']+want['slope']*F(str(v)) for v in market[8:]]
    for i,v in enumerate(predicted):close('project chronological holdout '+str(i),v,expected_pred[i],atol=0)
    holdout_sse=sum((F(str(a))-p)**2 for a,p in zip(asset[8:],expected_pred))
    close('project holdout RMSE',m.rmse(asset[8:],predicted),root(holdout_sse/2),atol=0)
    naive_mean=sum(map(lambda v:F(str(v)),asset[:8]))/8
    close('project training-only mean baseline RMSE',m.rmse(asset[8:],[float(naive_mean)]*2),root(sum((F(str(v))-naive_mean)**2 for v in asset[8:])/2),atol=0)
    for label,fn,want in [
        ('F136 integer offset slope',lambda:m.ols_simple([10**18+i for i in range(4)],y)['slope'],2),
        ('F136 integer offset prediction',lambda:m.predict(m.ols_simple([10**18+i for i in range(4)],y),10**18+4),11),
        ('F136 tiny predictor slope',lambda:m.ols_simple([1e-200,2e-200,3e-200],[1,2,3])['slope'],1e200),
        ('F136 huge predictor slope',lambda:m.ols_simple([1e200,2e200,3e200],[1,2,3])['slope'],1e-200),
        ('F136 large constant response',lambda:m.ols_simple([1,2,3],[1e308]*3)['intercept'],1e308),
        ('F136 RMSE large squares',lambda:m.rmse([-1e200,1e200],[0,0]),1e200),
        ('F136 RMSE tiny squares',lambda:m.rmse([-1e-200,1e-200],[0,0]),1e-200),
        ('F136 prediction cancels intermediate overflow',lambda:m.predict(dict(intercept=-1e308,slope=1e308),2),1e308),
    ]:num(label,fn,want)
    for label,fn in [
        ('E17 zero predictor variance',lambda:m.ols_simple([1,1,1],[1,2,3])),
        ('F136 decimal constant predictor',lambda:m.ols_simple([.05]*3,[1,2,3])),
        ('insufficient residual df',lambda:m.ols_simple([1,2],[3,5])),
        ('unequal lengths rejected',lambda:m.ols_simple([1,2,3],[1,2])),
        ('missing rejected',lambda:m.ols_simple([1,2,None],[1,2,3])),
        ('nonfinite rejected',lambda:m.ols_simple([1,2,math.inf],[1,2,3])),
        ('boolean rejected',lambda:m.ols_simple([True,2,3],[1,2,3])),
        ('F136 unreportable fit aggregate rejected',lambda:m.ols_simple([1,2,3],[-1e308,0,1e308])),
        ('F136 unreportable prediction rejected',lambda:m.predict(dict(intercept=1e308,slope=1e308),1)),
    ]:reject(label,fn)
    ck('project fixtures preserved',market==[.01,.02,.03,.04,.01,.02,.03,.04,.05,.06] and asset==[.02,.04,.05,.09,.03,.03,.07,.08,.11,.10])
    project=dict(market=market,asset=asset,period_labels=list(range(1,11)),dates=None,frequency='hypothetical daily',return_convention='raw decimal simple returns; no risk-free adjustment',
        fixture_sha256=hashlib.sha256(json.dumps([market,asset]).encode()).hexdigest(),train_periods=[1,8],window_periods=[[1,4],[5,8]],holdout_periods=[9,10],
        train=train,windows=windows,holdout_predictions=predicted,holdout_rmse=m.rmse(asset[8:],predicted),naive_training_mean=float(naive_mean),naive_rmse=m.rmse(asset[8:],[float(naive_mean)]*2),
        residual_table=[dict(period=i+1,market=market[i],asset=asset[i],fitted=train['fitted'][i],residual=train['residuals'][i]) for i in range(8)])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
