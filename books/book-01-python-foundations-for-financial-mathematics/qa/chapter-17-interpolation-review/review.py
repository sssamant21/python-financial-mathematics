"""Exact-source interpolation runs; independent rational/Decimal curve oracles."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.09-interpolation.md';source=BOOK/path
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
    with tempfile.TemporaryDirectory(prefix='book1-1709-') as tmp:
        Path(tmp,'interpolation.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and twelve tests',['interpolation.py']),('silent import',['-c','import interpolation']),('compile exact listing',['-m','compileall','-q','interpolation.py']),('exact SciPy interpolation snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label!='exact SciPy interpolation snippet':ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        import contextlib,io
        ns={};capture=io.StringIO()
        with contextlib.redirect_stdout(capture):exec(compile(blocks[0],'exact_scipy_snippet','exec'),ns)
        # On this knot interval the PCHIP endpoint slopes are1/200 and9/2600.
        # Hermite midpoint is(y1+y2)/2+h*(m1-m2)/8=31/650.
        num('SciPy PCHIP independent Hermite midpoint',lambda:float(ns['pchip'](2.5)),F(31,650))
        # Not-a-knot with four knots reproduces the unique global cubic here.
        knot_x=list(map(F,[1,2,3,5]));knot_y=list(map(F,['.04','.045','.05','.055']));lagrange=F(0)
        for i in range(4):
            term=knot_y[i]
            for j in range(4):
                if i!=j:term*=(F(5,2)-knot_x[j])/(knot_x[i]-knot_x[j])
            lagrange+=term
        num('SciPy spline independent cubic midpoint',lambda:float(ns['spline'](2.5)),lagrange)
        with localcontext() as ctx:ctx.prec=100;want=D('-.12').exp()
        num('SciPy log-discount independent midpoint',lambda:float(ns['np'].exp(ns['log_df_at_2_5'])),want)
        sampled=[float(ns['pchip'](x/10)) for x in range(10,51)]
        ck('SciPy sampled shape and domain',all(a<=b for a,b in zip(sampled,sampled[1:])) and math.isnan(float(ns['pchip'](6))) and math.isnan(float(ns['spline'](6))),second_exact_stdout=capture.getvalue(),scope='finite monotone-rate sample, not arbitrary curve/arbitrage proof')
    m=types.ModuleType('interpolation_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    for label,fn,want in [
      ('E1 linear midpoint',lambda:m.linear_interpolate([1,3],[2,6],2),4),
      ('E3 left endpoint',lambda:m.linear_interpolate([1,3],[2,6],1),2),
      ('E4 right endpoint',lambda:m.linear_interpolate([1,3],[2,6],3),6),
      ('E5 explicit extrapolation',lambda:m.linear_interpolate([1,3],[2,6],4,True),8),
      ('E16 linearly interpolated zero',lambda:m.linear_interpolate([1,3],[.04,.06],2),F(1,20)),
      ('E19 geometric log-discount midpoint',lambda:m.log_discount_interpolate([1,3],[.9,.81],2),D('.729').sqrt()),
      ('F166 wide x span',lambda:m.linear_interpolate([-1e308,1e308],[0,2],0),1),
      ('F166 wide y difference',lambda:m.linear_interpolate([0,1],[-1e308,1e308],.5),0),
      ('F166 huge constant ordinate',lambda:m.linear_interpolate([0,1],[1e308,1e308],.5),1e308),
      ('F166 integer ordinate cancellation',lambda:m.linear_interpolate([0,2],[-10**18,10**18+2],1),1),
      ('F166 exact integer coordinates',lambda:m.linear_interpolate([10**18,10**18+2],[0,2],10**18+1),1),
    ]:num(label,fn,want)
    # Exact knot identity is tested without float coercion of the expected integer.
    ck('F166 exact integer right knot preserved',m.linear_interpolate([0,1],[0,10**18+1],1)==10**18+1)
    ck('F166 supplied log-DF knot preserved',m.log_discount_interpolate([1,2],[.9,.81],1)==.9)
    with localcontext() as ctx:
        ctx.prec=400
        ratio=(D(10**18+1)/D(10**18)).ln()
        large_forward=(D('1e616')).ln()
        df=D('-.1').exp();log_mid=D('-.11').exp();forward=D('.055')
    num('F166 tiny integer-ratio forward',lambda:m.forward_rate(10**18+1,10**18,1,2),ratio)
    num('F166 huge ratio forward',lambda:m.forward_rate(1e308,1e-308,1,2),large_forward)
    num('F166 tiny ratio forward',lambda:m.forward_rate(1e-308,1e308,1,2),-large_forward)
    num('E18 source zero recovery',lambda:m.continuous_zero_rate(float(df),2),F(1,20))
    tenors=[1,2,3];zeros=[.04,.05,.06];discounts=[math.exp(-t*z) for t,z in zip(tenors,zeros)]
    num('lab zero-versus-log representation',lambda:m.log_discount_interpolate([1,3],[math.exp(-.04),math.exp(-.18)],2),log_mid)
    num('lab three-node log DF at2.5',lambda:m.log_discount_interpolate(tenors,discounts,2.5),D('-.14').exp())
    num('lab three-node zero at2.5',lambda:m.continuous_zero_rate(m.log_discount_interpolate(tenors,discounts,2.5),2.5),F(7,125))
    num('F166 huge-tenor close-query forward retained',lambda:m.piecewise_forward([0,1e308],[.9,.8],0,1e-308),D('1.125').ln()/D('1e308'))
    num('lab source piecewise forward',lambda:m.piecewise_forward(tenors,discounts,1,3),F(7,100))
    num('E21 interval forward',lambda:m.forward_rate(math.exp(-.05),math.exp(-.1),1,2),F(1,20))
    num('E22 E25 negative forward permitted',lambda:m.forward_rate(1,math.exp(.02),0,1),F(-1,50))
    num('F166 close-query piecewise forward retained',lambda:m.piecewise_forward([1,2],[10**18+1,10**18],1,1.000000000001),ratio)
    num('E29 supplemental coupon PV',lambda:F(5)*F(9,10)+F(105)*F(81,100),F(1791,20))
    for label,fn in [
      ('default extrapolation rejects',lambda:m.linear_interpolate([1,3],[2,6],4)),
      ('duplicate nodes',lambda:m.linear_interpolate([1,1],[2,3],1)),
      ('unsorted nodes',lambda:m.linear_interpolate([3,1],[6,2],2)),
      ('shape rejected',lambda:m.validate_nodes(None,None)),
      ('huge integer invalid finite range',lambda:m.linear_interpolate([0,10**1000],[0,1],1)),
      ('nonboolean extrapolation policy',lambda:m.linear_interpolate([1,3],[2,6],4,1)),
      ('unreportable nonzero linear value',lambda:m.linear_interpolate([0,1],[0,5e-324],.1)),
      ('unreportable extrapolation',lambda:m.linear_interpolate([0,1],[0,1e308],2,True)),
      ('unreportable forward',lambda:m.forward_rate(1e308,1e-308,0,5e-324)),
      ('piecewise query typed',lambda:m.piecewise_forward([1,2],[.9,.8],True,2)),
      ('piecewise validates empty curve first',lambda:m.piecewise_forward([],[],1,2)),
      ('nonpositive DF',lambda:m.log_discount_interpolate([1,2],[.9,0],1.5)),
      ('negative curve tenor',lambda:m.log_discount_interpolate([-1,2],[.9,.8],1)),
      ('zero rate at zero maturity',lambda:m.continuous_zero_rate(.9,0)),
      ('out-of-domain piecewise forward',lambda:m.piecewise_forward([1,2],[.9,.8],.5,1.5)),
    ]:reject('F166 '+label,fn)
    import scipy,numpy
    out=dict(python=platform.python_version(),platform=platform.platform(),numpy=numpy.__version__,scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,model=dict(tenors=tenors,continuous_zero_rates=zeros,discounts=discounts,units='years, continuous annual zero/forward rates, dimensionless discount factors',timing='fictional curve, no market/as-of calendar or day-count calibration',representation_comparison=dict(linear_zero_DF=str(df),log_discount_DF=str(log_mid))))
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
