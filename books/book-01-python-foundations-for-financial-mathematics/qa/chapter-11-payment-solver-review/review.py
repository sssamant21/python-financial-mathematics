"""Section 11.4 exact payment lab and independent balloon cash-flow benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.04-solving-for-payment.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1104-') as tmp:
        Path(tmp,'solving_for_payment.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['solving_for_payment.py']),('exact compilation',['-m','compileall','-q','solving_for_payment.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout.startswith('Monthly payment: ') if args==['solving_for_payment.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_payment_solver');exec(compile(code,str(source),'exec'),m.__dict__)
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    def unit(rate,n):
        return sum(((1+rate)**-k for k in range(1,n+1)),F(0))
    i=F(1,200);n=360;L=250000
    a=F(L)/unit(i,n)
    close('P1/P6 worked payment',m.payment(L,.005,n),a)
    close('P2 zero-rate payment',m.payment(1200,0,12),F(100))
    close('P3 one-period payment',m.payment(100,.1,1),F(110))
    ck('P4 supplemental nominal monthly arithmetic',F(6,100)/12==i)
    ck('P5 supplemental payment count',30*12==n)
    ck('worked display',commands[0]['stdout']==f'Monthly payment: {float(a):.2f}\n')
    close('P7 independent PV from solved payment',float(unit(i,n))*m.payment(L,.005,n),F(L))
    rate=F(1,100)
    for label,r,count in [('P8 higher rate',F(1,50),12),('P9 longer term',rate,24),('ordinary comparator',rate,12)]:
        close(label,m.payment(1000,float(r),count),F(1000)/unit(r,count))
    ck('P8/P9 ordered sensitivities',m.payment(1000,.02,12)>m.payment(1000,.01,12)>m.payment(1000,.01,24))
    opening=F(L);interest=F(0)
    for _ in range(n):
        accrued=opening*i;interest+=accrued;opening=opening+accrued-a
    ck('P10 supplemental total interest reconciliation',a*n-L==interest and opening==0)
    close('P11 inverse principal',m.present_value_of_payments(float(a),.005,n),F(L))
    close('P11 zero-rate inverse',m.present_value_of_payments(100,0,12),F(1200))
    k=12;B=200
    adjusted=(1000-B/(1+rate)**k)/unit(rate,k)
    actual=m.payment_with_balloon(1000,.01,k,B)
    close('P12 balloon regular payment',actual,adjusted)
    close('P12 independent PV with additional balloon',actual*float(unit(rate,k))+float(B/(1+rate)**k),F(1000))
    ck('P12 lowers scheduled payment',0<actual<m.payment(1000,.01,k))
    close('zero-rate balloon',m.payment_with_balloon(1000,0,4,200),F(200))
    close('zero balloon ordinary',m.payment_with_balloon(1000,.01,12,0),F(1000)/unit(rate,12))
    close('first interest',m.first_interest(1000,.01,12),F(10))
    close('zero-rate first interest',m.first_interest(1200,0,12),F(0))
    probe('F54 tiny rate payment',lambda:m.payment(.1,5e-324,1),F(1,10),0)
    probe('F56 finite balloon despite overflowing ordinary payment',lambda:m.payment_with_balloon(1e308,1,1,1e308),F(1e308),0)
    probe('F56 long balloon horizon',lambda:m.payment_with_balloon(100,1,2000,200),(100-F(200,2**2000))/unit(F(1),2000),0)
    probe('F66 tiny positive balloon installment',lambda:m.payment_with_balloon(100,5e-324,1,100),100*F(5e-324),0)
    for label,fn in [
        ('F54 payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 inverse underflow',lambda:m.present_value_of_payments(5e-324,1,1)),
        ('F54 inverse overflow',lambda:m.present_value_of_payments(1e308,0,2)),
        ('F54 first interest underflow',lambda:m.first_interest(5e-324,.5,1)),
        ('F54 first interest overflow',lambda:m.first_interest(1e308,2,1)),
        ('F67 first interest negative rate',lambda:m.first_interest(100,-.1,1)),
        ('F67 first interest invalid term',lambda:m.first_interest(100,.1,0)),
        ('F67 first interest invalid principal',lambda:m.first_interest(True,.1,1)),
        ('nonpositive balloon schedule',lambda:m.payment_with_balloon(100,.25,1,125)),
        ('negative balloon',lambda:m.payment_with_balloon(100,.1,1,-1))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,supplemental_arithmetic=[4,5,10],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
