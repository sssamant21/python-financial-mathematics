"""Section 10.12 exact lab and independent NPV benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.12-net-present-value.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1012-') as tmp:
        Path(tmp,'net_present_value.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['net_present_value.py']),('exact compilation',['-m','compileall','-q','net_present_value.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Example NPV: 4.13\n' if args==['net_present_value.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_npv');exec(compile(code,str(source),'exec'),m.__dict__)
    def ref(rate,flows):
        return sum((F(v)/(1+rate)**t for t,v in enumerate(flows)),F(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    r=F(1,10);flows=[-100,60,60]
    for label,data,rate in [('P2 initial cost',[-100],r),('P3 one-year receipt',[0,110],r),('P4 break-even',[-100,110],r),('P5 positive NPV',flows,r),('P6 negative NPV',[-100,40,40],r),('P7 zero rate',[-100,50,75],F(0)),('negative rate',[-100,90],-r),('nonconventional',[-100,230,-132],r),('empty',[],r)]:
        close(label,m.npv(float(rate),iter(data)),ref(rate,data))
    for r2 in (F(1,20),r,F(3,20)):
        close('P10 sensitivity '+str(r2),m.npv(float(r2),flows),ref(r2,flows))
    ck('P10 conventional sensitivity ordering',m.npv(.05,flows)>m.npv(.1,flows)>m.npv(.15,flows))
    close('P11 profitability index',m.profitability_index(.1,iter(flows)),ref(r,[0,60,60])/100)
    close('P11 zero receipts PI',m.profitability_index(.1,[-100,0]),F(0))
    for t,(period,value) in enumerate(m.discounted_components(.1,iter(flows))):
        ck(f'component period {t}',period==t)
        close(f'component amount {t}',value,F(flows[t])/(1+r)**t)
    close('component sum equals independent NPV',math.fsum(v for _,v in m.discounted_components(.1,flows)),ref(r,flows))
    close('signed cancellation',m.npv(0,[1e16,1,-1e16]),F(1))
    probe('F56 components need not form overflowing power',lambda:m.discounted_components(1e308,[0,0,0])[2][1],F(0),0)
    probe('F56 zero future flow need not form overflowing factor',lambda:m.npv(-.9,[0]*400),F(0),0)
    for label,fn in [
        ('F54 discount factor underflow',lambda:m.npv(1e308,[0,0,100])),
        ('F54 payment underflow',lambda:m.npv(1,[0,5e-324])),
        ('F54 PI overflow',lambda:m.profitability_index(0,[-5e-324,1])),
        ('F54 PI underflow',lambda:m.profitability_index(0,[-1e308,5e-324])),
        ('F59 PI nonfinite initial cost',lambda:m.profitability_index(.1,[-float('inf'),100])),
        ('F59 PI NaN initial cost',lambda:m.profitability_index(.1,[float('nan'),100])),
        ('invalid rate',lambda:m.npv(-1,flows)),
        ('invalid receipt',lambda:m.npv(.1,[-100,float('nan')])),
        ('nonconventional PI rejected',lambda:m.profitability_index(.1,[-100,50,-20])),
        ('nonnegative initial cost',lambda:m.profitability_index(.1,[100,20]))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[1,8,9,12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
