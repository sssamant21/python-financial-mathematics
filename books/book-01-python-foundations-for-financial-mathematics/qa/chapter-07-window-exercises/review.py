"""Scoped Section 7.14 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.14-rolling-and-expanding-calculations.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==6;program,test=blocks[4:6]
    expected='price rolling_mean rolling_std expanding_mean prior_mean\n2026-01-30 14:00:00+00:00 100.00 NaN NaN 100.00 NaN\n2026-01-30 14:10:00+00:00 102.00 NaN NaN 101.00 NaN\n2026-01-30 14:40:00+00:00 104.00 102.00 2.00 102.00 NaN\n2026-01-30 15:00:00+00:00 106.00 104.00 2.00 103.00 102.00\n2026-01-30 15:10:00+00:00 108.00 106.00 2.00 104.00 104.00\n'
    with tempfile.TemporaryDirectory(prefix='chapter07-window-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_714';lab.mkdir()
        for name,code in [('windows.py',program),('test_windows.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_714/windows.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_714','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_714'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('windows.py','test_windows.py')},{'windows.py':sha(program.encode()),'test_windows.py':sha(test.encode())})
        m=types.ModuleType('exact_windows');exec(compile(program,str(source),'exec'),m.__dict__);prices=m.fixture();before=prices.copy(deep=True);report=m.summaries(prices)
        ck('E1','independent final rolling and expanding means',(report['rolling_mean'].iloc[-1],report['expanding_mean'].iloc[-1]),(float((F(104)+106+108)/3),float((F(100)+102+104+106+108)/5)))
        ck('E2','rolling warmup mask',report['rolling_mean'].isna().tolist(),[True,True,False,False,False])
        ck('E2','previous-row warmup mask',report['prior_mean'].isna().tolist(),[True,True,True,False,False])
        ck('E2','first mature prior mean',report['prior_mean'].iloc[3],102.)
        stamp=prices.index[2];timed=prices.loc[(prices.index>stamp-pd.Timedelta(minutes=30))&(prices.index<=stamp)]
        ck('E3','explicit30min population excludes left endpoint',(timed.index.tolist(),timed.tolist()),([stamp],[104.]))
        ck('E3','three-row population is different',prices.iloc[:3].tolist(),[100.,102.,104.])
        ck('E3','time versus observation means',(prices.rolling('30min',min_periods=1,closed='right').mean().iloc[2],report['rolling_mean'].iloc[2]),(104.,102.))
        changed=prices.copy();changed.iloc[-1]=1000.;after=m.summaries(changed)
        ck('E4','future perturbation preserves earlier complete output',after.iloc[:-1].equals(report.iloc[:-1]),True)
        ck('E4','current final mean changes but prior does not',(abs(after['rolling_mean'].iloc[-1]-float((F(104)+106+1000)/3))<=1e-12,after['prior_mean'].iloc[-1]),(True,104.))
        ck('E4','independent changed expanding mean',after['expanding_mean'].iloc[-1],float((F(100)+102+104+106+1000)/5))
        variance=F(8,3);sample_variance=F(8,2)
        ck('E5','independent ddof variance references',(variance,sample_variance),(F(8,3),F(4)))
        sample=pd.Series([100.,102.,104.]);ck('E5','pandas standard deviations agree with scalar sqrt',(abs(sample.std(ddof=0)-float(variance)**.5)<=1e-12,sample.std(ddof=1)),(True,2.))
        ck('E6','prior feature delays are rows not fixed elapsed duration',[(prices.index[i]-prices.index[i-1]).total_seconds()for i in (3,4)],[20*60.,10*60.])
        # Independent prefix sums, not another expanding expression.
        numbers=[F(100),F(102),F(104),F(106),F(108)];prefix=F(0)
        for i,value in enumerate(numbers):
            prefix+=value;ck('E8','scalar expanding prefix row'+str(i),report['expanding_mean'].iloc[i],float(prefix/(i+1)))
        ck('ALL','original prices unchanged',prices.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=4,test_fence=5,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='Original trailing/expanding descriptive source and independent prefix/variance oracles;E7 availability contract conceptual only,no historical strategy acceptance')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
