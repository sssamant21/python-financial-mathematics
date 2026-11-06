"""Section 11.10 exact refinancing lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.10-refinancing-analysis.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1110-') as tmp:
        Path(tmp,'refinancing_analysis.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['refinancing_analysis.py']),('exact compilation',['-m','compileall','-q','refinancing_analysis.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and len(p.stdout.splitlines())==4 if args==['refinancing_analysis.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_refinancing');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def ref(L,r,n,H=0,d=0,upfront=0):
        L,r,d=map(lambda x:F(str(x)),(L,r,d))
        discount=1/(1+r)
        a=L/sum((discount**k for k in range(1,n+1)),F(0))
        b=L
        costs=F(upfront)
        for k in range(1,H+1):
            b=b+b*r-a
            costs+=a/(1+d)**k
        return a,b,costs+b/(1+d)**H
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e),independent_reference=str(want))
        else:close(label,value,want,atol=atol)
    old=(200000,.005,240); new=(200000,.00375,240)
    A=ref(*old)[0]; N=ref(*new)[0]; savings=A-N
    row=m.refinancing(*old,new[1],new[2],3000)
    for field,expected in [('old_payment',A),('new_payment',N),('monthly_savings',savings),('upfront_cost',3000),('new_principal',200000),('break_even_periods',math.ceil(3000/savings))]:
        numeric('worked cash comparison '+field,lambda:row[field],expected)
    financed=m.refinancing(*old,new[1],new[2],3000,True)
    numeric('P3 financed principal',lambda:financed['new_principal'],203000)
    numeric('P10 financed payment',lambda:financed['new_payment'],ref(203000,new[1],240)[0])
    numeric('P10 financed upfront',lambda:financed['upfront_cost'],0)
    numeric('P5 3,000 / 100 heuristic',lambda:m.refinancing(1200,0,3,0,4,3000)['break_even_periods'],30)
    ck('P6 no positive simple break-even',m.refinancing(*new,old[1],old[2],3000)['break_even_periods'] is None)
    extended=m.refinancing(*old,old[1],360)
    ck('P7 same-rate extension lowers payment and increases interest',extended['new_payment']<extended['old_payment'] and extended['new_payment']*360>extended['old_payment']*240)
    demonstrated=commands[0]['stdout'].splitlines()
    try: first=ast.literal_eval(demonstrated[0])
    except (IndexError,ValueError,SyntaxError):first={}
    ck('demo refinance fields',first==row)
    for j,H in enumerate((12,36,60),1):
        _,b,keep=ref(*old,H,.003)
        _,_,replace=ref(*new,H,.003,3000)
        numeric(f'P8 remaining balance at {H}',lambda:m.balance(*old,H),b)
        numeric(f'P9 keep PV at {H}',lambda:m.discounted_cost(*old,H,.003),keep)
        numeric(f'P9 refinance PV at {H}',lambda:m.discounted_cost(*new,H,.003,3000),replace)
        ck(f'P13/P14 demo PV savings at {H}',len(demonstrated)>j and demonstrated[j]==f'Months {H} PV savings {round(float(keep-replace),2)}',expected_savings=round(float(keep-replace),2))
    numeric('contract rate PV equals principal',lambda:m.discounted_cost(1000,.01,12,6,.01),1000)
    numeric('zero rate balance',lambda:m.balance(1200,0,12,5),700)
    numeric('maturity balance',lambda:m.balance(1000,.01,12,12),0)
    numeric('F56 opening endpoint independent of payment',lambda:m.balance(1e308,1,1,0),F('1e308'))
    numeric('F56 opening PV independent of payment',lambda:m.discounted_cost(1e308,1,1,0),F('1e308'))
    numeric('F56 finite PV at extreme discount',lambda:m.discounted_cost(100,0,2,2,1e200),ref(100,0,2,2,1e200)[2])
    numeric('F54 tiny-rate one-period installment',lambda:m.payment(.1,5e-324,1),F('0.1'))
    numeric('F73 exact break-even at three periods',lambda:m.refinancing(1,0,1,0,20,2.85)['break_even_periods'],3)
    numeric('F73 exact signed savings below rounded payment spacing',lambda:m.refinancing(1,0,1,1e-17,1)['monthly_savings'],-F('1e-17'))
    for label,fn in [
        ('F73 reject nonboolean finance flag',lambda:m.refinancing(1000,.01,12,.005,12,10,'cash')),
        ('F54 reject payment overflow',lambda:m.payment(1e308,1,1)),
        ('F54 reject payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 reject PV overflow',lambda:m.discounted_cost(1e308,0,1,1,0,1e308)),
        ('invalid horizon above term',lambda:m.discounted_cost(1000,.01,12,13)),
        ('invalid horizon bool',lambda:m.discounted_cost(1000,.01,12,True)),
        ('invalid negative discount',lambda:m.discounted_cost(1000,.01,12,6,-.01)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,conceptual_prompts=[1,11,12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
