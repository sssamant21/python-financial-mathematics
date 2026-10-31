"""Scoped Section 7.9 local exercise review, unchanged source."""
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
    source=BOOK/'chapter-07/7.09-date-and-time-indexes.md';text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==5;program,test=blocks[3:5]
    expected=re.findall(r'^```text\n(.*?)^```',text,re.M|re.S)[0]
    with tempfile.TemporaryDirectory(prefix='chapter07-date-exercises-')as tmp:
        parent=Path(tmp);lab=parent/'pandas_lab_79';lab.mkdir()
        for name,code in [('time_index.py',program),('test_time_index.py',test)]:
            (lab/name).write_bytes(code.encode());compile(code,str(lab/name),'exec')
        command('ALL','original demonstration',['pandas_lab_79/time_index.py'],parent,expected=expected)
        command('ALL','original unittest discovery',['-m','unittest','discover','-s','pandas_lab_79','-v'],parent,count=8)
        command('ALL','original compileall',['-m','compileall','-q','pandas_lab_79'],parent,expected='')
        ck('ALL','source listing hashes',{n:sha((lab/n).read_bytes())for n in ('time_index.py','test_time_index.py')},{'time_index.py':sha(program.encode()),'test_time_index.py':sha(test.encode())})
        m=types.ModuleType('exact_time_index');exec(compile(program,str(source),'exec'),m.__dict__)
        from datetime import datetime,timezone
        winter=datetime.fromisoformat('2026-01-30T09:30:00-05:00').astimezone(timezone.utc)
        ck('E1','independent standard-library offset arithmetic',winter.isoformat(),'2026-01-30T14:30:00+00:00')
        paired=pd.to_datetime(['2026-01-30T09:30:00-05:00','2026-01-30T14:30:00Z'],format='%Y-%m-%dT%H:%M:%S%z',utc=True)
        ck('E1','pandas explicit stamps identify same instant',(paired[0]==paired[1],paired[0].to_pydatetime()==winter),(True,True))
        raw=m.fixture();raw.loc[2,'timestamp']='2026-01-30T16:30:00+01:00';before=raw.copy(deep=True);series=m.price_series(raw)
        naive=raw.copy();naive.loc[0,'timestamp']='2026-01-30T10:00:00';reject('E2','removed offset rejected',lambda:m.price_series(naive))
        reversed_series=m.price_series(raw.iloc[::-1]);ck('E3','reverse valid fixture retains full timestamp-price pairing',reversed_series.equals(series),True)
        ck('E3','independent expected UTC pairs',[(x.isoformat(),v)for x,v in series.items()],[('2026-01-30T14:30:00+00:00',100.),('2026-01-30T15:00:00+00:00',101.),('2026-01-30T15:30:00+00:00',102.)])
        reject('E3','uncorrected fixture still rejects duplicate instants',lambda:m.price_series(m.fixture()))
        start=pd.Timestamp('2026-01-30T15:00:00Z');end=pd.Timestamp('2026-01-30T15:30:00Z')
        inclusive=series.loc[start:end];halfopen=series.loc[(series.index>=start)&(series.index<end)]
        ck('E4','inclusive versus half-open values',(inclusive.tolist(),halfopen.tolist()),([101.,102.],[101.]))
        ck('E4','inclusive versus half-open endpoint counts',(len(inclusive),len(halfopen)),(2,1))
        local_naive=pd.DatetimeIndex(['2026-01-30 09:30:00']);localized=local_naive.tz_localize('America/New_York',ambiguous='raise',nonexistent='raise');utc=localized.tz_convert('UTC');returned=utc.tz_convert('America/New_York')
        ck('E5','winter localized UTC matches independent oracle',utc[0].to_pydatetime(),winter)
        ck('E5','aware roundtrip preserves instant and local clock',(returned.equals(localized),returned.tz_localize(None).equals(local_naive)),(True,True))
        summer=pd.DatetimeIndex(['2026-07-30 09:30:00']).tz_localize('America/New_York',ambiguous='raise',nonexistent='raise');summer_utc=summer.tz_convert('UTC')
        ck('E6','runtime regional offset differs winter/summer',(localized[0].utcoffset().total_seconds(),summer[0].utcoffset().total_seconds()),(-5*3600.,-4*3600.))
        ck('E6','runtime summer NewYork opening converts13:30UTC',summer_utc[0].isoformat(),'2026-07-30T13:30:00+00:00')
        fixed=pd.Timestamp('2026-07-30T09:30:00-05:00').tz_convert('UTC');ck('E6','fixed offset is a different summer instant',(fixed-summer_utc[0]).total_seconds(),3600.)
        ck('ALL','source unchanged',raw.equals(before),True)
        ck('ALL','prepared versions',(platform.python_version(),pd.__version__,np.__version__),('3.12.14','2.2.3','2.3.5'))
        from importlib.metadata import version,PackageNotFoundError
        tzversions={}
        for dependency in ('pytz','tzdata'):
            try:tzversions[dependency]=version(dependency)
            except PackageNotFoundError:tzversions[dependency]=None
    output=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,platform=platform.platform(),copy_on_write=pd.options.mode.copy_on_write,timezone_type=type(localized.tz).__module__+'.'+type(localized.tz).__name__,timezone_packages=tzversions,source=str(source.relative_to(BOOK)),source_sha256=sha(source.read_bytes()),program_fence=3,test_fence=4,program_sha256=sha(program.encode()),test_sha256=sha(test.encode()),answers=8,command_records=len(commands),command_failed=sum(c['status']=='FAIL'for c in commands),existing_method_invocations=sum(c['actual_methods']or 0 for c in commands),predicates=len(checks),failed=sum(c['status']=='FAIL'for c in checks),commands=commands,checks=checks,scope='E1-6 original source and supplemental explicit time arithmetic;E7 composite key/E8 availability metadata conceptual only;host/provider results not platform acceptance')
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items()if k not in ('checks','commands')}));return bool(output['failed']or output['command_failed'])
if __name__=='__main__':raise SystemExit(run())
