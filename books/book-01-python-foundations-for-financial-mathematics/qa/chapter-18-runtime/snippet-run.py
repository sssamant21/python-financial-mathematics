import pathlib, re, subprocess, sys
source = next(pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-18').glob('18.15-*.md'))
match = re.search(r'(?ms)^~~~python[^\n]*\n(.*?)^~~~\s*$', source.read_text())
if match is None:
    raise RuntimeError('reference snippet not found')
output = pathlib.Path('/tmp/book1_ch18_01_14')
output.mkdir(exist_ok=True)
script = output / 'section_15.py'
script.write_text(match.group(1))
result = subprocess.run([sys.executable, str(script)], cwd=output, text=True,
                        capture_output=True, timeout=30)
(output / 'section_15.log').write_text(result.stdout + result.stderr)
print(result.stdout, end='')
print(result.stderr, end='', file=sys.stderr)
raise SystemExit(result.returncode)
