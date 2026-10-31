"""Scoped Section 7.6 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.06-data-types-and-conversion.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==3;program,test=blocks[1:3]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-conversion-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_76';lab.mkdir()
        for name,code in [('conversion.py',program),('test_conversion.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_76/conversion.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_76','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_76'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('conversion.py','test_conversion.py')},{'conversion.py':sha(program.encode()),'test_conversion.py':sha(test.encode())})
        m=types.ModuleType('conversion');exec(compile(program,str(source),'exec'),m.__dict__)
        raw=m.fixture();before=raw.copy(deep=True);typed=m.convert_records(raw)
        extended=pd.concat([raw,pd.DataFrame({'asset':['00007'],'lot_count':['2'],'price':['12.50'],'reviewed':['false']},index=[10])]);extra=m.convert_records(extended)
        ck('E1','additional leading-zero identifier survives',(extra.loc[10,'asset'],isinstance(extra.loc[10,'asset'],str)),('00007',True))
        ck('E1','extended dtypes remain explicit',[str(x)for x in extra.dtypes],['string','Int64','float64','boolean'])
        ck('E1','price independent rational reference',extra.loc[10,'price'],float(F(25,2)))
        ck('E2','unknown count distinct from known zero',(pd.isna(typed.loc[1,'lot_count']),typed.loc[2,'lot_count']),(True,0))
        bad=raw.copy();bad.loc[0,'price']='';reject('E2','empty price rejected',lambda:m.convert_records(bad))
        nullable=pd.Series([1,pd.NA],dtype='Int64')
        ck('E3','nullable integer dtype and missing mask',(str(nullable.dtype),nullable.isna().tolist()),('Int64',[False,True]))
        try:pd.Series([1,np.nan],dtype='int64');actual='no exception';trace='';failed=False
        except ValueError as error:actual=type(error).__name__;trace=traceback.format_exc();failed=True
        ck('E3','ordinary int64 cannot retain that NaN',failed,True);checks[-1].update(actual_exception=actual,expected_exception_trace=trace)
        # Adapter imports original source by its documented sibling name.
        previous=sys.modules.get('conversion');sys.modules['conversion']=m
        try:
            adapter=types.ModuleType('qa_yn_adapter');exec(compile((HERE/'yn_adapter.py').read_text(),str(HERE/'yn_adapter.py'),'exec'),adapter.__dict__)
            yn=raw.copy();yn['reviewed']=['Y','N','Y'];yn_before=yn.copy(deep=True);out=adapter.convert_yn(yn)
            ck('E4','explicit Y/N mapping output',(out['reviewed'].tolist(),str(out['reviewed'].dtype)),([True,False,True],'boolean'))
            ck('E4','other typed source fields unchanged',out.drop(columns='reviewed').equals(typed.drop(columns='reviewed')),True)
            ck('E4','adapter preserves source tokens',yn.equals(yn_before),True)
            for token in ['y','n','yes','true','',None,False]:
                invalid=yn.copy();invalid.loc[0,'reviewed']=token;reject('E4','unknown Boolean token '+repr(token),lambda:adapter.convert_yn(invalid))
            invalid=yn.copy();invalid.loc[0,'price']='BAD';reject('E4','adapter does not bypass original price grammar',lambda:adapter.convert_yn(invalid))
        finally:
            if previous is None:sys.modules.pop('conversion',None)
            else:sys.modules['conversion']=previous
        auditraw=pd.Series(['10','BAD',None,'20']);parsed=pd.to_numeric(auditraw,errors='coerce');introduced=auditraw.notna()&parsed.isna()
        ck('E5','coercion audit introduced versus all missing',(introduced.tolist(),parsed.isna().tolist(),int(introduced.sum()),int(parsed.isna().sum())),([False,True,False,False],[False,True,True,False],1,2))
        ck('E5','observed parsed numeric values',parsed.dropna().tolist(),[10.,20.])
        cast=pd.Series([1.75]).astype('int64').astype('float64')
        ck('E6','roundtrip cast cannot recover fractional source',(cast.iloc[0],cast.iloc[0]==float(F(7,4))),(1.,False))
        ck('E6','exact lost fraction',float(F(7,4)-F(int(cast.iloc[0]))),.75)
        maximum=2**63-1;at_limit=raw.copy();at_limit.loc[0,'lot_count']=str(maximum);near=m.convert_records(at_limit)
        ck('E8','original exact integer count boundary',int(near.loc[0,'lot_count']),maximum)
        ck('E8','independent unbounded arithmetic exceeds storage range',int(near.loc[0,'lot_count'])+1>maximum,True)
        at_limit.loc[0,'lot_count']=str(maximum+1);reject('E8','original converter rejects above exact bound',lambda:m.convert_records(at_limit))
        ck('ALL','original source preserved',raw.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
        (lab/'yn_adapter.py').write_bytes((HERE/'yn_adapter.py').read_bytes())
        caller="from conversion import fixture\nfrom yn_adapter import convert_yn\nr=fixture();r['reviewed']=['Y','N','Y']\nprint(convert_yn(r)['reviewed'].tolist())\nr.loc[0,'reviewed']='yes'\ntry:convert_yn(r)\nexcept ValueError as exc:print(str(exc))\n";(lab/'adapter_demo.py').write_text(caller)
        command('E4','supplemental adapter caller',['pandas_lab_76/adapter_demo.py'],parent,expected="[True, False, True]\nreviewed must be exactly Y or N\n")
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=1,test_fence=2,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),adapter_sha256=sha((HERE/'yn_adapter.py').read_bytes()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Exact original source;E4 separate Y/N adapter;E7 scaled-cents design and E8 downstream arithmetic policy not implemented')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
