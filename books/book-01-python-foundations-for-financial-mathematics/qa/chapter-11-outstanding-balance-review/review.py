"""Section 11.6 exact balance lab and independent schedule benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.06-outstanding-loan-balance.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1106-') as tmp:
        Path(tmp,'outstanding_loan_balance.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['outstanding_loan_balance.py']),('exact compilation',['-m','compileall','-q','outstanding_loan_balance.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout.startswith('Payment: ') if args==['outstanding_loan_balance.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_balances');exec(compile(code,str(source),'exec'),m.__dict__)
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    L=10000;r=F(1,200);n=24
    A=F(L)/sum(((1+r)**-k for k in range(1,n+1)),F(0))
    exact=[F(L)]
    for _ in range(n):exact.append(exact[-1]*(1+r)-A)
    close('worked payment',m.payment(L,.005,n),A)
    for k in (0,1,5,12,23,24):
        close('prospective k='+str(k),m.prospective_balance(L,.005,n,k),exact[k])
        close('retrospective k='+str(k),m.retrospective_balance(L,.005,n,k),exact[k])
    ck('P8 remaining count',n-5==19)
    for fn in (m.prospective_balance,m.retrospective_balance):
        close('P6 zero-rate '+fn.__name__,fn(1200,0,12,3),F(900))
    close('P10 exact extra-payment example',m.balance_after_extra(5000,0,1,0,400),F(4600))
    b=m.prospective_balance(L,.005,n,5)
    close('partial extra at period five',m.balance_after_extra(L,.005,n,5,400),exact[5]-400)
    close('full principal payoff',m.balance_after_extra(L,.005,n,5,b),F(0))
    ck('worked display',commands[0]['stdout'].splitlines()==[f'Payment: {float(A):.2f}',f'Balance after 12 payments: {float(exact[12]):.2f}'])
    probe('F54 tiny rate payment',lambda:m.payment(.1,5e-324,1),F(1,10),0)
    probe('F54 tiny rate prospective balance',lambda:m.prospective_balance(.1,5e-324,3,1),F(1,15),0)
    probe('F56 prospective start independent of payment',lambda:m.prospective_balance(1e308,1,1,0),F(1e308),0)
    probe('F56 retrospective start independent of payment',lambda:m.retrospective_balance(1e308,1,1,0),F(1e308),0)
    probe('F56 retrospective maturity without overflow',lambda:m.retrospective_balance(100,1,2000,2000),F(0),0)
    probe('F66 zero-rate retrospective cancellation',lambda:m.retrospective_balance(1e308,0,10**18,10**18-1),F(1e308)/10**18,0)
    probe('F66 long retrospective with finite result',lambda:m.retrospective_balance(100,1,2001,2000),F(50)/(1-F(1,2**2001)),0)
    for label,fn in [
        ('F54 zero-rate payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 nonfinite payment',lambda:m.payment(1e308,1,1)),
        ('F54 remaining balance underflow',lambda:m.prospective_balance(5e-324,0,2,1)),
        ('F69 slight overpayment still exceeds balance',lambda:m.balance_after_extra(1e-12,0,1,0,2e-12)),
        ('F69 nonzero extra at maturity',lambda:m.balance_after_extra(100,0,1,1,1e-10)),
        ('bad completed count',lambda:m.prospective_balance(100,.01,12,13)),
        ('negative extra',lambda:m.balance_after_extra(100,0,1,0,-1)),
        ('large extra',lambda:m.balance_after_extra(100,0,1,0,200))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[1,9,11],supplemental_arithmetic=[8],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
