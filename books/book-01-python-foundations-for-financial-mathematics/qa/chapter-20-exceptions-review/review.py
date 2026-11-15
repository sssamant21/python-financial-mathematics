"""Execute the exact manuscript fence;source predicates distinct from design review."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,math
from fractions import Fraction
from decimal import Decimal
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.09-exception-handling.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[]
def test(name,fn,want,tol=0):
 try:
  a=fn();ok=math.isclose(a,want,rel_tol=0,abs_tol=tol) if tol else a==want;cause=None
 except Exception as e:a=type(e).__name__;ok=a==want;cause=type(e.__cause__).__name__ if e.__cause__ else None
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=tol,passed=ok,cause=cause))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'financial_exceptions.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','financial_exceptions']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import financial_exceptions']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('exception_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for label,flows,rate in [('zero NPV',[-100,110],.1),('negative rate',[0,95],-.05),('negative flow',[0,-110],.1),('zero rate',[0,100],0),('ordinary',[5,-7,9],-.1)]:
  ref=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));test(label,lambda f=flows,r=rate:m.npv(f,r),ref,1e-10)
 for label,v in [('None',None),('empty',[]),('noniterable',100),('text','100'),('bool',[True]),('string',['100']),('Decimal',[Decimal(1)]),('NaN',[math.nan]),('inf',[math.inf]),('oversized',[10**1000])]:test('input '+label,lambda v=v:m.npv(v,.05),'FinancialInputError')
 for label,v in [('boundary',-1),('below',-1.01),('bool',True),('text','0'),('NaN',math.nan),('inf',math.inf),('oversized',10**1000)]:test('rate '+label,lambda v=v:m.npv([1],v),'FinancialInputError')
 for label,v in [('list',[-100,110]),('tuple',(-100,110)),('generator',iter([-100,110]))]:test('accept '+label,lambda v=v:m.npv(v,.1),0,1e-10)
 original=[-100,110];m.npv(original,.1);test('caller unchanged',lambda:original,[-100,110])
 def caught(fn):
  try:fn()
  except Exception as e:return e
  raise AssertionError('no exception')
 e=caught(lambda:m.npv(100,.05));test('noniterable cause',lambda:type(e.__cause__).__name__,'TypeError');test('noniterable boundary message',lambda:str(e),'cash flows must be iterable')
 for name,flows,rate in [('exponential',[0]*1000+[1],-.9),('summation',[1e308,1e308],0)]:
  e=caught(lambda:m.npv(flows,rate));test(name+' numerical category',lambda:type(e).__name__,'FinancialNumericalError');test(name+' overflow cause',lambda:type(e.__cause__).__name__,'OverflowError')
 def broken(kind):
  yield 1
  raise kind('private iterator sentinel')
 for kind in (TypeError,RuntimeError):
  test('late '+kind.__name__+' propagation',lambda k=kind:m.npv(broken(k),.05),kind.__name__)
 seen=[]
 def tracking():
  for x in [1,2]:seen.append(x);yield x
 test('invalid rate after materialization',lambda:m.npv(tracking(),True),'FinancialInputError');test('actual iterator consumption',lambda:seen,[1,2])
 test('input category inheritance',lambda:issubclass(m.FinancialInputError,ValueError),True);test('numerical category inheritance',lambda:issubclass(m.FinancialNumericalError,ArithmeticError),True)
 e=caught(lambda:m.npv(['private raw value'],0));test('raw input omitted from boundary message',lambda:'private raw value' not in str(e),True)
d=dict(candidate_based_on='14675f3f86154c3cdc5438c2808287592342eca8',selected_revision=REV,python=sys.version,manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,existing_unique_methods=14,method_invocations=42,new_historical_unique_methods=0,limits='Specific input/numerical/iterator categories and causes only;no external operations,retry,batch quarantine,traceback redaction or all-range NPV acceptance;F28/F32/F209 and independent/platform acceptance open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;5 commands');assert all(x['passed'] for x in rows) and all(x['returncode']==0 for x in commands)
