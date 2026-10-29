"""Sections3.4–3.6 exercises: original lab calls and explicit teaching variants."""
import ast,contextlib,hashlib,io,json,platform,re,sys
from decimal import Decimal as D
from pathlib import Path
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]


def run():
 checks=[];source={};spaces={};provenance=[]
 def check(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
 def raises(id,label,expected,call):
  try:call();actual='no exception'
  except Exception as error:actual=type(error).__name__
  check(id,label,actual,expected)
 for n in (4,5,6):
  p=next((BOOK/'chapter-03').glob(f'3.{n:02}-*.md'));text=p.read_text();start=re.search(r'^## .*Hands-On Lab.*$',text,re.M).start();end=text.find('\n## ',start+1);code=re.findall(r'^```python\n(.*?)^```',text[start:end],re.M|re.S)[0]
  state={};out=io.StringIO()
  with contextlib.redirect_stdout(out):exec(compile(code,str(p),'exec'),state)
  source[n]=code;spaces[n]=state;provenance.append(dict(source=str(p.relative_to(BOOK)),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),lab_code_sha256=hashlib.sha256(code.encode()).hexdigest(),stdout=out.getvalue()))
 fv=spaces[4]['future_value']
 tree=ast.parse(source[4]);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='future_value')
 for parent in ast.walk(function):
  for field,value in ast.iter_fields(parent):
   if isinstance(value,list):
    for index,item in enumerate(value):
     if isinstance(item,ast.Return):value[index]=ast.Expr(ast.Call(ast.Name('print',ast.Load()),[item.value],[]))
 changed=ast.fix_missing_locations(ast.Module([function],[]));state={'Decimal':D};exec(compile(changed,'print_variant','exec'),state)
 out=io.StringIO()
 with contextlib.redirect_stdout(out):value=state['future_value'](D(1000),D('.05'),2)
 check('3.4-E1','print variant returns None',value,None);check('3.4-E1','printed calculation',out.getvalue().strip(),'1102.5000')
 def net_cash_flow(inflow,outflow):return inflow-outflow
 for inflow,outflow,expected in [(10,5,5),(5,5,0),(5,10,-5)]:check('3.4-E2','signed net cash flow',net_cash_flow(D(inflow),D(outflow)),D(expected))
 check('3.4-E3','text and Decimal types differ',(type('1102.50').__name__,type(D('1102.50')).__name__),('str','Decimal'))
 check('3.4-E4','final supplied observation',spaces[4]['first_target_period']([D(100),D(110),D(121)],D(121)),2)
 for principal,rate in [(D('NaN'),D('.05')),(D(1000),D('Infinity'))]:raises('3.4-E5','nonfinite before arithmetic','ValueError',lambda principal=principal,rate=rate:fv(principal,rate,2))
 flows=[]
 def same_list(values):return values
 returned=same_list(flows);returned.append(D(1));check('3.4-E6','returned list shares caller state',(returned is flows,flows),(True,[D(1)]))
 # Exact introductory default function definition, without unrelated snippets.
 path=next((BOOK/'chapter-03').glob('3.05-*.md'));defs=[]
 for code in re.findall(r'^```python\n(.*?)^```',path.read_text(),re.M|re.S):
  try:tree=ast.parse(code)
  except SyntaxError:continue
  defs.extend(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='future_value_one_period')
 assert len(defs)==1
 state={'Decimal':D};exec(compile(ast.Module(defs,[]),'source_default_definition','exec'),state);one=state['future_value_one_period']
 check('3.5-E1','omitted/one/zero',(one(D(1000),D('.05')),one(D(1000),D('.05'),1),one(D(1000),D('.05'),0)),(D(1050),D(1050),D(1000)))
 check('3.5-E2','keywords in changed order',fv(periods=2,periodic_rate=D('.05'),present_value=D(1000)),D('1102.50'))
 # Teaching variant makes timing required and updates every lab call.
 tree=ast.parse(source[5])
 for node in tree.body:
  if isinstance(node,ast.FunctionDef) and node.name=='advance_balance':
   for i,arg in enumerate(node.args.kwonlyargs):
    if arg.arg=='contribution_timing':node.args.kw_defaults[i]=None
 class Calls(ast.NodeTransformer):
  def visit_Call(self,node):
   self.generic_visit(node)
   if isinstance(node.func,ast.Name) and node.func.id=='advance_balance' and not any(k.arg=='contribution_timing' for k in node.keywords):
    expansions=[k for k in node.keywords if k.arg is None]
    if expansions:
     assert len(expansions)==1
     expansions[0].value=ast.Dict([ast.Constant('contribution_timing'),None],[ast.Constant('end'),expansions[0].value])
    else:node.keywords.append(ast.keyword('contribution_timing',ast.Constant('end')))
   return node
 tree=ast.fix_missing_locations(Calls().visit(tree));variant=ast.unparse(tree)+'\n';(HERE/'required_timing_variant.py').write_text(variant);variant_state={};out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(tree,'required_timing_variant','exec'),variant_state)
 advance=variant_state['advance_balance'];raises('3.5-E3','keyword-only required timing','TypeError',lambda:advance(D(1000),D('.05')))
 check('3.5-E4','all updated lab checks execute','PASS: default and keyword argument checks' in out.getvalue(),True)
 check('3.5-E4','required explicit call',advance(D(1000),D('.05'),contribution_timing='end'),D(1050))
 original=spaces[5]['advance_balance']
 check('3.5-E5','zero rate timing equivalence',(original(D(1000),D(0),contribution=D(100),contribution_timing='end'),original(D(1000),D(0),contribution=D(100),contribution_timing='beginning')),(D(1100),D(1100)))
 for balance,rate in [(D('Infinity'),D('.05')),(D(1000),D('-1')),(D(1000),D('-1.01'))]:raises('3.5-E6','unsupported balance/rate','ValueError',lambda balance=balance,rate=rate:original(balance,rate))
 supplied=[];returned=spaces[5]['append_cash_flow'](D(1),supplied);check('3.5-E7','explicit empty list retained',returned is supplied,True)
 def replaces_empty(value,items=None):
  items=items or [];items.append(value);return items
 external=[];returned=replaces_empty(D(1),external);check('3.5-E7','truthiness replacement breaks ownership',(returned is external,len(external)),(False,0))
 def renamed(amount):return amount
 raises('3.5-E8','old keyword broken by rename','TypeError',lambda:renamed(principal=D(1)))
 namespace={'principal':D(1000)};exec('def local(principal):\n    principal=principal+1\n    return principal\n',namespace)
 check('3.6-E1','local rebinding versus module',(namespace['local'](D(10)),namespace['principal']),(D(11),D(1000)))
 project=spaces[6]['project_balance'];rates=[D('.03'),D('.07'),D('-.1')]
 first={rate:project(D(1000),rate,2) for rate in rates};reverse={rate:project(D(1000),rate,2) for rate in reversed(rates)}
 check('3.6-E2','negative scenario order independence',first,reverse);check('3.6-E2','negative known amount',first[D('-.1')],D(810))
 state={'rate':D('.05')};exec('def read_rate():\n    return rate\ndef update_rate(value):\n    global rate\n    rate=value\n',state);check('3.6-E3','global read',state['read_rate'](),D('.05'));state['update_rate'](D('.07'));check('3.6-E3','global rebinding explicit',state['rate'],D('.07'))
 def conditional(values):
  if values:answer=values[0]
  return answer
 raises('3.6-E4','empty conditional assignment','UnboundLocalError',lambda:conditional([]))
 def running_total():
  total=D(0)
  def add(value):
   nonlocal total
   total+=value
   return total
  return add
 a,b=running_total(),running_total();check('3.6-E5','independent closures',(a(D(1)),a(D(2)),b(D(10)),a(D(0))),(D(1),D(3),D(10),D(3)))
 closure=spaces[6]['make_projector'](D('-.1'));check('3.6-E6','enclosing captured rate survives',closure(D(1000),2),D(810))
 def explicit_rate(principal,rate):return principal*(1+rate)
 check('3.6-E7','explicit rate input',explicit_rate(D(1000),D('.05')),D(1050))
 def append_local(items):items.append(D(1))
 caller=[];append_local(caller);check('3.6-E8','local alias mutates caller',caller,[D(1)])
 from decimal import localcontext
 with localcontext() as c:
  c.prec=6;low=D(1)/D(7)
 with localcontext() as c:
  c.prec=28;high=D(1)/D(7)
 check('3.6-E9','explicit inputs do not fix context',low==high,False)
 output=dict(source_revision='7b9ee5df7c2f091b3bf260e185189b5e839de5ec',python=sys.version,platform=platform.platform(),exercise_records=25,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),source_provenance=provenance,teaching_variant_stdout=out.getvalue(),checks=checks)
 (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k not in ('source_provenance','checks','teaching_variant_stdout')},indent=2));return bool(output['failed'])

if __name__=='__main__':raise SystemExit(run())
