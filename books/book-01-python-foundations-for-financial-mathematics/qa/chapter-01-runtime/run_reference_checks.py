"""Run selected Chapter 1 examples and known-answer console fixtures.

Usage: python run_reference_checks.py CHAPTER01_DIR NEW_OUTPUT_DIR
Interactive stdin/output cases are not counted as unittest methods.
"""
import ast,hashlib,json,os,pathlib,platform,re,subprocess,sys
source=pathlib.Path(sys.argv[1]).resolve();output=pathlib.Path(sys.argv[2]).resolve()
if output.exists():raise SystemExit('Choose a new output directory to preserve prior evidence.')
output.mkdir(parents=True)
def section(n):return next(source.glob(f'1.{n:02}-*.md'))
def blocks(f):return [m.group(2) for m in re.finditer(r'(?ms)^(```|~~~)python[^\n]*\n(.*?)^\1\s*$',f.read_text())]
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1';env['MPLBACKEND']='Agg'
selection={1:[0],2:[0,1],3:[0,1],4:[0],5:[0,1,2,3],6:[0,14,17,20,21],7:[0,2,4,5,7,10,11,12,13,14,15,16,17,18,20,21,22,23],8:[0,11,12,13,22,27,28,29,30],9:[9,10,14,15,16,26,31,32,33],11:[0,1,2,3,4,6,7,8,9,10,11,12,14,15,17,18,20,21,22,23,26,28,29,30,31]}
results=[]
def launch(folder,name,args,data=None):
 p=subprocess.run([sys.executable,'-W','error::FutureWarning',*args],input=data,cwd=folder,env=env,text=True,capture_output=True,timeout=30)
 (folder/(name+'.log')).write_text(p.stdout+p.stderr)
 return p,{'operation':name,'command':[sys.executable,'-W','error::FutureWarning',*args],'returncode':p.returncode,'log':folder.name+'/'+name+'.log'}
for n,indices in selection.items():
 f=section(n);folder=output/f.stem;folder.mkdir();b=blocks(f);code='\n\n'.join(b[i] for i in indices);ast.parse(code);(folder/'examples.py').write_text(code)
 _,op=launch(folder,'examples',['examples.py']);_,comp=launch(folder,'compilation',['-m','compileall','-q','.']);results.append({'file':f.name,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'selected_python_block_indices':indices,'operations':[op,comp]});print(f.name,op['returncode'],flush=True)
companion=source/'solutions/1.13-solutions-and-reference-implementations.md';indices=[0,2,3,4,5,6,8,10,11,12,13,16,20];folder=output/'companion-selected-examples';folder.mkdir();b=blocks(companion);code='\n\n'.join(b[i] for i in indices);ast.parse(code);(folder/'examples.py').write_text(code);_,op=launch(folder,'examples',['examples.py']);_,comp=launch(folder,'compilation',['-m','compileall','-q','.']);results.append({'file':str(companion.relative_to(source)),'source_sha256':hashlib.sha256(companion.read_bytes()).hexdigest(),'selected_python_block_indices':indices,'operations':[op,comp]})
programs={'validated-input':(section(10),24),'project':(section(12),14),'savings':(companion,17),'trade':(companion,18),'reconciliation':(companion,19),'capstone':(companion,22)}
fixtures={
'validated-input':[
 ('known-value',['10000','5','3'],['Future value: $11,576.25']),
 ('period-zero',['10000','5','0'],['Future value: $10,000.00']),
 ('bad-number',['bad'],['Please enter valid numeric values.']),
 ('nonfinite',['nan','5','3'],['Principal and rate must be finite.']),
 ('negative-principal',['-1','5','3'],['Principal must be greater than zero']),
 ('negative-years',['10000','5','-1'],['Years cannot be negative'])],
'project':[
 ('simple-interest',['1','10000','5','3'],['Interest: $1,500.00','Ending Balance: $11,500.00']),
 ('monthly-compound',['2','10000','5','10','12'],['Future Value: $16,470.09']),
 ('percentage-change',['3','125','140'],['Percentage Change: 12.00%']),
 ('profit-loss',['4','50','58','100'],['Status: PROFIT','Profit/Loss: $800.00','Return: 16.00%']),
 ('posted-fee',['5','1250.75','1.25'],['Fee: $15.63','Total Paid: $1,266.38']),
 ('tolerance-inclusive',['6','1250000','1250000.01','0.01'],['Status: WITHIN TOLERANCE']),
 ('zero-denominator',['3','0','140'],['original value is zero']),
 ('negative-years',['2','1000','5','-1','12'],['Number of years cannot be negative']),
 ('zero-frequency',['2','1000','5','1','0'],['Compounding periods must be greater than zero']),
 ('nonfinite',['1','NaN'],['Invalid input: Financial input must be finite.']),
 ('bad-number',['1','bad'],['Invalid numeric input. Please enter valid numbers.']),
 ('invalid-menu',['9'],['Invalid calculator selection.']),
 ('negative-tolerance',['6','100','100','-0.01'],['Tolerance cannot be negative.']),
 ('outside-tolerance',['6','100','100.011','0.01'],['Status: RECONCILIATION EXCEPTION']),
 ('subcent-gain',['4','0.10','0.104','1'],['Status: PROFIT','Profit/Loss: $0.00','Return: 4.00%']),
 ('subcent-loss',['4','0.10','0.096','1'],['Status: LOSS','Profit/Loss: $-0.00','Return: -4.00%']),
 ('zero-rate',['2','10000','0','10','12'],['Future Value: $10,000.00']),
 ('period-zero',['2','10000','5','0','12'],['Future Value: $10,000.00'])],
'capstone':[
 ('simple-interest',['1','10000','5','3'],['Interest: $1,500.00','Ending balance: $11,500.00']),
 ('annual-compound',['2','10000','5','10'],['Future value: $16,288.95']),
 ('percentage-change',['3','125','140'],['Percentage change: 12.00%']),
 ('profit-loss',['4','50','58','100'],['Profit/Loss: $800.00','Return: 16.00%']),
 ('posted-fee',['5','1250.75','1.25'],['Fee: $15.63','Total paid: $1,266.38']),
 ('tolerance-inclusive',['6','100','100.01','0.01'],['Status: RECONCILED']),
 ('invalid-menu',['9'],['Invalid menu option.']),
 ('bad-number',['1','bad'],['Invalid financial input.']),
 ('nonfinite',['1','NaN'],['Invalid financial input.']),
 ('zero-growth-factor',['2','1000','-100','1'],['Invalid financial input.']),
 ('negative-periods',['2','1000','5','-1'],['Invalid financial input.']),
 ('zero-quantity',['4','50','58','0'],['Invalid financial input.']),
 ('negative-fee',['5','100','-1'],['Invalid financial input.']),
 ('negative-tolerance',['6','100','100','-1'],['Invalid financial input.']),
 ('zero-denominator',['3','0','140'],['Invalid financial input.']),
 ('zero-initial-value',['4','0','1','1'],['Profit/Loss: $1.00','Return: undefined']),
 ('subcent-gain',['4','0.10','0.104','1'],['Profit/Loss: $0.00','Return: 4.00%'])],
'savings':[
 ('monthly-growth',['10000','5','10','12'],['Future value: $16,470.09','Total growth: $6,470.09']),
 ('half-year',['10000','5','0.5','12'],['Future value: $10,252.62']),
 ('fractional-discrete-period',['10000','5','0.1','12'],['Invalid financial input.']),
 ('zero-frequency',['10000','5','1','0'],['Invalid financial input.']),
 ('zero-growth-factor',['10000','-1200','1','12'],['Invalid financial input.']),
 ('nonfinite',['NaN'],['Invalid financial input.'])],
'trade':[
 ('two-sided-fees',['50','58','100','1'],['Purchase fee: $50.00','Sale fee: $58.00','Net profit/loss: $692.00','Return: 13.70%']),
 ('zero-quantity',['50','58','0','1'],['Invalid financial input.']),
 ('zero-initial-value',['0','1','1','0'],['Net profit/loss: $1.00','Return: undefined']),
 ('negative-fee',['50','58','100','-1'],['Invalid financial input.'])],
'reconciliation':[
 ('tolerance-inclusive',['100','100.01','0.01'],['Status: RECONCILED']),
 ('outside-tolerance',['100','100.011','0.01'],['Status: RECONCILIATION EXCEPTION']),
 ('negative-tolerance',['100','100','-1'],['Invalid financial input.']),
 ('nonfinite',['NaN'],['Invalid financial input.'])]}
program_results=[]
for name,(f,index) in programs.items():
 folder=output/name;folder.mkdir();code=blocks(f)[index];ast.parse(code);(folder/'program.py').write_text(code);cases=[]
 for case,values,expected in fixtures[name]:
  stdin='\n'.join(values)+'\n';proc,op=launch(folder,case,['program.py'],stdin);normalized=' '.join(proc.stdout.split());missing=[s for s in expected if ' '.join(s.split()) not in normalized]
  record={**op,'stdin':stdin,'expected_output_contains':expected,'missing_output':missing,'stderr_empty':proc.stderr=='','status':'PASS' if proc.returncode==0 and not missing and proc.stderr=='' else 'FAIL'};cases.append(record)
  if record['status']!='PASS':print('FAIL',name,case,missing,proc.stderr,flush=True)
 _,comp=launch(folder,'compilation',['-m','compileall','-q','.']);program_results.append({'program':name,'file':str(f.relative_to(source)),'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'python_block_index':index,'cases':cases,'compilation':comp});print(name,len(cases),'cases',sum(x['status']=='PASS' for x in cases),'passed',flush=True)
versions={}
from importlib.metadata import version
for package in ('numpy','pandas','matplotlib'):versions[package]=version(package)
evidence={'environment':{'python':platform.python_version(),'platform':platform.platform(),'imported_package_versions':versions},'unit_test_methods':0,'example_groups':results,'interactive_programs':program_results,'comparison':'Expected output fragments matched after whitespace normalization; child exit zero and stderr empty required. Input errors intentionally printed by the educational scripts can exit zero.'}
(output/'results.json').write_text(json.dumps(evidence,indent=2)+'\n')
(output/'all-checks.log').write_text(''.join('\n===== '+r['file']+' / '+op['operation']+' =====\n'+(output/op['log']).read_text() for r in results for op in r['operations'])+''.join('\n===== '+p['program']+' / '+c['operation']+' =====\n'+(output/c['log']).read_text() for p in program_results for c in p['cases']+[p['compilation']]))
if any(op['returncode'] for r in results for op in r['operations']) or any(p['compilation']['returncode'] or any(c['status']!='PASS' for c in p['cases']) for p in program_results):sys.exit(1)
