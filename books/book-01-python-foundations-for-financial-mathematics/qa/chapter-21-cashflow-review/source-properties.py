from pathlib import Path
import subprocess,sys,tempfile,re,importlib,json,math,hashlib
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3];pin='7d6add00a538b049ca8bdeedc8af508c32238221';base='books/book-01-python-foundations-for-financial-mathematics/chapter-21/';raw=[subprocess.check_output(['git','show',pin+':'+base+p],cwd=ROOT,text=True) for p in ['21.06-cash-flow-module.md','21.05-time-value-of-money-module.md']];cash,tvm=[re.findall(r'```python\n(.*?)\n```',s,re.S) for s in raw]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);p=t/'financial_toolkit';p.mkdir()
 for n,s in [('cashflows.py',cash[0]),('__init__.py',cash[1]),('time_value.py',tvm[0])]:(p/n).write_text(s)
 sys.path.insert(0,tmp);m=importlib.import_module('financial_toolkit');f=m.net_present_value
 rows=[dict(name='aligned additivity',passed=math.isclose(f([-150.,90.,90.],.1),f([-100.,60.,60.],.1)+f([-50.,30.,30.],.1),rel_tol=5e-13,abs_tol=1e-10)),dict(name='positive future monotonicity',passed=f([0.,100.],.05)>f([0.,100.],.1)),dict(name='mixed-sign reverse direction',passed=f([100.,-110.],.05)<f([100.,-110.],.1))]
 d=dict(source_revision=pin,source_sha256=[hashlib.sha256(s.encode()).hexdigest() for s in raw],source_predicates=rows,limits='Three selected source properties,separate from62wheelpredicates;notinstalled-artifactexecution orall-range modelproof.')
(OUT/'source-properties.json').write_text(json.dumps(d,indent=2)+'\n');assert all(x['passed'] for x in rows);print('3selectedsourcepropertychecks pass')
