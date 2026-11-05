"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.13-solving-for-rate.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-913-') as tmp:
        lab=Path(tmp);(lab/'solving_for_rate.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['solving_for_rate.py']),('exact compilation',['-m','compileall','-q','solving_for_rate.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Two-year EAR: 10.000000%\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_rate_inference');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def close(label,value,expect,atol=1e-14):
        ck(label,abs(value-float(expect))<=atol,actual=value,high_precision_reference=str(expect),absolute_tolerance=atol)
    close('worked8000to9680 over2periods',m.periodic_rate(8000,9680,2),F(1,10))
    close('P1 400to420 over1period',m.periodic_rate(400,420,1),F(1,20))
    close('P2 5000to6050 over2years',m.effective_annual(5000,6050,2),F(1,10))
    close('P4 decline100to81',m.effective_annual(100,81,2),F(-1,10))
    close('same sign negativebalance support',m.periodic_rate(-100,-110,1),F(1,10))
    with localcontext() as ctx:
        ctx.prec=90
        continuous=D('1.10').ln()
        close('P3 continuous10%effective',m.continuous_rate(1000,1210,2),continuous)
        ratio=D('1.21')
        close('fractionalyear smoothannual model',m.effective_annual(1000,1210,1.5),ratio**(D(1)/D('1.5'))-1)
        nominal_ratio=(D(1)+D('.06')/12)**24
        future=float(D(1000)*nominal_ratio)
        close('nominalmonthly inverse24completeperiods',m.nominal_annual(1000,future,2,12),D('.06'))
    close('quarterannualization only when periodisquarter',(1+m.periodic_rate(8000,9680,2))**4-1,F(14641,10000)-1)
    ck('P5 zero growth across all conventions',
       m.periodic_rate(1000,1000,3)==0 and m.effective_annual(1000,1000,3)==0 and
       m.continuous_rate(1000,1000,3)==0 and m.nominal_annual(1000,1000,3,12)==0)
    implied=m.effective_annual(5000,6050,2)
    ck('inferred rate reconstructs unroundedbalance',abs(5000*(1+implied)**2-6050)<1e-9)
    ratio=math.nextafter(1.,2.)
    probes=[
      ('nominal period-product overflow',lambda:m.nominal_annual(1,2,1e308,12)),
      ('periodic rate underflow',lambda:m.periodic_rate(1,ratio,10**308)),
      ('effective rate underflow',lambda:m.effective_annual(1,ratio,1e308)),
      ('continuous rate underflow',lambda:m.continuous_rate(1,ratio,1e308)),
      ('nominal rate underflow',lambda:m.nominal_annual(1,ratio,1e308,1))]
    for label,fn in probes:
        try:actual=fn()
        except ValueError as error:ck('F48 '+label+' rejected',True,exception=str(error))
        except Exception as error:ck('F48 '+label+' rejected',False,exception=repr(error))
        else:ck('F48 '+label+' rejected',False,actual=actual)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=6,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
