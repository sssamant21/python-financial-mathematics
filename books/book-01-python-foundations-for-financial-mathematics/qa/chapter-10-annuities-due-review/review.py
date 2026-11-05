"""Section10.5 exact annuity-due lab and independent dated-payment benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.05-annuities-due.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-105-') as tmp:
        Path(tmp,'annuities_due.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['annuities_due.py']),('exact compilation',['-m','compileall','-q','annuities_due.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='PV due: 273.55\nFV due: 364.10\n' if args==['annuities_due.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_due105');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def probe(label,fn,reference):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(reference))
        else:close(label,actual,reference,atol=0)
    pv3=sum((F(100)*F(10,11)**k for k in range(3)),F(0))
    ordinary3=sum((F(100)*F(10,11)**k for k in range(1,4)),F(0))
    close('P3 due PV',m.due_pv(100,.1,3),pv3)
    close('P4 due FV',m.due_fv(100,.1,3),sum((F(100)*F(11,10)**k for k in range(1,4)),F(0)))
    close('P5 due versus ordinary',m.due_pv(100,.1,3),ordinary3*F(11,10))
    close('P5 ordinary component',m.ordinary_pv(100,.1,3),ordinary3)
    close('P6 zero rate',m.due_pv(200,0,5),F(1000))
    close('P7 negative rate',m.due_pv(100,-.1,2),F(100)+F(100)*F(10,9))
    ck('P8 nominal monthly',F(6,100)/12==F(5,1000),scope='supplemental rational conversion, no source converter')
    with localcontext() as ctx:
        ctx.prec=100
        effective_monthly=(D('1.06').ln()/12).exp()-1
        ck('P9 conversion identity',abs((1+effective_monthly)**12-D('1.06'))<D('1e-95'),decimal_periodic_rate=str(effective_monthly),scope='supplemental Decimal conversion')
        duefactor=sum((D(1)/D('1.05')**k for k in range(10)),D(0))
        inv=D(1000)/duefactor
    close('P10 payment inverse',m.due_payment_from_pv(1000,.05,10),inv)
    close('P10 inverse reconstruction',m.due_pv(m.due_payment_from_pv(1000,.05,10),.05,10),F(1000))
    close('P11 empty PV',m.due_pv(100,.05,0),F(0))
    close('P11 empty FV',m.due_fv(100,.05,0),F(0))
    close('P12 timeline',m.due_timeline_pv(125,.04,24),sum((F(125)*F(25,26)**k for k in range(24)),F(0)))
    close('signed due PV',m.due_pv(-100,.1,3),-pv3)
    close('genuine zero inverse',m.due_payment_from_pv(0,.05,10),F(0))
    close('single payment has timezero PV',m.due_pv(100,.1,1),F(100))
    probe('F54 tiny-rate ordinary PV',lambda:m.ordinary_pv(.1,5e-324,1),F(1,10))
    probe('F54 tiny-rate due PV',lambda:m.due_pv(.1,5e-324,1),F(1,10))
    probe('F54 tiny-rate due FV',lambda:m.due_fv(.1,5e-324,1),F(1,10))
    probe('F56 due PV without ordinary overflow',lambda:m.due_pv(1e308,-.9,1),F(10**308))
    # Independent finite accumulated series at terminal period100.
    probe('F56 due FV without product overflow',lambda:m.due_fv(1.7e308,-.9,100),F(17*10**307)*sum((F(1,10)**k for k in range(1,101)),F(0)))
    for label,fn in [('invalid rate',lambda:m.due_pv(100,-1,3)),('fractional count',lambda:m.due_pv(100,.05,2.5)),('empty inverse',lambda:m.due_payment_from_pv(100,.05,0)),('bool target',lambda:m.due_payment_from_pv(True,.05,10)),('F54 ordinary zero-rate overflow',lambda:m.ordinary_pv(1e308,0,2)),('F54 due zero-rate FV overflow',lambda:m.due_fv(1e308,0,2)),('F54 timeline factor underflow',lambda:m.due_timeline_pv(100,1e308,3)),('F54 timeline payment underflow',lambda:m.due_timeline_pv(5e-324,1,2)),('F55 inverse payment underflow',lambda:m.due_payment_from_pv(5e-324,0,2))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_only_prompts=[1,2],supplemental_only_prompts=[8,9],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
