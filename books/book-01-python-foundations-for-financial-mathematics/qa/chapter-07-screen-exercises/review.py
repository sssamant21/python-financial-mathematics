"""Scoped Section 7.10 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.10-sorting-filtering-and-querying.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==6;program,test=blocks[4:6]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-screen-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_710';lab.mkdir()
        for name,code in [('screen.py',program),('test_screen.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_710/screen.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_710','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_710'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('screen.py','test_screen.py')},{'screen.py':sha(program.encode()),'test_screen.py':sha(test.encode())})
        m=types.ModuleType('exact_screen');exec(compile(program,str(source),'exec'),m.__dict__);raw=m.fixture();before=raw.copy(deep=True)
        allrows,e=m.screen(raw,limit=10)
        ck('E1','all eligible equity records sorted deterministically',(allrows['asset'].tolist(),allrows['market_value'].tolist()),(['ALPHA','BETA','GAMMA'],[600.,600.,300.]))
        ck('E1','input/eligible/returned reconciliation',(e['input_rows'],e['eligible_rows'],e['returned_rows']),(5,3,3))
        boundary,eb=m.screen(raw,floor=600,limit=10);ck('E2','inclusive floor keeps both equal values',(boundary['asset'].tolist(),eb['eligible_rows']),(['ALPHA','BETA'],2))
        ck('E2','above-boundary next representable floor excludes equality',m.screen(raw,floor=np.nextafter(600.,np.inf),limit=10)[0].empty,True)
        a,_=m.screen(raw,limit=1);b,_=m.screen(raw.iloc[::-1],limit=1);ck('E3','limit-one tie break independent of source order',(a['asset'].tolist(),b['asset'].tolist()),(['ALPHA'],['ALPHA']))
        proper,ep=m.screen(raw,sector='bond',limit=1);early=raw.head(1).loc[lambda x:x['sector'].eq('bond')]
        ck('E4','eligibility before head preserves DELTA',(proper['asset'].tolist(),early['asset'].tolist()),(['DELTA'],[]))
        ck('E4','bond population evidence',(ep['input_rows'],ep['eligible_rows'],ep['returned_rows']),(5,1,1))
        extended=pd.concat([raw,pd.DataFrame({'asset':['ZETA'],'sector':['equity'],'market_value':[300.]})],ignore_index=True);ranked,et=m.screen(extended,limit=3)
        ck('E5','maximum-row policy resolves tied cutoff by asset',(ranked['asset'].tolist(),et['eligible_rows'],et['returned_rows']),(['ALPHA','BETA','GAMMA'],4,3))
        ck('E5','same maximum-row result after permutation',m.screen(extended.iloc[::-1],limit=3)[0]['asset'].tolist(),['ALPHA','BETA','GAMMA'])
        floor=300.;sectors=('equity','bond');masked=raw.loc[(raw['market_value']>=floor)&raw['sector'].isin(sectors)]
        queried=raw.query('market_value >= @floor and sector in @sectors',local_dict={'floor':floor,'sectors':sectors},engine='python')
        ck('E6','fixed two-sector query equals isin mask',queried.equals(masked),True)
        ck('E6','two-sector source-order population',queried['asset'].tolist(),['BETA','ALPHA','GAMMA','DELTA'])
        missing=raw.copy();missing.loc[4,'market_value']=np.nan;reject('E7','unselected DELTA missing value still rejects',lambda:m.screen(missing))
        empty,ee=m.screen(raw,sector='unknown');limited,el=m.screen(raw)
        ck('E8','existing evidence distinguishes no matches',(empty.empty,ee['input_rows'],ee['eligible_rows'],ee['returned_rows']),(True,5,0,0))
        ck('E8','existing counts identify truncation',(el['input_rows'],el['eligible_rows'],el['returned_rows'],el['eligible_rows']>el['returned_rows']),(5,3,2,True))
        ck('E8','existing criteria explicit',(el['floor'],el['sector'],el['limit']),(300.,'equity',2))
        ck('ALL','original source unchanged',raw.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=4,test_fence=5,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Original single-sector source;E6 supplemental authored two-sector expression;E8 proposed richer status/provenance evidence not implemented')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
