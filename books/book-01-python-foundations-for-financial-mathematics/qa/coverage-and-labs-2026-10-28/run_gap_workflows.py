"""Execute reviewed uncovered workflows; no manuscript code rewriting."""
import hashlib,json,os,pathlib,subprocess,sys
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
if out.exists(): raise SystemExit('Use a new output directory')
out.mkdir(parents=True); parser=MarkdownIt(); results=[]
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env.update(MPLBACKEND='Agg',PYTHONDONTWRITEBYTECODE='1')
def section(ch,n):return next((root/f'chapter-{ch:02}').glob(f'{ch}.{n:02}-*.md'))
def extract(ch,n):
 f=section(ch,n);return f,[t for t in parser.parse(f.read_text()) if t.type=='fence' and t.info.strip()=='python']
def write(p,code):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
def run(name,sources,files,oracle,prepare=None,args=None):
 folder=out/name;folder.mkdir();refs=[]
 for (ch,n,idx),target in sources:
  f,blocks=extract(ch,n);t=blocks[idx];write(folder/target,t.content);refs.append({'source':str(f.relative_to(root)),'python_block_index':idx,'line':t.map[0]+1,'code_sha256':hashlib.sha256(t.content.encode()).hexdigest(),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'target':target})
 for target,text in files.items():write(folder/target,text)
 if prepare:prepare(folder)
 command=[sys.executable,'-W','error::FutureWarning',*(args or ['check.py'])]
 try:
  p=subprocess.run(command,cwd=folder,env=env,capture_output=True,text=True,timeout=45); stdout=p.stdout;stderr=p.stderr;code=p.returncode
 except subprocess.TimeoutExpired as e:stdout=str(e.stdout or '');stderr=str(e.stderr or '');code=None
 write(folder/'stdout.log',stdout);write(folder/'stderr.log',stderr)
 passed=code==0 and not stderr and oracle(stdout,folder)
 record={'workflow':name,'sources':refs,'command':command,'returncode':code,'status':'PASS' if passed else 'FAIL','stdout':name+'/stdout.log','stderr':name+'/stderr.log'}
 results.append(record);print(name,record['status'],flush=True)
# Source-provided CSV fixture, then variant with BOM and a quoted comma.
f=section(19,2);csv=next(t.content for t in parser.parse(f.read_text()) if t.type=='fence' and t.info.strip()=='csv')
for name,fixture,expected in [('csv-read',csv,[{'instrument':'EXAMPLE','date':'2026-01-05','close':'100.00','currency':'USD'},{'instrument':'EXAMPLE','date':'2026-01-06','close':'101.50','currency':'USD'}]),('csv-bom-quoted','\ufeffinstrument,date,close,currency\n"EXAMPLE, A",2026-01-05,100.00,USD\n',[{'instrument':'EXAMPLE, A','date':'2026-01-05','close':'100.00','currency':'USD'}])]:
 run(name,[((19,2,0),'example.py')],{'prices.csv':fixture,'check.py':'import example\nassert example.rows == '+repr(expected)+'\nprint("CSV rows match controlled fixture")\n'},lambda s,p:s=='CSV rows match controlled fixture\n')
run('csv-write',[((19,2,1),'example.py')],{'check.py':'import example,csv\nfrom pathlib import Path\nwith open("output.csv",newline="",encoding="utf-8") as f:\n reader=csv.DictReader(f); assert reader.fieldnames==["instrument","close"]; assert list(reader)==[{"instrument":"EXAMPLE","close":"101.50"}]\nprint("CSV output matches")\n'},lambda s,p:s=='CSV output matches\n')
def workbook(folder):
 from openpyxl import Workbook
 w=Workbook();w.active.title='Prices';w.active.append(['instrument','date','close','currency']);w.active.append(['EXAMPLE','2026-01-05',100,'USD']);w.save(folder/'prices.xlsx');w.close()
run('excel-read',[((19,4,0),'example.py')],{},lambda s,p:s=="('instrument', 'date', 'close', 'currency')\n('EXAMPLE', '2026-01-05', 100, 'USD')\n",workbook,args=['example.py'])
run('assertion-benchmark',[((20,2,0),'example.py')],{},lambda s,p:s=='',args=['example.py'])
run('decimal-construction',[((20,6,0),'example.py')],{},lambda s,p:s=='0.1\n0.1000000000000000055511151231257827021181583404541015625\n',args=['example.py'])
run('type-hint-example',[((20,11,0),'example.py')],{'check.py':'from example import simple_return\nimport math\nassert math.isclose(simple_return(100.0,105.0),.05,abs_tol=1e-14)\nassert simple_return.__annotations__ == {"start":float,"end":float,"return":float}\nprint("Annotated function known-value check passed")\n'},lambda s,p:s=='Annotated function known-value check passed\n')
run('finlib-example',[((20,15,0),'finlib/__init__.py'),((20,15,1),'finlib/valuation.py'),((20,15,2),'example.py')],{},lambda s,p:s=='NPV: 4.132231\n',args=['example.py'])
# Exact scaffold, rather than the later Section 21.5 module used in initial assembly.
run('toolkit-scaffold-example',[((21,3,0),'financial_toolkit/__init__.py'),((21,3,1),'financial_toolkit/time_value.py'),((21,3,2),'example.py')],{},lambda s,p:s=='PV: 100.00 payment units\n',args=['example.py'])
run('toolkit-scaffold-tests',[((21,3,0),'financial_toolkit/__init__.py'),((21,3,1),'financial_toolkit/time_value.py'),((21,3,3),'test_scaffold.py')],{'check.py':'import unittest,test_scaffold\nsuite=unittest.defaultTestLoader.loadTestsFromModule(test_scaffold)\nassert suite.countTestCases()==12\nresult=unittest.TextTestRunner(stream=__import__("sys").stdout,verbosity=2).run(suite)\nassert result.wasSuccessful() and not result.skipped\n'},lambda s,p:'Ran 12 tests' in s and '\nOK\n' in s)
for ch,n,module,expected in [(21,1,'architecture','PV: 100.00 USD; model=pv-one-v1\n'),(21,2,'requirements','Ready for review: False\n')]:
 run(module+'-demo',[((ch,n,0),'example.py')],{},lambda s,p,e=expected:s==e,args=['example.py'])
expected_digest=hashlib.sha256(b'{"command":"not executed","python":"record actual version","revision":"synthetic-revision","status":"not_run"}').hexdigest()+'\n'
run('metadata-demo',[((21,16,0),'example.py')],{},lambda s,p:s==expected_digest,args=['example.py'])
(out/'results.json').write_text(json.dumps({'python':sys.version,'source_revision':'a4aebd6d937a97dd5ed3f6b6cbb947fb5f58e76f','results':results},indent=2)+'\n')
if any(r['status']!='PASS' for r in results):sys.exit(1)
