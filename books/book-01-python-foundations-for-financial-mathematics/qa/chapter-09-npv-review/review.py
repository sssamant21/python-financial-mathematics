"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.09-net-present-value.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-99-') as tmp:
        lab=Path(tmp);(lab/'net_present_value.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['net_present_value.py']),('exact compilation',['-m','compileall','-q','net_present_value.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='PV of future net flows: 1130.55 USD\nInitial cost: 1100.00 USD; NPV: +30.55 USD at t=0\nRate 0%: NPV +180.00 USD\nRate 5%: NPV +30.55 USD\nRate 10%: NPV -93.99 USD\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_npv');sys.modules[m.__name__]=m
    try:exec(compile(code,str(source),'exec'),m.__dict__)
    finally:sys.modules.pop(m.__name__,None)
    npv=m.net_present_value;Flow=m.Flow
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    events=m.fixture();rows,value=npv(1100,events,.05)
    future=300*F(20,21)-40*F(20,21)**2+1020*F(20,21)**3
    close('worked futureflows PV',m.value_flows(events,.05)[1],future)
    close('worked NPV includes costonce',value,future-1100)
    ck('initial cost audit factor1 and negated amount',rows[0]==('__initial_cost__',0,-1100,1,-1100))
    close('price sensitivity',npv(1150,events,.05)[1],future-1150)
    close('break-even cost computed at fullprecision',npv(float(future),events,.05)[1],F(0))
    for rate in [F(0),F(1,20),F(1,10)]:
        g=1+rate;expected=-1100+300/g-40/g**2+1020/g**3
        close('fixed schedule rate scenario '+str(rate),npv(1100,events,float(rate))[1],expected)
    one=[Flow('future',2,1210)]
    close('P1 nominalgrowth does not imply positiveNPV',npv(1000,one,.1)[1],F(0))
    close('P2 added initialcost decreases NPV',npv(1050,one,.1)[1],F(-50))
    ck('P3 supplemental costs subtractedonce',F(2400)-F(2250)==F(150),
       scope='Given aggregate PV and cost, not a separately specified event schedule')
    try:npv(100,[Flow('unknowncleanup',2,None)],.05)
    except TypeError:ck('P4 unknown cleanup rejected',True)
    else:ck('P4 unknown cleanup rejected',False)
    mixed=[Flow('in',1,230),Flow('out',2,-132)]
    for r in [F(1,10),F(1,5),F(3,20)]:
        exact=-100+230/(1+r)-132/(1+r)**2
        close('mixed signs exact NPV '+str(r),npv(100,mixed,float(r))[1],exact)
    a=npv(1000,[Flow('a',1,1200)],.1)[1];b=npv(1100,[Flow('b',1,1280)],.1)[1]
    incremental=npv(100,[Flow('inc',1,80)],.1)[1]
    close('incremental BminusA',b-a,F(-300,11))
    close('separate incremental schedule',incremental,F(-300,11))
    ck('order reversal preserves all auditrows',npv(1100,reversed(events),.05)==(rows,value))
    for label,cost,flows in [('cost',F(1,1<<2000),[]),('futureevent',0,[Flow('tiny',1,F(1,1<<2000))])]:
        try:npv(cost,flows,.05)
        except ValueError as error:ck('F46 '+label+' conversion loss rejected',True,exception=str(error))
        except Exception as error:ck('F46 '+label+' conversion loss rejected',False,exception=repr(error))
        else:ck('F46 '+label+' conversion loss rejected',False,actual='nonzero scalar accepted aszero')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
