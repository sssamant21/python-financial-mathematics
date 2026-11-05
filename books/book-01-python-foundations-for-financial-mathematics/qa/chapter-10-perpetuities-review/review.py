"""Section 10.8 exact lab and independent finite sums and tail bounds."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.08-perpetuities.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),rational_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-108-') as tmp:
        Path(tmp,'perpetuities.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['perpetuities.py']),('exact compilation',['-m','compileall','-q','perpetuities.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='PV: 2000.00\n' if args==['perpetuities.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_perpetuity108');exec(compile(code,str(source),'exec'),m.__dict__)
    rate=F(1,20);q=F(20,21)
    def pv_ref(payment,n,delay=0):
        return sum((F(payment)*q**k for k in range(delay+1,delay+n+1)),F(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    # Infinite sums use the first term and geometric tail, rather than C/i.
    ordinary=100*q/(1-q)
    close('P2 ordinary perpetuity',m.perpetuity_pv(100,.05),ordinary)
    required=F(4000)*(1-q)/q
    ck('P3 independent inverse payment',required==200,reference=str(required),scope='supplemental algebra; no inverse function')
    close('P3 reconstructed PV',m.perpetuity_pv(float(required),.05),F(4000))
    close('P4 implied rate from observed PV',120/m.perpetuity_pv(120,.05),F(120,2400))
    close('P7 due perpetuity',m.perpetuity_due_pv(100,.05),100+ordinary)
    close('P8 deferred perpetuity',m.deferred_perpetuity_pv(100,.05,2),100*q**3/(1-q))
    close('P8 zero delay',m.deferred_perpetuity_pv(100,.05,0),ordinary)
    actual20=m.finite_annuity_pv(100,.05,20)
    close('P9 twenty-payment direct sum',actual20,pv_ref(100,20))
    ck('P9 finite is below infinite',actual20<float(ordinary),actual=actual20)
    close('P11 signed obligation',m.perpetuity_pv(-100,.05),-ordinary)
    for n in (1,100,1000):
        close(f'P12 finite direct sum n={n}',m.finite_annuity_pv(100,.05,n),pv_ref(100,n))
    tail=ordinary*q**1000
    ck('P12 exact tail bound',0<tail<F(1,10**16),tail_approx=float(tail))
    close('empty finite stream',m.finite_annuity_pv(100,.05,0),F(0))
    close('genuine zero perpetuity',m.perpetuity_pv(0,.05),F(0))
    close('genuine zero due',m.perpetuity_due_pv(0,.05),F(0))
    close('genuine zero deferred',m.deferred_perpetuity_pv(0,.05,2),F(0))
    probe('F54 tiny-rate finite PV',lambda:m.finite_annuity_pv(.1,5e-324,1),F(1,10),atol=0)
    probe('F56 due time-zero contribution despite ordinary underflow',lambda:m.perpetuity_due_pv(5e-324,2),F(5e-324)*F(3,2),atol=0)
    probe('F56 finite deferred PV despite ordinary overflow',lambda:m.deferred_perpetuity_pv(1e308,.05,100),F(10**308)*q**101/(1-q),atol=0)
    probe('tiny-rate deferred division remains supported',lambda:m.deferred_perpetuity_pv(5e-324,5e-324,1),F(1),atol=0)
    for label,fn in [
        ('P6 zero rate invalid',lambda:m.perpetuity_pv(100,0)),
        ('P10 negative rate invalid',lambda:m.perpetuity_pv(100,-.02)),
        ('zero cash flow still needs positive rate',lambda:m.perpetuity_pv(0,0)),
        ('bool payment',lambda:m.perpetuity_pv(True,.05)),
        ('noninteger finite count',lambda:m.finite_annuity_pv(100,.05,2.5)),
        ('negative delay',lambda:m.deferred_perpetuity_pv(100,.05,-1)),
        ('F54 ordinary PV underflow',lambda:m.perpetuity_pv(5e-324,2)),
        ('F54 finite PV underflow',lambda:m.finite_annuity_pv(5e-324,1,1)),
        ('F54 deferred factor underflow',lambda:m.deferred_perpetuity_pv(100,.05,100000)),
        ('F54 deferred PV underflow',lambda:m.deferred_perpetuity_pv(5e-324,1,1))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_definition_and_convergence=[1,5],supplemental_inverse_arithmetic=[3,4],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
