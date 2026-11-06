"""Section 12.16 exact bond engine lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.16-chapter-project-bond-analytics-engine.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1216-') as tmp:
        Path(tmp,'bond_analytics_engine.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['bond_analytics_engine.py']),('isolated import',['-c','import bond_analytics_engine']),('exact compilation',['-m','compileall','-q','bond_analytics_engine.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['bond_analytics_engine.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_engine');sys.modules[m.__name__]=m;exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def pv(pos,bump=F(0)):
        face,c,n,f,y=pos
        value=F(str(face));c=value*F(str(c))/f
        base=1+(F(str(y))+bump)/f
        for _ in range(n):value=(value+c)/base
        return value
    def stats(pos):
        h=F('1e-8');v=pv(pos);u,d=pv(pos,h),pv(pos,-h)
        slope=(u-d)/(2*h);curvature=(u-2*v+d)/h**2
        mod=-slope/v
        return dict(price=v,macaulay=mod*(1+F(str(pos[-1]))/pos[3]),modified=mod,convexity=curvature/v,dv01=-slope/10000)
    def changes(pos,bp):
        dy=F(str(bp))/10000;a=stats(pos)
        linear=-a['price']*a['modified']*dy
        b=pv(pos,dy)
        return dict(exact=b-a['price'],duration=linear,duration_convexity=linear+a['price']*a['convexity']*dy**2/2,shocked_price=b)
    def matches(label,fn,want,rel=1e-12,atol=0):
        try: got=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,got.keys()==want.keys() and all(math.isclose(got[k],float(v),rel_tol=rel,abs_tol=atol) for k,v in want.items()),actual=repr(got),expected={k:float(v) for k,v in want.items()})
    def number(label,fn,want,atol=0):
        try:got=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,got,want,atol=atol)
    positions=[(1000,.06,6,2,.06),(2000,.04,10,2,.05),(1500,0,8,2,.045)]
    bonds=[(m.Bond(*pos[:4]),pos[-1]) for pos in positions]
    ck('A cash-flow table',bonds[0][0].cashflows()==[(k/2,30 if k<6 else 1030) for k in range(1,7)])
    ck('C single promised principal',bonds[2][0].cashflows()==[(k/2,0 if k<8 else 1500) for k in range(1,9)])
    lines=commands[0]['stdout'].splitlines()
    for idx,(pos,(bond,y)) in enumerate(zip(positions,bonds)):
        want=stats(pos)
        matches(f'bond {idx+1} base analytics',lambda:m.analytics(bond,y),want)
        number(f'bond {idx+1} roundtrip from independent price',lambda:m.solve_ytm(bond,float(want['price'])),F(str(y)),atol=1e-12)
        expected={k:round(float(v),6) for k,v in want.items()}
        ck(f'demo bond {idx+1} metrics and yield',len(lines)==12 and ast.literal_eval(lines[2*idx].split(' ',2)[2])==expected and float(lines[2*idx+1].split(': ')[1])==y)
    for idx,bp in enumerate((-200,-100,-50,50,100,200),6):
        inputs=[changes(p,bp) for p in positions]
        want={k:sum(row[k] for row in inputs) for k in ('exact','duration','duration_convexity')}
        for j,((bond,y),w) in enumerate(zip(bonds,inputs),1):
            matches(f'{bp:+} bp bond {j}',lambda:m.scenario(bond,y,bp),w,atol=1e-10)
        matches(f'{bp:+} bp portfolio P&L',lambda:m.portfolio_scenario(bonds,bp),want,atol=1e-10)
        matches(f'{bp:+} bp demo portfolio',lambda:ast.literal_eval(lines[idx].split(' bp ',1)[1]),want,atol=1e-10)
        ck(f'{bp:+} bp quadratic improves aggregate',abs(want['exact']-want['duration_convexity'])<abs(want['exact']-want['duration']))
    A=bonds[0][0]
    number('flat effective spot at 6.09% reconciles to par',lambda:m.spot_price(A,{k/2:.0609 for k in range(1,7)}),1000)
    from decimal import Decimal as D, localcontext
    with localcontext() as ctx:
        ctx.prec=65
        curve={k/2:float(F(30+k,1000)) for k in range(1,7)}
        want=sum(D(30 if k<6 else 1030)/(1+D(str(curve[k/2])))**(D(k)/2) for k in range(1,7))
    number('nonflat spot valuation uses each date',lambda:m.spot_price(A,curve),want)
    number('F93 tiny notional YTM respects relative residual',lambda:m.solve_ytm(m.Bond(1e-30,0,1,1),8e-31),F('.25'))
    matches('F93 tiny shock survives subtraction',lambda:m.scenario(A,.06,1e-21),changes(positions[0],1e-21))
    number('F54 finite spot PV despite discount underflow',lambda:m.spot_price(m.Bond(1e308,0,1000,1),{k:2 for k in range(1,1001)}),float(F('1e308')/3**1000))
    for label,fn in [
        ('F93 reject invalid solver tolerance',lambda:m.solve_ytm(A,950,tolerance=True)),
        ('F93 reject unachievable solver tolerance',lambda:m.solve_ytm(A,950,tolerance=1e-30)),
        ('reject bracket without root',lambda:m.solve_ytm(A,1000,low=.07,high=.08)),
        ('reject missing spot date',lambda:m.spot_price(A,{.5:.04})),
        ('reject invalid shock',lambda:m.scenario(A,.06,True)),
        ('F54 reject overflowing analytics',lambda:m.analytics(m.Bond(1e308,0,3,1),-.5)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,project_deliverable_records=6,conceptual_prompts=[17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
