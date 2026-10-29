"""Exercises 1–13: exact source snippets plus clearly separated supplemental answers."""
import ast
import contextlib
from decimal import Decimal as D
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import platform

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
PROMPTS=BOOK/'chapter-02/2.13-exercises-and-applied-problems.md'
COMPANION=BOOK/'chapter-02/solutions/2.13-solutions-and-reference-implementations.md'


def target_classification(balance,target):
    if balance < target:return 'Below target'
    if balance == target:return 'Exactly at target'
    return 'Above target'


def screen(investment,expected_return,years):
    return investment > 0 and expected_return > 0 and years >= 5


def contribution_rule(balance,target):
    if balance < target:return 'Contribution required'
    return 'Target already funded'


def run():
    blocks=re.findall(r'^```python\n(.*?)^```',COMPANION.read_text(),re.M|re.S)
    results=[];executions=[]
    def check(exercise,label,actual,expected,kind='exact source execution'):
        results.append(dict(exercise=exercise,label=label,kind=kind,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
    def execute(index,overrides=None,prelude=None):
        tree=ast.parse(blocks[index]);overrides=overrides or {};replaced=set()
        for node in tree.body:
            if isinstance(node,ast.Assign):
                for target in node.targets:
                    if isinstance(target,ast.Name) and target.id in overrides:
                        value=overrides[target.id]
                        expression='Decimal('+repr(str(value))+')' if isinstance(value,D) else repr(value)
                        node.value=ast.parse(expression,mode='eval').body;replaced.add(target.id)
        assert replaced==set(overrides)
        ast.fix_missing_locations(tree)
        state={'Decimal':D,**(prelude or {})};output=io.StringIO()
        with contextlib.redirect_stdout(output):exec(compile(tree,str(COMPANION), 'exec'),state)
        executions.append(dict(zero_based_fence=index,original_code_sha256=hashlib.sha256(blocks[index].encode()).hexdigest(),overrides={k:str(v) for k,v in overrides.items()},prelude={k:str(v) for k,v in (prelude or {}).items()},stdout=output.getvalue()))
        return state,output.getvalue()
    state,_=execute(0);check(1,'published target',state['target_reached'],False)
    for balance,expected in [('99999.99',False),('100000',True),('100000.01',True)]:
        state,_=execute(0,dict(balance=D(balance)));check(1,'inclusive target boundary '+balance,state['target_reached'],expected)
    for cash,expected in [('-2500',(False,True,False)),('0',(False,False,True)),('2500',(True,False,False))]:
        state,_=execute(1,dict(cash_flow=D(cash)));check(2,'cash-flow sign '+cash,tuple(state[k] for k in ('is_positive','is_negative','is_zero')),expected)
    for rate,expected in [('.08',True),('0',True),('.25',True),('-.0001',False),('.2501',False)]:
        state,_=execute(2,dict(discount_rate=D(rate)));check(3,'supported rate '+rate,state['is_valid'],expected)
    state,_=execute(3);check(4,'published compound condition',state['passes_screen'],True)
    for fields in [dict(investment=D(0)),dict(expected_return=D(0)),dict(years=4)]:
        state,_=execute(3,fields);check(4,'failed conjunct '+str(fields),state['passes_screen'],False)
    for value,missing,falsy in [(None,True,True),(D(0),False,True),(D(1),False,False)]:
        check(5,'presence and truthiness '+str(value),(value is None,not value),(missing,falsy),'supplemental reasoning probe')
    for r,g,expected in [('.09','.03',True),('.03','.03',False),('.02','.03',False)]:
        state,_=execute(4,dict(discount_rate=D(r),growth_rate=D(g)));check(6,'r > g '+r+'/'+g,state['valid_relationship'],expected)
    for amount,expected in [('250000',True),('1000',True),('500000',True),('999.99',False),('500000.01',False)]:
        state,_=execute(5,dict(loan_amount=D(amount)));check(7,'chained loan bounds '+amount,state['supported'],expected)
        value=D(amount);check(7,'logical loan bounds '+amount,value>=D(1000) and value<=D(500000),expected,'supplemental logical equivalent')
    for value,expected in [(None,False),('0.05',False),(.05,False),(True,False),(D('.05'),True),(D('NaN'),False),(D('sNaN'),False),(D('Infinity'),False)]:
        _,output=execute(6,prelude=dict(annual_return=value));check(8,'dependency guard '+repr(value),'Usable Decimal rate.' in output,expected)
    for rate,expected in [('.06','positive'),('0','zero'),('-.01','negative')]:
        state,_=execute(7,dict(annual_return=D(rate)));check(9,'classification '+rate,state['classification'],expected)
    for ratio,expected in [('.49','Low liquidity'),('.5','Moderate liquidity'),('.75','Moderate liquidity'),('.999','Moderate liquidity'),('1','High liquidity'),('1.01','High liquidity')]:
        state,_=execute(8,dict(cash_ratio=D(ratio)));check(10,'liquidity boundary '+ratio,state['classification'],expected)
    for balance,expected in [('99999','Below target'),('100000','Exactly at target'),('102500','Above target')]:check(11,'target classification '+balance,target_classification(D(balance),D(100000)),expected,'supplemental implementation')
    for principal,rate,years,expected in [(50000,'.07',8,True),(1,'.01',5,True),(0,'.01',5,False),(1,'0',5,False),(1,'.01',4,False)]:check(12,'screen '+str((principal,rate,years)),screen(D(principal),D(rate),years),expected,'supplemental implementation')
    for balance,expected in [('99999','Contribution required'),('100000','Target already funded'),('100001','Target already funded')]:check(13,'contribution rule '+balance,contribution_rule(D(balance),D(100000)),expected,'supplemental implementation')
    payload=dict(source_revision='e0f9cfdd30ce42f576fee3760fc86254be2bbdb7',python=sys.version,platform=platform.platform(),exercise_records=13,predicates=len(results),passed=sum(x['status']=='PASS' for x in results),failed=sum(x['status']=='FAIL' for x in results),exact_snippet_executions=len(executions),source_snippet_indices=list(range(9)),checks=results,executions=executions)
    (HERE/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('checks','executions')},indent=2))
    return bool(payload['failed'])

if __name__=='__main__':raise SystemExit(run())
