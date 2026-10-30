"""Formal scoped workflow review of Sections 7.13–7.16, unchanged source."""
import contextlib,hashlib,io,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
CONFIG=[(13,'7.13-resampling-time-series.md','resampling.py','test_resampling.py','bars'),
        (14,'7.14-rolling-and-expanding-calculations.md','windows.py','test_windows.py','summaries'),
        (15,'7.15-price-to-return-transformation.md','returns.py','test_returns.py','transform'),
        (16,'7.16-multi-asset-datasets.md','panel.py','test_panel.py','panel')]
DEMO={13:"""open high low close volume event_count has_observations
interval_end
2026-01-30 14:30:00+00:00 100.0 102.0 100.0 102.0 30.0 2 True
2026-01-30 15:00:00+00:00 101.0 101.0 101.0 101.0 5.0 1 True
2026-01-30 15:30:00+00:00 NaN NaN NaN NaN NaN 0 False
2026-01-30 16:00:00+00:00 103.0 103.0 103.0 103.0 7.0 1 True
Events accounted for: 4
""",14:"""price rolling_mean rolling_std expanding_mean prior_mean
2026-01-30 14:00:00+00:00 100.00 NaN NaN 100.00 NaN
2026-01-30 14:10:00+00:00 102.00 NaN NaN 101.00 NaN
2026-01-30 14:40:00+00:00 104.00 102.00 2.00 102.00 NaN
2026-01-30 15:00:00+00:00 106.00 104.00 2.00 103.00 102.00
2026-01-30 15:10:00+00:00 108.00 106.00 2.00 104.00 104.00
""",15:"""price simple_return cumulative_price_return
2026-01-30 16:00:00+00:00 100.0000 NaN 0.0000
2026-02-02 16:00:00+00:00 110.0000 0.1000 0.1000
2026-02-03 16:00:00+00:00 99.0000 -0.1000 -0.0100
Endpoint price return: -1.00%
Elapsed intervals: 3 days 00:00:00, 1 days 00:00:00
""",16:"""asset ALPHA BETA
time
2026-01-30 16:00:00+00:00 100.0 200.0
2026-01-31 16:00:00+00:00 110.0 NaN
2026-02-01 16:00:00+00:00 99.0 220.0
asset ALPHA BETA
time
2026-01-30 16:00:00+00:00 NaN NaN
2026-01-31 16:00:00+00:00 0.1000 NaN
2026-02-01 16:00:00+00:00 -0.1000 NaN
Complete aligned intervals: 0
"""}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
    checks=[];commands=[];sources=[];modules={};snippets={}
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
    with tempfile.TemporaryDirectory(prefix='chapter07-bars-returns-panel-') as tmp:
        parent=Path(tmp)
        command('ALL','preinstalled environment probe',['-c',"import json,platform,pandas as pd,numpy as np; print(json.dumps(dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,copy_on_write=pd.options.mode.copy_on_write,chained_assignment=pd.options.mode.chained_assignment)))"],parent,environment=True)
        for section,filename,application,test,entry in CONFIG:
            source=BOOK/'chapter-07'/filename;text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
            program_ids=[i for i,code in enumerate(blocks) if 'def '+entry+'(' in code];test_ids=[i for i,code in enumerate(blocks) if 'import unittest' in code]
            assert len(program_ids)==len(test_ids)==1;pi,ti=program_ids[0],test_ids[0];assert ti==pi+1
            labname='pandas_lab_7'+str(section);lab=parent/labname;lab.mkdir();files={application:blocks[pi],test:blocks[ti]}
            for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
            # Full console expectations transcribed from published tables/formulas;
            # whitespace normalized, timestamps/row order/NaNs retained.
            expected=[DEMO[section]]
            command(str(section),'original demonstration',[labname+'/'+application],parent,expected=expected[0])
            command(str(section),'original unittest discovery',['-m','unittest','discover','-s',labname,'-v'],parent,count=8)
            command(str(section),'original compileall',['-m','compileall','-q',labname],parent,expected='')
            command(str(section),'quiet import',['-c','import '+application[:-3]],lab,expected='')
            ck(str(section),'two reconstructed listings unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
            module=types.ModuleType('exact_lab_7'+str(section));exec(compile(blocks[pi],str(source),'exec'),module.__dict__);modules[section]=module
            namespace={'__name__':'prose_snippets_7'+str(section),'pd':pd,'np':np}
            if section==13:
                namespace.update(table=module.fixture(),result=pd.DataFrame())
                prelude='pd/np; table from original fixture; empty result table acquires volume resampler index'
            elif section==14:
                prices=module.fixture();namespace.update(prices=prices,rolling_mean=module.summaries(prices)['rolling_mean'])
                prelude='pd/np; prices from original fixture; rolling_mean from exact summaries(prices) because prose names its mean result mean'
            elif section==15:
                namespace['prices']=module.fixture();prelude='pd/np and prices from original fixture'
            else:
                records,assets,times=module.fixture();namespace.update(records=records,expected_assets=assets,expected_times=times)
                prelude='pd/np; records,expected_assets,expected_times from exact fixture; original pivot/reindex precede returns'
            captured=io.StringIO()
            with contextlib.redirect_stdout(captured):
                for index in range(pi):exec(compile(blocks[index],str(source)+':fence'+str(index),'exec'),namespace)
            snippets[section]=namespace
            sources.append(dict(section='7.'+str(section),source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=pi,test_fence=ti,program_file=application,test_file=test,listing_sha256={n:sha(c.encode()) for n,c in files.items()},prose_fences=list(range(pi)),prose_sha256=[sha(c.encode()) for c in blocks[:pi]],prose_stdout=captured.getvalue(),prose_prelude=prelude))
    m=modules[13];raw=m.fixture();before=raw.copy(deep=True);start=pd.Timestamp('2026-01-30T14:00:00Z');end=start+pd.Timedelta(hours=2);report=m.bars(raw,start=start,end=end)
    ck('13','independent first OHLC and event-volume sum',report.iloc[0][['open','high','low','close','volume']].tolist(),[100.,102.,100.,102.,float(F(10)+20)] )
    ck('13','left-closed bin assignment and independent counts',report['event_count'].tolist(),[2,1,0,1])
    ck('13','report end labels',[x.isoformat() for x in report.index],['2026-01-30T14:30:00+00:00','2026-01-30T15:00:00+00:00','2026-01-30T15:30:00+00:00','2026-01-30T16:00:00+00:00'])
    ck('13','empty bin measures unknown',report.iloc[2][['open','high','low','close','volume']].isna().all(),True)
    ck('13','observed count and volume conservation',(int(report['event_count'].sum()),report['volume'].sum(min_count=1)),(4,float(F(10)+20+5+7)))
    zero=m.bars(raw.assign(volume=0.),start=start,end=end);ck('13','observed zero differs from empty unknown',(zero.iloc[0]['volume'],pd.isna(zero.iloc[2]['volume'])),(0.,True))
    edges=m.bars(raw.iloc[[2]],start=start,end=end);ck('13','explicit horizon preserves leading and trailing empty bins',edges['event_count'].tolist(),[0,1,0,0])
    extra=raw.iloc[[0]].copy();extra.index=pd.DatetimeIndex([end]);reject('13','event exactly at reporting end rejected',lambda:m.bars(pd.concat([raw,extra]),start=start,end=end))
    ck('13','exact prose empty-volume policy',pd.isna(snippets[13]['result']['volume'].iloc[2]),True)
    report.iloc[0,0]=0;ck('13','bar mutation leaves input intact',raw.equals(before),True)
    m=modules[14];prices=m.fixture();before=prices.copy(deep=True);report=m.summaries(prices)
    oracle=[float(sum(map(F,[100,102,104,106,108][:i]))/i)for i in range(1,6)]
    ck('14','independent expanding scalar means',report['expanding_mean'].tolist(),oracle)
    ck('14','independent trailing means and sample standard deviations',(report['rolling_mean'].iloc[2:].tolist(),report['rolling_std'].iloc[2:].tolist()),([102.,104.,106.],[float((F(4)+0+4)/2)**.5]*3))
    ck('14','warmup states differ by prior-row shift',(report['rolling_mean'].isna().tolist(),report['prior_mean'].isna().tolist()),([True,True,False,False,False],[True,True,True,False,False]))
    ck('14','time-window endpoint excludes 14:10 at14:40',snippets[14]['timed'].iloc[2],104.)
    ck('14','original prose rolling/expanding/prior agreement',(snippets[14]['mean'].equals(report['rolling_mean']),snippets[14]['std'].equals(report['rolling_std']),snippets[14]['historical_mean'].equals(report['expanding_mean']),snippets[14]['prior_mean'].equals(report['prior_mean'])),(True,True,True,True))
    changed=prices.copy();changed.iloc[-1]=1000;future=m.summaries(changed)
    ck('14','future perturbation preserves all earlier outputs',future.iloc[:-1].equals(report.iloc[:-1]),True)
    ck('14','changed current mean but unchanged prior mean',(future['rolling_mean'].iloc[-1]!=report['rolling_mean'].iloc[-1],future['prior_mean'].iloc[-1]),(True,104.))
    ck('14','one-row input has no mature rolling statistic',(m.summaries(prices.iloc[:1])['rolling_mean'].isna().all(),m.summaries(prices.iloc[:1])['expanding_mean'].iloc[0]),(True,100.))
    reject('14','unsorted prices rejected rather than silently reordered',lambda:m.summaries(prices.iloc[::-1]))
    report.iloc[0,0]=0;ck('14','statistics mutation preserves source',prices.equals(before),True)
    m=modules[15];prices=m.fixture();before=prices.copy(deep=True);report=m.transform(prices);expected=[F(110,100)-1,F(99,110)-1]
    ck('15','independent rational adjacent returns',bool(np.allclose(report['simple_return'].iloc[1:],list(map(float,expected)),rtol=0,atol=1e-12)),True)
    linked=(1+expected[0])*(1+expected[1])-1;ck('15','independent gross product and endpoint match',(linked,F(99,100)-1),(F(-1,100),F(-1,100)))
    ck('15','source endpoint return matches rational reference',abs(report['cumulative_price_return'].iloc[-1]-float(linked))<=1e-12,True)
    ck('15','first undefined interval versus cumulative baseline',(pd.isna(report['simple_return'].iloc[0]),pd.isna(report['interval_start'].iloc[0]),pd.isna(report['elapsed'].iloc[0]),report['cumulative_price_return'].iloc[0]),(True,True,True,0.))
    ck('15','three-day then one-day intervals',[x.total_seconds() for x in report['elapsed'].iloc[1:]],[3*86400.,86400.])
    ck('15','unchanged explanatory simple/gross/log/start fragments',(snippets[15]['simple'].equals(report['simple_return']),snippets[15]['gross'].equals(report['gross_return']),snippets[15]['log_return'].equals(report['log_return']),snippets[15]['interval_start'].equals(report['interval_start'])),(True,True,True,True))
    # Independent math.log ratio route rather than NumPy log-price differences.
    import math
    ck('15','logarithmic sum versus independent endpoint log',abs(report['log_return'].iloc[1:].sum()-math.log(99/100))<=1e-12,True)
    reject('15','missing source price rejected',lambda:m.transform(prices.mask(prices==110)))
    reject('15','zero price excluded from combined simple/gross/log API',lambda:m.transform(prices*0))
    report.iloc[0,0]=0;ck('15','return report mutation preserves source',prices.equals(before),True)
    m=modules[16];raw,assets,times=m.fixture();before=raw.copy(deep=True);wide,returns,complete=m.panel(raw,assets,times)
    ck('16','expected axes preserve structural absence',(wide.shape,wide.columns.tolist(),pd.isna(wide.loc[times[1],'BETA'])),((3,2),['ALPHA','BETA'],True))
    ck('16','ALPHA rational adjacent-grid returns',bool(np.allclose(returns['ALPHA'].iloc[1:],[float(F(1,10)),float(F(-1,10))],rtol=0,atol=1e-12)),True)
    ck('16','BETA gap blocks both adjacent intervals',(returns['BETA'].isna().all(),complete.tolist()),(True,[False,False,False]))
    completed=pd.concat([raw,pd.DataFrame({'time':[times[1]],'asset':['BETA'],'price':[210.]})]);w,r,c=m.panel(completed,assets,times)
    ck('16','filled supplied record yields two complete intervals',c.tolist(),[False,True,True])
    ck('16','independent BETA completed adjacent ratios',bool(np.allclose(r['BETA'].iloc[1:],[float(F(210,200)-1),float(F(220,210)-1)],rtol=0,atol=1e-12)),True)
    ck('16','wholly absent expected asset remains visible',m.panel(raw.loc[raw['asset']=='ALPHA'],assets,times)[0]['BETA'].isna().all(),True)
    ck('16','wholly absent time remains visible',m.panel(raw.loc[raw['time']!=times[1]],assets,times)[0].iloc[1].isna().all(),True)
    ck('16','BETA endpoint is different two-day question',F(220,200)-1,F(1,10))
    ck('16','all original panel prose fragments agree',(snippets[16]['wide'].equals(wide),snippets[16]['returns'].equals(returns),snippets[16]['complete_interval'].tolist()),(True,True,[False]*3))
    reject('16','identical duplicate source key still rejects',lambda:m.panel(pd.concat([raw,raw.iloc[:1]]),assets,times))
    wide.iloc[0,0]=0;ck('16','panel mutation preserves source',raw.equals(before),True)
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,workflows=4,derived_step_units=32,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),existing_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),scope='preinstalled Linux runtime; setup PARTIAL; no fresh install or Windows/macOS/notebook acceptance',sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks')}));return bool(output['failed'] or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
