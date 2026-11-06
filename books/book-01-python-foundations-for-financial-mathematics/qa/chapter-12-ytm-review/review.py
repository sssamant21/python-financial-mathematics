"""Section 12.6 exact YTM lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.06-yield-to-maturity.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1206-') as tmp:
        Path(tmp,'yield_to_maturity.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['yield_to_maturity.py']),('exact compilation',['-m','compileall','-q','yield_to_maturity.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['yield_to_maturity.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_ytm');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def oracle(P):
        with localcontext() as ctx:
            ctx.prec=65
            y=D('.06')
            for _ in range(30):
                d=1/(1+y/2)
                p=sum((30 if k<6 else 1030)*d**k for k in range(1,7))
                dp=-sum(k*(30 if k<6 else 1030)*d**(k+1)/2 for k in range(1,7))
                step=(p-D(P))/dp
                y-=step
                if abs(step)<D('1e-58'):return y
            raise RuntimeError('independent Newton oracle did not converge')
    def reference(y):
        i=F(str(y))/2
        return sum(F(30 if k<6 else 1030)/(1+i)**k for k in range(1,7))
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    yields=[]
    for p in (900,950,1000,1050,1100):
        expected=oracle(p); y=m.ytm(1000,.06,6,p); yields.append(y)
        close(f'project independent yield at {p}',y,expected,atol=3e-11)
        ck(f'project relative repricing residual at {p}',abs(float(reference(y))-p)<=1e-11*p)
        close(f'project current yield at {p}',m.current_yield(1000,.06,p),F(60,p),atol=0)
    ck('project yields decrease with market price',all(x>y for x,y in zip(yields,yields[1:])))
    p=float(reference('.0475'))
    numeric('project known yield round-trip',lambda:m.ytm(1000,.06,6,p),F('.0475'),atol=3e-11)
    numeric('P13 exact zero yield',lambda:m.ytm(1000,.06,6,1180),0)
    numeric('P14 negative yield from independent price',lambda:m.ytm(1000,.06,6,float(reference('-.01'))),F('-.01'),atol=3e-11)
    numeric('P12 zero coupon independently inverted',lambda:m.ytm(1000,0,6,float(1000/F('1.03')**6)),F('.06'),atol=3e-11)
    ck('P3 P4 coupon count and cash-flow amount',6==3*2 and F(1000)*F('.06')/2==30)
    numeric('F83 tiny notional still uses relative residual',lambda:m.ytm(1e-30,0,1,8e-31,1),F('.25'))
    numeric('F83 supported high yield beyond legacy bracket',lambda:m.ytm(1e100,0,1,1e90,1),10**10-1)
    numeric('F83 multi-payment price with a near-zero yield',lambda:m.ytm(1,1e-100,2,1,1),F('1e-100'))
    numeric('F54 repricing despite underflowing discount factor',lambda:m.price(1e308,0,2,1e200,1),F('1e308')/(1+F('1e200'))**2)
    numeric('F54 finite current yield after intermediate scaling',lambda:m.current_yield(1e308,2,1e308),2)
    for label,fn in [
        ('F83 zero tolerance rejected',lambda:m.ytm(1000,.06,6,950,tolerance=0)),
        ('F83 boolean tolerance rejected',lambda:m.ytm(1000,.06,6,950,tolerance=True)),
        ('F83 unsatisfied repricing tolerance rejected',lambda:m.ytm(1000,.06,6,950,tolerance=1e-30)),
        ('F83 invalid current-yield face',lambda:m.current_yield(True,.06,1000)),
        ('F83 invalid current-yield coupon',lambda:m.current_yield(1000,-.06,1000)),
        ('F83 root rounding to lower domain boundary rejected',lambda:m.ytm(1e-308,0,1,1e308,1)),
        ('F54 reject underflowed price',lambda:m.price(1e-300,0,2,1e200,1)),
        ('F54 reject overflowing negative-yield price',lambda:m.price(1e308,0,1,-.5,1)),
    ]:reject(label,fn)
    expected=[f'Market price: {p:.2f}; YTM: {float(oracle(p)):.6%}; repriced: {p:.6f}' for p in (950,1000,1050)]
    ck('exact demo outputs',commands[0]['stdout'].splitlines()==expected,expected=expected)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,2,9,10,11,16,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
