"""Section 11.9 exact prepayment lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.09-extra-payments-and-prepayment.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1109-') as tmp:
        Path(tmp,'extra_payments_and_prepayment.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['extra_payments_and_prepayment.py']),('exact compilation',['-m','compileall','-q','extra_payments_and_prepayment.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and len(p.stdout.splitlines())==3 if args==['extra_payments_and_prepayment.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_prepayment');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def oracle(L,r,n,extra=0,start=1):
        L,r,extra=map(lambda x:F(str(x)),(L,r,extra))
        discount=sum(((1+r)**-i for i in range(1,n+1)),F(0))
        A=L/discount
        rows=[]
        accumulated_extra=F(0)
        for k in range(1,n+1):
            # At date k-1 the unpaid scheduled installments have this PV.
            opening=A*sum(((1+r)**-j for j in range(1,n-k+2)),F(0))-accumulated_extra
            interest=opening*r
            due=opening+interest
            scheduled=min(A,due)
            additional=min(extra,due-scheduled) if k>=start else F(0)
            closing=A*sum(((1+r)**-j for j in range(1,n-k+1)),F(0))-accumulated_extra*(1+r)-additional
            if scheduled+additional==due:
                closing=F(0)
            rows.append(dict(period=k,opening=opening,interest=interest,scheduled=scheduled,extra=additional,payment=scheduled+additional,closing=closing))
            if closing==0:
                break
            accumulated_extra=accumulated_extra*(1+r)+additional
        return rows
    def same(a,b):
        return math.isfinite(a) and math.isclose(a,float(b),rel_tol=1e-12,abs_tol=0)
    def summary(rows):
        return dict(periods=len(rows),interest=sum(row['interest'] for row in rows),paid=sum(row['payment'] for row in rows),final_balance=rows[-1]['closing'])
    def record_case(label,args):
        want=oracle(*args)
        try:rows=m.simulate(*args)
        except Exception as e:ck(label,False,exception=repr(e));return
        ok=len(rows)==len(want) and all(x.keys()==y.keys() and all(same(x[k],y[k]) for k in y) for x,y in zip(rows,want))
        ck(label,ok,actual_periods=len(rows),expected_periods=len(want),actual_last=repr(rows[-1]),expected_last={k:float(v) for k,v in want[-1].items()})
    args=(10000,.005,24)
    for label,case in [
        ('P3 baseline exact schedule',args),
        ('P3 and P13 recurring 50',(*args,50)),
        ('P3 and P13 recurring 100',(*args,100)),
        ('P12 recurring 100 from period 12',(*args,100,12)),
        ('start after maturity is baseline',(*args,100,25)),
        ('zero rate with extras',(1200,0,12,25)),
        ('P13 large extra capped',(1000,.01,12,2000)),
        ('F72 tiny balance may not be written off',(1e-10,0,4)),
        ('F72 positive residual at former absolute threshold',(1,0,2,.4999999999)),
        ('F72 one-payment loan at very large rate',(1,1e308,1)),
    ]:record_case(label,case)
    reference=[summary(oracle(*args,e)) for e in (0,50,100)]
    displayed=commands[0]['stdout'].splitlines()
    for j,e in enumerate((0,50,100)):
        want=reference[j]
        try:
            extra,raw=displayed[j].split(' ',1)
            got=ast.literal_eval(raw)
            ok=int(extra)==e and got.keys()==want.keys() and all(same(got[k],want[k]) for k in want)
        except (IndexError,TypeError,ValueError,SyntaxError):
            ok=False
        ck(f'demo scenario {e}',ok,expected={k:float(v) for k,v in want.items()})
    rows=m.simulate(*args,100)
    one=oracle(*args,100)[0]
    for label,got,want in [
        ('P2 payment',m.payment(*args),one['scheduled']),
        ('P4 first interest',rows[0]['interest'],one['interest']),
        ('P5 first payment',rows[0]['payment'],one['payment']),
        ('P6 first principal',rows[0]['payment']-rows[0]['interest'],one['payment']-one['interest']),
        ('P7 first closing',rows[0]['closing'],one['closing']),
        ('P8 next interest effect',m.simulate(*args)[1]['interest']-rows[1]['interest'],F(1,2)),
        ('P11 interest savings',m.metrics(*args)['interest']-m.metrics(*args,100)['interest'],reference[0]['interest']-reference[2]['interest']),
        ('P9 periods saved',24-len(rows),reference[0]['periods']-reference[2]['periods']),
    ]:close(label,got,want)
    ck('P12 delayed recurring interest',m.metrics(*args,100,12)['interest']>m.metrics(*args,100)['interest'])
    ck('row payment and balance identities',all(math.isclose(x['payment'],x['scheduled']+x['extra'],abs_tol=1e-10) and math.isclose(x['closing'],x['opening']+x['interest']-x['payment'],abs_tol=1e-10) and x['payment']<=x['opening']+x['interest']+1e-10 for x in rows))
    close('total principal',math.fsum(x['payment']-x['interest'] for x in rows),F(10000))
    for label,fn in [
        ('F54 payment overflow',lambda:m.payment(1e308,1,1)),
        ('F54 payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 interest underflow',lambda:m.simulate(5e-324,.25,1)),
        ('F54 due overflow',lambda:m.simulate(1e308,1,3)),
        ('F54 aggregate paid overflow',lambda:m.metrics(1e308,.75,2)),
        ('invalid extra start',lambda:m.simulate(*args,10,True)),
        ('invalid extra',lambda:m.simulate(*args,float('inf'))),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,conceptual_prompts=[1,10,14],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
