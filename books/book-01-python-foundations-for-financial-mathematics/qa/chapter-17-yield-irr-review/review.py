"""Yield/IRR exact-source commands and independent financial expectations."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from datetime import date,datetime,timedelta
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.04-solving-yield-and-irr-problems.md';source=BOOK/path
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    blocks=re.findall(rb'^```python\n(.*?)^```',data,re.M|re.S);code=next(b for b in blocks if b'import unittest' in b);commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn,kind=ValueError):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,kind),exception=repr(e),expected_exception=kind.__name__)
        else:ck(label,False,actual=repr(v),expected_exception=kind.__name__)
    with tempfile.TemporaryDirectory(prefix='book1-1704-') as tmp:
        Path(tmp,'solving_yield_and_irr_problems.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and 12 tests',['solving_yield_and_irr_problems.py']),('silent import',['-c','import solving_yield_and_irr_problems']),('compile exact listing',['-m','compileall','-q','solving_yield_and_irr_problems.py']),('exact SciPy IRR example',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            ok=p.returncode==0
            if methods is not None:ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            if label=='exact SciPy IRR example':
                try:
                    rr=float(re.search(r'IRR: (\S+)',p.stdout)[1]);res=float(re.search(r'NPV residual: (\S+)',p.stdout)[1]);ok=ok and abs(rr-((3+math.sqrt(69))/10-1))<1e-12 and abs(res)<1e-10
                except Exception:ok=False
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
    m=types.ModuleType('yield_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    with localcontext() as ctx:ctx.prec=100;twoirr=(D(3)+D(69).sqrt())/10-1;halfyear=(D('1.1')**(D(365)/182))-1
    d=date(2025,1,1);annual=[(d,-100),(date(2026,1,1),110)]
    for label,fn,want,atol in [
      ('E1 periodic IRR',lambda:m.periodic_irr([-100,110])['root'],F(1,10),1e-12),
      ('E2 two-year periodic IRR',lambda:m.periodic_irr([-100,0,121])['root'],F(1,10),1e-12),
      ('E3 zero NPV',lambda:m.pv(0,[-100,60,60]),20,0),
      ('E4 tenth NPV',lambda:m.pv(.1,[-100,60,60]),F(500,121),0),
      ('E5 upper bracket NPV',lambda:m.pv(.2,[-100,60,60]),F(-25,3),0),
      ('lab two-receipt IRR',lambda:m.periodic_irr([-100,60,60],0,.2)['root'],twoirr,1e-12),
      ('E6 zero-coupon price',lambda:m.bond_dirty_price(100,0,2,.1),F(10000,121),0),
      ('E7 rounded-price implied yield',lambda:m.bond_ytm(100,0,2,82.64463)['root'],D(100/82.64463).sqrt()-1,1e-12),
      ('E8 par bond',lambda:m.bond_dirty_price(100,.05,3,.05),100,0),
      ('E11 coupon',lambda:F(1000)*F(4,100),40,0),
      ('E18 clean plus accrued supplemental',lambda:F(99)+F(5,4),F(401,4),0),
      ('E32 residual supplemental',lambda:F(9800001,100000)-98,F(1,100000),0),
      ('E33 half-width supplemental',lambda:F(1,10**10)/2,F(1,2*10**10),0),
      ('E36 duration supplemental',lambda:F(2,100)/F(1,100),2,0),
      ('dated annual XNPV',lambda:m.dated_xnpv(.1,d,annual),0,1e-12),
      ('dated annual XIRR',lambda:m.xirr(d,annual)['root'],F(1,10),1e-12),
      ('dated 182-day XIRR',lambda:m.xirr(d,[(d,-100),(d+timedelta(days=182),110)])['root'],halfyear,1e-12),
      ('F161 periodic integer cancellation',lambda:m.pv(0,[-10**18,10**18+1]),1,0),
      ('F161 periodic tiny rate',lambda:m.pv(1e-308,[-1,1]),F(-1,10**308),0),
      ('F161 periodic power overflow',lambda:m.pv(1e308,[0,0,1e308]),F(1,10**308),0),
      ('F161 finite bond after coupon overflow',lambda:m.bond_dirty_price(1e308,2,1,10),F(3*10**308,11),0),
      ('F161 dated integer cancellation',lambda:m.dated_xnpv(0,d,[(d,-10**18),(d,10**18+1)]),1,0),
      ('F161 dated tiny rate',lambda:m.dated_xnpv(1e-308,d,[(d,-1),(d+timedelta(days=365),1)]),F(-1,10**308),0),
      ('F161 dated huge-rate exponent',lambda:m.dated_xnpv(1e308,d,[(d+timedelta(days=730),1e308)]),F(1,10**308),0),
      ('F161 wide midpoint',lambda:m.bisection(lambda x:x/1e308,-1e308,1e308)['root'],0,0),
    ]:num(label,fn,want,atol=atol)
    prices=[]
    for r in [.04,.05,.06]:
        want=sum(F(c)/(1+F(str(r)))**t for t,c in enumerate([0,5,5,105]));num('bond rational repricing '+str(r),lambda r=r:m.bond_dirty_price(100,.05,3,r),want);prices.append(m.bond_dirty_price(100,.05,3,r))
    ck('E9 E10 E14 price direction',prices[0]>100 and prices[1]==100 and prices[2]<100,prices=prices)
    num('lab recover six-percent YTM',lambda:m.bond_ytm(100,.05,3,prices[2])['root'],F(3,50),atol=1e-12,rtol=0)
    for lo,hi,w in [(.05,.15,F(1,10)),(.15,.25,F(1,5))]:
        num('E20 separate IRR bracket '+str(lo),lambda lo=lo,hi=hi:m.periodic_irr([-100,230,-132],lo,hi)['root'],w,atol=1e-12,rtol=0)
        num('E20 substitution '+str(w),lambda w=w:m.pv(float(w),[-100,230,-132]),0,atol=1e-12,rtol=0)
    for label,fn,kind in [
      ('all-zero periodic IRR',lambda:m.periodic_irr([0,0]),ValueError),
      ('all-zero dated IRR',lambda:m.xirr(d,[(d,0),(d+timedelta(days=365),0)]),ValueError),
      ('same-date cancelling XIRR',lambda:m.xirr(d,[(d,-100),(d,100)]),ValueError),
      ('dated generator rejected explicitly',lambda:m.xirr(d,(x for x in annual)),ValueError),
      ('datetime base rejected explicitly',lambda:m.dated_xnpv(.1,datetime(2025,1,1),[(datetime(2025,1,1),-100),(datetime(2026,1,1),110)]),ValueError),
      ('malformed dated flow',lambda:m.dated_xnpv(.1,d,[(d,1,2)]),ValueError),
      ('bad periodic rate',lambda:m.pv(-1,[-100,110]),ValueError),
      ('bad string bound',lambda:m.periodic_irr([-100,110],'bad',1),ValueError),
      ('unreportable positive PV',lambda:m.pv(1,[0,0,5e-324]),ValueError),
      ('all negative no IRR',lambda:m.periodic_irr([-100,-10,-10]),ValueError),
      ('no sign change',lambda:m.periodic_irr([-100,110],.2,.5),ValueError),
      ('iteration budget',lambda:m.bisection(lambda x:x*x-2,1,2,max_iter=1),RuntimeError),
      ('coordinate stagnation',lambda:m.bisection(lambda x:-1 if x<=1 else 1,1,math.nextafter(1,2),xtol=1e-30),RuntimeError),
      ('noncallable',lambda:m.bisection(None,0,1),ValueError),
      ('huge integer input',lambda:m.pv(10**1000,[-100,110]),ValueError),
    ]:reject('F161 '+label,fn,kind)
    # ACT/365 fixed includes leap day; exact two-date inverse is (1.1)^(365/366)-1.
    leap=date(2024,1,1)
    with localcontext() as ctx:ctx.prec=100;want=D('1.1')**(D(365)/366)-1
    num('E29 leap-year XIRR',lambda:m.xirr(leap,[(leap,-100),(date(2025,1,1),110)])['root'],want,atol=1e-12,rtol=0)
    num('dated pre-base annual amount',lambda:m.dated_xnpv(.1,d,[(d-timedelta(days=365),100)]),110)
    num('dated unordered duplicate aggregation',lambda:m.dated_xnpv(.1,d,[(date(2026,1,1),110),(d,-10**18),(d,10**18-100)]),0,atol=1e-12,rtol=0)
    num('dated fractional exponent repricing',lambda:m.dated_xnpv(.1,d,[(d+timedelta(days=182),110)]),D(110)/(D('1.1')**(D(182)/365)))
    num('E30 exact IRR endpoint',lambda:m.periodic_irr([-100,110],.1,.2)['root'],F(1,10))
    r=m.periodic_irr([-100,60,60],0,.2)
    num('lab independent repricing at solved rate',lambda:float(-F(100)+F(60)/(1+F(str(r['root'])))+F(60)/(1+F(str(r['root'])))**2),0,atol=1e-9,rtol=0)
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,model=dict(periodic_flows=[-100,60,60],bond=dict(face=100,coupon_rate=.05,years=3,prices=prices),dated_flows=[['2025-01-01',-100],['2026-01-01',110]],day_count='ACT/365 fixed',units='fictional common currency and annual effective rates',timing='t0 initial plus exact annual period ends; dated case uses actual elapsed calendar days',irr_result=r))
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
