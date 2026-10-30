"""Section 4.13 source workflows and explicitly supplemental interfaces."""
import copy,hashlib,json,os,platform,re,subprocess,sys,tempfile,types
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime, timezone
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-04/4.13-chapter-project-portfolio-holdings-manager.md'
TEXT=SOURCE.read_text();BLOCKS=re.findall(r'^```python\n(.*?)^```',TEXT,re.M|re.S)
M=types.ModuleType('original_manager');exec(compile(BLOCKS[0],str(SOURCE),'exec'),M.__dict__)

def lookup(catalog,portfolio,sid):
 """Full input validation; exact existing ID; new scalar-only record."""
 _,_,_,rows=M.validated_inputs(catalog,portfolio);sid=M.text(sid,'security_id')
 for key,quantity in rows:
  if key==sid:return dict(security_id=key,quantity=quantity)
 raise ValueError('absent target')

def membership(catalog,portfolio):
 _,pid,revision,rows=M.validated_inputs(catalog,portfolio)
 return dict(portfolio_id=pid,snapshot_id=revision,members=frozenset(sid for sid,_ in rows))

def multi(catalog,portfolios):
 if type(portfolios) is not list:raise TypeError('exact list required')
 output={}
 for p in portfolios:
  result=M.holdings_report(catalog,p);key=(result['portfolio_id'],result['snapshot_id'])
  if key in output:raise ValueError('duplicate portfolio snapshot')
  output[key]=result
 return output

def metadata_report(catalog,portfolio,*,catalog_version,observation_basis):
 """Caller-supplied nonempty labels; not verified observation times or catalog hashes."""
 cv=M.text(catalog_version,'catalog_version');basis=M.text(observation_basis,'observation_basis')
 return dict(catalog_version=cv,observation_basis=basis,report=M.holdings_report(catalog,portfolio))

def supplied_prices(catalog,portfolio,prices):
 """Exact supplied positive Decimal per-instrument-unit quotes at UTC instants.

 No arithmetic/FX: currency must match catalog; reject missing/stale prices
 downstream under an explicit valuation policy, not by inventing zero values.
 """
 lookup,_,_,_=M.validated_inputs(catalog,portfolio)
 if type(prices) is not list:raise TypeError('exact list required')
 result=[];seen=set()
 for row in prices:
  if type(row) is not dict:raise TypeError('exact price dict required')
  if set(row)!={'security_id','price','currency','quote_unit','observed_at','source_id'}:raise ValueError('price fields required')
  sid=M.text(row['security_id'],'security_id');currency=M.text(row['currency'],'currency');source=M.text(row['source_id'],'source_id')
  if sid not in lookup:raise ValueError('unknown priced security')
  if currency!=lookup[sid][1]:raise ValueError('currency mismatch; no FX')
  if type(row['quote_unit']) is not str or row['quote_unit']!='per_instrument_unit':raise ValueError('unsupported quote unit')
  price=M.quantity_value(row['price'])
  if price<=0:raise ValueError('positive supplied price required')
  instant=row['observed_at']
  if type(instant) is not datetime:raise TypeError('exact datetime required')
  if instant.tzinfo is not timezone.utc:raise ValueError('explicit UTC required')
  key=(sid,instant)
  if key in seen:raise ValueError('duplicate observation')
  seen.add(key);result.append(dict(row))
 return result

def run():
 checks=[]
 def ck(id,label,actual,expected):checks.append(dict(id=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,kind,fn):
  try:fn();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'rejection',actual,kind)
 commands=[]
 with tempfile.TemporaryDirectory(prefix='holdings_review_') as tmp:
  p=Path(tmp);(p/'portfolio_holdings_manager.py').write_text(BLOCKS[0]);(p/'demo_holdings_manager.py').write_text(BLOCKS[1]);env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
  for args,expect in [(['portfolio_holdings_manager.py'],'Ran 10 tests'),(['demo_holdings_manager.py'],'PASS: active report contains SEC-A and SEC-C; S0 baseline preserved'),(['-c','import portfolio_holdings_manager'],'')]:
   r=subprocess.run([sys.executable,'-B',*args],cwd=p,env=env,text=True,capture_output=True);ok=r.returncode==0 and ((expect in r.stdout+r.stderr) if expect else (r.stdout==r.stderr==''));commands.append(dict(argv=[sys.executable,'-B',*args],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,status='PASS' if ok else 'FAIL'))
 c=M.sample_catalog();p=M.sample_portfolio();saved=copy.deepcopy((c,p));s1=M.apply_command(c,p,operation='add',security_id='SEC-C',quantity=D(3),next_snapshot_id='S1');s2=M.apply_command(c,s1,operation='replace',security_id='SEC-A',quantity=D(20),next_snapshot_id='S2');s3=M.apply_command(c,s2,operation='remove',security_id='SEC-B',next_snapshot_id='S3')
 for name,value,expected in [('S0',p,[('SEC-B',D(0)),('SEC-A',D('12.5'))]),('S1',s1,[('SEC-B',D(0)),('SEC-A',D('12.5')),('SEC-C',D(3))]),('S2',s2,[('SEC-B',D(0)),('SEC-A',D(20)),('SEC-C',D(3))]),('S3',s3,[('SEC-A',D(20)),('SEC-C',D(3))])]:
  ck('sequence',name,[(r['security_id'],r['quantity']) for r in value['holdings']],expected);ck('sequence','identity '+name,(value['portfolio_id'],value['snapshot_id']),('PORT-01',name))
 ck('ownership','baseline/catalog', (c,p),saved)
 ck('report','all order',[r['security_id'] for r in M.holdings_report(c,p)['rows']],['SEC-A','SEC-B']);ck('report','active order',[r['security_id'] for r in M.holdings_report(c,p,active_only=True)['rows']],['SEC-A'])
 for sid,rev,kind in [(' SEC-A','S1','ValueError'),('SEC-A ', 'S1','ValueError'),('SEC-A',1,'TypeError')]:err('extension-1',kind,lambda sid=sid,rev=rev:M.apply_command(c,p,operation='replace',security_id=sid,quantity=D(1),next_snapshot_id=rev))
 bad=copy.deepcopy(p);del bad['holdings'][1]['quantity'];err('extension-1','ValueError',lambda:M.holdings_report(c,bad))
 err('hands-on','ValueError',lambda:M.apply_command(c,s1,operation='add',security_id='SEC-A',quantity=D(1),next_snapshot_id='S2'));ck('hands-on','duplicate failure preserves S1',[(r['security_id'],r['quantity']) for r in s1['holdings']],[('SEC-B',D(0)),('SEC-A',D('12.5')),('SEC-C',D(3))])
 row=lookup(c,p,'SEC-B');ck('extension-2','zero lookup',row,dict(security_id='SEC-B',quantity=D(0)));row['quantity']=D(99);ck('extension-2','fresh lookup',lookup(c,p,'SEC-B')['quantity'],D(0));err('extension-2','ValueError',lambda:lookup(c,p,'SEC-C'))
 bad=copy.deepcopy(p);bad['holdings'].append(dict(security_id='SEC-C',quantity='bad'));err('extension-2','TypeError',lambda:lookup(c,bad,'SEC-B'));ck('extension-3','all membership',membership(c,p),dict(portfolio_id='PORT-01',snapshot_id='S0',members=frozenset(['SEC-A','SEC-B'])));empty=dict(portfolio_id='P',snapshot_id='E',holdings=[]);ck('extension-3','empty identity',membership([],empty),dict(portfolio_id='P',snapshot_id='E',members=frozenset()))
 p2=copy.deepcopy(p);p2['portfolio_id']='P2';reports=multi(c,[p,p2]);ck('extension-4','two scoped portfolios',list(reports),[('PORT-01','S0'),('P2','S0')]);ck('extension-4','shared security retained',[(k,r['rows'][0]['security_id']) for k,r in reports.items()],[ (('PORT-01','S0'),'SEC-A'),(('P2','S0'),'SEC-A')]);err('extension-4','ValueError',lambda:multi(c,[p,p]));reports[('P2','S0')]['rows'][0]['name']='changed';ck('extension-4','other report isolated',reports[('PORT-01','S0')]['rows'][0]['name'],'Example Equity')
 meta=metadata_report(c,p,catalog_version='C1',observation_basis='synthetic supplied snapshot');ck('extension-6','labels',(meta['catalog_version'],meta['observation_basis']),('C1','synthetic supplied snapshot'));meta['report']['rows'][0]['quantity']=D(99);ck('extension-6','source preserved',p,saved[1]);err('extension-6','ValueError',lambda:metadata_report(c,p,catalog_version=' ',observation_basis='basis'))
 same=M.apply_command(c,p,operation='replace',security_id='SEC-A',quantity=D('12.50'),next_snapshot_id='S1');ck('revision','equal replacement uses new label',same['snapshot_id'],'S1');ck('revision','equal replacement values',same['holdings'],p['holdings']);err('revision','ValueError',lambda:M.apply_command(c,p,operation='replace',security_id='SEC-A',quantity=D(1),next_snapshot_id='S0'))
 historical=M.apply_command(c,s1,operation='replace',security_id='SEC-A',quantity=D(1),next_snapshot_id='S0');ck('revision-limit','historical label allowed',historical['snapshot_id'],'S0');competing=M.apply_command(c,p,operation='replace',security_id='SEC-A',quantity=D(2),next_snapshot_id='S1');ck('concurrency-limit','same label competing branch accepted',competing['snapshot_id'],s1['snapshot_id'])
 quote=dict(security_id='SEC-A',price=D('10.125'),currency='USD',quote_unit='per_instrument_unit',observed_at=datetime(2026,1,1,tzinfo=timezone.utc),source_id='SYNTHETIC')
 prices=supplied_prices(c,p,[quote]);ck('extension-9','supplied exact quote',prices,[quote]);prices[0]['price']=D(99);ck('extension-9','fresh quote record',quote['price'],D('10.125'))
 for changes,kind in [({'currency':'EUR'},'ValueError'),({'quote_unit':'per_100_nominal'},'ValueError'),({'observed_at':datetime(2026,1,1)},'ValueError'),({'price':D('NaN')},'ValueError'),({'price':D(0)},'ValueError'),({'security_id':'UNKNOWN'},'ValueError')]:err('extension-9',kind,lambda changes=changes:supplied_prices(c,p,[dict(quote,**changes)]))
 err('extension-9','ValueError',lambda:supplied_prices(c,p,[quote,quote]));ck('extension-9','empty price input',supplied_prices(c,p,[]),[])
 out=dict(python=platform.python_version(),platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),code_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in BLOCKS],predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),commands=commands,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','commands','code_sha256')}));return bool(out['failed'] or any(c['status']!='PASS' for c in commands))
if __name__=='__main__':raise SystemExit(run())
