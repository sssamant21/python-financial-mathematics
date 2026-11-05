"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.01-the-time-value-of-money.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-91-') as tmp:
        lab=Path(tmp);(lab/'tvm_introduction.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['tvm_introduction.py']),('exact compilation',['-m','compileall','-q','tvm_introduction.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='1000 today -> 1102.50 in two years\n1080 in two years -> 979.59 today\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_tvm');exec(compile(code,str(source),'exec'),m.__dict__)
    future=lambda a,r,n:m.equivalent(a,r,n,to_future=True)
    present=lambda a,r,n:m.equivalent(a,r,n,to_future=False)
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    close('worked A future at common date',future(1000,.05,2),1000*F(21,20)**2)
    close('worked B present at common date',present(1080,.05,2),1080/F(21,20)**2)
    ck('positive common factor preserves offer ranking',1000>present(1080,.05,2) and future(1000,.05,2)>1080)
    close('P1 future from rational effective factor',future(2000,.04,3),2000*F(26,25)**3)
    close('P1 round trip uses full computed amount',present(future(2000,.04,3),.04,3),F(2000))
    close('P2 common-date equality',future(500,.05,1),F(525))
    close('P3 negative-rate forward',future(1000,-.02,1),F(980))
    close('P3 negative-rate present',present(1000,-.02,1),1000/F(49,50))
    close('P4 input5 means gross factor6',future(1000,5,1),F(6000))
    close('P4 input .05 means gross factor1.05',future(1000,.05,1),F(1050))
    close('signed viewpoint preserved',future(-1000,.05,2),-1000*F(21,20)**2)
    close('zero-time factor',m.accumulation(.05,0),F(1))
    close('zero-rate factor',m.accumulation(0,20),F(1))
    close('same-rate composition with independent rational oracle',m.accumulation(.03,2)*m.accumulation(.03,5),F(103,100)**7)
    close('separate inflation purchasing-power units',future(1000,.05,1)/1.02,F(1050)/F(51,50))
    close('financial discounted value uses opportunity rate instead',present(1050,.05,1),F(1000))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
