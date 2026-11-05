"""Section10.4 exact ordinary-annuity lab and independent finite-series benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.04-ordinary-annuities.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-104-') as tmp:
        Path(tmp,'ordinary_annuities.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['ordinary_annuities.py']),('exact compilation',['-m','compileall','-q','ordinary_annuities.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='' if args==['ordinary_annuities.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_ordinary104');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def probe(label,fn,reference):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(reference))
        else:close(label,actual,reference,atol=0)
    pv3=sum((F(100)*F(10,11)**k for k in range(1,4)),F(0));fv3=F(331)
    close('P2 present value',m.pv(100,.1,3),pv3)
    close('P3 future value',m.fv(100,.1,3),fv3)
    close('P4 zero rate',m.pv(200,0,5),F(1000))
    ck('P5 nominal monthly',F(6,100)/12==F(5,1000),periodic_rate='.005',scope='independent rational conversion')
    with localcontext() as ctx:
        ctx.prec=100
        monthly=(D('1.06').ln()/12).exp()-1
        ck('P6 printed effective monthly percentage',round(float(monthly)*100,5)==.48676,decimal_periodic_rate=str(monthly),scope='independent Decimal conversion, no source conversion helper')
        inverse_factor=sum((D(1)/D('1.05')**k for k in range(1,11)),D(0))
        payment=D(1000)/inverse_factor
    close('P7 inverse payment',m.payment_from_pv(1000,.05,10),payment)
    close('P8 negative rate',m.pv(100,-.1,2),F(19000,81))
    close('P9 FV identity independently summed',m.fv(100,.1,3),pv3*F(11,10)**3)
    close('P10 signed payments',m.pv(-100,.1,3),-pv3)
    close('P11 empty PV',m.pv(100,.05,0),F(0))
    close('P11 empty FV',m.fv(100,.05,0),F(0))
    close('P12 independent timeline sum',m.pv(100,.08,12),sum((F(100)*F(25,27)**k for k in range(1,13)),F(0)))
    close('source inverse reconstruction',m.pv(m.payment_from_pv(1000,.05,10),.05,10),F(1000))
    close('zero target remains valid',m.payment_from_pv(0,.05,10),F(0))
    close('signed inverse payment',m.payment_from_pv(-1000,0,5),F(-200))
    probe('F54 tiny-rate PV',lambda:m.pv(.1,5e-324,1),F(1,10))
    probe('F54 tiny-rate FV',lambda:m.fv(.1,5e-324,1),F(1,10))
    # Direct finite future sum exists even though PV is outside float range.
    probe('F56 finite FV despite unsupported PV',lambda:m.fv(100,-.9,1000),F(1000,9)*(1-F(1,10)**1000))
    for label,fn in [('fractional count',lambda:m.pv(100,.05,2.5)),('invalid rate',lambda:m.pv(100,-1,3)),('zero-count inverse',lambda:m.payment_from_pv(100,.05,0)),('F54 zero-rate PV overflow',lambda:m.pv(1e308,0,2)),('F54 zero-rate FV overflow',lambda:m.fv(1e308,0,2)),('F54 positive-rate PV overflow',lambda:m.pv(1e308,.05,2)),('F55 bool target',lambda:m.payment_from_pv(True,.05,10)),('F55 NaN target',lambda:m.payment_from_pv(float('nan'),.05,10)),('F55 infinite target',lambda:m.payment_from_pv(float('inf'),.05,10)),('F55 inverse output overflow',lambda:m.payment_from_pv(1e308,1e308,1)),('F55 inverse output underflow',lambda:m.payment_from_pv(5e-324,0,2))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_only_prompts=[1],supplemental_only_prompts=[5,6],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
