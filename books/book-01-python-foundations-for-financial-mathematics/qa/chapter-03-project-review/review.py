import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-03/3.14-chapter-project-financial-mathematics-function-library.md'

def run():
 text=SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S);assert len(blocks)==3
 names=['financial_functions.py','test_function_library.py','demo_function_library.py'];records=[]
 def command(label,args,where,exit=0,fragment=None,exact=None):
  p=subprocess.run(args,cwd=where,text=True,capture_output=True,timeout=30,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));ok=p.returncode==exit and (fragment is None or fragment in p.stdout+p.stderr) and (exact is None or p.stdout==exact)
  records.append(dict(label=label,command=args,expected_exit=exit,expected_fragment=fragment,expected_stdout=exact,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,status='PASS' if ok else 'FAIL'))
 with tempfile.TemporaryDirectory(prefix='ch3-project-') as work:
  work=Path(work)
  for name,code in zip(names,blocks):(work/name).write_text(code)
  command('full published suite',[sys.executable,'-B','-m','unittest','-v','test_function_library'],work,fragment='Ran 12 tests')
  expected='Monthly effective rate: 1.00%\nEffective annual rate: 12.682503%\nFuture value: 1126.83\nRecovered present value: 1000.00\n'
  command('exact demo',[sys.executable,'-B','demo_function_library.py'],work,exact=expected)
  command('silent import',[sys.executable,'-B','-c','import financial_functions'],work,exact='')
  checker=os.environ.get('CH3_MYPY_PYTHON',sys.executable)
  command('checker version',[checker,'-m','mypy','--version'],work)
  command('all three strict',[checker,'-m','mypy','--strict',*names],work,fragment='Success: no issues found')
  needle='result = future_amount / _growth(periodic_rate, periods)';assert blocks[0].count(needle)==1
  (work/names[0]).write_text(blocks[0].replace(needle,'result = future_amount * _growth(periodic_rate, periods)'))
  command('temporary formula defect',[sys.executable,'-B','-m','unittest','-v','test_function_library'],work,1,fragment='FAIL')
  (work/names[0]).write_text(blocks[0]);command('restored suite',[sys.executable,'-B','-m','unittest','-v','test_function_library'],work,fragment='OK')
 out=dict(python=sys.version,platform=platform.platform(),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),extracted_files=[dict(name=n,sha256=hashlib.sha256(c.encode()).hexdigest()) for n,c in zip(names,blocks)],records=records,passed=sum(r['status']=='PASS' for r in records),failed=sum(r['status']=='FAIL' for r in records))
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('records','extracted_files')},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
