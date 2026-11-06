"""Section 12.7 exact yield/price lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.07-yield-and-price-relationships.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1207-') as tmp:
        Path(tmp,'yield_price_relationships.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['yield_price_relationships.py']),('exact compilation',['-m','compileall','-q','yield_price_relationships.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['yield_price_relationships.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_sensitivity');exec(compile(code,str(source),'exec'),m.__dict__)
    def oracle(y,face=1000,coupon=30,n=6,f=2):
        val=F(face)
        for _ in range(n):val=(val+coupon)/(1+y/f)
        return val
    def diffs(y,h,face=1000,coupon=30,n=6,f=2):
        up,base,down=[oracle(v,face,coupon,n,f) for v in (y+h,y,y-h)]
        return (up-down)/(2*h),(up-2*base+down)/(h*h)
    def short(v):
        return F(str(float(v)))
    args=(1000,.06,6)
    prices=[];demo=[]
    for k in range(3,10):
        y=F(k,100);p=oracle(y);d1,d2=diffs(y,F('1e-8'));v=m.metrics(*args,float(y))
        close(f'project price {k}%',v['price'],p,atol=0)
        prices.append(v['price'])
        if 4<=k<=8:demo.append(f'Yield={k:.1f}%; price={float(p):.2f}; duration={float(-d1/p):.4f}; convexity={float(d2/p):.4f}')
    ck('P1 P5–P7 monotonicity and par crossing',all(a>b for a,b in zip(prices,prices[1:])) and prices[1]>1000 and math.isclose(prices[3],1000,rel_tol=1e-12) and prices[5]<1000)
    ck('P3 P4 source flows',m.cashflows(*args)==[30]*5+[1030])
    ck('exact demo',commands[0]['stdout'].splitlines()==demo,expected=demo)
    y=F('.06');p=oracle(y);slope,curvature=diffs(y,F('1e-8'))
    met=m.metrics(*args,float(y))
    for k,w in [('first_derivative',slope),('second_derivative',curvature),('modified_duration',-slope/p),('convexity',curvature/p)]:
        close('P8–P11 independent '+k,met[k],short(w),atol=0)
    ck('P12 P13 duration and basis point arithmetic',-F('2.7')*F(100,10000)==-F('.027') and F(50,10000)==F('.005'))
    for bp in (25,50,100,-25,-50,-100):
        dy=F(bp,10000); exact=oracle(y+dy)-p
        got=m.metrics(*args,float(y+dy))['price']-met['price']
        close(f'project repricing {bp} bp',got,exact,atol=1e-10)
        linear=-met['price']*met['modified_duration']*float(dy)
        quadratic=linear+.5*met['price']*met['convexity']*float(dy)**2
        ck(f'project approximation {bp} bp',abs(quadratic-float(exact))<abs(linear-float(exact)),exact=float(exact),duration=linear,duration_convexity=quadratic)
    fd=m.finite_difference(*args,.06)
    d1,d2=diffs(y,F('.0001'))
    ck('P15 source default finite differences',math.isclose(fd['slope'],float(d1),abs_tol=1e-7) and math.isclose(fd['curvature'],float(d2),abs_tol=1e-3))
    tiny=m.finite_difference(*args,.06,1e-30)
    close('F84 tiny step slope',tiny['slope'],short(slope),atol=0)
    close('F84 tiny step curvature',tiny['curvature'],short(curvature),atol=0)
    close('P17 zero-coupon modified duration at five years',m.metrics(1000,0,10,.06)['modified_duration'],F(5)/F('1.03'),atol=0)
    try:r=m.metrics(1e308,0,1,1e155,1)
    except Exception as e:ck('F54 finite extreme derivative outputs',False,exception=repr(e))
    else:
        base=1+F('1e155');face=F('1e308')
        ck('F54 finite extreme derivative outputs',all(math.isclose(r[k],float(v),rel_tol=1e-12) for k,v in dict(price=face/base,first_derivative=-face/base**2,second_derivative=2*face/base**3,modified_duration=1/base,convexity=2/base**2).items()))
    for label,fn in [
        ('F84 boolean step rejected',lambda:m.finite_difference(*args,.06,True)),
        ('F84 step crossing lower yield bound rejected',lambda:m.finite_difference(*args,-1.99,.02)),
        ('F54 overflowing derivative rejected',lambda:m.metrics(1e308,0,1,0,1)),
        ('F54 underflowing positive result rejected',lambda:m.metrics(1e-300,0,2,1e200,1)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[2,10,16,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
