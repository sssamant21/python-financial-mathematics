"""Section 10.15 exact acceptance lab and independent exercise benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.15-exercises-and-applied-problems.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1015-') as tmp:
        Path(tmp,'chapter10_acceptance.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['chapter10_acceptance.py']),('exact compilation',['-m','compileall','-q','chapter10_acceptance.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='' if args==['chapter10_acceptance.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('acceptance');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import date,timedelta
    from decimal import Decimal as D,localcontext
    def other(section):
        p,=source.parent.glob(section+'-*.md')
        raw,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',p.read_bytes(),re.M|re.S)
        n=types.ModuleType('exact_'+section);exec(compile(raw,str(p),'exec'),n.__dict__)
        linked[section]=hashlib.sha256(raw).hexdigest()
        return n
    linked={};level=other('10.08');grow=other('10.09');dated=other('10.11')
    def ref(flows,r,h=0):
        return sum((F(c)*(1+r)**(h-t) for t,c in flows),F(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    def money(x):
        with localcontext() as ctx:
            ctx.prec=100
            if isinstance(x,F):x=D(x.numerator)/D(x.denominator)
            return ('-' if x < 0 else '') + f'${abs(x):,.2f}'
    def printed(n,*expected,phrase=None):
        body=source.read_text().split(f'### Exercise {n} — ',1)[1].split('### Exercise ',1)[0]
        answer=body.split('**Worked answer:**',1)[1].split('\n\n',1)[0]
        values=[money(x) for x in expected]
        ck(f'E{n} published rounded answer',all(v in answer for v in values) and (phrase is None or phrase in answer),expected=values,required_phrase=phrase,answer=answer)
    r=F(1,10)
    for n,flows,rate in [(1,[(0,-2000),(1,700),(2,800),(3,900)],F(2,25)),(3,[(0,-100),(1,40),(2,-20)],r)]:
        close(f'E{n} signed timeline',m.pv(flows,float(rate)),ref(flows,rate))
    pv2=ref([(2,500)],F(3,50));fv2=ref([(2,500)],F(3,50),5)
    close('E2 value at 0',m.pv([(2,500)],.06),pv2)
    close('E2 value at 5',m.fv([(2,500)],.06,5),fv2)
    printed(2,pv2,fv2)
    for n,pay,count,rate,start in [(4,1000,5,F(7,100),1),(6,500,4,F(2,25),0),(7,300,3,F(3,50),4)]:
        value=ref([(k,pay) for k in range(start,start+count)],rate)
        close(f'E{n} annuity valuation',m.annuity(pay,count,float(rate),start),value)
        printed(n,value)
    fv5=ref([(k,250) for k in range(1,5)],F(1,20),4)
    close('E5 ordinary FV',m.fv([(k,250) for k in range(1,5)],.05,4),fv5);printed(5,fv5)
    pv8=ref([(1,100),(2,105),(3,F(441,4))],r)
    close('E8 growing annuity',m.growing(100,.05,3,.1),pv8);printed(8,pv8)
    close('E9 linked level perpetuity',level.perpetuity_pv(80,.08),F(1000))
    close('E10 linked growing perpetuity',grow.pv(100,.09,.03),F(5000,3))
    reject('E11 linked nonconvergence',lambda:grow.pv(100,.04,.05))
    mixed=[(0,-100),(1,60),(2,60)]
    close('E12 PV',m.pv(mixed,.1),F(500,121))
    close('E12 FV',m.fv(mixed,.1,2),F(5));printed(12,F(500,121),F(5))
    with localcontext() as ctx:
        ctx.prec=100
        dated13=D(365)/D('1.1')**(D(182)/365)
        monthly=D('1.08')**(D(1)/12)-1
        health=-D(2000)+D(1300)/D('1.08')**(D(1)/4)+D(900)/D('1.08')**(D(3)/4)
    anchor=date(2026,1,1)
    close('E13 linked ACT/365F source',dated.xnpv(.1,[(anchor+timedelta(days=182),365)],anchor),dated13)
    npv14=ref([(0,-500),(1,300),(2,300)],r)
    close('E14 investment NPV',m.pv([(0,-500),(1,300),(2,300)],.1),npv14);printed(14,npv14)
    for label,flows,lo,hi,want in [('E15 single root',[(0,-400),(1,460)],0,.5,F(3,20)),('E16 first root',[(0,-100),(1,230),(2,-132)],.05,.15,r),('E16 second root',[(0,-100),(1,230),(2,-132)],.15,.3,F(1,5))]:
        actual=m.bisect_irr(flows,lo,hi)
        close(label,actual,want)
        ck(label+' independent residual',abs(ref(flows,F(actual)))<F(1,10**7),residual=float(ref(flows,F(actual))))
    equipment=[]
    for cost,saving in [(4000,1200),(5000,1550)]:
        flows=[(0,-cost)]+[(k,saving) for k in range(1,5)]
        value=ref(flows,F(2,25));equipment.append(value)
        close(f'E17 cost={cost}',m.pv(flows,.08),value)
    ck('E17 benchmark selects B',equipment[1]>0>equipment[0])
    printed(17,*equipment,phrase='B has the higher NPV')
    close('E18 monthly model',m.pv([(0,-2000),(3,1300),(9,900)],float(monthly)),health)
    printed(18,health)
    scenario=[(0,-1000),(1,400),(2,450),(3,500)];grid=[]
    for rate in (F(1,20),r,F(3,20)):
        value=ref(scenario,rate);grid.append(value)
        close('E19 sensitivity '+str(rate),m.pv(scenario,float(rate)),value)
    ck('E19 all positive and decreasing',grid[0]>grid[1]>grid[2]>0)
    printed(19,*grid,phrase='all three')
    probe('F60 scaled IRR',lambda:m.bisect_irr([(0,-1e-200),(1,1.1e-200)],0,1),r)
    probe('F60 large bracket midpoint',lambda:m.bisect_irr([(0,-7e-309),(1,1)],1e308,1.7e308,1e296),1/F(7e-309)-1,0)
    probe('F65 iterator reused by bisection',lambda:m.bisect_irr(iter([(0,-100),(1,110)]),0,1),r)
    probe('F56 zero cash flow',lambda:m.fv([(0,0)],.1,10000),F(0))
    probe('F56 growing without overflowing power',lambda:m.growing(1e-308,1e308,3,0),F(1e-308)*sum(((1+F(1e308))**k for k in range(3)),F(0)),0)
    for label,fn in [
        ('F54 discounted term underflow',lambda:m.pv([(1,5e-324)],1)),
        ('F54 growing amount underflow',lambda:m.growing(5e-324,-.5,2,0)),
        ('F60 tiny same-sign bracket',lambda:m.bisect_irr([(0,-1e-200),(1,5e-201)],0,1)),
        ('F61 infinite tolerance',lambda:m.bisect_irr([(0,-100),(1,110)],0,1,float('inf'))),
        ('F62 indeterminate root',lambda:m.bisect_irr([(0,-100),(0,100)],0,1)),
        ('F63 boolean payment',lambda:m.pv([(0,True)],0)),
        ('F63 empty schedule validates payment',lambda:m.annuity(float('nan'),0,.1)),
        ('F63 negative period',lambda:m.pv([(-1,100)],.1)),
        ('F63 invalid growth',lambda:m.growing(100,-1,3,.1))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),linked_source_listing_sha256=linked,commands=commands,checks=checks,assessment_workflow_records=1,chapter_wide_answer_records=20,conceptual_prompts=[20],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
