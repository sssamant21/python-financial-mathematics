"""Scoped Section 7.12 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.12-joining-and-merging-financial-data.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==3;program,test=blocks[1:3]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-merge-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_712';lab.mkdir()
        for name,code in [('merging.py',program),('test_merging.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_712/merging.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_712','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_712'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('merging.py','test_merging.py')},{'merging.py':sha(program.encode()),'test_merging.py':sha(test.encode())})
        m=types.ModuleType('exact_merging');exec(compile(program,str(source),'exec'),m.__dict__);h,q=m.fixture();hc=h.copy(deep=True);qc=q.copy(deep=True)
        audit,result,total=m.reconcile(h,q.iloc[:2]);cash=audit.loc[audit['asset']=='CASH'].iloc[0]
        ck('E1','unpriced CASH remains visible',(cash['_merge'],cash['quantity'],pd.isna(cash['price'])),('left_only',1.,True))
        ck('E1','incomplete match withholds all valuation',(result,total),(None,None))
        ck('E1','outer audit preserves all holdings',audit['asset'].tolist(),['ALPHA','BETA','CASH'])
        extra=q.iloc[[0]].copy();extra['asset']='OTHER';extended=pd.concat([q,extra]);a,r,t=m.reconcile(h,extended)
        ck('E2','extra quote visible under exact-population contract',(a.loc[a['_merge']=='right_only','asset'].tolist(),r,t),(['OTHER'],None,None))
        broad=h.merge(extended,on=m.KEY,how='left',validate='one_to_one',indicator=True)
        ck('E2','broader-reference left join is a different controlled population',(len(broad),broad['_merge'].eq('both').all()),(3,True))
        duplicated=pd.concat([q,q.iloc[[0]]]);reject('E3','public prevalidation rejects duplicate quote key',lambda:m.reconcile(h,duplicated))
        try:h.merge(duplicated,on=m.KEY,how='outer',validate='one_to_one');actual='no exception';trace=''
        except Exception as error:actual=type(error).__name__;trace=traceback.format_exc()
        ck('E3','pandas one_to_one guard independently rejects duplicate',actual,'MergeError');checks[-1]['expected_exception_trace']=trace
        left=pd.DataFrame({'asset':['A','A'],'quantity':[1.,2.]});right=pd.DataFrame({'asset':['A','A'],'price':[10.,11.]});cross=left.merge(right,on='asset')
        ck('E4','two-by-two keyed merge creates four pairs',list(zip(cross['quantity'],cross['price'])),[(1.,10.),(1.,11.),(2.,10.),(2.,11.)])
        ck('E4','merged quantity count is doubled',(len(cross),cross['quantity'].sum(),left['quantity'].sum()),(4,6.,3.))
        ck('E4','independent candidate-pair value sum',float((cross['quantity']*cross['price']).sum()),float(F(1)*10+F(1)*11+F(2)*10+F(2)*11))
        original=m.reconcile(h,q);reversed_result=m.reconcile(h.iloc[::-1],q.iloc[::-1])
        ck('E5','source reversal preserves normalized audits and valuations',(original[0].equals(reversed_result[0]),original[1].equals(reversed_result[1]),original[2],reversed_result[2]),(True,True,1000.,1000.))
        ck('E5','independent keyed valuation',(original[1]['market_value'].tolist(),original[2]),([600.,300.,100.],float(F(6)*100+F(3)*100+100)))
        many=left.merge(right.iloc[:1],on='asset',validate='many_to_one');ck('E6','mechanical many-left to unique-right example',(len(many),many['quantity'].sum()),(2,3.))
        wrong=q.copy();wrong['valuation_date']='2026-01-29';reject('E7','different date rejected before matching',lambda:m.reconcile(h,wrong))
        reject('E8','original narrow schema rejects extra provenance fields',lambda:m.reconcile(h.assign(holdings_source_row=range(3)),q))
        original[1].loc[0,'price']=0;ck('ALL','report mutation preserves both sources',(h.equals(hc),q.equals(qc)),(True,True))
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=1,test_fence=2,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Exact original strict reconciliation;mechanical pandas cardinality/left-join examples;E6 account contract/E7 intraday metadata/E8 provenance designs not integrated')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
