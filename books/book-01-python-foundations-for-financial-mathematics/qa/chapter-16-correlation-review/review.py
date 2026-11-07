"""Correlation lab and independent pairwise covariance/stress benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.11-correlation-and-diversification.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.11-correlation-and-diversification.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:
            if value is None:ck(label,False,actual='None',independent_reference=str(want))
            else:close(label,value,want)
    def reject(label,fn):
        try:v=fn()
        except ValueError as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(v))
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80;return (D(v.numerator)/D(v.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1611-') as tmp:
        Path(tmp,'correlation_and_diversification.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['correlation_and_diversification.py']),('isolated import',['-c','import correlation_and_diversification']),('exact compilation',['-m','compileall','-q','correlation_and_diversification.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['correlation_and_diversification.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    x=[1,2,3];positive=[2,4,6];negative=[6,4,2]
    for label,fn,want in [
      ('E1 perfect positive',lambda:m.sample_correlation(x,positive),1),
      ('E2 perfect negative',lambda:m.sample_correlation(x,negative),-1),
      ('E3 zero sample correlation',lambda:m.sample_correlation([-1,0,1],[1,-2,1]),0),
      ('E4 sample covariance',lambda:m.sample_covariance(x,positive),2),
      ('E5 covariance from correlation',lambda:m.covariance_from_volatility([.2,.3],[[1,.5],[.5,1]])[0][1],F(3,100)),
      ('F152 integer centering retained',lambda:m.sample_covariance([10**18,10**18+1],[10**18,10**18+1]),F(1,2)),
      ('F152 huge constant mean avoids overflow',lambda:m.sample_covariance([1e308,1e308],[1e308,1e308]),0),
      ('F152 finite covariance after division',lambda:m.sample_covariance([-1e154,0,1e154],[-1e154,0,1e154]),1e308),
      ('F152 tiny correlation avoids moment underflow',lambda:m.sample_correlation([0,1e-200],[0,2e-200]),1),
      ('F152 huge correlation avoids moment overflow',lambda:m.sample_correlation([-1e308,1e308],[-1e308,1e308]),1),
      ('F152 normalized tolerated budget volatility',lambda:m.portfolio_volatility([1.00000000005],[[1]]),1),
      ('F152 root before quadratic underflow',lambda:m.portfolio_volatility([.1,.9],[[1e-323,0],[0,0]]),root(F(1,10**325))),
      ('F152 accepted correlation diagonal normalized',lambda:m.covariance_from_volatility([.2],[[1.00000000005]])[0][0],F(1,25)),
      ('F152 accepted off-diagonal upper excursion clipped',lambda:m.covariance_from_volatility([.2,.2],[[1,1.00000000005],[1.00000000005,1]])[0][1],F(1,25)),
    ]:num(label,fn,want)
    close('E6 supplemental inverse conversion',F(1,100)/(F(1,5)*F(3,10)),F(1,6))
    for rho,want in [(0,F(1,50)),(1,F(1,25)),(-1,0)]:
      c=m.covariance_from_volatility([.2,.2],[[1,rho],[rho,1]])
      num('E7-E9 portfolio SD '+str(rho),lambda c=c:m.portfolio_volatility([.5,.5],c),root(want))
    c0=m.covariance_from_volatility([.2,.3],[[1,0],[0,1]]);c1=m.covariance_from_volatility([.2,.3],[[1,.1],[.1,1]])
    close('E10 supplemental/source variance sensitivity',(m.portfolio_volatility([.5,.5],c1)**2-m.portfolio_volatility([.5,.5],c0)**2)/.1,F(3,100))
    # Common complete dates, asset-major orientation. Pairwise differences are the oracle.
    rows=[[-.01,0,.01,0],[.01,-.02,.01,0],[0,.01,0,-.01]]
    def paircov(a,b):return sum((F(str(a[i]))-F(str(a[j])))*(F(str(b[i]))-F(str(b[j]))) for i in range(len(a)) for j in range(i+1,len(a)))/(len(a)*(len(a)-1))
    scov=[[paircov(a,b) for b in rows] for a in rows]
    estimated=m.correlation_matrix(rows)
    for i in range(3):
      for j in range(3):
        num('lab source sample covariance '+str((i,j)),lambda i=i,j=j:m.sample_covariance(rows[i],rows[j]),scov[i][j])
        expected=(1 if scov[i][j]>=0 else -1)*root(scov[i][j]**2/(scov[i][i]*scov[j][j]))
        close('lab source sample correlation '+str((i,j)),estimated[i][j],expected)
    normalized=m.covariance_from_volatility([.2]*3,estimated)
    # Estimated dependence with assumed .2 standalone SD is a separately labelled rescaled model.
    normal_risk=m.portfolio_volatility([1/3]*3,normalized)
    with localcontext() as ctx:
        ctx.prec=80
        reference_sd=(D('.04')*(3-2/root(3))/9).sqrt()
    close('lab rescaled empirical-dependence model SD',normal_risk,reference_sd)
    stresses=[]
    for rho in [0,.25,.75]:
      r=m.equicorrelation(3,rho);c=m.covariance_from_volatility([.2]*3,r);sd=m.portfolio_volatility([1/3]*3,c)
      want=F(1,25)*(F(str(rho))+(1-F(str(rho)))/3)
      close('lab common correlation stress '+str(rho),sd,root(want));stresses.append(dict(rho=rho,correlation=r,covariance=c,volatility=sd))
    r5=m.equicorrelation(5,.25);num('E13 five-asset common model',lambda:m.portfolio_volatility([.2]*5,m.covariance_from_volatility([.2]*5,r5)),root(F(2,125)))
    close('E14 supplemental common floor',root(F(1,25)*F(1,4)),F(1,10))
    for n in [3,4,7]:
      r=m.equicorrelation(n,-1/(n-1))
      ck('E11/E12 generated bound '+str(n),F(str(r[0][1]))>=F(-1,n-1),actual=str(r[0][1]),lower=str(F(-1,n-1)))
    ck('lab estimated matrix symmetric and unit diagonal',all(estimated[i][j]==estimated[j][i] and estimated[i][i]==1 for i in range(3) for j in range(3)))
    nonlinear_x=[-2,-1,0,1,2];nonlinear_y=[4,1,0,1,4]
    num('E19 zero correlation despite nonlinear dependence',lambda:m.sample_correlation(nonlinear_x,nonlinear_y),0)
    for label,fn in [
      ('PSD extension invalid full correlation rejected',lambda:m.covariance_from_volatility([.2]*3,[[1,.9,.9],[.9,1,-.9],[.9,-.9,1]])),
      ('PSD extension invalid full covariance rejected',lambda:m.portfolio_volatility([1,0],[[1,2],[2,1]])),
      ('F152 negative tiny variance not clipped',lambda:m.portfolio_volatility([1],[[-1e-300]])),
      ('F152 zero-variance nonzero row rejected',lambda:m.portfolio_volatility([1,0],[[1,1e-20],[1e-20,0]])),
      ('F152 unreportable covariance underflow rejected',lambda:m.sample_covariance([0,1e-200],[0,1e-200])),
      ('F152 unreportable covariance output rejected',lambda:m.covariance_from_volatility([1e308],[[1]])),
      ('F152 huge integer sample ValueError',lambda:m.sample_correlation([10**1000,0],[1,0])),
      ('constant sample correlation undefined',lambda:m.sample_correlation([1,1,1],[1,2,3])),
      ('invalid three-asset common rho rejected',lambda:m.equicorrelation(3,-.75)),
      ('invalid sample alignment rejected',lambda:m.sample_covariance([1,2],[1])),
      ('short weights rejected',lambda:m.portfolio_volatility([1.2,-.2],[[1,0],[0,1]])),
    ]:reject(label,fn)
    report=dict(assets=['fictional A','fictional B','fictional C'],sample_series_asset_major=rows,observation_labels=[1,2,3,4],sample_covariance=[[str(v) for v in row] for row in scov],sample_correlation=estimated,
      rescaled_standalone_SDs=[.2]*3,rescaled_covariance=normalized,rescaled_model_volatility=normal_risk,stress_models=stresses,
      units='decimal one-period simple returns; squared covariance',currency='fictional common USD',dates=None,missingness='complete common observations; no imputation',model_scope='sample dependence, rescaled dependence model, and hypothetical equicorrelation stresses kept separate',fixture_sha256=hashlib.sha256(json.dumps(rows).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
