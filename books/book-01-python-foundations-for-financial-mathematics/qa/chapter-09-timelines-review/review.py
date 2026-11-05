"""Section9.1 exact lab with rational and conceptual-contract review."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    source=BOOK/'chapter-09/9.02-financial-timelines.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    checks=[];commands=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='book1-92-') as tmp:
        lab=Path(tmp);(lab/'financial_timeline.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['financial_timeline.py']),('exact compilation',['-m','compileall','-q','financial_timeline.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=lab,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',p.stderr);methods=int(match[1]) if match else None
            if label.startswith('exact demonstration'):
                ok=methods==8 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='Investor cash flows; USD; annual boundary periods\nt=0: -1000.00\nt=1: +75.00\nt=2: +0.00\nt=3: +1080.00\n'
            else:ok=not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,methods=methods,passed=ok and p.returncode==0))
    m=types.ModuleType('exact_timeline');sys.modules[m.__name__]=m
    try:exec(compile(code,str(source),'exec'),m.__dict__)
    finally:sys.modules.pop(m.__name__,None)
    D=m.Decimal;E=m.Event
    original=m.fixture()
    ordered,totals=m.timeline(original,horizon=3,currency='USD')
    oracle={0:-100000,1:7500,2:0,3:108000}
    ck('every fixture total from independent integer cents',
       {t:int(v*100) for t,v in totals.items()}==oracle)
    ck('dense grid includes four boundaries for three intervals',list(totals)==[0,1,2,3])
    ck('five separate event identities retained',
       len(ordered)==5 and {e.event_id for e in ordered}=={'initial','income1','fee1','income3','principal3'})
    ck('simultaneous events sorted deterministically by ID',
       [e.event_id for e in ordered if e.period==1]==['fee1','income1'])
    rev=m.timeline(reversed(original),horizon=3,currency='USD')
    ck('source order does not change ledger or period totals',rev==(ordered,totals))
    borrower=(E('advance',0,D('2000'),'Loan'),E('first',1,D('-1100'),'Repay'),E('second',2,D('-1100'),'Repay'))
    bo,bt=m.timeline(borrower,horizon=2,currency='USD')
    lo,lt=m.timeline([E(e.event_id,e.period,-e.amount,e.description) for e in borrower],horizon=2,currency='USD')
    ck('P1 borrower and opposite lender schedules',
       list(bt.values())==list(map(D,['2000','-1100','-1100'])) and
       [bt[t]+lt[t] for t in bt]==[D(0)]*3)
    ck('P1 undiscounted signed sum is minus200',sum(bt.values(),D(0))==D('-200'))
    begin=[E('b'+str(i),i,D('-100'),'Beginning deposit') for i in range(3)]
    end=[E('e'+str(i),i+1,D('-100'),'End deposit') for i in range(3)]
    be,bv=m.timeline(begin,horizon=3,currency='USD')
    en,ev=m.timeline(end,horizon=3,currency='USD')
    ck('P2 shifting dates does not shift amount signs',
       [e.period for e in be]==[0,1,2] and [e.period for e in en]==[1,2,3] and
       all(e.amount==D('-100') for e in be+en))
    events=[E('receipt',2,D('50'),'Receipt'),E('fee',2,D('-50'),'Fee')]
    ze,zt=m.timeline(events,horizon=2,currency='USD')
    ck('P3 two gross events with zero period total',len(ze)==2 and zt[2]==0 and {e.event_id for e in ze}=={'receipt','fee'})
    empty,et=m.timeline([],horizon=2,currency='USD')
    ck('zero grid does not identify gross events',empty==() and et==zt)
    ck('P5 fixture undiscounted sum155 agrees with independent cents',
       sum(totals.values(),D(0))==D(sum(oracle.values()))/100)
    ck('input frozen events and original sequence preserved',
       original==m.fixture() and original[0].amount==D('-1000'))
    bad=E('unknown',2,D('NaN'),'Unknown')
    try:m.timeline([bad],horizon=3,currency='USD')
    except ValueError as error:ck('unknown amount rejected without imputing zero','unknown is not zero' in str(error))
    else:ck('unknown amount rejected without imputing zero',False)
    try:m.timeline([E('x',0,0.1,'Binaryfloat')],horizon=1,currency='USD')
    except TypeError:ck('float amount rejected before summing',True)
    else:ck('float amount rejected before summing',False)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=sha(source.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,workflow_records=1,local_exercises=5,
             historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
