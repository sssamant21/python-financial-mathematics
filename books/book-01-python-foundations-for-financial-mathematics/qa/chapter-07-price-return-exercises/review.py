"""Scoped Section 7.15 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.15-price-to-return-transformation.md'
    blocks=re.findall(r'^```python\n(.*?)^```',source.read_text(),re.M|re.S)
    assert len(blocks)==5
    program,test=blocks[3:5]
    expected="""price simple_return cumulative_price_return
2026-01-30 16:00:00+00:00 100.0000 NaN 0.0000
2026-02-02 16:00:00+00:00 110.0000 0.1000 0.1000
2026-02-03 16:00:00+00:00 99.0000 -0.1000 -0.0100
Endpoint price return: -1.00%
Elapsed intervals: 3 days 00:00:00, 1 days 00:00:00
"""
    def close(section,label,actual,expected):
        ck(section,label,bool(np.allclose(actual,np.asarray(expected,dtype=float),rtol=0,atol=1e-12)),True)
        checks[-1].update(values=repr(actual),reference=repr(expected),absolute_tolerance=1e-12)
    with tempfile.TemporaryDirectory(prefix='chapter07-return-exercises-') as tmp:
        parent=Path(tmp); lab=parent/'pandas_lab_715'; lab.mkdir()
        for name,code in [('returns.py',program),('test_returns.py',test)]:
            (lab/name).write_bytes(code.encode())
        command('ALL','original demonstration',['pandas_lab_715/returns.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_715','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_715'],parent,expected='')
    m=types.ModuleType('exact_returns')
    exec(compile(program,str(source),'exec'),m.__dict__)
    p=m.fixture(); before=p.copy(deep=True); r=m.transform(p)
    a,b,c=map(F,(100,110,99))
    close('E1','adjacent returns',r.simple_return.iloc[1:],[b/a-1,c/b-1])
    close('E1','linked return',r.cumulative_price_return.iloc[-1],(b/a)*(c/b)-1)
    ck('E2','first interval fields undefined',r.iloc[0][['interval_start','elapsed','simple_return','gross_return','log_return']].isna().tolist(),[True]*5)
    ck('E2','baseline defined',r.cumulative_price_return.iloc[0],0)
    ck('E2','right alignment and elapsed days',(r.index.equals(p.index),r.interval_start.iloc[1:].tolist(),r.elapsed.iloc[1:].dt.days.tolist()),(True,p.index[:2].tolist(),[3,1]))
    q=p.copy(); q.iloc[-1]=121
    z=m.transform(q)
    close('E3','adjacent returns',z.simple_return.iloc[1:],[b/a-1,F(121)/b-1])
    close('E3','independent endpoint',z.cumulative_price_return.iloc[-1],F(121)/a-1)
    close('E3','linked from source intervals',np.prod(1+z.simple_return.iloc[1:])-1,F(121)/a-1)
    q=p.copy(); q.iloc[1]=np.nan
    reject('E4','source rejects missing price',lambda:m.transform(q))
    ck('E4','supplemental no-fill has no defined return',q.pct_change(fill_method=None).isna().tolist(),[True]*3)
    filled=q.ffill().pct_change(fill_method=None)
    ck('E4','forward fill first row still undefined',pd.isna(filled.iloc[0]),True)
    close('E4','forward fill manufactures an intermediate zero',filled.iloc[1:],[F(0),c/a-1])
    dropped=m.transform(q.dropna())
    close('E4','dropped-row return',dropped.simple_return.iloc[1],c/a-1)
    ck('E4','dropped row changes interval',dropped.elapsed.iloc[1],pd.Timedelta(days=4))
    scaled=m.transform(p*10)
    for col in ('simple_return','gross_return','log_return','cumulative_price_return'):
        close('E5',col,scaled[col].iloc[1:],r[col].iloc[1:])
    ck('E5','source unchanged',p.equals(before),True)
    rates=list(map(F,('1','1.1','1.2')))
    close('E6','supplemental changing FX on flat local series',np.diff([float(100*x) for x in rates])/[100.,110.],[F(1,10),F(1,11)])
    q=p.copy(); q.iloc[-1]=0
    reject('E7','combined source rejects terminal zero',lambda:m.transform(q))
    q=p.copy(); q.iloc[:]=[100.,1e-6,1e-14]
    ck('range','rational cumulative gross below half-ulp at one',F(1,10**16)<F(1,2**54),False)
    # Both steps are about 1e-8 gross; the endpoint gross is about 1e-16.
    # Use a smaller last price to put the endpoint below half the gap above -1.
    q.iloc[-1]=1e-15
    ck('range','endpoint gross positive and below rounding threshold',0<F(1,10**17)<F(1,2**54),True)
    reject('range','source rejects cumulative return rounded to -100%',lambda:m.transform(q))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=3,test_fence=4,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Exact return transformation, rational oracles and separately identified supplemental illustrations; FX ingestion, simple-only API and source metadata design not implemented')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
