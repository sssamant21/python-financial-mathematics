"""Reproduce source lab commands and deliberate failure exercises in temporary copies."""
import hashlib,json,os,re,subprocess,sys,tempfile,platform
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
FILES={4:'return_values_lab.py',5:'default_keyword_arguments_lab.py',6:'variable_scope_lab.py',7:'type_hints_lab.py',8:'docstrings_lab.py',9:'pv_fv_lab.py',10:'rate_discounting_lab.py',11:'composition_lab.py',12:'reproducibility_lab.py',13:'test_financial_functions.py'}


def run():
 records=[];labs=[];sources={}
 def command(label,args,cwd,expected_exit=0,fragment=None):
  proc=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=40,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
  ok=proc.returncode==expected_exit and (fragment is None or fragment in proc.stdout+proc.stderr)
  records.append(dict(label=label,command=[str(x) for x in args],expected_exit=expected_exit,expected_fragment=fragment,actual_exit=proc.returncode,stdout=proc.stdout,stderr=proc.stderr,status='PASS' if ok else 'FAIL'))
  return proc
 with tempfile.TemporaryDirectory(prefix='ch03-labs-') as temp:
  root=Path(temp)
  for n,name in FILES.items():
   path=next((BOOK/'chapter-03').glob(f'3.{n:02}-*.md'));text=path.read_text();m=re.search(r'^## .*Hands-On Lab.*$',text,re.M);end=text.find('\n## ',m.end());section=text[m.start():end if end!=-1 else len(text)]
   codes=re.findall(r'^```python\n(.*?)^```',section,re.M|re.S);assert len(codes)==1
   expected=re.findall(r'^```text\n(.*?)^```',section,re.M|re.S);assert len(expected)==1
   work=root/str(n);work.mkdir();(work/name).write_text(codes[0]);sources[n]=(codes[0],path,section)
   if n==13:(work/FILES[12]).write_text(sources[12][0])
   args=[sys.executable,name] if n!=13 else [sys.executable,'-m','unittest','-v','test_financial_functions']
   proc=command(f'3.{n} direct command',args,work,fragment='Ran 12 tests' if n==13 else expected[0])
   if n!=13:
    records.append(dict(label=f'3.{n} exact documented stdout',expected=expected[0],actual=proc.stdout,status='PASS' if proc.stdout==expected[0] and not proc.stderr else 'FAIL'))
   if 8<=n<=12:command(f'3.{n} explicit doctest',[sys.executable,'-m','doctest','-v',name],work,fragment='Test passed.')
   labs.append(dict(section=f'3.{n}',filename=name,source=str(path.relative_to(BOOK)),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),lab_section_sha256=hashlib.sha256(section.encode()).hexdigest(),code_sha256=hashlib.sha256(codes[0].encode()).hexdigest(),expected_stdout=expected[0],prerequisites='Section3.12 reproducibility_lab.py beside test module' if n==13 else 'Python3.10+ standard library; ambient Decimal for 3.4–3.11, fixed context in 3.12',status='PASS_SCOPED'))
  # Static fixture is checked only; never executed as runtime code.
  checker=os.environ.get('CH3_MYPY_PYTHON',sys.executable)
  command('mypy version',[checker,'-m','mypy','--version'],root)
  work=root/'7';command('typed lab strict',[checker,'-m','mypy','--strict',FILES[7]],work)
  full=sources[7][1].read_text();m=full.index('## 3.7.16');end=full.index('## 3.7.17');bad=re.findall(r'^```python\n(.*?)^```',full[m:end],re.M|re.S);assert len(bad)==1
  (work/'type_hints_bad_calls.py').write_text(bad[0]);command('deliberate bad static calls',[checker,'-m','mypy','--strict','type_hints_bad_calls.py'],work,1,'Found 3 errors')
  command('testing lab strict',[checker,'-m','mypy','--strict',FILES[12],FILES[13]],root/'13')
  # Real doctest failure, restored exact code, then misleading prose that examples cannot detect.
  work=root/'8';original=sources[8][0];assert '\n    True\n' in original
  (work/FILES[8]).write_text(original.replace('\n    True\n','\n    False\n',1))
  command('documentation expectation defect',[sys.executable,'-m','doctest','-v',FILES[8]],work,1,'1 failed')
  (work/FILES[8]).write_text(original);command('documentation restored',[sys.executable,'-m','doctest','-v',FILES[8]],work,fragment='Test passed.')
  misleading=original.replace('No intermediate contributions, withdrawals, fees, taxes, inflation','Beginning-of-period contributions are supported.\n    No withdrawals, fees, taxes, inflation',1);assert misleading!=original
  (work/FILES[8]).write_text(misleading);command('unsupported prose remains invisible to doctests',[sys.executable,'-m','doctest','-v',FILES[8]],work,fragment='Test passed.')
  (work/FILES[8]).write_text(original)
  # Run the published suite against a single formula defect, then restore and rerun.
  work=root/'13';original=sources[12][0];needle='result = future_amount / growth';assert original.count(needle)==1
  (work/FILES[12]).write_text(original.replace(needle,'result = future_amount * growth'))
  command('valuation mutation suite failure',[sys.executable,'-m','unittest','-v','test_financial_functions'],work,1,'FAIL: test_known_values')
  (work/FILES[12]).write_text(original)
  # Avoid timestamp/size bytecode reuse after rapid restore by suppressing stale caches.
  for path in work.glob('__pycache__/*.pyc'):path.unlink()
  command('valuation restored suite',[sys.executable,'-m','unittest','-v','test_financial_functions'],work,fragment='OK')
  command('isolated known-value method',[sys.executable,'-m','unittest','-v','test_financial_functions.TestPresentValue.test_known_values'],work,fragment='Ran 1 test')
 output=dict(source_revision='61e4e27d1d05d7aa60e8b2ca0cdba853d1e67cd3',python=sys.version,platform=platform.platform(),labs=len(labs),verification_records=len(records),passed=sum(r['status']=='PASS' for r in records),failed=sum(r['status']=='FAIL' for r in records),lab_register=labs,records=records)
 (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('lab_register','records')},indent=2));return bool(output['failed'])

if __name__=='__main__':raise SystemExit(run())
