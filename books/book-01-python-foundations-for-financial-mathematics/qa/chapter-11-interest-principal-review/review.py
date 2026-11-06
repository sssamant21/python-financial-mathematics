"""Section 11.5 exact component lab and independent amortization benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-11/11.05-interest-and-principal-components.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1105-') as tmp:
        Path(tmp,'interest_principal_components.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['interest_principal_components.py']),('exact compilation',['-m','compileall','-q','interest_principal_components.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and len(p.stdout.splitlines())==3 if args==['interest_principal_components.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_components');exec(compile(code,str(source),'exec'),m.__dict__)
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    L=10000;r=F(1,200);n=24
    a=F(L)/sum(((1+r)**-k for k in range(1,n+1)),F(0))
    opening=F(L);expected=[]
    for k in range(1,n+1):
        interest=opening*r;principal=a-interest;opening-=principal
        expected.append(dict(period=k,payment=a,interest=interest,principal=principal,balance=opening))
    rows=m.amortization(L,.005,n)
    ck('all 24 rows vs exact retrospective recurrence',len(rows)==n and all(x['period']==y['period'] and all(math.isclose(x[key],float(y[key]),abs_tol=1e-10,rel_tol=1e-12) for key in ('payment','interest','principal','balance')) for x,y in zip(rows,expected)))
    for k,(line,want) in enumerate(zip(commands[0]['stdout'].splitlines(),expected[:3],strict=True),1):
        cols=line.split();ck('demonstration period '+str(k),int(cols[0])==k)
        for j,key in enumerate(('payment','interest','principal','balance')):
            ck(f'demonstration row {k} {key}',cols[1+2*j]==key and float(cols[2+2*j])==round(float(want[key]),2),expected=round(float(want[key]),2),actual=cols[2+2*j])
    lines=source.read_text().splitlines()
    for k,want in enumerate(expected[:3],1):
        line=next(l for l in lines if l.startswith(f'| {k} |'))
        got=[v.replace(',','') for v in re.findall(r'\$([\d,.]+)',line)]
        cents=[f'{float(want[key]):.2f}' for key in ('interest','principal','balance')]
        ck('F68 printed worked table row '+str(k),got==cents,expected=cents,actual=got)
    ck('P1/P3 each payment equals both components',all(math.isclose(x['payment'],x['interest']+x['principal'],rel_tol=1e-12) for x in rows))
    for label,v,w in [('P2/P5 first interest',rows[0]['interest'],expected[0]['interest']),('P6 first principal',rows[0]['principal'],expected[0]['principal']),('P7 closing balance',rows[0]['balance'],expected[0]['balance']),('P8 next interest',rows[1]['interest'],expected[1]['interest'])]:
        close(label,v,w)
    ck('P4 balance recurrence across rows',all(math.isclose(x['balance'],(L if j==0 else rows[j-1]['balance'])*(1+.005)-x['payment'],abs_tol=1e-10,rel_tol=1e-12) for j,x in enumerate(rows)))
    ck('P9 interest declines and principal grows',all(x['interest']>y['interest'] and x['principal']<y['principal'] for x,y in zip(rows,rows[1:])))
    s=m.summary(L,.005,n)
    close('P10 total principal',s['principal'],F(L))
    close('P11 total interest',s['interest'],a*n-L)
    close('summary final balance',s['final_balance'],F(0))
    zr=m.summary(1200,0,12)
    ck('zero-rate summary',zr==dict(payment=100,interest=0,principal=1200,final_balance=0))
    probe('F54 tiny positive rate payment',lambda:m.payment(.1,5e-324,1),F(1,10),0)
    probe('F66 large interest first principal',lambda:m.amortization(1,1e100,2)[0]['principal'],1/(2+F(1e100)),0)
    probe('F66 one-payment closing balance',lambda:m.amortization(1,1e308,1)[0]['balance'],F(0),0)
    for label,fn in [
        ('F54 zero-rate payment underflow',lambda:m.payment(5e-324,0,2)),
        ('F54 nonfinite payment',lambda:m.payment(1e308,1,1)),
        ('F54 nonzero interest underflow',lambda:m.amortization(5e-324,.5,1)),
        ('F54 summary interest overflow',lambda:m.summary(1e308,1,3)),
        ('bad principal',lambda:m.payment(0,.01,12)),
        ('bad rate',lambda:m.payment(100,-.01,12)),
        ('bad count',lambda:m.payment(100,.01,0))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
