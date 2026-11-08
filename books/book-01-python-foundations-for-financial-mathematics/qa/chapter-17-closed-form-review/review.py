"""Closed-form lab and independent rational/Decimal scale benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-17/17.02-closed-form-vs-numerical-solutions.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-17/17.02-closed-form-vs-numerical-solutions.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1702-') as tmp:
        Path(tmp,'closed_form_vs_numerical_solutions.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['closed_form_vs_numerical_solutions.py']),('isolated import',['-c','import closed_form_vs_numerical_solutions']),('exact compilation',['-m','compileall','-q','closed_form_vs_numerical_solutions.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['closed_form_vs_numerical_solutions.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    for label,fn,want in [
      ('E1 source future value',lambda:m.future_value(100,.1,2),121),
      ('E2 source inverse rate',lambda:m.implied_rate(100,121,2),F(1,10)),
      ('E4 source zero-rate annuity',lambda:m.annuity_pv(100,0,5),500),
      ('F159 tiny implied rate from integer amounts',lambda:m.implied_rate(10**18,10**18+1,1),F(1,10**18)),
      ('F159 extreme ratio implied rate finite',lambda:m.implied_rate(1e-308,1e308,2),1e308),
      ('F159 future value avoids power overflow',lambda:m.future_value(1e-308,1,1024),F(2**1024,10**308)),
      ('F159 zero principal avoids irrelevant power overflow',lambda:m.future_value(0,1,1024),0),
      ('F159 tiny NPV retained',lambda:m.npv(1e-308,[-1,1]),F(-1,10**308)),
      ('F159 NPV avoids power overflow',lambda:m.npv(1e308,[0,0,1e308]),F(1,10**308)),
      ('F159 quadrature finite after accumulation',lambda:m.trapezoid(lambda x:1e308,0,1,2),1e308),
      ('F159 wide-bracket midpoint stable',lambda:m.bisect(lambda x:x/1e308,-1e308,1e308),0),
    ]:num(label,fn,want)
    single_irr=m.irr([-100,110]);ck('E8 source single IRR',abs(F(str(single_irr))-F(1,10))<=F(1,10**12),actual=single_irr,independent_reference='1/10',absolute_rate_tolerance='1e-12')
    close('E3 supplemental discount inverse',F(121)/(F(11,10)**2),100)
    annuity=sum(F(100)/(F(21,20)**i) for i in range(1,6));closed=m.annuity_pv(100,.05,5);summed=m.annuity_pv_sum(100,.05,5)
    close('E5 exact rational annuity expectation',closed,annuity);close('E6 independent direct sum expectation',summed,annuity)
    extra_annuity=[]
    for rate,n in [(1e-12,5),(-.5,1100),(1e308,5)]:
      payment=1e-308 if rate<0 else (1e308 if rate>1 else 100)
      expected=F(str(payment))*sum((1+F(str(rate)))**(-i) for i in range(1,n+1))
      for name in ['annuity_pv','annuity_pv_sum']:num('source annuity '+name+' '+str((rate,n)),lambda name=name,rate=rate,n=n,payment=payment:getattr(m,name)(payment,rate,n),expected)
      try:extra_annuity.append(dict(payment=payment,rate=rate,periods=n,closed=m.annuity_pv(payment,rate,n),direct=m.annuity_pv_sum(payment,rate,n)))
      except Exception as e:extra_annuity.append(dict(rate=rate,periods=n,error=repr(e)))
    for rate in [.1,.2]:ck('E7/E12 original NPV substitution '+str(rate),abs(m.npv(rate,[-100,230,-132]))<=1e-12,actual=m.npv(rate,[-100,230,-132]),absolute_dollar_tolerance=1e-12)
    irrs=[]
    for a,b,want in [(.05,.15,F(1,10)),(.15,.25,F(1,5))]:
      r=m.irr([-100,230,-132],a,b);ck('lab separate bracket '+str((a,b)),abs(F(str(r))-want)<=F(1,10**12),actual=r,reference=str(want));irrs.append(r)
    quadratic=[]
    for a,b,c,expected in [(1,-3,2,[1,2]),(1e200,-3e200,2e200,[1,2]),(1e-200,-3e-200,2e-200,[1,2]),(1,1e308,1,[-1e308,-1e-308]),(1,-1e16,1,[1e-16,1e16])]:
      try:roots=sorted(m.quadratic(a,b,c))
      except Exception as e:ck('source quadratic scale '+str(a)+','+str(b),False,exception=repr(e))
      else:
        for i,want in enumerate(expected):close('source quadratic root '+str((a,b,i)),roots[i],want)
        quadratic.append(dict(coefficients=[a,b,c],roots=roots))
    num('quadratic zero-linear coefficient negative root',lambda:min(m.quadratic(1,0,-1)),-1)
    num('quadratic zero-linear coefficient positive root',lambda:max(m.quadratic(1,0,-1)),1)
    ck('quadratic repeated root',m.quadratic(1,-2,1)==(1,1))
    sqrt2_estimate=m.bisect(lambda x:x*x-2,0,2);ck('lab numerical sqrt2 independent error',abs(D(str(sqrt2_estimate))-D(2).sqrt())<D('1e-12'),actual=sqrt2_estimate,reference='sqrt(2)')
    close('E14 supplemental midpoint',F(0+2,2),1);close('E15 supplemental ten-halving width',F(2,2**10),F(1,512));close('E18 supplemental Newton step',1-F(-1,2),F(3,2))
    integrals=[]
    for n in [10,20]:
      value=m.trapezoid(lambda x:x*x,0,1,n);close('E22/E23 finite trapezoid '+str(n),value,F(1,3)+F(1,6*n*n));integrals.append(value)
    num('E20/E21 source linear integral',lambda:m.trapezoid(lambda x:x,0,1,10),F(1,2))
    ck('quadrature error shrinks by factor four',math.isclose((integrals[0]-1/3)/(integrals[1]-1/3),4,rel_tol=1e-10))
    close('E26 supplemental portfolio variance',F(1,4)*F(1,25)+F(1,4)*F(9,100),F(13,400))
    ck('E33 float example remains approximate',.1+.2!=.3 and math.isclose(.1+.2,.3,rel_tol=1e-12),scope='binary-float demonstration, not a source financial-result policy claim')
    for label,fn in [
      ('E11 no real roots rejects',lambda:m.quadratic(1,0,1)),
      ('F159 tiny negative discriminant not erased',lambda:m.quadratic(1e-200,0,1e-200)),
      ('F159 future-value underflow rejected',lambda:m.future_value(1e-300,-.5,100)),
      ('F159 covariance-like quadratic unreportable root rejected',lambda:m.quadratic(1e-308,1e308,1)),
      ('F159 zero-cashflow IRR nonidentifiable',lambda:m.irr([0,0,0])),
      ('F159 huge integer input ValueError',lambda:m.implied_rate(10**1000,1,1)),
      ('F159 finite callback bool only rejected',lambda:m.bisect(lambda x:False,0,1)),
      ('F159 unreportable quadrature rejected',lambda:m.trapezoid(lambda x:1e-300,0,1e-300,2)),
      ('E17 bad bracket rejected',lambda:m.bisect(lambda x:x*x+1,-1,1)),
      ('invalid rate rejected',lambda:m.npv(-1,[-100,110])),
      ('invalid periods rejected',lambda:m.annuity_pv(100,.1,True)),
    ]:reject(label,fn)
    try:result=m.bisect(lambda x:x*x-2,1,2,1e-30,200)
    except RuntimeError as e:ck('F159 exhausted coordinates report failure',True,exception=repr(e))
    except Exception as e:ck('F159 exhausted coordinates report failure',False,exception=repr(e))
    else:ck('F159 exhausted coordinates report failure',False,actual=result)
    project=dict(cashflows=[-100,110],principal=100,future=121,periods=2,annuity_payment=100,annuity_rate=.05,annuity_periods=5,annuity_closed=closed,annuity_direct=summed,other_annuity_cases=extra_annuity,multiple_irr=irrs,quadratics=quadratic,quadratic_integrals=integrals,
      units='fictional USD principal/period-end payments; dimensionless periodic rates',timing='equally spaced periods, initial t0 and end-of-period future flows',dates=None,scope='standard-library benchmarks, no actual market calibration or SciPy backend',fixture_sha256=hashlib.sha256(json.dumps([100,121,2,100,.05,5,[-100,230,-132]]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,project_report=project)
    def sanitize(value):
      if isinstance(value,float) and not math.isfinite(value):return repr(value)
      if isinstance(value,dict):return {k:sanitize(v) for k,v in value.items()}
      if isinstance(value,(list,tuple)):return [sanitize(v) for v in value]
      return value
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(sanitize(out),indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
