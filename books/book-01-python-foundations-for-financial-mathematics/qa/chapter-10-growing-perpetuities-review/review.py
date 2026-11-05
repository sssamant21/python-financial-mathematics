"""Section 10.9 exact lab and independent growing-stream benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.09-growing-perpetuities.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-109-') as tmp:
        Path(tmp,'growing_perpetuities.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['growing_perpetuities.py']),('exact compilation',['-m','compileall','-q','growing_perpetuities.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='' if args==['growing_perpetuities.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_growing_perpetuity');exec(compile(code,str(source),'exec'),m.__dict__)
    i,g=F(2,25),F(3,100);q=(1+g)/(1+i)
    ref=100/(1+i)/(1-q)
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    close('P2 ordinary PV',m.pv(100,.08,.03),ref)
    next_payment=100*(1+g)
    ck('P3 supplemental first-payment conversion',next_payment==103)
    close('P4 updated PV',m.pv(float(next_payment),.08,.03),next_payment/(1+i)/(1-q))
    close('P7 declining stream',m.pv(100,.05,-.02),F(10000,7))
    close('P8 due PV',m.due_pv(100,.08,.03),100/(1-q))
    close('P9 deferred PV',m.deferred_pv(100,.08,.03,2),ref/(1+i)**2)
    payment=F(2000)*(1+i)*(1-q)
    ck('P10 supplemental inverse arithmetic',payment==100)
    close('P10 reconstructed PV',m.pv(float(payment),.08,.03),F(2000))
    for spread in (F(1,100),F(1,1000)):
        q2=(1+g)/(1+g+spread)
        close(f'P11 positive payment spread={spread}',m.pv(100,float(g+spread),.03),F(100)/(1+g+spread)/(1-q2))
    close('P11 negative payment sensitivity',m.pv(-100,.031,.03),F(-100000))
    for n in (1,20,100,1000):
        expected=sum((100*q**k/(1+i) for k in range(n)),F(0))
        close(f'P12 direct finite sum n={n}',m.finite_pv(100,.08,.03,n),expected)
    ck('P12 exact remaining tail bound',0<ref*q**1000<F(1,10**16),tail=float(ref*q**1000))
    close('zero period value',m.finite_pv(100,.08,.03,0),F(0))
    close('zero first payment',m.due_pv(0,.08,.03),F(0))
    close('negative discount with more negative growth',m.pv(100,-.05,-.1),F(2000))
    close('zero delay',m.deferred_pv(100,.08,.03,0),ref)
    d=.05;near=math.nextafter(d,0)
    benchmark=sum((F(100)*(1+F(near))**k/(1+F(d))**(k+1) for k in range(12)),F(0))
    probe('F11 finite near-equal cancellation',lambda:m.finite_pv(100,d,near,12),benchmark)
    probe('F54 finite tiny-rate value',lambda:m.finite_pv(.1,5e-324,0,1),F(1,10),0)
    probe('F56 finite PV despite infinite overflow',lambda:m.finite_pv(1e308,.05,0,1),F(10**308)/F(21,20),0)
    probe('F56 empty stream despite infinite overflow',lambda:m.finite_pv(1e308,.05,0,0),F(0),0)
    probe('F56 due next payment overflow',lambda:m.due_pv(1e307,1e308,1e100),F(1e307)*(1+F(1e308))/(F(1e308)-F(1e100)),0)
    probe('F56 finite deferral despite ordinary overflow',lambda:m.deferred_pv(1e308,.05,0,100),F(10**308)*F(20,21)**100/F(1,20),0)
    for label,fn in [
        ('P6 equal rates rejected',lambda:m.pv(100,.03,.03)),
        ('P5 growth above discount rejected',lambda:m.pv(100,.02,.03)),
        ('invalid growth',lambda:m.pv(100,.05,-1)),
        ('invalid delay',lambda:m.deferred_pv(100,.08,.03,-1)),
        ('due bool rejected',lambda:m.due_pv(True,.08,.03)),
        ('F54 ordinary underflow',lambda:m.pv(5e-324,2,0)),
        ('F54 due total overflow',lambda:m.due_pv(1.2e308,1,0)),
        ('F54 deferral factor underflow',lambda:m.deferred_pv(100,.05,0,100000)),
        ('F54 deferred PV underflow',lambda:m.deferred_pv(5e-324,1,0,1))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[1,5,6,11],supplemental_arithmetic_prompts=[3,10],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
