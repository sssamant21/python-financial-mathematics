"""Exact source workflows plus independently specified contract probes."""
import ast,copy,hashlib,json,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from decimal import Decimal as D
from datetime import date
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
NAMES=['comprehensions_lab','sorting_filtering_lab','cash_flow_schedule_lab','securities_portfolios_lab','immutability_lab','data_structure_choice_lab']

def run():
 records=[];checks=[];mods={}
 def ck(section,label,actual,expected):checks.append(dict(section=section,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(section,label,expected,call):
  try:call();actual='no exception'
  except Exception as exc:actual=type(exc).__name__
  ck(section,label,actual,expected)
 with tempfile.TemporaryDirectory(prefix='book1-ch4-workflows-') as tmp:
  for n,name in enumerate(NAMES,7):
   path=next((BOOK/'chapter-04').glob(f'4.{n:02}-*.md'));s=path.read_text();m=re.search(r'^## .*Complete Runnable Lab.*$',s,re.M);assert m;end=s.find('\n## ',m.end());section=s[m.start():end];code=re.findall(r'^```python\n(.*?)^```',section,re.M|re.S);assert len(code)==1
   work=Path(tmp)/name;work.mkdir();(work/(name+'.py')).write_text(code[0]);tree=ast.parse(code[0]);methods=[f.name for cls in tree.body if isinstance(cls,ast.ClassDef) for f in cls.body if isinstance(f,ast.FunctionDef) and f.name.startswith('test_')];assert len(methods)==7
   p=subprocess.run([sys.executable,'-B',name+'.py'],cwd=work,text=True,capture_output=True,timeout=20);ck(n,'published direct command',p.returncode,0);ck(n,'seven methods and no skips','Ran 7 tests' in p.stderr and 'OK' in p.stderr and 'skipped' not in p.stderr.lower(),True)
   imported=subprocess.run([sys.executable,'-B','-c','import '+name],cwd=work,text=True,capture_output=True,timeout=10);ck(n,'silent import',(imported.returncode,imported.stdout,imported.stderr),(0,'',''))
   mod=types.ModuleType(name);exec(compile(code[0],str(path),'exec'),mod.__dict__);mods[n]=mod
   records.append(dict(section=n,module=name,source=str(path.relative_to(BOOK)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code[0].encode()).hexdigest(),test_methods=methods,command=[sys.executable,'-B',name+'.py'],exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
  m=mods[7];source=m.sample_positions();before=copy.deepcopy(source);rows,lookup=m.build_active_views(source);ck(7,'active source order',[r['instrument_id'] for r in rows],['BOND-A','ETF-B']);ck(7,'zero deliberately excluded',list(lookup),['BOND-A','ETF-B']);rows[0]['quantity']=D(99);ck(7,'fresh output records',source,before);err(7,'duplicate zero ID rejected','ValueError',lambda:m.build_active_views(source+[{'instrument_id':'CASH-RESERVE','quantity':D(0)}]))
  m=mods[8];source=m.sample_positions();report=m.ranked_positions(source,currency='USD',minimum=D(100),limit=3);ck(8,'value descending ID ascending',[r['position_id'] for r in report],['BETA','ALPHA','ZETA']);ck(8,'filter before limit',[r['position_id'] for r in m.ranked_positions(list(reversed(source)),currency='USD',minimum=D(100),limit=2)],['BETA','ALPHA']);bad=copy.deepcopy(source);bad[1]['market_value']=D('NaN');err(8,'excluded currency still validated','ValueError',lambda:m.ranked_positions(bad,currency='USD',minimum=D(100),limit=0))
  m=mods[9];source=m.sample_schedule();saved=copy.deepcopy(source);normal,groups=m.normalize_schedule(source);ck(9,'canonical event order',[r['event_id'] for r in normal['events']],['E-0','E-1','E-2','E-3']);ck(9,'same date preserves both events',[r['event_id'] for r in groups[date(2028,1,15)]],['E-2','E-3']);normal['events'][0]['amount']=D(99);ck(9,'independent grouped output',groups[date(2027,1,15)][0]['amount'],D(-1000));ck(9,'source preserved',source,saved)
  m=mods[10];catalog=m.sample_catalog();source=m.sample_portfolio();result=m.enrich_portfolio(catalog,source);ck(10,'source holdings order',[r['security_id'] for r in result['holdings']],['SEC-B','SEC-A']);ck(10,'zero resolves catalog currency',(result['holdings'][0]['quantity'],result['holdings'][0]['quote_currency']),(D(0),'EUR'));bad=copy.deepcopy(catalog)+[{'security_id':'UNUSED','name':'Unused','quote_currency':'GBP'}];err(10,'unused invalid catalog rejected','ValueError',lambda:m.enrich_portfolio(bad,source))
  m=mods[11];source=m.sample_holdings();snapshot=m.capture_holdings(source);revised=m.replace_quantity(snapshot,'SEC-A',D(20));ck(11,'immutable capture',snapshot,(('SEC-B',D(0)),('SEC-A',D('12.5'))));ck(11,'absolute replacement',revised,(('SEC-B',D(0)),('SEC-A',D(20))));source[0]['quantity']=D(99);ck(11,'capture unaffected by source edit',snapshot[0],('SEC-B',D(0)));err(11,'invalid later snapshot prevents replacement','TypeError',lambda:m.replace_quantity((('SEC-A',D(1)),('BAD',True)),'SEC-A',D(2)))
  m=mods[12];source=m.sample_holdings();snapshot,lookup,members=m.build_views(source);lookup['SEC-A']=D(99);lookup['NEW']=D(1);ck(12,'snapshot and membership immutable',(snapshot,members),((('SEC-B',D(0)),('SEC-A',D('12.5'))),frozenset(['SEC-A','SEC-B'])));source.append({'security_id':'SEC-C','quantity':D(3)});rebuilt=m.build_views(source);ck(12,'new source version rebuild',rebuilt[2],frozenset(['SEC-A','SEC-B','SEC-C']));ck(12,'old membership retained',members,frozenset(['SEC-A','SEC-B']));ck(12,'empty outputs',m.build_views([]),((),{},frozenset()))
 output=dict(python=sys.version,platform=platform.platform(),workflow_records=6,existing_methods_rerun=42,new_unique_methods=0,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),workflows=records,checks=checks)
 (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('checks','workflows')},indent=2));return bool(output['failed'])
if __name__=='__main__':raise SystemExit(run())
