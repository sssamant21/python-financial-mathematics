"""Section 11.7 exact and rounded schedules with independent rational oracles."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.07-amortization-schedules.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1107-') as tmp:
        Path(tmp,'amortization_schedules.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['amortization_schedules.py']),('exact compilation',['-m','compileall','-q','amortization_schedules.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and len(p.stdout.splitlines())==4 if args==['amortization_schedules.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_schedules');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal
    def half_up(x):
        return (2*x.numerator+x.denominator)//(2*x.denominator)
    def rounded_ref(principal,rate,n):
        opening=half_up(F(str(principal))*100)
        r=F(str(rate))
        a=half_up(F(opening)/sum(((1+r)**-k for k in range(1,n+1)),F(0)))
        rows=[]
        for k in range(1,n+1):
            interest=half_up(opening*r)
            paid=opening+interest if k==n else min(a,opening+interest)
            repaid=paid-interest;closing=opening-repaid
            rows.append(dict(period=k,opening=opening,payment=paid,interest=interest,principal=repaid,closing=closing))
            opening=closing
        return rows
    def cents(rows):
        return [{key:(v if key=='period' else int(v*100)) for key,v in row.items()} for row in rows]
    def as_decimal(row):
        return {key:(v if key=='period' else Decimal(f'{v//100}.{v%100:02d}')) for key,v in row.items()}
    L=10000;r=F(1,200);n=24
    a=F(L)/sum(((1+r)**-k for k in range(1,n+1)),F(0))
    opening=F(L);expected=[]
    for k in range(1,n+1):
        interest=opening*r;repaid=a-interest;closing=opening-repaid
        expected.append(dict(period=k,opening=opening,payment=a,interest=interest,principal=repaid,closing=closing))
        opening=closing
    rows=m.exact_schedule(L,.005,n)
    ck('P1 exact six-column contract',set(rows[0])=={'period','opening','payment','interest','principal','closing'})
    ck('all exact rows vs independent Fraction recurrence',len(rows)==n and all(x['period']==y['period'] and all(math.isclose(x[key],float(y[key]),abs_tol=1e-10,rel_tol=1e-12) for key in x if key!='period') for x,y in zip(rows,expected)))
    lines=source.read_text().splitlines()
    for k,want in enumerate(expected[:3],1):
        line=next(l for l in lines if l.startswith(f'| {k} |'))
        actual=[v.replace(',','') for v in re.findall(r'\$([\d,.]+)',line)]
        want=[f'{float(want[key]):.2f}' for key in ('opening','interest','principal','payment','closing')]
        ck('F68 printed table row '+str(k),actual==want,actual=actual,expected=want)
    for j,key in ((0,'interest'),(0,'principal'),(0,'closing'),(1,'interest')):
        close(f'P2–P5 row {j+1} {key}',rows[j][key],expected[j][key])
    ck('P6 exact payment identity',all(math.isclose(x['payment'],x['principal']+x['interest'],rel_tol=1e-12) for x in rows))
    ck('P7 exact balance identity',all(math.isclose(x['closing'],x['opening']-x['principal'],rel_tol=1e-12,abs_tol=1e-10) for x in rows))
    close('P8 exact principal total',math.fsum(x['principal'] for x in rows),F(L))
    close('P9 exact interest total',math.fsum(x['interest'] for x in rows),n*a-L)
    zr=m.exact_schedule(1200,0,12)
    ck('P10 zero-rate schedule',all(x['payment']==x['principal']==100 and x['interest']==0 for x in zr))
    rounded=m.rounded_schedule(L,.005,n); oracle=rounded_ref(L,.005,n)
    ck('all rounded rows vs independent integer-cent oracle',cents(rounded)==oracle)
    expect=[str(as_decimal(x)) for x in oracle[:3]]+['Final: '+str(as_decimal(oracle[-1]))]
    ck('exact demonstration first three and final rounded rows',commands[0]['stdout'].splitlines()==expect,expected=expect)
    ck('P11 final rounded installment differs',rounded[-1]['payment']!=rounded[0]['payment'],first=str(rounded[0]['payment']),final=str(rounded[-1]['payment']))
    ck('P12 both policies mature at zero within tolerance',abs(rows[-1]['closing'])<1e-10 and rounded[-1]['closing']==0)
    ck('P13 interest on opening balance',all(x['interest']==m.money(x['opening']*Decimal('.005')) for x in rounded))
    ck('F70 half-up payment tie .15/6',cents(m.rounded_schedule(.15,0,6))==rounded_ref(.15,0,6),expected=rounded_ref(.15,0,6),actual=cents(m.rounded_schedule(.15,0,6)))
    ck('F70 regular payment based on rounded opening',cents(m.rounded_schedule(.005,0,2))==rounded_ref(.005,0,2),expected=rounded_ref(.005,0,2),actual=cents(m.rounded_schedule(.005,0,2)))
    try:big=m.rounded_schedule(1e30,0,1)[0]['closing']
    except Exception as e:ck('F70 finite large cent schedule',False,exception=repr(e))
    else:ck('F70 finite large cent schedule',big==0,closing=str(big))
    close('F54 tiny-rate payment',m.level_payment(.1,5e-324,1),F(1,10),atol=0)
    close('F66 large-rate first principal',m.exact_schedule(1,1e100,2)[0]['principal'],1/(2+F(1e100)),atol=0)
    close('F66 one-payment final balance',m.exact_schedule(1,1e308,1)[0]['closing'],F(0),atol=0)
    for label,fn in [
        ('F54 payment underflow',lambda:m.level_payment(5e-324,0,2)),
        ('F54 payment overflow',lambda:m.level_payment(1e308,1,1)),
        ('F54 interest underflow',lambda:m.exact_schedule(5e-324,.5,1)),
        ('F70 rounded opening cannot be zero',lambda:m.rounded_schedule(.004,0,2)),
        ('invalid rate',lambda:m.exact_schedule(100,-.1,12)),
        ('invalid count',lambda:m.rounded_schedule(100,.01,True))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,conceptual_prompts=[14],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
