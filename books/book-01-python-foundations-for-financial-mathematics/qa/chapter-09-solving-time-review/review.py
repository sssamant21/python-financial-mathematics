"""Section 9.14 exact lab with independent logarithmic and contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.14-solving-for-time.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-914-') as tmp:
        lab=Path(tmp);(lab/'solving_for_time.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['solving_for_time.py']),('exact compilation',['-m','compileall','-q','solving_for_time.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Time to grow 1000 to 1210 at 10% EAR: 2.000000 years\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_time');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    def close(label,value,expect,atol=1e-12):
        ck(label,abs(value-float(expect))<=atol,actual=value,high_precision_reference=str(expect),absolute_tolerance=atol)
    with localcontext() as ctx:
        ctx.prec=100
        close('worked annual1000to1210',m.effective_years(1000,1210,.1),F(2))
        close('P1 annual500to605',m.effective_years(500,605,.1),F(2))
        doubling=D(2).ln()/D('1.08').ln()
        close('P2 doubling8%',m.effective_years(100,200,.08),doubling)
        monthly=D('1.10').ln()/D('1.01').ln()
        close('P4 monthlyperiods',m.periodic_periods(100,110,.01),monthly)
        double7=D(2).ln()/D('1.07').ln()
        close('worked doubling7%',m.effective_years(100,200,.07),double7)
        close('P3 continuousfactor exp.15',
              m.continuous_years(100,float(D(100)*D('.15').exp()),.05),F(3))
        fv=D(1000)*(1+D('.06')/12)**24
        close('nominalmonthly24periods',m.nominal_years(1000,float(fv),.06,12),F(2))
        p=1e300;up=math.nextafter(p,math.inf);down=math.nextafter(p,0.)
        up_ref=(D.from_float(up)/D.from_float(p)).ln()/D('1.05').ln()
        down_ref=(D.from_float(down)/D.from_float(p)).ln()/D('.95').ln()
    close('P5 negativeannualdecline',m.effective_years(100,81,-.1),F(2))
    close('same-sign liabilitydecline',m.effective_years(-100,-81,-.1),F(2))
    ck('P4 firstfull monthlycredit is10',F(101,100)**9<F(11,10)<=F(101,100)**10)
    ck('worked doublingfirstannualcredit is11',F(107,100)**10<F(2)<=F(107,100)**11)
    for label,pv,fv in [('impossible',100,120),('nonunique',100,100)]:
        try:m.effective_years(pv,fv,0)
        except ValueError as error:ck('P6 '+label+' zero rate rejected',True,exception=str(error))
        else:ck('P6 '+label+' zero rate rejected',False)
    ck('equal balances at nonzero rate havezero time',m.effective_years(100,100,.04)==0 and m.continuous_years(-100,-100,-.04)==0)
    for label,actual,reference in [('increase',m.effective_years(p,up,.05),up_ref),
                                    ('decline',m.effective_years(p,down,-.05),down_ref)]:
        ck('F49 adjacentlargebalance '+label,math.isclose(actual,float(reference),rel_tol=1e-12,abs_tol=0),
           actual=actual,decimal_reference=str(reference),relative_tolerance=1e-12,absolute_tolerance=0)
    for label,fn in [
       ('opposed adjacent target',lambda:m.effective_years(p,up,-.05)),
       ('division underflow',lambda:m.continuous_years(1,math.nextafter(1.,2.),1e308)),
       ('nonfinite nominal log factor',lambda:m.nominal_years(100,50,-9e307,10**308))]:
        try:actual=fn()
        except ValueError as error:ck('F49 '+label+' rejected',True,exception=str(error))
        except Exception as error:ck('F49 '+label+' rejected',False,exception=repr(error))
        else:ck('F49 '+label+' rejected',False,actual=actual)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=6,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
