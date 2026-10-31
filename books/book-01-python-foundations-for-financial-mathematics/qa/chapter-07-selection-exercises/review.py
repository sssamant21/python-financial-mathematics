"""Scoped Section 7.4 local exercise review, unchanged source."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from known_condition import select_known
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
    source=BOOK/'chapter-07/7.04-indexing-and-selection.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==4;program,test=blocks[2:4]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-selection-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_74';lab.mkdir()
        for name,code in [('selection.py',program),('test_selection.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_74/selection.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_74','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_74'],parent,expected='')
        ck('ALL','source listings unchanged',{n:sha((lab/n).read_bytes())for n in ('selection.py','test_selection.py')},{'selection.py':sha(program.encode()),'test_selection.py':sha(test.encode())})
        m=types.ModuleType('exact_selection');exec(compile(program,str(source),'exec'),m.__dict__);table=m.fixture();before=table.copy(deep=True)
        subset=m.select_assets(table,('BETA','CASH'),('market_value',))
        ck('E1','requested ordered one-column table',(isinstance(subset,pd.DataFrame),subset.shape,subset.index.tolist(),subset.columns.tolist(),subset['market_value'].tolist()),(True,(2,1),['BETA','CASH'],['market_value'],[300.,100.]))
        variants=[table.loc['BETA'],table.loc[['BETA']],table.iloc[1],table.iloc[[1]]]
        ck('E2','label and position result ranks',[(type(x).__name__,x.shape)for x in variants],[('Series',(3,)),('DataFrame',(1,3)),('Series',(3,)),('DataFrame',(1,3))])
        ck('E2','equivalent label/position values on supplied order',(variants[0].equals(variants[2]),variants[1].equals(variants[3])),(True,True))
        ck('E3','inclusive label slice versus exclusive positional stop',(table.loc['ALPHA':'BETA'].index.tolist(),table.iloc[0:1].index.tolist()),(['ALPHA','BETA'],['ALPHA']))
        mask=(table['market_value']>=300)&(table['quantity']>0);array=mask.to_numpy();reordered=table.loc[['CASH','ALPHA','BETA']]
        ck('E4','unmoved positional mask changes selected identities',(table.iloc[array].index.tolist(),reordered.iloc[array].index.tolist()),(['ALPHA','BETA'],['CASH','ALPHA']))
        ck('E4','label mask retains asset meaning after target reorder',reordered.loc[mask].index.tolist(),['ALPHA','BETA'])
        ck('E4','explicitly realigned array restores intended result',reordered.iloc[mask.reindex(reordered.index).to_numpy()].index.tolist(),['ALPHA','BETA'])
        unknown=pd.Series([True,pd.NA,False],index=table.index,dtype='boolean')
        ck('E5','unguarded pandas omits unknown condition',(unknown.isna().tolist(),table.loc[unknown].index.tolist()),([False,True,False],['ALPHA']))
        reject('E5','supplemental explicit unknown rejection',lambda:select_known(table,unknown))
        known=pd.Series([True,False,False],index=table.index,dtype='boolean')
        ck('E5','same guard allows fully known condition',select_known(table,known).index.tolist(),['ALPHA'])
        # pandas absent-list policy is KeyError rather than helper ValueError.
        try:table.loc[['ABSENT']];actual='no exception';trace=''
        except Exception as error:actual=type(error).__name__;trace=traceback.format_exc()
        ck('E6','loc required absent label',actual,'KeyError');checks[-1]['expected_exception_trace']=trace
        absent=table.reindex(['ABSENT']);ck('E6','reindex constructs unknown row',(absent.index.tolist(),absent.shape,absent.isna().all().all()),(['ABSENT'],(1,3),True))
        reject('E6','checked selector rejects absent requested asset',lambda:m.select_assets(table,('ABSENT',),('price',)))
        scenario=table.copy(deep=True);scenario.loc['BETA','price']=90.
        ck('E7','repricing alone leaves stored BETA value stale',scenario.loc['BETA','market_value'],300.)
        scenario.loc[:,'market_value']=scenario['quantity']*scenario['price']
        ck('E7','independent rational BETA repricing',(scenario.loc['BETA','market_value'],scenario['market_value'].sum(skipna=False)),(float(F(3)*90),float(F(6)*100+F(3)*90+100)))
        ck('E7','scenario update preserves source',table.equals(before),True)
        stale=table.copy();stale.loc['BETA','price']=90.
        selected=m.select_assets(stale,('BETA',),('price','market_value'));ck('E8','selector intentionally does not reconcile financial values',selected.iloc[0].tolist(),[90.,300.])
        unobserved=table.copy();unobserved.loc['BETA','price']=np.nan
        ck('E8','selector intentionally permits numeric missingness',pd.isna(m.select_assets(unobserved,('BETA',),('price',)).iloc[0,0]),True)
        subset.loc['BETA','market_value']=0.;ck('ALL','selected output mutation leaves source intact',table.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
        (lab/'known_condition.py').write_bytes((HERE/'known_condition.py').read_bytes())
        caller="import pandas as pd\nfrom selection import fixture\nfrom known_condition import select_known\nt=fixture();mask=pd.Series([True,pd.NA,False],index=t.index,dtype='boolean')\ntry:select_known(t,mask)\nexcept ValueError as exc:print(str(exc))\nmask=pd.Series([True,False,False],index=t.index,dtype='boolean')\nprint(', '.join(select_known(t,mask).index))\n";(lab/'guard_demo.py').write_text(caller)
        command('E5','supplemental unknown-condition caller',['pandas_lab_74/guard_demo.py'],parent,expected='unknown Boolean condition: selection withheld\nALPHA\n')
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=2,test_fence=3,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),supplement_sha256=sha((HERE/'known_condition.py').read_bytes()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Unchanged selection source and explicit pandas mechanics;E5 supplemental known-condition guard;E8 source-boundary probes plus conceptual currency/context limits')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
