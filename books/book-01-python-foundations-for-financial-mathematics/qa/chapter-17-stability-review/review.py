"""Exact stability examples and reference; independent rational/Decimal oracles."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.11-numerical-stability.md';source=BOOK/path
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
    with tempfile.TemporaryDirectory(prefix='book1-1711-') as tmp:
        Path(tmp,'numerical_stability.py').write_bytes(code)
        selected=[('epsilon example',blocks[0],{}),('summation example',blocks[1],{}),('log-return contextual example',blocks[2],{'P0':100,'P1':101}),('SciPy stability snippet',blocks[3],{})]
        tasks=[('exact demonstration and twelve tests',['numerical_stability.py']),('silent import',['-c','import numerical_stability']),('compile exact listing',['-m','compileall','-q','numerical_stability.py'])]
        for i,(label,block,bindings) in enumerate(selected):
            filename='example_'+str(i)+'.py';Path(tmp,filename).write_bytes(block)
            # Contextual fragment gets only its explicitly required two bindings.
            args=[filename] if not bindings else ['-c',f'exec(compile(open({filename!r}).read(),{filename!r},"exec"),{bindings!r})']
            tasks.append((label,args))
        for label,args in tasks:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            elif label in ['silent import','compile exact listing']:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        ns={};exec(compile(blocks[3],'exact_scipy_snippet','exec'),ns)
        num('SciPy linear solve component0',lambda:float(ns['x'][0]),F(1,11))
        num('SciPy linear solve component1',lambda:float(ns['x'][1]),F(7,11))
        num('SciPy survival at8 independent erfc oracle',lambda:float(ns['tail']),.5*math.erfc(8/math.sqrt(2)),rtol=1e-12)
        num('SciPy logsumexp independent log2',lambda:float(ns['logsumexp'](ns['values'])),1000+math.log(2))
    m=types.ModuleType('stability_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    with localcontext() as ctx:
        ctx.prec=1000
        annuity=D(2000)*(1-D('-.1').exp());tiny_annuity=D(100)*(1-(-D('1e-12')*2).exp())/D('1e-12')
        negative_annuity=D('1e-308')*(D(1000).exp()-1)/1000
        log_up=D('1e616').ln();log_down=-log_up;growth=(D('1.01')**12)
        small_lse=(1+D(-40).exp()).ln()
    for label,fn,want in [
      ('E8 zero annuity',lambda:m.continuous_annuity(0,2,100),200),
      ('E9 positive annuity',lambda:m.continuous_annuity(.05,2,100),annuity),
      ('lab tiny-rate annuity',lambda:m.continuous_annuity(1e-12,2,100),tiny_annuity),
      ('E10 log return',lambda:m.stable_log_return(100,101),D('1.01').ln()),
      ('E12 compound',lambda:m.stable_compound(.01,12),growth),
      ('E13 NPV known zero',lambda:m.npv([-100,110],.1),0),
      ('E17 logsumexp',lambda:m.log_sum_exp([1000,1000]),1000+math.log(2)),
      ('F168 scaled annuity avoids tiny product loss',lambda:m.continuous_annuity(1e-308,1e-308,1e308),1),
      ('F168 annuity exponential overflow avoided',lambda:m.continuous_annuity(-1000,1,1e-308),negative_annuity),
      ('F168 zero intensity avoids irrelevant overflow',lambda:m.continuous_annuity(-1000,1,0),0),
      ('F168 log return huge ratio',lambda:m.stable_log_return(1e-308,1e308),log_up),
      ('F168 log return tiny ratio',lambda:m.stable_log_return(1e308,1e-308),log_down),
      ('F168 finite sum despite intermediate overflow',lambda:m.stable_sum([1e308,1e308,-1e308,-1e308,1]),1),
      ('F168 integer NPV difference retained',lambda:m.npv([-10**18,10**18+1],0),1),
      ('F168 tiny NPV rate retained',lambda:m.npv([-1,1],1e-308),F(-1,10**308)),
      ('F168 discounted flow before exponential underflow',lambda:m.npv([0,0,1e308],1e308),F(1,10**308)),
      ('F168 logsumexp small positive correction',lambda:m.log_sum_exp([0,-40]),small_lse),
      ('zero periods compound',lambda:m.stable_compound(.01,0),1),
      ('zero tenor annuity',lambda:m.continuous_annuity(-1000,0,100),0),
    ]:num(label,fn,want,atol=1e-12 if label=='E13 NPV known zero' else 0)
    for scale in [1,1e200,1e-200]:
        for idx,want in enumerate([1,2]):num('F168 scaled quadratic '+str((scale,idx)),lambda scale=scale,idx=idx:sorted(m.quadratic_real_roots(scale,-3*scale,2*scale))[idx],want)
    for idx,want in enumerate([-1e308,-1e-308]):num('F168 large linear coefficient quadratic '+str(idx),lambda idx=idx:sorted(m.quadratic_real_roots(1,1e308,1))[idx],want)
    num('quadratic repeated root',lambda:m.quadratic_real_roots(1,-2,1)[0],1)
    num('quadratic b-zero branch',lambda:min(m.quadratic_real_roots(1,0,-1)),-1)
    num('E3 stable sum',lambda:m.stable_sum([1e16,1,-1e16]),1)
    num('residual absolute value',lambda:m.residual(lambda x:x*x-4,1),3)
    ck('E1 binary64 spacing observation',sys.float_info.epsilon==2**-52,epsilon=sys.float_info.epsilon,scope='recorded runtime, not cross-platform acceptance')
    ck('E2 nonassociative operations',((1e16+1.0)-1e16)==0.0)
    x=1e-16
    ck('E4 E5 small increment log example',math.log(1+x)==0 and math.log1p(x)>0,naive=math.log(1+x),stable=math.log1p(x))
    ck('E6 expm1 example',math.exp(x)-1==0 and math.expm1(x)>0,naive=math.exp(x)-1,stable=math.expm1(x))
    naive_small=(1e8-math.sqrt(1e16-4))/2
    ck('E27 naive quadratic cancellation observed',abs(naive_small-1e-8)>1e-10,naive_small_root=naive_small,scope='contrast demonstration; source roots checked independently above')
    for label,fn in [
      ('discount underflow',lambda:m.stable_discount(1000,1)),
      ('discount overflow',lambda:m.stable_discount(-1000,1)),
      ('compound underflow',lambda:m.stable_compound(-.5,2000)),
      ('compound overflow',lambda:m.stable_compound(1,2000)),
      ('annuity underflow',lambda:m.continuous_annuity(0,1e-308,1e-308)),
      ('negative tiny discriminant',lambda:m.quadratic_real_roots(1e-200,0,1e-200)),
      ('huge integer finite-range check',lambda:m.stable_discount(10**1000,1)),
      ('noncallable residual',lambda:m.residual(None,1)),
      ('boolean residual coordinate',lambda:m.residual(lambda x:0,True)),
      ('unreportable positive logsumexp',lambda:m.log_sum_exp([0,-1000])),
      ('nonfinite sum',lambda:m.stable_sum([float('nan')])),
      ('invalid NPV rate',lambda:m.npv([1],-1)),
      ('empty NPV',lambda:m.npv([],.1)),
    ]:reject('F168 '+label,fn)
    reject('F168 Decimal exponential underflow guarded',lambda:m.stable_discount(1e308,1))
    reject('F168 enormous-period compound underflow guarded',lambda:m.stable_compound(-.5,10**1000))
    import numpy,scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),numpy=numpy.__version__,scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,observations=dict(sum_builtin=sum([1e16,1,-1e16]),sum_fsum=math.fsum([1e16,1,-1e16]),epsilon=sys.float_info.epsilon,context_fragment_bindings={'P0':100,'P1':101}),model=dict(cashflows=[-100,110],periodic_rate=.1,continuous_annuity=dict(rate=.05,tenor=2,intensity=100),units='fictional currency/intensity per year, compatible periodic returns and continuous annual rates',timing='periodic t0/t1 and separate continuous payments; no market inputs'))
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
