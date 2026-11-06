"""Section 12.12 exact interest-rate sensitivity lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.12-interest-rate-sensitivity.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1212-') as tmp:
        Path(tmp,'interest_rate_sensitivity.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['interest_rate_sensitivity.py']),('exact compilation',['-m','compileall','-q','interest_rate_sensitivity.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['interest_rate_sensitivity.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_portfolio');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def price(pos,shift=F(0)):
        face,c,n,y,*freq=pos
        f=freq[0] if freq else 2
        value=F(str(face));coupon=value*F(str(c))/f
        base=1+(F(str(y))+shift)/f
        for _ in range(n):value=(value+coupon)/base
        return value
    def stats(pos):
        h=F('1e-8');p=price(pos)
        d,u=price(pos,-h),price(pos,h)
        return p,(u-d)/(2*h),(u-2*p+d)/h**2
    def model(pos,bp):
        p,dp,ddp=stats(pos); dy=F(str(bp))/10000
        return dict(exact=float(price(pos,dy)-p),duration=float(dp*dy),second_order=float(dp*dy+ddp*dy**2/2))
    def matches(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,value.keys()==want.keys() and all(math.isclose(value[k],float(v),rel_tol=1e-12,abs_tol=atol) for k,v in want.items()),actual=repr(value),expected={k:float(v) for k,v in want.items()})
    def analytics(totals):
        p,dp,ddp=totals
        return dict(price=p,duration=-dp/p,convexity=ddp/p,dv01=-dp/10000)
    positions=[(1000,.06,6,.06,2),(2000,.04,10,.05,2),(1500,0,8,.045,2)]
    totals=tuple(sum(v) for v in zip(*(stats(p) for p in positions)))
    for i,pos in enumerate(positions,1):
        matches(f'project bond {i} analytics',lambda:m.bond(*pos),analytics(stats(pos)))
    matches('F89 source portfolio base analytics',lambda:m.portfolio_analytics(positions),analytics(totals))
    for bp in (-200,-100,-50,50,100,200):
        components=[model(pos,bp) for pos in positions]
        want={k:math.fsum(row[k] for row in components) for k in components[0]}
        matches(f'F89 project portfolio common {bp:+} bp with explicit frequency',lambda:m.portfolio(positions,bp),want,atol=1e-10)
        component_outputs=[m.shock(*pos[:4],bp,pos[4]) for pos in positions]
        ck(f'project {bp:+} bp component reconciliation',all(math.isclose(math.fsum(row[k] for row in component_outputs),v,rel_tol=1e-12) for k,v in want.items()))
        ck(f'project {bp:+} bp quadratic improves',abs(want['exact']-want['second_order'])<abs(want['exact']-want['duration']))
    quarterly=(1500,0,16,.045,4)
    mixed=[positions[0][:4],quarterly]
    c1,c2=[model(pos,37.5) for pos in mixed]
    matches('F89 mixed frequencies and fractional bp',lambda:m.portfolio(mixed,37.5),{k:c1[k]+c2[k] for k in c1},atol=1e-10)
    p0=positions[0][:4]
    close('DV01 scales with face',m.bond(10000,.06,6,.06)['dv01'],float(analytics(stats(p0))['dv01']*10),atol=0)
    matches('zero shock all outputs',lambda:m.portfolio([p0],0),dict(exact=0,duration=0,second_order=0))
    matches('F89 tiny exact price change',lambda:m.shock(*p0,1e-21),model(p0,1e-21))
    ck('P6–P11 exercise basis points and P&L',F(50,10000)==F('.005') and 2700*F('.005')==F('13.5') and 1000-F('13.5')==F('986.5') and 2700*F('.0001')==F('.27') and F('.27')*25==F('6.75'))
    lines=commands[0]['stdout'].splitlines()
    if lines:
        matches('demo base',lambda:ast.literal_eval(lines[0].split(': ',1)[1]),analytics(stats(p0)))
    for idx,bp in enumerate((-200,-100,-50,-25,25,50,100,200),1):
        matches(f'demo shock {bp}',lambda:ast.literal_eval(lines[idx].split('bp: ',1)[1]),model(p0,bp),atol=1e-10)
    big=(1e308,0,3,0,1)
    matches('F54 finite shock despite out-of-range absolute slope',lambda:m.shock(*big[:4],1,big[4]),model(big,1))
    for label,fn in [
        ('F89 position row arity rejected',lambda:m.portfolio([(1000,.06,6)],10)),
        ('F89 invalid explicit frequency rejected',lambda:m.portfolio([(1000,.06,6,.06,False)],10)),
        ('F54 reject unrepresentable bond output',lambda:m.bond(1e-300,0,2,1e200,1)),
        ('negative bumped periodic base rejected',lambda:m.shock(1000,.06,6,-1.99,-200)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[13,14,15,16,17],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
