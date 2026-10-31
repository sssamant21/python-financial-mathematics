"""Scoped Section 7.5 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.05-reading-financial-data.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==2;program,test=blocks
    fixture=re.findall(r'^```csv\n(.*?)^```',text,re.M|re.S);assert len(fixture)==1;payload=fixture[0].encode()
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0].replace('<hash of the exact local file bytes>',sha(payload))
    snapshots={}
    with tempfile.TemporaryDirectory(prefix='chapter07-csv-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_75';lab.mkdir()
        for name,code in [('read_holdings.py',program),('test_read_holdings.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        (lab/'holdings.csv').write_bytes(payload)
        command('ALL','original demonstration',['pandas_lab_75/read_holdings.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_75','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_75'],parent,expected='')
        ck('ALL','two source listings and CSV unchanged',{n:sha((lab/n).read_bytes())for n in ('read_holdings.py','test_read_holdings.py','holdings.csv')},{'read_holdings.py':sha(program.encode()),'test_read_holdings.py':sha(test.encode()),'holdings.csv':sha(payload)})
        m=types.ModuleType('exact_csv');exec(compile(program,str(source),'exec'),m.__dict__)
        def load(data):
            probe=parent/'probe.csv';probe.write_bytes(data);return m.load_holdings(probe,currency='USD',valuation_date='2026-01-30')
        def retain(name,data,result):
            table,total,evidence=result;(HERE/name).write_bytes(data);snapshots[name]=dict(source_bytes_sha256=sha(data),rows=table.reset_index().to_dict(orient='records'),total=total,evidence=evidence)
        original=load(payload);table,total,evidence=original;retain('holdings-lf.csv',payload,original)
        ck('ALL','independent fixture value and literal IDs',(table.index.tolist(),table['market_value'].tolist(),total),(['00123','BETA','NA'],[600.,300.,100.],float(F(6)*100+F(3)*100+100)))
        renamed_payload=payload.replace(b'00123',b'00007');renamed=load(renamed_payload);retain('holdings-renamed.csv',renamed_payload,renamed)
        ck('E1','leading-zero replacement is literal text',(renamed[0].index[0],isinstance(renamed[0].index[0],str)),('00007',True))
        ck('E1','renaming does not change per-row value',(renamed[0].loc['00007','market_value'],renamed[1]),(600.,1000.))
        omitted_payload=payload.replace(b'BETA,3,100,USD,2026-01-30\n',b'');omitted=load(omitted_payload);retain('holdings-omitted.csv',omitted_payload,omitted)
        ck('E2','missing whole record still satisfies local uniqueness',(omitted[0].index.is_unique,omitted[2]['rows'],omitted[0].index.tolist()),(True,2,['00123','NA']))
        ck('E2','missing BETA accepted subtotal is not original full value',omitted[1],float(F(6)*100+100))
        reject('E3','changed currency rejected',lambda:load(payload.replace(b'USD',b'EUR',1)))
        reject('E3','changed calendar label rejected',lambda:load(payload.replace(b'2026-01-30',b'2026-01-29',1)))
        reject('E4','empty supplied price rejected',lambda:load(payload.replace(b'BETA,3,100,',b'BETA,3,,')))
        zero=load(payload.replace(b'BETA,3,100,',b'BETA,3,0,'));ck('E4','literal zero accepted as different economic observation',(zero[0].loc['BETA','market_value'],zero[1]),(0.,700.))
        crlf_payload=payload.replace(b'\n',b'\r\n');crlf=load(crlf_payload);retain('holdings-crlf.csv',crlf_payload,crlf)
        ck('E5','LF and CRLF retain equal financial rows',(crlf[0].equals(table),crlf[1]),(True,total))
        ck('E5','each snapshot hashes actual bytes',(evidence['sha256'],crlf[2]['sha256']),(sha(payload),sha(crlf_payload)))
        ck('E5','byte identity differs with line endings',evidence['sha256']!=crlf[2]['sha256'],True)
        ck('E5','one extra CR per LF line',(crlf[2]['bytes']-evidence['bytes']),payload.count(b'\n'))
        lines=payload.decode().splitlines();reordered_payload=('\n'.join([lines[0],*lines[:0:-1]])+'\n').encode();reordered=load(reordered_payload);retain('holdings-reordered.csv',reordered_payload,reordered)
        ck('E6','loader retains reversed source record order',reordered[0].index.tolist(),['NA','BETA','00123'])
        ck('E6','asset-level values and total preserved',(reordered[0].sort_index().equals(table.sort_index()),reordered[1]),(True,total))
        ck('E6','reordered bytes have different source hash',reordered[2]['sha256']!=evidence['sha256'],True)
        extra=load(payload+b'OTHER,1,1,USD,2026-01-30\n');ck('E7','current loader has no external expected-set boundary',(extra[0].index.tolist(),extra[1]),(['00123','BETA','NA','OTHER'],1001.))
        reject('E8','single full-file loader detects duplicate across appended groups',lambda:load(payload+lines[1].encode()+b'\n'))
        ck('ALL','documented LF fixture hash',sha(payload),'e68b437d0a8476c1b21a01a0ae4577144b54c79b8383d1f0d9779dd958297c11')
        ck('ALL','source CSV unchanged',(lab/'holdings.csv').read_bytes(),payload)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    (HERE/'snapshots.json').write_text(json.dumps(dict(scope='QA serialization of unchanged loader outputs;not an expected-set or chunked implementation',snapshots=snapshots),indent=2,allow_nan=False)+'\n')
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=0,test_fence=1,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),fixture_sha256=sha(payload),snapshots_sha256=sha((HERE/'snapshots.json').read_bytes()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='E1-6 original loader calls;E7 expected-set contract/test design only;E8 chunked design plus single-full-file duplicate illustration,not streaming execution')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
