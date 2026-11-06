"""Section 12.2 exact cash-flow lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-12/12.02-bond-cash-flows.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1202-') as tmp:
        Path(tmp,'bond_cash_flows.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['bond_cash_flows.py']),('exact compilation',['-m','compileall','-q','bond_cash_flows.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['bond_cash_flows.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_cash_flows');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    demo=[]
    for name,L,c,y,mult,n in [('A',1000,F('.06'),3,2,6),('B',1000,F(0),3,2,6),('C',2000,F('.08'),5,4,20)]:
        rows=m.schedule(L,float(c),y,mult)
        C=L*c/mult
        expected=[dict(period=k,time_years=float(F(k,mult)),coupon=float(C),principal=L if k==n else 0,cash_flow=float(C+(L if k==n else 0))) for k in range(1,n+1)]
        ck(name+' exact period rows and maturity redemption',rows==expected)
        ck(name+' totals',m.totals(rows)==dict(coupon=float(n*C),principal=L,cash_flow=float(n*C+L)))
        ck(name+' explicit row composition',all(r['coupon']+r['principal']==r['cash_flow'] for r in rows))
        prices=[]
        for rate in (F('.04'),F('.06'),F('.08')):
            want=sum(((C+(L if k==n else 0))/(1+rate/mult)**k for k in range(1,n+1)),F(0))
            got=m.price(rows,float(rate),mult)
            close(name+' nominal yield '+str(rate),got,want,atol=0)
            prices.append(got)
        ck(name+' declining prices',prices[0]>prices[1]>prices[2]>0)
        if name=='A':
            demo=expected
    rows=m.schedule(1000,.06,3,2)
    ck('worked par',m.price(rows,.06,2)==1000 or math.isclose(m.price(rows,.06,2),1000,rel_tol=1e-12))
    close('zero-yield identity',m.price(rows,0,2),1180,atol=0)
    close('E12 zero-coupon price',m.price(m.schedule(1000,0,3,2),.06,2),F(1000)/F('1.03')**6,atol=0)
    lines=commands[0]['stdout'].splitlines()
    ck('exact demo rows',len(lines)==8 and [ast.literal_eval(x) for x in lines[:6]]==demo)
    ck('exact demo totals and price',len(lines)==8 and ast.literal_eval(lines[6].split(': ',1)[1])==dict(coupon=180,principal=1000,cash_flow=1180) and float(lines[7].split(': ',1)[1])==1000)
    def change(row,key,value):
        copy=[x.copy() for x in rows]; copy[row][key]=value
        return copy
    try: large=m.schedule(1e308,2,1,4)
    except Exception as e:ck('F54 finite coupon after scaling',False,exception=repr(e))
    else:ck('F54 finite coupon after scaling',large[0]['coupon']==5e307 and large[-1]['cash_flow']==1.5e308)
    try: pv=m.price(m.schedule(1e308,0,2,1),1e200,1)
    except Exception as e:ck('F54 representable PV despite tiny discount factor',False,exception=repr(e))
    else:close('F54 representable PV despite tiny discount factor',pv,F('1e308')/(1+F('1e200'))**2,atol=0)
    for label,fn in [
        ('F78 near-zero count cannot round to zero',lambda:m.schedule(1000,.06,1e-12,2)),
        ('F78 decimal fractional count cannot round to one',lambda:m.schedule(1000,.06,.3333333333333333,3)),
        ('F79 reject schedule and discount frequency mismatch',lambda:m.price(rows,.06,4)),
        ('F79 reject duplicate period',lambda:m.price(change(1,'period',1),.06,2)),
        ('F79 reject wrong row composition',lambda:m.price(change(0,'cash_flow',31),.06,2)),
        ('F79 reject nonfinite row in totals',lambda:m.totals(change(0,'cash_flow',float('nan')))),
        ('F79 reject missing bullet redemption',lambda:m.price(rows[:-1],.06,2)),
        ('F54 reject nonfinite maturity flow',lambda:m.schedule(1e308,2,1,1)),
        ('F54 reject unrepresentable positive price',lambda:m.price(m.schedule(1e-300,0,2,1),1e200,1)),
        ('F54 reject overflowing nominal total',lambda:m.totals(m.schedule(1e308,1,2,2))),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,applied_project_records=1,conceptual_prompts=[15,16,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
