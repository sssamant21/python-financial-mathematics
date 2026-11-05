"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.04-compound-interest.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-94-') as tmp:
        lab=Path(tmp);(lab/'compound_interest.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['compound_interest.py']),('exact compilation',['-m','compileall','-q','compound_interest.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Period | Opening | Interest | Closing (illustrative USD)\n1 | 2000.000 | 80.000 | 2080.000\n2 | 2080.000 | 83.200 | 2163.200\n3 | 2163.200 | 86.528 | 2249.728\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_compound');exec(compile(code,str(source),'exec'),m.__dict__)
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    rows=m.schedule(2000,.04,3)
    for i,row in enumerate(rows,1):
        opening=2000*F(26,25)**(i-1);interest=opening*F(1,25);closing=opening+interest
        ck('worked period'+str(i)+' every field',(row[0]==i and all(abs(v-float(x))<=1e-10 for v,x in zip(row[1:],(opening,interest,closing)))),
           actual=row,exact_reference=list(map(str,(opening,interest,closing))))
    close('closed formula independent rational result',m.compound_amount(2000,.04,3),2000*F(26,25)**3)
    close('sum of retained credits',math.fsum(row[2] for row in rows),2000*(F(26,25)**3-1))
    ck('every row opens at previous closing',all(a[3]==b[1] for a,b in zip(rows,rows[1:])))
    close('P1 first closing',m.schedule(1500,.03,2)[0][3],1500*F(103,100))
    close('P1 second closing',m.compound_amount(1500,.03,2),1500*F(103,100)**2)
    close('P1 total interest',math.fsum(r[2] for r in m.schedule(1500,.03,2)),F(9135,100))
    close('P2 difference from unchanged-principal simple amount',
          m.compound_amount(1500,.03,2)-1590,F(135,100))
    close('P3 closing',m.compound_amount(800,.02,3),800*F(51,50)**3)
    close('P3 total credits',math.fsum(r[2] for r in m.schedule(800,.02,3)),800*(F(51,50)**3-1))
    close('P4 second credit uses2080 base',rows[1][2],F(2080)*F(1,25))
    close('same-rate staged composition',m.compound_amount(m.compound_amount(2000,.04,2),.04,3),2000*F(26,25)**5)
    close('negative-rate exact closing',m.compound_amount(1000,-.02,2),1000*F(49,50)**2)
    ck('zero-time and zero-principal boundaries',
       m.schedule(2000,.04,0)==[] and m.compound_amount(2000,.04,0)==2000 and m.compound_amount(0,.04,10)==0)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
