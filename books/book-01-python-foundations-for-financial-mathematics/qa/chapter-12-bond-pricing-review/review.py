"""Section 12.5 exact bond pricing lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.05-bond-pricing.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1205-') as tmp:
        Path(tmp,'bond_pricing.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['bond_pricing.py']),('exact compilation',['-m','compileall','-q','bond_pricing.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['bond_pricing.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_pricing');exec(compile(code,str(source),'exec'),m.__dict__)
    def ref(y,n=6,FV=1000,C=30,mult=2):
        p=F(FV)
        for _ in range(n): p=(p+C)/(1+y/mult)
        return p
    def numeric(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    rows=m.cash_flows(1000,.06,6)
    ck('P1–P5 full six rows',rows==[(k,k/2,30 if k<6 else 1030) for k in range(1,7)])
    vals=[]
    for k in range(3,9):
        y=F(k,100)
        want=ref(y)
        direct=m.flat_price(rows,float(y))
        annuity=m.annuity_price(1000,.06,6,float(y))
        close(f'matrix direct {k}%',direct,want,atol=0)
        close(f'matrix annuity {k}%',annuity,want,atol=0)
        close(f'matrix +100bp shock {k}%',m.parallel_shock(rows,float(y),.01),ref(y+F('.01'))-want,atol=0)
        vals.append(direct)
    ck('P6 P10 P11 premium par discount',vals[1]>1000 and math.isclose(vals[3],1000,rel_tol=1e-12) and vals[5]<1000)
    ck('P12 strictly decreasing prices',all(a>b for a,b in zip(vals,vals[1:])))
    numeric('P9 zero yield',lambda:m.flat_price(rows,0),1180)
    numeric('negative yield',lambda:m.flat_price(rows,-.01),ref(F('-.01')))
    numeric('P13 flat discount factors',lambda:m.curve_price(rows,[float(F('1.03')**-k) for k in range(1,7)]),1000)
    ds=tuple(map(F,('.985','.967','.949','.930','.910','.889')))
    curve=sum(a*b for a,b in zip((30,30,30,30,30,1030),ds))
    numeric('P14 explicit nonflat curve',lambda:m.curve_price(rows,list(map(float,ds))),curve)
    numeric('P15 zero coupon',lambda:m.flat_price(m.cash_flows(1000,0,6),.06),ref(F('.06'),C=0))
    bumped=rows[:-1]+[(6,3,2030)]
    numeric('P16 deliberate doubled redemption adds discounted face',lambda:m.flat_price(bumped,.06)-m.flat_price(rows,.06),1000/F('1.03')**6)
    numeric('F54 finite PV despite discount underflow',lambda:m.flat_price([(1,1,0),(2,2,1e308)],1e200,1),F('1e308')/(1+F('1e200'))**2)
    numeric('F54 finite annuity PV before cash flow reporting',lambda:m.annuity_price(1e308,2,4,2,4),F('1e308'))
    numeric('F82 tiny signed shock does not cancel',lambda:m.parallel_shock(rows,.06,1e-18),ref(F('.06')+F('1e-18'))-ref(F('.06')))
    for label,fn in [
        ('F82 mismatch between frequency and schedule',lambda:m.flat_price(rows,.06,4)),
        ('F82 duplicate period rejects positional curve',lambda:m.curve_price([rows[0],rows[0],*rows[2:]],[1]*6)),
        ('F82 negative row amount',lambda:m.flat_price([(1,.5,-100)],.06)),
        ('F82 no promised positive flow',lambda:m.curve_price([(1,.5,0)],[1])),
        ('F82 annuity bool yield',lambda:m.annuity_price(1000,.06,6,True)),
        ('F82 shock bool',lambda:m.parallel_shock(rows,.06,True)),
        ('F54 overflowing curve PV',lambda:m.curve_price([(1,.5,1e308)],[2])),
        ('F54 underflowed curve PV',lambda:m.curve_price([(1,.5,1e-300)],[1e-100])),
    ]:reject(label,fn)
    demo=[f'Yield {y:.1%}: price {float(ref(F(str(y)))):.2f}' for y in (.04,.06,.08)]
    demo+=['100bp yield rise price change: '+str(round(float(ref(F('.07'))-ref(F('.06'))),2))]
    ck('exact demo',commands[0]['stdout'].splitlines()==demo,expected=demo)
    ck('F82 nonflat factor fixture supplied in project',all(str(v) in source.read_text() for v in ('0.985','0.967','0.949','0.930','0.910','0.889')))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
