"""Section 10.14 exact capstone and independent valuation benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.14-chapter-project-cash-flow-valuation-engine.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),rational_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1014-') as tmp:
        Path(tmp,'cash_flow_engine.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['cash_flow_engine.py']),('exact compilation',['-m','compileall','-q','cash_flow_engine.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='NPV at 10%: 4.13\nIRR: 0.130662\n' if args==['cash_flow_engine.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_engine');sys.modules[m.__name__]=m;exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    r=F(1,10)
    def ref(flows,rate,horizon):
        return sum((F(v)*(1+rate)**(horizon-t) for t,v in flows),F(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    def records(pairs):
        return [m.CashFlow(t,v) for t,v in pairs]
    ck('P1 signed time-zero record',[(x.period,x.amount) for x in records([(0,-100)])]==[(0,-100)])
    for label,first in [('P2 ordinary',1),('P3 due',0),('P4 deferred',4)]:
        expected=[(k,50) for k in range(first,first+3)];actual=m.ordinary(50,3,first)
        ck(label+' schedule',[(x.period,x.amount) for x in actual]==expected)
        close(label+' valuation',m.value_at(actual,.1),ref(expected,r,0))
    expected=[(1,100),(2,105),(3,F(441,4))]
    actual=m.growing(100,.05,3)
    ck('P5 growing dates and amounts',all(x.period==t and math.isclose(x.amount,float(v),abs_tol=1e-12) for x,(t,v) in zip(actual,expected,strict=True)))
    close('P5 growing valuation',m.value_at(actual,.1),ref(expected,r,0))
    pairs=[(0,-100),(1,60),(2,60)];flows=records(pairs)
    close('P6 and P9 worked NPV',m.value_at(iter(flows),.1),F(500,121))
    close('P7 value at period five',m.value_at(flows,.1,5),ref(pairs,r,5))
    close('P8 reconciliation',m.value_at(flows,.1,5),ref(pairs,r,0)*(1+r)**5)
    close('value before last receipt',m.value_at(flows,.1,1),ref(pairs,r,1))
    close('repeated dates and signed receipts',m.value_at(records([(1,10),(1,-5),(1,25)]),.1),F(300,11))
    close('unsorted generator',m.value_at(iter(reversed(flows)),.1),ref(pairs,r,0))
    close('zero rate',m.value_at(flows,0,5),F(20))
    close('negative rate',m.value_at(records([(1,90)]),-.1),F(100))
    close('empty valuation',m.value_at([],r.numerator/r.denominator),F(0))
    with localcontext() as ctx:
        ctx.prec=100
        two=(D(69).sqrt()-7)/10
    for label,data,lo,hi,ref_rate in [
        ('P10 one period',[(0,-100),(1,110)],0,1,F(1,10)),
        ('worked quadratic',pairs,0,1,two),
        ('P11 first root',[(0,-100),(1,230),(2,-132)],.05,.15,F(1,10)),
        ('P11 second root',[(0,-100),(1,230),(2,-132)],.15,.3,F(1,5)),
        ('lower endpoint',[(0,-100),(1,100)],0,1,F(0)),
        ('upper endpoint',[(0,-100),(1,200)],0,1,F(1))]:
        root=m.irr(records(data),lo,hi)
        close(label,root,ref_rate)
        value=ref(data,F(root),0)
        ck(label+' independent residual and bracket',abs(value)<F(1,10**6) and lo<=root<=hi,residual=float(value))
    probe('F60 scaled IRR',lambda:m.irr(records([(0,-1e-200),(1,1.1e-200)])),F(1,10))
    probe('F60 large finite bracket midpoint',lambda:m.irr(records([(0,-7e-309),(1,1)]),1e308,1.7e308,1e296),1/F(7e-309)-1,0)
    probe('F56 zero amount with distant valuation period',lambda:m.value_at(records([(0,0)]),.1,10000),F(0))
    probe('F56 zero rate with huge integer date',lambda:m.value_at(records([(10**1000,40),(0,-10)]),0),F(30))
    probe('F56 growing avoids overflowing standalone power',lambda:m.growing(1e-308,1e308,3)[-1].amount,F(1e-308)*(1+F(1e308))**2,0)
    for label,fn in [
        ('P12 not a calendar-date engine',lambda:m.CashFlow('2026-01-01',1)),
        ('invalid record in IRR',lambda:m.irr([('not',100)])),
        ('invalid value_at rate',lambda:m.value_at([], -1)),
        ('F54 nonzero discount underflow',lambda:m.value_at(records([(1,5e-324)]),1)),
        ('F54 growing nonzero amount underflow',lambda:m.growing(5e-324,-.5,2)),
        ('F60 tiny same-sign bracket',lambda:m.irr(records([(0,-1e-200),(1,5e-201)]))),
        ('F61 infinite tolerance',lambda:m.irr(flows,tolerance=float('inf'))),
        ('F61 bool iteration cap',lambda:m.irr(records([(0,-100),(1,200)]),iterations=True)),
        ('F62 identically zero IRR',lambda:m.irr(records([(0,-100),(0,100)]))),
        ('F63 invalid empty ordinary payment',lambda:m.ordinary(float('nan'),0)),
        ('F63 invalid empty growing payment',lambda:m.growing(float('nan'),.05,0)),
        ('F63 bool first payment',lambda:m.growing(True,.05,2)),
        ('absent bracket',lambda:m.irr(records([(0,-100),(1,40)]),.1,.5))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,project_acceptance_records=6,conceptual_prompts=[12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
