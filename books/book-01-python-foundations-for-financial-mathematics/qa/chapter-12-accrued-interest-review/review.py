"""Section 12.8 exact accrued interest lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.08-accrued-interest-and-clean-vs-dirty-price.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1208-') as tmp:
        Path(tmp,'accrued_interest.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['accrued_interest.py']),('exact compilation',['-m','compileall','-q','accrued_interest.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['accrued_interest.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_accrual');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import date,datetime
    def numeric(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e),independent_reference=str(want))
        else:close(label,value,want,atol=0)
    start,end=date(2026,1,1),date(2026,7,1)
    length=sum((31,28,31,30,31,30))
    ck('P5 semiannual coupon',m.coupon(1000,.06)==30)
    ck('P6 P7 independent month lengths',length==181 and sum((31,28,31))==90)
    for day,elapsed in [(start,0),(date(2026,2,1),31),(date(2026,4,1),90),(date(2026,6,1),151),(date(2026,6,30),180)]:
        alpha=F(elapsed,length)
        interest=m.accrued(1000,.06,2,start,end,day)
        full=m.dirty(1020,interest)
        close(f'date {day} fraction',m.fraction(start,end,day),alpha,atol=0)
        close(f'date {day} accrued',interest,30*alpha,atol=0)
        close(f'date {day} dirty',full,1020+30*alpha,atol=0)
        close(f'date {day} reverse reconciliation',m.clean(full,interest),1020,atol=0)
    close('leap-year actual period',m.fraction(date(2024,1,1),date(2024,7,1),date(2024,4,1)),F(91,182),atol=0)
    close('new period resets on coupon date',m.fraction(end,date(2027,1,1),end),0,atol=0)
    close('P12 quarterly coupon',m.coupon(2000,.08,4),40,atol=0)
    cash=F('101.25')*250000/100
    ck('P13 P14 supplemental quote conversion',cash==253125 and m.dirty(float(cash),3750)==256875)
    ck('P15 Actual/360 differs from modeled period',F(90,360)!=F(90,181))
    want=f'Accrued interest: {float(F(2700,181)):.6f}; dirty price: {float(1020+F(2700,181)):.6f}'
    ck('exact demo matches independent fixture',commands[0]['stdout'].splitlines()==[want],expected=want)
    numeric('F54 finite coupon despite unscaled overflow',lambda:m.coupon(1e308,2,4),F('5e307'))
    numeric('F54 finite accrued despite coupon outside float range',lambda:m.accrued(1e308,2,1,start,end,date(2026,4,1)),F('2e308')*F(90,181))
    for label,fn in [
        ('F85 datetime silently truncates partial days',lambda:m.fraction(datetime(2026,1,1),datetime(2026,7,1),datetime(2026,4,1,12))),
        ('F85 mixed date and datetime rejected',lambda:m.fraction(start,end,datetime(2026,4,1,12))),
        ('next coupon date excluded',lambda:m.fraction(start,end,end)),
        ('earlier settlement rejected',lambda:m.fraction(start,end,date(2025,12,31))),
        ('zero-length period rejected',lambda:m.fraction(start,start,start)),
        ('F54 dirty total overflow rejected',lambda:m.dirty(1e308,1e308)),
        ('F54 coupon overflow rejected',lambda:m.coupon(1e308,2,1)),
        ('F54 coupon underflow rejected',lambda:m.coupon(5e-324,.25,2)),
        ('negative clean price rejected',lambda:m.clean(5,6)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,2,3,4,16,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
