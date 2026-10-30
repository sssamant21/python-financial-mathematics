"""Chapter 7 chapter-wide source execution, captured locals and scoped oracles."""
import hashlib,json,math,os,platform,re,subprocess,sys,tempfile
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
PROMPTS=BOOK/'chapter-07/7.18-exercises-and-applied-problems.md'
SOURCE=BOOK/'chapter-07/7.18-solutions-and-reference-implementations.md'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
    text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==1
    checks=[];commands=[]
    def ck(problem,label,a,x):checks.append(dict(problem=problem,label=label,actual=repr(a),expected=repr(x),status='PASS' if a==x else 'FAIL'))
    def near(problem,label,a,x):ck(problem,label,math.isclose(float(a),float(x),rel_tol=1e-12,abs_tol=1e-12),True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    with tempfile.TemporaryDirectory(prefix='chapter07-answers-') as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_718';lab.mkdir();script=lab/'chapter07_solutions.py';script.write_text(blocks[0]);compile(blocks[0],str(script),'exec')
        specs=[('unchanged source discovery',['-m','unittest','discover','-s','pandas_lab_718','-p','chapter07_solutions.py','-v'],20),('unchanged source compileall',['-m','compileall','-q','pandas_lab_718'],None),('observer rerun, unchanged source',[str(HERE/'observe.py'),str(script),str(HERE/'observed-locals.json')],20)]
        for label,args,count in specs:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=parent,env=env,capture_output=True,text=True,timeout=60)
            counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None
            ok=r.returncode==0 and ((actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))) if count is not None else r.stdout==r.stderr=='')
            commands.append(dict(label=label,args=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
        ck('ALL','original listing bytes unchanged',sha(script.read_bytes()),sha(blocks[0].encode()))
    obs=json.loads((HERE/'observed-locals.json').read_text());ck('ALL','all twenty original methods observed',sorted(obs),['test_problem_'+str(i).zfill(2) for i in range(1,21)])
    def record(i,key):return obs['test_problem_'+str(i).zfill(2)][key]
    weights=dict(zip(record(1,'w')['index'],map(F,record(1,'w')['values'])));decimal_w={'A':F(3,5),'B':F(3,10),'C':F(1,10)};decimal_r={'C':F(0),'A':F(1,10),'B':F(-1,20)}
    ck('01','independent aligned vs positional arithmetic',(sum(decimal_w[k]*decimal_r[k] for k in decimal_w),sum(w*r for w,r in zip(decimal_w.values(),decimal_r.values()))),(F(9,200),F(1,40)))
    ck('01','source fixture arrival order retained',record(1,'r')['index'],['C','A','B'])
    ck('02','source series metadata',(record(2,'s')['name'],record(2,'s')['index_name'],record(2,'s')['dtype']),('opening_value','asset','float64'))
    ck('02','integer identity order distinct from positions',(record(2,'t')['index'],record(2,'t')['values']),([1,0],[10.,20.]))
    ck('03','independent quantity times price values',record(3,'t')['values'],[[6.,100.,600.],[3.,100.,300.]])
    ck('04','owned reordered subset vs unchanged source',(record(4,'s')['index'],record(4,'s')['values'],record(4,'t')['values']),(['C','A'],[[100.],[0.]],[[600.],[300.],[100.]]))
    ck('05','literal identifiers and separately parsed source fields',record(5,'t')['values'],[['00123','100'],['NA','80']])
    ck('06','nullable observed zero vs unknown',(record(6,'s')['dtype'],record(6,'s')['values']),('Int64',[6,None,0]))
    ck('07','coerced values and distinct missing counts',record(7,'parsed')['values'],[100.,None,None])
    raw=record(7,'raw')['values'];parsed=record(7,'parsed')['values'];ck('07','introduced vs total missing', (sum(a is not None and b is None for a,b in zip(raw,parsed)),sum(b is None for b in parsed)),(1,2))
    ck('08','incomplete contribution population retained',record(8,'s')['values'],[.06,None,0.])
    ck('09','all normalized duplicates flagged',(record(9,'normalized')['values'],record(9,'duplicates')['values']),(['BETA','BETA','CASH'],[True,True,False]))
    ck('09','raw spaced token still retained',record(9,'raw')['values'][0][0],' BETA ')
    ck('10','offset arithmetic gives same UTC instant',record(10,'t')['values'],['2026-01-30T15:00:00+00:00']*2)
    ck('11','winter localization and two half-hour instants',(record(11,'local')['values'],record(11,'idx')['values']),(['2026-01-30T09:30:00-05:00'],['2026-01-30T14:30:00+00:00','2026-01-30T15:00:00+00:00']))
    ck('12','mask and authored query preserve identical rows',record(12,'a'),record(12,'b'))
    candidates=record(12,'a')['values'];chosen=[r[0] for r in sorted(candidates,key=lambda r:(-r[2],r[0]))[:2]];ck('12','independent tie ordering',chosen,['A','B'])
    ck('13','rational sector denominators',(F(45,900), (F(1,10)+F(-1,20))/2, F(45,1000)),(F(1,20),F(1,40),F(9,200)))
    ck('14','two by two quote multiplication count',len(record(14,'a')['values'])*len(record(14,'b')['values']),4)
    audit=record(15,'r');ck('15','all outer match categories',dict(zip(audit['index'],[row[-1] for row in audit['values']])),{'A':'both','B':'left_only','C':'right_only'})
    events=record(16,'t');ck('16','source event instants retained',events['index'],['2026-01-30T14:00:00+00:00','2026-01-30T14:29:00+00:00','2026-01-30T15:00:00+00:00'])
    # Supplemental bar materialization; source g is a resampler, not a stored result.
    event_frame=pd.DataFrame({'price':[100.,102.,101.],'volume':[10.,20.,5.]},index=pd.to_datetime(events['index']))
    g=event_frame.resample('30min',closed='left',label='right',origin='epoch');ohlc=g['price'].ohlc();volume=g['volume'].sum(min_count=1)
    ck('16','supplemental bin labels',list(map(lambda x:x.isoformat(),ohlc.index)),['2026-01-30T14:30:00+00:00','2026-01-30T15:00:00+00:00','2026-01-30T15:30:00+00:00'])
    ck('16','independent observed first bar',ohlc.iloc[0].tolist(),[100.,102.,100.,102.]);ck('16','empty middle bin stays missing',bool(ohlc.iloc[1].isna().all() and pd.isna(volume.iloc[1])),True)
    ck('17','observed rolling warm-up',record(17,'m')['values'],[None,None,102.,104.])
    ck('17','independent expanding arithmetic',[sum(map(F,[100,102,104,106][:n]))/n for n in range(1,5)],list(map(F,[100,101,102,103])))
    ck('18','undefined first return remains missing',record(18,'r')['values'][0],None);near('18','source linked return',record(18,'linked'),F(-1,100))
    ck('19','source complete expected grid',record(19,'w')['values'],[[100.,200.],[110.,None],[99.,220.]])
    ck('19','B no-fill grid returns stay missing',[row[1] for row in record(19,'r')['values']],[None,None,None])
    ck('20','source compact release flags and withheld B',(record(20,'complete')['values'],record(20,'linked')['B']),([True,False],None))
    # A concrete supplemental Problem20 record for the actual five-row panel.
    payload=b'time,asset,price\n2026-01-30T16:00:00Z,A,100\n2026-01-31T16:00:00Z,A,110\n2026-02-01T16:00:00Z,A,99\n2026-01-30T16:00:00Z,B,200\n2026-02-01T16:00:00Z,B,220\n'
    (HERE/'panel.csv').write_bytes(payload)
    times=['2026-01-30T16:00:00+00:00','2026-01-31T16:00:00+00:00','2026-02-01T16:00:00+00:00'];panel=record(19,'w')['values']
    report=dict(scope='supplemental controlled Problem20 record, not Section7.17 analyzer execution',source_sha256=sha(payload),source_record_count=5,expected_assets=['A','B'],expected_times=times,expected_cells=6,observed_cells=5,versions=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__),policy='strict no-fill adjacent expected-grid price-only path; no linked result for incomplete path',assets={})
    for j,asset in enumerate(('A','B')):
        prices=[row[j] for row in panel];complete=all(v is not None for v in prices);endpoint=F(prices[-1])/F(prices[0])-1
        linked=math.prod(F(prices[i])/F(prices[i-1]) for i in range(1,3))-1 if complete else None
        report['assets'][asset]=dict(observed_prices=sum(v is not None for v in prices),expected_prices=3,complete_path=complete,endpoint_return=float(endpoint),linked_return=float(linked) if linked is not None else None,release_linked=complete)
    (HERE/'panel-report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    ck('20','supplemental actual-panel record count',len(payload.decode().splitlines())-1,5)
    ck('20','separate endpoint/linked decisions',report['assets'],{'A':dict(observed_prices=3,expected_prices=3,complete_path=True,endpoint_return=-.01,linked_return=-.01,release_linked=True),'B':dict(observed_prices=2,expected_prices=3,complete_path=False,endpoint_return=.1,linked_return=None,release_linked=False)})
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),prompt_source_sha256=sha(PROMPTS.read_bytes()),companion_source_sha256=sha(SOURCE.read_bytes()),executed_listing_sha256=sha(blocks[0].encode()),answer_records=20,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),existing_method_invocations=sum(c['actual_methods'] or 0 for c in commands),existing_unique_methods=20,predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),supplemental_evidence_sha256={name:sha((HERE/name).read_bytes()) for name in ('observe.py','observed-locals.json','panel.csv','panel-report.json')},commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('commands','checks','supplemental_evidence_sha256')}));return bool(output['failed'] or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
