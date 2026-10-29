import hashlib,json,platform,re,sys,types
from pathlib import Path
from decimal import Decimal as D
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]

def indexed_positive(values:object)->list[tuple[int,D]]:
 """Finite exact Decimal list; index0 is period0, retain original ordinals."""
 if not isinstance(values,list):raise TypeError('list required')
 for value in values:
  if type(value) is not D:raise TypeError('exact Decimal required')
  if not value.is_finite():raise ValueError('finite amount required')
 return [(i,v) for i,v in enumerate(values) if v>0]

def run():
 checks=[];sources=[];mods={}
 def ck(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def err(id,label,expected,call):
  try:call();actual='no exception'
  except Exception as e:actual=type(e).__name__
  ck(id,label,actual,expected)
 for n in (1,2,3):
  p=next((BOOK/'chapter-04').glob(f'4.{n:02}-*.md'));s=p.read_text();a=re.search(r'^## .*Hands-On Lab.*$',s,re.M).start();e=s.find('\n## ',a+1);code=re.findall(r'^```python\n(.*?)^```',s[a:e],re.M|re.S)[0];m=types.ModuleType('original_lab_'+str(n));exec(compile(code,str(p),'exec'),m.__dict__);mods[n]=m;sources.append(dict(source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code.encode()).hexdigest()))
 first=mods[1].sample_payment();second=dict(first);second['payment_id']='OTHER';ck('4.1-E3','two equal payments distinct IDs',first['payment_id']!=second['payment_id'],True);ck('4.1-E3','both valid',all(mods[1].validate_payment(v)==v for v in (first,second)),True)
 bad=dict(first);bad['amount']=D('Infinity');err('4.1-E6','infinite amount','ValueError',lambda:mods[1].validate_payment(bad))
 values=list(map(D,('-1000','100','150','200','300')));ck('4.2-E1','period0 plus four observations',len(values),5);ck('4.2-E2','slice indices1,2',values[1:3],[D(100),D(150)])
 a=[];a.append([D(1),D(2)]);b=[];b.extend([D(1),D(2)]);ck('4.2-E3','append versus extend',(a,b),([[D(1),D(2)]],[D(1),D(2)]))
 repeated=[D(100),D(100)];repeated.remove(D(100));ck('4.2-E4','remove first equal value',repeated,[D(100)])
 err('4.2-E5','empty pop','IndexError',lambda:[].pop())
 original=[D(1)];alias=original;shallow=list(original);alias.append(D(2));ck('4.2-E6','alias versus shallow top-level',(original,shallow),([D(1),D(2)],[D(1)]))
 rows=[{'amount':D(1)}];shallow=list(rows);shallow[0]['amount']=D(2);ck('4.2-E7','nested record shared',rows,[{'amount':D(2)}])
 values[2]=D(0) # Separate selection fixture includes an observed zero.
 ck('4.2-E8','original period indices',indexed_positive(values),[(1,D(100)),(3,D(200)),(4,D(300))]);ck('4.2-E8','empty',indexed_positive([]),[]);err('4.2-E8','invalid later entry before selection','ValueError',lambda:indexed_positive([D(100),D('NaN')]));err('4.2-E8','wrong type','TypeError',lambda:indexed_positive([True]))
 ck('4.2-E9','renumbering changes origin',[i for i,_ in indexed_positive(values)]==list(range(3)),False)
 ck('4.3-E1','empty and singleton',((),(D(1),)),(tuple(),tuple([D(1)])))
 period,amount=(3,D(200));ck('4.3-E2','explicit period pair',(period,amount),(3,D(200)))
 def unpack():a,b=(1,2,3)
 err('4.3-E3','wrong length unpack','ValueError',unpack)
 def assign():
  item=(D(1),);item[0]=D(2)
 err('4.3-E4','tuple item immutable','TypeError',assign)
 ck('4.3-E5','supported upper period',mods[3].positive_period_flows([(1000,D(1))]),[(1000,D(1))])
 frozen=(D(1),);nested=({'quantity':D(1)},);nested[0]['quantity']=D(2);ck('4.3-E7','tuple descendant mutation',(frozen,nested[0]['quantity']),((D(1),),D(2)))
 ck('4.3-E9','period-preserving source selection',mods[3].positive_period_flows([(0,D(-1000)),(2,D(100)),(5,D(200))]),[(2,D(100)),(5,D(200))])
 out=dict(python=sys.version,platform=platform.platform(),exercise_records=27,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),source_provenance=sources,checks=checks)
 (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('checks','source_provenance')},indent=2));return bool(out['failed'])
if __name__=='__main__':raise SystemExit(run())
