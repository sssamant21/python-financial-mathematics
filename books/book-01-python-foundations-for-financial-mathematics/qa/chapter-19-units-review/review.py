"""Exact source execution and independent unit identities, not FX acceptance."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING,ROUND_HALF_UP,Overflow
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=ROOT/'chapter-19/19.10-currency-and-unit-normalization.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(REPO))],cwd=REPO,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,call,expected):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'currency_unit_normalization.py';path.write_text(code)
    for argv in [[sys.executable,str(path)],[sys.executable,'-m','compileall','-q',str(path)],[sys.executable,'-c','import currency_unit_normalization']]:
        z=subprocess.run(argv,cwd=tmp,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('unit_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for name,call,expected in [('cents',lambda:m.cents_to_dollars('10000'),Decimal('100')),('percent',lambda:m.percent_to_decimal('5'),Decimal('.05')),('one basis point',lambda:m.basis_points_to_decimal('1'),Decimal('.0001')),('hundred bp',lambda:m.basis_points_to_decimal('100'),Decimal('.01')),('negative rate unit',lambda:m.percent_to_decimal('-5'),Decimal('-.05')),('FX',lambda:m.convert_target_per_source('100','1.10'),Decimal('110')),('negative amount',lambda:m.convert_target_per_source('-100','1.10'),Decimal('-110')),('zero amount',lambda:m.convert_target_per_source('0','1.10'),Decimal('0')),('reciprocal',lambda:m.reciprocal('1.10'),Decimal('0.9090909090909090909090909091')),('reverse conversion',lambda:m.convert_target_per_source('110',str(m.reciprocal('1.10'))),Decimal('100')),('FX shift',lambda:m.convert_target_per_source('100','1.05'),Decimal('105')),('FX PnL',lambda:m.convert_target_per_source('100','1.05')-m.convert_target_per_source('100','1.10'),Decimal('-5')),('half even low tie',lambda:m.round_usd_cents('1.005'),Decimal('1.00')),('half even high tie',lambda:m.round_usd_cents('1.015'),Decimal('1.02')),('half even negative tie',lambda:m.round_usd_cents('-1.005'),Decimal('-1.00')),('no currency boundary by default',lambda:m.convert_target_per_source('1.005','1'),Decimal('1.005')),('numeric padding',lambda:m.decimal_text(' 1.00 '),Decimal('1.00')),('scientific text',lambda:m.decimal_text('1e2'),Decimal('100')),('scale preserved',lambda:m.decimal_text('1.00').as_tuple().exponent,-2)]:check(name,call,expected)
    for value in [None,True,1,Decimal('1'),'', ' ','abc','NaN','sNaN','Infinity','-Infinity']:check('reject text '+repr(value),lambda v=value:m.decimal_text(v),'ValueError')
    for rate in ['0','-1']:check('reject FX rate '+rate,lambda rate=rate:m.convert_target_per_source('100',rate),'ValueError');check('reject reciprocal '+rate,lambda rate=rate:m.reciprocal(rate),'ValueError')
    check('rate move percentage points',lambda:Decimal('6')-Decimal('5'),Decimal('1'))
    check('rate move relative',lambda:(Decimal('6')-Decimal('5'))/Decimal('5'),Decimal('.2'))
    # Exact half-even 28-digit report of 1/1.10=10/11; caller controls must not choose it.
    for rounding in [ROUND_FLOOR,ROUND_CEILING]:
        with localcontext() as ctx:
            ctx.rounding=rounding
            check('private reciprocal rounding '+rounding,lambda:m.reciprocal('1.10'),Decimal('0.9090909090909090909090909091'))
    with localcontext() as ctx:
        ctx.Emax=2
        check('private FX exponent bound',lambda:m.convert_target_per_source('1000','1.10'),Decimal('1100'))
        ctx.traps[Overflow]=False
        check('private FX trap/exponent policy',lambda:m.convert_target_per_source('1000','1.10'),Decimal('1100'))
    with localcontext() as ctx:
        ctx.prec=2
        check('private reciprocal precision',lambda:m.reciprocal('1.10'),Decimal('0.9090909090909090909090909091'))
        check('private cents precision',lambda:m.cents_to_dollars('123456.78'),Decimal('1234.5678'))
    # Lab8 explicitly chosen alternative is supplemental Decimal quantization.
    alternative=Decimal('1.005').quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    supplement=dict(name='lab8 half-up alternative',actual=str(alternative),expected='1.01',passed=alternative==Decimal('1.01'),scope='Supplemental policy comparison,not source settlement convention')
d=dict(selected_revision=REV,candidate_based_on='2b521783ba191220b3f1f3318ad4d94575e68c4b',manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,predicates=rows,supplemental_rounding=supplement,existing_methods=12,new_historical_unique_methods=0)
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;one separate supplemental rounding comparison')
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows) and supplement['passed']
