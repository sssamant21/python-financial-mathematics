"""Execute pinned/working sole Section2.12 fence with declared AST fixture substitutions.
Usage: python THIS baseline|working output_stem
"""
import ast,contextlib,io,json,sys,re,subprocess,hashlib,platform
from pathlib import Path
from fractions import Fraction
here=Path(__file__).resolve().parent;root=here.parents[3];path='books/book-01-python-foundations-for-financial-mathematics/chapter-02/2.12-chapter-project-investment-scenario-analyzer.md';pin='e9ec4a06368bd666e2e50ed77efdb224d5faad0e'
mode,stem=sys.argv[1:3];assert mode in ('baseline','working','corrected');raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root) if mode=='baseline' else (subprocess.check_output(['git','cat-file','blob','4cae6d150a26cb0a231e6e33d75f74a669dedef4'],cwd=root) if mode=='corrected' else (root/path).read_bytes())
if mode!='baseline':assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='4cae6d150a26cb0a231e6e33d75f74a669dedef4'
code=re.findall(r'```python\n(.*?)```',raw.decode(),re.S);assert len(code)==1;records=[]
def execute(overrides):
 tree=ast.parse(code[0]);seen=set()
 for node in tree.body:
  if isinstance(node,ast.Assign):
   for name in node.targets:
    if isinstance(name,ast.Name) and name.id in overrides:node.value=ast.parse(overrides[name.id],mode='eval').body;seen.add(name.id)
 assert seen==set(overrides);ast.fix_missing_locations(tree);state={};out=io.StringIO();exc=None
 try:
  with contextlib.redirect_stdout(out):exec(compile(tree,path,'exec'),state)
 except Exception as e:exc=dict(type=type(e).__name__,message=str(e))
 return state,out.getvalue(),exc
for field,label in [('initial_investment','Initial investment'),('annual_contribution','Annual contribution'),('target_balance','Target balance')]:
 for tag,value in [('str',"'25000'"),('int','25000'),('float','25000.0'),('bool','True'),('None','None'),('list','[]'),('bytes',"b'25000'")]:
  state,out,exc=execute({field:value});expected=label+' must be Decimal.';ok=exc is None and state.get('errors')==[expected] and 'results' not in state
  records.append(dict(case=field+' '+tag,kind='representation guard',fixture_expression=value,expected=expected,exception=exc,stdout=out,passed=ok))
 for value in ['NaN','sNaN','Infinity','-Infinity']:
  state,out,exc=execute({field:'Decimal('+repr(value)+')'});ok=exc is None and state.get('errors')==[label+' must be finite.'] and 'results' not in state
  records.append(dict(case=field+' '+value,kind='finite guard',exception=exc,stdout=out,passed=ok))
# Independent closed-form reference for unchanged supported baseline first crossings and balances.
state,out,exc=execute({});assert exc is None
for row in state['results']:
 P=Fraction(25000);C=Fraction(5000);R=Fraction(row['annual_return']);T=Fraction(100000)
 def balance(n):return P*(1+R)**n+C*((1+R)**n-1)/R
 year=next((n for n in range(21) if balance(n)>=T),None);n=20 if year is None else year;expected=balance(n);actual=Fraction(row['ending_balance']);tolerance=max(Fraction(1),abs(expected))*Fraction(1,10**26)
 records.append(dict(case='supported '+str(R),kind='independent finance',expected_year=year,actual_year=row['target_year'],expected_balance=str(expected),actual_balance=str(row['ending_balance']),absolute_tolerance=str(tolerance),passed=row['target_year']==year and abs(actual-expected)<=tolerance))
# Reject all three representations together before any scenario loop.
state,out,exc=execute(dict(initial_investment="'25000'",annual_contribution='5.',target_balance='True'))
records.append(dict(case='all shared representations',kind='aggregate guard',stdout=out,exception=exc,passed=exc is None and len(state.get('errors',[]))==3 and 'results' not in state))
result=dict(mode=mode,baseline_revision=pin,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=hashlib.sha256(code[0].encode()).hexdigest(),python=sys.version,platform=platform.platform(),records=records,passed=sum(x['passed'] for x in records),failed=sum(not x['passed'] for x in records),limits='Declared AST fixture assignments only;rest of exact fence unchanged. Typed Decimal rejection policy,not arbitrary external parsing or all-range Decimal/model/independent approval.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(mode,result['passed'],'passed',result['failed'],'failed')
raise SystemExit(bool(result['failed']))
