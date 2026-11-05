"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.03-simple-interest.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-93-') as tmp:
        lab=Path(tmp);(lab/'simple_interest.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['simple_interest.py']),('exact compilation',['-m','compileall','-q','simple_interest.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Interest: 216.00; maturity amount: 2616.00\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_simple');exec(compile(code,str(source),'exec'),m.__dict__)
    def compare(label,actual,expected):
        ck(label,all(abs(a-float(b))<=1e-10 for a,b in zip(actual,expected)),
           actual=actual,exact_reference=[str(x) for x in expected],absolute_tolerance=1e-10)
    compare('worked18month case',m.simple_interest(2400,.06,1.5),(F(216),F(2616)))
    for t in [F(0),F(1,2),F(1),F(3,2)]:
        interest=2400*F(3,50)*t
        compare('every worked half-year accrual '+str(t),m.simple_interest(2400,.06,t),(interest,2400+interest))
    compare('same proportional simple model in monthly units',
            m.simple_interest(2400,.005,18),(F(216),F(2616)))
    for basis in (360,365):
        interest=10000*F(3,50)*F(90,basis)
        compare('fixed day denominator '+str(basis),
                m.simple_interest(10000,.06,m.year_fraction(90,basis)),(interest,10000+interest))
    compare('P1 3500 at4.2% for2.25years',m.simple_interest(3500,.042,2.25),(F(33075,100),F(383075,100)))
    compare('P2 8000 at3% for halfyear',m.simple_interest(8000,.03,.5),(F(120),F(8120)))
    compare('P3 fixed360 daybasis',m.simple_interest(12000,.045,m.year_fraction(60,360)),(F(90),F(12090)))
    unchanged=m.simple_interest(1000,.05,2)[0]-m.simple_interest(1000,.05,1)[0]
    rolled=m.simple_interest(m.simple_interest(1000,.05,1)[1],.05,1)
    ck('P4 second-year accrual50 versus rollover52.50',unchanged==50 and rolled[0]==52.5)
    ck('P5 term9% is6% annual simple',
       F(216,2400)==F(9,100) and F(216,2400)/F(3,2)==F(3,50),
       scope='Independent unit derivation, not rate inference by validator')
    ck('zero factors preserve principal without interest',
       m.simple_interest(1000,0,2)==(0,1000) and m.simple_interest(1000,.05,0)==(0,1000))
    a=m.simple_interest(2400,.06,.5)[0]+m.simple_interest(2400,.06,1)[0]
    ck('unchanged-base durations are additive',a==m.simple_interest(2400,.06,1.5)[0]==216)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
