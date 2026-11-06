"""Section 12.9 exact duration lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.09-duration.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1209-') as tmp:
        Path(tmp,'bond_duration.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['bond_duration.py']),('exact compilation',['-m','compileall','-q','bond_duration.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['bond_duration.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_duration');exec(compile(code,str(source),'exec'),m.__dict__)
    def p(y,c,n=6,f=2):
        v=F(1000)
        for _ in range(n):v=(v+c)/(1+y/f)
        return v
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    y=F('.06'); h=F('1e-9'); macaulay=[]
    for rate in (0,2,4,6,8):
        c=F(1000)*F(rate,100)/2
        value=p(y,c)
        slope=(p(y+h,c)-p(y-h,c))/(2*h)
        mod=-slope/value; mac=mod*(1+y/2)
        terms=[(c+(1000 if k==6 else 0))/(1+y/2)**k for k in range(1,7)]
        vals=m.analytics(1000,rate/100,6,.06)
        for key,want in [('price',value),('macaulay_duration',mac),('modified_duration',mod)]:
            close(f'project {rate}% {key}',vals[key],float(want),atol=0)
        ck(f'project {rate}% weights reconcile',len(vals['weights'])==6 and math.isclose(math.fsum(vals['weights']),1,rel_tol=1e-12) and all(math.isclose(a,float(b/value),rel_tol=1e-12,abs_tol=0) for a,b in zip(vals['weights'],terms)))
        delta=F('.005');approx=m.approximate_change(1000,rate/100,6,.06,float(delta))
        close(f'project {rate}% +50bp first-order change',approx,float(slope*delta),atol=0)
        exact=p(y+delta,c)-value
        close(f'project {rate}% +50bp exact reprice',m.analytics(1000,rate/100,6,.065)['price']-vals['price'],exact,atol=1e-10)
        ck(f'project {rate}% signed approximation error',float(exact)>approx,approximate=approx,exact=float(exact))
        macaulay.append(vals['macaulay_duration'])
    ck('P8 P10 P11 durations decrease with coupon',macaulay[0]==3 and all(a>b for a,b in zip(macaulay,macaulay[1:])))
    ck('P5 P6 full timeline',m.cashflows(1000,.06,6)==[(k/2,30 if k<6 else 1030) for k in range(1,7)])
    close('P9 five-year zero Macaulay duration',m.analytics(1000,0,10,.06)['macaulay_duration'],5,atol=0)
    ck('P13–P17 shock and DV01 units',F(25,10000)==F('.0025') and -1000*F('2.7')*F('.0025')==F('-6.75') and 1000-F('6.75')==F('993.25') and 1000*F('2.7')*F('.0001')==F('.27'))
    ck('exact demo output',commands[0]['stdout'].splitlines()==['Price 1000.0 Macaulay 2.789854 Modified 2.708596'])
    num('F54 finite duration despite overflowing weighted sum',lambda:m.analytics(1e308,0,3,0,1)['macaulay_duration'],3)
    num('F54 finite duration despite discount underflow',lambda:m.analytics(1e308,0,2,1e200,1)['macaulay_duration'],2)
    num('F54 finite scaled shock despite overflowing intermediate',lambda:m.approximate_change(1e308,0,3,0,.001,1),F('-3e305'))
    for label,fn in [
        ('F86 boolean shock rejected',lambda:m.approximate_change(1000,.06,6,.06,True)),
        ('F54 unrepresentable shock rejected',lambda:m.approximate_change(1e308,0,3,0,1,1)),
        ('F54 nonfinite maturity cash flow rejected',lambda:m.cashflows(1e308,2,1,1)),
        ('F54 underflowing price rejected',lambda:m.analytics(1e-300,0,2,1e200,1)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,2,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
