"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.08-multiple-cash-flows.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-98-') as tmp:
        lab=Path(tmp);(lab/'multiple_cash_flows.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['multiple_cash_flows.py']),('exact compilation',['-m','compileall','-q','multiple_cash_flows.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Event | Period | Amount | Factor to t=0 | Equivalent (USD)\nincome1 | 1 | +300.00 | 0.952380952 | +285.71\nfee2 | 2 | -40.00 | 0.907029478 | -36.28\nincome3 | 3 | +120.00 | 0.863837599 | +103.66\nprincipal3 | 3 | +900.00 | 0.863837599 | +777.45\nTotal at t=0: 1130.55 USD\nTotal at t=3: 1308.75 USD\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_multiflows');sys.modules[m.__name__]=m
    try:exec(compile(code,str(source),'exec'),m.__dict__)
    finally:sys.modules.pop(m.__name__,None)
    vf=m.value_flows;Flow=m.Flow
    def close(label,value,expect,atol=1e-10):
        ck(label,abs(value-float(expect))<=atol,actual=value,exact_reference=str(expect),absolute_tolerance=atol)
    events=m.fixture();rows,total=vf(events,.05)
    exact_rows=[('income1',1,300),('fee2',2,-40),('income3',3,120),('principal3',3,900)]
    for row,(name,t,a) in zip(rows,exact_rows):
        factor=F(20,21)**t
        ck('full auditrow '+name,row[:3]==(name,t,a) and abs(row[3]-float(factor))<1e-12
           and abs(row[4]-float(a*factor))<1e-10,
           exact_factor=str(factor),exact_equivalent=str(a*factor))
    pv=sum(F(a)*F(20,21)**t for _,t,a in exact_rows)
    close('independent summed PV',total,pv)
    close('common future target3',vf(events,.05,target=3)[1],F(130875,100))
    middle=sum(F(a)*F(21,20)**(2-t) for _,t,a in exact_rows)
    close('common intermediate target2',vf(events,.05,target=2)[1],middle)
    ck('source reversal retains ordered audit and total',vf(reversed(events),.05)==(rows,total))
    simple=[Flow('one',1,110),Flow('two',2,121)]
    close('P1 time0 two receipts',vf(simple,.1)[1],F(200))
    close('P2 target2 two receipts',vf(simple,.1,target=2)[1],F(242))
    two=[Flow('receipt',2,150),Flow('fee',2,-50)]
    tr,tt=vf(two,.05,target=2)
    ck('P3 same-date net retains two sourceevents',len(tr)==2 and tt==100)
    cross=[Flow('receipt',1,100),Flow('payment',3,-100)]
    close('P4 differently dated equal nominal amounts do notcancel',vf(cross,.05)[1],
          F(100)*F(20,21)-F(100)*F(20,21)**3)
    opposite=[Flow(e.event_id,e.period,-e.amount) for e in events]
    close('perspective reversal',vf(opposite,.05)[1],-pv)
    ck('immediate empty and explicitzero remain distinct audit',
       vf([],.05)==([],0) and len(vf([Flow('zero',0,0)],.05)[0])==1 and vf([Flow('now',0,-1000)],.05)[1]==-1000)
    close('careful source summation preserves cancellation residual',
          vf([Flow('a',0,1e16),Flow('b',0,1),Flow('c',0,-1e16)],0)[1],F(1))
    try:vf([Flow('tiny',1,F(1,1<<2000))],.05)
    except ValueError as error:ck('F46 lostnonzeroevent rejected',True,exception=str(error))
    except Exception as error:ck('F46 lostnonzeroevent rejected',False,exception=repr(error))
    else:ck('F46 lostnonzeroevent rejected',False,actual='accepted nonzero rational event aszero')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
