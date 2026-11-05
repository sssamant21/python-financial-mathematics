"""Section10.1 exact lab, rational benchmarks and contract review."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.01-cash-flow-mathematics.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-101-') as tmp:
        Path(tmp,'cash_flow_mathematics.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['cash_flow_mathematics.py']),('exact compilation',['-m','compileall','-q','cash_flow_mathematics.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Example NPV: 41.32\n' if args==['cash_flow_mathematics.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_cashflow101');sys.modules[m.__name__]=m
    try:exec(compile(code,str(source),'exec'),m.__dict__)
    finally:sys.modules.pop(m.__name__,None)
    c=m.CashFlow
    timeline=[c(0,-500),c(1,550)]
    ck('P1 full signed timeline',[(x.year,x.amount) for x in timeline]==[(0,-500),(1,550)])
    close('P2 discount1210',m.present_value(c(2,1210),.1),F(1000))
    stream=[c(1,100),c(2,200)]
    close('P3 multiple dates',m.value_at(stream,.1),F(100)*F(10,11)+F(200)*F(10,11)**2)
    investment=[c(0,-1000),c(1,600),c(2,600)]
    close('P4 NPV',m.value_at(investment,.1),-1000+F(600)*F(10,11)+F(600)*F(10,11)**2)
    close('P5 date shift',m.value_at([c(0,100)],.05,2),F(100)*F(21,20)**2)
    close('P6 zero rate',m.value_at([c(2,80),c(4,-30)],0),F(50))
    close('P7 negative rate',m.present_value(c(2,81),-.1),F(100))
    close('worked single receipt',m.present_value(c(2,121),.1),F(100))
    close('discount factor',m.discount_factor(.1,2),F(10,11)**2)
    close('nonzero future valuation date',m.value_at(stream,.1,3),F(341))
    close('nonzero date identity',m.value_at(stream,.1,3),F(11,10)**3*F(31000,121))
    close('empty iterator',m.value_at(iter(()),.1),F(0))
    close('same-date net',m.value_at([c(0,-100),c(0,40),c(0,60)],.07),F(0))
    close('fsum cancellation',m.value_at([c(0,1e16),c(0,1),c(0,-1e16)],0),F(1))
    for label,fn in [('negative time',lambda:c(-1,100)),('bool amount',lambda:c(1,True)),('bool rate',lambda:m.discount_factor(True,1)),('invalid growth',lambda:m.discount_factor(-1,1)),('tuple instead of CashFlow',lambda:m.value_at([(1,100)],.05)),('negative valuation date',lambda:m.value_at(stream,.05,-1)),('factor underflow',lambda:m.discount_factor(.1,1e308)),('factor overflow',lambda:m.discount_factor(-.99,1e308)),('nonfinite amount',lambda:c(1,float('inf')))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=8,conceptual_only_prompts=[8],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
