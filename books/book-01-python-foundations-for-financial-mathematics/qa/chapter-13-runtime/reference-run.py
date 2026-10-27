import ast,json,pathlib,re,subprocess,sys
src=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-13');out=pathlib.Path('/tmp/book1_ch13_01_15');out.mkdir(exist_ok=True);results=[]
for f in sorted(src.glob('13.*.md')):
 n=int(f.name.split('.')[1][:2])
 if not 1<=n<=15:continue
 blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())];code=next(x for x in blocks if 'unittest' in x and '__main__' in x);ast.parse(code);module=f'section_{n:02}';(out/f'{module}.py').write_text(code);proc=subprocess.run([sys.executable,'-m','unittest','-v',module],cwd=out,text=True,capture_output=True,timeout=30);log=proc.stdout+proc.stderr;(out/f'{module}.log').write_text(log);m=re.search(r'Ran (\d+) tests? in',log);results.append({'section':f'13.{n}', 'source':str(f), 'test_count':int(m.group(1)) if m else None,'exit_code':proc.returncode,'result':'PASS' if proc.returncode==0 and m and re.search(r'(?m)^OK\s*$',log) else 'FAIL_OR_UNKNOWN','log':f'{module}.log'})
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
