"""Section10.3 exact annuity lab and independent finite-series benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.03-level-annuities.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-103-') as tmp:
        Path(tmp,'level_annuities.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['level_annuities.py']),('exact compilation',['-m','compileall','-q','level_annuities.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==10 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='PV: 399.27\nFV: 586.66\n' if args==['level_annuities.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_annuities103');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    ck('P2 complete schedule',m.level_cash_flows(100,3)==[(1,100),(2,100),(3,100)])
    pv3=sum((F(100)*F(10,11)**k for k in range(1,4)),F(0))
    fv3=sum((F(100)*F(11,10)**k for k in range(3)),F(0))
    close('P3 PV',m.pv_level_ordinary(100,.1,3),pv3)
    close('P4 FV',m.fv_level_ordinary(100,.1,3),fv3)
    close('P5 zero rate',m.pv_level_ordinary(200,0,5),F(1000))
    ck('P6 nominal monthly conversion',F(6,100)/12==F(5,1000),periodic_decimal='.005',scope='supplemental exact rational rate derivation, no source conversion function')
    close('P7 negative rate',m.pv_level_ordinary(100,-.1,2),F(100)*F(10,9)+F(100)*F(10,9)**2)
    close('P8 shifted payments',m.pv_from_timeline(100,.1,3,2),sum((F(100)*F(10,11)**k for k in range(2,5)),F(0)))
    close('P9 PV/FV via independent sum',m.fv_level_ordinary(200,.05,6),sum((F(200)*F(21,20)**k for k in range(6)),F(0)))
    close('worked PV timeline',m.pv_from_timeline(100,.1,3),pv3)
    close('demonstration PV',m.pv_level_ordinary(100,.08,5),sum((F(100)*F(25,27)**k for k in range(1,6)),F(0)))
    close('demonstration FV',m.fv_level_ordinary(100,.08,5),sum((F(100)*F(27,25)**k for k in range(5)),F(0)))
    close('signed payment',m.pv_level_ordinary(-100,.1,3),-pv3)
    close('empty PV',m.pv_level_ordinary(100,.1,0),F(0))
    close('empty FV',m.fv_level_ordinary(100,.1,0),F(0))
    ck('zero timeline empty',m.level_cash_flows(100,0)==[])
    with localcontext() as ctx:
        ctx.prec=100
        tiny_rate=D('1e-16');small_pv=sum((D(100)/(1+tiny_rate)**k for k in range(1,11)),D(0))
    close('small rate finite-series oracle',m.pv_level_ordinary(100,1e-16,10),small_pv)
    close('F54 smallest-rate PV',m.pv_level_ordinary(.1,5e-324,1),F(1,10),atol=0)
    close('F54 smallest-rate FV',m.fv_level_ordinary(.1,5e-324,1),F(1,10),atol=0)
    for label,fn in [('P10 fractional count',lambda:m.pv_level_ordinary(100,.05,2.5)),('invalid rate',lambda:m.pv_level_ordinary(100,-1,2)),('bool payment',lambda:m.fv_level_ordinary(True,.1,2)),('negative first period',lambda:m.level_cash_flows(100,3,-1)),('F54 zero-rate PV overflow',lambda:m.pv_level_ordinary(1e308,0,2)),('F54 zero-rate FV overflow',lambda:m.fv_level_ordinary(1e308,0,2)),('F54 timeline factor underflow',lambda:m.pv_from_timeline(100,1e308,1,2)),('F54 timeline nonzero term underflow',lambda:m.pv_from_timeline(5e-324,1,1))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=10,conceptual_only_prompts=[1],supplemental_only_prompts=[6],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
