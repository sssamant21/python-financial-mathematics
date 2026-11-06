"""Section 11.11 exact borrowing-cost lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-11/11.11-effective-borrowing-cost.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1111-') as tmp:
        Path(tmp,'effective_borrowing_cost.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['effective_borrowing_cost.py']),('exact compilation',['-m','compileall','-q','effective_borrowing_cost.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and len(p.stdout.splitlines())==4 if args==['effective_borrowing_cost.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_borrowing_cost');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def oracle(L,r,n,fee):
        with localcontext() as ctx:
            ctx.prec=65
            L,r,fee=(D(str(v)) for v in (L,r,fee))
            payment=L/sum(((1+r)**(-k) for k in range(1,n+1)),D(0))
            if not fee: return payment,r
            if n==1: return payment,payment/(L-fee)-1
            q=r
            for _ in range(50):
                discount=1/(1+q)
                total=sum((payment*discount**k for k in range(1,n+1)),D(0))
                slope=-sum((k*payment*discount**(k+1) for k in range(1,n+1)),D(0))
                step=(total-(L-fee))/slope
                q-=step
                if abs(step)<D("1e-58"):break
            else:raise RuntimeError("independent Newton iteration did not converge")
            return payment,q
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e),independent_reference=str(want))
        else:close(label,value,want,atol=atol)
    a,q=oracle(10000,.005,24,200)
    numeric('P1 net proceeds',lambda:m.net_proceeds(10000,200),9800)
    numeric('P2 contractual payment on face amount',lambda:m.payment(10000,.005,24),a)
    numeric('P3 P10 effective periodic root',lambda:m.periodic_irr(10000,.005,24,200),q)
    numeric('P4 no fee root',lambda:m.periodic_irr(10000,.005,24),F(1,200))
    _,q2=oracle(10000,.005,24,300)
    numeric('P5 higher fee root',lambda:m.periodic_irr(10000,.005,24,300),q2)
    ck('P5 monotonic fee effect',q2>q)
    numeric('P6 nominal annualization',lambda:m.annual_rates(.01)[0],F(12,100))
    numeric('P7 effective annualization',lambda:m.annual_rates(.01)[1],F(101,100)**12-1)
    ck('P8 effective exceeds nominal',m.annual_rates(.01)[1]>m.annual_rates(.01)[0])
    numeric('P9 zero note rate with fee',lambda:m.periodic_irr(1200,0,12,50),oracle(1200,0,12,50)[1])
    numeric('P11 PV reconciliation',lambda:m.pv_level(m.payment(10000,.005,24),m.periodic_irr(10000,.005,24,200),24),9800)
    want=[f'Net proceeds: {9800.0:g}',f'Periodic cost: {round(float(q),8)}',f'Annualized nominal: {round(float(12*q),6)}',f'Effective annual: {round(float((1+q)**12-1),6)}']
    lines=commands[0]['stdout'].splitlines()
    ck('demo reconciles to independent root',len(lines)==4 and lines[1:]==want[1:] and float(lines[0].split(': ')[1])==9800,expected=want)
    with localcontext() as ctx:
        ctx.prec=65
        fee=D("1e-100")
        b=3-4*fee
        # Stable positive root of 2(1-fee)q² + (3-4fee)q - 2fee = 0.
        expected_tiny=4*fee/(b+(b*b+16*(1-fee)*fee).sqrt())
    numeric('F74 very small positive two-period bisection root',lambda:m.periodic_irr(1,0,2,1e-100),expected_tiny)
    numeric('F74 very small positive one-period root',lambda:m.periodic_irr(1,0,1,1e-100),F('1e-100'))
    numeric('F74 subnormal-fee one-period root',lambda:m.periodic_irr(1,0,1,1e-310),F('1e-310'))
    numeric('F74 large finite root despite bracket doubling overflow',lambda:m.periodic_irr(1,1e308,1,.1),F('1e308')/F('.9'))
    numeric('F54 tiny positive note payment',lambda:m.payment(.1,5e-324,1),F('.1'))
    numeric('F54 finite PV avoids underflowing intermediate',lambda:m.pv_level(.1,5e-324,1),F('.1'))
    for label,fn in [
      ('F74 annualization rejects boolean rate',lambda:m.annual_rates(True)),
      ('F74 PV rejects boolean period',lambda:m.pv_level(100,.01,True)),
      ('F74 PV rejects negative installment',lambda:m.pv_level(-1,.01,12)),
      ('F74 PV rejects negative period',lambda:m.pv_level(100,.01,-1)),
      ('F54 annualization overflow',lambda:m.annual_rates(1e308,12)),
      ('F54 payment underflow',lambda:m.payment(5e-324,0,2)),
      ('F54 payment overflow',lambda:m.payment(1e308,1,1)),
      ('F54 PV overflow',lambda:m.pv_level(1e308,0,2)),
      ('invalid fees equal principal',lambda:m.periodic_irr(1000,.01,12,1000)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=14,conceptual_prompts=[12,13,14],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
