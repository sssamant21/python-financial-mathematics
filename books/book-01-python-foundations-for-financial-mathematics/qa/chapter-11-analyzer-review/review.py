"""Section 11.13 loan analyzer exact workflow and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.13-chapter-project-loan-and-mortgage-analyzer.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1113-') as tmp:
        Path(tmp,'loan_mortgage_analyzer.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['loan_mortgage_analyzer.py']),('exact compilation',['-m','compileall','-q','loan_mortgage_analyzer.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['loan_mortgage_analyzer.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_analyzer');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def pmt(L,r,n):
        return L/sum(((1+r)**-i for i in range(1,n+1)),F(0))
    def reference(L,r,n,extra=0,start=1):
        B,r,extra=map(lambda x:F(str(x)),(L,r,extra))
        a=pmt(B,r,n)
        rows=[]
        for k in range(1,n+1):
            interest=B*r
            due=B+interest
            scheduled=min(a,due)
            add=min(extra,due-scheduled) if k>=start else F(0)
            paid=scheduled+add
            principal=paid-interest
            closing=B-principal
            rows.append(dict(period=k,opening=B,interest=interest,scheduled=scheduled,extra=add,payment=paid,principal=principal,closing=closing))
            if not closing:break
            B=closing
        return rows
    def same(a,b):
        return math.isfinite(a) and math.isclose(a,float(b),rel_tol=1e-11,abs_tol=0)
    def totals(rows):
        return dict(periods=len(rows),total_interest=sum(x['interest'] for x in rows),total_paid=sum(x['payment'] for x in rows),final_balance=rows[-1]['closing'])
    def record(label,args):
        want=reference(*args)
        try:rows=m.schedule(*args)
        except Exception as e:ck(label,False,exception=repr(e));return
        ok=len(rows)==len(want) and all(x.keys()==y.keys() and all(same(x[k],y[k]) for k in y) for x,y in zip(rows,want))
        ck(label,ok,actual_periods=len(rows),expected_periods=len(want),last=repr(rows[-1]),expected_last={k:float(v) for k,v in want[-1].items()})
    base=(240000,.005,360); fast=(*base,200)
    for label,args in [('Phase A 360 baseline rows',base),('Phase B all accelerated rows',fast),
                       ('delayed extra', (10000,.005,24,100,12)),('zero rate',(1200,0,12)),
                       ('payoff cap',(1000,.01,12,2000)),('F72 tiny principal retains term',(1e-10,0,4)),
                       ('F72 positive post-extra residual',(1,0,2,.4999999999)),
                       ('F66 cancellation-safe principal at high rate',(1,1e100,2))]:
        record(label,args)
    refs=[reference(*base),reference(*fast)]
    wants=list(map(totals,refs))
    base_rows=m.schedule(*base); fast_rows=m.schedule(*fast)
    for name,rs,w in zip(('baseline','accelerated'),(base_rows,fast_rows),wants):
        out=m.summary(rs)
        for k,v in w.items():close(name+' '+k,out[k],v,atol=0)
        ck('Phase C valid '+name+' audit',m.audit(rs,240000))
    close('P5 first interest',base_rows[0]['interest'],1200)
    close('P6 uncapped first extra',fast_rows[0]['payment'],refs[0][0]['payment']+200)
    close('P7 interest saved',m.summary(base_rows)['total_interest']-m.summary(fast_rows)['total_interest'],wants[0]['total_interest']-wants[1]['total_interest'])
    ck('P8 periods saved',len(base_rows)-len(fast_rows)==len(refs[0])-len(refs[1]))
    want_balance=refs[0][59]['closing']
    close('Phase D balance after 60',m.remaining_balance(*base,60),want_balance)
    close('Phase D maturity balance',m.remaining_balance(*base,360),0,atol=0)
    close('F56 opening endpoint independent of payment',m.remaining_balance(1e308,1,1,0),F('1e308'),atol=0)
    old=pmt(F(200000),F(1,200),240); new=pmt(F(200000),F(3,800),240)
    rr=m.refinance(200000,.005,240,.00375,240,3000)
    for k,v in dict(old_payment=old,new_payment=new,monthly_saving=old-new,simple_break_even=math.ceil(3000/(old-new))).items():close('Phase E '+k,rr[k],v)
    ck('P13 3000 / 100 heuristic',m.refinance(1200,0,3,0,4,3000)['simple_break_even']==30)
    ck('F73 exact threshold before ceiling',m.refinance(1,0,1,0,20,2.85)['simple_break_even']==3)
    close('F73 distinguish rounded-equal installments',m.refinance(1,0,1,1e-17,1)['monthly_saving'],-F('1e-17'),atol=0)
    for label,key,value in [('F76 incorrect scheduled plus extra','extra',100),('F76 invalid first period','period',9),('F76 negative scheduled','scheduled',-10)]:
        rows=[x.copy() for x in base_rows];rows[0][key]=value
        ck(label,not m.audit(rows,240000))
    ck('F76 tiny false payoff rejected',not m.audit(m.schedule(1e-10,0,4)[:1],1e-10))
    ck('F76 inconsistent original rejected',not m.audit(base_rows,250000))
    for label,fn in [
        ('F54 payment overflow',lambda:m.payment(1e308,1,1)),
        ('F54 payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 row interest underflow',lambda:m.schedule(5e-324,.25,1)),
        ('F54 aggregate overflow',lambda:m.summary(m.schedule(1e308,.75,2))),
        ('invalid extra start',lambda:m.schedule(*base,10,True)),
    ]:reject(label,fn)
    lines=dict(line.split(': ',1) for line in commands[0]['stdout'].splitlines())
    for key,want in zip(('Base','Extra $200'),wants):
        out=ast.literal_eval(lines[key])
        ck('demo '+key,all(same(out[k],v) for k,v in want.items()))
    ck('demo interest savings',float(lines['Interest saved'])==round(float(wants[0]['total_interest']-wants[1]['total_interest']),2))
    ck('demo audit pair',lines['Audits']=='True True')
    ck('F76 demo includes Phase D balance',lines.get('Balance after 60 payments')==f'{float(want_balance):.2f}')
    ck('demo refinance',ast.literal_eval(lines['Refinance'])==rr)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,project_acceptance_records=12,conceptual_prompts=[14],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
