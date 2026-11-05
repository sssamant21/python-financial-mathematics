"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.07-discount-factors.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-97-') as tmp:
        lab=Path(tmp);(lab/'discount_factors.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['discount_factors.py']),('exact compilation',['-m','compileall','-q','discount_factors.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Periods | Factor at 4% | PV of 5000 (illustrative USD)\n0 | 1.000000000 | 5000.00\n1 | 0.961538462 | 4807.69\n2 | 0.924556213 | 4622.78\n3 | 0.888996359 | 4444.98\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_factors');exec(compile(code,str(source),'exec'),m.__dict__)
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    df=m.discount_factor;between=m.discount_between;payment=m.discounted_payment
    for n in range(4):
        exact=F(25,26)**n
        close('workedfactor row'+str(n),df(.04,n),exact)
        close('workedpayment row'+str(n),payment(5000,.04,n),5000*exact)
    close('ratio commonorigin yields elapsed3',df(.04,5)/df(.04,2),F(25,26)**3)
    close('between2and5 useselapsed3',between(.04,valuation=2,payment=5),F(25,26)**3)
    close('composition0to2to5',df(.04,2)*between(.04,valuation=2,payment=5),F(25,26)**5)
    close('P1 factor10% twoyears',df(.1,2),F(100,121))
    close('P1 payment1210',payment(1210,.1,2),F(1000))
    close('P2 year4payment valuedat1',between(.05,valuation=1,payment=4),F(20,21)**3)
    close('P3 immediatepaymentfactor',between(.04,valuation=3,payment=3),F(1))
    ck('P4 grid not probabilitynormalized',abs(sum(df(.04,n) for n in range(4))-1)>1)
    close('negative rate aboveone',df(-.02,1),F(50,49))
    close('signed factor scaling',payment(-5000,.04,3),-5000*F(25,26)**3)
    # P5 supplies a factor directly; it is supplemental signed multiplication.
    close('P5 signedobligation times suppliedfactor',-2000*.95,-2000*F(19,20))
    try:payment(F(1,1<<2000),.04,1)
    except ValueError as error:ck('F46 lostnonzeroamount rejected',True,exception=str(error))
    except Exception as error:ck('F46 lostnonzeroamount rejected',False,exception=repr(error))
    else:ck('F46 lostnonzeroamount rejected',False,actual='returnedzero for nonzero rational input')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
