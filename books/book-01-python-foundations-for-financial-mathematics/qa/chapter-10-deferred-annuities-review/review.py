"""Section10.6 exact deferred-annuity lab and independent dated-payment benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.06-deferred-annuities.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value,rational_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-106-') as tmp:
        Path(tmp,'deferred_annuities.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['deferred_annuities.py']),('exact compilation',['-m','compileall','-q','deferred_annuities.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='PV deferred: 205.52\n' if args==['deferred_annuities.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_deferred106');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def probe(label,fn,reference):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(reference))
        else:close(label,actual,reference,atol=0)
    pv3=sum((F(100)*F(10,11)**k for k in range(3,6)),F(0))
    close('P2 zero delay ordinary',m.deferred_pv(100,.1,3,0),sum((F(100)*F(10,11)**k for k in range(1,4)),F(0)))
    close('P3 deferred PV',m.deferred_pv(100,.1,3,2),pv3)
    close('P4 discount identity',m.deferred_pv(100,.1,3,2),F(331000,1331)*F(10,11)**2)
    close('P5 zero rate',m.deferred_pv(200,0,5,100),F(1000))
    close('P6 empty schedule',m.deferred_pv(100,.05,0,10),F(0))
    close('P7 negative rate',m.deferred_pv(100,-.1,2,1),sum((F(100)*F(10,9)**k for k in (2,3)),F(0)))
    close('P8 one extra delay',m.deferred_pv(100,.1,3,3),pv3*F(10,11))
    ck('P9 nominal monthly',F(6,100)/12==F(5,1000),scope='supplemental rational conversion, no source converter')
    with localcontext() as ctx:
        ctx.prec=100
        factor=sum((D(1)/D('1.05')**k for k in range(4,14)),D(0))
        inverse=D(1000)/factor
    close('P10 inverse payment',m.deferred_payment(1000,.05,10,3),inverse)
    close('P10 reconstruction',m.deferred_pv(m.deferred_payment(1000,.05,10,3),.05,10,3),F(1000))
    close('P11 outgoing stream',m.deferred_pv(-100,.1,3,2),-pv3)
    close('P12 explicit timeline',m.timeline_pv(125,.04,24,7),sum((F(125)*F(25,26)**k for k in range(8,32)),F(0)))
    close('negative rate extra delay',m.deferred_pv(100,-.1,2,2),sum((F(100)*F(10,9)**k for k in (3,4)),F(0)))
    close('zero target inverse valid',m.deferred_payment(0,.05,10,3),F(0))
    probe('F54 tiny-rate ordinary PV',lambda:m.ordinary_pv(.1,5e-324,1),F(1,10))
    probe('F54 tiny-rate deferred PV',lambda:m.deferred_pv(.1,5e-324,1,0),F(1,10))
    finite_deferred=F(10**308)*sum((F(20,21)**k for k in range(101,111)),F(0))
    probe('F56 finite deferred PV despite ordinary overflow',lambda:m.deferred_pv(1e308,.05,10,100),finite_deferred)
    for label,fn in [('invalid rate',lambda:m.deferred_pv(100,-1,3,2)),('negative delay',lambda:m.deferred_pv(100,.05,3,-1)),('fractional count',lambda:m.deferred_pv(100,.05,2.5,1)),('empty inverse',lambda:m.deferred_payment(100,.05,0,2)),('bool target',lambda:m.deferred_payment(True,.05,10,3)),('F54 zero-rate ordinary overflow',lambda:m.ordinary_pv(1e308,0,2)),('F54 deferral factor underflow',lambda:m.deferred_pv(100,.1,1,10000)),('F54 deferred nonzero value underflow',lambda:m.deferred_pv(5e-324,1,1,0)),('F54 timeline factor underflow',lambda:m.timeline_pv(100,1e308,1,1)),('F54 timeline payment underflow',lambda:m.timeline_pv(5e-324,1,1,0)),('F55 inverse underflow',lambda:m.deferred_payment(5e-324,0,2,0))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_only_prompts=[1],supplemental_only_prompts=[9],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
