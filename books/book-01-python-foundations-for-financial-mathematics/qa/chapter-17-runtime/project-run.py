import pathlib,re,subprocess,sys
src=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-17');out=pathlib.Path('/tmp/book1_ch17_01_14');out.mkdir(exist_ok=True)
f=next(src.glob('17.14-*.md'));blocks=[m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
(out/'financial_solver.py').write_text(blocks[0]);(out/'test_financial_solver.py').write_text(blocks[1]);p=subprocess.run([sys.executable,'-m','unittest','-v','test_financial_solver'],cwd=out,text=True,capture_output=True,timeout=30);(out/'section_14.log').write_text(p.stdout+p.stderr);print('section 17.14 exit',p.returncode);print((p.stdout+p.stderr)[-800:]);raise SystemExit(p.returncode)
