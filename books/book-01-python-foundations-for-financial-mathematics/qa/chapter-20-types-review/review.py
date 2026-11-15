"""Exact annotated source vs runtime contracts;no static-checker acceptance implied."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,math,typing
from fractions import Fraction
from decimal import Decimal,Context,localcontext,Inexact,ROUND_HALF_EVEN,ROUND_DOWN
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.11-type-hints.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();fences=re.findall(r'~~~python\n(.*?)\n~~~',text,re.S);assert len(fences)==2;commands=[];rows=[];supp=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=math.isclose(a,want,rel_tol=0,abs_tol=tol) if tol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=tol,passed=ok))
def ref(a,b):
 vals=[]
 for prec in (1600,2000):
  with localcontext(Context(prec=prec)):z=(b-a)/a
  with localcontext(Context(prec=28,rounding=ROUND_HALF_EVEN)):vals.append(+z)
 assert vals[0]==vals[1];return vals[0]
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'type_hints_finance.py';src.write_text(fences[1]);intro=tmp/'intro_types.py';intro.write_text(fences[0])
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','type_hints_finance']),('both fence compilation',[sys.executable,'-m','compileall','-q',src.name,intro.name]),('quiet import',[sys.executable,'-c','import type_hints_finance,intro_types']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('typed_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for name,flows,rate in [('known',[-100.,110.],.1),('negative rate',[0.,95.],-.05),('negative flow',[0.,-110.],.1),('zero rate',[0.,100.],0.)]:
  value=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));test(name,lambda f=flows,r=rate:m.npv(f,r),value,1e-10)
 for name,vals in [('tuple',(-100.,110.)),('generator',iter([-100.,110.]))]:test('accept '+name,lambda vals=vals:m.npv(vals,.1),0.,1e-10)
 for name,vals in [('empty',[]),('bool',[True]),('integer',[100]),('Decimal',[Decimal(1)]),('NaN',[math.nan]),('inf',[math.inf])]:test('flow reject '+name,lambda vals=vals:m.npv(vals,0.),'ValueError')
 for name,rate in [('integer',0),('bool',True),('boundary',-1.),('NaN',math.nan),('inf',math.inf)]:test('rate reject '+name,lambda rate=rate:m.npv([1.],rate),'ValueError')
 for v in [None,0.,-1.,math.nan,math.inf,True,100,Decimal(100)]:test('price reject '+repr(v),lambda v=v:m.require_price(v),'ValueError')
 test('price accepts float',lambda:m.require_price(100.),100.)
 original=[-100.,110.];m.npv(original,.1);test('caller list unchanged',lambda:original,[-100.,110.])
 seen=[]
 def flows():
  for x in [-100.,110.]:seen.append(x);yield x
 test('materialization before rate rejection',lambda:m.npv(flows(),0),'ValueError');test('actual consumption',lambda:seen,[-100.,110.])
 pairs=[('ordinary','100','101.50'),('zero terminal','100','0'),('near one','1','1.'+'0'*39+'1'),('large common scale','1e100','1.015e100'),('third','3','4')]
 for label,a,b in pairs:
  A,B=map(Decimal,(a,b));want=ref(A,B);test('Decimal '+label,lambda A=A,B=B:m.decimal_return(A,B),want)
 for name,a,b in [('wrong type',100.,Decimal(101)),('zero',Decimal(0),Decimal(1)),('negative end',Decimal(1),Decimal(-1)),('NaN',Decimal('NaN'),Decimal(1)),('sNaN',Decimal('sNaN'),Decimal(1)),('infinite',Decimal(1),Decimal('Infinity'))]:test('Decimal reject '+name,lambda a=a,b=b:m.decimal_return(a,b),'ValueError')
 for label in ['trapped inexact','restricted range','rounding and precision']:
  A,B=(Decimal(3),Decimal(4)) if label=='trapped inexact' else (Decimal(1),Decimal('1e100')) if label=='restricted range' else (Decimal(1),Decimal('1.'+'0'*39+'1'))
  want=ref(A,B)
  with localcontext(Context(prec=2,rounding=ROUND_DOWN)) as ctx:
   if label=='trapped inexact':ctx.traps[Inexact]=True
   if label=='restricted range':ctx.Emax=9;ctx.Emin=-9
   before=(ctx.prec,ctx.rounding,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))
   test('ambient '+label,lambda A=A,B=B:m.decimal_return(A,B),want);test('caller context unchanged '+label,lambda:(ctx.prec,ctx.rounding,ctx.Emax,ctx.Emin,dict(ctx.traps),dict(ctx.flags))==before,True)
 # Runtime annotation demonstrations,not independent static analysis or financial APIs.
 ns={};exec(fences[0],ns);cases=[('intro zero',lambda:ns['simple_return'](0.,1.),'ZeroDivisionError'),('NewType float identity',lambda value=.05:m.DecimalRate(value) is value,True),('NewType does not validate bool',lambda:m.DecimalRate(True) is True,True),('optional annotation',lambda:typing.get_type_hints(m.require_price)['value']==(float|None),True),('return annotation',lambda:typing.get_type_hints(m.decimal_return)['return'] is Decimal,True)]
 for label,fn,want in cases:
  try:a=fn()
  except Exception as e:a=type(e).__name__
  supp.append(dict(name=label,actual=repr(a),expected=repr(want),passed=a==want))
checker={name:dict(available=importlib.util.find_spec(name) is not None,status='Not executed — no configured static checker/target/environment acceptance claimed') for name in ['mypy','pyright']}
d=dict(candidate_based_on='5386dc2e5da136dbb1f31bbcc015a86b4d4fb190',selected_revision=REV,python=sys.version,manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in fences],commands=commands,source_call_predicates=rows,supplemental_annotation_observations=supp,static_checker_status=checker,existing_unique_methods=12,method_invocations=36,new_historical_unique_methods=0,limits='Two exact fences/runtime and selected Decimal reports only;no static-checker signoff,all-exponent resources,NPV extremes,platform or independent acceptance. F28/F32/F209 and broader gaps open.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;5 separate annotation controls;5 commands');assert all(x['passed'] for x in rows+supp) and all(x['returncode']==0 for x in commands)
