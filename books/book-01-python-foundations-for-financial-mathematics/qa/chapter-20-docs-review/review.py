"""Execute the documented source,help output and explicit input/iterator contracts."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,math,inspect
from fractions import Fraction
from decimal import Decimal
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.12-documentation.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[];supp=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=math.isclose(a,want,rel_tol=0,abs_tol=tol) if tol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'documented_finance.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','documented_finance']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import documented_finance']),('help rendering',[sys.executable,'-c','from documented_finance import npv;help(npv)']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('docs_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for label,flows,rate in [('known',[-100.,110.],.1),('t0 identity',[3.],.1),('negative rate',[0.,95.],-.05),('negative flow',[0.,-110.],.1),('zero rate',[0.,100.],0.),('ordinary',[5.,-7.,9.],-.1)]:
  ref=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));test(label,lambda f=flows,r=rate:m.npv(f,r),ref,1e-10)
 for label,flows in [('None',None),('noniterable',100),('empty',[]),('integer member',[100]),('bool member',[True]),('text','100'),('Decimal',[Decimal(1)]),('NaN',[math.nan]),('inf',[math.inf])]:test('invalid '+label,lambda f=flows:m.npv(f,0.),'ValueError')
 for label,rate in [('integer',0),('bool',True),('boundary',-1.),('below',-1.01),('NaN',math.nan),('inf',math.inf)]:test('rate '+label,lambda r=rate:m.npv([1.],r),'ValueError')
 for label,flows in [('tuple',(-100.,110.)),('generator',iter([-100.,110.]))]:test('accepted '+label,lambda f=flows:m.npv(f,.1),0.,1e-10)
 def caught(fn):
  try:fn()
  except Exception as e:return e
  raise AssertionError('expected failure')
 for value in [None,100]:
  e=caught(lambda:m.npv(value,0.));test('noniterable cause '+repr(value),lambda e=e:type(e.__cause__).__name__,'TypeError')
 for kind in (TypeError,RuntimeError):
  instance=kind('synthetic iterator error')
  def broken():
   yield 1.
   raise instance
  e=caught(lambda:m.npv(broken(),0.));test('late '+kind.__name__+' identity',lambda e=e:e is instance,True)
 seen=[]
 def tracking():
  for x in [-100.,110.]:seen.append(x);yield x
 test('materialization before bad rate',lambda:m.npv(tracking(),0),'ValueError');test('actual iterator order',lambda:seen,[-100.,110.])
 original=[-100.,110.];m.npv(original,.1);test('caller unchanged',lambda:original,[-100.,110.])
 e=caught(lambda:m.npv([0.]*1000+[1.],-.9));test('detected overflow category',lambda:type(e).__name__,'ValueError');test('detected overflow cause',lambda:type(e.__cause__).__name__,'OverflowError')
 doc=inspect.getdoc(m.npv);helpout=next(x['stdout'] for x in commands if x['label']=='help rendering')
 for label,fn in [('docstring runtime visibility',lambda:'time zero' in doc),('help contract rendered',lambda:'time zero' in helpout and 'day-count' in helpout),('strict flow contract stated',lambda:'built-in floats' in doc),('limitations stated',lambda:'Underflow' in doc and 'currencies' in doc)]:supp.append(dict(name=label,passed=fn(),scope='Documentation visibility/text observation,not financial accuracy acceptance'))
d=dict(candidate_based_on='5ada3da82c869410cdc54311b187fe51e695fdcf',selected_revision=REV,python=sys.version,manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,supplemental_documentation_observations=supp,existing_unique_methods=12,method_invocations=36,new_historical_unique_methods=0,limits='Selected contract/input/iterator/ordinary NPV and help rendering only;not provenance,source truth,all-range NPV,static-checker,platform or independent acceptance. F28/F32/F209 and broader gaps open.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;4 separate documentation observations;6 commands');assert all(x['passed'] for x in rows+supp) and all(x['returncode']==0 for x in commands)
