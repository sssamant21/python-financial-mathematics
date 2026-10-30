"""Formal scoped workflow review of Sections 7.5–7.8, unchanged source."""
import contextlib,hashlib,io,json,os,platform,re,subprocess,sys,tempfile,traceback,types
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
CONFIG=[(5,'7.05-reading-financial-data.md','read_holdings.py','test_read_holdings.py','load_holdings'),
        (6,'7.06-data-types-and-conversion.md','conversion.py','test_conversion.py','convert_records'),
        (7,'7.07-missing-financial-data.md','missingness.py','test_missingness.py','assess'),
        (8,'7.08-cleaning-financial-datasets.md','cleaning.py','test_cleaning.py','clean')]
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
    with tempfile.TemporaryDirectory(prefix='chapter07-ingestion-') as tmp:
        parent=Path(tmp)
        command('ALL','preinstalled environment probe',['-c',"import json,platform,pandas as pd,numpy as np; print(json.dumps(dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,copy_on_write=pd.options.mode.copy_on_write,chained_assignment=pd.options.mode.chained_assignment)))"],parent,environment=True)
        for section,filename,application,test,entry in CONFIG:
            source=BOOK/'chapter-07'/filename;text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
            program_ids=[i for i,code in enumerate(blocks) if 'def '+entry+'(' in code];test_ids=[i for i,code in enumerate(blocks) if 'import unittest' in code]
            assert len(program_ids)==len(test_ids)==1;pi,ti=program_ids[0],test_ids[0];assert ti==pi+1
            labname='pandas_lab_7'+str(section);lab=parent/labname;lab.mkdir();files={application:blocks[pi],test:blocks[ti]}
            for name,code in files.items():(lab/name).write_text(code);compile(code,str(lab/name),'exec')
            fixture=None
            if section==5:
                csv_blocks=re.findall(r'^```csv\n(.*?)^```',text,re.M|re.S);assert len(csv_blocks)==1;fixture=csv_blocks[0].encode();(lab/'holdings.csv').write_bytes(fixture)
            expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S);assert len(expected)==1
            if section==5:expected[0]=expected[0].replace('<hash of the exact local file bytes>',sha(fixture))
            command(str(section),'original demonstration',[labname+'/'+application],parent,expected=expected[0])
            command(str(section),'original unittest discovery',['-m','unittest','discover','-s',labname,'-v'],parent,count=8)
            command(str(section),'original compileall',['-m','compileall','-q',labname],parent,expected='')
            command(str(section),'quiet import',['-c','import '+application[:-3]],lab,expected='')
            ck(str(section),'two reconstructed listings unchanged',{n:sha((lab/n).read_bytes()) for n in files},{n:sha(c.encode()) for n,c in files.items()})
            module=types.ModuleType('exact_lab_7'+str(section));exec(compile(blocks[pi],str(source),'exec'),module.__dict__);modules[section]=module
            namespace={'__name__':'prose_snippets_7'+str(section),'pd':pd,'np':np}
            if section==8:
                captured_locals={}
                def observe(frame,event,arg):
                    if event=='return' and frame.f_code.co_filename==str(source) and frame.f_code.co_name=='clean':captured_locals.update(frame.f_locals)
                    return observe
                previous=sys.gettrace()
                try:
                    sys.settrace(observe);module.clean(module.fixture())
                finally:sys.settrace(previous)
                namespace['normalized']=captured_locals['normalized'].copy(deep=True)
            captured=io.StringIO()
            with contextlib.redirect_stdout(captured):
                for index in range(pi):exec(compile(blocks[index],str(source)+':fence'+str(index),'exec'),namespace)
            snippets[section]=namespace
            sources.append(dict(section='7.'+str(section),source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=pi,test_fence=ti,program_file=application,test_file=test,listing_sha256={n:sha(c.encode()) for n,c in files.items()},prose_fences=list(range(pi)),prose_sha256=[sha(c.encode()) for c in blocks[:pi]],prose_stdout=captured.getvalue(),fixture_sha256=sha(fixture) if fixture is not None else None,prose_prelude='normalized captured from original clean(fixture()) return-event locals' if section==8 else ('pandas/NumPy imports supplied for illustrative fragment' if pi else 'none')))
    m=modules[5];source=BOOK/'chapter-07/7.05-reading-financial-data.md';payload=re.findall(r'^```csv\n(.*?)^```',source.read_text(),re.M|re.S)[0].encode()
    with tempfile.TemporaryDirectory(prefix='csv-snapshot-probes-') as tmp:
        path=Path(tmp)/'holdings.csv';path.write_bytes(payload);table,total,evidence=m.load_holdings(path,currency='USD',valuation_date='2026-01-30')
        ck('5','literal identifiers and independent valuation',(table.index.tolist(),table['market_value'].tolist(),total),(['00123','BETA','NA'],[600.,300.,100.],float(F(6)*100+F(3)*100+F(1)*100)))
        ck('5','same parsed snapshot bytes hashed',(evidence['sha256'],evidence['bytes'],evidence['rows']),(sha(payload),len(payload),3))
        ck('5','published LF-fixture hash',evidence['sha256'],'e68b437d0a8476c1b21a01a0ae4577144b54c79b8383d1f0d9779dd958297c11')
        crlf=payload.replace(b'\n',b'\r\n');path.write_bytes(crlf);other,other_total,other_evidence=m.load_holdings(path,currency='USD',valuation_date='2026-01-30')
        ck('5','CRLF preserves financial table but changes bytes',(other.equals(table),other_total,other_evidence['sha256']!=evidence['sha256']),(True,1000.,True))
        path.write_bytes(payload.replace(b'BETA',b'00123'));reject('5','duplicate raw identifier rejected',lambda:m.load_holdings(path,currency='USD',valuation_date='2026-01-30'))
        path.write_bytes(payload.replace(b'USD',b'EUR',1));reject('5','different currency rejected without conversion',lambda:m.load_holdings(path,currency='USD',valuation_date='2026-01-30'))
        path.write_bytes(payload);reject('5','invalid expected calendar date rejected',lambda:m.load_holdings(path,currency='USD',valuation_date='2026-02-30'))
        ck('5','read does not mutate local payload',path.read_bytes(),payload)
    m=modules[6];raw=m.fixture();before=raw.copy(deep=True);typed=m.convert_records(raw)
    ck('6','explicit output schema/dtypes',[str(t) for t in typed.dtypes],['string','Int64','float64','boolean'])
    ck('6','literal identities Boolean map and observed zero',(typed['asset'].tolist(),typed['reviewed'].tolist(),typed.loc[2,'lot_count'],pd.isna(typed.loc[1,'lot_count'])),(['00123','NA','BETA'],[True,False,True],0,True))
    ck('6','text decimal price reference',typed.loc[0,'price'],float(F(401,4)))
    maxint=raw.copy();maxint.loc[0,'lot_count']=str(2**63-1);ck('6','Int64 maximum kept exactly',int(m.convert_records(maxint).loc[0,'lot_count']),2**63-1)
    maxint.loc[0,'lot_count']=str(2**63);reject('6','above Int64 bound rejected before float route',lambda:m.convert_records(maxint))
    bad=raw.copy();bad.loc[0,'reviewed']='False';reject('6','undocumented Boolean spelling rejected',lambda:m.convert_records(bad))
    typed.loc[0,'price']=0;ck('6','typed output edits preserve raw text',raw.equals(before),True)
    ck('6','prose introduced-failure vs all-missing counts',(int(snippets[6]['introduced'].sum()),int(snippets[6]['parsed'].isna().sum())),(1,2))
    m=modules[7];w=pd.Series([.6,.3,.1],index=['A','B','C']);r=pd.Series([.1,0.],index=['A','C']);wc=w.copy();rc=r.copy();report,total,summary=m.assess(w,r)
    ck('7','coverage first missing/absent policy',(total,summary),(None,dict(expected=3,observed=2,missing=1,absent=1,complete=False)))
    explicit=pd.Series([.1,np.nan,0.],index=w.index);_,_,explicit_summary=m.assess(w,explicit);ck('7','explicit missing differs from absent record',(explicit_summary['missing'],explicit_summary['absent']),(1,0))
    _,empty_total,empty_summary=m.assess(w,pd.Series(dtype='float64'));ck('7','empty source returns retains full expected population',(empty_total,empty_summary),(None,dict(expected=3,observed=0,missing=3,absent=3,complete=False)))
    _,complete_total,complete_summary=m.assess(w,pd.Series([.1,-.05,0.],index=w.index));ck('7','complete rational contribution total',abs(complete_total-float(F(9,200)))<=1e-12,True)
    ck('7','zero is observed not missing',m.assess(w,pd.Series([0.,0.,0.],index=w.index))[1],0.)
    ck('7','missing zero-weight asset still blocks total',m.assess(pd.Series([1.,0.],index=['A','B']),pd.Series([.1],index=['A']))[1],None)
    reject('7','unexpected return identity rejected',lambda:m.assess(w,pd.Series([.1],index=['OTHER'])))
    report.loc['A','weight']=99;ck('7','coverage report edit preserves inputs',(w.equals(wc),r.equals(rc)),(True,True))
    m=modules[8];raw=m.fixture();before=raw.copy(deep=True);good,bad,log=m.clean(raw)
    ck('8','record conservation and outcomes',(len(raw),len(good),len(bad),len(log)),(6,2,4,6))
    ck('8','independent accepted asset values',(good['asset'].tolist(),good['market_value'].tolist()),(['ALPHA','CASH'],[float(F(6)*100),float(F(1)*100)]))
    ck('8','all duplicate records quarantined',bad.loc[bad['reason'].str.contains('duplicate_asset'),'source_row'].tolist(),[1,2])
    ck('8','one audit ordinal per source record',sorted(good['source_row'].tolist()+bad['source_row'].tolist()),list(range(6)))
    ck('8','approved normalization change count',int(log['changed'].sum()),2)
    ck('8','raw duplicate token retained',bad.loc[bad['source_row']==2,'asset'].iloc[0],' BETA ')
    ck('8','exact prose duplicate mask from captured normalized table',snippets[8]['duplicate'].tolist(),[False,True,True,False,False,False])
    original_raw=raw.to_dict(orient='records');audit=dict(scope='exact original clean(fixture()) output; not complete batch valuation',raw=original_raw,accepted=good.to_dict(orient='records'),rejected=bad.to_dict(orient='records'),audit=log.to_dict(orient='records'))
    (HERE/'cleaning-audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
    good.loc[0,'price']=0;ck('8','accepted edit preserves original text source',raw.equals(before),True)
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,workflows=4,derived_step_units=32,command_records=len(commands),command_failed=sum(c['status']=='FAIL' for c in commands),existing_method_invocations=sum(c['actual_methods'] or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL' for c in checks),scope='preinstalled Linux runtime; setup PARTIAL; no fresh install or Windows/macOS/notebook acceptance',sources=sources,cleaning_audit_sha256=sha((HERE/'cleaning-audit.json').read_bytes()),commands=commands,checks=checks)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('sources','commands','checks')}));return bool(output['failed'] or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
