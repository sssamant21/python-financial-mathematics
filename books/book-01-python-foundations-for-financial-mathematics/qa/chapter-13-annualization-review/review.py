"""Section 13.6 exact annualization lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.06-annualization.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1306-') as tmp:
        Path(tmp,'annualization.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['annualization.py']),('isolated import',['-c','import annualization']),('exact compilation',['-m','compileall','-q','annualization.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['annualization.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_annual');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import date,datetime
    from decimal import Decimal as D, localcontext
    import csv
    def equivalent(g,exponent):
        with localcontext() as ctx:
            ctx.prec=80
            return (D(g.numerator)/D(g.denominator))**(D(exponent.numerator)/D(exponent.denominator))-1
    def num(label,fn,want):
        try:got=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,got,want,atol=0)
    for r,t,w in [(.08,1,'.08'),(.21,2,'.1'),(.44,2,'.2'),(.05,.5,'.1025'),(-.19,2,'-.1'),(-.08,1,'-.08')]:
        num(f'E1–E6 annualize {r} over {t}',lambda:m.annualize_cumulative(r,t),F(w))
    num('E7 deannualized gain',lambda:m.deannualize(.1,3),F('.331'))
    num('E8 deannualized loss',lambda:m.deannualize(-.1,2),F('-.19'))
    ck('E9 supplemental quarterly cumulative',F('1.03')*F('.99')-1==F('.0197'))
    num('E10 quarterly annualization',lambda:m.annualize_periods([.03,-.01],4),F('1.0197')**2-1)
    num('E11 daily annualization',lambda:m.annualize_periods([.001]*252,252),float(F('1.001')**252-1))
    day90=equivalent(F('1.02'),F(365,90))
    num('E12 actual 90-day annualization',lambda:m.annualize_dates(.02,date(2025,1,1),date(2025,4,1)),day90)
    num('leap-year Actual/365 Fixed uses 366 elapsed days',lambda:m.years_actual_365(date(2024,1,1),date(2025,1,1)),F(366,365))
    ck('E13 E14 supplemental log',math.isclose(math.log(1.21)/2,math.log(1.1),rel_tol=1e-12) and math.isclose(math.expm1(math.log(1.1)),.1))
    num('E15 nominal to effective',lambda:m.effective_from_nominal(.06,2),F('.0609'))
    num('E16 effective to nominal',lambda:m.nominal_apr_from_effective(.0609,2),F('.06'))
    num('E17 explicit total-loss policy',lambda:m.annualize_cumulative(-1,3),-1)
    num('valid total loss series',lambda:m.annualize_periods([.1,-1,.2],12),-1)
    observed=[];rows=[]
    for name,r,t in [('A',.21,F(2)),('B',.05,F(1,2)),('C',-.19,F(2)),('D',.02,F(90,365))]:
        want=equivalent(1+F(str(r)),1/t)
        result=m.annualize_dates(r,date(2025,1,1),date(2025,4,1)) if name=='D' else m.annualize_cumulative(r,float(t))
        close(f'project {name} annual-effective',result,want,atol=0)
        reconstructed=m.deannualize(result,float(t));err=reconstructed-r
        ck(f'project {name} inverse residual <= 1e-10',abs(err)<=1e-10,residual=err)
        close(f'project {name} supplemental annual log',math.log1p(result),math.log1p(r)/float(t),atol=0)
        rows.append([name,r,float(t),result,math.log1p(result),err])
        observed.append((name,r,result))
    ck('project rankings differ', [x[0] for x in sorted(observed,key=lambda x:-x[1])]==list('ABDC') and [x[0] for x in sorted(observed,key=lambda x:-x[2])]==list('BADC'))
    with (HERE/'project.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(['strategy','cumulative_return','years','annual_effective','annual_log_growth','roundtrip_residual'])
        writer.writerows(rows)
    ck('F100 corrected actual/365 rounding appears in all three places',source.read_text().count(f'{float(day90):.3%}')>=3,expected=f'{float(day90):.3%}')
    num('F100 tiny compounded gain through recovery',lambda:m.annualize_periods([-.2,1e-30,.25],3),F('1e-30'))
    num('F54 tiny nominal input survives frequency scaling',lambda:m.effective_from_nominal(5e-324,2),F('5e-324'))
    for label,fn in [
        ('E18 invalid horizon',lambda:m.annualize_cumulative(.1,0)),
        ('F100 total loss does not hide later invalid data',lambda:m.annualize_periods([-1,float('nan')],252)),
        ('F100 total loss does not hide later invalid return',lambda:m.annualize_periods([-1,-1.1],252)),
        ('F100 timestamps not valid calendar dates',lambda:m.years_actual_365(datetime(2025,1,1),datetime(2025,4,1,12))),
        ('F54 overflowed annualization rejected',lambda:m.annualize_cumulative(1,.0001)),
        ('F54 positive factor cannot report total loss',lambda:m.deannualize(-.99,1000)),
    ]:
        reject(label,fn)
    num('frequency one preserves valid negative quote',lambda:m.nominal_apr_from_effective(-.9999999999999999,1),F('-.9999999999999999'))
    ck('exact demo',commands[0]['stdout'].splitlines()==['21% over 2 years: 10.0000%','5% over 6 months: 10.2500%','6% nominal semiannual: 6.0900%'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
