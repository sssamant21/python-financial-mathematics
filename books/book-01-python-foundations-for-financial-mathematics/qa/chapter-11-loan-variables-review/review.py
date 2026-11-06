"""Section 11.2 exact loan lab and independent rate and schedule benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.02-principal-rate-term-and-payment.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1102-') as tmp:
        Path(tmp,'loan_variables.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['loan_variables.py']),('exact compilation',['-m','compileall','-q','loan_variables.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout.startswith('Monthly payment: ') if args==['loan_variables.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_loan_variables');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    def unit(rate,n):
        return sum(((1+rate)**-k for k in range(1,n+1)),F(0))
    ck('P1 purchase minus down payment',300000-50000==250000)
    ck('P2 monthly count',15*12==180)
    ck('P3 quarterly count',5*4==20)
    close('P4 nominal monthly',m.monthly_rate_from_nominal_apr(.06),F(1,200))
    with localcontext() as ctx:
        ctx.prec=100
        monthly=(D('1.12').ln()/12).exp()-1
    close('P5 effective monthly',m.monthly_rate_from_annual_effective(.12),monthly)
    close('P6 zero-rate payment',m.payment(1200,0,12),F(100))
    close('P7 one-period payment',m.payment(100,.1,1),F(110))
    i=F(1,200);a=F(250000)/unit(i,360);cost=a*360-250000
    close('P8 worked mortgage payment',m.payment(250000,.005,360),a)
    close('worked total scheduled interest',m.interest_total(250000,.005,360),cost)
    ck('worked display',commands[0]['stdout'].splitlines()==[f'Monthly payment: {float(a):.2f}',f'Total scheduled interest: {float(cost):.2f}'])
    close('P9 inverse principal',m.principal_from_payment(float(a),.005,360),F(250000))
    close('P9 zero-rate inverse',m.principal_from_payment(100,0,12),F(1200))
    close('P10 doubled principal',m.payment(2000,.01,12),F(2000)/unit(F(1,100),12))
    for n in (12,24):
        p=F(1000)/unit(F(1,100),n)
        close(f'P11 payment n={n}',m.payment(1000,.01,n),p)
        close(f'P11 total interest n={n}',m.interest_total(1000,.01,n),p*n-1000)
    ck('P11 comparative trade-off',m.payment(1000,.01,24)<m.payment(1000,.01,12) and m.interest_total(1000,.01,24)>m.interest_total(1000,.01,12))
    close('higher-rate payment',m.payment(1000,.02,12),F(1000)/unit(F(1,50),12))
    probe('F54 tiny rate payment',lambda:m.payment(.1,5e-324,1),F(1,10),0)
    probe('F66 tiny positive interest',lambda:m.interest_total(1000,1e-18,12),F(1000)*(12/unit(F(1e-18),12)-1),0)
    probe('F66 smallest-rate positive interest',lambda:m.interest_total(1e100,5e-324,2),F(1e100)*(2/unit(F(5e-324),2)-1),0)
    probe('F56 finite interest without representable payment',lambda:m.interest_total(1e308,1,1),F(1e308),0)
    probe('zero interest at extreme principal',lambda:m.interest_total(1e308,0,3),F(0),0)
    for label,fn in [
        ('F54 zero-rate payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 nominal rate underflow',lambda:m.monthly_rate_from_nominal_apr(5e-324)),
        ('F54 effective rate underflow',lambda:m.monthly_rate_from_annual_effective(5e-324)),
        ('F54 inverse principal underflow',lambda:m.principal_from_payment(5e-324,1,1)),
        ('F54 inverse principal overflow',lambda:m.principal_from_payment(1e308,0,2)),
        ('F54 total interest overflow',lambda:m.interest_total(1e308,1,10)),
        ('invalid principal',lambda:m.payment(0,.01,12)),
        ('invalid rate',lambda:m.payment(100,-.01,12)),
        ('invalid term',lambda:m.payment(100,.01,0)),
        ('boolean annual rate',lambda:m.monthly_rate_from_annual_effective(True))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[12],supplemental_arithmetic=[1,2,3],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
