"""Section 12.4 exact zero-coupon lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.04-zero-coupon-bonds.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1204-') as tmp:
        Path(tmp,'zero_coupon_bonds.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['zero_coupon_bonds.py']),('exact compilation',['-m','compileall','-q','zero_coupon_bonds.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['zero_coupon_bonds.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_zero');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def numeric(label,fn,want,atol=0):
        try: value=fn()
        except Exception as e: ck(label,False,exception=repr(e),independent_reference=str(want))
        else: close(label,value,want,atol=atol)
    prices={}
    for n in (1,3,5,10):
        for y in (2,4,6,8):
            factor=(1+F(y,200))**(-2*n)
            expected=(1000*factor,factor,n/(1+F(y,200)),F(y,100))
            p=m.price(1000,y/100,n)
            values=(p,m.discount_factor(y/100,n),m.modified_duration(y/100,n),m.implied_yield(1000,p,n))
            ck(f'matrix T={n}, y={y}%',all(math.isclose(x,float(v),rel_tol=1e-12) for x,v in zip(values,expected)),
                actual=values,expected=[float(v) for v in expected])
            prices[n,y]=p
    ck('prices decrease with yield',all(prices[n,y]>prices[n,y+2] for n in (1,3,5,10) for y in (2,4,6)))
    ck('prices decrease with maturity at positive yield',all(prices[a,y]>prices[b,y] for a,b in [(1,3),(3,5),(5,10)] for y in (2,4,6,8)))
    exact=F(1000)/F('1.03')**6
    numeric('P6 price',lambda:m.price(1000,.06,3),exact)
    numeric('P7 discount to face',lambda:1000-m.price(1000,.06,3),1000-exact)
    numeric('P8 rounded price implies a different yield',lambda:m.implied_yield(1000,837.48,3),2*((D(1000)/D('837.48'))**(D(1)/6)-1))
    ck('P9 P10 supplemental annual equivalents',F('1.03')**2-1==F('.0609') and round(200*float(D('1.03').ln()),4)==5.9118)
    numeric('P12 zero yield',lambda:m.price(1000,0,3),1000)
    numeric('P13 negative yield',lambda:m.price(1000,-.01,3),F(1000)/F('.995')**6)
    numeric('negative yield round-trip',lambda:m.implied_yield(1000,m.price(1000,-.01,3),3),F('-.01'))
    numeric('P17 analytic convexity',lambda:m.convexity(.06,3),F(42,4)/F('1.03')**2)
    with localcontext() as ctx:
        ctx.prec=70
        h=D('1e-9')
        p=lambda y:D(1000)/(1+y/2)**6
        center=D('.06')
        duration=-(p(center+h)-p(center-h))/(2*h*p(center))
        curvature=(p(center+h)-2*p(center)+p(center-h))/(h*h*p(center))
    numeric('P16 independent first price derivative',lambda:m.modified_duration(.06,3),duration)
    numeric('P17 independent second price derivative',lambda:m.convexity(.06,3),curvature)
    numeric('F54 finite price despite underflowed discount factor',lambda:m.price(1e308,1e200,2,1),F('1e308')/(1+F('1e200'))**2)
    numeric('F81 finite yield despite overflowing face/price ratio',lambda:m.implied_yield(1e308,1e-308,4,1),F('1e154')-1)
    numeric('F81 negative yield despite underflowing face/price ratio',lambda:m.implied_yield(1e-308,1e308,1000,1),D(10)**D('-.616')-1)
    numeric('F81 finite convexity with large maturity and yield',lambda:m.convexity(1e200,1e200,1),1)
    for label,fn in [
        ('F54 reject overflowing negative-yield price',lambda:m.price(1e308,-.9,3,1)),
        ('F54 reject underflowed positive price',lambda:m.price(1e-300,1e200,2,1)),
        ('F81 reject rounded lower-bound inverse',lambda:m.implied_yield(1e-308,1e308,1,1)),
        ('F81 duration rejects bool rate',lambda:m.modified_duration(True,3)),
        ('F81 convexity rejects bool rate',lambda:m.convexity(True,3)),
        ('invalid periodic yield at -100%',lambda:m.price(1000,-2,3,2)),
    ]:reject(label,fn)
    want=['Price: 837.48','Implied nominal annual yield: 0.06','Discount factor: 0.83748426','Modified duration: 2.912621']
    ck('exact demo values',commands[0]['stdout'].splitlines()==want,expected=want)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,2,15,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
