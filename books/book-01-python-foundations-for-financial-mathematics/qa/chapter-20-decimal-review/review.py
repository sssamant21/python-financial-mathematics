"""Exact Decimal manuscript examples; source contracts and supplemental context demos."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform
from decimal import Decimal,Context,localcontext,ROUND_HALF_EVEN,ROUND_HALF_UP,Inexact,Rounded,Overflow,InvalidOperation
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.06-testing-decimal-calculations.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();fences=re.findall(r'~~~python\n(.*?)\n~~~',text,re.S);assert len(fences)==2;code=fences[1];rows=[];commands=[]
def test(name,fn,want):
 try:a=fn();ok=a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),passed=ok))
def return_ref(a,b):
 with localcontext(Context(prec=160)):x=(Decimal(b)-Decimal(a))/Decimal(a)
 with localcontext(Context(prec=28,rounding=ROUND_HALF_EVEN)):return +x
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'decimal_calculation_tests.py';src.write_text(code);(tmp/'construction_example.py').write_text(fences[0])
 for label,args in [('construction source',[sys.executable,'construction_example.py']),('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','decimal_calculation_tests']),('compile both fences',[sys.executable,'-m','compileall','-q','.']),('quiet import',[sys.executable,'-c','import decimal_calculation_tests']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('decimal_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for a,b,want in [('100.00','.05','5.0000'),('100','0','0'),('-100','.05','-5'),('100','-.05','-5'),('200','.05','10')]:test('interest '+repr((a,b)),lambda a=a,b=b:m.simple_interest(a,b),Decimal(want))
 for a,b in [('100.00','101.50'),('100','0'),('3','4'),('1','1.00000000000000000000000000001'),('1','0.99999999999999999999999999999'),('1e100','1.00000000000000000000000000001e100')]:test('complete decimal return '+repr((a,b)),lambda a=a,b=b:m.simple_return(a,b),return_ref(a,b))
 for val,mode,want in [('1.005',ROUND_HALF_EVEN,'1.00'),('1.015',ROUND_HALF_EVEN,'1.02'),('1.005',ROUND_HALF_UP,'1.01'),('-1.005',ROUND_HALF_EVEN,'-1.00'),('-1.005',ROUND_HALF_UP,'-1.01'),('0',ROUND_HALF_EVEN,'0.00')]:
  test('cents numeric '+val+mode,lambda v=val,r=mode:m.round_cents(v,r),Decimal(want));test('cents exponent '+val+mode,lambda v=val,r=mode:m.round_cents(v,r).as_tuple().exponent,-2)
 for val in ['',' ','invalid','NaN','sNaN','Infinity',None,.1,True]:test('parser reject '+repr(val),lambda v=val:m.decimal_text(v),'ValueError')
 for name,fn in [('zero start',lambda:m.simple_return('0','1')),('negative end',lambda:m.simple_return('1','-1')),('bad mode',lambda:m.round_cents('1','invalid')),('unsupported cents magnitude',lambda:m.round_cents('1e30',ROUND_HALF_EVEN))]:test(name,fn,'ValueError')
 def hostile(fn,mode):
  with localcontext() as c:
   c.prec=3;c.rounding=ROUND_HALF_UP;c.Emax=9;c.Emin=-9
   if mode=='traps':c.traps[Inexact]=True;c.traps[Rounded]=True
   if mode=='no-overflow':c.traps[Overflow]=False
   return fn()
 for label,fn,want in [('interest',lambda:m.simple_interest('3.141592653589793238462643383','2'),Decimal('6.283185307179586476925286766')),('return',lambda:m.simple_return('3','4'),return_ref('3','4')),('cents',lambda:m.round_cents('1.005',ROUND_HALF_EVEN),Decimal('1.00'))]:test('caller traps isolated '+label,lambda f=fn:hostile(f,'traps'),want)
 test('caller exponent isolated interest',lambda:hostile(lambda:m.simple_interest('1e10','1e10'),'no-overflow'),Decimal('1e20'))
 def parsing_preserves_flags():
  with localcontext() as c:
   c.clear_flags();before=dict(c.flags)
   try:m.decimal_text('invalid')
   except Exception as e:kind=type(e).__name__
   return kind,dict(c.flags)==before
 test('malformed parser preserves caller flags',parsing_preserves_flags,('ValueError',True))
 def caller_unchanged():
  with localcontext() as c:
   c.prec=7;c.rounding=ROUND_HALF_UP;c.flags[Inexact]=True
   before=(c.prec,c.rounding,c.Emax,c.Emin,dict(c.traps),dict(c.flags));m.simple_return('3','4');after=(c.prec,c.rounding,c.Emax,c.Emin,dict(c.traps),dict(c.flags));return before==after
 test('successful call preserves configured caller and flags',caller_unchanged,True)
 test('round lines vs total',lambda:(m.round_cents('.005',ROUND_HALF_EVEN)+m.round_cents('.005',ROUND_HALF_EVEN),m.round_cents('.010',ROUND_HALF_EVEN)),(Decimal('.00'),Decimal('.01')))
# Supplemental Decimal demonstrations,not source financial implementations.
with localcontext(Context(prec=4)):four=str(Decimal(1)/3)
with localcontext(Context(prec=28)):twentyeight=str(Decimal(1)/3)
supplement=[dict(name='text vs float construction differ',actual=Decimal('.1')!=Decimal(.1),expected=True),dict(name='numeric equality separate from scale',actual=(Decimal('1.0')==Decimal('1.00'),Decimal('1.0').as_tuple().exponent!=Decimal('1.00').as_tuple().exponent),expected=(True,True)),dict(name='one third two precisions',actual=(four,twentyeight),expected=('0.3333','0.3333333333333333333333333333'))]
for x in supplement:x['passed']=x['actual']==x['expected']
d=dict(candidate_based_on='ba6d48c308ad25aa6c2d0cfd17f73ac11afa0599',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in fences],commands=commands,source_call_predicates=rows,supplemental_decimal_predicates=supplement,existing_unique_methods=14,method_invocations=42,new_historical_unique_methods=0,limits='Selected Decimal teaching context/return/rounding/parser contracts;unbounded lexical/coefficient/exponent resources,all magnitude/financial/platform/independent acceptance remain open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;3 supplemental controls;6 source commands');assert all(x['passed'] for x in rows+supplement) and all(x['returncode']==0 for x in commands)
