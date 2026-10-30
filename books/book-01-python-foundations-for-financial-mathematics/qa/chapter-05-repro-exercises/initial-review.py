"""Exact-source executions and independent integer benchmarks for 5.11."""
import copy
import hashlib
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).resolve().parent
BOOK = HERE.parents[1]
SOURCE = BOOK/'chapter-05/5.11-reproducible-financial-research.md'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def wire(obj):
    return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()

def integer_units(text):
    whole, _, fractional = text.partition('.')
    return int(whole)*10000 + int(fractional.ljust(4,'0'))

def cents(units):
    quotient, remainder = divmod(units,100)
    # Nearest cent, exact halfway ties to an even integer cent.
    return quotient + (remainder > 50 or (remainder == 50 and quotient % 2 == 1))

def display(value):
    return f'{value//100}.{value%100:02d}'

def oracle(rows, each=False):
    units = [integer_units(r['amount']) for r in rows]
    value = sum(map(cents,units)) if each else cents(sum(units))
    return dict(currency='USD',count=len(rows),total=display(value),
                method='round_each_then_sum' if each else 'sum_then_round',rounding='ROUND_HALF_EVEN')

def load(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def run():
    text = SOURCE.read_text();blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
    json_blocks = re.findall(r'^```json\n(.*?)^```',text,re.M|re.S)
    assert len(blocks)==2
    files=dict(zip(['research.py','test_research.py'],blocks));files.update(dict(zip(['inflows.json','settings.json'],json_blocks[:2])))
    operations,checks=[],[]
    def ck(exercise,label,actual,expected):
        checks.append(dict(exercise=exercise,label=label,actual=repr(actual),expected=repr(expected),status='PASS' if actual==expected else 'FAIL'))
    def reject(exercise,label,fn):
        try:fn();actual='no exception'
        except Exception as e:actual=type(e).__name__
        ck(exercise,label,actual,'ValueError')
    env={k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME')};env['PYTHONDONTWRITEBYTECODE']='1'
    retained=HERE/'evidence-bundle';retained.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix='research-exercises-') as tmp:
        root=Path(tmp)
        for name,code in files.items():(root/name).write_text(code,encoding='utf-8')
        original=load('research',root/'research.py')
        experiments=load('research_qa_experiments',HERE/'experiments.py')
        data=(root/'inflows.json').read_bytes();config=(root/'settings.json').read_bytes();source=(root/'research.py').read_bytes()
        rows=json.loads(data);expected=oracle(rows)
        def command(label,args,*,error=None,methods=None):
            r=subprocess.run([sys.executable,'-B',*map(str,args)],cwd=root,env=env,capture_output=True,text=True,timeout=30)
            found=re.findall(r'Ran (\d+) tests? in',r.stderr);count=int(found[0]) if len(found)==1 else None
            ok=r.returncode==0 and r.stdout==r.stderr==''
            if error:ok=r.returncode!=0 and r.stdout=='' and error in r.stderr
            if methods:ok=r.returncode==0 and count==methods and bool(re.search(r'^OK\s*$',r.stderr,re.M))
            operations.append(dict(label=label,args=list(map(str,args)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,actual_methods=count,expected_methods=methods,expected_error=error,status='PASS' if ok else 'FAIL'))
            return r
        command('exact original nine-method suite',['-m','unittest','discover','-v'],methods=9)
        third=rows+[dict(id='CF-3',currency='USD',amount='0.005')]
        ck('5.11-E1','integer tie benchmark',oracle(third)['total'],'30.02')
        ck('5.11-E1','source third inflow',original.analyze(wire(third),config),oracle(third))
        maximum=[dict(id=f'MAX-{i}',currency='USD',amount='1000000.0000') for i in range(1000)]
        ck('5.11-E2','integer boundary benchmark',oracle(maximum)['total'],'1000000000.00')
        ck('5.11-E2','source 1000 maximum rows',original.analyze(wire(maximum),config),oracle(maximum))
        reject('5.11-E2','1001 rows',lambda:original.analyze(wire(maximum+[dict(maximum[0],id='OVER')]),config))
        reject('5.11-E2','maximum plus smallest supported unit',lambda:original.analyze(wire([dict(rows[0],amount='1000000.0001')]),config))
        ck('5.11-E3','integer sum-then-round fixture',expected['total'],'30.01')
        ck('5.11-E3','integer each-then-sum fixture',oracle(rows,True)['total'],'30.00')
        ck('5.11-E3','supplemental alternate policy',experiments.round_each_then_sum(data,config),oracle(rows,True))
        ck('5.11-E3','original policy unchanged',original.analyze(data,config),expected)
        with __import__('decimal').localcontext() as context:
            context.prec=2;context.rounding=__import__('decimal').ROUND_DOWN;context.traps[__import__('decimal').Inexact]=True
            ck('5.11-E3','separate policy hostile caller context',experiments.round_each_then_sum(data,config),oracle(rows,True))
        reject('5.11-E3','alternate keeps original rejection contract',lambda:experiments.round_each_then_sum(wire([dict(rows[0],amount='-1')]),config))
        whitespace=b' \n\t'+data+b' \n';(root/'whitespace.json').write_bytes(whitespace)
        ck('5.11-E4','same decoded data',json.loads(whitespace),rows)
        ck('5.11-E4','same result',original.analyze(whitespace,config),expected)
        ck('5.11-E4','different input digest',sha(whitespace)!=sha(data),True)
        runtime=dict(python=platform.python_version(),implementation=platform.python_implementation(),system=platform.system())
        def validate(raw,**options):
            values=dict(returncode=0,data_raw=data,config_raw=config,source_raw=source,expected_result=expected,expected_runtime=runtime);values.update(options)
            return experiments.validate_artifact(raw,**values)
        reports={}
        for label,input_name,benchmark,raw in [('run-a','inflows.json',expected,data),('run-b','inflows.json',expected,data),('whitespace','whitespace.json',expected,whitespace),('third','third.json',oracle(third),wire(third)),('maximum','maximum.json',oracle(maximum),wire(maximum))]:
            (root/input_name).write_bytes(raw);output=root/(label+'.json')
            process=command('source CLI '+label,['research.py','--input',input_name,'--config','settings.json','--output',output])
            report=output.read_bytes();reports[label]=report
            accepted=validate(report,returncode=process.returncode,data_raw=raw,expected_result=benchmark)
            ck('5.11-E6',label+' completed/bound artifact result',accepted['result'],benchmark)
            (retained/(label+'.json')).write_bytes(report)
        ck('5.11-E7','same local runtime artifacts byte-identical',reports['run-a'],reports['run-b'])
        a,w=json.loads(reports['run-a']),json.loads(reports['whitespace'])
        ck('5.11-E4','whitespace full artifact changes',reports['run-a']!=reports['whitespace'],True)
        ck('5.11-E4','whitespace artifact result same',a['result'],w['result'])
        ck('5.11-E4','whitespace stored digest differs',a['evidence']['input_sha256']!=w['evidence']['input_sha256'],True)
        command('E6 exclusive existing-output failure',['research.py','--input','inflows.json','--config','settings.json','--output','run-a.json'],error='FileExistsError')
        ck('5.11-E6','existing successful artifact unchanged',(root/'run-a.json').read_bytes(),reports['run-a'])
        # A file from a failed/truncated write is not a successful run artifact.
        invalid_cases=[]
        def mutant(label,fn):
            value=copy.deepcopy(a);fn(value);invalid_cases.append((label,wire(value)))
        mutant('boolean schema version',lambda x:x.update(schema_version=True))
        mutant('unknown artifact field',lambda x:x.update(extra=0))
        mutant('missing result',lambda x:x.pop('result'))
        mutant('boolean count',lambda x:x['result'].update(count=True))
        mutant('zero count',lambda x:x['result'].update(count=0))
        mutant('too many count',lambda x:x['result'].update(count=1001))
        mutant('float total',lambda x:x['result'].update(total=30.01))
        mutant('exponent total',lambda x:x['result'].update(total='3.001e1'))
        mutant('leading zero total',lambda x:x['result'].update(total='030.01'))
        mutant('out of bound total',lambda x:x['result'].update(total='1000000000.01'))
        mutant('wrong numeric answer',lambda x:x['result'].update(total='30.00'))
        mutant('wrong rounding stage',lambda x:x['result'].update(method='round_each_then_sum'))
        mutant('wrong currency',lambda x:x['result'].update(currency='EUR'))
        mutant('missing runtime',lambda x:x['evidence'].pop('python'))
        mutant('blank runtime',lambda x:x['evidence'].update(system=''))
        mutant('runtime mismatch',lambda x:x['evidence'].update(python='0.0.0'))
        mutant('dependency drift',lambda x:x['evidence'].update(third_party_runtime_dependencies=['unreviewed']))
        mutant('uppercase digest',lambda x:x['evidence'].update(input_sha256='A'*64))
        mutant('unbound input digest',lambda x:x['evidence'].update(input_sha256='0'*64))
        mutant('unbound config digest',lambda x:x['evidence'].update(config_sha256='0'*64))
        mutant('unbound source digest',lambda x:x['evidence'].update(source_sha256='0'*64))
        invalid_cases.extend([('duplicate schema version',reports['run-a'].replace(b'"schema_version": 1',b'"schema_version": 1, "schema_version": 1')),('nonfinite extra',b'{"extra":NaN}'),('wrong top-level',b'[]')])
        for label,raw in invalid_cases:reject('5.11-E6',label,lambda raw=raw:validate(raw))
        # JSON decoder errors subclass ValueError; keep exact class for corrupt files.
        for label,raw in [('empty artifact',b''),('truncated artifact',reports['run-a'][:-5])]:
            try:validate(raw);actual='accepted'
            except json.JSONDecodeError:actual='JSONDecodeError'
            ck('5.11-E6',label,actual,'JSONDecodeError')
        reject('5.11-E6','valid bytes with failed status',lambda:validate(reports['run-a'],returncode=1))
        reject('5.11-E6','byte-mutated input with old report',lambda:validate(reports['run-a'],data_raw=whitespace))
        for name in files:(retained/name).write_bytes((root/name).read_bytes())
        (retained/'whitespace-input.json').write_bytes(whitespace);(retained/'third-input.json').write_bytes(wire(third))
        # Maximum input is exactly regenerable from the retained runner; manifest
        # records its consumed digest/size instead of archiving 1000 repeated rows.
        ck('all','original four files unchanged',{n:sha((root/n).read_bytes()) for n in files},{n:sha(code.encode()) for n,code in files.items()})
        manifest=dict(schema_version=1,baseline='015fa852cf678fe91948643c03d7570d9b46b69e',files=[dict(path=p.name,size=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(retained.iterdir()) if p.is_file() and p.name!='manifest.json'],generated_maximum_input=dict(generator='review.py: maximum list, wire()',sha256=sha(wire(maximum)),size=len(wire(maximum))),dependency_artifacts=[],dependency_scope='No third-party runtime or build dependency in this standalone lab; Python/platform libraries are not preserved binaries',tests_and_docs=[dict(path=p.name,sha256=sha(p.read_bytes())) for p in [HERE/'review.py',HERE/'experiments.py']])
        (retained/'manifest.json').write_bytes(wire(manifest))
    output=dict(python=platform.python_version(),platform=platform.platform(),source=str(SOURCE.relative_to(BOOK)),source_sha256=sha(SOURCE.read_bytes()),exercise_records=8,command_records=len(operations),command_passed=sum(x['status']=='PASS' for x in operations),command_failed=sum(x['status']=='FAIL' for x in operations),source_method_invocations=sum(x['actual_methods'] or 0 for x in operations),predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),integer_oracle='base 10000 units, divmod 100, >50 or ==50 with odd quotient increments',operations=operations,checks=checks)
    (HERE/'results.json').write_bytes(wire(output));print(json.dumps({k:v for k,v in output.items() if k not in ('operations','checks')}))
    return bool(output['failed'] or output['command_failed'])

if __name__=='__main__':
    raise SystemExit(run())
