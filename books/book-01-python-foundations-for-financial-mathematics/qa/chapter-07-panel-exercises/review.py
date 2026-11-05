"""Scoped Section 7.16 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.16-panel-data-layouts.md'
    source,=source.parent.glob('7.16-*.md')
    blocks=re.findall(r'^```python\n(.*?)^```',source.read_text(),re.M|re.S)
    assert len(blocks)==5
    program,test=blocks[3:5]
    expected="""asset ALPHA BETA
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
"""
    def close(section,label,actual,expected):
        ck(section,label,bool(np.allclose(actual,np.asarray(expected,dtype=float),rtol=0,atol=1e-12)),True)
        checks[-1].update(values=repr(actual),reference=repr(expected),absolute_tolerance=1e-12)
    with tempfile.TemporaryDirectory(prefix='chapter07-panel-exercises-') as tmp:
        parent=Path(tmp); lab=parent/'pandas_lab_716'; lab.mkdir()
        for name,code in [('panel.py',program),('test_panel.py',test)]:
            (lab/name).write_bytes(code.encode())
        command('ALL','original demonstration',['pandas_lab_716/panel.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_716','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_716'],parent,expected='')
    m=types.ModuleType('exact_panel')
    exec(compile(program,str(source),'exec'),m.__dict__)
    raw,assets,times=m.fixture(); before=raw.copy(deep=True)
    wide,r,complete=m.panel(raw,assets,times)
    full=pd.concat([raw,pd.DataFrame({'time':[times[1]],'asset':['BETA'],'price':[210.]})],ignore_index=True)
    _,fr,fc=m.panel(full,assets,times)
    ck('E1','complete intervals',fc.tolist(),[False,True,True])
    close('E1','ALPHA rational returns',fr.ALPHA.iloc[1:],[F(110,100)-1,F(99,110)-1])
    close('E1','BETA rational returns',fr.BETA.iloc[1:],[F(210,200)-1,F(220,210)-1])
    aw,ar,ac=m.panel(raw.loc[raw.asset!='BETA'],assets,times)
    ck('E2','expected BETA retained',(aw.columns.tolist(),aw.BETA.isna().all(),ar.BETA.isna().all(),ac.any()),(['ALPHA','BETA'],True,True,False))
    tw,tr,tc=m.panel(raw.loc[raw.time!=times[1]],assets,times)
    ck('E3','all-missing middle row and no bridged intervals',(tw.index.equals(times),tw.iloc[1].isna().all(),tr.isna().all().all(),tc.any()),(True,True,True,False))
    duplicated=pd.concat([raw,raw.iloc[:1].assign(price=102.)],ignore_index=True)
    reject('E4','duplicate conflicts rejected',lambda:m.panel(duplicated,assets,times))
    rw,rr,rc=m.panel(raw,assets[::-1],times)
    ck('E5','expected columns move together',rw.columns.tolist(),['BETA','ALPHA'])
    ck('E5','labeled prices and returns preserved',(rw.reindex(columns=list(assets)).equals(wide),rr.reindex(columns=list(assets)).equals(r),rc.equals(complete)),(True,True,True))
    ck('E6','BETA daily intervals remain unknown',r.BETA.isna().tolist(),[True,True,True])
    close('E6','supplemental BETA two-day endpoint',wide.BETA.iloc[-1]/wide.BETA.iloc[0]-1,F(220,200)-1)
    close('E7','supplemental common two-day endpoint',wide.iloc[-1]/wide.iloc[0]-1,[F(99,100)-1,F(220,200)-1])
    ck('E7','endpoint horizon days',(wide.index[-1]-wide.index[0]).days,2)
    ck('ALL','input unchanged',raw.equals(before),True)
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=3,test_fence=4,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Exact panel workflow with rational oracles; endpoint ratios are supplemental, and export/portfolio risk remains design')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
