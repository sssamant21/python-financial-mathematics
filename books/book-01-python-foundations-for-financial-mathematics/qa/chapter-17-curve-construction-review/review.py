"""Exact-source elementary curve construction, repricing and scope evidence."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.10-curve-construction-concepts.md';source=BOOK/path
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    blocks=re.findall(rb'^```python\n(.*?)^```',data,re.M|re.S);code=next(b for b in blocks if b'import unittest' in b);commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,ValueError),exception=repr(e),expected_exception='ValueError')
        else:ck(label,False,actual=repr(v),expected_exception='ValueError')
    with tempfile.TemporaryDirectory(prefix='book1-1710-') as tmp:
        Path(tmp,'curve_construction.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and twelve tests',['curve_construction.py']),('silent import',['-c','import curve_construction']),('compile exact listing',['-m','compileall','-q','curve_construction.py']),('exact SciPy bootstrap snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label!='exact SciPy bootstrap snippet':ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        import contextlib,io
        ns={};capture=io.StringIO()
        with contextlib.redirect_stdout(capture):exec(compile(blocks[0],'exact_scipy_snippet','exec'),ns)
        num('SciPy independent bootstrap DF',lambda:ns['df_two'],F(127,140))
        num('SciPy independent rational repricing',lambda:F(5)*F(19,20)+F(105)*F(str(ns['df_two'])),100,atol=1e-12,rtol=0)
    m=types.ModuleType('curve_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    times=[1,2,3];rates=[.04,.05,.055];flows=[(1,5),(2,105)]
    with localcontext() as ctx:
        ctx.prec=400
        d1=D('-.04').exp();d2=D('-.1').exp();df25=D('-.1325').exp();pv=5*d1+105*d2
        implied=-(D(127)/140).ln()/2;tinyforward=(D(10**18+1)/D(10**18)).ln();bigforward=D('1e616').ln()
        coupled=D('1e308')*D(-800).exp()
        bumped=5*D('-.0401').exp()+105*D('-.1002').exp()
    boot1=m.bootstrap_one_year_df(95,100);boot2=m.bootstrap_two_year_df(100,5,100,boot1)
    for label,fn,want in [
      ('E1 source discount',lambda:m.discount_from_zero(2,.05),d2),
      ('E2 source zero',lambda:m.zero_from_discount(2,float(d2)),F(1,20)),
      ('E3 source negative rate',lambda:m.discount_from_zero(2,-.01),D('.02').exp()),
      ('E4 supplemental single PV',lambda:F(100)*F(9,10),90),
      ('E5 source coupon PV',lambda:m.price_cashflows(flows,times,rates),pv),
      ('E6 one-year bootstrap',lambda:boot1,F(19,20)),
      ('E7 two-year bootstrap',lambda:boot2,F(127,140)),
      ('lab bootstrapped zero recovery',lambda:m.zero_from_discount(2,boot2),implied),
      ('lab two-year bond repricing',lambda:F(5)*F(str(boot1))+F(105)*F(str(boot2)),100),
      ('lab three-node interpolation',lambda:m.log_discount_curve(times,rates,2.5),df25),
      ('E17 average forward',lambda:m.forward_between(1,2,float(d1),float(d2)),F(3,50)),
      ('E18 negative forward',lambda:m.forward_between(1,2,1,math.exp(.02)),F(-1,50)),
      ('E35 parallel-zero-bump price',lambda:m.price_cashflows(flows,times,[x+.0001 for x in rates]),bumped),
      ('F167 integer cashflow cancellation',lambda:m.price_cashflows([(1,-10**18),(1,10**18+1)],[1,2],[0,0]),1),
      ('F167 cashflow accumulation avoids overflow',lambda:m.price_cashflows([(1,1e308),(1,1e308),(1,-1e308),(1,-1e308),(1,1)],[1,2],[0,0]),1),
      ('F167 discount underflow offset before PV reporting',lambda:m.price_cashflows([(1,1e308)],[1,2],[800,800]),coupled),
      ('F167 log-node products cancel before exponential',lambda:m.log_discount_curve([1e308,1.5e308],[1.5e308,-1e308],1.25e308),1),
      ('F167 finite two-year bootstrap despite denominator overflow',lambda:m.bootstrap_two_year_df(1e308,1e308,1e308,.5),F(1,4)),
      ('F167 bootstrap integer numerator retained',lambda:m.bootstrap_two_year_df(10**18+1,10**18,1,1),F(1,10**18+1)),
      ('F167 exact-ratio tiny forward',lambda:m.forward_between(1,2,10**18+1,10**18),tinyforward),
      ('F167 huge forward ratio',lambda:m.forward_between(1,2,1e308,1e-308),bigforward),
    ]:num(label,fn,want)
    # Roundtrip through explicit zero nodes is a local source API chain, not a
    # general instrument bootstrap or proof that float DF/zero conversions exact.
    zeros=[m.zero_from_discount(1,boot1),m.zero_from_discount(2,boot2)]
    num('local bootstrap-zero-price chain',lambda:m.price_cashflows(flows,[1,2],zeros),100,atol=1e-12,rtol=0)
    ck('parallel upward zero shift decreases positive-CF PV',m.price_cashflows(flows,times,[x+.0001 for x in rates])<m.price_cashflows(flows,times,rates),scope='direct zero-node shift, NOT market-quote bootstrap DV01')
    for label,fn in [
      ('malformed curve',lambda:m.validate(None,None)),
      ('huge integer input',lambda:m.discount_from_zero(10**1000,.05)),
      ('DF underflow rejects',lambda:m.discount_from_zero(1,1000)),
      ('DF overflow rejects',lambda:m.discount_from_zero(1,-1000)),
      ('unreportable zero rate',lambda:m.zero_from_discount(5e-324,1e-308)),
      ('one-year ratio underflow rejects',lambda:m.bootstrap_one_year_df(1e-308,1e308)),
      ('generator policy explicit',lambda:m.price_cashflows((x for x in flows),times,rates)),
      ('empty generator policy explicit',lambda:m.price_cashflows(iter(()),times,rates)),
      ('malformed cashflow record',lambda:m.price_cashflows([(1,2,3)],times,rates)),
      ('boolean cashflow time',lambda:m.price_cashflows([(True,5)],times,rates)),
      ('unreportable PV',lambda:m.price_cashflows([(1,1e-308)],[1,2],[800,800])),
      ('negative discount',lambda:m.zero_from_discount(2,-.9)),
      ('out-of-domain cashflow',lambda:m.price_cashflows([(4,5)],times,rates)),
      ('negative tenor',lambda:m.discount_from_zero(-1,.05)),
      ('duplicate curve tenor',lambda:m.log_discount_curve([1,1],[.04,.05],1)),
      ('unsorted tenor',lambda:m.log_discount_curve([2,1],[.05,.04],1.5)),
      ('negative bootstrap discount',lambda:m.bootstrap_two_year_df(1,5,100,.95)),
      ('nonpositive face',lambda:m.bootstrap_one_year_df(95,0)),
    ]:reject('F167 '+label,fn)
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,acceptance_control_records=12,historical_unique_methods_added=0,model=dict(tenors=times,continuous_zero_rates=rates,cashflows=flows,bootstrap=dict(zero_price=95,face=100,coupon_price=100,coupon=5,df1=boot1,df2=boot2),units='years, continuous annual zero/forward rates, fictional common currency and dimensionless DFs',timing='annual coupon dates only; no actual valuation/settlement/calendars/market close'),scipy_secondary_stdout=capture.getvalue())
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
