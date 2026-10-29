"""Execute exact Section 2.12 code in fresh processes with declared fixture overrides."""
import ast
import contextlib
from decimal import Decimal
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-02/2.12-chapter-project-investment-scenario-analyzer.md'


def source_code():
    blocks=re.findall(r'^```python\n(.*?)^```',SOURCE.read_text(),re.M|re.S)
    assert len(blocks)==1
    return blocks[0]


def child():
    overrides=json.loads(sys.argv[2]);tree=ast.parse(source_code());replaced=set()
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for name in node.targets:
                if isinstance(name,ast.Name) and name.id in overrides:
                    node.value=ast.parse(overrides[name.id],mode='eval').body;replaced.add(name.id)
    assert replaced==set(overrides)
    ast.fix_missing_locations(tree);state={};out=io.StringIO();error=None
    try:
        with contextlib.redirect_stdout(out):exec(compile(tree,str(SOURCE),'exec'),state)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
    names=['initial_investment','annual_contribution','target_balance','maximum_years','early_target_threshold_years','return_scenarios','errors','results','rejections','total_scenarios','evaluated_scenarios','rejected_scenarios','target_reached_scenarios','target_not_reached_scenarios']
    print(json.dumps(dict(stdout=out.getvalue(),exception=error,scenario_types=[type(x).__name__ for x in state.get('return_scenarios',[])],state={k:state[k] for k in names if k in state}),default=str))


def closed(p,r,c,n):
    p,r,c=map(Fraction,(p,r,c))
    return p*(1+r)**n+(c*n if r==0 else c*((1+r)**n-1)/r)


def run():
    cases=[]
    def case(name,overrides=None,expected_error=None,limitation=None):cases.append(dict(name=name,overrides=overrides or {},expected_error=expected_error,limitation=limitation))
    def d(value):return 'Decimal('+repr(str(value))+')'
    def rates(values):return '['+','.join(d(v) for v in values)+']'
    case('published baseline')
    case('period zero',dict(initial_investment=d(100000)))
    case('zero contribution',dict(annual_contribution=d(0)))
    case('zero return',dict(return_scenarios=rates(['0'])))
    case('negative return',dict(return_scenarios=rates(['-.1'])))
    case('exact -100 percent',dict(return_scenarios=rates(['-1'])))
    case('below -100 percent',dict(return_scenarios=rates(['-1.01'])))
    case('just above -100 percent',dict(return_scenarios=rates(['-.999999'])))
    case('nonfinite scenarios',dict(return_scenarios=rates(['NaN','sNaN','Infinity','-Infinity'])))
    case('representation rejected',dict(return_scenarios="[None, '0.05', 0.05, True, Decimal('0')]"))
    case('empty scenarios',dict(return_scenarios='[]'))
    case('final year crossing',dict(initial_investment=d(100),annual_contribution=d(100),target_balance=d(300),maximum_years='2',return_scenarios=rates(['0'])))
    case('target missed at final year',dict(initial_investment=d(100),annual_contribution=d(100),target_balance=d('300.001'),maximum_years='2',return_scenarios=rates(['0'])))
    case('display cannot create crossing',dict(initial_investment=d('99999.996'),annual_contribution=d(0),maximum_years='1',return_scenarios=rates(['0'])))
    case('year one crossing',dict(initial_investment=d(100),annual_contribution=d(0),target_balance=d(105),maximum_years='1',return_scenarios=rates(['.05'])))
    case('supported horizon 100',dict(maximum_years='100',return_scenarios=rates(['0'])))
    case('classification threshold equal',dict(initial_investment=d(100),annual_contribution=d(10),target_balance=d(200),return_scenarios=rates(['0'])))
    case('classification threshold after',dict(initial_investment=d(100),annual_contribution=d(10),target_balance=d(210),return_scenarios=rates(['0'])))
    case('reversed scenarios',dict(return_scenarios=rates(['.09','.07','.05','.03'])))
    case('duplicate scenarios retained',dict(return_scenarios=rates(['.05','.05'])))
    for field,value,message in [('initial_investment','0','greater than zero'),('initial_investment','-1','greater than zero'),('initial_investment','NaN','must be finite'),('annual_contribution','-1','cannot be negative'),('annual_contribution','Infinity','must be finite'),('target_balance','0','greater than zero'),('target_balance','-1','greater than zero'),('target_balance','NaN','must be finite')]:case(field+' '+value,{field:d(value)},message)
    for value,message in [('True','must be an integer'),('0','greater than zero'),('-1','greater than zero'),('101','exceeds the supported'),('1.5','must be an integer')]:case('invalid horizon '+value,dict(maximum_years=value),message)
    case('shared representation precondition',dict(initial_investment="'25000'"),limitation='AttributeError')
    records=[];predicate_count=0
    for fixture in cases:
        proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',json.dumps(fixture['overrides'])],text=True,capture_output=True,timeout=10)
        payload=json.loads(proc.stdout);state=payload['state'];predicates=[]
        def check(label,ok,actual=None,expected=None):predicates.append(dict(label=label,status='PASS' if ok else 'FAIL',actual=str(actual),expected=str(expected)))
        check('child completed',proc.returncode==0 and not proc.stderr,proc.returncode,0)
        if fixture['limitation']:
            check('known typed-shared-input limitation observed',payload['exception'] is not None and payload['exception']['type']==fixture['limitation'],payload['exception'],fixture['limitation'])
            disposition='OPEN_LIMITATION'
        elif fixture['expected_error']:
            check('validation diagnostic and no results',payload['exception'] is None and fixture['expected_error'] in payload['stdout'] and 'results' not in state,payload['stdout'],fixture['expected_error']);disposition='PASS_SCOPED'
        else:
            check('no exception or shared errors',payload['exception'] is None and not state.get('errors'),payload['exception'],None)
            supplied=state['return_scenarios'];result=state['results'];rejections=state['rejections']
            check('scenario identity counts',len(result)+len(rejections)==len(supplied),[len(result),len(rejections)],len(supplied))
            check('stored counts',len(result)==state['evaluated_scenarios'] and len(rejections)==state['rejected_scenarios'],[len(result),len(rejections)],[state['evaluated_scenarios'],state['rejected_scenarios']])
            check('outcome counts',state['target_reached_scenarios']+state['target_not_reached_scenarios']==len(result))
            valid=[];invalid=[]
            for value,kind in zip(supplied,payload['scenario_types']):
                if kind!='Decimal':invalid.append('representation');continue
                rate=Decimal(value)
                if not rate.is_finite():invalid.append('finite')
                elif rate<=-1:invalid.append('domain')
                else:valid.append(rate)
            check('independent accepted count',len(result)==len(valid),len(result),len(valid))
            check('independent rejected count',len(rejections)==len(invalid),len(rejections),len(invalid))
            for row,rate in zip(result,valid):
                expected=next((n for n in range(state['maximum_years']+1) if closed(state['initial_investment'],rate,state['annual_contribution'],n)>=Fraction(state['target_balance'])),None)
                check('first crossing '+str(rate),row['target_year']==expected,row['target_year'],expected)
                n=state['maximum_years'] if expected is None else expected
                oracle=closed(state['initial_investment'],rate,state['annual_contribution'],n);actual=Fraction(row['ending_balance']);bound=max(Fraction(1),abs(oracle))*Fraction(1,10**26)
                check('rational ending balance',abs(actual-oracle)<=bound,actual,oracle)
                classification=('Target not reached' if expected is None else 'Target already reached' if expected==0 else 'Target reached within '+str(state['early_target_threshold_years'])+' years' if expected<=state['early_target_threshold_years'] else 'Target reached after '+str(state['early_target_threshold_years'])+' years')
                check('outcome classification',row['outcome']==classification,row['outcome'],classification)
            if fixture['name']=='display cannot create crossing':check('display rounds up but raw misses',result[0]['target_year'] is None and '$100,000.00' in payload['stdout'])
            disposition='PASS_SCOPED'
        predicate_count+=len(predicates)
        records.append(dict(**fixture,disposition=disposition,checks=predicates,execution=payload,stderr=proc.stderr,exit_code=proc.returncode))
    failed=sum(p['status']=='FAIL' for r in records for p in r['checks'])
    output=dict(source_revision='fc18c1b2178751f9b8c5a179df01057e73f52551',source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),source_code_sha256=hashlib.sha256(source_code().encode()).hexdigest(),python=sys.version,platform=platform.platform(),cases=len(records),passing_cases=sum(all(p['status']=='PASS' for p in r['checks']) and r['disposition']=='PASS_SCOPED' for r in records),open_limitation_cases=sum(r['disposition']=='OPEN_LIMITATION' for r in records),predicates=predicate_count,failed_predicates=failed,records=records)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k!='records'},indent=2));return bool(failed)

if __name__=='__main__':
    if '--child' in sys.argv:child()
    else:raise SystemExit(run())
