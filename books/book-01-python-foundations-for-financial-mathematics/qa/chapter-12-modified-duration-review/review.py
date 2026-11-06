"""Section 12.10 exact modified duration lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.10-modified-duration.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1210-') as tmp:
        Path(tmp,'modified_duration.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['modified_duration.py']),('exact compilation',['-m','compileall','-q','modified_duration.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['modified_duration.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_modified');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def pv(y,face=1000):
        v=F(face)
        for _ in range(6):v=(v+F(face)*F('.03'))/(1+y/2)
        return v
    y=F('.06');p=pv(y);h=F('1e-8')
    slope=(pv(y+h)-pv(y-h))/(2*h)
    mod=-slope/p; mac=mod*(1+y/2)
    got=m.bond(1000,.06,6,.06)
    for key,w in dict(price=p,macaulay=mac,modified=mod,derivative=slope,dv01=-slope/10000).items():
        close('base '+key,got[key],float(w),atol=0)
    ck('P3 reported Macaulay-to-modified relation',math.isclose(got['modified'],got['macaulay']/1.03,rel_tol=1e-12))
    ck('P4–P6 periodic inputs',F('.06')/2==F('.03') and 1000*F('.03')==30 and 3*2==6)
    demo=[f"Price {round(float(p),4)} Modified duration {round(float(mod),6)} DV01 {round(float(-slope/10000),6)}"]
    errors={}
    for bp in (-100,-50,-25,25,50,100):
        change=F(bp,10000)
        expected=pv(y+change)-p
        actual,approx=m.shock(1000,.06,6,.06,float(change))
        close(f'{bp:+} bp exact price change',actual,expected,atol=1e-10)
        close(f'{bp:+} bp first-order estimate',approx,float(slope*change),atol=0)
        ck(f'{bp:+} bp convexity correction is positive',actual>approx,exact=actual,approximate=approx,error=actual-approx)
        errors[bp]=actual-approx
        if bp!=-25:demo.append(f'{bp:+} bp: exact={float(expected):.4f}; first-order={float(slope*change):.4f}')
    ck('signed shocks have unequal approximation errors',all(errors[-bp]>errors[bp] for bp in (25,50,100)))
    close('notional scaling at 250,000',m.bond(250000,.06,6,.06)['dv01'],float(-slope/10000*250),atol=0)
    ck('P9–P15 worked approximation arithmetic',F(50,10000)==F('.005') and F('-2.7')*F('.005')==F('-.0135') and -2700*F('.005')==F('-13.5') and F('-2.7')*F('-.005')==F('.0135') and 2700*F('.0001')==F('.27'))
    ck('exact demo output',commands[0]['stdout'].splitlines()==demo,expected=demo)
    exact,approx=m.shock(1000,.06,6,.06,1e-25)
    close('F87 tiny exact change remains nonzero',exact,float(pv(y+F('1e-25'))-p),atol=0)
    def numeric(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    numeric('F54 finite slope despite underflowed discount',lambda:m.bond(1e308,0,2,1e200,1)['derivative'],-2*F('1e308')/(1+F('1e200'))**3)
    numeric('F54 finite repricing difference despite overflowing slope',lambda:m.shock(1e308,0,3,0,.001,1)[1],F('-3e305'))
    for label,fn in [
        ('F87 validate zero frequency before dividing',lambda:m.bond(1000,.06,6,.06,0)),
        ('F87 shock crossing lower bound',lambda:m.shock(1000,.06,6,-1.99,-.02)),
        ('F54 unrepresentable bond derivative rejected',lambda:m.bond(1e308,0,3,0,1)),
        ('F54 underflowed bond price rejected',lambda:m.bond(1e-300,0,2,1e200,1)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
