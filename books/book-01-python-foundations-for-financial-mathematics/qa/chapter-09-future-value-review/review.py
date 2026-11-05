"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.06-future-value.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-96-') as tmp:
        lab=Path(tmp);(lab/'future_value.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['future_value.py']),('exact compilation',['-m','compileall','-q','future_value.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='7500 today at 4.5% effective annually: year-4 FV = 8943.89\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_fv');exec(compile(code,str(source),'exec'),m.__dict__)
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    fv=m.future_value;at=m.value_at
    factor=F(209,200)**4
    close('worked7500 toyear4',fv(7500,.045,4),7500*factor)
    close('workedtotalgrowth',fv(7500,.045,4)-7500,7500*(factor-1))
    close('start2 target5 uses3periods',at(2000,.05,start=2,target=5),2000*F(21,20)**3)
    ck('start2 target5 is not five periods',abs(at(2000,.05,start=2,target=5)-fv(2000,.05,5))>1)
    close('common target later8000',at(8000,.045,start=2,target=4),8000*F(209,200)**2)
    close('common target difference',at(7500,.045,start=0,target=4)-at(8000,.045,start=2,target=4),
          7500*factor-8000*F(209,200)**2)
    close('P1 3000 today toyear2',fv(3000,.06,2),3000*F(53,50)**2)
    close('P1 growth',fv(3000,.06,2)-3000,F(37080,100))
    close('P2 3000 atyear2 toyear4',at(3000,.06,start=2,target=4),3000*F(53,50)**2)
    close('P3 common future for1000 now',at(1000,.05,start=0,target=2),F(110250,100))
    close('P3 common future for1050 at1',at(1050,.05,start=1,target=2),F(110250,100))
    close('P4 signed obligation',fv(-1000,.05,1),F(-1050))
    close('negative rate shrinks positive balance',fv(1000,-.02,2),1000*F(49,50)**2)
    ck('same-date is identity after validinput',at(-123,.045,start=3,target=3)==-123)
    try:fv(F(1,1<<2000),.05,1)
    except ValueError as error:ck('F46 input underflow rejection',True,exception=str(error))
    except Exception as error:ck('F46 input underflow rejection',False,exception=repr(error))
    else:ck('F46 input underflow rejection',False,actual='returnedzero for nonzero rational amount')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
