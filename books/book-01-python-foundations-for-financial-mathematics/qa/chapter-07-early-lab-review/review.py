"""Formal scoped workflow review of Sections 7.1–7.4, unchanged source."""
import contextlib,hashlib,io,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
CONFIG=[(1,'7.01-why-pandas.md','alignment.py','test_alignment.py','contributions'),
        (2,'7.02-series.md','series_lab.py','test_series_lab.py','holding_values'),
        (3,'7.03-dataframe.md','holdings.py','test_holdings.py','holdings_table'),
        (4,'7.04-indexing-and-selection.md','selection.py','test_selection.py','select_assets')]
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
    with tempfile.TemporaryDirectory(prefix='chapter07-early-') as tmp:
        parent=Path(tmp)
        command('ALL','preinstalled environment probe',['-c',"import json,platform,pandas as pd,numpy as np; print(json.dumps(dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,copy_on_write=pd.options.mode.copy_on_write,chained_assignment=pd.options.mode.chained_assignment)))"],parent,environment=True)
        for section,filename,application,test,entry in CONFIG:
            source=BOOK/'chapter-07'/filename;text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
            program_ids=[i for i,code in enumerate(blocks) if 'def '+entry+'(' in code];test_ids=[i for i,code in enumerate(blocks) if 'import unittest' in code]
            assert len(program_ids)==len(test_ids)==1;pi,ti=program_ids[0],test_ids[0];assert ti==pi+1
            labname='pandas_lab_7'+str(section);lab=parent/labname;lab.mkdir();files={application:blocks[pi],test:blocks[ti]}
            for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
            expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S);assert len(expected)==1
            command(str(section),'original demonstration',[labname+'/'+application],parent,expected=expected[0])
            command(str(section),'original unittest discovery',['-m','unittest','discover','-s',labname,'-v'],parent,count=8)
            command(str(section),'original compileall',['-m','compileall','-q',labname],parent,expected='')
            command(str(section),'quiet import',['-c','import '+application[:-3]],lab,expected='')
            ck(str(section),'two reconstructed listings unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
            module=types.ModuleType('exact_lab_7'+str(section));exec(compile(blocks[pi],str(source),'exec'),module.__dict__);modules[section]=module
            namespace={'__name__':'prose_snippets_7'+str(section)}
            if section==4:namespace['t']=module.fixture()  # Documented t precondition.
            captured=io.StringIO()
            with contextlib.redirect_stdout(captured):
                for index in range(pi):exec(compile(blocks[index],str(source)+':fence'+str(index),'exec'),namespace)
            snippets[section]=namespace
            sources.append(dict(section='7.'+str(section),source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=pi,test_fence=ti,program_file=application,test_file=test,listing_sha256={n:sha(c.encode()) for n,c in files.items()},prose_fences=list(range(pi)),prose_sha256=[sha(c.encode()) for c in blocks[:pi]],prose_stdout=captured.getvalue(),prose_prelude='t=exact original fixture()' if section==4 else 'none; original snippet order supplies dependencies'))
    m=modules[1];w=pd.Series([.6,.3,.1],index=['ALPHA','BETA','CASH']);r=pd.Series([0.,.1,-.05],index=['CASH','ALPHA','BETA']);wc=w.copy(deep=True);rc=r.copy(deep=True)
    frame,total=m.contributions(w,r);oracle=[F(3,50),F(-3,200),F(0)]
    ck('1','independent rational known contributions',bool(np.allclose(frame['contribution'],list(map(float,oracle)),rtol=0,atol=1e-12)),True)
    ck('1','independent rational portfolio return',abs(total-float(sum(oracle)))<=1e-12,True)
    ck('1','output follows opening weight identity order',frame.index.tolist(),['ALPHA','BETA','CASH'])
    ck('1','permutation preserves result',m.contributions(w,r.iloc[::-1])[1],total)
    reject('1','missing asset fails before partial aggregation',lambda:m.contributions(w,r.drop('BETA')))
    reject('1','nullable extension dtype excluded by narrow API',lambda:m.contributions(w,pd.Series([0,0,0],index=w.index,dtype='Int64')))
    frame.iloc[0,0]=99;ck('1','frame edit preserves both caller Series',(w.equals(wc),r.equals(rc)),(True,True))
    ck('1','exact prose positional error',abs(snippets[1]['wrong']-float(F(1,40)))<=1e-12,True)
    ck('1','exact prose gap remains missing',bool(pd.isna(snippets[1]['product'].loc['B'])),True)
    m=modules[2];a=np.array([600.,300.,100.]);s=m.holding_values(('ALPHA','BETA','CASH'),a)
    ck('2','Series metadata',(s.name,s.index.name,str(s.dtype),s.shape),('opening_value','asset','float64',(3,)))
    ck('2','value identity and positional access',(s.loc['BETA'],s.iloc[1]),(300.,300.))
    ck('2','zero-valued constructor remains valid',m.holding_values(('ZERO',),[0]).tolist(),[0.])
    a[0]=0;ck('2','constructor owns numeric copy',s.loc['ALPHA'],600.)
    absent=s.reindex(['CASH','DELTA']);ck('2','size/count and strict/default sums',(absent.size,absent.count(),absent.sum(),pd.isna(absent.sum(skipna=False))),(2,1,100.,True))
    exported=s.to_numpy(copy=True);exported[0]=1;ck('2','independent export edit',s.loc['ALPHA'],600.)
    reject('2','negative opening value rejected',lambda:m.holding_values(('A','B'),[1,-1]))
    ck('2','prose mapping selects by key and exposes absent label',(snippets[2]['requested'].loc['BETA'],pd.isna(snippets[2]['requested'].loc['DELTA'])),(300.,True))
    m=modules[3];source=m.fixture();before=source.copy(deep=True);table,total=m.holdings_table(source)
    ck('3','independent holdings values and total',(table['market_value'].tolist(),total),([600.,300.,100.],float(F(6)*100+F(3)*100+F(1)*100)))
    ck('3','derived schema and dtypes',(table.columns.tolist(),table.index.name,[str(x) for x in table.dtypes]),(['quantity','price','market_value'],'asset',['float64']*3))
    alternative=source.copy();alternative['price']=[101.5,80.25,1.];_,alt_total=m.holdings_table(alternative);ck('3','independent exact fractional price fixture',alt_total,float(F(6)*F('101.5')+F(3)*F('80.25')+1))
    ck('3','all-zero table allowed',m.holdings_table(source*0)[1],0.)
    reject('3','derived field cannot be supplied as source',lambda:m.holdings_table(source.assign(market_value=0.)))
    table.loc['ALPHA','price']=110.;ck('3','derived column is stored, not reactive',table.loc['ALPHA','market_value'],600.)
    ck('3','report edit leaves source unchanged',source.equals(before),True)
    ck('3','exact prose Series assignment follows labels',snippets[3]['example']['check'].tolist(),[30.,20.,10.])
    m=modules[4];table=m.fixture();before=table.copy(deep=True);subset=m.select_assets(table,('CASH','ALPHA'),('price','market_value'))
    ck('4','requested axes, values and table rank',(subset.index.tolist(),subset.columns.tolist(),subset.shape,subset.values.tolist()),(['CASH','ALPHA'],['price','market_value'],(2,2),[[100.,100.],[100.,600.]]))
    ck('4','singleton remains a table',m.select_assets(table,('ALPHA',),('price',)).shape,(1,1))
    subset.iloc[0,0]=0;ck('4','numeric subset copy preserves source',table.equals(before),True)
    reject('4','absent requested asset rejected',lambda:m.select_assets(table,('UNKNOWN',),('price',)))
    invalid=table.copy();invalid.loc['ALPHA','price']=np.nan
    ck('4','selection alone intentionally permits NaN',bool(pd.isna(m.select_assets(invalid,('ALPHA',),('price',)).iloc[0,0])),True)
    stale=table.copy();stale.loc['ALPHA','price']=110.;ck('4','selector does not reconcile stale derived values',m.select_assets(stale,('ALPHA',),('price','market_value')).iloc[0].tolist(),[110.,600.])
    ck('4','exact prose one-step update recalculates',(snippets[4]['scenario'].loc['ALPHA','market_value'],float(snippets[4]['scenario']['market_value'].sum())),(660.,1060.))
    ck('4','prose copy leaves original fixture unchanged',snippets[4]['t'].equals(before),True)
    ck('ALL','independent known currency-value sum',sum([F(600),F(300),F(100)]),F(1000))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,workflows=4,derived_step_units=32,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),existing_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),scope='preinstalled Linux runtime; setup PARTIAL; no fresh install or Windows/macOS/notebook acceptance',sources=sources,commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks')}));return bool(output['failed'] or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
