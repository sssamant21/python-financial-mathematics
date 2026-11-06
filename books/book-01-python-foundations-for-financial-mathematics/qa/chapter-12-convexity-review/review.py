"""Section 12.11 exact convexity lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.11-convexity.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1211-') as tmp:
        Path(tmp,'bond_convexity.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['bond_convexity.py']),('exact compilation',['-m','compileall','-q','bond_convexity.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['bond_convexity.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_convexity');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def pv(y):
        value=F(1000)
        for _ in range(6):value=(value+30)/(1+y/2)
        return value
    y=F('.06');p=pv(y);h=F('1e-8')
    u,d=pv(y+h),pv(y-h)
    slope=(u-d)/(2*h); curvature=(u-2*p+d)/h**2
    a=m.analytics(1000,.06,6,.06)
    for key,want in dict(price=p,slope=slope,curvature=curvature,modified_duration=-slope/p,convexity=curvature/p).items():
        close('independent base '+key,a[key],float(want),atol=0)
    close('P15 closed-form zero convexity',m.analytics(1000,0,6,.06)['convexity'],F(42,4)/F('1.03')**2,atol=0)
    ck('P7–P11 worked approximation arithmetic',F(100,10000)==F('.01') and -F('2.7')*F('.01')==F('-.027') and F('9.5')*F('.01')**2/2==F('.000475') and F('-.027')+F('.000475')==F('-.026525'))
    ck('P12–P14 bond inputs',1000*F('.06')/2==30 and 3*2==6 and p==1000)
    benchmarks={}
    for bp in (-200,-100,-50,-25,25,50,100,200):
        dy=F(bp,10000)
        exact=(pv(y+dy)-p)/p
        linear=slope*dy/p
        quad=linear+curvature*dy**2/(2*p)
        want=dict(exact_pct=float(exact),duration_pct=float(linear),duration_convexity_pct=float(quad))
        got=m.scenario(1000,.06,6,.06,float(dy))
        for key,v in want.items():close(f'{bp:+} bp {key}',got[key],v,atol=0)
        e1=abs(got['exact_pct']-got['duration_pct']);e2=abs(got['exact_pct']-got['duration_convexity_pct'])
        ck(f'{bp:+} bp second-order improves',0<e2<e1,linear_error=e1,quadratic_error=e2)
        benchmarks[bp]=want
    ck('gain exceeds loss at symmetric shocks',all(benchmarks[-bp]['exact_pct']>-benchmarks[bp]['exact_pct'] for bp in (25,50,100,200)))
    lines=commands[0]['stdout'].splitlines()
    want_header=f'Price {float(p)} Duration {round(float(-slope/p),6)} Convexity {round(float(curvature/p),6)}'
    expected_shocks=(-100,-50,25,50,100)
    def check_demo():
        if len(lines)!=6 or lines[0]!=want_header:return False
        for line,bp in zip(lines[1:],expected_shocks):
            num,unit,data=line.split(' ',2)
            vals=ast.literal_eval(data)
            if int(num)!=bp or unit!='bp' or not all(math.isclose(vals[k],v,rel_tol=1e-12) for k,v in benchmarks[bp].items()):return False
        return True
    ck('exact demo matches derived values',check_demo())
    shock=m.scenario(1000,.06,6,.06,1e-25)
    close('F88 tiny exact relative change',shock['exact_pct'],(pv(y+F('1e-25'))-p)/p,atol=0)
    try:v=m.analytics(1e308,0,1,1e155,1)
    except Exception as e:ck('F54 finite extreme curvature',False,exception=repr(e))
    else:close('F54 finite extreme curvature',v['curvature'],2*F('1e308')/(1+F('1e155'))**3,atol=0)
    try:v=m.scenario(1e308,0,3,0,.01,1)
    except Exception as e:ck('F54 finite relative risk despite overflowing absolute curvature',False,exception=repr(e))
    else:
        expected=(F('1.01')**-3-1,F('-.03'),F('-.0294'))
        ck('F54 finite relative risk despite overflowing absolute curvature',
           all(math.isclose(v[k],float(w),rel_tol=1e-12) for k,w in zip(('exact_pct','duration_pct','duration_convexity_pct'),expected)),actual=repr(v))
    for label,fn in [
        ('F54 reject overflowing curvature',lambda:m.analytics(1e308,0,3,0,1)),
        ('F54 reject underflowed price',lambda:m.analytics(1e-300,0,2,1e200,1)),
        ('bump below yield domain rejected',lambda:m.scenario(1000,.06,6,-1.99,-.02)),
        ('boolean shock rejected',lambda:m.scenario(1000,.06,6,.06,True)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
