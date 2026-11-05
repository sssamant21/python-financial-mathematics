"""Section 11.1 exact loan lab and independent schedule benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.01-loan-mathematics.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1101-') as tmp:
        Path(tmp,'loan_mathematics.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['loan_mathematics.py']),('exact compilation',['-m','compileall','-q','loan_mathematics.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout.startswith('Payment: ') if args==['loan_mathematics.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_loan');exec(compile(code,str(source),'exec'),m.__dict__)
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    def direct_factor(rate,n):
        return sum(((1+rate)**-k for k in range(1,n+1)),F(0))
    i=F(1,200);p=F(10000)/direct_factor(i,24)
    close('P4 zero-rate payment',m.payment(1200,0,12),F(100))
    close('P5 one period',m.payment(100,.1,1),F(110))
    close('P6/P7 worked payment vs direct sum',m.payment(10000,.005,24),p)
    close('P6 unrounded payment PV',m.payment(10000,.005,24)*float(direct_factor(i,24)),F(10000))
    opening=F(10000);balances=[opening];interests=[];reductions=[]
    for _ in range(24):
        interest=opening*i;interests.append(interest)
        reduction=p-interest;reductions.append(reduction)
        opening-=reduction;balances.append(opening)
    first=m.first_period(10000,.005,24)
    for key,want in [('payment',p),('interest',interests[0]),('principal',reductions[0]),('balance',balances[1])]:
        close('P8/P9/P10 first period '+key,first[key],want)
    for k in (0,1,12,23,24):
        close('P10/P11 retrospective balance '+str(k),m.balance(10000,.005,24,k),balances[k])
    ck('exact schedule principal reconciles',sum(reductions)==10000 and balances[-1]==0)
    ck('exact interest decreases and principal increases',all(a>b for a,b in zip(interests,interests[1:])) and all(a<b for a,b in zip(reductions,reductions[1:])))
    close('zero-rate balance',m.balance(1200,0,12,3),F(900))
    display=commands[0]['stdout'].splitlines()
    ck('worked console displays independently rounded values',display==[f'Payment: {float(p):.2f}',f'Balance after 12: {float(balances[12]):.2f}'],expected_payment=round(float(p),2),expected_balance12=round(float(balances[12]),2))
    probe('F54 tiny rate payment',lambda:m.payment(.1,5e-324,1),F(1,10),0)
    probe('F54 tiny rate balance',lambda:m.balance(.1,5e-324,3,1),F(1,15),0)
    probe('F66 zero-rate balance cancellation',lambda:m.balance(1e308,0,10**18,10**18-1),F(1e308)/10**18,0)
    probe('F56 initial balance without representable payment',lambda:m.balance(1e308,1,1,0),F(1e308),0)
    probe('F66 one-period principal despite high interest',lambda:m.first_period(1,1e308,1)['principal'],F(1),0)
    probe('F66 one-period closing balance',lambda:m.first_period(1,1e308,1)['balance'],F(0),0)
    for label,fn in [
        ('F54 zero-rate payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 nonzero balance underflow',lambda:m.balance(5e-324,0,2,1)),
        ('F54 nonzero first interest underflow',lambda:m.first_period(5e-324,.5,1)),
        ('bad principal',lambda:m.payment(0,.01,12)),
        ('bad periodic rate',lambda:m.payment(100,-.01,12)),
        ('zero payment periods',lambda:m.payment(100,.01,0)),
        ('bool term',lambda:m.payment(100,.01,True)),
        ('past final payment',lambda:m.balance(100,.01,12,13)),
        ('fractional completed',lambda:m.balance(100,.01,12,1.5))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[1,2,3,12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
