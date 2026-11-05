"""Section 10.7 exact lab and independent dated-payment benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.07-growing-annuities.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-107-') as tmp:
        Path(tmp,'growing_annuities.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['growing_annuities.py']),('exact compilation',['-m','compileall','-q','growing_annuities.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==14 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='' if args==['growing_annuities.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_growing107');exec(compile(code,str(source),'exec'),m.__dict__)
    def pv_ref(first,i,g,n):
        return sum((first*(1+g)**(k-1)/(1+i)**k for k in range(1,n+1)),F(0))
    def fv_ref(first,i,g,n):
        return sum((first*(1+g)**(k-1)*(1+i)**(n-k) for k in range(1,n+1)),F(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    a,b=F(1,10),F(1,20)
    ck('P1 exact payment list',[100*(1+b)**k for k in range(3)]==[100,105,F(441,4)])
    close('P2 PV',m.pv(100,.1,.05,3),pv_ref(100,a,b,3))
    close('P3 equal rates',m.pv(100,.05,.05,4),F(400,1)/F(21,20))
    close('P4 zero growth',m.pv(100,.1,0,3),pv_ref(100,a,F(0),3))
    close('P5 zero discount',m.pv(100,0,.1,3),F(331))
    ck('P6 exact declining payments',[100*(1-a)**k for k in range(3)]==[100,90,81])
    close('P6 declining PV',m.pv(100,.1,-.1,3),pv_ref(100,a,-a,3))
    close('P7 growth above discount',m.pv(100,.03,.08,5),pv_ref(100,F(3,100),F(2,25),5))
    close('P8 empty PV',m.pv(100,.1,.05,0),F(0))
    close('P8 empty FV',m.fv(100,.1,.05,0),F(0))
    close('P9 terminal FV',m.fv(100,.1,.05,3),fv_ref(100,a,b,3))
    close('P10 signed PV',m.pv(-100,.1,.05,3),pv_ref(-100,a,b,3))
    close('P11 equal-rate FV',m.fv(100,.05,.05,4),fv_ref(100,b,b,4))
    close('P12 explicit timeline',m.pv_timeline(100,.1,.05,3),pv_ref(100,a,b,3))
    for discount,growth in [(.05,.05+1e-10),(.05+1e-10,.05),(.05,math.nextafter(.05,math.inf))]:
        close('F11 near-equal represented rates '+repr((discount,growth)),m.pv(100,discount,growth,12),pv_ref(100,F(discount),F(growth),12))
    close('F11 extreme ratio fallback',m.pv(100,1e308,-.5,1),F(100)/(1+F(1e308)),atol=0)
    probe('F54 tiny-rate PV',lambda:m.pv(.1,5e-324,0,1),F(1,10),atol=0)
    probe('F54 tiny-rate FV',lambda:m.fv(.1,5e-324,0,1),F(1,10),atol=0)
    probe('F56 equal-rate avoidable intermediate overflow',lambda:m.pv(1e308,1e308,1e308,2),2*F(1e308)/(1+F(1e308)))
    probe('F56 finite FV without representable PV',lambda:m.fv(100,-.9,0,1000),F(1000,9)*(1-F(1,10)**1000))
    for label,fn in [
        ('F54 equal-rate overflow',lambda:m.pv(1e308,-.9,-.9,1)),
        ('F54 nonzero PV underflow',lambda:m.pv(5e-324,1,0,1)),
        ('F54 timeline payment underflow',lambda:m.pv_timeline(5e-324,1,0,1)),
        ('F54 nonzero FV underflow',lambda:m.fv(100,-.9,-.9,1000)),
        ('invalid discount',lambda:m.pv(100,-1,.05,3)),
        ('invalid growth',lambda:m.pv(100,.05,-1,3)),
        ('fractional count',lambda:m.pv(100,.05,.02,2.5)),
        ('bool payment',lambda:m.pv(True,.05,.02,3))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,supplemental_payment_lists=[1,6],conceptual_branch_explanation=[11],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
