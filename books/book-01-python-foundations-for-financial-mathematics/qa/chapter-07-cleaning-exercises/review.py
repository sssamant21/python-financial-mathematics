"""Scoped Section 7.8 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.08-cleaning-financial-datasets.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==3;program,test=blocks[1:3]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-cleaning-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_78';lab.mkdir()
        for name,code in [('cleaning.py',program),('test_cleaning.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_78/cleaning.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_78','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_78'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('cleaning.py','test_cleaning.py')},{'cleaning.py':sha(program.encode()),'test_cleaning.py':sha(test.encode())})
        m=types.ModuleType('cleaning');exec(compile(program,str(source),'exec'),m.__dict__);raw=m.fixture();before=raw.copy(deep=True);good,bad,log=m.clean(raw)
        ck('E1','all three output populations',(len(good),len(bad),len(log)),(2,4,6))
        ck('E1','raw rejection lineage and reasons',list(zip(bad['source_row'],bad['asset'],bad['reason'])),[(1,'BETA','duplicate_asset'),(2,' BETA ','duplicate_asset'),(4,'BAD','invalid_price'),(5,'EURO','unsupported_currency')])
        ck('E1','each source ordinal accounted once',sorted(good['source_row'].tolist()+bad['source_row'].tolist()),list(range(6)))
        ck('E1','decision log all source ordinals/status',list(zip(log['source_row'],log['status'])),[(0,'accepted'),(1,'rejected'),(2,'rejected'),(3,'accepted'),(4,'rejected'),(5,'rejected')])
        added=pd.concat([raw,pd.DataFrame([['00007','0.5','100','USD']],columns=m.FIELDS)],ignore_index=True);g,b,l=m.clean(added)
        ck('E2','leading-zero identifier retained',(g['asset'].tolist(),g.iloc[-1]['market_value']),(['ALPHA','CASH','00007'],float(F(1,2)*100)))
        ck('E2','new record does not cure other batch rejections',(len(b),len(g)+len(b),len(l)),(4,7,7))
        third=pd.concat([raw,pd.DataFrame([['BETA','1','oops','USD']],columns=m.FIELDS)],ignore_index=True);g,b,l=m.clean(third)
        ck('E3','all BETA records stay quarantined',b.loc[b['normalized_asset']=='BETA','source_row'].tolist(),[1,2,6])
        ck('E3','third BETA keeps both reasons',b.loc[b['source_row']==6,'reason'].iloc[0],'duplicate_asset;invalid_price')
        ck('E3','no BETA winner appears',(g['asset'].tolist(),len(b)),(['ALPHA','CASH'],5))
        previous=sys.modules.get('cleaning');sys.modules['cleaning']=m
        try:
            am=types.ModuleType('qa_audit');exec(compile((HERE/'audit_extension.py').read_text(),str(HERE/'audit_extension.py'),'exec'),am.__dict__);audit=am.audited_clean(raw);changes=audit['field_changes']
            ck('E5','field-level changes preserve exact tokens',list(zip(changes['source_row'],changes['field'],changes['before'],changes['after'])),[(0,'asset',' ALPHA ','ALPHA'),(0,'currency',' usd ','USD'),(2,'asset',' BETA ','BETA')])
            ck('E5','three field changes across two changed rows',(len(changes),changes['source_row'].nunique(),int(log['changed'].sum())),(3,2,2))
            ck('E5','supplement preserves original cleaning outputs',(audit['accepted'].equals(good),audit['rejected'].equals(bad),audit['decision_log'][log.columns].equals(log)),(True,True,True))
            ck('E5','supplement does not mutate raw source',raw.equals(before),True)
            ck('E6','EUR remains unsupported not relabeled',bad.loc[bad['source_row']==5,['currency','reason']].iloc[0].tolist(),['EUR','unsupported_currency'])
            ck('E7','current batch has unresolved records',(bad.empty,good['asset'].tolist()),(False,['ALPHA','CASH']))
            payload=audit['source_payload'];digest=sha(payload)
            ck('E8','batch hash binds exact retained parsed-record bytes',audit['source_batch_sha256'],digest)
            ck('E8','all decisions carry digest and explicit policy',(audit['decision_log']['source_batch_sha256'].tolist(),audit['decision_log']['policy_version'].tolist()),([digest]*6,[am.POLICY_VERSION]*6))
            ck('E8','field changes carry same batch/policy',(changes['source_batch_sha256'].tolist(),changes['policy_version'].tolist()),([digest]*3,[am.POLICY_VERSION]*3))
            ck('E8','hash kind distinguishes record serialization from file bytes',audit['source_hash_kind'],'sha256-canonical-utf8-json-records-v1')
            ck('E8','repeat same source produces same batch hash',am.audited_clean(raw)['source_batch_sha256'],digest)
            reordered=am.audited_clean(raw.iloc[::-1]);ck('E8','source order changes batch bytes/hash',reordered['source_batch_sha256']!=digest,True)
            indexed=raw.copy();indexed.index=[7,7,8,8,9,9];ck('E8','original pandas index excluded from declared record hash',am.audited_clean(indexed)['source_batch_sha256'],digest)
            ck('E8','local ordinals still distinct from batch identity',audit['decision_log']['source_row'].tolist(),list(range(6)))
            (HERE/'source-batch.json').write_bytes(payload)
            retained={k:audit[k].to_dict(orient='records')for k in ('accepted','rejected','decision_log','field_changes')};retained.update(source_batch_sha256=digest,source_hash_kind=audit['source_hash_kind'],policy_version=am.POLICY_VERSION,scope='Supplemental audit wrapper;source hash covers canonical parsed records,not original CSV;not complete portfolio valuation')
            (HERE/'audit.json').write_text(json.dumps(retained,indent=2,allow_nan=False)+'\n')
        finally:
            if previous is None:sys.modules.pop('cleaning',None)
            else:sys.modules['cleaning']=previous
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
        (lab/'audit_extension.py').write_bytes((HERE/'audit_extension.py').read_bytes())
        caller="from cleaning import fixture\nfrom audit_extension import audited_clean\na=audited_clean(fixture())\nprint('Field changes: '+str(len(a['field_changes'])))\nprint('Changed rows: '+str(int(a['decision_log']['changed'].sum())))\nprint('Batch digest characters: '+str(len(a['source_batch_sha256'])))\n";(lab/'audit_demo.py').write_text(caller)
        command('E5/E8','supplemental audit caller',['pandas_lab_78/audit_demo.py'],parent,expected='Field changes: 3\nChanged rows: 2\nBatch digest characters: 64\n')
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=1,test_fence=2,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),extension_sha256=sha((HERE/'audit_extension.py').read_bytes()),audit_sha256=sha((HERE/'audit.json').read_bytes()),source_batch_sha256=sha((HERE/'source-batch.json').read_bytes()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Exact original cleaner plus separate E5/E8 field-change/record-hash audit;E4 lot grain/E7 expected universe are designs,not revised financial model')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
