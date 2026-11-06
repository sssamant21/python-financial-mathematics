"""Section 13.10 exact money-weighted returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.10-money-weighted-return.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1310-') as tmp:
        Path(tmp,'money_weighted_return.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['money_weighted_return.py']),('isolated import',['-c','import money_weighted_return']),('exact compilation',['-m','compileall','-q','money_weighted_return.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['money_weighted_return.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_mwr');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import date, datetime
    from decimal import Decimal as D, localcontext
    def num(label,fn,want,atol=1e-10):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    def quadratic(end):
        with localcontext() as ctx:
            ctx.prec=50
            return ((D(2500+400*end).sqrt()-50)/200)-1
    contribution=quadratic(180); loss=quadratic(144)
    a=date(2025,1,1);z=date(2026,1,1)
    dated=[(a,-100),(z,110)]
    both=[-100,230,-132]
    for label,fn,want in [
        ('E1 gain',lambda:m.irr_bisection([-100,110]),.1),
        ('E2 loss',lambda:m.irr_bisection([-100,90]),-.1),
        ('E3 square root',lambda:m.irr_bisection([-100,0,121]),.1),
        ('E4 zero',lambda:m.irr_bisection([-100,100]),0),
        ('E8 quadratic',lambda:m.irr_bisection([-100,-50,180]),contribution),
        ('E10 quadratic',lambda:m.irr_bisection([-100,-50,144]),loss),
        ('E12 365 day annual rate',lambda:m.xirr_bisection(dated),.1),
        ('E13 zero residual',lambda:m.npv(.1,[-100,110]),0),
        ('E14 lower bracket root',lambda:m.irr_bisection(both,low=0,high=.15),.1),
        ('E14 upper bracket root',lambda:m.irr_bisection(both,low=.15,high=.25),.2),
        ('§10 terminal proceeds with distribution',lambda:m.irr_bisection([-100,115]),.15),
        ('F104 tiny-scale periodic root',lambda:m.irr_bisection([-1e-250,1.125e-250]),.125),
        ('F104 tiny-scale dated root',lambda:m.xirr_bisection([(a,-1e-250),(z,1.125e-250)]),.125),
        ('F104 dated upper endpoint',lambda:m.xirr_bisection([(a,-100),(z,112.5)],low=0,high=.125),.125),
        ('F104 dated lower endpoint',lambda:m.xirr_bisection([(a,-100),(z,112.5)],low=.125,high=.5),.125),
    ]:num(label,fn,want,0 if 'endpoint' in label else 1e-10)
    for label,fn in [
        ('E15 same sign bracket may contain two roots',lambda:m.irr_bisection(both,low=0,high=.3)),
        ('F104 scaled same sign bracket',lambda:m.irr_bisection([-1e-250,2e-250],low=0,high=.5)),
        ('F104 reverse bracket',lambda:m.irr_bisection([-100,112.5],low=.5,high=0)),
        ('F104 zero-width endpoint',lambda:m.xirr_bisection([(a,-100),(z,112.5)],low=.125,high=.125)),
        ('F104 infinite tolerance',lambda:m.irr_bisection([-100,112.5],tolerance=math.inf)),
        ('F104 boolean tolerance',lambda:m.xirr_bisection(dated,tolerance=True)),
        ('F104 boolean rate',lambda:m.npv(True,[-100,110])),
        ('F104 fractional iteration count',lambda:m.irr_bisection([-100,110],max_iterations=1.5)),
        ('F104 dates decrease after the first date',lambda:m.xnpv(.1,[(a,-100),(z,10),(date(2025,7,1),100)])),
        ('F104 timestamps must not silently discard hours',lambda:m.xnpv(.1,[(datetime(2025,1,1),-100),(datetime(2026,1,1,12),110)])),
        ('F104 same-date cancellation is not a unique root',lambda:m.xirr_bisection([(a,-100),(a,100)])),
        ('F104 all-date cancellation is not a unique root',lambda:m.xirr_bisection([(a,-100),(a,100),(z,-10),(z,10)])),
    ]:reject(label,fn)
    num('366 days under Actual/365 Fixed',lambda:m.xirr_bisection([(date(2024,1,1),-100),(date(2025,1,1),110)]),1.1**(365/366)-1)
    from benchmark import project_rows, terminal_root
    rows=project_rows()
    for label,data in [('base',rows),('terminal haircut',rows[:-1]+[(z,10795)])]:
        days=[(d-a).days for d,_ in data]
        expected=terminal_root([x for _,x in data],[(365-i,365) for i in days])
        num('project '+label+' XIRR',lambda:m.xirr_bisection(data),expected)
        num('project '+label+' XNPV residual',lambda:m.xnpv(m.xirr_bisection(data),data),0,1e-7)
    expected=terminal_root([x for _,x in rows],[(3-i,1) for i in range(4)])
    num('project equal intervals',lambda:m.irr_bisection([x for _,x in rows]),expected)
    ck('project signed capital and multiple',F(500+12700,12000)==F(11,10) and F(500+10795,12000)==F(753,800))
    prose=source.read_text()
    ck('F104 printed exercise rates agree with closed form',prose.count(f'{contribution:.2%}')>=2 and prose.count(f'−{abs(loss):.2%}')>=2)
    ck('exact demo',commands[0]['stdout'].splitlines()[0]==f'Periodic money-weighted return: {contribution:.4%}' and abs(float(commands[0]['stdout'].splitlines()[1].split(': ')[1]))<=1e-8)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
