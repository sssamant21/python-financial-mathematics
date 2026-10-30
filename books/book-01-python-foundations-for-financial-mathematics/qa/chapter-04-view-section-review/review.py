"""Exact-source view checks and explicit new schema/format teaching interfaces."""
import copy,hashlib,json,platform,re,types
from pathlib import Path
from datetime import date
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]

def load(n):
 p=next((BOOK/'chapter-04').glob(f'4.{n:02}-*.md'));s=p.read_text();a=re.search(r'^## .*Complete Runnable Lab.*$',s,re.M).start();e=s.find('\n## ',a+1);code=re.findall(r'^```python\n(.*?)^```',s[a:e],re.M|re.S)[0];m=types.ModuleType('original_'+str(n));exec(compile(code,str(p),'exec'),m.__dict__);return m,dict(source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code.encode()).hexdigest())
M7,P7=load(7);M8,P8=load(8);M9,P9=load(9)

def include_zero(value):
 """Validate original input contract; return fresh all-position views in source order."""
 M7.build_active_views(value)
 rows=[dict(r) for r in value]
 return rows,{r['instrument_id']:r['quantity'] for r in rows}

def tagged_active(value):
 """Extended exact row schema adds tags:list[str]; preserve order/duplicates, copy tags."""
 if not isinstance(value,list):raise TypeError('list required')
 base=[]
 for row in value:
  if not isinstance(row,dict):raise TypeError('record required')
  if set(row)!={'instrument_id','quantity','tags'}:raise ValueError('extended fields required')
  if not isinstance(row['tags'],list) or any(type(x) is not str for x in row['tags']):raise TypeError('tags must be list of exact strings')
  base.append(dict(instrument_id=row['instrument_id'],quantity=row['quantity']))
 M7.build_active_views(base)
 return [dict(instrument_id=r['instrument_id'],quantity=r['quantity'],tags=list(r['tags'])) for r in value if r['quantity']>0]

def multi_portfolio(value):
 """Unique unpadded portfolio IDs; exact wrapper fields; active key=(portfolio,instrument)."""
 if not isinstance(value,list):raise TypeError('list required')
 result={};seen=set()
 for portfolio in value:
  if not isinstance(portfolio,dict):raise TypeError('portfolio dictionary required')
  if set(portfolio)!={'portfolio_id','positions'}:raise ValueError('portfolio fields required')
  pid=portfolio['portfolio_id']
  if type(pid) is not str:raise TypeError('portfolio_id must be exact str')
  if not pid or pid.strip()!=pid or pid in seen:raise ValueError('invalid/duplicate portfolio_id')
  seen.add(pid);rows,_=M7.build_active_views(portfolio['positions'])
  for row in rows:result[(pid,row['instrument_id'])]=dict(row)
 return result

def account_report(value,*,currency):
 """Extended schema; unique(account_id,instrument_id), amount descending then both IDs."""
 if not isinstance(value,list):raise TypeError('list required')
 M8.checked_currency(currency)
 checked=[];seen=set()
 for row in value:
  if not isinstance(row,dict):raise TypeError('record required')
  if set(row)!={'account_id','instrument_id','currency','market_value'}:raise ValueError('extended fields required')
  key=(row['account_id'],row['instrument_id'])
  for part in key:
   if type(part) is not str:raise TypeError('exact string IDs required')
   if not part or part.strip()!=part:raise ValueError('invalid ID')
  if key in seen:raise ValueError('duplicate account/instrument')
  seen.add(key);M8.checked_currency(row['currency']);M8.checked_amount(row['market_value'],'market_value');checked.append(dict(row))
 ordered=sorted([row for row in checked if row['currency']==currency],key=lambda row:(row['account_id'],row['instrument_id']))
 return sorted(ordered,key=lambda row:row['market_value'],reverse=True)

def report_with_metadata(rows,*,snapshot_id,currency,minimum,limit):
 """Fresh ranked source-contract report with caller-supplied snapshot/selection metadata."""
 if type(snapshot_id) is not str or not snapshot_id or snapshot_id.strip()!=snapshot_id:raise ValueError('snapshot_id required')
 result=M8.ranked_positions(rows,currency=currency,minimum=minimum,limit=limit)
 return dict(snapshot_id=snapshot_id,selection=dict(currency=currency,minimum=minimum,limit=limit),rows=result)

def parse_payment_date(value):
 """Exact ASCII YYYY-MM-DD text only; no padding/timestamps; ValueError for calendar errors."""
 if type(value) is not str:raise TypeError('exact string required')
 if re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',value) is None:raise ValueError('YYYY-MM-DD required')
 return date.fromisoformat(value)

def run():
 checks=[]
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,expected,call):
  try:call();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'expected rejection',actual,expected)
 quantities=[D('12.5'),D(0),D(3)];loop=[]
 for q in quantities:
  if q>0:loop.append(q)
 ck('4.7-E1','loop preserves positive order',loop,[D('12.5'),D(3)])
 rows,_=M7.build_active_views(M7.sample_positions());ck('4.7-E2','active IDs',[r['instrument_id'] for r in rows],['BOND-A','ETF-B'])
 rows,lookup=include_zero(M7.sample_positions());ck('4.7-E3','inclusive view IDs',list(lookup),['BOND-A','CASH-RESERVE','ETF-B']);ck('4.7-E3','empty inclusive outputs',include_zero([]),([],{}))
 ck('4.7-E4','duplicate overwrites quantity',{k:v for k,v in [('A',D(1)),('A',D(2))]},{'A':D(2)})
 case=[{'instrument_id':'A','quantity':D(1)},{'instrument_id':'a','quantity':D(2)}];ck('4.7-E5','case policy retained',list(M7.build_active_views(case)[1]),['A','a'])
 tagged=[{'instrument_id':'A','quantity':D(1),'tags':['x']}];shallow=dict(tagged[0]);shallow['tags'].append('shared');ck('4.7-E6','alias demonstrated',tagged[0]['tags'],['x','shared']);out=tagged_active(tagged);out[0]['tags'].append('new');ck('4.7-E6','explicit tag copy',tagged[0]['tags'],['x','shared']);err('4.7-E6','TypeError',lambda:tagged_active([dict(tagged[0],tags=[1])]))
 portfolios=[dict(portfolio_id='P1',positions=case[:1]),dict(portfolio_id='P2',positions=case[:1])];ck('4.7-E7','same instrument distinct portfolios',list(multi_portfolio(portfolios)),[('P1','A'),('P2','A')]);err('4.7-E7','ValueError',lambda:multi_portfolio([dict(portfolio_id='P1',positions=[case[0],case[0]])]));err('4.7-E8','ValueError',lambda:M7.build_active_views(case+[dict(instrument_id='BAD',quantity=D(-1))]))
 sample=M8.sample_positions();ranked=M8.ranked_positions(sample,currency='USD',minimum=D(0),limit=99);ascending=sorted(ranked,key=lambda row:(row['market_value'],row['position_id']));ck('4.8-E1','ascending amount/ID',[r['position_id'] for r in ascending],['ZERO','ALPHA','ZETA','BETA'])
 ck('4.8-E2','reverse tuple reverses tie IDs',sorted([(D(100),'ALPHA'),(D(100),'ZETA')],reverse=True),[(D(100),'ZETA'),(D(100),'ALPHA')])
 boundary=[dict(position_id='AT',currency='USD',market_value=D(100)),dict(position_id='BELOW',currency='USD',market_value=D(99))];ck('4.8-E3','inclusive threshold without rounding',[r['position_id'] for r in M8.ranked_positions(boundary,currency='USD',minimum=D(100),limit=9)],['AT'])
 for values in [sample,list(reversed(sample)),sample[2:]+sample[:2]]:ck('4.8-E4','tie invariant',[r['position_id'] for r in M8.ranked_positions(values,currency='USD',minimum=D(100),limit=3)],['BETA','ALPHA','ZETA'])
 accounts=[dict(account_id='A1',instrument_id='X',currency='USD',market_value=D(100)),dict(account_id='A2',instrument_id='X',currency='USD',market_value=D(100))]
 ck('4.8-E5','composite identity',[(r['account_id'],r['instrument_id']) for r in account_report(list(reversed(accounts)),currency='USD')],[('A1','X'),('A2','X')]);err('4.8-E5','ValueError',lambda:account_report([accounts[0],accounts[0]],currency='USD'))
 saved=copy.deepcopy(sample);report=report_with_metadata(sample,snapshot_id='S1',currency='USD',minimum=D(100),limit=2);ck('4.8-E7','metadata retained',(report['snapshot_id'],report['selection']['limit']),('S1',2));report['rows'][0]['market_value']=D(0);ck('4.8-E7','source unchanged',sample,saved)
 bad=copy.deepcopy(sample);bad[1]['currency']='GBP';err('4.8-E9','ValueError',lambda:M8.ranked_positions(bad,currency='USD',minimum=D(100),limit=0))
 schedule=M9.sample_schedule();schedule['events'].append(dict(event_id='E-00',payment_date=date(2027,1,15),amount=D(1)));normal,group=M9.normalize_schedule(schedule);ck('4.9-E1','first date identities',[r['event_id'] for r in group[date(2027,1,15)]],['E-0','E-00'])
 eur=copy.deepcopy(schedule);eur['currency']='EUR';enormal,_=M9.normalize_schedule(eur);ck('4.9-E3','relabel preserves amounts',[r['amount'] for r in enormal['events']],[r['amount'] for r in normal['events']])
 bad=copy.deepcopy(schedule);bad['events'][-1]['event_id']=1;err('4.9-E4','TypeError',lambda:M9.normalize_schedule(bad));bad=copy.deepcopy(schedule);bad['events'][-1]['extra']=0;err('4.9-E4','ValueError',lambda:M9.normalize_schedule(bad))
 ck('4.9-E5','leap day',parse_payment_date('2028-02-29'),date(2028,2,29))
 for text in ['2027-02-29',' 2028-02-29','2028-2-29','2028-02-29 ']:err('4.9-E5','ValueError',lambda text=text:parse_payment_date(text))
 reversed_schedule=copy.deepcopy(schedule);reversed_schedule['events'].reverse();ck('4.9-E9','reversal canonicalization',M9.normalize_schedule(reversed_schedule),M9.normalize_schedule(schedule))
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=27,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),sources=[P7,P8,P9],checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','sources')},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
