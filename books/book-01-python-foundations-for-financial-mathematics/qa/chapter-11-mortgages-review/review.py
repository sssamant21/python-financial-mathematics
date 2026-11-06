"""Section 11.8 exact mortgage lab and rational payment oracles."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.08-mortgages.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1108-') as tmp:
        Path(tmp,'mortgages.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['mortgages.py']),('direct invocation of exact embedded suite',['-m','unittest','-v','mortgages']),('exact compilation',['-m','compileall','-q','mortgages.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and (len(p.stdout.splitlines())==3 if args==['mortgages.py'] else not p.stdout) if label!='exact compilation' else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_mortgages');exec(compile(code,str(source),'exec'),m.__dict__)
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e),independent_reference=str(want))
        else:close(label,value,want,atol=atol)
    def pay(L,r,n):
        return F(L)/sum(((1+r)**-i for i in range(1,n+1)),F(0))
    L=240000;r=F(1,200);n=360;A=pay(L,r,n)
    A15=pay(L,r,180)
    numeric('P1 purchase principal',lambda:m.loan_from_purchase(300000,60000),L)
    numeric('P2 financed fee principal',lambda:m.loan_from_purchase(300000,60000,2000),242000)
    numeric('P3 valuation-based LTV',lambda:m.loan_to_value(L,300000),F(4,5))
    numeric('P4 count and P5 nominal rate through P6 payment',lambda:m.mortgage_payment(L,.06,30),A)
    numeric('P7 first interest using fixture periodic rate',lambda:L*(.06/12),1200)
    numeric('P8 first principal',lambda:m.mortgage_payment(L,.06,30)-L*.005,A-1200)
    numeric('P9 tax allowance',lambda:m.monthly_housing_cost(0,3600,0),300)
    numeric('P10 insurance allowance',lambda:m.monthly_housing_cost(0,0,1200),100)
    numeric('P11 housing allowance',lambda:m.monthly_housing_cost(m.mortgage_payment(L,.06,30),3600,1200),A+400)
    numeric('P13 fifteen-year payment',lambda:m.mortgage_payment(L,.06,15),A15)
    numeric('P13 thirty-year interest',lambda:n*m.mortgage_payment(L,.06,30)-L,n*A-L)
    numeric('P13 fifteen-year interest',lambda:180*m.mortgage_payment(L,.06,15)-L,180*A15-L)
    ck('P13 trade-off at positive rate',A<A15 and n*A-L>180*A15-L)
    numeric('zero-rate installment, integer years',lambda:m.mortgage_payment(1200,0,1),100)
    numeric('quarterly installment, integer years',lambda:m.mortgage_payment(1000,.12,1,4),pay(1000,F(3,100),4))
    numeric('fractional years, whole payment count',lambda:m.mortgage_payment(1200,.12,.25),pay(1200,F(1,100),3))
    numeric('decimal term and nonmonthly frequency',lambda:m.mortgage_payment(100,.2,.3,10),pay(100,F(1,50),3))
    numeric('F54 tiny one-period payment',lambda:m.mortgage_payment(.1,5e-324,1.0,1),F(1,10))
    numeric('large finite payment',lambda:m.mortgage_payment(1e308,1.5,2.0,2),pay(F(1e308),F(3,4),4))
    numeric('housing extras',lambda:m.monthly_housing_cost(1500,3600,1200,100,50),2050)
    for label,fn in [
        ('fractional payment count rejected',lambda:m.mortgage_payment(100,.06,.2)),
        ('F71 decimal term must give an exact whole count',lambda:m.mortgage_payment(100,.06,.3333333333333333,3)),
        ('invalid bool frequency',lambda:m.mortgage_payment(100,.06,1.0,True)),
        ('F54 payment underflow',lambda:m.mortgage_payment(5e-324,0,1.0)),
        ('F54 payment overflow',lambda:m.mortgage_payment(1e308,1,1.0,1)),
        ('F54 periodic rate underflow',lambda:m.mortgage_payment(1e308,5e-324,1.0,12)),
        ('F54 LTV overflow',lambda:m.loan_to_value(1e308,.1)),
        ('F54 LTV underflow',lambda:m.loan_to_value(5e-324,1e308)),
        ('F54 financed principal overflow',lambda:m.loan_from_purchase(1e308,0,1e308)),
        ('F54 housing cost overflow',lambda:m.monthly_housing_cost(1e308,0,0,1e308)),
        ('F54 housing cost underflow',lambda:m.monthly_housing_cost(0,5e-324,0))]:reject(label,fn)
    lines=['Principal: 240000 LTV: 0.8',f'Principal and interest: {float(A):.2f}',f'Illustrative housing cost: {float(A+400):.2f}']
    ck('three demonstration lines vs rational amounts',commands[0]['stdout'].splitlines()==lines,expected=lines)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,conceptual_prompts=[12,14],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
