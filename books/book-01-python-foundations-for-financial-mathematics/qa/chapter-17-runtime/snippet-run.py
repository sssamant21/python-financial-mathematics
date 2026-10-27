import pathlib,re,subprocess,sys
src=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-17');out=pathlib.Path('/tmp/book1_ch17_01_14');out.mkdir(exist_ok=True)
f=next(src.glob('17.15-*.md'));m=re.search(r'(?ms)^~~~python[^\n]*\n(.*?)^~~~\s*$',f.read_text());
if m is None: raise RuntimeError('snippet not found')
script=out/'section_15.py';script.write_text(m.group(1));p=subprocess.run([sys.executable,str(script)],cwd=out,text=True,capture_output=True,timeout=30);(out/'section_15.log').write_text(p.stdout+p.stderr);print('section 17.15 exit',p.returncode);print(p.stdout+p.stderr);raise SystemExit(p.returncode)
