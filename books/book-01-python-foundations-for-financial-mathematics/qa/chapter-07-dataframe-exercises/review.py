"""Scoped Section 7.3 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.03-dataframe.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==5;program,test=blocks[3:5]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-dataframe-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_73';lab.mkdir()
        for name,code in [('holdings.py',program),('test_holdings.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_73/holdings.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_73','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_73'],parent,expected='')
        ck('ALL','source listings unchanged',{n:sha((lab/n).read_bytes())for n in ('holdings.py','test_holdings.py')},{'holdings.py':sha(program.encode()),'test_holdings.py':sha(test.encode())})
        m=types.ModuleType('exact_holdings');exec(compile(program,str(source),'exec'),m.__dict__)
        raw=m.fixture();before=raw.copy(deep=True);table,total=m.holdings_table(raw);table_before=table.copy(deep=True)
        ck('E1','single bracket price selection is Series',(isinstance(table['price'],pd.Series),table['price'].shape,table['price'].ndim),(True,(3,),1))
        ck('E1','list bracket price selection is DataFrame',(isinstance(table[['price']],pd.DataFrame),table[['price']].shape,table[['price']].ndim),(True,(3,1),2))
        reversed_table,reversed_total=m.holdings_table(raw.iloc[::-1])
        ck('E2','row order reversed with full labels',(reversed_table.index.tolist(),reversed_table['market_value'].tolist()),(['CASH','BETA','ALPHA'],[100.,300.,600.]))
        ck('E2','independent exact total invariant',(total,reversed_total),(float(F(6)*100+F(3)*100+100),1000.))
        columns,ctotal=m.holdings_table(raw.loc[:,['price','quantity']])
        ck('E3','output fields normalized while input order flexible',columns.columns.tolist(),['quantity','price','market_value'])
        ck('E3','column reorder preserves all asset values',(columns.equals(table),ctotal),(True,total))
        derived=table.assign(price_times_two=table['price']*2)
        ck('E4','separate derived price field not a holdings-value computation',derived['price_times_two'].tolist(),[200.,200.,200.])
        ck('E4','derived field has different values from market value',derived['price_times_two'].equals(derived['market_value']),False)
        ck('E4','assign leaves original report unchanged',(table.equals(table_before),'price_times_two'in table.columns),(True,False))
        external=pd.Series([1.,101.],index=['CASH','ALPHA']);copied=table.copy(deep=True);copied['external_price']=external
        ck('E5','external Series aligns existing asset labels',(copied.loc['ALPHA','external_price'],copied.loc['CASH','external_price']),(101.,1.))
        ck('E5','missing BETA remains explicit',copied['external_price'].isna().to_dict(),{'ALPHA':False,'BETA':True,'CASH':False})
        ck('E5','assignment neither fills gaps nor mutates original',(copied['external_price'].count(),table.equals(table_before)),(2,True))
        duplicate=raw.copy();duplicate.index=['ALPHA','ALPHA','CASH'];reject('E6','duplicate asset index rejected',lambda:m.holdings_table(duplicate))
        dupcol=pd.DataFrame([[6.,100.]],index=['ALPHA'],columns=['quantity','quantity']);reject('E6','duplicate source columns rejected',lambda:m.holdings_table(dupcol))
        reject('E6','unexpected currency source field rejected',lambda:m.holdings_table(raw.assign(currency='USD')))
        changed=table.copy(deep=True);changed.loc['ALPHA','quantity']=7.
        ck('E7','quantity edit leaves stored derived value stale',(changed.loc['ALPHA','quantity'],changed.loc['ALPHA','market_value'],float(changed['market_value'].sum(skipna=False))),(7.,600.,1000.))
        reject('E7','passing stale report directly violates source schema',lambda:m.holdings_table(changed))
        recomputed,new_total=m.holdings_table(changed.loc[:,['quantity','price']])
        ck('E7','independent recomputed values and total',(recomputed['market_value'].tolist(),new_total),([float(F(7)*100),300.,100.],float(F(7)*100+F(3)*100+100)))
        ck('E7','recomputation returns new output not reactive linkage',(changed.loc['ALPHA','market_value'],recomputed.loc['ALPHA','market_value']),(600.,700.))
        ck('ALL','all source calls preserve original fixture',raw.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=3,test_fence=4,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='E1-7 exact source plus supplemental pandas field/selection mechanics;E8 multi-context valuation design only;no replacement financial API')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
