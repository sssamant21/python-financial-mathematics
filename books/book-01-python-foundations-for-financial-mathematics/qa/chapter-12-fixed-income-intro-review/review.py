"""Section 12.1 exact bond lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.01-introduction-to-fixed-income.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1201-') as tmp:
        Path(tmp,'introduction_to_fixed_income.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['introduction_to_fixed_income.py']),('exact compilation',['-m','compileall','-q','introduction_to_fixed_income.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['introduction_to_fixed_income.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_bonds');exec(compile(code,str(source),'exec'),m.__dict__)
    def oracle(face,c,n,y,m):
        cf=F(face)*c/m
        values=[cf]*(n-1)+[cf+face]
        return sum((v/(1+y/m)**k for k,v in enumerate(values,1)),F(0))
    def numeric(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e),independent_reference=str(want))
        else:close(label,value,want,atol=0)
    rows=m.bond_cash_flows(1000,.05,3,2)
    ck('P2–P6 six promised flows and total',rows==[(k,25 if k<6 else 1025) for k in range(1,7)] and sum(v for _,v in rows)==1150)
    expected=[];actual=[]
    for k in range(3,8):
        y=F(k,100);want=oracle(1000,F(1,20),6,y,2)
        p=m.price(1000,.05,3,float(y),2)
        label='premium' if k<5 else 'discount' if k>5 else 'par'
        close(f'project independent price at {k}%',p,want,atol=0)
        ck(f'project classification at {k}%',m.classify(1000,.05,3,float(y),2)==label)
        expected.append(f'Yield: {k:.1f}% Price: {float(want):.2f} Classification: {label}')
        actual.append(p)
    ck('project positive finite decreasing prices',all(math.isfinite(v) and v>0 for v in actual) and all(a>b for a,b in zip(actual,actual[1:])))
    ck('exact demo displays 3, 5 and 7 percent',commands[0]['stdout'].splitlines()==expected[::2],expected=expected[::2])
    close('P8 P12 zero coupon and periodic yield',m.price(1000,0,3,.06,2),F(1000)/F('1.03')**6,atol=0)
    close('zero yield equals promised total',m.price(1000,.05,3,0,2),1150,atol=0)
    ck('fractional year with a whole count',m.bond_cash_flows(1000,.05,1.5,2)[-1][0]==3)
    ck('F78 tiny face discount must not be par',m.classify(1e-10,.05,3,.07,2)=='discount')
    ck('F78 close but unequal yield is premium',m.classify(1000,.05,3,.04999999999999999,2)=='premium')
    numeric('F54 finite PV despite overflowing raw coupon product',lambda:m.price(1e308,2,1,2,4),F('1e308'))
    numeric('F54 finite discounted principal despite underflowing discount factor',lambda:m.price(1e308,0,2,1e200,1),F('1e308')/(1+F('1e200'))**2)
    for label,fn in [
        ('F78 nonintegral count near zero',lambda:m.price(1000,.05,1e-12,.05,2)),
        ('F78 nonintegral count at float rounding boundary',lambda:m.price(1000,.05,.3333333333333333,.05,3)),
        ('F54 underflowed positive price',lambda:m.price(1e-300,0,2,1e200,1)),
        ('F54 nonfinite undiscounted total',lambda:m.price(1e308,2,1,0,1)),
        ('F54 nonfinite maturity flow',lambda:m.bond_cash_flows(1e308,2,1,1)),
        ('negative yield rejected within teaching contract',lambda:m.price(1000,.05,3,-.05,2)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=16,applied_mini_project_records=1,conceptual_prompts=[1,7,13,14,15,16],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
