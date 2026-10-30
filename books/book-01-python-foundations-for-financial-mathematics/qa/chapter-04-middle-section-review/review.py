"""Exact Section4.4–4.6 functions and explicit teaching object/identity probes."""
import copy,hashlib,json,platform,re,types
from pathlib import Path
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]

def run():
 checks=[];sources=[];mods={}
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,label,expected,call):
  try:call();actual='no exception'
  except Exception as exc:actual=type(exc).__name__
  ck(id,label,actual,expected)
 for n in (4,5,6):
  p=next((BOOK/'chapter-04').glob(f'4.{n:02}-*.md'));s=p.read_text();a=re.search(r'^## .*Hands-On Lab.*$',s,re.M).start();e=s.find('\n## ',a+1);code=re.findall(r'^```python\n(.*?)^```',s[a:e],re.M|re.S)[0];m=types.ModuleType('source_lab_'+str(n));exec(compile(code,str(p),'exec'),m.__dict__);mods[n]=m;sources.append(dict(source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code.encode()).hexdigest()))
 example={'payment_id':'VALUE','amount':D(0)};ck('4.4-E1','key versus value membership',('payment_id' in example,'VALUE' in example,'VALUE' in example.values()),(True,False,True))
 missing={'payment_id':'A'};err('4.4-E2','required lookup','KeyError',lambda:missing['amount']);ck('4.4-E2','get is absence not zero',missing.get('amount'),None)
 index=mods[4].index_payments;record=mods[4].sample_payment();before=copy.deepcopy(record)
 err('4.4-E4','identical ID rejected','ValueError',lambda:index([record,dict(record)]));ck('4.4-E4','failed index leaves source',record,before)
 other=dict(record,payment_id='p001');result=index([record,other]);ck('4.4-E5','case distinct IDs retained',list(result),['P001','p001']);ck('4.4-E5','same amounts preserved',[r['amount'] for r in result.values()],[D(100),D(100)])
 notes={'notes':['first']};shallow=dict(notes);shallow['notes'].append('second');ck('4.4-E7','mutable descendants shared',notes['notes'],['first','second'])
 ordered={'A':1,'B':2,'C':3};del ordered['B'];ordered['B']=2;ck('4.4-E8','reinsert moves key to end',list(ordered),['A','C','B'])
 ck('4.5-E1','empty dictionary versus set',(type({}).__name__,type(set()).__name__),('dict','set'))
 reconcile=mods[5].reconcile_ids;r=reconcile(['A','B','C'],['B','C','D']);ck('4.5-E2','four independent expected sets',r,dict(missing={'A'},unexpected={'D'},matched={'B','C'},duplicate_received=set()))
 r=reconcile(['A'],['B','B']);ck('4.5-E3','unexpected duplicate evidence',r,dict(missing={'A'},unexpected={'B'},matched=set(),duplicate_received={'B'}))
 values={'A'};err('4.5-E4','remove missing','KeyError',lambda:values.remove('X'));ck('4.5-E4','discard missing',values.discard('X'),None);ck('4.5-E4','set preserved',values,{'A'})
 ck('4.5-E5','set loses repeated amount',(len([D(100),D(100)]),len(set([D(100),D(100)]))),(2,1))
 for expected,received in [([],[]),(['A','B','C'],['B','C','D']),(['A'],['B','B']),(['A','B'],['A','B','B'])]:
  saved=(list(expected),list(received));r=reconcile(expected,received);e=set(expected);a=set(received)
  ck('4.5-E7','expected partition',r['missing']|r['matched'],e);ck('4.5-E7','received partition',r['unexpected']|r['matched'],a);ck('4.5-E7','disjoint partitions',(r['missing']&r['matched'],r['unexpected']&r['matched']),(set(),set()));ck('4.5-E7','inputs preserved',(expected,received),saved)
 ck('4.5-E8','alphabetic is not arrival order',sorted(['B','A'])==['B','A'],False)
 m=mods[6];positions=m.sample_positions();portfolio=m.sample_portfolio(positions);saved=copy.deepcopy(portfolio);invalid=copy.deepcopy(portfolio);del invalid['positions'][1]['instrument_id'];err('4.6-E3','missing inner ID','ValueError',lambda:m.flatten_portfolio(invalid));ck('4.6-E3','valid baseline preserved',portfolio,saved)
 shallow=dict(portfolio);shallow['positions'].append({'instrument_id':'FUND-C','quantity':D(1)});ck('4.6-E4','outer copy shares positions',portfolio['positions'] is shallow['positions'],True)
 row={'instrument_id':'A','quantity':D(1)};repeated=[row]*3;repeated[0]['quantity']=D(2);ck('4.6-E5','three aliases not independent',[r['quantity'] for r in repeated],[D(2)]*3)
 empty=m.sample_portfolio([]);ck('4.6-E2','explicit empty positions valid',m.flatten_portfolio(empty),[]);bad=dict(empty);del bad['positions'];err('4.6-E2','missing positions invalid','ValueError',lambda:m.flatten_portfolio(bad))
 wrapper={'portfolio_id':empty['portfolio_id'],'currency':empty['currency'],'rows':m.flatten_portfolio(empty)};ck('4.6-E7','proposed wrapper retains empty identity',wrapper,{'portfolio_id':'PORT-01','currency':'USD','rows':[]})
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=27,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),sources=sources,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','sources')},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
