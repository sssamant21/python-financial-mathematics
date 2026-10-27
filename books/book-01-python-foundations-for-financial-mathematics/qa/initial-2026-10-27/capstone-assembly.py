import re,pathlib
base=pathlib.Path('qa_snapshot/books/book-01-python-foundations-for-financial-mathematics/chapter-21')
out=pathlib.Path('/tmp/book1_capstone'); (out/'src/financial_toolkit').mkdir(parents=True,exist_ok=True);(out/'tests').mkdir(exist_ok=True);(out/'examples').mkdir(exist_ok=True)
def blocks(n):
 p=next(base.glob(f'21.{n:02d}-*.md'));s=p.read_text();return [(m.group(1),m.group(2)) for m in re.finditer(r'(?ms)^```([^\n]*)\n(.*?)^```\s*$',s)]
for n in range(5,15):
 b=blocks(n);py=[x[1] for x in b if x[0].strip()=='python'];
 if n in (5,6,7,8,9,10,11,12,13,14):
  names={5:'time_value',6:'cashflows',7:'loans',8:'bonds',9:'returns',10:'portfolio',11:'statistics',12:'simulation',13:'validation',14:'visualization'}
  (out/'src/financial_toolkit'/f'{names[n]}.py').write_text(py[0]);(out/'src/financial_toolkit/__init__.py').write_text(py[1]);
  test=next(x for x in py if 'unittest' in x and 'class ' in x)
  (out/'tests'/f'test_section_{n}.py').write_text(test)
for n in (15,17):
 py=[x[1] for x in blocks(n) if x[0].strip()=='python'];
 if n==17:(out/'examples/integrated_case.py').write_text(py[0])
 test=next(x for x in py if 'unittest' in x and 'class ' in x)
 (out/'tests'/f'test_section_{n}.py').write_text(test)
print('assembled',out)
