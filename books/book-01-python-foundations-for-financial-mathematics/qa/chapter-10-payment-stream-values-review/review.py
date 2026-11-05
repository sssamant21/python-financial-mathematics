"""Section 10.10 exact lab and independent signed-stream benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.10-present-and-future-values-of-payment-streams.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1010-') as tmp:
        Path(tmp,'payment_stream_values.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['payment_stream_values.py']),('exact compilation',['-m','compileall','-q','payment_stream_values.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='PV = -17.66\n' if args==['payment_stream_values.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_payment_streams');exec(compile(code,str(source),'exec'),m.__dict__)
    rate=F(1,10);mixed=[(0,-500),(1,200),(3,400)]
    def value_ref(flows,i,horizon):
        return sum((F(amount)*(1+i)**(horizon-period) for period,amount in flows),F(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    close('P1 single dated PV',m.pv([(3,100)],.1),value_ref([(3,100)],rate,0))
    for horizon in (1,3,5):
        close(f'P2 single flow at horizon={horizon}',m.value_at([(3,100)],.1,horizon),value_ref([(3,100)],rate,horizon))
    close('P3 time zero outflow',m.pv([(0,-500)],.1),F(-500))
    for label,start in [('P4 ordinary',1),('P5 due',0),('P6 deferred',3)]:
        flows=[(start+k,100) for k in range(3)]
        got=m.level_stream(100,start,3)
        ck(label+' dates and amounts',got==flows,actual=got)
        close(label+' PV',m.pv(got,.1),value_ref(flows,rate,0))
    close('P7 repeated date',m.pv([(1,50),(1,25)],.1),F(750,11))
    close('P8 zero rate',m.pv([(1,100),(4,200)],0),F(300))
    close('P9 negative rate',m.pv([(1,100)],-.1),F(1000,9))
    close('P10 worked mixed PV',m.pv(mixed,.1),value_ref(mixed,rate,0))
    close('P11 mixed terminal value',m.fv(mixed,.1,3),F(-47,2))
    close('P11 same PV-to-FV identity',m.fv(mixed,.1,3),value_ref(mixed,rate,0)*(1+rate)**3)
    close('P12 source level stream direct sum',m.pv(m.level_stream(100,1,3),.1),value_ref([(1,100),(2,100),(3,100)],rate,0))
    close('ordinary terminal FV',m.fv(m.level_stream(100,1,3),.1,3),F(331))
    close('unsorted generator',m.pv(iter(reversed(mixed)),.1),value_ref(mixed,rate,0))
    close('empty stream',m.value_at([],.05,3),F(0))
    close('fsum mixed signs',m.pv([(0,1e16),(0,1),(0,-1e16)],.05),F(1))
    probe('F56 zero cash flow needs no factor',lambda:m.value_at([(0,0)],.1,10000),F(0),0)
    probe('F56 zero rate needs no date conversion',lambda:m.value_at([(10**1000,100),(0,-60)],0,10**1000),F(40),0)
    for label,fn in [
        ('F54 discount factor underflow',lambda:m.pv([(10000,100)],.1)),
        ('F54 nonzero payment underflow',lambda:m.pv([(1,5e-324)],1)),
        ('invalid rate',lambda:m.pv([(1,100)],-1)),
        ('invalid amount',lambda:m.pv([(1,float('nan'))],.1)),
        ('invalid period',lambda:m.pv([(-1,100)],.1)),
        ('bool period',lambda:m.pv([(True,100)],.1)),
        ('fractional horizon',lambda:m.fv([(1,100)],.1,2.5)),
        ('negative count',lambda:m.level_stream(100,1,-1))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,supplemental_audit=[12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
