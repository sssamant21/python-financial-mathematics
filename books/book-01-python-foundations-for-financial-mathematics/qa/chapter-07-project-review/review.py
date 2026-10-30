"""Unchanged Section 7.17 project: scoped commands, source probes and rational oracles."""
import contextlib,hashlib,io,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def safe(value):
    if isinstance(value,dict):return {str(k):safe(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [safe(v)for v in value]
    if isinstance(value,(np.bool_,np.integer)):return value.item()
    if isinstance(value,(float,np.floating)) and not np.isfinite(value):return None
    if isinstance(value,pd.Timestamp):return value.isoformat()
    return value
DEMO='''observed_prices expected_prices observed_intervals complete_path endpoint_return linked_return
asset
ALPHA 3 3 2 True -0.0100 -0.0100
BETA 2 3 0 False 0.1000 NaN
Complete aligned intervals: 0
Source records: 5
'''
def run():
    source=BOOK/'chapter-07/7.17-chapter-project-financial-time-series-analyzer.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==3
    fixture=re.findall(r'^```csv\n(.*?)^```',text,re.M|re.S);assert len(fixture)==1;payload=fixture[0].encode()
    checks=[];commands=[]
    def ck(label,actual,expected):checks.append(dict(label=label,actual=repr(actual),expected=repr(expected),status='PASS'if actual==expected else'FAIL'))
    def reject(label,fn,kind=ValueError):
        try:fn();actual='no exception';trace=''
        except Exception as error:actual=type(error).__name__;trace=traceback.format_exc();valid=isinstance(error,kind)
        else:valid=False
        ck(label,valid,True);checks[-1].update(actual_exception=actual,expected_exception=kind.__name__,expected_rejection_trace=trace)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    def command(label,args,cwd,expected=None,methods=None):
        r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
        count=re.findall(r'Ran (\d+) tests? in',r.stderr);count=int(count[0])if len(count)==1 else None;ok=r.returncode==0
        if expected is not None:
            normalize=lambda v:[' '.join(x.split())for x in v.splitlines()]
            ok=ok and normalize(r.stdout)==normalize(expected) and r.stderr==''
        if methods is not None:ok=ok and count==methods and bool(re.search(r'^OK\s*$',r.stderr,re.M))
        commands.append(dict(label=label,args=args,cwd_role='sibling lab'if label=='quiet production-module imports'else('unrelated directory'if label=='demonstration from unrelated directory'else'parent'),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=count,status='PASS'if ok else'FAIL'))
    with tempfile.TemporaryDirectory(prefix='chapter07-project-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_717';lab.mkdir();files=dict(zip(('panel.py','analyzer.py','test_analyzer.py'),blocks));files['prices.csv']=fixture[0]
        for name,body in files.items():
            (lab/name).write_bytes(body.encode())
            if name.endswith('.py'):compile(body,str(lab/name),'exec')
        command('prepared environment',['-c',"import platform,pandas as pd,numpy as np;print(platform.python_version(),pd.__version__,np.__version__)"] ,parent,expected='3.12.14 2.2.3 2.3.5\n')
        command('original demonstration',['pandas_lab_717/analyzer.py'],parent,expected=DEMO)
        command('original unittest discovery',['-m','unittest','discover','-s','pandas_lab_717','-v'],parent,methods=8)
        command('original compileall',['-m','compileall','-q','pandas_lab_717'],parent,expected='')
        command('quiet production-module imports',['-c','import panel,analyzer'],lab,expected='')
        other=parent/'unrelated';other.mkdir();command('demonstration from unrelated directory',[str(lab/'analyzer.py')],other,expected=DEMO)
        ck('four reconstructed files byte-identical',{n:sha((lab/n).read_bytes())for n in files},{n:sha(c.encode())for n,c in files.items()})
        previous=sys.modules.get('panel');pm=types.ModuleType('panel');exec(compile(blocks[0],str(source)+':fence0','exec'),pm.__dict__);sys.modules['panel']=pm
        try:
            am=types.ModuleType('exact_analyzer');exec(compile(blocks[1],str(source)+':fence1','exec'),am.__dict__)
            assets=('ALPHA','BETA');times=pd.date_range('2026-01-30T16:00:00Z',periods=3,freq='D');path=lab/'prices.csv'
            def analyze(data=payload,universe=assets,grid=times):
                probe=parent/'probe.csv';probe.write_bytes(data);return am.analyze(probe,universe,grid)
            result=am.analyze(path,assets,times);summary=result['summary'];e=result['evidence']
            ck('exact parsed payload identity',(e['sha256'],e['bytes'],e['records']),(sha(payload),len(payload),5))
            ck('runtime/currency evidence',(e['python'],e['pandas'],e['numpy'],e['currency']),('3.12.14','2.2.3','2.3.5','USD'))
            ck('independently specified grid retained',(result['prices'].columns.tolist(),[x.isoformat()for x in result['prices'].index]),(list(assets),[x.isoformat()for x in times]))
            ck('per-asset expected versus observed prices',(summary['observed_prices'].tolist(),summary['expected_prices'].tolist()),([3,2],[3,3]))
            ck('per-asset interval counts/complete path',(summary['observed_intervals'].tolist(),summary['complete_path'].tolist()),([2,0],[True,False]))
            ar=[F(110,100)-1,F(99,110)-1];alpha=(1+ar[0])*(1+ar[1])-1;beta=F(220,200)-1
            ck('rational ALPHA adjacent returns',bool(np.allclose(result['returns']['ALPHA'].iloc[1:],list(map(float,ar)),rtol=0,atol=1e-12)),True)
            ck('ALPHA linked return independent rational product',abs(summary.loc['ALPHA','linked_return']-float(alpha))<=1e-12,True)
            ck('ALPHA endpoint independent ratio',abs(summary.loc['ALPHA','endpoint_return']-float(F(99,100)-1))<=1e-12,True)
            ck('BETA endpoint-only rational ratio',abs(summary.loc['BETA','endpoint_return']-float(beta))<=1e-12,True)
            ck('BETA grid path not fabricated',(pd.isna(summary.loc['BETA','linked_return']),result['returns']['BETA'].isna().all()),(True,True))
            ck('coverage per time and complete interval',(result['coverage']['observed_prices'].tolist(),result['coverage']['expected_prices'].tolist(),result['coverage']['complete_interval'].tolist()),([2,1,2],[2,2,2],[False,False,False]))
            ck('rolling warmup and missing BETA',(result['rolling_mean_2']['ALPHA'].iloc[:2].isna().all(),result['rolling_mean_2']['BETA'].isna().all()),(True,True))
            ck('ALPHA arithmetic mean differs from linked return',(abs(result['rolling_mean_2']['ALPHA'].iloc[-1]-float(sum(ar)/2))<=1e-12,abs(summary.loc['ALPHA','linked_return']-.0)>1e-3),(True,True))
            complete_payload=payload+b'2026-01-31T16:00:00Z,BETA,USD,210\n';completed=analyze(complete_payload);br=[F(210,200)-1,F(220,210)-1]
            ck('completed fixture aligned coverage',completed['coverage']['complete_interval'].tolist(),[False,True,True])
            ck('completed BETA scalar rational intervals',bool(np.allclose(completed['returns']['BETA'].iloc[1:],list(map(float,br)),rtol=0,atol=1e-12)),True)
            ck('completed BETA linked full horizon',abs(completed['summary'].loc['BETA','linked_return']-float((1+br[0])*(1+br[1])-1))<=1e-12,True)
            ck('completed BETA rolling mean is not full horizon return',abs(completed['rolling_mean_2']['BETA'].iloc[-1]-float(sum(br)/2))<=1e-12,True)
            crlf=analyze(payload.replace(b'\n',b'\r\n'));ck('CRLF changes bytes not normalized report',(crlf['evidence']['sha256']!=e['sha256'],crlf['summary'].equals(summary)),(True,True))
            lines=payload.decode().splitlines();reverse=('\n'.join([lines[0],*lines[:0:-1]])+'\n').encode();reordered=analyze(reverse)
            ck('record-order byte evidence differs while report agrees',(reordered['evidence']['sha256']!=e['sha256'],reordered['summary'].equals(summary)),(True,True))
            absent=analyze(universe=assets+('CASH',));ck('absent expected asset stays visible',(absent['prices']['CASH'].isna().all(),absent['summary'].loc['CASH','observed_prices'],pd.isna(absent['summary'].loc['CASH','endpoint_return'])),(True,0,True))
            literal=analyze(payload.replace(b'ALPHA',b'NA'),universe=('NA','BETA'));ck('literal NA identifier preserved',literal['summary'].loc['NA','observed_prices'],3)
            # Deliberate source rejection probes; not unexpected failures.
            for label,data in [('duplicate composite key',payload+lines[1].encode()+b'\n'),('wrong currency',payload.replace(b'USD',b'EUR',1)),('wrong ordered header',payload.replace(b'time,asset',b'asset,time',1)),('wrong field width',payload.replace(b',100\n',b',100,extra\n',1)),('zero supplied price',payload.replace(b',100\n',b',0\n',1)),('missing numeric token',payload.replace(b',100\n',b',\n',1)),('exponent price token',payload.replace(b',100\n',b',1e2\n',1)),('naive time token',payload.replace(b'T16:00:00Z',b'T16:00:00',1)),('invalid calendar token',payload.replace(b'2026-01-30',b'2026-02-30',1)),('unexpected asset',payload.replace(b'ALPHA',b'OTHER'))]:
                reject('reject '+label,lambda data=data:analyze(data))
            reject('strict UTF8 rejects bad bytes',lambda:analyze(b'\xff'+payload),UnicodeDecodeError)
            reject('bounded snapshot rejects1000001bytes',lambda:analyze(b'x'*1_000_001))
            report={key:safe(result[key].reset_index().to_dict(orient='records'))for key in ('prices','returns','rolling_mean_2','coverage','summary')}
            fullreport={key:safe(completed[key].reset_index().to_dict(orient='records'))for key in ('prices','returns','rolling_mean_2','coverage','summary')}
            retained=dict(scope='QA serialization of unchanged analyzer outputs,not a source report writer;NaN represented as null',expected_assets=list(assets),expected_utc_grid=[x.isoformat()for x in times],incomplete=dict(evidence=e,**report),complete=dict(evidence=completed['evidence'],**fullreport))
            (HERE/'report-snapshots.json').write_text(json.dumps(retained,indent=2,allow_nan=False)+'\n');(HERE/'prices.csv').write_bytes(payload);(HERE/'prices-complete.csv').write_bytes(complete_payload)
            ck('input CSV unchanged by commands and source calls',path.read_bytes(),payload)
            result['prices'].iloc[0,0]=1;ck('returned output mutation does not change retained input',path.read_bytes(),payload)
            ck('independent rerun restores original observation',am.analyze(path,assets,times)['prices'].iloc[0,0],100.)
            source716=BOOK/'chapter-07/7.16-multi-asset-datasets.md';previous_blocks=re.findall(r'^```python\n(.*?)^```',source716.read_text(),re.M|re.S)
            oldpanel=next(c for c in previous_blocks if 'def panel('in c).split('\n\ndef fixture():')[0].rstrip()
            ck('local helper matches Section7.16 pre-fixture source',blocks[0].rstrip(),oldpanel)
        finally:
            if previous is None:sys.modules.pop('panel',None)
            else:sys.modules['panel']=previous
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),listing_sha256={n:sha(c.encode())for n,c in files.items()},python_fences=[dict(index=i,sha256=sha(c.encode()))for i,c in enumerate(blocks)],fixture_sha256=sha(payload),workflows=1,derived_step_units=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,report_snapshots_sha256=sha((HERE/'report-snapshots.json').read_bytes()),scope='Prepared Linux runtime;project step/checklist review only;8 local extension prompts remain pending;no independent acceptance')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands','listing_sha256','python_fences')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
