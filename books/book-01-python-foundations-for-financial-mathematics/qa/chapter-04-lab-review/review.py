import ast,hashlib,json,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
NAMES=['structured_information_lab','lists_lab','tuples_lab','dictionaries_lab','sets_lab','nested_structures_lab']
def run():
 records=[]
 with tempfile.TemporaryDirectory(prefix='book1-ch4labs-') as root:
  for n,name in enumerate(NAMES,1):
   p=next((BOOK/'chapter-04').glob(f'4.{n:02}-*.md'));s=p.read_text();start=re.search(r'^## .*Hands-On Lab.*$',s,re.M).start();end=s.find('\n## ',start+1);section=s[start:end if end!=-1 else len(s)];codes=re.findall(r'^```python\n(.*?)^```',section,re.M|re.S);assert len(codes)==1
   work=Path(root)/name;work.mkdir();(work/(name+'.py')).write_text(codes[0]);tree=ast.parse(codes[0]);methods=[node.name for cls in tree.body if isinstance(cls,ast.ClassDef) for node in cls.body if isinstance(node,ast.FunctionDef) and node.name.startswith('test_')];assert len(methods)==6
   proc=subprocess.run([sys.executable,'-B','-m','unittest','-v',name],cwd=work,text=True,capture_output=True,timeout=20);ok=proc.returncode==0 and 'Ran 6 tests' in proc.stderr and 'OK' in proc.stderr and 'skipped' not in proc.stderr.lower()
   imported=subprocess.run([sys.executable,'-B','-c','import '+name],cwd=work,text=True,capture_output=True,timeout=10)
   records.append(dict(section=f'4.{n}',module=name,source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),section_sha256=hashlib.sha256(section.encode()).hexdigest(),code_sha256=hashlib.sha256(codes[0].encode()).hexdigest(),test_methods=methods,command=[sys.executable,'-B','-m','unittest','-v',name],exit_code=proc.returncode,stdout=proc.stdout,stderr=proc.stderr,suite_status='PASS' if ok else 'FAIL',import_status='PASS' if imported.returncode==0 and not imported.stdout and not imported.stderr else 'FAIL'))
 out=dict(python=sys.version,platform=platform.platform(),labs=len(records),existing_methods_rerun=36,new_unique_methods=0,verification_records=12,passed=sum(x[k]=='PASS' for x in records for k in ('suite_status','import_status')),failed=sum(x[k]=='FAIL' for x in records for k in ('suite_status','import_status')),records=records)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
