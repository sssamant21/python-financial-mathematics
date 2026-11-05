"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.11-compounding-frequency.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    from decimal import Decimal as D,localcontext
    names=[('Annual',1),('Semiannual',2),('Quarterly',4),('Monthly',12),('Daily (365)',365)]
    with localcontext() as ctx:
        ctx.prec=90;one=D(1)
        references={f:(one+D('.06')/f)**f-one for _,f in names}
        expected_stdout=''.join(f'{name:13} EAR={references[f]:.8%} balance={D(10000)*(one+references[f]):,.2f}\n' for name,f in names)
    with tempfile.TemporaryDirectory(prefix='book1-911-') as tmp:
        lab=Path(tmp);(lab/'compounding_frequency.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['compounding_frequency.py']),('exact compilation',['-m','compileall','-q','compounding_frequency.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout==expected_stdout
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_frequency');exec(compile(code,str(source),'exec'),m.__dict__)
    ear=m.effective_annual;fv=m.future_value;nom=m.nominal_for_effective
    def close(label,value,expect,atol=1e-14):
        ck(label,abs(value-float(expect))<=atol,actual=value,high_precision_reference=str(expect),absolute_tolerance=atol)
    for name,f in names:
        close(name+' effective annual Decimal reference',ear(.06,f),references[f])
        close(name+' balance rational reference',fv(10000,.06,f,1),10000*(1+F(3,50*f))**f,atol=1e-9)
    with localcontext() as ctx:
        ctx.prec=90
        for _,f in names:
            ref=D(f)*((D('1.06'))**(D(1)/f)-1)
            close('fixed effective annual6% nominal '+str(f),nom(.06,f),ref)
            close('fixed effective annual balance '+str(f),fv(10000,float(ref),f,1),D(10600),atol=1e-9)
        continuous=D(10000)*(D('.06')*3).exp()
    close('P1 nominal8% periodic quarterly',.08/4,F(1,50))
    close('P2 nominal8% quarterly EAR',ear(.08,4),F(51,50)**4-1)
    ck('P3 monthlynominal6% differs from effective6%',ear(.06,12)>.06)
    ck('P4 doubling monthlyfrequency does not double interest',
       0<fv(10000,.06,24,1)-10000<2*(fv(10000,.06,12,1)-10000))
    close('P5 threeyears monthly36period balance',fv(10000,.06,12,3),10000*F(201,200)**36,atol=1e-8)
    ck('daily finitefrequency below independent continuous limit',fv(10000,.06,365,3)<float(continuous),limit=str(continuous))
    for label,fn in [('forward',ear),('reverse',nom)]:
        try:fn(F(1,1<<2000),12)
        except ValueError as error:ck('F46 '+label+' input conversion loss rejected',True,exception=str(error))
        except Exception as error:ck('F46 '+label+' input conversion loss rejected',False,exception=repr(error))
        else:ck('F46 '+label+' input conversion loss rejected',False,actual='nonzero rational rate becamezero')
    try:nom(5e-324,12)
    except ValueError as error:ck('F47 reverse intermediate underflow rejected',True,exception=str(error),input=repr(5e-324))
    except Exception as error:ck('F47 reverse intermediate underflow rejected',False,exception=repr(error))
    else:ck('F47 reverse intermediate underflow rejected',False,actual='zero nominal rate returned for nonzero float effective rate')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=6,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
