"""Controlled project/applied/capstone runs with Fraction/int monetary oracles."""
import hashlib,json,os,pathlib,re,subprocess,sys
from fractions import Fraction as F
from markdown_it import MarkdownIt
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
if out.exists():raise SystemExit('Choose a new output directory')
out.mkdir(parents=True);p=MarkdownIt();cases=[];results=[]
def cents(x):
 x=F(x);q,r=divmod(abs(x.numerator)*100,x.denominator);q+=2*r>=x.denominator
 return ('-' if x<0 and q else '')+f'{q//100:,}.'+str(q%100).zfill(2)
def add(name,program,values,expected,reason):cases.append(dict(name=name,program=program,stdin='\n'.join(values)+'\n',expected=expected,reason=reason))
for name,pr,rate,years in [('simple-interest','12500','4.5','3'),('zero-rate','10000','0','5'),('fractional-time','8000','6','1.5'),('negative-rate','1000','-5','1'),('large-finite','100000000000000000000','0','1')]:
 interest=F(pr)*F(rate)/100*F(years);add(name,'project',['1',pr,rate,years],['Interest: $'+cents(interest),'Ending Balance: $'+cents(F(pr)+interest)],'Prt oracle; finite model inputs; signs and time units explicit')
for m in ['1','12']:
 fv=F(15000)*(1+F(5,100)/int(m))**(10*int(m));add('compound-m'+m,'project',['2','15000','5','10',m],['Future Value: $'+cents(fv)],'Exact rational growth; final-only cent half-up rounding')
for old,new in [('80','92'),('120','102'),('-100','-50')]:add('percentage-'+old,'project',['3',old,new],['Percentage Change: '+cents((F(new)-F(old))/F(old)*100)+'%'],'Signed nonzero denominator; mathematical percentage interpretation')
for name,buy,sell,qty in [('profit','32.50','37.80','250'),('loss','75','68','150'),('break-even','40','40','500'),('fractional-quantity','125.40','132.10','2.75'),('subcent-profit','.10','.104','1')]:
 gain=(F(sell)-F(buy))*F(qty);ret=gain/(F(buy)*F(qty))*100;add(name,'project',['4',buy,sell,qty],['Status: '+('PROFIT' if gain>0 else 'LOSS' if gain<0 else 'BREAK-EVEN'),'Profit/Loss: $'+cents(gain),'Return: '+cents(ret)+'%'],'Return and sign use unrounded computational gain')
fee=F(cents(F(4250)*F('1.75')/100).replace(',',''));add('posted-fee','project',['5','4250','1.75'],['Fee: $'+cents(fee),'Total Paid: $'+cents(F(4250)+fee)],'Cent-posted fee reused as required by this policy')
for b in ['1000','1000.006','1000.01','1000.011']:
 wanted='WITHIN TOLERANCE' if abs(F(b)-1000)<=F('.01') else 'RECONCILIATION EXCEPTION';add('reconciliation-'+b,'project',['6','1000',b,'.01'],['Status: '+wanted],'Compare exact difference before formatting')
for name,values,needle in [('zero-denominator',['3','0','50'],'original value is zero'),('invalid-text',['1','abc'],'Invalid numeric input'),('nonfinite',['1','Infinity'],'must be finite'),('bad-integer',['2','1000','5','1','12.5'],'Invalid input:'),('negative-tolerance',['6','100','100','-.01'],'Tolerance cannot be negative')]:add(name,'project',values,[needle],'Declared invalid-input or domain boundary')
fv=F(15000)*F(241,240)**120;add('savings-monthly','savings',['15000','5','10','12'],['Future value: $'+cents(fv),'Total growth: $'+cents(fv-15000)],'Applied Problem 1 exact rational benchmark')
add('savings-fractional-period','savings',['15000','5','.1','12'],['Invalid financial input.'],'Reject 1.2 discrete periods rather than truncate')
for name,buy,sell,q,rate in [('trade-posted-fees','32.5','37.8','250','1'),('trade-fractional-fees','125.4','132.1','2.75','1.75')]:
 cost=F(buy)*F(q);sale=F(sell)*F(q);bf=F(cents(cost*F(rate)/100).replace(',',''));sf=F(cents(sale*F(rate)/100).replace(',',''));gain=sale-sf-cost-bf;ret=gain/(cost+bf)*100;add(name,'trade',[buy,sell,q,rate],['Purchase fee: $'+cents(bf),'Sale fee: $'+cents(sf),'Net profit/loss: $'+cents(gain),'Return: '+cents(ret)+'%'],'Two separately posted fees; return uses total cost and raw net gain')
for b in ['1000','1000.006','1000.01','1000.011']:
 wanted='RECONCILED' if abs(F(b)-1000)<=F('.01') else 'RECONCILIATION EXCEPTION';add('applied-reconcile-'+b,'reconciliation',['1000',b,'.01'],['Status: '+wanted],'Applied Problem 3 exact decision boundary')
expected=[]
for name,r in [('A',F(1,25)),('B',F(1,20)),('C',F(3,50))]:
 fv=F(10000)*(1+r)**10;expected.append(name+' $10,000.00 '+cents(r*100)+'% $'+cents(fv)+' $'+cents(fv-10000))
add('scenario-comparison','scenarios',[],expected,'Applied Problem 4 independent scenario endpoints and growth')
for name,values,expected in [('console-success',['1','12500','4.5','3'],['Interest: $1,687.50','Ending balance: $14,187.50']),('console-zero',['1','10000','0','5'],['Interest: $0.00']),('console-invalid',['1','abc'],['Invalid financial input.']),('console-rounding',['5','125.665','100'],['Fee: $125.67','Total paid: $251.34']),('console-reconciliation',['6','1000','1000.01','.01'],['Status: RECONCILED'])]:add(name,'capstone',values,expected,'Required capstone success/zero/invalid/rounding/reconciliation demonstration')
add('nan-input','project',['1','NaN'],['must be finite'],'Explicit NaN rejection in the complete calculator')
project=next((root/'chapter-01').glob('1.12-*.md'));comp=root/'chapter-01/solutions/1.13-solutions-and-reference-implementations.md'
def blocks(f):return [x.content for x in p.parse(f.read_text()) if x.type=='fence' and x.info.strip()=='python']
b=blocks(comp);programs={'project':(project,14,blocks(project)[14]),'savings':(comp,17,b[17]),'trade':(comp,18,b[18]),'reconciliation':(comp,19,b[19]),'scenarios':(comp,20,b[20]),'capstone':(comp,22,b[22])}
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None);env['PYTHONDONTWRITEBYTECODE']='1'
for case in cases:
 folder=out/case['name'];folder.mkdir();src,index,code=programs[case['program']];(folder/'program.py').write_text(code);proc=subprocess.run([sys.executable,'program.py'],cwd=folder,env=env,input=case['stdin'],capture_output=True,text=True,timeout=20);normal=' '.join(proc.stdout.split());missing=[s for s in case['expected'] if ' '.join(s.split()) not in normal];record={**case,'source':str(src.relative_to(root)),'python_block_index':index,'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'command':[sys.executable,'program.py'],'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'missing':missing,'status':'PASS' if proc.returncode==0 and proc.stderr=='' and not missing else 'FAIL'};results.append(record)
(out/'results.json').write_text(json.dumps({'python':sys.version,'cases':results},indent=2)+'\n');print(json.dumps({'cases':len(results),'failed':[x for x in results if x['status']!='PASS']},indent=2));sys.exit(any(x['status']!='PASS' for x in results))
