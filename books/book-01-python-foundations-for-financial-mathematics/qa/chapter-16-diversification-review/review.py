"""Diversification lab and independent equicorrelation/concentration benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.08-diversification.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.08-diversification.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
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
    with tempfile.TemporaryDirectory(prefix='book1-1608-') as tmp:
        Path(tmp,'diversification.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['diversification.py']),('isolated import',['-c','import diversification']),('exact compilation',['-m','compileall','-q','diversification.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['diversification.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    # Independent equicorrelation quadratic: s^2*(rho+(1-rho)/n).
    def equivar(n,s,rho):return F(str(s))**2*(F(str(rho))+(1-F(str(rho)))/n)
    scenarios=[]
    for rho in [1,.5,0,-1]:
      cov=m.equal_asset_covariance(2,.2,rho);w=[.5,.5];q=equivar(2,.2,rho);sig=root(q)
      num('lab scenario variance '+str(rho),lambda cov=cov:m.portfolio_variance(w,cov),q)
      num('lab scenario SD '+str(rho),lambda cov=cov:m.portfolio_volatility(w,cov),sig)
      num('lab scenario weighted standalone '+str(rho),lambda cov=cov:m.weighted_standalone_volatility(w,cov),F(1,5))
      num('lab scenario benefit '+str(rho),lambda cov=cov:m.diversification_benefit(w,cov),D('.2')-sig)
      if q:
        num('lab scenario ratio '+str(rho),lambda cov=cov:m.diversification_ratio(w,cov),D('.2')/sig)
        ratio=m.diversification_ratio(w,cov)
      else:
        reject('lab zero-risk ratio undefined',lambda:m.diversification_ratio(w,cov));ratio=None
      scenarios.append(dict(correlation=rho,covariance=cov,variance=m.portfolio_variance(w,cov),volatility=m.portfolio_volatility(w,cov),benefit=m.diversification_benefit(w,cov),ratio=ratio))
    for n,s,rho in [(3,.3,0),(10,.2,0),(25,.2,0),(5,.2,.25)]:
      cov=m.equal_asset_covariance(n,s,rho);w=[1/n]*n;q=equivar(n,s,rho)
      num('E10-E13 count '+str(n)+' variance',lambda cov=cov,w=w:m.portfolio_variance(w,cov),q)
      num('E10-E13 count '+str(n)+' SD',lambda cov=cov,w=w:m.portfolio_volatility(w,cov),root(q))
    for label,fn,want in [
      ('E16 concentrated effective holdings',lambda:m.effective_number([.5,.25,.25]),F(8,3)),
      ('E17 equal effective holdings',lambda:m.effective_number([.25]*4),4),
      ('E18 one effective holding',lambda:m.effective_number([1,0,0]),1),
      ('F149 normalized tolerated budget variance',lambda:m.portfolio_variance([1.00000000005],[[1]]),1),
      ('F149 normalized tolerated budget HHI inverse',lambda:m.effective_number([1.00000000005]),1),
      ('F149 tiny-benefit cancellation avoided',lambda:m.diversification_benefit([1,1e-300],[[1,0],[0,1]]),F(1,10**300)),
      ('F149 SD before covariance quadratic underflow',lambda:m.portfolio_volatility([.1,.9],[[1e-323,0],[0,0]]),root(F(1,10**325))),
      ('F149 generated boundary rho above one snapped',lambda:m.equal_asset_covariance(2,.2,1+5e-13)[0][1],F(1,25)),
      ('F149 generated boundary lower rho snapped',lambda:m.portfolio_variance([.5,.5],m.equal_asset_covariance(2,.2,-1-5e-13)),0),
      ('F149 zero-diagonal valid asset retained',lambda:m.portfolio_volatility([.5,.5],[[1,0],[0,0]]),F(1,2)),
    ]:num(label,fn,want)
    for n in [4,7,12]:
      try:
        boundary=m.equal_asset_covariance(n,.2,-1/(n-1))
        try:v=m.portfolio_variance([1/n]*n,boundary)
        except Exception as e:ck('generated rounded boundary requested variance '+str(n),False,exception=repr(e))
        else:ck('generated rounded boundary requested variance '+str(n),0<=v<=1e-16,actual=v,maximum_rounding_variance=1e-16)
        # Tiny positive inward rounding is permitted; replace exact-zero comparison below.
        actual=F(str(boundary[0][1]));lower=-F(str(boundary[0][0]))/(n-1)
        ck('generated rounded lower bound '+str(n),actual>=lower,actual=str(actual),lower_bound=str(lower))
      except Exception as e:ck('generated rounded boundary construction '+str(n),False,exception=repr(e))
    c3=m.equal_asset_covariance(3,.2,-.5)
    num('lab three-asset boundary PSD hedge',lambda:m.portfolio_variance([1/3]*3,c3),0)
    num('lab three-asset boundary entry',lambda:c3[0][1],F(-1,50))
    hhi=F(1,2)**2+2*F(1,4)**2
    close('E15 supplemental HHI',hhi,F(3,8))
    close('E14 supplemental common-correlation limiting SD',root(F(1,25)*F(1,4)),F(1,10))
    ck('lab stress increases SD',scenarios[2]['volatility']<scenarios[1]['volatility']<scenarios[0]['volatility'])
    # Three names can have a high name count but exactly one common risk direction.
    num('E28 correlated three-name effective count',lambda:m.effective_number([1/3]*3),3)
    num('E28 correlated three-name volatility',lambda:m.portfolio_volatility([1/3]*3,m.equal_asset_covariance(3,.2,1)),F(1,5))
    for label,fn in [
      ('PSD extension requested positive direction rejected',lambda:m.portfolio_variance([1,0],[[1,2],[2,1]])),
      ('PSD extension standalone validates entire matrix',lambda:m.weighted_standalone_volatility([1,0],[[1,2],[2,1]])),
      ('PSD extension pairwise bounds insufficient',lambda:m.diversification_ratio([1,0,0],[[1,.9,.9],[.9,1,-.9],[.9,-.9,1]])),
      ('F149 generated covariance underflow rejected',lambda:m.equal_asset_covariance(2,1e-200,0)),
      ('F149 generated covariance overflow ValueError',lambda:m.equal_asset_covariance(2,1e308,0)),
      ('F149 tiny negative form not clipped',lambda:m.portfolio_variance([.5,.5],[[1e-300,-2e-300],[-2e-300,1e-300]])),
      ('F149 zero-variance nonzero covariance rejected',lambda:m.portfolio_variance([1,0],[[1,1e-20],[1e-20,0]])),
      ('F149 variance output underflow rejected',lambda:m.portfolio_variance([.1,.9],[[1e-323,0],[0,0]])),
      ('F149 huge integer matrix ValueError',lambda:m.portfolio_volatility([1],[[10**1000]])),
      ('invalid three-asset equicorrelation rejected',lambda:m.equal_asset_covariance(3,.2,-.75)),
      ('invalid count rejected',lambda:m.equal_asset_covariance(True,.2,0)),
      ('short weights rejected',lambda:m.effective_number([1.2,-.2])),
      ('invalid budget rejected',lambda:m.effective_number([.6,.3])),
      ('asymmetric matrix rejected',lambda:m.portfolio_volatility([.5,.5],[[1,.1],[.3,1]])),
      ('nonfinite matrix rejected',lambda:m.portfolio_volatility([1],[[math.nan]])),
    ]:reject(label,fn)
    report=dict(assets=['fictional A','fictional B'],units='decimal simple-return SD and squared decimal covariance',horizon='one common synthetic period',currency='fictional common USD',dates=None,weights=[.5,.5],standalone_volatilities=[.2,.2],scenarios=scenarios,three_asset_boundary_matrix=c3,
      concentration_weights=[.5,.25,.25],HHI=str(hhi),effective_holdings=m.effective_number([.5,.25,.25]),fixture_sha256=hashlib.sha256(json.dumps([[.5,.5],.2,[1,.5,0,-1]]).encode()).hexdigest(),scope='static synthetic covariance and concentration; no actual data calibration, FX, costs or rebalance')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
