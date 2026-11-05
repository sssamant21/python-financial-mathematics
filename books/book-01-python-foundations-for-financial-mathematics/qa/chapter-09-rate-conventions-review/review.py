"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.10-effective-vs-nominal-rates.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-910-') as tmp:
        lab=Path(tmp);(lab/'rate_conventions.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['rate_conventions.py']),('exact compilation',['-m','compileall','-q','rate_conventions.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='6% nominal, monthly -> effective annual 6.16778119%\n6% effective annual -> nominal, monthly 5.84106068%\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_rates');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    forward=m.nominal_to_effective;reverse=m.effective_to_nominal
    def close(label,value,expect,atol=1e-14):
        ck(label,abs(value-float(expect))<=atol,actual=value,high_precision_reference=str(expect),absolute_tolerance=atol)
    with localcontext() as ctx:
        ctx.prec=90;one=D(1)
        def nominal(j,f):return (one+j/D(f))**f-one
        def effective(e,f):return D(f)*((one+e)**(one/D(f))-one)
        e6=nominal(D('.06'),12);j6=effective(D('.06'),12)
        close('worked monthly nominal6% forward',forward(.06,12),e6)
        close('worked effective6% reverse',reverse(.06,12),j6)
        close('P1 quarterly8%nominal',forward(.08,4),nominal(D('.08'),4))
        close('P2 quarterly8%effective',reverse(.08,4),effective(D('.08'),4))
        close('P4 correct monthly effective',reverse(.06,12)/12,j6/12)
        close('negative-rate nominal conversion',forward(-.02,12),nominal(D('-.02'),12))
        tiny=D('1e-16')
        close('tiny finitefloat forward preserved independently',forward(1e-16,12),nominal(tiny,12),atol=1e-30)
        close('tiny finitefloat reverse preserved independently',reverse(1e-16,12),effective(tiny,12),atol=1e-30)
        three_year=D(10000)*(one+D('.06')/12)**36
    close('three-year balances agree to rational reference',
          10000*(1+forward(.06,12))**3,F(10000)*F(201,200)**36,atol=1e-9)
    ck('common basis offer ranking',forward(.06,12)>.0615 and 10000*(1+forward(.06,12))>10615)
    ck('P3 annual identity',abs(forward(.08,1)-.08)<1e-15 and abs(reverse(.08,1)-.08)<1e-15)
    ck('zero conversions are genuine zeros',forward(0,12)==0 and reverse(0,12)==0)
    ck('P4 annualeffective divide12 is different scenario',
       abs(reverse(.06,12)/12-.005)>1e-6)
    for label,fn in [('nominal',forward),('effective',reverse)]:
        try:fn(F(1,1<<2000),12)
        except ValueError as error:ck('F46 '+label+' input conversion loss rejected',True,exception=str(error))
        except Exception as error:ck('F46 '+label+' input conversion loss rejected',False,exception=repr(error))
        else:ck('F46 '+label+' input conversion loss rejected',False,actual='returnedzero for nonzero rational rate')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
