"""Two-asset opportunity set and independent rational optimum benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.09-two-asset-portfolios.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.09-two-asset-portfolios.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1609-') as tmp:
        Path(tmp,'two_asset_portfolios.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['two_asset_portfolios.py']),('isolated import',['-c','import two_asset_portfolios']),('exact compilation',['-m','compileall','-q','two_asset_portfolios.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['two_asset_portfolios.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    mu1=.08;mu2=.04;s1=.2;s2=.3;rho=1/6
    def moments(w,c):
        w=F(str(w));a=F(1,25);b=F(9,100)
        return w*F(2,25)+(1-w)*F(1,25),w*w*a+(1-w)**2*b+2*w*(1-w)*c
    p=m.portfolio(.6,mu1,mu2,s1,s2,rho)
    for field,want in [('expected_return',F(8,125)),('variance',F(21,625)),('volatility',root(F(21,625)))]:close('E1/E3/E4 main '+field,p[field],want)
    close('E2 supplemental covariance',F(1,5)*F(3,10)*F(1,6),F(1,100))
    for w,er,var in [(1,F(2,25),F(1,25)),(0,F(1,25),F(9,100))]:
        result=m.portfolio(w,mu1,mu2,s1,s2,rho)
        close('E5/E6 endpoint return '+str(w),result['expected_return'],er);close('E5/E6 endpoint variance '+str(w),result['variance'],var)
    for rho2,want in [(0,F(1,50)),(1,F(1,25)),(-1,0)]:num('E7-E9 equal-risk variance '+str(rho2),lambda rho2=rho2:m.portfolio(.5,0,0,.2,.2,rho2)['variance'],want)
    for label,fn,want in [
      ('unconstrained perfect-correlation hedge weight',lambda:m.minimum_variance_weight(.2,.3,1,False)['w1'],3),
      ('unconstrained outside-range target weight',lambda:m.target_return_weight(.12,.09,.05,False)['w1'],F(7,4)),
      ('E10 target allocation',lambda:m.target_return_weight(.07,.09,.05)['w1'],F(1,2)),
      ('E12 zero-correlation minimum A',lambda:m.minimum_variance_weight(.2,.3,0)['w1'],F(9,13)),
      ('E13 zero-correlation minimum B',lambda:1-m.minimum_variance_weight(.2,.3,0)['w1'],F(4,13)),
      ('E15 long-only boundary optimum',lambda:m.minimum_variance_weight(.1,.2,1)['w1'],1),
      ('E18 signed expected return',lambda:m.portfolio(1.2,.1,.05,.2,.3,0,True)['expected_return'],F(11,100)),
      ('E19 complementary weight',lambda:m.portfolio(.3,0,0,.2,.3,0)['w2'],F(7,10)),
      ('F150 small-scale nondegenerate optimizer',lambda:m.minimum_variance_weight(1e-200,2e-200,0)['w1'],F(4,5)),
      ('F150 large-scale optimizer before squared overflow',lambda:m.minimum_variance_weight(1e200,2e200,0)['w1'],F(4,5)),
      ('F150 near-identical but distinct long-only optimum',lambda:m.minimum_variance_weight(1,1.000000000000001,1)['w1'],1),
      ('F150 nearby means remain distinct',lambda:m.target_return_weight(1.5e-16,2e-16,1e-16)['w1'],F(1,2)),
      ('F150 large integer target retains difference',lambda:m.target_return_weight(10**18+1,10**18+2,10**18)['w1'],F(1,2)),
      ('F150 expected-return signed integer cancellation',lambda:m.portfolio(.5,10**18+2,-10**18,0,0,0)['expected_return'],1),
      ('F150 huge sigma exact hedge',lambda:m.portfolio(.5,0,0,1e308,1e308,-1)['variance'],0),
    ]:num(label,fn,want)
    ck('equal means attainable target nonunique',m.target_return_weight(.05,.05,.05)['w1'] is None)
    ck('E16 exactly identical risk nonunique',m.minimum_variance_weight(.2,.2,1)['w1'] is None)
    try:zero=m.minimum_variance_weight(0,0,0);ck('F150 both zero volatilities nonunique',zero['w1'] is None)
    except Exception as e:ck('F150 both zero volatilities nonunique',False,exception=repr(e))
    grid=m.frontier(mu1,mu2,s1,s2,rho,10)
    ck('E20 inclusive grid count',len(grid)==11)
    for i,point in enumerate(grid):
      er,var=moments(F(i,10),F(1,100))
      close('lab grid return '+str(i),point['expected_return'],er);close('lab grid variance '+str(i),point['variance'],var)
    profiles=[]
    for label,c,rr,expected_w,grid_w in [('main',F(1,100),rho,F(8,11),F(7,10)),('zero',0,0,F(9,13),F(7,10)),('positive',F(3,50),1,1,1),('negative',F(-3,50),-1,F(3,5),F(3,5))]:
      optimum=m.minimum_variance_weight(s1,s2,rr)['w1'];close('lab analytic optimum '+label,optimum,expected_w)
      curve=m.frontier(mu1,mu2,s1,s2,rr,10);chosen=min(curve,key=lambda x:x['variance'])
      close('lab discrete optimum '+label,chosen['w1'],grid_w)
      result=m.portfolio(optimum,mu1,mu2,s1,s2,rr)
      _,minimum=moments(expected_w,c)
      close('lab analytic minimum variance '+label,result['variance'],minimum)
      ck('lab discrete vs analytic '+label,chosen['variance']>=result['variance']-1e-15,discrete=chosen['variance'],analytic=result['variance'])
      profiles.append(dict(label=label,correlation=rr,analytic_weight=optimum,analytic=result,grid_minimum=chosen))
    num('lab six-percent target in main model',lambda:m.target_return_weight(.06,mu1,mu2)['w1'],F(1,2))
    num('E14 separate zero-rho minimum variance',lambda:m.portfolio(9/13,mu1,mu2,s1,s2,0)['variance'],F(9,325))
    num('E14 separate zero-rho minimum SD',lambda:m.portfolio(9/13,mu1,mu2,s1,s2,0)['volatility'],root(F(9,325)))
    num('E17 correlation sensitivity',lambda:(m.portfolio(.5,0,0,s1,s2,.1)['variance']-m.portfolio(.5,0,0,s1,s2,0)['variance'])/.1,F(3,100))
    # Analytic complete-square identity is independent of an optimizer implementation.
    c=F(1,100);den=F(11,100);wstar=F(8,11);minimum=F(7,220)
    ck('lab independent complete-square minimum proof',all(moments(F(i,10),c)[1]==minimum+den*(F(i,10)-wstar)**2 for i in range(11)),minimum_reference=str(minimum),weight_reference=str(wstar))
    for label,fn in [
      ('E11 outside long-only target rejected',lambda:m.target_return_weight(.12,.09,.05)),
      ('F150 unequal tiny target not erased',lambda:m.target_return_weight(2e-16,1e-16,1e-16)),
      ('F150 nonboolean portfolio policy rejected',lambda:m.portfolio(.5,0,0,.2,.3,0,'yes')),
      ('F150 nonboolean optimizer policy rejected',lambda:m.minimum_variance_weight(.2,.3,0,'yes')),
      ('F150 nonboolean target policy rejected',lambda:m.target_return_weight(.07,.09,.05,'yes')),
      ('F150 unreportable required variance rejected',lambda:m.portfolio(.5,0,0,1e-200,1e-200,0)),
      ('F150 unreportable variance overflow ValueError',lambda:m.portfolio(.5,0,0,1e308,1e308,0)),
      ('F150 unreconcilable displayed weight budget rejected',lambda:m.portfolio(1e100,0,0,1,1,1,True)),
      ('F150 huge integer parameter ValueError',lambda:m.portfolio(.5,10**1000,0,.2,.3,0)),
      ('invalid correlation rejected',lambda:m.portfolio(.5,0,0,.2,.3,2)),
      ('short permission required',lambda:m.portfolio(1.2,0,0,.2,.3,0)),
      ('invalid steps rejected',lambda:m.frontier(0,0,.2,.3,0,True)),
    ]:reject(label,fn)
    report=dict(assets=['fictional A','fictional B'],expected_returns=[mu1,mu2],volatilities=[s1,s2],rho_displayed=rho,ideal_rational_rho='1/6',units='decimal simple-return means/SD and squared covariance',horizon='one common synthetic period',currency='fictional common USD',dates=None,main_weight=.6,main_result=p,profiles=profiles,
      grid=grid,target_return='.06',target_weight=m.target_return_weight(.06,mu1,mu2),model_scope='static fictional population moments; no actual calibration/financing/costs',fixture_sha256=hashlib.sha256(json.dumps([mu1,mu2,s1,s2,rho]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
