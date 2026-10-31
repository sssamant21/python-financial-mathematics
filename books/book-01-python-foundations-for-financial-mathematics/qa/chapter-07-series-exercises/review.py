"""Scoped Section 7.2 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.02-series.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==7;program,test=blocks[5:7]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-series-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_72';lab.mkdir()
        for name,code in [('series_lab.py',program),('test_series_lab.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_72/series_lab.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_72','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_72'],parent,expected='')
        ck('ALL','source listings unchanged',{n:sha((lab/n).read_bytes())for n in ('series_lab.py','test_series_lab.py')},{'series_lab.py':sha(program.encode()),'test_series_lab.py':sha(test.encode())})
        m=types.ModuleType('exact_series');exec(compile(program,str(source),'exec'),m.__dict__)
        assets=('ALPHA','BETA','CASH');values=[600,300,100];series=m.holding_values(assets,values);before=series.copy(deep=True)
        mapped=pd.Series({'ALPHA':600.,'BETA':300.,'CASH':100.},name='opening_value',dtype='float64')
        ck('E1','dictionary fixture retains key/value order',(mapped.index.tolist(),mapped.tolist()),(list(assets),list(map(float,values))))
        ck('E1','dictionary dtype and Series name match',(str(mapped.dtype),mapped.name),(str(series.dtype),series.name))
        ck('E1','mapping alone does not infer index axis name',(mapped.index.name,series.index.name),(None,'asset'))
        mapped=mapped.rename_axis('asset');ck('E1','explicit axis name gives identical fixture',mapped.equals(series),True)
        ck('E1','independent exact fixture total',series.sum(skipna=False),float(F(600)+300+100))
        reordered=series.reindex(['CASH','ALPHA','BETA'])
        ck('E2','positional answer changes after reorder',(series.iloc[0],reordered.iloc[0]),(600.,100.))
        ck('E2','label answer retains asset meaning',(series.loc['ALPHA'],reordered.loc['ALPHA']),(600.,600.))
        selected=series.loc[['CASH','ALPHA']]
        ck('E3','list label selector preserves Series rank/order',(isinstance(selected,pd.Series),selected.ndim,selected.shape,selected.index.tolist(),selected.tolist()),(True,1,(2,),['CASH','ALPHA'],[100.,600.]))
        ck('E3','selected field and axis names',(selected.name,selected.index.name),('opening_value','asset'))
        ck('E4','inclusive label slice versus exclusive positional stop',(series.loc['ALPHA':'BETA'].index.tolist(),series.iloc[0:1].index.tolist()),(['ALPHA','BETA'],['ALPHA']))
        ck('E4','slice values',(series.loc['ALPHA':'BETA'].tolist(),series.iloc[0:1].tolist()),([600.,300.],[600.]))
        missing=series.reindex(['ALPHA','DELTA'])
        ck('E5','size versus observed count',(missing.size,int(missing.count())),(2,1))
        ck('E5','missing mask keeps expected labels',(missing.isna().index.tolist(),missing.isna().tolist()),(['ALPHA','DELTA'],[False,True]))
        ck('E5','default sum is partial observed value',missing.sum(),600.)
        ck('E5','strict sum remains unknown',pd.isna(missing.sum(skipna=False)),True)
        reject('E6','duplicate asset labels reject',lambda:m.holding_values(('ALPHA','ALPHA'),[600,300]))
        reject('E6','negative opening value rejects',lambda:m.holding_values(('ALPHA','BETA'),[600,-300]))
        reject('E6','numeric strings require upstream parsing',lambda:m.holding_values(assets,['600','300','100']))
        owned=series.copy(deep=True);owned.loc['ALPHA']=650.
        ck('E7','explicit copied update isolated',(owned.loc['ALPHA'],series.loc['ALPHA'],series.equals(before)),(650.,600.,True))
        ck('E7','copy retains numeric field/index metadata',(str(owned.dtype),owned.name,owned.index.name),('float64','opening_value','asset'))
        ck('ALL','selections/reindex leave source intact',series.equals(before),True)
        ck('ALL','prepared runtime versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=5,test_fence=6,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='E1-7 original source calls and explicitly supplemental pandas mechanics;E8 conceptual units/valuation metadata,not external integration')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
