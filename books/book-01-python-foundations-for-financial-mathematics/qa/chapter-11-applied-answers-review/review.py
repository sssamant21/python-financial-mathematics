"""Section 11.14 chapter assessment exact workflow and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.14-exercises-and-applied-problems.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1114-') as tmp:
        Path(tmp,'chapter_11_exercise_checks.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['chapter_11_exercise_checks.py']),('exact compilation',['-m','compileall','-q','chapter_11_exercise_checks.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['chapter_11_exercise_checks.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_assessment');exec(compile(code,str(source),'exec'),m.__dict__)
    def pmt(L,r,n):
        return L/sum(((1+r)**-j for j in range(1,n+1)),F(0))
    def reference(L,r,n,extra=0,once=None):
        L,r,extra=map(lambda x:F(str(x)),(L,r,extra))
        a=pmt(L,r,n);rows=[]
        for k in range(1,n+1):
            opening=L;interest=opening*r
            paid=min(a+(extra if once is None or k==once else 0),opening+interest)
            repaid=paid-interest
            L=opening-repaid
            rows.append((k,opening,interest,paid,repaid,L))
            if not L:break
        return rows
    def near(x,y):
        return math.isfinite(x) and math.isclose(x,float(y),rel_tol=1e-11,abs_tol=0)
    def check_rows(label,args):
        want=reference(*args); got=m.schedule(*args)
        ck(label,len(want)==len(got) and all(all(near(x,y) for x,y in zip(a,b)) for a,b in zip(got,want)),
           actual_periods=len(got),expected_periods=len(want),last=repr(got[-1]))
    a=(10000,.005,24);b=(240000,.005,360)
    x=reference(*a)
    for label,args in [('E4–E11 standard schedule',a),('E3 zero-rate schedule',(1200,0,12)),
        ('case baseline',b),('case recurring extra',(*b,200)),('cap on oversized extra',(1000,.01,12,2000)),
        ('F72 tiny principal term',(1e-10,0,4)),('F72 positive small residual',(1,0,2,.4999999999)),
        ('F66 high-rate principal stays nonzero',(1,1e100,2))]:check_rows(label,args)
    ck('E1 E2 conversion and periods',.06/12==.005 and 15*12==180 and 30*12==360)
    ck('E3 zero rate installment',m.payment(1200,0,12)==100)
    close('E4 reference installment',m.payment(*a),x[0][3])
    first=m.schedule(*a)[0]
    for label,j in [('E5 first interest',2),('E6 first principal',4),('E7 first closing',5)]:
        close(label,first[j],x[0][j])
    close('E8 prospective balance after ten',m.balance(*a,10),x[9][-1])
    G=F(201,200)**10
    close('E9 retrospective balance after ten',m.balance(*a,10),10000*G-x[0][3]*(G-1)/F(1,200))
    close('E11 total interest',math.fsum(row[2] for row in m.schedule(*a)),24*x[0][3]-10000)
    ck('E12 E13 principal and LTV',300000-60000==240000 and F(240000,300000)==F(4,5))
    close('E14 mortgage payment',m.payment(*b),pmt(F(240000),F(1,200),360))
    close('E15 housing estimate',m.payment(*b)+3600/12+1200/12,pmt(F(240000),F(1,200),360)+400)
    extra=m.schedule(*a,100)
    want=reference(*a,100)
    close('E16 first extra payment',extra[0][3],want[0][3])
    close('E16 first extra balance',extra[0][-1],want[0][-1])
    close('E17 second-period interest drops by 0.50',m.schedule(*a)[1][2]-extra[1][2],F(1,2))
    def interest(rows):return sum(row[2] for row in rows)
    early=reference(*a,500,once=2);late=reference(*a,500,once=20)
    ck('E18 supplemental one-time timing comparison',interest(early)<interest(late),early=float(interest(early)),late=float(interest(late)))
    o=pmt(F(200000),F(1,200),240);n=pmt(F(200000),F(3,800),240)
    close('E19 old installment',m.payment(200000,.005,240),o)
    close('E19 new installment',m.payment(200000,.00375,240),n)
    ck('E20 arithmetic threshold',F(3000,100)==30)
    close('E24 annualization',m.effective_annual(.01),F(101,100)**12-1)
    from decimal import Decimal as D, localcontext
    with localcontext() as ctx:
        ctx.prec=65
        payment=D(x[0][3].numerator)/D(x[0][3].denominator)
        ir=D(".005")
        for _ in range(20):
            df=1/(1+ir)
            pv=sum(payment*df**j for j in range(1,25))
            slope=-sum(j*payment*df**(j+1) for j in range(1,25))
            ir-=(pv-9800)/slope
        ck('E22 E23 independent root and net proceeds',9800==10000-200 and abs(pv-9800)<D("1e-55") and ir>D(".005"))
    close('E23 source cost reconciles to Newton benchmark',m.borrowing_cost(*a,200),ir,atol=0)
    close('F74 tiny borrowing cost',m.borrowing_cost(1,0,1,1e-100),F('1e-100'),atol=0)
    close('F54 tiny-rate payment',m.payment(.1,5e-324,1),F('.1'),atol=0)
    close('F56 opening endpoint',m.balance(1e308,1,1,0),F('1e308'),atol=0)
    for label,fn in [
        ('F54 nonfinite payment',lambda:m.payment(1e308,1,1)),
        ('F54 underflowed payment',lambda:m.payment(5e-324,0,2)),
        ('F54 annualization overflow',lambda:m.effective_annual(1e308,12)),
        ('F77 boolean principal',lambda:m.payment(True,0,1)),
        ('F77 boolean extra',lambda:m.schedule(*a,True)),
        ('F77 nonintegral annualization frequency',lambda:m.effective_annual(.01,1.5)),
        ('F77 NaN fee',lambda:m.borrowing_cost(*a,float('nan'))),
    ]:reject(label,fn)
    baseline,accelerated=reference(*b),reference(*b,200)
    lines=commands[0]['stdout'].splitlines()
    interest_saved=interest(baseline)-interest(accelerated)
    due=math.ceil(3000/(o-n))
    wanted=[f'Baseline: 360 payments, interest {round(float(interest(baseline)),2)}',
            f'Accelerated: {len(accelerated)} payments, interest {round(float(interest(accelerated)),2)}',
            f'Monthly payment: {float(baseline[0][3]):.2f}; first interest: {float(baseline[0][2]):.2f}',
            f'Interest saved: {float(interest_saved):.2f}; periods saved: {360-len(accelerated)}',
            f'Refinance: {float(o):.2f} -> {float(n):.2f}; monthly savings: {float(o-n):.2f}; simple break-even: {due}',
            'Reconciled: True True']
    for i,w in enumerate(wanted):ck('assessment demo '+str(i+1),len(lines)>i and lines[i]==w,expected=w)
    manuscript=source.read_text()
    for label,terms in [
        ('F77 written refinance answers',('1,432.86','1,265.30','167.56')),
        ('F77 written case outcomes',('278,011.65','192,926.32','85,085.34','265','95','18 months')),
    ]:ck(label,all(term in manuscript for term in terms),expected_terms=terms)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,chapterwide_answer_records=25,applied_case_records=4,conceptual_prompts=[21,25],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
