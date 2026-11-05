"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.05-present-value.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-95-') as tmp:
        lab=Path(tmp);(lab/'present_value.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['present_value.py']),('exact compilation',['-m','compileall','-q','present_value.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='5000 in three years at 4% effective annually: PV = 4444.98\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_pv');exec(compile(code,str(source),'exec'),m.__dict__)
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    pv=m.present_value
    factor=F(26,25)**3
    close('worked present value from rational reciprocal',pv(5000,.04,3),F(5000)/factor)
    close('worked future reconstruction retains full input',pv(5000,.04,3)*float(factor),F(5000))
    close('wrong subtraction fails to invert',4400*float(factor),F(4400)*factor)
    close('today common-date advantage',4500-pv(5000,.04,3),4500-F(5000)/factor)
    close('year3 common-date advantage',4500*float(factor)-5000,4500*factor-5000)
    close('P1 1210 discounts to1000',pv(1210,.1,2),F(1000))
    close('P1 rational roundtrip',pv(1210,.1,2)*float(F(11,10)**2),F(1210))
    close('P2 payer obligation staysnegative',pv(-2160,.08,1),F(-2000))
    close('P3 offers equal at common valuation date',pv(1210,.1,2),F(1000))
    ck('P4 fixed positive payment decreases at higher rate',pv(5000,.06,3)<pv(5000,.04,3))
    exact=F(5000)/factor
    rounded=pv(5000,.04,3);rounded=round(rounded,2)
    ck('P5 display rounding changes reverse amount',
       abs(rounded*float(factor)-5000)>1e-6 and abs(pv(5000,.04,3)*float(factor)-5000)<1e-9)
    close('negative-rate present exceeds future amount',pv(1000,-.02,1),F(1000)/F(49,50))
    close('staged constant-rate discount',pv(pv(5000,.04,2),.04,1),F(5000)/factor)
    ck('zero boundaries preserve signed amount',pv(-5000,0,20)==-5000 and pv(5000,.04,0)==5000 and pv(0,.04,3)==0)
    # Cross-section boundary: a finite nonzero Real must not vanish in conversion.
    tiny=F(1,1<<2000)
    all_sources={str(source.relative_to(BOOK)):sha(source.read_bytes())}
    modules=[('9.5',m,lambda mod:mod.present_value(tiny,.04,1))]
    legacy=[
      ('9.1','9.01-the-time-value-of-money.md','tvm_introduction',lambda mod:mod.equivalent(tiny,.05,1,to_future=True)),
      ('9.3','9.03-simple-interest.md','simple_interest',lambda mod:mod.simple_interest(tiny,.05,1)),
      ('9.4','9.04-compound-interest.md','compound_interest',lambda mod:mod.compound_amount(tiny,.04,1))]
    with tempfile.TemporaryDirectory(prefix='book1-range-followup-') as tmp:
        for sec,name,modname,call in legacy:
            path=BOOK/'chapter-09'/name
            listing,=re.findall(rb'^```python\n(.*?)^```',path.read_bytes(),re.M|re.S)
            all_sources[str(path.relative_to(BOOK))]=sha(path.read_bytes())
            lab=Path(tmp)/sec;lab.mkdir();(lab/(modname+'.py')).write_bytes(listing)
            for label,args in [('legacy exact unittest',['-m','unittest',modname,'-v']),('legacy exact compilation',['-m','compileall','-q',modname+'.py'])]:
                r=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
                match=re.search(r'Ran (\d+) tests?',r.stderr);count=int(match[1]) if match else None
                ok=r.returncode==0 and (count==8 and bool(re.search(r'^OK\s*$',r.stderr,re.M)) if 'unittest' in label else not(r.stdout or r.stderr))
                commands.append(dict(section=sec,label=label,args=args,stdout=r.stdout,stderr=r.stderr,returncode=r.returncode,methods=count,passed=ok))
            mod=types.ModuleType('range_'+sec);exec(compile(listing,str(path),'exec'),mod.__dict__)
            modules.append((sec,mod,call))
        for sec,mod,call in modules:
            try:actual=call(mod)
            except ValueError as error:ck(sec+' rejects nonzero principal/payment lost during input conversion',True,exception=str(error),exact_input='1 / 2**2000')
            except Exception as error:ck(sec+' rejects nonzero principal/payment lost during input conversion',False,exception=repr(error))
            else:ck(sec+' rejects nonzero principal/payment lost during input conversion',False,actual=repr(actual),exact_input='1 / 2**2000')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),all_source_sha256=all_sources,commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
