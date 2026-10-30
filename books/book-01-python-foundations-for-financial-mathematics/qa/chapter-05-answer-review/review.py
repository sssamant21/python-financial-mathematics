"""Chapter-wide answer probes; unchanged source plus independent Fraction oracle.

Use --builder PATH to rerun the exact installed-wheel workflows as well.
"""
import argparse,hashlib,json,os,platform,re,shutil,subprocess,sys,tempfile,types
from pathlib import Path
from decimal import Decimal, Inexact, ROUND_DOWN, localcontext
from fractions import Fraction
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
CHAPTER=BOOK/'chapter-05'
def python_blocks(path):return re.findall(r'^```python\n(.*?)^```',path.read_text(),re.M|re.S)
project=next(CHAPTER.glob('5.12-*.md'));config=next(CHAPTER.glob('5.10-*.md'));companion=CHAPTER/'solutions/5.13-solutions-and-reference-implementations.md'
core_code=python_blocks(project)[1];configuration_code=python_blocks(config)[0]
core=types.ModuleType('exact_core');exec(compile(core_code,str(project),'exec'),core.__dict__)
configuration=types.ModuleType('exact_configuration');sys.modules[configuration.__name__]=configuration;exec(compile(configuration_code,str(config),'exec'),configuration.__dict__)
CONFIG=b'{"currency":"USD","rounding":"ROUND_HALF_EVEN","scale":"0.01"}'
def data(amounts):return json.dumps([dict(id=str(i),currency='USD',amount=a) for i,a in enumerate(amounts)]).encode()
def cents(value):
 """Round a nonnegative exact rational amount to integer cents, ties to even."""
 scaled=value*100;q,r=divmod(scaled.numerator,scaled.denominator)
 return q+int(2*r>scaled.denominator or (2*r==scaled.denominator and q%2==1))
def formatted(n):return f'{n//100}.{n%100:02d}'
def run():
 parser=argparse.ArgumentParser();parser.add_argument('--builder',type=Path);args=parser.parse_args();checks=[]
 def ck(id,label,actual,expected):checks.append(dict(problem=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,kind,fn):
  try:fn();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'rejection',actual,kind)
 amounts=['10.005','20.005'];raw=data(amounts)
 ck(13,'rational exact sum',sum(map(Fraction,amounts)),Fraction(3001,100));ck(13,'sum then round cents',cents(sum(map(Fraction,amounts))),3001);ck(13,'round each then sum cents',sum(cents(Fraction(x)) for x in amounts),3000)
 fixtures=[['0'],['0.005'],['0.015'],['0.025'],['0.0001','0.0049'],amounts,['999999.9999','0.0001'],['1000000']*1000]
 for values in fixtures:ck(13,'independent rational benchmark '+str(len(values))+' rows',core.analyze(data(values),CONFIG)['total'],formatted(cents(sum(map(Fraction,values)))))
 with localcontext() as ctx:
  ctx.prec=2;ctx.rounding=ROUND_DOWN;ctx.traps[Inexact]=True;before=(ctx.prec,ctx.rounding,dict(ctx.traps),dict(ctx.flags));answer=core.analyze(raw,CONFIG);ck(14,'hostile caller result',answer['total'],'30.01');ck(14,'caller context unchanged',(ctx.prec,ctx.rounding,dict(ctx.traps),dict(ctx.flags)),before)
 ck(14,'maximum total exact cents',core.analyze(data(['1000000']*1000),CONFIG)['total'],'1000000000.00');err(14,'ValueError',lambda:core.analyze(data(['0']*1001),CONFIG));err(14,'ValueError',lambda:core.analyze(data(['1000000.0001']),CONFIG))
 changed=raw+b'\n';ck(15,'digest differs',hashlib.sha256(raw).digest()!=hashlib.sha256(changed).digest(),True);ck(15,'meaning same',core.analyze(raw,CONFIG),core.analyze(changed,CONFIG));ck(15,'input preserved',raw,data(amounts))
 with tempfile.TemporaryDirectory(prefix='config-review-') as tmp:
  path=Path(tmp)/'settings.json';path.write_text('{"currency":"EUR"}')
  resolved=configuration.resolve(path,{'FINLAB_CURRENCY':'USD'},{'currency':'EUR'});ck(10,'precedence',(resolved.currency,dict(resolved.sources)['currency']),('EUR','cli'));err(10,'ValueError',lambda:configuration.resolve(path,{'FINLAB_CURRENCY':''},{'currency':'EUR'}));ck(10,'absent environment',(configuration.resolve(path,{},{}).currency),'EUR')
 err(11,'ValueError',lambda:core.analyze(b'[]',CONFIG))
 # Prompt 2 checks exact source metadata wiring, not assumed normalization.
 import tomllib
 metadata=tomllib.loads(re.findall(r'^```toml\n(.*?)^```',project.read_text(),re.M|re.S)[0]);ck(2,'distribution name',metadata['project']['name'],'book1-financial-inflows');ck(2,'console target',metadata['project']['scripts'],{'financial-inflows':'financial_inflows.cli:main'});ck(6,'runtime dependencies',metadata['project']['dependencies'],[]);ck(6,'backend pin',metadata['build-system']['requires'],['setuptools==84.0.0'])
 ck(17,'public output keys',set(core.analyze(raw,CONFIG)),{'currency','count','total','method','rounding'});ck(17,'rounding policy',core.analyze(raw,CONFIG)['method'],'sum_then_round')
 installed=dict(status='NOT_RUN',reason='Invoke --builder with declared setuptools84.0.0 to execute installed workflow; source probes are not installed acceptance.')
 if args.builder:
  driver=BOOK/'qa/chapter-05-runtime/backend-resolution/run_package_checks.py'
  with tempfile.TemporaryDirectory(prefix='chapter5-answers-') as tmp:
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
   r=subprocess.run([sys.executable,'-B',str(driver),str(CHAPTER),str(Path(tmp)/'packages'),str(args.builder.resolve())],env=env,capture_output=True,text=True,timeout=600)
   (HERE/'installed-driver.log').write_text(r.stdout+r.stderr);folder=Path(tmp)/'packages'
   if (folder/'results.json').exists():
    evidence=json.loads((folder/'results.json').read_text());installed=dict(status='PASS' if r.returncode==0 and all(x['status']=='PASS' for x in evidence['results']) else 'FAIL',driver_returncode=r.returncode,evidence=evidence,driver_sha256=hashlib.sha256(driver.read_bytes()).hexdigest())
    for name in ['base.log','extended.log','base-compile.log','extended-compile.log']:shutil.copyfile(folder/name,HERE/name)
   else:installed=dict(status='FAIL',driver_returncode=r.returncode,reason='No completed installed evidence; inspect installed-driver.log')
 sources=[dict(path=str(p.relative_to(BOOK)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [project,config,companion,next(CHAPTER.glob('5.13-*.md'))]]
 out=dict(python=platform.python_version(),platform=platform.platform(),problem_records=20,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),installed=installed,sources=sources,code_sha256=dict(core=hashlib.sha256(core_code.encode()).hexdigest(),configuration=hashlib.sha256(configuration_code.encode()).hexdigest()),checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','sources','installed','code_sha256')}));print('installed:',installed['status']);return bool(out['failed'] or installed['status']=='FAIL')
if __name__=='__main__':raise SystemExit(run())
