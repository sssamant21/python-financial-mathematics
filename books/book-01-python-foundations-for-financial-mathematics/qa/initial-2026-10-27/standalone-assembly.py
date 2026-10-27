import pathlib,re
base=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-21');out=pathlib.Path('/tmp/book1_capstone')
def py(n):
 s=next(base.glob(f'21.{n:02d}-*.md')).read_text();return [m.group(1) for m in re.finditer(r'(?ms)^```python[^\n]*\n(.*?)^```\s*$',s)]
for n,name in [(1,'capstone_architecture'),(2,'requirements_check'),(4,'numerical_policy'),(16,'run_metadata')]:
 parts=py(n);(out/f'{name}.py').write_text(parts[0]);test=next(x for x in parts if 'unittest' in x and 'class ' in x);(out/'tests'/f'test_section_{n}.py').write_text(test)
parts=py(18);(out/'tests/test_section_18.py').write_text(next(x for x in parts if 'unittest' in x and 'class ' in x))
parts=py(3);(out/'tests/test_section_3.py').write_text(next(x for x in parts if 'unittest' in x and 'class ' in x))
print('assembled standalone sections')
