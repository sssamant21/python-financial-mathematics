"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.12-continuous-compounding.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-912-') as tmp:
        lab=Path(tmp);(lab/'continuous_compounding.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['continuous_compounding.py']),('exact compilation',['-m','compileall','-q','continuous_compounding.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Continuous FV: 10,618.37\nContinuous EAR: 6.18365465%\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_continuous');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,high_precision_reference=str(expect),absolute_tolerance=atol)
    with localcontext() as ctx:
        ctx.prec=90
        exp06=D('.06').exp()
        close('worked one-year balance',m.future_value(10000,.06,1),10000*exp06)
        close('worked effective annual',m.effective_annual(.06),exp06-1,atol=1e-14)
        close('worked PV15000 in3years',m.present_value(15000,.04,3),D(15000)*D('-.12').exp())
        close('P1 FV5000 at3% fortwoyears',m.future_value(5000,.03,2),D(5000)*exp06)
        close('P2 continuous5% to effective',m.effective_annual(.05),D('.05').exp()-1,atol=1e-14)
        close('P3 effective5% to continuous',m.continuous_from_effective(.05),D('1.05').ln(),atol=1e-14)
        close('P4 PV2000 at4% for1.5years',m.present_value(2000,.04,1.5),D(2000)*D('-.06').exp())
        for frequency in (1,2,4,12,365):
            exact=D(frequency)*(1+D('.06')/frequency).ln()
            close('nominal6% equivalent continuous freq'+str(frequency),
                  m.continuous_from_nominal(.06,frequency),exact,atol=1e-14)
        close('negative continuous2% twoyears',m.future_value(10000,-.02,2),D(10000)*D('-.04').exp())
    ck('P5 continuous6% not effective6%',m.effective_annual(.06)>.06)
    close('P6 intervalcomposition',m.accumulation(.035,1.5)*m.accumulation(.035,2.5),m.accumulation(.035,4),atol=1e-14)
    close('unrounded PV inverse',m.future_value(m.present_value(15000,.04,3),.04,3),F(15000),atol=1e-9)
    close('signed zero-time identity',m.future_value(-200,.04,0),F(-200))
    tiny=F(1,1<<2000)
    probes=[
      ('futureamount',lambda:m.future_value(tiny,.06,1)),
      ('presentamount',lambda:m.present_value(tiny,.06,1)),
      ('continuousrate',lambda:m.effective_annual(tiny)),
      ('effectiverate',lambda:m.continuous_from_effective(tiny)),
      ('nominalrate',lambda:m.continuous_from_nominal(tiny,12))]
    for label,fn in probes:
        try:fn()
        except ValueError as error:ck('F46 '+label+' input loss rejected',True,exception=str(error))
        except Exception as error:ck('F46 '+label+' input loss rejected',False,exception=repr(error))
        else:ck('F46 '+label+' input loss rejected',False,actual='nonzero scalar treated aszero')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=6,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
