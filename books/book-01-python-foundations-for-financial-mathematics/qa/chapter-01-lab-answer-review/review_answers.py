"""Check worked answers using Fraction/int oracles, separate from Decimal source."""
import ast,contextlib,hashlib,io,json,pathlib,re,sys
from decimal import Decimal,InvalidOperation,ROUND_HALF_EVEN,ROUND_HALF_UP,localcontext
from fractions import Fraction as F
from unittest.mock import patch
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
if out.exists():raise SystemExit('Choose a new output directory')
out.mkdir(parents=True);source=root/'chapter-01/solutions/1.13-solutions-and-reference-implementations.md';text=source.read_text();parser=MarkdownIt();rows=[]
def decimal_text(value):
 value=F(value);sign='-' if value<0 else '';n,d=abs(value.numerator),value.denominator;q,r=divmod(n,d);digits=[]
 while r and len(digits)<300:
  qdigit,r=divmod(r*10,d);digits.append(str(qdigit))
 if r:raise ValueError('Nonterminating exact decimal')
 return sign+str(q)+('.'+''.join(digits) if digits else '')
def cents(value,even=False):
 value=F(value);q,r=divmod(abs(value.numerator)*100,value.denominator)
 if 2*r>value.denominator or (2*r==value.denominator and (not even or q%2)):q+=1
 return ('-' if value<0 and q else '')+str(q//100)+'.'+str(q%100).zfill(2)
def sec(n):
 m=re.search(r'^## Solution '+str(n)+r' — .*\n',text,re.M);end=re.search(r'^#{1,2} ',text[m.end():],re.M);return text[m.start():m.end()+end.start() if end else len(text)]
def blocks(s):return [t.content for t in parser.parse(s) if t.type=='fence' and t.info.strip()=='python']
conventions=blocks(text)[0]
def run(n,setup=None,stdin=()):
 ns={'Decimal':Decimal,'InvalidOperation':InvalidOperation,'ROUND_HALF_UP':ROUND_HALF_UP,'ROUND_HALF_EVEN':ROUND_HALF_EVEN};exec(conventions,ns);ns.update(setup or {});capture=io.StringIO()
 with patch('builtins.input',side_effect=list(stdin)),contextlib.redirect_stdout(capture):
  for code in blocks(sec(n)):exec(compile(code,f'Solution-{n}','exec'),ns)
 return ns,capture.getvalue()
def record(n,label,expected,actual):
 passed=expected==actual;rows.append({'solution':n,'check':label,'expected':expected,'actual':actual,'status':'PASS' if passed else 'FAIL'});return passed
def value(n,name,expected,setup=None):
 ns,_=run(n,setup);actual=F(ns[name]);record(n,name,str(F(expected)),str(actual))
def prose(n,check,needle):record(n,check,True,needle in sec(n).replace('\\%','%'))
# Direct execution of reference snippets with exact rational expectations.
value(4,'interest',6000)
ns,_=run(5);types=[type(eval(compile(ast.Expression(x.value),'types','eval'),ns)).__name__ for x in ast.parse(blocks(sec(5))[0]).body if isinstance(x,ast.Expr)];record(5,'literal types',['int','float','str','bool','Decimal'],types)
record(6,'different decimal construction',True,Decimal('.1')!=Decimal(.1))
value(7,'interest_rate',F(19,400));value(8,'new_balance',10800);value(9,'transaction_value',F(21375,4))
for s in ['0.05','0.0725','0.005','0.1275','-0.0025']:prose(10,'percentage conversion '+s,s)
value(11,'ending_balance',31000,{'principal':Decimal('25000'),'rate':Decimal('.06'),'years':Decimal('4')})
exact=F(5000)*F(26,25)**8;ns,_=run(12);record(12,'source calculation exact value',str(exact),str(F(ns['amount'])));m=re.search(r'Unrounded result: `([^`]+)`',sec(12));record(12,'printed exact answer',decimal_text(exact),m.group(1) if m else None);record(12,'final half-up cents',cents(exact),str(ns['display_amount']))
ns,printed=run(13,stdin=['10000','5','3']);record(13,'interpreted input display',['Interpreted principal: 10000','Interpreted annual decimal rate: 0.05','Interpreted years: 3'],printed.splitlines());record(13,'rate conversion','1/20',str(F(ns['annual_rate'])))
value(14,'rate',F(13,200));_,printed=run(15);record(15,'monetary formatting','$1,234,567.80\n',printed)
record(16,'float and Decimal differ',True,F(.1+.2)!=F(Decimal('.1')+Decimal('.2')))
for x in ['125.665','125.675']:
 for rounding,even in [(ROUND_HALF_UP,False),(ROUND_HALF_EVEN,True)]:record(17,x+' '+rounding,cents(F(x),even),str(Decimal(x).quantize(Decimal('.01'),rounding=rounding)))
for x in ['12.345','99.999','1000.005','0.004']:
 expected=cents(F(x));actual=str(Decimal(x).quantize(Decimal('.01'),rounding=ROUND_HALF_UP));record(18,'round '+x,expected,actual);prose(18,'tabulated '+expected,expected)
final_only=cents(F(1,10)*F(21,20)**2);posted=F(cents(F(1,10)*F(21,20)));posted=F(cents(posted*F(21,20)));record(19,'rounding-stage counterexample',['0.11','0.12'],[final_only,cents(posted)])
for n,p,r,t in [(20,F(12500),F(9,200),F(3)),(21,F(10000),F(0),F(5)),(22,F(8000),F(3,50),F(3,2))]:
 interest=p*r*t
 expected={20:'1687.50',21:'10000',22:'720'}[n];prose(n,'stated numeric benchmark',expected);rows.append({'solution':n,'check':'independent simple-interest derivation','rational_interest':str(interest),'rational_ending':str(p+interest),'expected_display_interest':cents(interest),'status':'BENCHMARK_RECORDED'})
annual=F(15000)*F(21,20)**10;value(23,'future_value',annual);prose(23,'annual cent answer',cents(annual).replace('24433','24,433'))
monthly=F(15000)*F(241,240)**120;prose(24,'monthly cent answer',cents(monthly).replace('24705','24,705'));record(24,'frequency comparison',True,monthly>annual)
for freq in [0,-1,12]:
 try:run(25,{'periods_per_year':freq});actual='accepted'
 except ValueError:actual='rejected'
 record(25,'frequency '+str(freq),'rejected' if freq<=0 else 'accepted',actual)
for n,start,end,pct in [(26,80,92,15),(27,120,102,-15),(29,-100,-50,-50)]:
 actual=(F(end)-F(start))/F(start)*100;record(n,'exact percentage',str(F(pct)),str(actual));prose(n,'printed percent',str(pct)+'%')
prose(28,'zero-denominator explanation','zero')
for n,buy,sell,qty in [(30,F('32.5'),F('37.8'),F(250)),(31,F(75),F(68),F(150)),(32,F(40),F(40),F(500)),(33,F('125.4'),F('132.1'),F('2.75'))]:
 cost=buy*qty;gain=(sell-buy)*qty;ret=gain/cost*100;rows.append({'solution':n,'check':'exact trade benchmark','initial_investment':decimal_text(cost),'raw_profit_loss':decimal_text(gain),'display_profit_loss':cents(gain),'return_percent_fraction':str(ret),'status':'BENCHMARK_RECORDED'})
for n,needle in [(30,'1325'),(31,'1,050.00'),(32,'BREAK-EVEN'),(33,'18.425'),(33,'344.85'),(33,'5.342903')]:prose(n,'stated trade answer '+needle,needle)
raw_fee=F(4250)*F(7,400);posted_fee=F(cents(raw_fee));record(34,'fee oracle',['74.375','74.38','4324.38'],[decimal_text(raw_fee),cents(raw_fee),cents(F(4250)+posted_fee)])
for n,needles in [(34,['74.375','74.38','4,324.38']),(35,['4,175.62'])]:
 for needle in needles:prose(n,'stated posted-fee result '+needle,needle)
for n,a,b,tol in [(36,'750000','750000','.01'),(37,'1000','1000.006','.01'),(38,'1000','1000.01','.01'),(39,'1000','1000.011','.01')]:
 diff=abs(F(a)-F(b));record(n,'reconciliation decision',n!=39,diff<=F(tol));prose(n,'printed difference',decimal_text(diff))
prose(40,'negative tolerance rejection','rejected')
with localcontext() as ctx:
 ctx.traps[InvalidOperation]=True
 try:Decimal('abc');actual='no exception'
 except InvalidOperation:actual='InvalidOperation'
 record(41,'trapped malformed input','InvalidOperation',actual)
 ctx.traps[InvalidOperation]=False;ctx.clear_flags();x=Decimal('abc');record(41,'untrapped malformed input',[True,True],[x.is_nan(),ctx.flags[InvalidOperation]])
for x in ['NaN','Infinity','-Infinity']:record(42,x+' finite',False,Decimal(x).is_finite())
ns,_=run(43)
for raw,wanted in [('125.75','125.75'),(' 125.75 ','125.75'),('abc','InvalidOperation'),('NaN','ValueError'),('Infinity','ValueError')]:
 try:
  with patch('builtins.input',return_value=raw):actual=str(ns['read_decimal']('Amount: '))
 except (ValueError,InvalidOperation) as exc:actual=type(exc).__name__
 record(43,'read_decimal '+repr(raw),wanted,actual)
record(44,'five percent as fraction','1/20',str(F(5)/100));record(45,'float-to-decimal difference',True,F(Decimal(.1))!=F(1,10));prose(46,'zero guard','old_value != 0')
record(47,'premature rounding changes decision',[False,True],[F('.011')<=F('.01'),F(cents(F('.011')))<=F('.01')])
value(48,'result',F('125.67'),{'amount':Decimal('125.665')})
# Bind the qualitative review inventory to each exercise and solution section.
exercise=root/'chapter-01/1.13-exercises-and-applied-problems.md';ex=exercise.read_text();rubric=[]
for n in range(1,49):
 m=re.search(r'^### .*Exercise '+str(n)+r' — .*$',ex,re.M);assert m;end=re.search(r'^#{1,3} ',ex[m.end():],re.M);prompt=ex[m.start():m.end()+end.start() if end else len(ex)]
 rubric.append({'id':f'E{n:02}','exercise_heading':m.group(0),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'solution_sha256':hashlib.sha256(sec(n).encode()).hexdigest(),'automated_checks':[r['check'] for r in rows if r['solution']==n],'review_state':'TECHNICAL_REVIEW_SCOPED','scope':'Prompt/answer alignment, stated assumptions/units and bounded numerical/Python semantics; independent human/model/editorial acceptance remains pending.'})
(out/'answer-checks.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'checks':rows,'pass':sum(r['status']=='PASS' for r in rows),'fail':sum(r['status']=='FAIL' for r in rows)},indent=2)+'\n');(out/'exercise-review-register.json').write_text(json.dumps(rubric,indent=2)+'\n');(out/'rational-benchmarks.json').write_text(json.dumps({'solution12':{'fraction':str(exact),'exact_decimal':decimal_text(exact),'display':cents(exact)},'solution23_annual':{'fraction':str(annual),'display':cents(annual)},'solution24_monthly':{'fraction':str(monthly),'display':cents(monthly)}},indent=2)+'\n')
print(json.dumps({'checks':len(rows),'failed':[r for r in rows if r['status']=='FAIL']},indent=2));sys.exit(any(r['status']=='FAIL' for r in rows))
