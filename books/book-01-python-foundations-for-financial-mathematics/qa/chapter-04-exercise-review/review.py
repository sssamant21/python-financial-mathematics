"""Exact Chapter4 source extraction with independent representation/ownership fixtures."""
import contextlib,copy,hashlib,importlib.util,io,json,platform,re,subprocess,sys,tempfile
from pathlib import Path
from datetime import date,datetime
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
PROJECT=BOOK/'chapter-04/4.13-chapter-project-portfolio-holdings-manager.md'
COMP=BOOK/'chapter-04/solutions/4.14-solutions-and-reference-implementations.md'

def run():
 checks=[];runs=[]
 def ck(ex,label,actual,expected):checks.append(dict(exercise=ex,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(ex,label,expected,call):
  try:call();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(ex,label,actual,expected)
 project=re.findall(r'^```python\n(.*?)^```',PROJECT.read_text(),re.M|re.S);comp=re.findall(r'^```python\n(.*?)^```',COMP.read_text(),re.M|re.S);assert len(comp)==1
 with tempfile.TemporaryDirectory(prefix='book1-ch4-') as tmp:
  tmp=Path(tmp);(tmp/'portfolio_holdings_manager.py').write_text(project[0]);(tmp/'chapter04_solutions.py').write_text(comp[0]);sys.path.insert(0,str(tmp))
  import portfolio_holdings_manager as manager
  import chapter04_solutions as s
  original=[{'security_id':'A','quantity':1}];other=original;other[0]['quantity']=2;other=[];ck(2,'mutation then rebinding',(original,other),([{'security_id':'A','quantity':2}],[]))
  shallow=({'quantity':1},);shallow[0]['quantity']=2;ck(3,'tuple descendant mutable',shallow[0]['quantity'],2)
  pairs=[('A',D(1)),('A',D(2)),('B',D(0))];ck(4,'duplicate dictionary result',dict(pairs),{'A':D(2),'B':D(0)});ck(4,'membership loses multiplicity',set(sid for sid,_ in pairs),{'A','B'})
  fixture=[{'security_id':'SEC-B','quantity':D(0)},{'security_id':'SEC-A','quantity':D('12.5')},{'security_id':'SEC-C','quantity':D(3)}];baseline=copy.deepcopy(fixture)
  expected=(('SEC-B',D(0)),('SEC-A',D('12.5')),('SEC-C',D(3)))
  ck(7,'immutable ordered capture',s.capture(fixture),expected)
  ck(8,'active values',s.active_rows(fixture),[{'security_id':'SEC-A','quantity':D('12.5')},{'security_id':'SEC-C','quantity':D(3)}])
  ck(9,'zero lookup',s.quantity_lookup(fixture)['SEC-B'],D(0));ck(10,'sorted IDs',[r['security_id'] for r in s.id_report(list(reversed(fixture)))],['SEC-A','SEC-B','SEC-C'])
  ck(11,'membership-only comparison',s.compare_ids(['A','B','B'],['B','C']),{'missing':['A'],'unexpected':['C']})
  ck(12,'inclusive threshold',s.at_least(fixture,D(3)),baseline[1:]);ck(12,'zero threshold',s.at_least(fixture,D(0)),baseline)
  for number,fn in [(7,s.capture),(8,s.active_rows),(9,s.quantity_lookup),(10,s.id_report),(16,s.views)]:
   invalid=copy.deepcopy(fixture)+[{'security_id':'BAD','quantity':True}];saved=copy.deepcopy(invalid);err(number,'invalid final row rejected','TypeError',lambda fn=fn:fn(invalid));ck(number,'failed view preserves input',invalid,saved)
   err(number,'duplicate rejected before view','ValueError',lambda fn=fn:fn([{'security_id':'A','quantity':D(0)},{'security_id':'A','quantity':D(2)}]))
  err(12,'invalid final row despite no qualifying rows','TypeError',lambda:s.at_least(fixture+[{'security_id':'BAD','quantity':None}],D(99)))
  for number,fn,expected_empty in [(7,s.capture,()),(8,s.active_rows,[]),(9,s.quantity_lookup,{}),(10,s.id_report,[])]:ck(number,'empty input',fn([]),expected_empty)
  for number,fn in [(8,s.active_rows),(10,s.id_report),(12,lambda x:s.at_least(x,D(0)))]:
   result=fn(fixture);result[0]['quantity']=D(99);ck(number,'fresh dictionary ownership',fixture,baseline)
  day=date(2030,1,1);events=[{'event_id':'B','payment_date':day,'amount':D(0)},{'event_id':'A','payment_date':day,'amount':D(-5)}];saved=copy.deepcopy(events);groups=s.group_events(events)
  ck(13,'same-day events ordered/preserved',groups[day],[{'event_id':'A','payment_date':day,'amount':D(-5)},{'event_id':'B','payment_date':day,'amount':D(0)}]);groups[day][0]['amount']=D(99);ck(13,'event view ownership',events,saved);ck(13,'empty events',s.group_events([]),{})
  err(13,'duplicate ID across dates','ValueError',lambda:s.group_events(events+[{'event_id':'A','payment_date':date(2031,1,1),'amount':D(1)}]))
  err(13,'datetime excluded','TypeError',lambda:s.group_events(events+[{'event_id':'C','payment_date':datetime(2030,1,2),'amount':D(1)}]))
  snapshot,lookup,members=s.views(fixture);fixture[0]['quantity']=D(88);lookup['SEC-A']=D(99);ck(16,'immutable snapshot after edits',snapshot,expected);ck(16,'membership after edits',members,frozenset(['SEC-A','SEC-B','SEC-C']))
  port=manager.sample_portfolio();catalog=manager.sample_catalog();before=copy.deepcopy(port);row=s.find_holding(catalog,port,'SEC-B');ck(17,'stored zero returned',row,{'security_id':'SEC-B','quantity':D(0)});row['quantity']=D(10);ck(17,'lookup preserves portfolio',port,before)
  bad_catalog=copy.deepcopy(catalog);bad_catalog[-1]['quote_currency']='GBP';err(17,'unused invalid catalog rejected before lookup','ValueError',lambda:s.find_holding(bad_catalog,port,'SEC-B'))
  for label,args in [('add',dict(operation='add',security_id='SEC-C',quantity=D(3),next_snapshot_id='S1')),('replace',dict(operation='replace',security_id='SEC-A',quantity=D(20),next_snapshot_id='S2')),('remove',dict(operation='remove',security_id='SEC-B',next_snapshot_id='S3'))]:port=manager.apply_command(catalog,port,**args)
  ck(18,'final absolute quantities/order',port['holdings'],[{'security_id':'SEC-A','quantity':D(20)},{'security_id':'SEC-C','quantity':D(3)}]);ck(18,'S0 unchanged',before,manager.sample_portfolio())
  proc=subprocess.run([sys.executable,'-B','-m','unittest','-v','portfolio_holdings_manager','chapter04_solutions'],cwd=tmp,text=True,capture_output=True,timeout=30);runs.append(dict(command='python -B -m unittest -v portfolio_holdings_manager chapter04_solutions',exit_code=proc.returncode,stdout=proc.stdout,stderr=proc.stderr));ck('regression','combined suite exit',proc.returncode,0);ck('regression','23 existing methods','Ran 23 tests' in proc.stderr,True)
  sys.path.remove(str(tmp))
 out=dict(python=sys.version,platform=platform.platform(),source_hashes={str(p.relative_to(BOOK)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT,COMP)},exercises_reviewed=20,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),existing_methods_rerun=23,new_unique_methods=0,checks=checks,runs=runs)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','runs')},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
