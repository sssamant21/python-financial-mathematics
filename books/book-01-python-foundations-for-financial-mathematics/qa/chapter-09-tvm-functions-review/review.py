"""Section 9.15 exact module and independent numerical review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.15-python-tvm-functions.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-915-') as tmp:
        lab=Path(tmp);(lab/'tvm_functions.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['tvm_functions.py']),('exact compilation',['-m','compileall','-q','tvm_functions.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='FV: 1,127.16\nEAR: 6.167781%\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_tvm');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def close(label,actual,reference,atol=1e-12,rtol=1e-12):
        ck(label,math.isclose(actual,float(reference),rel_tol=rtol,abs_tol=atol),actual=actual,reference=str(reference),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (ValueError,TypeError) as e:ck(label,True,exception=str(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=actual)
    with localcontext() as ctx:
        ctx.prec=100
        factor=(D(1)+D('.06')/12)**24
        close('worked monthly FV',m.future_value(1000,.06,2,12),D(1000)*factor)
        close('worked NPV',m.net_present_value([(0,-1000),(1,1100)],.1),0)
        close('P1 FV',m.future_value(2000,.05,2),F(2205))
        close('P2 PV',m.present_value(2205,.05,2),F(2000))
        ear=(1+D('.06')/12)**12-1
        close('P3 EAR',m.effective_annual(.06,12),ear)
        close('P4 continuous FV',m.continuous_future_value(500,.04,3),D(500)*D('.12').exp())
        close('P5 NPV',m.net_present_value([(0,-100),(1,110)],.1),0)
        close('nominal conversion back',m.nominal_from_effective(float(ear),12),D('.06'))
        close('nominal inverse',m.solve_nominal_rate(1000,float(1000*factor),2,12),D('.06'))
        close('time inverse',m.solve_years(1000,float(1000*factor),.06,12),2)
    close('discrete roundtrip',m.present_value(m.future_value(-1200,.03,1.5,4),.03,1.5,4),-1200)
    close('continuous roundtrip',m.continuous_present_value(m.continuous_future_value(750,-.02,2),-.02,2),750)
    close('empty iterable',m.net_present_value(iter(()),.05),0)
    close('cancellation fsum',m.net_present_value(iter([(0,1e16),(0,1),(0,-1e16)]),0),1)
    close('true zero inferred rate',m.solve_nominal_rate(-100,-100,3,12),0)
    close('true zero elapsed time',m.solve_years(-100,-100,.05,12),0)
    reject('negative date',lambda:m.net_present_value([(-1,100)],.05))
    reject('zero rate nonunique time',lambda:m.solve_years(100,100,0))
    reject('zero rate unreachable time',lambda:m.solve_years(100,110,0))
    tiny=F(1,10**400)
    reject('F46 nonzero amount conversion underflow',lambda:m.future_value(tiny,.05,1))
    reject('F46 nonzero rate conversion underflow',lambda:m.future_value(100,tiny,1))
    reject('F47 nominal reverse underflow',lambda:m.nominal_from_effective(5e-324,12))
    reject('F48 totalperiod overflow',lambda:m.solve_nominal_rate(1,2,1e308,12))
    reject('F48 inference division underflow',lambda:m.solve_nominal_rate(1,math.nextafter(1.,2.),1e308))
    p=1e300;up=math.nextafter(p,math.inf);down=math.nextafter(p,0.)
    for label,f,rate in [('increase',up,.05),('decline',down,-.05)]:
        with localcontext() as ctx:
            ctx.prec=100
            ratio=D.from_float(f)/D.from_float(p)
            reference=ratio.ln()/(1+D(str(rate))).ln()
            rate_reference=ratio-1
        close('F49 nearby time '+label,m.solve_years(p,f,rate),reference,atol=0)
        close('F49 nearby implied rate '+label,m.solve_nominal_rate(p,f,1),rate_reference,atol=0)
    reject('F49 opposed nearby target',lambda:m.solve_years(p,up,-.05))
    reject('F49 elapsed division underflow',lambda:m.solve_years(1,math.nextafter(1.,0.),-8e307,10**308))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=6,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
