"""Sections3.7–3.9: exact source calls and explicit supplemental exercise variants."""
import ast,contextlib,doctest,hashlib,io,json,platform,re,sys,types
from decimal import Decimal,Inexact,ROUND_HALF_UP,getcontext,localcontext
from fractions import Fraction
from pathlib import Path
from typing import Literal,cast
HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]


def signed_difference(ending:Decimal,starting:Decimal)->Decimal:
    """Return signed same-currency ending minus starting amount.

    When interpreted as investment gain, assume no intermediate cash flows,
    fees, taxes or currency conversion. Inputs are validated finite Decimal;
    arithmetic uses the active context; no explicit cent quantization.
    """
    if not isinstance(ending,Decimal) or not isinstance(starting,Decimal):raise TypeError('Decimal inputs required')
    if not ending.is_finite() or not starting.is_finite():raise ValueError('Finite inputs required')
    return ending-starting


def typed_balance(balance:Decimal,rate:Decimal,*,contribution:Decimal=Decimal(0),timing:Literal['end','beginning'])->Decimal:
    """Advance one matching period; contribution occurs at end or beginning.

    Same currency; finite nonnegative balance/contribution; finite rate>-1;
    active Decimal context, no explicit quantization or external reads.
    TypeError for representations; ValueError for unsupported values/timing.
    No withdrawals, fees, taxes, inflation or currency conversion.
    """
    for value in (balance,rate,contribution):
        if not isinstance(value,Decimal):raise TypeError('Decimal inputs required')
        if not value.is_finite():raise ValueError('Finite inputs required')
    if balance<0 or contribution<0 or rate<=-1:raise ValueError('Unsupported domain')
    if timing not in ('end','beginning'):raise ValueError('Unsupported timing')
    return balance*(1+rate)+contribution if timing=='end' else (balance+contribution)*(1+rate)


def run():
    checks=[];provenance=[];modules={};codes={}
    def check(id,label,actual,expected):checks.append(dict(exercise=id,label=label,actual=str(actual),expected=str(expected),status='PASS' if actual==expected else 'FAIL'))
    def raises(id,label,expected,call):
        try:call();actual='no exception'
        except Exception as e:actual=type(e).__name__
        check(id,label,actual,expected)
    for n in (7,8,9):
        path=next((BOOK/'chapter-03').glob(f'3.{n:02}-*.md'));text=path.read_text();start=re.search(r'^## .*Hands-On Lab.*$',text,re.M).start();end=text.find('\n## ',start+1);code=re.findall(r'^```python\n(.*?)^```',text[start:end],re.M|re.S)[0];codes[n]=code
        module=types.ModuleType('lab_'+str(n));output=io.StringIO()
        with contextlib.redirect_stdout(output):exec(compile(code,str(path),'exec'),module.__dict__)
        modules[n]=module;provenance.append(dict(source=str(path.relative_to(BOOK)),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),code_sha256=hashlib.sha256(code.encode()).hexdigest(),import_stdout=output.getvalue()))
    D=Decimal
    for end,start,expected in [(10,5,5),(5,5,0),(5,10,-5)]:check('3.7-E1','typed signed difference',signed_difference(D(end),D(start)),D(expected))
    raises('3.7-E2','annotated NaN still rejected','ValueError',lambda:modules[7].future_value(D(100),D('NaN'),1))
    raises('3.7-E3','bool explicitly rejected','TypeError',lambda:modules[7].future_value(D(100),D('.05'),True))
    def first_qualifying(balances:list[Decimal],target:Decimal)->int|None:return modules[7].first_target_period(balances,target)
    period=first_qualifying([D(100),D(110)],D(100));check('3.7-E4','period zero handled as present',(period,period is not None),(0,True));check('3.7-E4','absent returns None',first_qualifying([D(100)],D(200)),None)
    Amount=Decimal;PeriodicRate=Decimal;check('3.7-E5','ordinary aliases same runtime type',Amount is PeriodicRate,True)
    raises('3.7-E6','wrong principal representation','TypeError',lambda:modules[7].future_value('100',D('.05'),1));raises('3.7-E6','negative count','ValueError',lambda:modules[7].future_value(D(100),D('.05'),-1))
    check('3.7-E7','Literal beginning timing',typed_balance(D(1000),D('.05'),contribution=D(100),timing='beginning'),D(1155));raises('3.7-E7','required keyword timing','TypeError',lambda:typed_balance(D(1000),D('.05')))
    text='100';check('3.7-E9','cast does not parse',(cast(Decimal,text) is text,type(cast(Decimal,text)).__name__),(True,'str'))
    check('3.8-E1','gain assumption documented','no intermediate cash flows' in signed_difference.__doc__,True)
    check('3.8-E2','two timing recurrences',(typed_balance(D(1000),D('.05'),contribution=D(100),timing='end'),typed_balance(D(1000),D('.05'),contribution=D(100),timing='beginning')),(D(1150),D(1155)))
    # Add a zero-principal doctest only to an in-memory teaching copy.
    tree=ast.parse(codes[8]);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='future_value');function.body[0].value.value+='\n    >>> future_value(Decimal("0"), Decimal("0.05"), 2) == Decimal("0")\n    True\n    '
    module=types.ModuleType('zero_principal_variant');exec(compile(ast.fix_missing_locations(tree),'zero_principal_variant','exec'),module.__dict__)
    output=io.StringIO()
    with contextlib.redirect_stdout(output):result=doctest.testmod(module,verbose=True)
    check('3.8-E3','added doctest failures',result.failed,0);check('3.8-E3','six total doctests',result.attempted,6)
    raises('3.8-E4','infinite principal matches Raises','ValueError',lambda:modules[8].future_value(D('Infinity'),D('.05'),2))
    # Temporary horizon policy revision, including docstring, plus explicit new boundary fixtures.
    tree=ast.parse(codes[8]);function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='future_value');count=0
    for node in ast.walk(function):
        if isinstance(node,ast.Constant) and isinstance(node.value,int) and not isinstance(node.value,bool) and node.value==1000:node.value=10;count+=1
        elif isinstance(node,ast.Constant) and isinstance(node.value,str):node.value=node.value.replace('through 1000','through 10').replace('between 0 and 1000','between 0 and 10')
    # Keep explanatory checks outside this changed-definition experiment.
    revised=types.ModuleType('horizon_variant');revised.Decimal=Decimal
    exec(compile(ast.fix_missing_locations(ast.Module([function],[])),'horizon_variant','exec'),revised.__dict__);state=revised.__dict__
    with contextlib.redirect_stdout(io.StringIO()): revised_result=doctest.testmod(revised)
    check('3.8-E8','revised docstring examples still valid',revised_result.failed,0)
    check('3.8-E8','one horizon constant changed',count,1);check('3.8-E8','new upper boundary',state['future_value'](D(100),D(0),10),D(100));raises('3.8-E8','above revised limit','ValueError',lambda:state['future_value'](D(100),D(0),11))
    f=modules[9].future_value;p=modules[9].present_value
    expected=Fraction(2000)*Fraction(26,25)**3;actual=f(D(2000),periodic_rate=D('.04'),periods=3);check('3.9-E1','exact rational FV',Fraction(actual),expected)
    check('3.9-E2','independently known amount PV',p(D('2249.728'),periodic_rate=D('.04'),periods=3),D(2000))
    check('3.9-E3','more negative rate higher PV',p(D(100),periodic_rate=D('-.2'),periods=1)>p(D(100),periodic_rate=D('-.1'),periods=1),True)
    raises('3.9-E4','fractional period','TypeError',lambda:p(D(100),periodic_rate=D('.05'),periods=1.5));raises('3.9-E4','string amount','TypeError',lambda:p('100',periodic_rate=D('.05'),periods=1))
    check('3.9-E6','annual12 percent is not monthly12 percent',D(100)*D('1.12')**12==D(100)*D('1.12'),False)
    def wrong_forward(value):return value*D('1.1')**2
    def wrong_back(value):return value/D('1.1')**2
    check('3.9-E7','wrong pair passes roundtrip',wrong_back(wrong_forward(D(100))),D(100));check('3.9-E7','independent5percent oracle catches wrong pair',wrong_forward(D(100))==D('110.25'),False)
    before=getcontext().copy()
    with localcontext() as c:
        c.prec=2;c.traps[Inexact]=True
        raises('3.9-E8','restricted context signals','Inexact',lambda:f(D(100),periodic_rate=D('.05'),periods=2))
    after=getcontext();check('3.9-E8','caller settings flags traps restored',(after.prec,after.rounding,dict(after.flags),dict(after.traps)),(before.prec,before.rounding,dict(before.flags),dict(before.traps)))
    raw=D('1.005');display=f'{raw:.2f}';quantized=raw.quantize(D('.01'),rounding=ROUND_HALF_UP)
    check('3.9-E9','format leaves raw unchanged',raw,D('1.005'));check('3.9-E9','early quantization changes later value',(raw*2,quantized*2),(D('2.010'),D('2.02')))
    payload=dict(source_revision='00b7cd53ca165d1e7d684ce54d1ea09ea3f13701',python=sys.version,platform=platform.platform(),exercise_records=27,predicates=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),source_provenance=provenance,added_doctest_transcript=output.getvalue(),checks=checks)
    (HERE/'results.json').write_text(json.dumps(payload,indent=2)+'\n');print(json.dumps({k:v for k,v in payload.items() if k not in ('source_provenance','checks','added_doctest_transcript')},indent=2));return bool(payload['failed'])

if __name__=='__main__':raise SystemExit(run())
