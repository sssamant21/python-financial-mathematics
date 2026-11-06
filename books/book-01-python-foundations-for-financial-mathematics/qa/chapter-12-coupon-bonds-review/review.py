"""Section 12.3 exact coupon bond lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.03-coupon-bonds.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1203-') as tmp:
        Path(tmp,'coupon_bonds.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['coupon_bonds.py']),('exact compilation',['-m','compileall','-q','coupon_bonds.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['coupon_bonds.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_coupon');exec(compile(code,str(source),'exec'),m.__dict__)
    def pv(Face,C,n,i):
        value=F(Face)
        for _ in range(n): value=(value+C)/(1+i)
        return value
    def numeric(label,fn,want):
        try: value=fn()
        except Exception as e: ck(label,False,exception=repr(e))
        else: close(label,value,want,atol=0)
    a=(1000,.06,3); rows=m.cashflows(*a)
    ck('P2–P7 full contractual flows',rows==[(k,30 if k<6 else 1030) for k in range(1,7)] and sum(x[1] for x in rows)==1180)
    numeric('P6 lifetime coupon income',lambda:m.coupon_income(*a),180)
    ck('P12 P13 annual coupon and current yield',F(1000)*F('.06')==60 and round(100*float(F(60,1050)),4)==5.7143)
    ck('P17 quarterly coupon',m.cashflows(2000,.08,5,4)[0][1]==40)
    want_lines=[];prices=[]
    for y in range(3,9):
        i=F(y,200);want=pv(1000,30,6,i)
        direct=m.price(*a,y/100);annuity=m.annuity_price(*a,y/100)
        close(f'direct {y}%',direct,want,atol=0)
        close(f'annuity {y}%',annuity,want,atol=0)
        ck(f'method agreement {y}%',math.isclose(direct,annuity,rel_tol=1e-12))
        label='premium' if y<6 else 'discount' if y>6 else 'par'
        ck(f'classification {y}%',m.label(*a,y/100)==label)
        if y%2==0: want_lines.append(f'Yield {y:.1f}%: price={float(want):.2f}; {label}')
        prices.append(direct)
    ck('project prices strictly decline',all(x>y>0 for x,y in zip(prices,prices[1:])))
    ck('exact demo output',commands[0]['stdout'].splitlines()==want_lines,expected=want_lines)
    numeric('P15 zero yield',lambda:m.annuity_price(*a,0),1180)
    numeric('P16 zero coupon',lambda:m.price(1000,0,3,.06),pv(1000,0,6,F('.03')))
    numeric('F80 coupon income lost beside large principal',lambda:m.coupon_income(1e100,1e-100,1,1),1)
    numeric('F54 finite par despite overflowing coupon product',lambda:m.annuity_price(1e308,2,1,2,4),F('1e308'))
    numeric('F54 finite PV despite tiny discount factor',lambda:m.price(1e308,0,2,1e200,1),pv(F('1e308'),0,2,F('1e200')))
    ck('F78 tiny non-par bond retains classification',m.label(1e-10,.06,3,.08)=='discount')
    for label,fn in [
        ('F78 rejects maturity rounded to zero',lambda:m.terms(1000,.06,1e-12,2,.06)),
        ('F78 rejects fractional count rounded to one',lambda:m.price(1000,.06,.3333333333333333,.06,3)),
        ('F54 rejects overflowing final flow',lambda:m.cashflows(1e308,2,1,1)),
        ('F54 rejects underflowed positive price',lambda:m.annuity_price(1e-300,0,2,1e200,1)),
        ('F54 rejects overflowing nominal coupon income',lambda:m.coupon_income(1e308,1,2,2)),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
