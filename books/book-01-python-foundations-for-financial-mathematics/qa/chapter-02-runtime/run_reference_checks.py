"""Execute selected Chapter 2 examples and controlled scenario-analyzer cases.

Usage: python run_reference_checks.py CHAPTER02_DIR NEW_OUTPUT_DIR
No unittest methods are added or counted. Constant overrides are controlled data.
"""
import ast,hashlib,json,os,pathlib,platform,re,subprocess,sys
from decimal import Decimal,localcontext
source=pathlib.Path(sys.argv[1]).resolve();output=pathlib.Path(sys.argv[2]).resolve()
if output.exists():raise SystemExit('Choose a new output directory to preserve prior evidence.')
output.mkdir(parents=True)
def blocks(f):return [m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
def section(n):return next(source.glob(f'2.{n:02}-*.md'))
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1'
selection={1:[4,5,8,9,10,16],2:[0,2,4,6,8,10,11],3:[0,1,6,7,8,12,15],4:[4,5,6,7,20,21,22,23,24,25,26],5:[9,11,13,17],6:[4,5,6,7,8],7:[2,4,5,6],8:[42,43,44],9:[21,22,23],10:[22,23,24],11:[13,14,15,16]}
results=[]
def run(folder,label,args):
 proc=subprocess.run([sys.executable,'-W','error::FutureWarning',*args],cwd=folder,env=env,text=True,capture_output=True,timeout=20)
 (folder/(label+'.log')).write_text(proc.stdout+proc.stderr)
 return proc,{'operation':label,'returncode':proc.returncode,'command':[sys.executable,'-W','error::FutureWarning',*args],'log':folder.name+'/'+label+'.log'}
for n,indices in selection.items():
 f=section(n);b=blocks(f);folder=output/f.stem;folder.mkdir();code='from decimal import Decimal\n\n'+'\n\n'.join(b[i] for i in indices);ast.parse(code);(folder/'examples.py').write_text(code)
 _,op=run(folder,'examples',['examples.py']);_,comp=run(folder,'compilation',['-m','compileall','-q','.'])
 results.append({'file':f.name,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'selected_python_block_indices':indices,'prelude':'from decimal import Decimal','operations':[op,comp]});print(f.name,op['returncode'],flush=True)
f=source/'solutions/2.13-solutions-and-reference-implementations.md';indices=[0,1,2,3,4,5,7,8];b=blocks(f);folder=output/'companion-selected-examples';folder.mkdir();(folder/'examples.py').write_text('from decimal import Decimal\n\n'+'\n\n'.join(b[i] for i in indices));_,op=run(folder,'examples',['examples.py']);_,comp=run(folder,'compilation',['-m','compileall','-q','.']);results.append({'file':str(f.relative_to(source)),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'selected_python_block_indices':indices,'prelude':'from decimal import Decimal','operations':[op,comp]})
project_file=section(12);project=blocks(project_file)[0]
cases=[
 ('baseline',{},None),
 ('zero-rate-last-year',{'return_scenarios':"[Decimal('0')]",'maximum_years':'15'},None),
 ('zero-rate-beyond-horizon',{'return_scenarios':"[Decimal('0')]",'maximum_years':'14'},None),
 ('already-reached',{'target_balance':"Decimal('25000')",'return_scenarios':"[Decimal('0'),Decimal('0.05'),Decimal('-0.5')]"},None),
 ('invalid-and-zero-rates',{'return_scenarios':"[None,True,'0.05',Decimal('NaN'),Decimal('Infinity'),Decimal('-1'),Decimal('-1.10'),Decimal('0')]"},None),
 ('reversed-scenarios',{'return_scenarios':"[Decimal('0.09'),Decimal('0.07'),Decimal('0.05'),Decimal('0.03')]"},None),
 ('boolean-horizon',{'maximum_years':'True'},'Maximum years must be an integer.'),
 ('zero-horizon',{'maximum_years':'0'},'Maximum years must be greater than zero.'),
 ('oversized-horizon',{'maximum_years':'101'},'Maximum years exceeds the supported model horizon.'),
 ('negative-contribution',{'annual_contribution':"Decimal('-1')"},'Annual contribution cannot be negative.'),
 ('nonfinite-initial',{'initial_investment':"Decimal('NaN')"},'Initial investment must be finite.'),
 ('zero-target',{'target_balance':"Decimal('0')"},'Target balance must be greater than zero.'),
]
probe='''import contextlib,io,json,runpy,sys
out=io.StringIO()
with contextlib.redirect_stdout(out): state=runpy.run_path(sys.argv[1])
record={k:state.get(k) for k in ('errors','results','rejections','total_scenarios','evaluated_scenarios','rejected_scenarios','target_reached_scenarios','target_not_reached_scenarios')}
record['program_stdout']=out.getvalue()
print(json.dumps(record,default=str))
'''
project_results=[]
def closed_form(p,c,r,n):
 if r==0:return p+c*n
 power=(1+r)**n
 return p*power+c*(power-1)/r
for name,overrides,expected_error in cases:
 folder=output/('project-'+name);folder.mkdir();code=project
 if overrides:
  tree=ast.parse(project);changed=set()
  for node in tree.body:
   if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in overrides:
    key=node.targets[0].id;node.value=ast.parse(overrides[key],mode='eval').body;changed.add(key)
  if changed!=set(overrides):raise ValueError('unknown override')
  code=ast.unparse(ast.fix_missing_locations(tree))+'\n'
 (folder/'analyzer.py').write_text(code);proc,op=run(folder,'scenario',['-c',probe,'analyzer.py']);check_errors=[];record=None
 if proc.returncode==0:
  record=json.loads(proc.stdout);(folder/'program.log').write_text(record['program_stdout'])
  if expected_error:
   if expected_error not in record['errors'] or record['results'] is not None:check_errors.append('shared validation rejection mismatch')
  else:
   if record['errors']:check_errors.append('unexpected shared validation error')
   rates=['0.03','0.05','0.07','0.09'];p=Decimal('25000');c=Decimal('5000');target=Decimal('100000');h=20;rejected=0
   if name.startswith('zero-rate-'):rates=['0'];h=15 if name.endswith('last-year') else 14
   if name=='already-reached':rates=['0','0.05','-0.5'];target=Decimal('25000')
   if name=='invalid-and-zero-rates':rates=['0'];rejected=7
   if name=='reversed-scenarios':rates=list(reversed(rates))
   if record['evaluated_scenarios']!=len(rates) or record['rejected_scenarios']!=rejected or record['total_scenarios']!=len(rates)+rejected or len(record['rejections'])!=rejected:check_errors.append('scenario accounting mismatch')
   if [x['annual_return'] for x in record['results']]!=rates:check_errors.append('scenario order or inclusion mismatch')
   for row in record['results']:
    r=Decimal(row['annual_return'])
    with localcontext() as ctx:
     ctx.prec=50
     expected_year=0 if p>=target else next((n for n in range(1,h+1) if closed_form(p,c,r,n)>=target),None)
     expected_balance=closed_form(p,c,r,expected_year if expected_year is not None else h)
    if row['target_year']!=expected_year or abs(Decimal(row['ending_balance'])-expected_balance)>Decimal('1e-18'):check_errors.append('closed-form amount or first-crossing mismatch')
   reached=sum(row['target_year'] is not None for row in record['results'])
   if reached!=record['target_reached_scenarios'] or len(rates)-reached!=record['target_not_reached_scenarios']:check_errors.append('target accounting mismatch')
 else:check_errors.append('analyzer execution failed')
 _,comp=run(folder,'compilation',['-m','compileall','-q','.'])
 status='PASS' if not check_errors and comp['returncode']==0 else 'FAIL'
 project_results.append({'case':name,'constant_overrides':overrides,'expected_shared_error':expected_error,'status':status,'check_errors':check_errors,'record':record,'operations':[op,comp]});print('project',name,status,flush=True)
evidence={'environment':{'python':platform.python_version(),'platform':platform.platform(),'dependencies':'Python standard library'},'unit_test_methods':0,'example_groups':results,'project_source':{'file':project_file.name,'source_sha256':hashlib.sha256(project_file.read_bytes()).hexdigest(),'python_block_index':0},'project_cases':project_results,'benchmark':'50-digit Decimal closed-form accumulation with end-of-period contributions; amount absolute tolerance 1e-18; first-crossing year and accounting checked exactly'}
(output/'results.json').write_text(json.dumps(evidence,indent=2)+'\n')
(output/'all-checks.log').write_text(''.join('\n===== '+r['file']+' / '+op['operation']+' =====\n'+(output/op['log']).read_text() for r in results for op in r['operations'])+''.join('\n===== project '+r['case']+' / '+op['operation']+' =====\n'+(output/op['log']).read_text() for r in project_results for op in r['operations']))
if any(op['returncode'] for r in results for op in r['operations']) or any(r['status']!='PASS' for r in project_results):sys.exit(1)
