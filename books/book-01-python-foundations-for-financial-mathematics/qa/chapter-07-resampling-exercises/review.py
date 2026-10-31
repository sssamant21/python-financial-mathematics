"""Scoped Section 7.13 local exercise review, unchanged source."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
    checks=[];commands=[]
    def ck(section,label,a,x):checks.append(dict(section=section,label=label,actual=repr(a),expected=repr(x),status='PASS' if a==x else 'FAIL'))
    def reject(section,label,fn):
        try:fn();actual='no exception';detail=''
        except Exception as error:actual=type(error).__name__;detail=traceback.format_exc()
        ck(section,label,actual,'ValueError');checks[-1]['expected_exception_trace']=detail
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
    def command(section,label,args,cwd,expected=None,count=None,environment=False):
        r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
        counts=re.findall(r'Ran (\d+) tests? in',r.stderr);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
        if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',r.stderr,re.M))
        if expected is not None:
            normalize=lambda s:[' '.join(line.split()) for line in s.splitlines()]
            ok=ok and normalize(r.stdout)==normalize(expected) and r.stderr==''
        if environment:
            v=json.loads(r.stdout);ok=ok and (v['python'],v['pandas'],v['numpy'])==('3.12.14','2.2.3','2.3.5') and r.stderr==''
        commands.append(dict(section=section,label=label,args=args,cwd_role='lab directory' if label=='quiet import' else 'parent directory',returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=actual,status='PASS' if ok else 'FAIL'))
    source=BOOK/'chapter-07/7.13-resampling-time-series.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==4;program,test=blocks[2:4]
    expected='open high low close volume event_count has_observations\ninterval_end\n2026-01-30 14:30:00+00:00 100.0 102.0 100.0 102.0 30.0 2 True\n2026-01-30 15:00:00+00:00 101.0 101.0 101.0 101.0 5.0 1 True\n2026-01-30 15:30:00+00:00 NaN NaN NaN NaN NaN 0 False\n2026-01-30 16:00:00+00:00 103.0 103.0 103.0 103.0 7.0 1 True\nEvents accounted for: 4\n'
    with tempfile.TemporaryDirectory(prefix='chapter07-resampling-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_713';lab.mkdir()
        for name,code in [('resampling.py',program),('test_resampling.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_713/resampling.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_713','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_713'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('resampling.py','test_resampling.py')},{'resampling.py':sha(program.encode()),'test_resampling.py':sha(test.encode())})
        m=types.ModuleType('exact_resampling');exec(compile(program,str(source),'exec'),m.__dict__);raw=m.fixture();before=raw.copy(deep=True);start=pd.Timestamp('2026-01-30T14:00:00Z');end=pd.Timestamp('2026-01-30T16:00:00Z')
        def bars(data):return m.bars(data,start=start,end=end)
        result=bars(raw)
        ck('E1','independent first-bin OHLC and volume',result.iloc[0][['open','high','low','close','volume']].tolist(),[100.,102.,100.,102.,float(F(10)+20)])
        ck('E1','four supplied events and volume conservation',(int(result['event_count'].sum()),result['volume'].sum(min_count=1)),(4,float(F(10)+20+5+7)))
        ck('E2','boundary event enters next bin',result.loc[pd.Timestamp('2026-01-30T15:00:00Z'),['open','close','event_count']].tolist(),[101.,101.,1])
        ck('E2','all bin memberships',result['event_count'].tolist(),[2,1,0,1])
        reduced=bars(raw.iloc[2:]);ck('E3','explicit horizon retains leading empty bin',(reduced.shape,reduced['event_count'].tolist()),((4,7),[0,1,0,1]))
        ck('E3','leading empty financial fields remain unknown',reduced.iloc[0][['open','high','low','close','volume']].isna().all(),True)
        zeros=bars(raw.assign(volume=0.));ck('E4','observed zero volume bins remain zero',zeros.loc[zeros['has_observations'],'volume'].tolist(),[0.,0.,0.])
        ck('E4','empty bin has unknown volume and no observations',(pd.isna(zeros.iloc[2]['volume']),zeros.iloc[2]['has_observations'],zeros.iloc[2]['event_count']),(True,False,0))
        terminal=raw.iloc[[0]].copy();terminal.index=pd.DatetimeIndex([end]);reject('E5','exact reporting-end event rejected',lambda:bars(pd.concat([raw,terminal])))
        ck('E5','last permitted supplied event still assigned',result.iloc[-1]['close'],103.)
        grid=raw['price'].asfreq('30min');ck('E6','asfreq selects grid observation rather than last-bin-event close',(grid.iloc[0],result.iloc[0]['close']),(100.,102.))
        ck('E6','off-grid14:29 event is not an asfreq sample',pd.Timestamp('2026-01-30T14:29:00Z') in grid.index,False)
        reject('E7','original simplified instant key rejects multiple simultaneous events',lambda:bars(pd.concat([raw,raw.iloc[[0]]])))
        omitted=raw.drop(pd.Timestamp('2026-01-30T14:29:00Z'));partial=bars(omitted)
        ck('E8','missing whole event not discoverable from local conservation',(int(partial['event_count'].sum()),partial.iloc[0]['event_count'],partial.iloc[0]['close']),(3,1,100.))
        ck('E8','original empty interval has no supplied observations',(result.iloc[2]['event_count'],result.iloc[2]['has_observations']),(0,False))
        result.iloc[0,0]=0.;ck('ALL','source remains unchanged',raw.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=2,test_fence=3,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Original observed-event bars;independent OHLC/volume membership;E7 simultaneous-event key and E8 calendar/feed completeness controls remain designs')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
