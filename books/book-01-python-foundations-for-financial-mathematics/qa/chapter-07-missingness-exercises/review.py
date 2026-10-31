"""Scoped Section 7.7 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.07-missing-financial-data.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==3;program,test=blocks[1:3]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-missingness-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_77';lab.mkdir()
        for name,code in [('missingness.py',program),('test_missingness.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_77/missingness.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_77','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_77'],parent,expected='')
        ck('ALL','source listings unchanged',{n:sha((lab/n).read_bytes())for n in ('missingness.py','test_missingness.py')},{'missingness.py':sha(program.encode()),'test_missingness.py':sha(test.encode())})
        m=types.ModuleType('exact_missingness');exec(compile(program,str(source),'exec'),m.__dict__)
        w=pd.Series([.6,.3,.1],index=['ALPHA','BETA','CASH']);absent=pd.Series([.1,0.],index=['ALPHA','CASH']);explicit=pd.Series([.1,np.nan,0.],index=w.index);wc=w.copy(deep=True);ac=absent.copy(deep=True)
        ra,ta,sa=m.assess(w,absent);explicit_report,te,se=m.assess(w,explicit)
        ck('E1','absent versus explicit missing counts',(sa['missing'],sa['absent'],se['missing'],se['absent']),(1,1,1,0))
        ck('E1','both input states withhold total',(ta,te),(None,None))
        ck('E1','distinct structural flags on BETA',(ra.loc['BETA','absent_record'],explicit_report.loc['BETA','absent_record'],ra.loc['BETA','missing_return'],explicit_report.loc['BETA','missing_return']),(True,False,True,True))
        zero=pd.Series([0.,0.,0.],index=w.index);rz,tz,sz=m.assess(w,zero)
        ck('E2','observed zero is complete',(tz,sz),(0.,dict(expected=3,observed=3,missing=0,absent=0,complete=True)))
        ck('E2','zero contributions observed not imputed',rz['contribution'].tolist(),[0.,0.,0.])
        empty=pd.Series(dtype='float64');rr,tr,sr=m.assess(w,empty)
        ck('E3','empty returns retain expected coverage',(tr,sr),(None,dict(expected=3,observed=0,missing=3,absent=3,complete=False)))
        ck('E3','all expected identities remain in report',(rr.index.tolist(),rr['missing_return'].tolist()),(w.index.tolist(),[True]*3))
        full=pd.Series([.1,-.05,0.],index=w.index);rf,tf,sf=m.assess(w,full)
        partial=F(3,5)*F(1,10)+F(1,10)*0;renormalized=partial/(F(3,5)+F(1,10));complete=partial+F(3,10)*F(-1,20)
        ck('E4','independent rational alternatives',(partial,renormalized,complete),(F(3,50),F(3,35),F(9,200)))
        ck('E4','unguarded partial contribution agrees with scalar benchmark',abs((w*absent).sum()-float(partial))<=1e-12,True)
        ck('E4','renormalized observed exposures are another question',abs((w*absent).sum()/w.loc[absent.index].sum()-float(renormalized))<=1e-12,True)
        ck('E4','complete source return matches rational benchmark',abs(tf-float(complete))<=1e-12,True)
        ck('E4','display values only for interpretation',[format(float(x),'.4%')for x in (partial,renormalized,complete)],['6.0000%','8.5714%','4.5000%'])
        ck('E4','partial total never published by strict API',(ta,sa['complete']),(None,False))
        extra=pd.concat([full,pd.Series([.02],index=['OTHER'])]);reject('E5','unexpected return identifier rejects',lambda:m.assess(w,extra))
        prices=pd.Series([100.,np.nan,110.]);before=prices.copy(deep=True)
        ck('E6','forward fill uses prior observation',prices.ffill().tolist(),[100.,100.,110.])
        ck('E6','backward fill uses later observation',prices.bfill().tolist(),[100.,110.,110.])
        ck('E6','fill returns new object without changing missing source',prices.equals(before),True)
        zero_weights=pd.Series([1.,0.],index=['ALPHA','BETA']);only_active=pd.Series([.1],index=['ALPHA'])
        rs,ts,ss=m.assess(zero_weights,only_active)
        ck('E8','original strict implementation blocks missing zero-weight return',(ts,ss['missing'],ss['absent'],ss['complete']),(None,1,1,False))
        rz,tz,sz=m.assess(zero_weights,pd.Series([.1,0.],index=zero_weights.index));ck('E8','observed zero-weight return permits strict complete calculation',(tz,sz['complete']),(.1,True))
        tiny=1e-15;tiny_weights=pd.Series([1.-tiny,tiny],index=['ALPHA','BETA']);ck('E8','small positive missing exposure also blocks strict total',m.assess(tiny_weights,only_active)[1],None)
        reject('E8','invalid observed return still rejected on zero weight',lambda:m.assess(zero_weights,pd.Series([.1,np.inf],index=zero_weights.index)))
        ra.loc['ALPHA','weight']=9;ck('ALL','report mutation preserves caller inputs',(w.equals(wc),absent.equals(ac)),(True,True))
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=1,test_fence=2,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Original strict source assessment and supplemental rational/fill mechanics;E7 quote-age and E8 zero-weight exception designs not implemented')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
