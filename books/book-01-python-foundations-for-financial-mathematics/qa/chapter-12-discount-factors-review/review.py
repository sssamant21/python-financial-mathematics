"""Section 12.14 exact discount factors lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.14-discount-factors-and-spot-rates.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1214-') as tmp:
        Path(tmp,'discount_factors_spot_rates.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['discount_factors_spot_rates.py']),('exact compilation',['-m','compileall','-q','discount_factors_spot_rates.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['discount_factors_spot_rates.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_discount');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def number(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    nodes={1:F('.03'),2:F('.035'),3:F('.04'),4:F('.0425'),5:F('.045')}
    factors={t:(1+r)**-t for t,r in nodes.items()}
    with localcontext() as ctx:
        ctx.prec=65
        z={t:(1+D(r.numerator)/D(r.denominator)).ln() for t,r in nodes.items()}
        cont_factor=(-D('.08')).exp()
    flows=[(t,50+(1000 if t==5 else 0)) for t in nodes]
    value=sum(amount*factors[t] for t,amount in flows)
    ann={t:float(v) for t,v in nodes.items()};cont={t:float(v) for t,v in z.items()}
    for t,r in nodes.items():
        number(f'{t}y annual DF',lambda:m.df_from_spot(float(r),t),factors[t])
        number(f'{t}y inverse',lambda:m.spot_from_df(float(factors[t]),t),r)
        number(f'{t}y continuous equivalent',lambda:m.df_from_spot(cont[t],t,'continuous'),factors[t])
        number(f'{t}y zero PV',lambda:m.pv([(t,1000)],ann),1000*factors[t])
        if t<5:number(f'{t}y–{t+1}y forward',lambda:m.implied_forward(float(factors[t]),float(factors[t+1]),t,t+1),factors[t]/factors[t+1]-1)
    number('project five-year annual coupon PV',lambda:m.pv(flows,ann),value)
    number('project continuous coupon PV equivalent',lambda:m.pv(flows,cont,'continuous'),value)
    number('E6 annual 4% DF',lambda:m.df_from_spot(.04,2),F('1.04')**-2)
    number('E9 semiannual 4% DF',lambda:m.df_from_spot(.04,2,'periodic',2),F('1.02')**-4)
    number('E11 continuous 4% DF',lambda:m.df_from_spot(.04,2,'continuous'),cont_factor)
    number('E12 continuous inverse',lambda:m.spot_from_df(float(cont_factor),2,'continuous'),F('.04'))
    number('periodic inversion at quarterly frequency',lambda:m.spot_from_df(float(F('1.01')**-8),2,'periodic',4),F('.04'))
    number('E15 negative spot factor exceeds one',lambda:m.df_from_spot(-.01,2),F('.99')**-2)
    worked=30/F('1.04')+1030/F('1.05')**2
    number('E14 worked multirate price',lambda:m.pv([(1,30),(2,1030)],{1:.04,2:.05}),worked)
    number('F91 quarterly PV accepts explicit frequency',lambda:m.pv([(2,1000)],{2:.04},'periodic',frequency=4),1000/F('1.01')**8)
    number('F54 finite scaled PV despite factor underflow',lambda:m.pv([(1000,1e308)],{1000:2}),F('1e308')/3**1000)
    number('F54 finite forward despite factor ratio overflow',lambda:m.implied_forward(1e308,1e-308,1,1001),D(10)**D('.616')-1)
    number('F54 signed PV offsets before reporting',lambda:m.pv([(2,1e308),(2,-1e308),(1,1)],{2:-.9,1:0}),1)
    for label,fn in [
        ('F54 unsupported factor underflow',lambda:m.df_from_spot(2,1000)),
        ('F54 unsupported factor overflow',lambda:m.df_from_spot(-.9,400)),
        ('F91 inverse rounds to invalid lower bound',lambda:m.spot_from_df(1e308,1)),
        ('F91 negative forward rounds to invalid lower bound',lambda:m.implied_forward(1e-308,1e308,1,2)),
        ('F91 validate periodic frequency in PV',lambda:m.pv([(2,1000)],{2:.04},'periodic',frequency=False)),
        ('missing maturity rate rejected',lambda:m.pv([(2,1000)],{1:.04})),
    ]:reject(label,fn)
    text=source.read_text()
    ck('F91 worked values correctly rounded in prose and exercises',text.count(f'{float(worked):.2f}')>=2 and f'{float(F("1.02")**-4):.8f}' in text,expected_pv=f'{float(worked):.2f}',expected_semiannual=f'{float(F("1.02")**-4):.8f}')
    lines=commands[0]['stdout'].splitlines()
    expected=[f'{t}y spot={float(nodes[t]):.2%} DF={float(factors[t]):.8f} recovered={float(nodes[t]):.2%}' for t in (1,2,3)]
    ck('exact demo output',len(lines)==4 and lines[:3]==expected and math.isclose(float(lines[3].split(': ',1)[1]),float(worked),rel_tol=1e-12))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
