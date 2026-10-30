"""Exact local layout/configuration/research workflows with retained artifacts."""
import hashlib,json,os,platform,re,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
CONFIG={9:dict(files={'financial_layout/__init__.py':0,'financial_layout/quantities.py':1,'financial_layout/__main__.py':2,'tests/test_layout.py':3},fixtures=['fixtures/holdings.json'],tests=['-m','unittest','discover','-s','tests','-v'],count=8,imports='import financial_layout,financial_layout.quantities,financial_layout.__main__'),10:dict(files={'configuration.py':0,'config_demo.py':1,'test_configuration.py':2},fixtures=['development.json'],tests=['-m','unittest','discover','-v'],count=8,imports='import configuration,config_demo'),11:dict(files={'research.py':0,'test_research.py':1},fixtures=['inflows.json','settings.json'],tests=['-m','unittest','discover','-v'],count=9,imports='import research')}
def digest(raw):return hashlib.sha256(raw).hexdigest()
def run():
 records=[];checks=[];env={k:v for k,v in os.environ.items() if k not in {'PYTHONPATH','PYTHONHOME','FINLAB_ENVIRONMENT','FINLAB_CURRENCY','FINLAB_DECIMAL_PLACES'}};env['PYTHONDONTWRITEBYTECODE']='1'
 def ck(label,actual,expected):checks.append(dict(label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 for n,cfg in CONFIG.items():
  source=next((BOOK/'chapter-05').glob(f'5.{n:02}-*.md'));text=source.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);jsons=re.findall(r'^```json\n(.*?)^```',text,re.M|re.S);files={path:blocks[index] for path,index in cfg['files'].items()};files.update(zip(cfg['fixtures'],jsons));operations=[]
  if n==9:
   for lang,name in [('markdown','README.md'),('gitignore','.gitignore')]:files[name]=re.findall(r'^```'+lang+r'\n(.*?)^```',text,re.M|re.S)[0]
  with tempfile.TemporaryDirectory(prefix=f'book1-research-{n}-') as tmp:
   folder=Path(tmp)
   for name,code in files.items():p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
   baseline={name:(folder/name).read_bytes() for name in files}
   def command(label,args,*,expected_stdout=None,expected_json=None,count=None,error=None,extra_env=None):
    r=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=folder,env=dict(env,**(extra_env or {})),capture_output=True,text=True,timeout=60);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
    if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
    else:
     if expected_stdout is not None:ok=ok and r.stdout==expected_stdout and r.stderr==''
     if expected_json is not None:
      try:ok=ok and json.loads(r.stdout)==expected_json and r.stderr==''
      except json.JSONDecodeError:ok=False
     if count is not None:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M)) and not re.search(r'skipped=',log)
    operations.append(dict(label=label,args=[str(x) for x in args],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,expected_error=error,expected_count=count,actual_count=actual,status='PASS' if ok else 'FAIL'))
   command('documented suite',cfg['tests'],count=cfg['count']);command('fresh quiet import',['-c',cfg['imports']],expected_stdout='')
   if n==9:
    for path in ['fixtures/holdings.json',folder/'fixtures/holdings.json']:
     command('local package explicit input',['-m','financial_layout','--input',path],expected_stdout='Active IDs: SEC-A, SEC-C\n')
    with tempfile.TemporaryDirectory(prefix='external-holdings-') as ext:
     path=Path(ext)/'holdings.json';path.write_bytes((folder/'fixtures/holdings.json').read_bytes());command('external absolute input, local package',['-m','financial_layout','--input',path],expected_stdout='Active IDs: SEC-A, SEC-C\n')
   if n==10:
    expected=dict(currency='EUR',decimal_places=2,environment='development',sources=dict(currency='cli',decimal_places='file',environment='file'));command('baseline precedence',['config_demo.py','--config','development.json','--currency','EUR'],expected_json=expected)
    expected=dict(currency='USD',decimal_places=2,environment='test',sources=dict(currency='file',decimal_places='file',environment='environment'));command('process override',['config_demo.py','--config','development.json'],expected_json=expected,extra_env={'FINLAB_ENVIRONMENT':'test'})
    command('unsupported decimal setting',['config_demo.py','--config','development.json','--decimal-places','3'],error='invalid decimal_places in cli');command('missing required config',['config_demo.py'],error='--config')
   if n==11:
    args=['research.py','--input','inflows.json','--config','settings.json','--output']
    for name in ['run-a.json','run-b.json']:command('documented experiment',args+[name],expected_stdout='')
    command('documented byte comparison',['-c',"from pathlib import Path;assert Path('run-a.json').read_bytes()==Path('run-b.json').read_bytes();print('Identical run artifacts')"],expected_stdout='Identical run artifacts\n')
    raw=(folder/'run-a.json').read_bytes();parsed=json.loads(raw);ck('known result',parsed['result'],dict(count=2,currency='USD',method='sum_then_round',rounding='ROUND_HALF_EVEN',total='30.01'))
    for field,name in [('input_sha256','inflows.json'),('config_sha256','settings.json'),('source_sha256','research.py')]:ck('artifact '+field,parsed['evidence'][field],digest(baseline[name]))
    command('existing artifact rejection',args+['run-a.json'],error='FileExistsError');ck('existing artifact unchanged',(folder/'run-a.json').read_bytes(),raw)
    (folder/'bad.json').write_text('[]');command('invalid input no report',['research.py','--input','bad.json','--config','settings.json','--output','invalid-output.json'],error='expected 1 to 1000 inflows');ck('invalid report absent',(folder/'invalid-output.json').exists(),False)
    probe="""
from fractions import Fraction
import json
from research import analyze
from decimal import localcontext,Inexact,ROUND_DOWN
from pathlib import Path
def cents(value):
 s=value*100;q,r=divmod(s.numerator,s.denominator);return q+int(2*r>s.denominator or (2*r==s.denominator and q%2==1))
config=Path('settings.json').read_bytes()
for amounts in [['10.005','20.005'],['0.005'],['0.015'],['1000000']*1000]:
 rows=[dict(id=str(i),currency='USD',amount=a) for i,a in enumerate(amounts)];expected=cents(sum(map(Fraction,amounts)));assert analyze(json.dumps(rows).encode(),config)['total']==f'{expected//100}.{expected%100:02d}'
with localcontext() as ctx:
 ctx.prec=2;ctx.rounding=ROUND_DOWN;ctx.traps[Inexact]=True
 assert analyze(Path('inflows.json').read_bytes(),config)['total']=='30.01'
 assert ctx.prec==2 and ctx.rounding==ROUND_DOWN and ctx.traps[Inexact]
"""
    command('supplemental rational/context assertions',['-c',probe],expected_stdout='')
    bundle=HERE/'research-bundle';bundle.mkdir(exist_ok=True)
    for name in ['research.py','test_research.py','inflows.json','settings.json','run-a.json','run-b.json']:shutil.copyfile(folder/name,bundle/name)
   ck(f'5.{n} supplied files unchanged',{name:(folder/name).read_bytes() for name in baseline},baseline)
  records.append(dict(section=f'5.{n}',source=str(source.relative_to(BOOK)),source_sha256=digest(source.read_bytes()),files=[dict(path=name,sha256=digest(code.encode())) for name,code in files.items()],operations=operations))
 operations=[op for rec in records for op in rec['operations']];out=dict(python=platform.python_version(),platform=platform.platform(),lab_records=3,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),artifact_predicates=len(checks),artifact_passed=sum(x['status']=='PASS' for x in checks),artifact_failed=sum(x['status']=='FAIL' for x in checks),existing_methods=sum(x['actual_count'] or 0 for x in operations),records=records,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('records','checks')}));return bool(out['command_failed'] or out['artifact_failed'])
if __name__=='__main__':raise SystemExit(run())
