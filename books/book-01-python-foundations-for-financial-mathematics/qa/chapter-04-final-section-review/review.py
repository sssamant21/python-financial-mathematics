"""Exact-source probes plus explicit schema extensions; standard library only."""
import copy, hashlib, io, json, platform, re, types, unittest
from pathlib import Path
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
def load(n):
 p=next((BOOK/'chapter-04').glob(f'4.{n:02}-*.md'));s=p.read_text();a=re.search(r'^## .*Complete Runnable Lab.*$',s,re.M).start();e=s.find('\n## ',a+1);code=re.findall(r'^```python\n(.*?)^```',s[a:e],re.M|re.S)[0];m=types.ModuleType('original_'+str(n));exec(compile(code,str(p),'exec'),m.__dict__);return m,dict(source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code.encode()).hexdigest())
M10,P10=load(10);M11,P11=load(11);M12,P12=load(12)
def combined(catalog,portfolios):
 result={};seen=set()
 for p in portfolios:
  out=M10.enrich_portfolio(catalog,p);key=(out['portfolio_id'],out['snapshot_id'])
  if key in seen:raise ValueError('duplicate portfolio version')
  seen.add(key)
  for row in out['holdings']:result[(*key,row['security_id'])]=row
 return result

def tagged_report(catalog,portfolio):
 base=[];tags={}
 for r in catalog:
  if set(r)!={'security_id','name','quote_currency','tags'}:raise ValueError('extended fields required')
  if type(r['tags']) is not list or any(type(t) is not str for t in r['tags']):raise TypeError('exact string tags required')
  base.append({k:v for k,v in r.items() if k!='tags'});tags[r['security_id']]=r['tags']
 out=M10.enrich_portfolio(base,portfolio)
 for r in out['holdings']:r['tags']=list(tags[r['security_id']])
 return out

def capture_tags(rows):
 if type(rows) is not list:raise TypeError('exact list required')
 base=[];result=[]
 for r in rows:
  if type(r) is not dict:raise TypeError('exact dict required')
  if set(r)!={'security_id','quantity','tags'}:raise ValueError('extended fields required')
  tags=r['tags']
  if type(tags) is not tuple:raise TypeError('exact tag tuple required')
  for tag in tags:M11.checked_id(tag)
  if len(set(tags))!=len(tags):raise ValueError('duplicate tag')
  base.append(dict(security_id=r['security_id'],quantity=r['quantity']));result.append((r['security_id'],r['quantity'],tags))
 M11.capture_holdings(base)
 return tuple(result)

def insert(snapshot,sid,quantity):
 checked=M11.checked_snapshot(snapshot);sid=M11.checked_id(sid);quantity=M11.checked_quantity(quantity)
 if sid in {r[0] for r in checked}:raise ValueError('duplicate ID')
 return checked+((sid,quantity),)

def wrapped(pid,snapshot_id,holdings,*,views=False):
 pid=M11.checked_id(pid);snapshot_id=M11.checked_id(snapshot_id)
 return dict(portfolio_id=pid,snapshot_id=snapshot_id,**({'views':M12.build_views(holdings)} if views else {'holdings':M11.capture_holdings(holdings)}))

def display_ids(views):return sorted(views[1])

def run():
 checks=[]
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,kind,fn):
  try:fn();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,'rejection',actual,kind)
 c=M10.sample_catalog();p=M10.sample_portfolio();saved=copy.deepcopy((c,p));expected=M10.enrich_portfolio(c,p)
 ck('4.10-E1','reversed catalog',M10.enrich_portfolio(c[::-1],p),expected)
 extended=c+[dict(security_id='SEC-C',name='Unused',quote_currency='USD')]
 ck('4.10-E2','unused valid metadata',M10.enrich_portfolio(extended,p),expected)
 extended[-1]['quote_currency']='GBP';err('4.10-E2','ValueError',lambda:M10.enrich_portfolio(extended,p))
 for field,value,exception in [('extra',0,'ValueError'),('security_id',1,'TypeError')]:
  bad=copy.deepcopy(p);bad['holdings'][0][field]=value;before=copy.deepcopy(bad);err('4.10-E3',exception,lambda:M10.enrich_portfolio(c,bad));ck('4.10-E3','failure preserves input',bad,before)
 p2=copy.deepcopy(p);p2['portfolio_id']='PORT-02';report=combined(c,[p,p2]);ck('4.10-E4','shared security keys',[k for k in report if k[-1]=='SEC-A'],[('PORT-01','SNAP-01','SEC-A'),('PORT-02','SNAP-01','SEC-A')]);err('4.10-E4','ValueError',lambda:combined(c,[p,p]))
 tagged=[dict(r,tags=['x','x']) for r in c];out=tagged_report(tagged,p);out['holdings'][0]['tags'].append('edited');ck('4.10-E6','source tags owned',tagged[1]['tags'],['x','x']);ck('4.10-E6','other report fresh',tagged_report(tagged,p)['holdings'][0]['tags'],['x','x']);err('4.10-E6','TypeError',lambda:tagged_report([dict(c[0],tags=[1])],p));err('4.10-E6','ValueError',lambda:M10.enrich_portfolio(tagged,p))
 relabel=copy.deepcopy(c);relabel[1]['quote_currency']='USD';ck('4.10-E8','quantities unchanged',[r['quantity'] for r in M10.enrich_portfolio(relabel,p)['holdings']],[D(0),D('12.5')]);ck('4.10-E1','source preservation',(c,p),saved)
 caller=[1]
 def rebind(x):x=[2];return x
 def append(x):x.append(3)
 ck('4.11-E1','rebind result',rebind(caller),[2]);ck('4.11-E1','caller unchanged',caller,[1]);append(caller);ck('4.11-E1','append shared',caller,[1,3])
 nested=('A',[]);nested[1].append('mutable');ck('4.11-E2','mutable descendant',nested,('A',['mutable']))
 tags=[dict(security_id='A',quantity=D(0),tags=('z','a'))];ck('4.11-E3','tag order',capture_tags(tags),(('A',D(0),('z','a')),))
 for bad,kind in [(('x','x'),'ValueError'),(['x'],'TypeError'),((1,),'TypeError'),((' x',),'ValueError')]:err('4.11-E3',kind,lambda bad=bad:capture_tags([dict(tags[0],tags=bad)]))
 err('4.11-E3','ValueError',lambda:capture_tags(tags+tags))
 class SubD(D):pass
 err('4.11-E4','TypeError',lambda:M11.capture_holdings([dict(security_id='A',quantity=SubD('1'))]))
 baseline=M11.capture_holdings(M11.sample_holdings());changed=M11.replace_quantity(baseline,'SEC-A',D('12.50'));ck('4.11-E5','equal value',changed,baseline);ck('4.11-E5','new tuple',changed is baseline,False);ck('4.11-E5','baseline literal',baseline,(('SEC-B',D(0)),('SEC-A',D('12.5'))));err('4.11-E4','TypeError',lambda:M11.replace_quantity(baseline,'SEC-A',SubD(2)))
 ck('4.11-E6','append insert',insert(baseline,'SEC-C',D(3)),baseline+(('SEC-C',D(3)),));ck('4.11-E6','empty insert',insert((),'A',D(0)),(('A',D(0)),));err('4.11-E6','ValueError',lambda:insert(baseline,'SEC-A',D(1)));err('4.11-E6','ValueError',lambda:insert(baseline+(('X',D('NaN')),),'C',D(1)));err('4.11-E6','ValueError',lambda:M11.replace_quantity(baseline,'SEC-C',D(1)))
 w=wrapped('P','S',[]);ck('4.11-E7','empty identity',w,dict(portfolio_id='P',snapshot_id='S',holdings=()));err('4.11-E7','ValueError',lambda:wrapped(' P','S',[]))
 ck('4.12-E2','unidentified equal events collapse',len(set([('2027-01-01',D(1)),('2027-01-01',D(1))])),1);ck('4.12-E2','distinct identities retained',len(set([('E1','2027-01-01',D(1)),('E2','2027-01-01',D(1))])),2)
 rows=M12.sample_holdings();old=M12.build_views(rows);rev=M12.build_views(rows[::-1]);ck('4.12-E3','snapshot reverse',rev[0],old[0][::-1]);ck('4.12-E3','lookup reverse',list(rev[1]),list(old[1])[::-1]);ck('4.12-E3','membership invariant',rev[2],old[2]);ck('4.12-E3','zero member included','SEC-B' in old[2],True)
 w=wrapped('P','S',rows,views=True);w['views'][1]['SEC-A']=D(99);w['portfolio_id']='changed';ck('4.12-E4','immutable snapshot preserved',w['views'][0],(('SEC-B',D(0)),('SEC-A',D('12.5'))));ck('4.12-E4','source preserved',rows,M12.sample_holdings());ck('4.12-E6','display sorted',display_ids(old),['SEC-A','SEC-B']);ck('4.12-E6','lookup order unchanged',list(old[1]),['SEC-B','SEC-A'])
 class SubS(str):pass
 err('4.12-E7','TypeError',lambda:M12.build_views([dict(security_id=SubS('A'),quantity=D(1))]))
 suites=[]
 for module,source in [(M10,P10),(M11,P11),(M12,P12)]:
  suite=unittest.defaultTestLoader.loadTestsFromModule(module);stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite);suites.append(dict(source=source['source'],methods=result.testsRun,successful=result.wasSuccessful(),output=stream.getvalue()))
 out=dict(python=platform.python_version(),platform=platform.platform(),exercise_records=27,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),sources=[P10,P11,P12],existing_suites=suites,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','sources','existing_suites')}));return bool(out['failed'] or not all(s['successful'] for s in suites))
if __name__=='__main__':raise SystemExit(run())
