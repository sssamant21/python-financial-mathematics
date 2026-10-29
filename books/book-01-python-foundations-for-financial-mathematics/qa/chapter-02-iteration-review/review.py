"""Check source claims, exact snippets and supplemental iteration answers separately."""
import contextlib
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import sys
from reference import annual_schedule, print_schedule, crossing_while, crossing_break, search_loop_else, cashflow_counts, discounted_cashflows, scenario_projection, quarters, process_missing, reject_scenarios

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
COMP=BOOK/'chapter-02/solutions/2.13-solutions-and-reference-implementations.md'


def closed_form(principal,rate,contribution,n):
    p,r,c=map(F,(principal,rate,contribution))
    return p*(1+r)**n + (c*n if r==0 else c*((1+r)**n-1)/r)


def run():
    checks=[];benchmarks=[]
    def check(exercise,label,actual,expected,kind='supplemental execution'):
        checks.append(dict(exercise=exercise,label=label,kind=kind,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
    def rational(exercise,label,actual,expected):
        error=abs(F(actual)-expected)
        bound=max(F(1),abs(expected))*F(1,10**26)
        checks.append(dict(exercise=exercise,label=label,kind='exact Fraction oracle',actual=str(actual),expected=str(expected),error=str(error),bound=str(bound),status='PASS' if error<=bound else 'FAIL'))
    def crossing(exercise,p,r,c,t,h,method=crossing_while):
        actual=method(*map(D,(p,r,c,t)),h) if method is crossing_while else method(D(p),D(r),D(t),h)
        expected=next((n for n in range(h+1) if closed_form(p,r,c,n)>=F(t)),None)
        check(exercise,'first crossing '+str((p,r,c,t,h)),actual['first_year'],expected)
        end=expected if expected is not None else h
        check(exercise,'stopping period',actual['ending_year'],end)
        rational(exercise,'stopping balance',actual['balance'],closed_form(p,r,c,end))
        benchmarks.append(dict(exercise=exercise,inputs=[p,r,c,t,h],expected_first_year=expected,expected_ending_balance=str(closed_form(p,r,c,end)),actual={k:str(v) for k,v in actual.items()}))
        return actual
    rows=annual_schedule(D(10000),D(0),D(2500),5)
    check(14,'annual contributions',rows,[(1,D(12500)),(2,D(15000)),(3,D(17500)),(4,D(20000)),(5,D(22500))])
    output=io.StringIO()
    with contextlib.redirect_stdout(output):print_schedule(rows)
    check(14,'printed every ending balance',output.getvalue(),'Year 1: 12,500.00\nYear 2: 15,000.00\nYear 3: 17,500.00\nYear 4: 20,000.00\nYear 5: 22,500.00\n')
    rows=annual_schedule(D(10000),D('.05'),D(0),10)
    check(15,'ten modeled years',[year for year,_ in rows],list(range(1,11)))
    for year,balance in rows:rational(15,'year '+str(year),balance,F(10000)*F(21,20)**year)
    output=io.StringIO()
    with contextlib.redirect_stdout(output):print_schedule(rows)
    check(15,'printed ten labeled years',len(output.getvalue().splitlines()),10)
    end=annual_schedule(D(10000),D('.05'),D(2000),5)
    start=annual_schedule(D(10000),D('.05'),D(2000),5,beginning=True)
    for year,balance in end:rational(16,'end contribution year '+str(year),balance,closed_form(10000,'.05',2000,year))
    beginning_oracle=F(10000)*F(21,20)**5+F(2000)*F(21,20)*((F(21,20)**5-1)/F(1,20))
    rational(16,'beginning contribution terminal',start[-1][1],beginning_oracle)
    check(16,'timing affects value',start[-1][1]>end[-1][1],True)
    crossing(17,'20000','0','5000','50000',20)
    crossing(17,'20000','0','5000','20000',20)
    crossing(17,'20000','0','5000','50000',6)
    crossing(17,'20000','0','5000','50000',5)
    original18=crossing(18,'25000','.05','0','75000',30)
    crossing(18,'25000','.05','0','75000',22)
    crossing(18,'75000','.05','0','75000',30)
    crossing(19,'20000','0','0','50000',5)
    crossing(19,'20000','-.1','0','50000',5)
    crossing(19,'0','.05','0','50000',5)
    flows=list(map(D,(-10000,3000,3500,4000)));counts=cashflow_counts(flows)
    check(20,'arithmetic total',counts['total'],D(500))
    check(21,'sign reconciliation',(counts['positive'],counts['negative'],counts['zero']),(3,1,0))
    counts=cashflow_counts([D(-1),D(0),D(1)]);check(21,'zero observed',(counts['positive'],counts['negative'],counts['zero']),(1,1,1))
    discounted,total=discounted_cashflows(list(map(D,(5000,6000,7000))),D('.08'))
    for n,pv in discounted:rational(22,'period '+str(n),pv,F((5000,6000,7000)[n-1])/F(27,25)**n)
    rational(22,'total PV',total,sum((F(cf)/F(27,25)**n for n,cf in enumerate((5000,6000,7000),1)),F(0)))
    check(22,'display PV',f'{total:,.2f}','15,330.49')
    check(23,'inclusive years',list(range(1,16)),list(range(1,15))+[15])
    check(23,'wrong exclusive endpoint',15 in range(1,15),False)
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        print('Period 0: initial state')
        for period in range(1,11):print(f'Period {period}: future state')
    check(24,'separate initial and future periods',output.getvalue().splitlines(),['Period 0: initial state']+[f'Period {n}: future state' for n in range(1,11)])
    check(25,'quarter ordinals',[r[2] for r in quarters(5)],list(range(1,21)))
    rates=[D('.03'),D('.05'),D('.07')];scenarios=scenario_projection(rates)
    for rate,schedule in scenarios:
        rational(26,'scenario '+str(rate),schedule[-1][1],F(10000)*(1+F(rate))**5)
        rational(26,'first year '+str(rate),schedule[0][1],F(10000)*(1+F(rate)))
    check(27,'year-quarter labels',quarters(3),[(y,q,(y-1)*4+q) for y in (1,2,3) for q in (1,2,3,4)])
    check(28,'permutation independence',dict((r,s[-1][1]) for r,s in scenarios),dict((r,s[-1][1]) for r,s in scenario_projection(list(reversed(rates)))))
    # Deliberately contaminated counterexample: no repair to manuscript required.
    contaminated=D(10000)
    for rate in rates:
        for _ in range(5):contaminated*=1+rate
    check(28,'shared state changes last scenario',contaminated==scenarios[-1][1][-1][1],False,'deliberate counterexample')
    original29=crossing(29,'20000','.06','0','50000',30,crossing_break)
    crossing(29,'50000','.06','0','50000',30,crossing_break)
    crossing(29,'20000','.06','0','50000',15,crossing_break)
    crossing(29,'20000','.06','0','50000',16,crossing_break)
    crossing(29,'20000','.06','0','50000',0,crossing_break)
    check(30,'processed/missing and sum',process_missing([D(5000),None,D(-2000),D(3000),None]),(3,2,D(6000)))
    check(30,'zero preserved',process_missing([None,D(0)]),(1,1,D(0)))
    accepted,rejected=reject_scenarios([D('.05'),D('NaN'),D('-1.10'),D('.08')])
    check(31,'accepted scenarios',accepted,[D('.05'),D('.08')]);check(31,'rejection reasons',rejected,[('NaN','nonfinite'),('-1.10','return must exceed -100%')])
    check(31,'untrusted representation first',reject_scenarios(['.05',None])[0],[])
    check(32,'loop break success',search_loop_else(D(20000),D('.06'),D(50000)),'Reached in year 16')
    check(32,'normal exhaustion',search_loop_else(D(20000),D(0),D(50000)),'Not reached within 25 years')
    check(32,'period zero',search_loop_else(D(50000),D('.06'),D(50000)),'Reached at period 0')
    check(32,'last allowed year',search_loop_else(D(1),D(1),D(2)**25),'Reached in year 25')
    # Execute the two actual companion fragments using their stated missing prerequisites.
    source=COMP.read_text();blocks=re.findall(r'^```python\n(.*?)^```',source,re.M|re.S);snippets=[]
    for index,prelude,expected in [(9,dict(balance=D(10000),annual_return=D('.05')),D(10000)*D('1.05')**10),(10,dict(balance=D(10000),annual_return=D('.05'),annual_contribution=D(2000)),D(12500))]:
        state={'Decimal':D,**prelude}
        with localcontext() as context:
            context.prec=28;exec(compile(blocks[index],str(COMP),'exec'),state)
        check(15 if index==9 else 16,'exact companion snippet',state['balance'],expected,'exact source execution')
        snippets.append(dict(zero_based_fence=index,sha256=hashlib.sha256(blocks[index].encode()).hexdigest(),prelude={k:str(v) for k,v in prelude.items()},actual_balance=str(state['balance'])))
    def answer_section(n):
        match=re.search(r'^### 2\.13\.'+str(n)+r' — .*$',source,re.M);end=source.find('\n### ',match.end());return source[match.start():end if end!=-1 else len(source)]
    for n,result in [(18,original18),(29,original29)]:
        section=answer_section(n);raw=re.search(r'Internal balance: `([^`]+)`',section)[1]
        check(n,'published internal balance claim',result['balance'],D(raw),'published answer comparison')
        check(n,'published display',f"{result['balance']:,.2f}",re.search(r'displayed: `\$([^`]+)`',section)[1],'published answer comparison')
    section=answer_section(22)
    for period,value in discounted:
        claimed=re.search(r'Period '+str(period)+r' PV: `([^`]+)`',section)[1]
        check(22,'published per-period claim '+str(period),value,D(claimed),'published answer comparison')
    check(22,'published total claim',total,D(re.search(r'Total: `([^`]+)`',section)[1]),'published answer comparison')
    payload=dict(source_revision='9f792d034343fc946783af2036c2006a44e49235',python=sys.version,platform=platform.platform(),exercises_reviewed=19,predicates=len(checks),passed=sum(x['status']=='PASS' for x in checks),failed=sum(x['status']=='FAIL' for x in checks),checks=checks,benchmarks=benchmarks,source_snippets=snippets)
    (HERE/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('checks','benchmarks','source_snippets')},indent=2))
    return bool(payload['failed'])

if __name__=='__main__':raise SystemExit(run())
