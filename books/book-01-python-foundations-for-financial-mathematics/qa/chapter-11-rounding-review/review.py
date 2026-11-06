"""Section 11.12 rounding and reconciliation with a rational cent oracle."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-11/11.12-numerical-and-rounding-considerations.md'
    float_demo, decimal_demo, code=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=float(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1112-') as tmp:
        Path(tmp,'numerical_and_rounding_considerations.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['numerical_and_rounding_considerations.py']),('exact compilation',['-m','compileall','-q','numerical_and_rounding_considerations.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and len(p.stdout.splitlines())==3 if args==['numerical_and_rounding_considerations.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
        for label,body,want,flags in (
            ('exact float snippet',float_demo,'False\nTrue\n',[]),
            ('exact Decimal snippet',decimal_demo,'1.01\n',[]),
            ('F75 optimized reconciliation probe',b"""
from numerical_and_rounding_considerations import cents_schedule,reconcile
from decimal import Decimal
rows=cents_schedule(100,.01,2)
rows[0]['payment']=Decimal('0.00')
try:
    reconcile(rows,100)
except ValueError:
    print('rejected')
else:
    print('accepted')
""",'rejected\n',['-O']),
        ):
            p=subprocess.run([sys.executable,'-B',*flags,'-c',body.decode()],cwd=tmp,capture_output=True,text=True,timeout=60)
            commands.append(dict(label=label,args=flags+['-c'],returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=None,passed=p.returncode==0 and p.stdout==want and not p.stderr))
    m=types.ModuleType('exact_rounding');exec(compile(code,str(source),'exec'),m.__dict__)
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
        return [{key:(v if key in ('period','k') else int(v*100)) for key,v in row.items()} for row in rows]
    def as_decimal(row):
        return {key:(v if key in ('period','k') else Decimal(f'{v//100}.{v%100:02d}')) for key,v in row.items()}
    L=10000;r=F(1,200);n=24
    def installment(L,r,n):
        return F(L)/sum(((1+r)**-k for k in range(1,n+1)),F(0))
    a=installment(L,r,n)
    close('P2 ordinary stable payment',m.stable_payment(L,.005,n),a)
    close('P2 ordinary naive payment',m.naive_payment(L,.005,n),a)
    close('P3 zero rate',m.stable_payment(1200,0,12),100)
    tiny=installment(L,F(1,10**12),360)
    close('tiny positive rate versus exact rational value',m.stable_payment(L,1e-12,360),tiny,atol=0)
    ck('naive loses accuracy at tiny rate',abs(m.naive_payment(L,1e-12,360)-float(tiny))>1e-5)
    ck('P5 positive half-cent rounds up',m.cents("1.005")==Decimal("1.01"))
    ck('P5 negative half-cent rounds away from zero',m.cents("-1.005")==Decimal("-1.01"))
    rows=m.cents_schedule(L,.005,n)
    ck('P6 first interest',rows[0]['interest']==Decimal("50.00"))
    def cents_case(label,L,r,n):
        try:rows=m.cents_schedule(L,r,n)
        except Exception as e:ck(label,False,exception=repr(e));return
        expected=[{'k':x['period'],**{k:v for k,v in x.items() if k!='period'}} for x in rounded_ref(L,r,n)]
        actual=cents(rows)
        ck(label,actual==expected,first=actual[0],last=actual[-1],expected_first=expected[0],expected_last=expected[-1])
    cents_case('P7–P12 all ordinary rows and cent totals',10000,.005,24)
    cents_case('zero-rate rows',1200,0,12)
    cents_case('F70 exact regular installment half-cent tie',.15,0,6)
    cents_case('F70 installment based on booked principal',.005,0,2)
    cents_case('F70 finite large cent values',1e30,0,1)
    ck('P11 final adjustment',rows[-1]['payment']==Decimal("443.11") and rows[0]['payment']==Decimal("443.21"))
    ck('P12 exact maturity and reconciliation',rows[-1]['closing']==Decimal(0) and m.reconcile(rows,L))
    close('F54 stable tiny-rate one-period payment',m.stable_payment(.1,5e-324,1),F(1,10),atol=0)
    bad=[dict(x) for x in rows]
    bad[0]['payment']=Decimal(0)
    for label,fn in [
        ('F75 explicit rejection of inconsistent row',lambda:m.reconcile(bad,L)),
        ('F75 explicit rejection of empty schedule',lambda:m.reconcile([],L)),
        ('F70 zero booked principal is invalid',lambda:m.cents_schedule(.004,0,2)),
        ('F54 stable payment underflow',lambda:m.stable_payment(5e-324,0,2)),
        ('F54 stable payment overflow',lambda:m.stable_payment(1e308,1,1)),
    ]:reject(label,fn)
    demo=commands[0]['stdout'].splitlines()
    ck('demo installments and reconciliation',demo[1:]==['Regular installment: 443.21 final: 443.11','Reconciled: True'] and math.isclose(float(demo[0].split(': ')[1]),float(a),rel_tol=1e-12))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,conceptual_prompts=[4,13,14],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
