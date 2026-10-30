"""Supplemental compatibility predicates, not additional unittest methods."""
import json
from typing import get_type_hints
from decimal import Inexact, ROUND_DOWN, localcontext
import financial_inflows as package
from financial_inflows import analyze,inflow_count
from financial_inflows.result_types import AnalyzeResult

CONFIG=b'{"currency":"USD","rounding":"ROUND_HALF_EVEN","scale":"0.01"}'
DATA=b'[{"id":"A","currency":"USD","amount":"10.005"},{"id":"B","currency":"USD","amount":"20.005"}]'
expected=dict(currency='USD',count=2,total='30.01',method='sum_then_round',rounding='ROUND_HALF_EVEN')
records=[]
def ck(label,actual,wanted):
    records.append(dict(label=label,actual=repr(actual),expected=repr(wanted),status='PASS' if actual==wanted else 'FAIL'))
def rejected(label,fn):
    try:fn();actual='no exception'
    except Exception as error:actual=type(error).__name__
    ck(label,actual,'ValueError')
ck('original public API preserved',analyze(DATA,CONFIG),expected)
ck('new public count',inflow_count(DATA,CONFIG),2)
ck('explicit public exports',package.__all__,['analyze','inflow_count'])
ck('TypedDict exact required fields',AnalyzeResult.__required_keys__,frozenset(expected))
ck('runtime annotation identifies typed result',get_type_hints(analyze)['return'],AnalyzeResult)
before=(DATA,CONFIG)
inflow_count(DATA,CONFIG);ck('input bytes preserved',(DATA,CONFIG),before)
with localcontext() as context:
    context.prec=2;context.rounding=ROUND_DOWN;context.traps[Inexact]=True
    ck('count retains context isolation',inflow_count(DATA,CONFIG),2)
    ck('caller context unchanged',(context.prec,context.rounding,context.traps[Inexact]),(2,ROUND_DOWN,True))
rejected('new function validates all records',lambda:inflow_count(DATA.replace(b'20.005',b'-1'),CONFIG))
rejected('typed analyze keeps amount validation',lambda:analyze(DATA.replace(b'10.005',b'NaN'),CONFIG))
rejected('new function retains configuration validation',lambda:inflow_count(DATA,CONFIG.replace(b'USD',b'EUR')))
rejected('new function rejects empty input',lambda:inflow_count(b'[]',CONFIG))
# TypedDict is a documentation/type-checker aid, not runtime construction checks.
ck('TypedDict constructor is ordinary unvalidated dict',AnalyzeResult(currency='EUR'),{'currency':'EUR'})
print(json.dumps(records))
raise SystemExit(any(x['status']!='PASS' for x in records))
