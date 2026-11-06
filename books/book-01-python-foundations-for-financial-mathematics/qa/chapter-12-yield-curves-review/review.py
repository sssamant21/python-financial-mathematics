"""Section 12.13 exact yield curves lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.13-yield-curves.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1213-') as tmp:
        Path(tmp,'yield_curves.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['yield_curves.py']),('exact compilation',['-m','compileall','-q','yield_curves.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['yield_curves.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_curve');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def factor(t,r):
        with localcontext() as ctx:
            ctx.prec=65
            return (1+D(r.numerator)/D(r.denominator))**(-D(str(t)))
    def numeric(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    curve=[(1,.03),(2,.035),(3,.04),(5,.045)]
    expected=[(1,F('.03')),(1.5,F('.0325')),(2,F('.035')),(3,F('.04')),(4,F('.0425')),(5,F('.045'))]
    df={}
    for t,r in expected:
        df[t]=factor(t,r)
        numeric(f'base {t}y rate',lambda:m.interpolate(curve,t),r)
        numeric(f'base {t}y discount',lambda:m.discount_factor(curve,t),df[t])
        numeric(f'base {t}y zero price',lambda:m.zero_price(1000,curve,t),1000*df[t])
    ck('endpoint slope 150bp',m.shape(curve)=='upward' and F('.045')-F('.03')==F('.015'))
    ck('shape describes endpoints, not the interior',m.shape([(1,.03),(2,.05),(3,.03)])=='flat-endpoints')
    f12=F('1.035')**2/F('1.03')-1
    f23=F('1.04')**3/F('1.035')**2-1
    numeric('1y–2y implied forward',lambda:m.forward(curve,1,2),f12)
    numeric('2y–3y implied forward',lambda:m.forward(curve,2,3),f23)
    shifts=dict(parallel=lambda t:F('.005'),steepening=lambda t:F('.01')*(F(str(t))-1)/4,
                flattening=lambda t:F('.01')*(5-F(str(t)))/4)
    for name,bump in shifts.items():
        stressed=[(t,float(F(str(r))+bump(t))) for t,r in curve]
        vals=[m.zero_price(1000,stressed,t) for t,r in expected]
        want=[1000*factor(t,r+bump(t)) for t,r in expected]
        ck(f'supplemental {name} construction; exact source prices',all(math.isclose(v,float(w),rel_tol=1e-12) for v,w in zip(vals,want)),actual=vals,expected=[float(w) for w in want])
    lines=commands[0]['stdout'].splitlines()
    want=['Curve shape: upward']+[f'{t:.1f}y: spot={float(r):.4%}, DF={float(df[t]):.6f}' for t,r in expected]
    ck('exact demo rows and forward',len(lines)==8 and lines[:7]==want and math.isclose(float(lines[-1].split(': ',1)[1]),float(f12),rel_tol=1e-12))
    text=source.read_text()
    ck('F90 worked 2y values agree with rational price',text.count(f'{float(df[2]):.5f}')>=2 and text.count(f'{float(1000*df[2]):.2f}')>=2,expected_df=f'{float(df[2]):.5f}',expected_price=f'{float(1000*df[2]):.2f}')
    tiny=[(1,1e-50),(2,1e-50)]
    numeric('F90 tiny forward survives rounded discount cancellation',lambda:m.forward(tiny,1,2),F('1e-50'))
    large=[(1000,2),(1001,2)]
    numeric('F54 forward survives discount underflow',lambda:m.forward(large,1000,1001),2)
    numeric('F54 scaled zero price survives discount underflow',lambda:m.zero_price(1e308,large,1000),F('1e308')/3**1000)
    numeric('F54 finite interpolation despite intermediate rate difference',lambda:m.interpolate([(1,-.5),(10,1e308)],5),F('-.5')+(F('1e308')+F('.5'))*F(4,9))
    for label,fn in [
        ('F90 validate rejects spot at -100%',lambda:m.validate([(1,-1),(2,.04)])),
        ('F90 shape rejects spot below -100%',lambda:m.shape([(1,-1.1),(2,.04)])),
        ('no extrapolation',lambda:m.interpolate(curve,.5)),
        ('invalid forward interval',lambda:m.forward(curve,2,2)),
        ('F54 unreportable discount rejected',lambda:m.discount_factor(large,1000)),
        ('F54 unreportable zero price rejected',lambda:m.zero_price(1e308,[(1,-.9),(2,-.9)],2)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,2,3,4,14,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
