import ast,json,pathlib,re,subprocess,sys
src=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-20');out=pathlib.Path('/tmp/book1_ch20_01_13');out.mkdir(exist_ok=True);results=[]
for f in sorted(src.glob('20.*.md')):
 n=int(f.name.split('.')[1][:2])
 if not 1<=n<=13:continue
 blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())];code=next(x for x in blocks if 'unittest' in x and '__main__' in x);ast.parse(code);script=out/f'section_{n:02}.py';script.write_text(code);proc=subprocess.run([sys.executable,str(script)],cwd=out,text=True,capture_output=True,timeout=30);log=proc.stdout+proc.stderr;(out/f'section_{n:02}.log').write_text(log);m=re.search(r'Ran (\d+) tests? in',log);results.append({'section':f'20.{n}', 'source':str(f), 'test_count':int(m.group(1)) if m else None,'exit_code':proc.returncode,'result': 'PASS' if proc.returncode==0 and m else 'FAIL_OR_UNKNOWN','log':f'section_{n:02}.log'})
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
