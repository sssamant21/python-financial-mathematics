"""Formal scoped workflow review of Sections 7.9–7.12, unchanged source."""
import contextlib,hashlib,io,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
CONFIG=[(9,'7.09-date-and-time-indexes.md','time_index.py','test_time_index.py','price_series'),
        (10,'7.10-sorting-filtering-and-querying.md','screen.py','test_screen.py','screen'),
        (11,'7.11-grouping-and-aggregation.md','grouping.py','test_grouping.py','summarize'),
        (12,'7.12-joining-and-merging-financial-data.md','merging.py','test_merging.py','reconcile')]
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
    with tempfile.TemporaryDirectory(prefix='chapter07-time-group-merge-') as tmp:
        parent=Path(tmp)
        command('ALL','preinstalled environment probe',['-c',"import json,platform,pandas as pd,numpy as np; print(json.dumps(dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,copy_on_write=pd.options.mode.copy_on_write,chained_assignment=pd.options.mode.chained_assignment)))"],parent,environment=True)
        for section,filename,application,test,entry in CONFIG:
            source=BOOK/'chapter-07'/filename;text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
            program_ids=[i for i,code in enumerate(blocks) if 'def '+entry+'(' in code];test_ids=[i for i,code in enumerate(blocks) if 'import unittest' in code]
            assert len(program_ids)==len(test_ids)==1;pi,ti=program_ids[0],test_ids[0];assert ti==pi+1
            labname='pandas_lab_7'+str(section);lab=parent/labname;lab.mkdir();files={application:blocks[pi],test:blocks[ti]}
            for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
            expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)
            if section==11:
                # Published full-report values are tabular, not a text fence.
                expected=['        asset_count  opening_value  price_pnl  portfolio_weight  portfolio_contribution  sector_return\nsector\ncash 1 100.0000 0.0000 0.1000 0.0000 0.0000\nequity 2 900.0000 45.0000 0.9000 0.0450 0.0500\nunused 1 0.0000 0.0000 0.0000 0.0000 NaN\nPortfolio price return: 4.50%\n']
            assert len(expected)==1
            command(str(section),'original demonstration',[labname+'/'+application],parent,expected=expected[0])
            command(str(section),'original unittest discovery',['-m','unittest','discover','-s',labname,'-v'],parent,count=8)
            command(str(section),'original compileall',['-m','compileall','-q',labname],parent,expected='')
            command(str(section),'quiet import',['-c','import '+application[:-3]],lab,expected='')
            ck(str(section),'two reconstructed listings unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
            module=types.ModuleType('exact_lab_7'+str(section));exec(compile(blocks[pi],str(source),'exec'),module.__dict__);modules[section]=module
            namespace={'__name__':'prose_snippets_7'+str(section),'pd':pd,'np':np}
            if section==9:
                raw=module.fixture();raw.loc[2,'timestamp']='2026-01-30T16:30:00+01:00'
                series=module.price_series(raw)
                namespace.update(series=series,start=series.index[1],end=series.index[2])
                prelude='pd/np imports; series from exact price_series on documented corrected fixture; start=15:00Z, end=15:30Z'
            elif section==10:
                table=module.fixture();floor=300.;sector='equity'
                # First prose fragment presupposes eligible before the later mask fragment defines it.
                eligible=table.loc[(table['market_value']>=floor)&table['sector'].eq(sector)]
                namespace.update(table=table,floor=floor,sector=sector,eligible=eligible)
                prelude='pd/np imports, exact fixture table, default floor/sector, eligible from explicitly stated mask'
            elif section==11:
                table=module.fixture();table['price_pnl']=table['opening_value']*table['asset_return']
                namespace['table']=table
                prelude='pd/np imports; exact fixture table with price_pnl explicitly calculated from documented V*r'
            else:
                holdings,quotes=module.fixture();namespace.update(holdings=holdings,quotes=quotes)
                prelude='pd/np imports; holdings and quotes from exact fixture()'
            captured=io.StringIO()
            with contextlib.redirect_stdout(captured):
                for index in range(pi):exec(compile(blocks[index],str(source)+':fence'+str(index),'exec'),namespace)
            snippets[section]=namespace
            sources.append(dict(section='7.'+str(section),source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=pi,test_fence=ti,program_file=application,test_file=test,listing_sha256={n:sha(c.encode()) for n,c in files.items()},prose_fences=list(range(pi)),prose_sha256=[sha(c.encode()) for c in blocks[:pi]],prose_stdout=captured.getvalue(),prose_prelude=prelude))
    m=modules[9];raw=m.fixture();reject('9','duplicate UTC instant despite distinct source tokens',lambda:m.price_series(raw))
    raw.loc[2,'timestamp']='2026-01-30T16:30:00+01:00';before=raw.copy(deep=True);series=m.price_series(raw)
    ck('9','independent UTC offset arithmetic and price attachment',[(x.isoformat(),v) for x,v in series.items()],[('2026-01-30T14:30:00+00:00',100.),('2026-01-30T15:00:00+00:00',101.),('2026-01-30T15:30:00+00:00',102.)])
    ck('9','explanatory inclusive versus half-open interval',(snippets[9]['inclusive'].tolist(),snippets[9]['window'].tolist()),([101.,102.],[101.]))
    ck('9','explicit winter localization',snippets[9]['utc'][0].isoformat(),'2026-01-30T14:30:00+00:00')
    ck('9','independent thirty minute elapsed time',(series.index[1]-series.index[0]).total_seconds(),30*60)
    for token in ['2026-01-30T10:00:00','2026-01-30T10:00:00.1Z','2026-01-30T10:00:00+24:00','2026-01-30T10:00:00+00:60','2026-02-30T10:00:00Z']:
        bad=raw.copy();bad.loc[0,'timestamp']=token;reject('9','contract rejects '+token,lambda:m.price_series(bad))
    ck('9','row reversal preserves timestamp-price pairs',m.price_series(raw.iloc[::-1]).equals(series),True)
    series.iloc[0]=0;ck('9','output mutation leaves raw source intact',raw.equals(before),True)
    m=modules[10];raw=m.fixture();before=raw.copy(deep=True);report,e=m.screen(raw)
    ck('10','independent sort keys and population counts',(report['asset'].tolist(),e['input_rows'],e['eligible_rows'],e['returned_rows']),(['ALPHA','BETA'],5,3,2))
    ck('10','floor boundary includes equality',m.screen(raw,floor=600,limit=10)[0]['asset'].tolist(),['ALPHA','BETA'])
    ck('10','no-match is empty report not invented value',(m.screen(raw,sector='missing')[0].shape,m.screen(raw,sector='missing')[1]['eligible_rows']),((0,3),0))
    ck('10','eligibility must precede limit',(m.screen(raw,sector='bond',limit=1)[0]['asset'].tolist(),raw.head(1).loc[lambda x:x['sector'].eq('bond'),'asset'].tolist()),(['DELTA'],[]))
    ck('10','tie-break independent of source order',m.screen(raw.iloc[::-1],limit=1)[0]['asset'].tolist(),['ALPHA'])
    ck('10','all four prose fragments preserve semantics',(snippets[10]['ranked']['asset'].tolist(),snippets[10]['eligible_query'].equals(snippets[10]['eligible']),snippets[10]['columns_only'].shape),(['ALPHA','BETA','GAMMA'],True,(5,1)))
    bad=raw.copy();bad.loc[4,'market_value']=np.nan;reject('10','unselected invalid row still rejects complete batch',lambda:m.screen(bad))
    duplicate_index=raw.copy();duplicate_index.index=[0]*5
    ck('10','source index is lineage not unique financial key',m.screen(duplicate_index)[0].index.tolist(),[0,0])
    report.iloc[0,2]=0;ck('10','screen result owns copy',raw.equals(before),True)
    m=modules[11];raw=m.fixture();before=raw.copy(deep=True);report,total=m.summarize(raw)
    pnl=F(600)*F(1,10)+F(300)*F(-1,20);portfolio=pnl/F(1000);sector=pnl/F(900)
    ck('11','independent rational portfolio return',abs(total-float(portfolio))<=1e-12,True)
    ck('11','equity totals and distinct denominators',(report.loc['equity','opening_value'],report.loc['equity','price_pnl'],round(report.loc['equity','sector_return'],12),round(report.loc['equity','portfolio_contribution'],12)),(900.,float(pnl),float(sector),float(portfolio)))
    ck('11','equal-weight mean is different from value-weighted return',float((F(1,10)+F(-1,20))/2),.025)
    ck('11','zero observed sector undefined return and zero contribution',(pd.isna(report.loc['unused','sector_return']),report.loc['unused','portfolio_contribution']),(True,0.))
    ck('11','count/value/contribution conservation',(int(report['asset_count'].sum()),report['opening_value'].sum(),abs(report['portfolio_contribution'].sum()-float(portfolio))<=1e-12),(4,1000.,True))
    ck('11','all prose group/transform results',(snippets[11]['report']['price_pnl'].to_dict(),snippets[11]['sector_values'].tolist(),int(snippets[11]['with_missing_key'].size().sum())),({'cash':0.,'equity':45.,'unused':0.},[900.,900.,100.,0.],3))
    ck('11','repeated transformed totals are not group totals',snippets[11]['sector_values'].sum(),1900.)
    bad=raw.copy();bad.loc[3,'asset_return']=np.nan;reject('11','zero-exposure missing return still blocks complete-input contract',lambda:m.summarize(bad))
    reject('11','all-zero portfolio has no return denominator',lambda:m.summarize(raw.assign(opening_value=0.)))
    report.loc['equity','price_pnl']=0;ck('11','group report edit preserves source',raw.equals(before),True)
    m=modules[12];h,q=m.fixture();hc=h.copy(deep=True);qc=q.copy(deep=True);audit,report,total=m.reconcile(h,q.iloc[::-1])
    ck('12','independent keyed valuation with unordered quotes',(report['asset'].tolist(),report['market_value'].tolist(),total),(['ALPHA','BETA','CASH'],[float(F(6)*100),float(F(3)*100),float(F(1)*100)],1000.))
    qalt=q.copy();qalt['price']=[101.5,80.25,0.];ck('12','exact fractional alternative scalar valuation',m.reconcile(h,qalt)[2],float(F(6)*F(203,2)+F(3)*F(321,4)))
    a,r,t=m.reconcile(h,q.iloc[:2]);ck('12','missing quote retains outer evidence but withholds value',(a.loc[a['_merge']=='left_only','asset'].tolist(),r,t),(['CASH'],None,None))
    extra=q.iloc[[0]].copy();extra['asset']='OTHER';a,r,t=m.reconcile(h,pd.concat([q,extra]));ck('12','extra quote also blocks strict exact-population valuation',(a.loc[a['_merge']=='right_only','asset'].tolist(),r,t),(['OTHER'],None,None))
    reject('12','duplicate composite quote key fails',lambda:m.reconcile(h,pd.concat([q,q.iloc[[0]]])))
    reject('12','null keys cannot become valid matches',lambda:m.reconcile(h,q.assign(asset=[None,'BETA','CASH'])))
    ck('12','all-zero valuation permitted without return denominator',m.reconcile(h.assign(quantity=0.),q)[2],0.)
    ck('12','exact explanatory merge observes complete population',snippets[12]['audit']['_merge'].tolist(),['both']*3)
    report.loc[0,'price']=0;ck('12','merged result edit preserves both sources',(h.equals(hc),q.equals(qc)),(True,True))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,workflows=4,derived_step_units=32,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),existing_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),scope='preinstalled Linux runtime; setup PARTIAL; no fresh install or Windows/macOS/notebook acceptance',sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks')}));return bool(output['failed'] or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
