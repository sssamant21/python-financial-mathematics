"""Section 11.3 exact loan lab and independent amortization benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.03-level-payment-loans.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1103-') as tmp:
        Path(tmp,'level_payment_loans.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['level_payment_loans.py']),('exact compilation',['-m','compileall','-q','level_payment_loans.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout.startswith('Payment: ') if args==['level_payment_loans.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_level_payment');exec(compile(code,str(source),'exec'),m.__dict__)
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    L=10000;r=F(1,200);n=24
    a=F(L)/sum(((1+r)**-k for k in range(1,n+1)),F(0))
    opening=F(L);expected=[]
    for k in range(1,n+1):
        interest=opening*r;principal=a-interest;opening-=principal
        expected.append((k,a,interest,principal,opening))
    rows=m.schedule(L,.005,n)
    ck('all rows agree with exact retrospective recurrence',len(rows)==n and all(x[0]==y[0] and all(math.isclose(u,float(v),abs_tol=1e-10,rel_tol=1e-12) for u,v in zip(x[1:],y[1:])) for x,y in zip(rows,expected)))
    ck('P1 level payments',all(row[1]==rows[0][1] for row in rows))
    close('P2 worked payment',m.payment(L,.005,n),a)
    close('P3 zero-rate payment',m.payment(1200,0,12),F(100))
    close('P4 one period',m.payment(100,.1,1),F(110))
    for label,v,want in [('P5 interest',rows[0][2],expected[0][2]),('P6 principal',rows[0][3],expected[0][3]),('P7 new balance',rows[0][4],expected[0][4])]:
        close(label,v,want)
    for k in (0,1,12,23,24):
        close('P8/P9 prospective vs retrospective k='+str(k),m.balance(L,.005,n,k),F(L) if k==0 else expected[k-1][4])
    close('P10 total interest',m.total_interest(L,.005,n),sum((y[2] for y in expected),F(0)))
    close('P10 sum of source interest',math.fsum(x[2] for x in rows),a*n-L)
    close('P11 sum of principal',math.fsum(x[3] for x in rows),F(L))
    ck('row payment reconciliation',all(math.isclose(A,i+p,abs_tol=1e-10,rel_tol=1e-12) for _,A,i,p,_ in rows))
    ck('interest declines',all(a[2]>b[2] for a,b in zip(rows,rows[1:])))
    close('zero-rate total interest',m.total_interest(1200,0,12),F(0))
    ck('worked display',commands[0]['stdout'].splitlines()==[f'Payment: {float(a):.2f}',f'Total interest: {float(a*n-L):.2f}'])
    probe('F54 tiny rate payment',lambda:m.payment(.1,5e-324,1),F(1,10),0)
    probe('F56 opening balance independent of payment',lambda:m.balance(1e308,1,1,0),F(1e308),0)
    probe('F56 finite total interest independent of payment',lambda:m.total_interest(1e308,1,1),F(1e308),0)
    probe('F66 first principal on large-interest loan',lambda:m.schedule(1,1e100,2)[0][3],1/(2+F(1e100)),0)
    probe('F66 one-period closing balance',lambda:m.schedule(1,1e308,1)[0][4],F(0),0)
    tiny=F(1e-18);exact_payment=F(1000)/sum(((1+tiny)**-k for k in range(1,13)),F(0))
    probe('F66 tiny positive total interest',lambda:m.total_interest(1000,1e-18,12),exact_payment*12-1000,0)
    for label,fn in [
        ('F54 zero-rate payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 nonfinite payment',lambda:m.payment(1e308,1,1)),
        ('F54 schedule interest underflow',lambda:m.schedule(5e-324,.5,1)),
        ('F54 total interest overflow',lambda:m.total_interest(1e308,1,10)),
        ('invalid principal',lambda:m.payment(0,.01,12)),
        ('invalid rate',lambda:m.payment(100,-.01,12)),
        ('invalid completed',lambda:m.balance(100,.01,12,13))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
