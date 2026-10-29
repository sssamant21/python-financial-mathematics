"""Exercises 33–60: actual executions and independent expected results."""
import contextlib
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
from reference import investment_valid, contribution_valid, period_valid, finite_decimal, rate_error, analyze, report, quality, pv_grid, annual_schedule

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
COMP=BOOK/'chapter-02/solutions/2.13-solutions-and-reference-implementations.md'


def closed(p,r,c,n):
    p,r,c=map(F,(p,r,c))
    return p*(1+r)**n+(n*c if r==0 else c*((1+r)**n-1)/r)


def source_inputs():
    blocks=re.findall(r'^```python\n(.*?)^```',COMP.read_text(),re.M|re.S)
    state={'Decimal':D};exec(compile(blocks[11],str(COMP),'exec'),state)
    args=[state[x] for x in ('initial_investment','annual_contribution','target_balance','maximum_years','return_scenarios')]
    return args,hashlib.sha256(blocks[11].encode()).hexdigest()


def run():
    checks=[];models=[]
    def check(ex,label,actual,expected,kind='supplemental execution'):
        checks.append(dict(exercise=ex,label=label,kind=kind,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
    def oracle(ex,label,actual,expected):
        error=abs(F(actual)-expected);bound=max(F(1),abs(expected))*F(1,10**26)
        checks.append(dict(exercise=ex,label=label,kind='exact rational benchmark',actual=str(actual),expected=str(expected),error=str(error),bound=str(bound),status='PASS' if error<=bound else 'FAIL'))
    def model(ex,p,c,t,h,rates):
        result=analyze(D(p),D(c),D(t),h,rates)
        for row in result['results']:
            rate=F(row['rate']);year=next((n for n in range(h+1) if closed(p,rate,c,n)>=F(t)),None)
            check(ex,'first crossing '+str(row['rate']),row['first_year'],year)
            ending=year if year is not None else h
            check(ex,'ending period',row['ending_year'],ending)
            oracle(ex,'ending balance',row['balance'],closed(p,rate,c,ending))
        counts=result['counts']
        check(ex,'scenario reconciliation',counts['evaluated']+counts['rejected'],counts['total'])
        check(ex,'outcome reconciliation',counts['reached']+counts['not_reached'],counts['evaluated'])
        models.append(dict(exercise=ex,inputs=[p,c,t,h,[str(r) for r in rates]],actual=result))
        return result
    for value,expected in [(D(25000),True),(D(0),False),(D(-1),False),(D('NaN'),False),(None,False),('25000',False)]:check(33,'positive finite '+str(value),investment_valid(value),expected)
    for value,expected in [(D(0),True),(D(-1),False),(D(1),True),(D('Infinity'),False)]:check(34,'contribution '+str(value),contribution_valid(value),expected)
    for value,expected in [(20,True),(True,False),(False,False),(0,False),(1,True),(100,True),(101,False),(D(20),False)]:check(35,'whole horizon '+str(value),period_valid(value),expected)
    for value,expected in [(D('.05'),True),(D('NaN'),False),(D('Infinity'),False),(D('-Infinity'),False)]:check(36,'finiteness '+str(value),finite_decimal(value),expected)
    for r,g,expected in [('.09','.04',True),('.04','.04',False),('.03','.04',False)]:check(37,'stable growth '+r+'/'+g,D(r)>D(g),expected,'reasoning probe')
    for value,expected in [(None,'missing rate'),('.05','rate must be Decimal'),(D('NaN'),'annual return is non-finite'),(D('-1'),'annual return must exceed -100%'),(D('.05'),None)]:check(38,'dependency stage '+str(value),rate_error(value),expected)
    single=model(39,'15000','6000','75000',20,[D('.04')]);check(39,'published exact raw balance',single['results'][0]['balance'],D('75813.8933168701440000'),'published claim comparison')
    multi=model(40,'15000','6000','75000',20,list(map(D,('.02','.04','.06','.08'))))
    check(40,'published target years',[r['first_year'] for r in multi['results']],[9,8,8,7],'published claim comparison')
    check(40,'published display amounts',[f"{r['balance']:,.2f}" for r in multi['results']],['76,454.16','75,813.89','83,292.53','79,244.18'],'published claim comparison')
    counts,reasons=quality([D(5000),None,D(-2500),D('NaN'),D(0),D(4200),None]);check(41,'two-level quality counts',counts,dict(processed=4,missing=2,rejected=1,positive=2,negative=1,zero=1));check(41,'rejection retained',reasons,[(3,'finite Decimal cash flow required')])
    grid,rejections=pv_grid(list(map(D,(10000,12000,15000))),list(map(D,('.04','.06','.08'))))
    for rate,rows,total in grid:oracle(42,'PV grid '+str(rate),total,sum((F(cf)/(1+F(rate))**n for n,cf in enumerate((10000,12000,15000),1)),F(0)))
    check(42,'published PV grid',[f'{total:,.2f}' for _,_,total in grid],['34,045.00','32,708.21','31,454.81'],'published claim comparison')
    check(42,'invalid discount scenario recorded',pv_grid([D(100)],[D('-1'),D('NaN')])[1],[(0,'annual return must exceed -100%'),(1,'annual return is non-finite')])
    end=annual_schedule(D(10000),D('.05'),D(2000),5)[-1][1];beginning=annual_schedule(D(10000),D('.05'),D(2000),5,True)[-1][1]
    oracle(43,'end-year value',end,closed(10000,'.05',2000,5));oracle(43,'beginning-year value',beginning,closed(10000,'.05',0,5)+F(2000)*F(21,20)*((F(21,20)**5-1)/F(1,20)))
    check(43,'published timing displays',(f'{end:,.2f}',f'{beginning:,.2f}'),('23,814.08','24,366.64'),'published claim comparison')
    balance=D('99999.996');target=D('100000')
    check(44,'raw versus policy versus display',(balance>=target,balance.quantize(D('.01'),rounding=ROUND_HALF_UP)>=target,f'{balance:,.2f}'),(False,True,'100,000.00'))
    tied=model(45,'100','0','105',5,[D('.05'),D('.06'),D('.01')]);check(45,'retain both earliest scenarios',tied['earliest_indices'],[0,1]);check(45,'earliest year',tied['earliest_year'],1)
    reversed_ties=analyze(D(100),D(0),D(105),5,[D('.01'),D('.06'),D('.05')])
    check(45,'reverse order preserves rates in tie',{reversed_ties['results'][i]['rate'] for i in reversed_ties['earliest_indices']},{D('.05'),D('.06')})
    check(46,'include final year',list(range(1,4+1)),[1,2,3,4]);check(46,'wrong stop excludes horizon',4 in range(1,4),False,'deliberate counterexample')
    reversed_model=analyze(D(15000),D(6000),D(75000),20,list(reversed(list(map(D,('.02','.04','.06','.08'))))))
    check(47,'state independent of order',{r['rate']:r['balance'] for r in multi['results']},{r['rate']:r['balance'] for r in reversed_model['results']})
    check(48,'bool is int but rejected',(isinstance(True,int),period_valid(True)),(True,False))
    check(49,'NaN rejection before comparison',rate_error(D('NaN')),'annual return is non-finite')
    check(50,'display reparse changes decision',(balance>=target,D(f'{balance:.2f}')>=target),(False,True),'deliberate counterexample')
    check(51,'missing counts retained',quality([None,D(0)])[0],dict(processed=1,missing=1,rejected=0,positive=0,negative=0,zero=1))
    check(52,'one period operation order',(annual_schedule(D(100),D('.1'),D(10),1)[0][1],annual_schedule(D(100),D('.1'),D(10),1,True)[0][1]),(D(120),D(121)))
    check(53,'pre versus post update target',(D(100)>=D(105),D(100)*D('1.1')>=D(105)),(False,True),'reasoning probe')
    check(54,'invalid remains rejected',rate_error(D('NaN')) is not None,True,'reasoning probe')
    check(55,'clamping changes assumption',D('.30')==min(D('.30'),D('.25')),False,'reasoning probe')
    check(57,'mathematical relationship only',D('.20')>D('.19'),True,'reasoning probe')
    check(58,'specific rejection text',rate_error(D('NaN')),'annual return is non-finite')
    args,source_hash=source_inputs();integrated=model(59,str(args[0]),str(args[1]),str(args[2]),args[3],args[4])
    check(59,'published first crossing years',[r['first_year'] for r in integrated['results']],[16,14,12,10],'published claim comparison')
    check(59,'published ending displays',[f"{r['balance']:,.2f}" for r in integrated['results']],['153,019.28','161,701.76','161,585.54','151,687.12'],'published claim comparison')
    check(59,'published reconciliation',integrated['counts'],dict(total=6,evaluated=4,rejected=2,reached=4,not_reached=0),'published claim comparison')
    check(59,'earliest unique year',(integrated['earliest_year'],integrated['earliest_indices']),(10,[3]))
    check(59,'rejection reasons',[r['reason'] for r in integrated['rejections']],['annual return is non-finite','annual return must exceed -100%'])
    model(59,'100','0','100',1,[D(0)])
    failed=model(59,'100','0','200',2,[D(0),D('-.1')]);check(59,'no reached scenario',(failed['earliest_year'],failed['earliest_indices']),(None,[]))
    model(59,'100','100','300',2,[D(0)])
    for fields,fragment in [((D(0),D(0),D(100),1,[]),'principal'),((D(100),D(-1),D(100),1,[]),'contribution'),((D(100),D(0),D('NaN'),1,[]),'target'),((D(100),D(0),D(100),True,[]),'years')]:
        try:analyze(*fields);actual='accepted'
        except ValueError as error:actual=str(error)
        check(59,'shared invalid '+fragment,fragment in actual,True)
    transcript=report(integrated);(HERE/'analyzer-output.txt').write_text(transcript+'\n')
    check(59,'report includes assumptions/rejection/tie/caveat',all(s in transcript for s in ('end-of-year','non-finite','Earliest year: 10','not an investment recommendation')),True)
    (HERE/'models.json').write_text(json.dumps(models,default=str,indent=2)+'\n')
    payload=dict(source_revision='8ebbdb6859b8d23a1b62fd114c13a1f19de3370c',python=sys.version,platform=platform.platform(),exercises_reviewed=28,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),source_inputs_fence_index=11,source_inputs_sha256=source_hash,checks=checks)
    (HERE/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k!='checks'},indent=2))
    return bool(payload['failed'])

if __name__=='__main__':raise SystemExit(run())
