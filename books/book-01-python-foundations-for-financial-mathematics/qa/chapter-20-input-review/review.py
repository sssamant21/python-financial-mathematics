"""Exact input-validation manuscript; numeric/type/iterator behavior and design observations."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from decimal import Decimal,Context,localcontext
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.08-input-validation.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[]
def test(name,fn,want,rtol=0,atol=0):
 try:a=fn();ok=math.isfinite(a) and math.isclose(a,want,rel_tol=rtol,abs_tol=atol) if (rtol or atol) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),relative_tolerance=rtol,absolute_tolerance=atol,passed=ok))
def retref(a,b):
 refs=[]
 for prec in (1600,2000):
  with localcontext(Context(prec=prec)):f=float((Decimal(b)-Decimal(a))/Decimal(a));refs.append(f if math.isfinite(f) else 'ValueError')
 assert refs[0]==refs[1]
 return refs[0]
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'financial_input_validation.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','financial_input_validation']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import financial_input_validation']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('input_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for name,vals in [('list',[-100,110]),('tuple',(-100,110)),('generator',iter([-100,110]))]:test('validate '+name,lambda v=vals:m.validate_cashflows(v),[-100,110])
 original=[-100,110];test('fresh copied list',lambda:m.validate_cashflows(original) is not original,True);test('caller list unchanged',lambda:original,[-100,110])
 for name,vals in [('None',None),('empty',[]),('noniterable',100),('text','100'),('bool member',[True]),('string member',['100']),('Decimal member',[Decimal(1)]),('NaN',[math.nan]),('infinity',[math.inf]),('oversized member',[10**1000])]:test('validate reject '+name,lambda v=vals:m.validate_cashflows(v),'ValueError')
 for flows,r in [([-100,110],.1),([0,95],-.05),([0,-110],.1),([0,100],0),([5,-7,9],-.1)]:test('independent NPV '+repr((flows,r)),lambda f=flows,r=r:m.npv(f,r),float(sum((Fraction(c)/(1+Fraction(r))**i for i,c in enumerate(flows)),Fraction())),atol=1e-10)
 for label,r in [('boundary',-1),('below',-1.01),('NaN',math.nan),('inf',math.inf),('bool',True),('text','0'),('oversized',10**1000)]:test('rate reject '+label,lambda r=r:m.npv([1],r),'ValueError')
 for a,b in [(100,101.5),(100,0),(1e308,math.nextafter(1e308,math.inf)),(1e-308,1e308)]:test('complete return '+repr((a,b)),lambda a=a,b=b:m.simple_return(a,b),retref(a,b),rtol=4e-15)
 for label,a,b in [('zero start',0,1),('negative start',-1,1),('negative end',1,-1),('missing',None,1),('bool',True,1),('text','1',1),('Decimal',Decimal(1),1),('nonfinite',1,math.inf),('oversized start',10**1000,1),('oversized end',1,10**1000)]:test('return reject '+label,lambda a=a,b=b:m.simple_return(a,b),'ValueError')
 def broken(kind):
  yield 1
  raise kind('deliberate iterator failure')
 test('late TypeError remains iterator failure',lambda:m.validate_cashflows(broken(TypeError)),'TypeError');test('late RuntimeError propagates',lambda:m.validate_cashflows(broken(RuntimeError)),'RuntimeError')
 seen=[]
 def tracked():
  for x in [-100,110]:seen.append(x);yield x
 test('flow materialization precedes invalid rate',lambda:m.npv(tracked(),True),'ValueError');test('actual flow consumption order',lambda:seen,[-100,110])
 # Actual accepted shapes are design observations,not acceptance predicates.
 shape=[]
 for label,value in [('numeric mapping',{0:100,1:110}),('numeric set',{100,110}),('bytes',b'100')]:
  try:a=m.validate_cashflows(value);shape.append(dict(name=label,actual=repr(a),status='OPEN DESIGN — ordered sequence/shape policy and resource limits require an explicit surrounding contract'))
  except Exception as e:shape.append(dict(name=label,actual=repr(e),status='OPEN DESIGN — surrounding shape policy requires review'))
supplement=[dict(name='rate and basis-point units',actual=(str(Decimal(5)/100),str(Decimal(100)/10000)),expected=('0.05','0.01'))]
for x in supplement:x['passed']=x['actual']==x['expected']
d=dict(candidate_based_on='059e25f0f2b1bf376bad2a973e9703d5f6efe749',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,supplemental_unit_predicates=supplement,collection_shape_observations=shape,existing_unique_methods=14,method_invocations=42,new_historical_unique_methods=0,limits='Selected finite/value/type/late-iterator contracts;collection shape/order/resource policy(F209),broader NPV range/underflow,F28/F32/platform/independent acceptance remain open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;1 supplemental units;3 OPEN design observations;5 commands');assert all(x['passed'] for x in rows+supplement) and all(x['returncode']==0 for x in commands)
