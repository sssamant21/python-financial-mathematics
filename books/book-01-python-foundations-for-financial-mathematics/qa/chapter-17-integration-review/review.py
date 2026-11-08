"""Exact-source quadrature lab; independent finite-grid and analytic oracles."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.08-numerical-integration.md';source=BOOK/path
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
    with tempfile.TemporaryDirectory(prefix='book1-1708-') as tmp:
        Path(tmp,'numerical_integration.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and twelve tests',['numerical_integration.py']),('silent import',['-c','import numerical_integration']),('compile exact listing',['-m','compileall','-q','numerical_integration.py']),('exact SciPy quad snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            else:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        ns={};exec(compile(blocks[0],'exact_scipy_snippet','exec'),ns)
        with localcontext() as ctx:ctx.prec=100;cash= D(2000)*(1-D('-.1').exp())
        num('SciPy polynomial independent oracle',lambda:ns['value'],F(1,3))
        num('SciPy cashflow independent Decimal oracle',lambda:ns['pv'],cash)
    m=types.ModuleType('integration_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    lab=[]
    for n in [2,10,100]:
        row=dict(panels=n)
        for name,want in [('midpoint',F(1,3)-F(1,12*n*n)),('trapezoid',F(1,3)+F(1,6*n*n)),('simpson',F(1,3))]:
            value=getattr(m,name)(lambda x:x*x,0,1,n);row[name]=value;num('lab x squared finite-grid '+name+' '+str(n),lambda value=value:value,want)
        lab.append(row)
    for label,fn,want in [
      ('E1 constant integral',lambda:m.simpson(lambda x:1,0,3,10),3),
      ('E2 E6 midpoint linear',lambda:m.midpoint(lambda x:x,0,1,1),F(1,2)),
      ('E7 trapezoid linear',lambda:m.trapezoid(lambda x:x,0,1,1),F(1,2)),
      ('E4 E16 cubic Simpson',lambda:m.simpson(lambda x:x**3,0,1,10),F(1,4)),
      ('E25 supplemental uniform variance',lambda:F(1,3)-F(1,4),F(1,12)),
      ('E26 uniform payoff',lambda:m.discounted_payoff_expectation(lambda x:max(x-.5,0),lambda x:1,0,1,1000),F(1,8)),
      ('E28 zero-rate cashflow',lambda:m.discounted_continuous_cashflow(0,2,100),200),
      ('E31 cashflow PV',lambda:m.discounted_continuous_cashflow(.05,2,100),cash),
      ('F165 discounted helper actually discounts',lambda:m.discounted_payoff_expectation(lambda x:max(x-.5,0),lambda x:1,0,1,1000,rate=.05,horizon=2),D('-.1').exp()/8),
      ('F165 tiny horizon integrated before report',lambda:m.simpson(lambda x:1e308,0,1e-308,10),1),
      ('F165 paired payoff-density before quadrature',lambda:m.discounted_payoff_expectation(lambda x:1e308,lambda x:1e308,0,1e-308,10),1e308),
      ('F165 zero cashflow avoids irrelevant exponential overflow',lambda:m.discounted_continuous_cashflow(-1e308,2,0,10),0),
    ]:num(label,fn,want)
    for name in ['midpoint','trapezoid','simpson']:
        num('F165 '+name+' finite large sum',lambda name=name:getattr(m,name)(lambda x:1e308,0,1,10),1e308)
        num('F165 '+name+' wide-span constant',lambda name=name:getattr(m,name)(lambda x:1e-308,-1e308,1e308,10),2)
    for n in [10,20]:num('E15 quartic Simpson finite-grid '+str(n),lambda n=n:m.simpson(lambda x:x**4,0,1,n),F(1,5)+F(2,15*n**4))
    num('E20 Phi zero',lambda:m.normal_cdf_integrated(0),F(1,2))
    num('E22 normal density zero',lambda:m.normal_pdf(0),D('0.398942280401432677939946059934381868475858631164934657'))
    for z in [-1,1]:num('lab normal CDF '+str(z),lambda z=z:m.normal_cdf_integrated(z),.5*math.erfc(-z/math.sqrt(2)),atol=1e-10,rtol=0)
    num('E21 CDF symmetry',lambda:m.normal_cdf_integrated(-1)+m.normal_cdf_integrated(1),1)
    ck('E36 normal excluded tails quantified',math.isclose(math.erfc(3/math.sqrt(2)),.00269979606326019,rel_tol=1e-12),excluded_mass=math.erfc(3/math.sqrt(2)),scope='supplemental erfc tail oracle; not infinite-domain quadrature')
    # Independent finite Simpson geometric series, NOT the limiting integral.
    with localcontext() as ctx:
        ctx.prec=100;n=1000;q=D('.8').exp()
        finite_pv=D('1e-308')*D('.002')/3*(1+q**n+4*q*(q**n-1)/(q*q-1)+2*q*q*(q**(n-2)-1)/(q*q-1))
    num('F165 negative-rate cashflow finite-grid expectation',lambda:m.discounted_continuous_cashflow(-400,2,1e-308,1000),finite_pv)
    for label,fn in [
      ('odd Simpson panels',lambda:m.simpson(lambda x:x,0,1,3)),
      ('reversed bounds',lambda:m.midpoint(lambda x:x,1,0,10)),
      ('nonfinite integrand',lambda:m.trapezoid(lambda x:float('nan'),0,1,2)),
      ('repeated trapezoid grid',lambda:m.trapezoid(lambda x:x,1,math.nextafter(1,2),2)),
      ('midpoint not representable',lambda:m.midpoint(lambda x:x,1,math.nextafter(1,2),1)),
      ('huge integer bound',lambda:m.simpson(lambda x:x,0,10**1000,2)),
      ('huge integer callback',lambda:m.simpson(lambda x:10**1000,0,1,2)),
      ('underflowed nonzero integral',lambda:m.simpson(lambda x:1e-308,0,1e-308,2)),
      ('normal PDF boolean',lambda:m.normal_pdf(True)),
      ('normal CDF panels validated at zero',lambda:m.normal_cdf_integrated(0,3)),
      ('normal CDF extreme domain disclosed',lambda:m.normal_cdf_integrated(9)),
      ('negative payoff density',lambda:m.discounted_payoff_expectation(lambda x:1,lambda x:-1,0,1,10)),
      ('boolean payoff',lambda:m.discounted_payoff_expectation(lambda x:True,lambda x:1,0,1,10)),
    ]:reject('F165 '+label,fn)
    reject('F165 cashflow integer horizon retains coordinate contract',lambda:m.discounted_continuous_cashflow(0,10**18+1,1,2))
    import scipy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,lab_results=lab,model=dict(domain=[0,1],panels=[2,10,100],cashflow=dict(rate=.05,horizon=2,annual_intensity=100),units='years, fictional currency/year cashflow, continuous rate/year; probability/payoff units explicit',timing='continuous payment on[0,2]; uniform terminal payoff atT=2 only when discount requested',normal_reference='math.erfc independent tail algorithm, not same quadrature implementation'))
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
