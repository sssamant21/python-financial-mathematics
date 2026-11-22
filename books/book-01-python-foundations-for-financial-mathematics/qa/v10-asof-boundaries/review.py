"""Availability audit under supplied clocks, latency and revision provenance boundaries."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime,timezone,timedelta
import subprocess,tempfile,re,importlib.util,json,sys,hashlib,platform,itertools
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='e40e5540302f0767f169978f9964e94655d5fc1e';path='books/book-01-python-foundations-for-financial-mathematics/chapter-15/15.13-statistical-pitfalls-in-financial-data.md';raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);listing=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S)[0];rows=[];commands=[];models=[]
def ck(name,got,want,kind):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=got==want))
with tempfile.TemporaryDirectory() as tmp:
 f=Path(tmp)/'statistical_pitfalls.py';f.write_text(listing);spec=importlib.util.spec_from_file_location('pitfall_source',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for args in [[sys.executable,f.name],[sys.executable,'-m','compileall','-q',f.name]]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 offsets=[timezone(timedelta(hours=-5)),timezone.utc,timezone(timedelta(hours=5,minutes=30))];epoch=datetime(2026,1,1,tzinfo=timezone.utc);ticks=list(range(-2,3));aware_records=[]
 for i,d in enumerate(ticks):
  for j,a in enumerate(ticks):
   ck(f'numeric decision{d} available{a}',m.audit_asof([(d,a)]),[a>d],'native flag vs declared integer-clock order')
   decision=(epoch+timedelta(seconds=d)).astimezone(offsets[i%3]);available=(epoch+timedelta(seconds=a)).astimezone(offsets[(j+1)%3]);got=m.audit_asof([(decision,available)])
   ck(f'aware decision{d} available{a}',got,[a>d],'native UTC flag vs known elapsed-second construction, not lexical clocks')
   aware_records.append(dict(decision=decision.isoformat(),available=available.isoformat(),known_decision_seconds=d,known_available_seconds=a,flag=got[0]))
 for available,delay,eligible in [(9.8,.1,True),(9.95,.1,False),(10,.1,False)]:
  ck(f'latency boundary availability{available} native flag',m.audit_asof([(10,available)]),[False],'source only compares recorded availability to decision')
  actual=F(str(available))+F(str(delay))<=10;ck(f'latency boundary availability{available} caller readiness',actual,eligible,'supplemental positive processing-delay convention, not native pipeline acceptance')
 revision=[dict(value=100,available=9),dict(value=150,available=12)]
 for decision,expected_flags,expected_value in [(10,[False,True],100),(13,[False,False],150)]:
  flags=m.audit_asof([(decision,r['available']) for r in revision]);ck('revision flags at'+str(decision),flags,expected_flags,'native flags of supplied version availability')
  selected=max((r for r,late in zip(revision,flags) if not late),key=lambda r:r['available'])['value'];ck('caller latest eligible revision at'+str(decision),selected,expected_value,'caller version selection, no native as-of join/version adapter')
 ck('supplied backdated availability not authenticated',m.audit_asof([(10,9)]),[False],'same numeric record could carry a misdeclared revised value; source has no source-authenticity input')
 ck('mismatched numeric units cause late flag',m.audit_asof([(10,9000)]),[True],'declared seconds versus supplied milliseconds violates caller common-unit prerequisite')
 ck('caller unit conversion gives safe flag',m.audit_asof([(10,9)]),[False],'9000ms converted to9seconds, no native conversion API')
 for name,record in [('bool ticks',[(True,1)]),('nonfinite ticks',[(1,float('nan'))]),('lexical timestamps',[('10','9')]),('naive datetimes',[(datetime(2026,1,1),datetime(2026,1,1))]),('mixed clock families',[(10,epoch)])]:
  try:m.audit_asof(record);actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(name,actual,'ValueError','native clock-family/domain rejection, not clock synchronization validation')
 models.append(dict(name='known-clock matrix',numeric_cases=25,aware_cases=25,aware_records=aware_records,scope='Fixed explicit UTC offsets only; no new ZoneInfo/DST database/platform claim. Earlier F139 DST evidence retains its own scope.'))
 models.append(dict(name='caller pipeline and revision policy',revision_records=revision,processing_latency_seconds='.1',scope='Publication/ingestion/readiness/decision/execution clocks and metadata authenticity remain caller contracts. Native False is not an acceptance signal.'))
prior=json.loads((here.parent/'chapter-15-pitfalls-review/results.json').read_text());assert hashlib.sha256(listing.encode()).hexdigest()==prior['listing_sha256'];clarification=json.loads((here.parent/'v10-selection-ledger/F219-assumption-clarification.json').read_text());assert hashlib.sha256(raw).hexdigest()==clarification['candidate_source_sha256']
result=dict(pin=pin,executed_at_utc=datetime.now(timezone.utc).isoformat(),source_path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(listing.encode()).hexdigest(),python=platform.python_version(),platform=platform.platform(),rows=rows,models=models,commands=commands,prior_evidence_identity_verified=True,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),scope='Supplied clock/availability/revision boundary review; no authentic source, latency, venue execution, real revision history, platform or independent acceptance')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
