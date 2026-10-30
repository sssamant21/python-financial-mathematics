"""Exact flat-layout baseline plus explicit no-overwrite output and nested-test copy."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=next((BOOK/'chapter-05').glob('5.09-*.md'))
TEXT=SOURCE.read_text();BLOCKS=re.findall(r'^```python\n(.*?)^```',TEXT,re.M|re.S)
M=types.ModuleType('original_layout_quantities');exec(compile(BLOCKS[1],str(SOURCE),'exec'),M.__dict__)
NESTED='''import unittest
from financial_layout.quantities import active_ids

class NestedLayoutTests(unittest.TestCase):
    def test_no_active_holdings(self):
        self.assertEqual(active_ids([dict(security_id='ZERO',quantity='0')]),())

    def test_id_and_top_level_rejections(self):
        for sid,exception in [(' A',ValueError),(1,TypeError)]:
            with self.subTest(sid=sid),self.assertRaises(exception):
                active_ids([dict(security_id=sid,quantity='0')])
        with self.assertRaises(TypeError):
            active_ids({})
'''
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run():
 checks=[];operations=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,kind,fn):
  try:fn();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'source rejection',actual,kind)
 for sid,kind in [(' A','ValueError'),('A ','ValueError'),(1,'TypeError')]:err('5.9-E2',kind,lambda sid=sid:M.active_ids([dict(security_id=sid,quantity='0')]))
 for value in [{},None,'not-list']:err('5.9-E2','TypeError',lambda value=value:M.active_ids(value))
 files=dict(zip(['financial_layout/__init__.py','financial_layout/quantities.py','financial_layout/__main__.py','tests/test_layout.py'],BLOCKS));files['fixtures/holdings.json']=re.findall(r'^```json\n(.*?)^```',TEXT,re.M|re.S)[0]
 with tempfile.TemporaryDirectory(prefix='layout-exercises-') as tmp:
  folder=Path(tmp);outside=folder/'outside';outside.mkdir()
  for name,code in files.items():p=folder/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
  before={name:sha((folder/name).read_bytes()) for name in files}
  def command(label,args,*,stdout=None,count=None,error=None,cwd=None):
   r=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=cwd or folder,env=env,capture_output=True,text=True,timeout=30);log=r.stdout+r.stderr;counts=re.findall(r'Ran (\d+) tests? in',log);actual=int(counts[0]) if len(counts)==1 else None;ok=r.returncode==0
   if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
   if stdout is not None:ok=ok and (r.stdout,r.stderr)==(stdout,'')
   if count:ok=ok and actual==count and bool(re.search(r'^OK\s*$',log,re.M))
   operations.append(dict(label=label,args=[str(x) for x in args],cwd=str(cwd or folder),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_method_count=actual,expected_error=error,status='PASS' if ok else 'FAIL'));return r
  command('exact original eight-method suite',['-m','unittest','discover','-s','tests','-v'],count=8)
  zero=folder/'fixtures/no-active.json';zero.write_text('[{"security_id":"ZERO-A","quantity":"0"},{"security_id":"ZERO-B","quantity":"0.0000"}]');zero_before=zero.read_bytes();command('E1 exact empty-active stdout',['-m','financial_layout','--input',zero],stdout='Active IDs: \n')
  for name,value,error in [('padded',[dict(security_id=' A',quantity='0')],'ValueError'),('numeric',[dict(security_id=1,quantity='0')],'TypeError'),('not-list',{},'TypeError')]:
   bad=folder/(name+'.json');bad.write_text(json.dumps(value));command('E2 CLI '+name,['-m','financial_layout','--input',bad],error=error)
  original=files['financial_layout/__main__.py'];needle='    parser.add_argument("--input", type=Path, required=True)\n';display='    print("Active IDs: " + ", ".join(ids))\n';assert original.count(needle)==original.count(display)==1
  extended=original.replace(needle,needle+'    parser.add_argument("--output", type=Path, help="Exclusive UTF-8 output file; never overwrite")\n').replace(display,'    message = "Active IDs: " + ", ".join(ids)\n    if args.output is None:\n        print(message)\n    else:\n        with args.output.open("x", encoding="utf-8", newline="\\n") as stream:\n            stream.write(message + "\\n")\n')
  (folder/'financial_layout/__main__.py').write_text(extended)
  output=folder/'report.txt';command('E3 new exclusive output option',['-m','financial_layout','--input','fixtures/holdings.json','--output',output],stdout='');raw=output.read_bytes();ck('5.9-E3','known output file bytes',raw,b'Active IDs: SEC-A, SEC-C\n')
  command('E3 existing-output failure',['-m','financial_layout','--input','fixtures/holdings.json','--output',output],error='FileExistsError');ck('5.9-E3','existing output unchanged',output.read_bytes(),raw)
  source=folder/'fixtures/holdings.json';command('E3 input cannot be overwritten',['-m','financial_layout','--input',source,'--output',source],error='FileExistsError');ck('5.9-E3','input bytes unchanged',sha(source.read_bytes()),before['fixtures/holdings.json'])
  invalid=folder/'invalid.json';invalid.write_text('[]wrong-json');no_output=folder/'invalid-report.txt';command('E3 invalid input before output creation',['-m','financial_layout','--input',invalid,'--output',no_output],error='JSONDecodeError');ck('5.9-E3','invalid-input output absent',no_output.exists(),False)
  (folder/'tests/__init__.py').write_text('');(folder/'tests/nested').mkdir();(folder/'tests/nested/__init__.py').write_text('');(folder/'tests/nested/test_extra.py').write_text(NESTED)
  nested=command('E5 explicit regular nested-test discovery',['-m','unittest','discover','-s','tests','-t','.','-v'],count=10);ck('5.9-E5','fully qualified nested cases found','tests.nested.test_extra.NestedLayoutTests' in nested.stderr,True)
  command('E6 absolute input does not install package',['-I','-m','financial_layout','--input',source],cwd=outside,error='No module named financial_layout')
  ck('5.9-E3','second input fixture unchanged',zero.read_bytes(),zero_before);ck('all','original core/test/fixture unchanged',{name:sha((folder/name).read_bytes()) for name in files if name!='financial_layout/__main__.py'},{name:digest for name,digest in before.items() if name!='financial_layout/__main__.py'})
  # Retain synthetic new fixture and supplemental source/test copies, not an installed distribution.
  supplements={'financial_layout/__main__.py':extended,'tests/__init__.py':'','tests/nested/__init__.py':'','tests/nested/test_extra.py':NESTED,'fixtures/no-active.json':zero.read_text()}
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=8,source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),original_files=[dict(path=name,sha256=sha(code.encode())) for name,code in files.items()],supplemental_files=supplements,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),source_method_invocations=sum(len(re.findall(r'^test_\w+ \([^)]*\.LayoutTests\.\w+\)',x['stderr'],re.M)) for x in operations),supplemental_nested_method_invocations=sum(len(re.findall(r'^test_\w+ \([^)]*\.NestedLayoutTests\.\w+\)',x['stderr'],re.M)) for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),operations=operations,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('operations','checks','original_files','supplemental_files')}));return bool(out['command_failed'] or out['failed'])
if __name__=='__main__':raise SystemExit(run())
