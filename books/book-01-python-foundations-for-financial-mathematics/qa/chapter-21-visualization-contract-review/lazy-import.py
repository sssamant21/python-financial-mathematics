"""Block Matplotlib imports to exercise actual source dependency boundary."""
import sys,json,importlib.abc
from pathlib import Path
from datetime import datetime,timezone,timedelta
class BlockPlot(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname=='matplotlib' or fullname.startswith('matplotlib.'):raise ImportError('blocked optional plotting dependency')
block=BlockPlot();sys.meta_path.insert(0,block);rows=[]
try:
 import financial_toolkit as m
 rows.append(dict(case='core import without plotting dependency',passed='matplotlib' not in sys.modules))
 try:m.plot_price_series([],[],'X','USD','Raw');kind='returned'
 except Exception as e:kind=type(e).__name__
 rows.append(dict(case='invalid input rejected before plotting import',actual=kind,expected='ValueError',passed=kind=='ValueError'))
 t=datetime(2025,1,2,tzinfo=timezone.utc)
 try:m.plot_price_series([t,t+timedelta(days=1)],[1.,2.],'X','USD','Raw');kind='returned'
 except Exception as e:kind=type(e).__name__
 rows.append(dict(case='valid input requires optional plotting dependency',actual=kind,expected='ImportError',passed=kind=='ImportError'))
finally:sys.meta_path.remove(block)
d=dict(predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Source import hook blocks optional dependency;not package metadata/extras/clean-wheel or installation approval.');Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d));assert d['failed']==0
