"""Exact-source box-constrained GMV lab and independent rational KKT checks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-17/17.06-constrained-optimization.md';source=BOOK/path
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
    with tempfile.TemporaryDirectory(prefix='book1-1706-') as tmp:
        Path(tmp,'constrained_optimization.py').write_bytes(code);Path(tmp,'scipy_example.py').write_bytes(blocks[0])
        for label,args in [('exact demonstration and twelve tests',['constrained_optimization.py']),('silent import',['-c','import constrained_optimization']),('compile exact listing',['-m','compileall','-q','constrained_optimization.py']),('exact SciPy SLSQP snippet',['scipy_example.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            ok=p.returncode==0
            if label=='exact demonstration and twelve tests':ok=ok and methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            else:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
        ns={};exec(compile(blocks[0],'exact_scipy_snippet','exec'),ns);v=ns['result'];wa,wb=map(float,v.x)
        num('SciPy analytic cap weight A',lambda:wa,F(2,5),atol=1e-8,rtol=0)
        num('SciPy analytic cap weight B',lambda:wb,F(3,5),atol=1e-8,rtol=0)
        num('SciPy independent objective',lambda:F(str(wa))**2*F(1,25)+F(str(wb))**2*F(9,100),F(97,2500),atol=1e-9,rtol=0)
        ck('SciPy independent bounds and budget',-1e-8<=wa<=.4+1e-8 and -1e-8<=wb<=1+1e-8 and abs(wa+wb-1)<1e-8,weights=[wa,wb])
    m=types.ModuleType('constrained_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    for args,want in [((),(0,1)),((.4,1),(0,.4)),((1,.6),(.4,1)),((.6,.7,.2,.1),(.3,.6))]:
        for i in [0,1]:num('interval '+str(args)+' '+str(i),lambda args=args,i=i:m.feasible_interval(*args)[i],F(str(want[i])))
    free=m.constrained_two_asset_gmv(.04,.09,0);capped=m.constrained_two_asset_gmv(.04,.09,0,cap_a=.4)
    num('E12 free weight',lambda:free['weight_a'],F(9,13));num('E15 free risk',lambda:free['variance'],F(9,325))
    num('E13 cap weight',lambda:capped['weight_a'],F(2,5));num('E14 cap risk',lambda:capped['variance'],F(97,2500))
    num('lab objective cost of cap',lambda:F(str(capped['variance']))-F(9,325),F(361,32500))
    for w in [.3,.4,.5]:
        sl=m.constraint_residuals(w,.4,1)
        num('E19 E20 cap slack '+str(w),lambda sl=sl:sl['a_max_slack'],F(2,5)-F(str(w)))
        num('budget identity '+str(w),lambda sl=sl:sl['budget'],0,atol=1e-15,rtol=0)
    r=m.grid_solve(lambda w:m.variance(w,.04,.09,0),0,.4,1000)
    num('lab grid winner',lambda:r['x'],F(2,5));num('lab grid risk',lambda:r['value'],F(97,2500));num('lab grid spacing',lambda:r['grid_spacing'],F(1,2500))
    for scale in [1e-200,1e200]:
        num('F163 scale-invariant weight '+str(scale),lambda scale=scale:m.constrained_two_asset_gmv(4*scale,9*scale,0)['weight_a'],F(9,13))
    num('F163 large risk cancellation',lambda:m.variance(.5,1e308,1e308,-1e308),0)
    num('F163 tiny positive risk retained',lambda:m.variance(.5,4e-200,9e-200,0),F(13,4*10**200))
    num('F163 wide grid',lambda:m.grid_solve(lambda x:abs(x),-1e308,1e308,2)['x'],0)
    num('F163 integer objective ordering',lambda:m.grid_solve(lambda x:10**18+int((x-1)**2),0,2,2)['x'],1)
    singleton=m.constrained_two_asset_gmv(.04,.04,.04,cap_a=.4,min_a=.4)
    ck('F163 singleton feasible set is unique',singleton['nonunique'] is False,result=singleton)
    ck('constant objective interval remains nonunique',m.constrained_two_asset_gmv(.04,.04,.04)['nonunique'] is True)
    for label,fn,kind in [
      ('small actual infeasibility',lambda:m.feasible_interval(.5,.4999999999999),ValueError),
      ('two 40 percent caps',lambda:m.feasible_interval(.4,.4),ValueError),
      ('inverted asset bounds',lambda:m.feasible_interval(.3,1,min_a=.5),ValueError),
      ('tiny invalid covariance',lambda:m.constrained_two_asset_gmv(1e-200,1e-200,2e-200),ValueError),
      ('large invalid covariance',lambda:m.constrained_two_asset_gmv(1e200,1e200,2e200),ValueError),
      ('variance export validates covariance',lambda:m.variance(.5,.04,.09,.1),ValueError),
      ('variance export validates weight',lambda:m.variance(True,.04,.09,0),ValueError),
      ('variance export long-only domain',lambda:m.variance(1.2,.04,.09,0),ValueError),
      ('variance underflow rejects',lambda:m.variance(.5,5e-324,0,0),ValueError),
      ('grid repeated coordinates',lambda:m.grid_solve(lambda x:x,1,math.nextafter(1,2),2),ValueError),
      ('noncallable objective',lambda:m.grid_solve(None,0,1),ValueError),
      ('slack nonfinite input',lambda:m.constraint_residuals(float('nan'),.4,1),ValueError),
      ('slack invalid bound policy',lambda:m.constraint_residuals(.4,2,1),ValueError),
      ('huge integer input',lambda:m.constrained_two_asset_gmv(10**1000,1,0),ValueError),
      ('nonfinite objective',lambda:m.grid_solve(lambda x:float('nan'),0,1),ValueError),
    ]:reject('F163 '+label,fn,kind)
    num('singleton grid',lambda:m.grid_solve(lambda x:(x-.3)**2,.4,.4,10)['x'],F(2,5))
    # Independent reduced one-variable KKT derivation; source does not export multipliers.
    derivative=2*F(13,100)*F(2,5)-2*F(9,100);multiplier=-derivative
    ck('supplemental KKT cap certificate',multiplier==F(19,250) and derivative+multiplier==0 and multiplier*(F(2,5)-F(2,5))==0,derivative=str(derivative),upper_multiplier=str(multiplier),scope='analytic reduced convex fixture, not a source multiplier export')
    reject('F163 interval reporting cannot relax tiny hard minimum',lambda:m.constrained_two_asset_gmv(.04,.09,0,min_b=1e-308))
    import scipy,numpy
    out=dict(python=platform.python_version(),platform=platform.platform(),scipy=scipy.__version__,numpy=numpy.__version__,source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,historical_unique_methods_added=0,lab_results=dict(free=free,capped=capped,grid=r,slacks=m.constraint_residuals(.4,.4,1)),model=dict(covariance=[[.04,0],[0,.09]],cap_a=.4,units='dimensionless weights and compatible single-period squared-return variance',timing='fictional same-horizon risk model; no market/as-of data'))
    def safe(x):
        if isinstance(x,F):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
