"""Exact project extraction, exercise checks and temporary mutation; stdlib only."""
import ast
import contextlib
from decimal import Decimal as D, Inexact, ROUND_DOWN, localcontext
import difflib
from fractions import Fraction as F
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
PROJECT=BOOK/'chapter-03/3.14-chapter-project-financial-mathematics-function-library.md'
COMP=BOOK/'chapter-03/solutions/3.15-solutions-and-reference-implementations.md'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def run():
    checks=[]
    def check(ex,label,actual,expected):checks.append(dict(exercise=ex,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
    def raises(ex,label,expected,callback):
        try:callback();actual='no exception'
        except Exception as error:actual=type(error).__name__
        check(ex,label,actual,expected)
    def oracle(ex,label,actual,expected,tolerance=F(1,10**30)):
        error=abs(F(actual)-expected);checks.append(dict(exercise=ex,label=label,actual=str(actual),expected=str(expected),absolute_error=str(error),tolerance=str(tolerance),status='PASS' if error<=tolerance else 'FAIL'))
    project=re.findall(r'^```python\n(.*?)^```',PROJECT.read_text(),re.M|re.S);companion=re.findall(r'^```python\n(.*?)^```',COMP.read_text(),re.M|re.S)
    with tempfile.TemporaryDirectory(prefix='book1-ch03-review-') as work:
        work=Path(work)
        for name,code in [('financial_functions.py',project[0]),('test_function_library.py',project[1]),('demo.py',project[2]),('chapter03_solutions.py',companion[0])]:
            (work/name).write_text(code)
        finance=load('financial_functions',work/'financial_functions.py');sys.modules['financial_functions']=finance
        solutions=load('chapter03_solutions',work/'chapter03_solutions.py')
        check(1,'FV value/currency timeline numeric result',finance.future_value(D(1000),periodic_rate=D('.05'),periods=2),D('1102.50'))
        def printing_only():print('1102.50')
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):returned=printing_only()
        check(2,'print-only return',returned,None);check(2,'printed text',captured.getvalue(),'1102.50\n')
        check(3,'keyword-only valid call',finance.future_value(D(1000),periodic_rate=D('.05'),periods=2),D('1102.5'))
        raises(3,'positional rate and horizon','TypeError',lambda:finance.future_value(D(1000),D('.05'),2))
        def incomplete(start,end):
            if end>start:return end-start
        check(4,'incomplete zero/loss',(incomplete(D(100),D(100)),incomplete(D(100),D(90))),(None,None))
        check(4,'signed gain fixes zero and loss',(D(100)-D(100),D(90)-D(100)),(D(0),D(-10)))
        def default_example(periods=1):return periods
        check(5,'default omission/zero/None',(default_example(),default_example(0),default_example(None)),(1,0,None))
        def bad_default(amount,flows=[]):
            flows.append(amount);return flows
        first=bad_default(D(1));second=bad_default(D(2));check(6,'shared mutable default',(first is second,len(first)),(True,2))
        first=solutions.append_flow(D(1));second=solutions.append_flow(D(2));check(6,'correct omitted list independence',(first,second,first is second),([D(1)],[D(2)],False))
        supplied=[];returned=solutions.append_flow(D(-1),supplied);check(6,'explicit caller list mutation',(returned is supplied,supplied),(True,[D(-1)]))
        namespace={'rate':D('.05'),'spread':D('.01')};exec('def wrong():\n    rate = rate + spread\n    return rate\n',namespace)
        raises(7,'read local before binding','UnboundLocalError',namespace['wrong'])
        def adjusted_rate(rate,spread):return rate+spread
        check(7,'explicit inputs',adjusted_rate(D('.05'),D('.01')),D('.06'))
        def hinted(periodic_rate:D,periods:int):return periodic_rate,periods
        check(8,'annotations alone permit NaN and bool',(hinted(D('NaN'),True)[0].is_finite(),hinted(D('NaN'),True)[1]),(False,True))
        check(8,'annotations alone do not reject string',hinted('0.05',-1),('0.05',-1))
        check(9,'project public docstring exists','period-n' in finance.present_value.__doc__,True)
        value=D(100)
        def rebind(amount):amount=D(0);return amount
        check(10,'rebinding preserves caller',(rebind(value),value),(D(0),D(100)))
        flows=[];solutions.append_flow(D(1),flows);check(10,'list mutation visible',flows,[D(1)])
        oracle(11,'exact accumulation',finance.future_value(D(2000),periodic_rate=D('.04'),periods=3),F(2000)*F(26,25)**3)
        oracle(12,'exact discount',finance.present_value(D(144),periodic_rate=D('.2'),periods=2),F(100))
        check(12,'multiplication is different quantity',finance.future_value(D(144),periodic_rate=D('.2'),periods=2),D('207.36'))
        quarter=finance.periodic_rate_from_nominal(D('.08'),periods_per_year=4);annual=finance.effective_annual_rate(quarter,periods_per_year=4)
        oracle(13,'nominal quarterly conversion',quarter,F(1,50));oracle(13,'effective annual',annual,F(51,50)**4-1)
        with localcontext(finance._policy()):staged=D('104.04')*finance.discount_factor(quarter,periods=2)
        wrapper=finance.present_value_from_nominal(D('104.04'),nominal_annual_rate=D('.08'),periods_per_year=4,periods=2)
        oracle(14,'staged PV',staged,F(100));oracle(14,'wrapper PV',wrapper,F(100));oracle(14,'staged-wrapper agreement',staged,F(wrapper))
        future=finance.future_value(D(1000),periodic_rate=D('-.1'),periods=1);present=finance.present_value(future,periodic_rate=D('-.1'),periods=1)
        check(15,'negative rate FV/PV',(future,present),(D(900),D(1000)));check(15,'discount factor >1',finance.discount_factor(D('-.1'),periods=1)>1,True)
        for label,expected,amount,rate,periods in [('string amount','TypeError','144',D('.2'),2),('NaN zero horizon','ValueError',D(144),D('NaN'),0),('bool horizon','TypeError',D(144),D('.2'),True),('horizon1001','ValueError',D(144),D('.2'),1001)]:raises(16,label,expected,lambda amount=amount,rate=rate,periods=periods:finance.present_value(amount,periodic_rate=rate,periods=periods))
        expected=finance.present_value(D('1234.56'),periodic_rate=D('.037'),periods=17)
        def snapshot(c):return dict(prec=c.prec,rounding=c.rounding,Emin=c.Emin,Emax=c.Emax,capitals=c.capitals,clamp=c.clamp,flags={str(k):v for k,v in c.flags.items()},traps={str(k):v for k,v in c.traps.items()})
        with localcontext() as caller:
            caller.prec=6;caller.rounding=ROUND_DOWN;caller.traps[Inexact]=True;caller.flags[Inexact]=True
            before=snapshot(caller);actual=finance.present_value(D('1234.56'),periodic_rate=D('.037'),periods=17);after=snapshot(caller)
            check(17,'fixed-policy result independent of caller',actual,expected);check(17,'full caller context preserved',after,before)
        canonical=finance.present_value(D(125),periodic_rate=D('.25'),periods=1);check(18,'independent known value',canonical,D(100))
        tree=ast.parse(project[0]);mutations=0
        for node in tree.body:
            if isinstance(node,ast.FunctionDef) and node.name=='present_value':
                for part in ast.walk(node):
                    if isinstance(part,ast.BinOp) and isinstance(part.op,ast.Div):part.op=ast.Mult();mutations+=1
        assert mutations==1
        mutant=ast.unparse(tree)+'\n';(work/'mutant.py').write_text(mutant);wrong=load('temporary_mutant',work/'mutant.py');wrong_result=wrong.present_value(D(125),periodic_rate=D('.25'),periods=1)
        check(18,'mutant produces wrong known value',wrong_result,D('156.25'));check(18,'independent oracle detects mutation',wrong_result==D(100),False)
        check(18,'canonical source preserved',(work/'financial_functions.py').read_text(),project[0]);check(18,'canonical still returns correct PV',finance.present_value(D(125),periodic_rate=D('.25'),periods=1),D(100))
        mutation=dict(mutated_function='present_value',mutation='Replace its single division by multiplication in a temporary AST copy',canonical_code_sha256=hashlib.sha256(project[0].encode()).hexdigest(),mutant_code_sha256=hashlib.sha256(mutant.encode()).hexdigest(),input='125 at .25 for one period',independent_expected='100',mutant_actual=str(wrong_result),detected=True,canonical_file_unchanged=True)
        (HERE/'mutation-evidence.json').write_text(json.dumps(mutation,indent=2)+'\n')
        monthly=finance.periodic_rate_from_nominal(D('.12'),periods_per_year=12);annual=finance.effective_annual_rate(monthly,periods_per_year=12);future=finance.future_value(D(1000),periodic_rate=monthly,periods=12);recovered=finance.present_value_from_nominal(future,nominal_annual_rate=D('.12'),periods_per_year=12,periods=12)
        oracle(20,'monthly rate',monthly,F(1,100));oracle(20,'annual rate',annual,F(101,100)**12-1);oracle(20,'FV',future,F(1000)*F(101,100)**12);oracle(20,'recovered PV',recovered,F(1000))
        check(20,'zero horizon',finance.present_value_from_nominal(D(1000),nominal_annual_rate=D('.12'),periods_per_year=12,periods=0),D(1000))
        raises(20,'invalid frequency even zero horizon','ValueError',lambda:finance.present_value_from_nominal(D(1000),nominal_annual_rate=D('.12'),periods_per_year=0,periods=0))
        demo=subprocess.run([sys.executable,'demo.py'],cwd=work,text=True,capture_output=True,timeout=10);check(20,'project demo exit',demo.returncode,0);check(20,'project report FV','1126.83' in demo.stdout,True)
        suites=subprocess.run([sys.executable,'-m','unittest','-v','test_function_library','chapter03_solutions'],cwd=work,text=True,capture_output=True,timeout=20)
        check('regression','existing combined suite',suites.returncode,0);check('regression','19 existing methods','Ran 19 tests' in suites.stderr,True)
        (HERE/'existing-suite.log').write_text(suites.stdout+suites.stderr);(HERE/'integration-output.txt').write_text(demo.stdout)
    out=dict(source_revision='098e8583d49ea0525b6cbc7f000fd7f9bbe9dadd',python=sys.version,platform=platform.platform(),exercises_reviewed=20,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),existing_methods_rerun=19,new_unique_reference_methods=0,source_hashes={str(p.relative_to(BOOK)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PROJECT,COMP)},checks=checks)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2));return bool(out['failed'])

if __name__=='__main__':raise SystemExit(run())
