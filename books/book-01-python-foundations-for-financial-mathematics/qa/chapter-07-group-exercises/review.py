"""Scoped Section 7.11 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.11-grouping-and-aggregation.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==5;program,test=blocks[3:5]
    # Explicit full-table expectation from published table and independent formulas.
    expected='asset_count opening_value price_pnl portfolio_weight portfolio_contribution sector_return\nsector\ncash 1 100.0000 0.0000 0.1000 0.0000 0.0000\nequity 2 900.0000 45.0000 0.9000 0.0450 0.0500\nunused 1 0.0000 0.0000 0.0000 0.0000 NaN\nPortfolio price return: 4.50%\n'
    with tempfile.TemporaryDirectory(prefix='chapter07-group-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_711';lab.mkdir()
        for name,code in [('grouping.py',program),('test_grouping.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_711/grouping.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_711','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_711'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('grouping.py','test_grouping.py')},{'grouping.py':sha(program.encode()),'test_grouping.py':sha(test.encode())})
        m=types.ModuleType('exact_grouping');exec(compile(program,str(source),'exec'),m.__dict__);raw=m.fixture();before=raw.copy(deep=True);report,total=m.summarize(raw)
        simple=(F(1,10)+F(-1,20))/2;pnl=F(600)*F(1,10)+F(300)*F(-1,20);weighted=pnl/900;contribution=pnl/1000
        ck('E1','independent rational mean/weighted/contribution',(simple,weighted,contribution),(F(1,40),F(1,20),F(9,200)))
        ck('E1','source equity denominators and portfolio total',(abs(report.loc['equity','sector_return']-float(weighted))<=1e-12,abs(report.loc['equity','portfolio_contribution']-float(contribution))<=1e-12,abs(total-float(contribution))<=1e-12),(True,True,True))
        reverse,rt=m.summarize(raw.iloc[::-1]);ck('E2','fixture reversal preserves keyed summary',(reverse.equals(report),rt),(True,total))
        ck('E2','report keys deliberately sorted',report.index.tolist(),['cash','equity','unused'])
        added=pd.concat([raw,pd.DataFrame({'asset':['CASH2'],'sector':['cash'],'opening_value':[200.],'asset_return':[.02]})],ignore_index=True);augmented,at=m.summarize(added)
        ck('E3','new cash sector counts and scalar PnL',(augmented.loc['cash','asset_count'],augmented.loc['cash','opening_value'],augmented.loc['cash','price_pnl']),(2,300.,float(F(200)*F(1,50))))
        ck('E3','new invested portfolio conserves rows/value/PnL',(int(augmented['asset_count'].sum()),augmented['opening_value'].sum(),augmented['price_pnl'].sum()),(5,1200.,49.))
        ck('E3','cash sector return and portfolio contribution use different denominators',(abs(augmented.loc['cash','sector_return']-float(F(4,300)))<=1e-12,abs(augmented.loc['cash','portfolio_contribution']-float(F(4,1200)))<=1e-12),(True,True))
        ck('E3','independent new portfolio price return',abs(at-float(F(49,1200)))<=1e-12,True)
        ck('E3','group contributions reconcile new portfolio',abs(augmented['portfolio_contribution'].sum()-at)<=1e-12,True)
        missing=raw.copy();missing.loc[0,'sector']=None
        ck('E4','generic pandas dropna choice changes population',(int(missing.groupby('sector').size().sum()),int(missing.groupby('sector',dropna=False).size().sum())),(3,4))
        ck('E4','generic default drops unclassified opening exposure',missing.groupby('sector')['opening_value'].sum().sum(),400.)
        reject('E4','public source rejects missing classification',lambda:m.summarize(missing))
        extra_zero=pd.concat([raw,pd.DataFrame({'asset':['ZERO2'],'sector':['otherzero'],'opening_value':[0.],'asset_return':[.1]})],ignore_index=True);zr,zt=m.summarize(extra_zero)
        ck('E5','observed zero sector remains with undefined own return',(zr.loc['otherzero','asset_count'],zr.loc['otherzero','opening_value'],pd.isna(zr.loc['otherzero','sector_return']),zr.loc['otherzero','portfolio_contribution']),(1,0.,True,0.))
        ck('E5','zero exposure does not change total return',zt,total)
        transformed=raw.groupby('sector')['opening_value'].transform('sum');ck('E6','row-aligned sector totals',transformed.tolist(),[900.,900.,100.,0.])
        ck('E6','summing repeated transform is not group reconciliation',(transformed.sum(),report['opening_value'].sum()),(1900.,1000.))
        omitted=raw.loc[raw['asset']!='BETA'];orpt,ot=m.summarize(omitted)
        ck('E8','whole missing asset can still pass local source validation',(int(orpt['asset_count'].sum()),orpt['opening_value'].sum(),abs(ot-float(F(60,700)))<=1e-12),(3,700.,True))
        ck('ALL','source preserved',raw.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=3,test_fence=4,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Exact original source and supplemental group/transform mechanics;independent rational denominators;E7 account keys and E8 external population reconciliation conceptual only')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
