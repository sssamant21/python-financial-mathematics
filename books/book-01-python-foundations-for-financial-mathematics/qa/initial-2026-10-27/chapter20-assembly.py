import re,pathlib
src=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-20');out=pathlib.Path('/tmp/book1_ch20');(out/'finlib').mkdir(parents=True,exist_ok=True);(out/'tests').mkdir(exist_ok=True)
def get(n):
 s=next(src.glob(f'20.{n:02d}-*.md')).read_text();return [m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',s)]
(out/'tests/test_2014.py').write_text(get(14)[0]);b=get(15);(out/'finlib/__init__.py').write_text(b[0]);(out/'finlib/valuation.py').write_text(b[1]);(out/'tests/test_2015.py').write_text(b[3]);(out/'tests/test_2016.py').write_text(get(16)[0]);print('assembled chapter 20 sections 14–16')
