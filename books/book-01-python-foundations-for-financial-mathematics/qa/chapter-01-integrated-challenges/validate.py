"""Concrete Challenge 3 matrix, including retained CLI transcripts and rational oracles."""
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from build_extension import build
from reference import present_value, discount_amount, basis_points, simple_interest_report, money

HERE=Path(__file__).resolve().parent


def run():
    build()
    rows=[]
    def direct(category,operation,inputs,expected,reason,error=False):
        funcs={'PV':present_value,'discount':discount_amount,'bps':basis_points,'simple':simple_interest_report,'round':money}
        try:
            result=funcs[operation](*inputs)
            actual=repr(result)
            ok=not error and result==expected
        except ValueError as e:
            actual='ValueError: '+str(e)
            ok=error and expected in str(e)
        rows.append(dict(category=category,operation=operation,inputs=[str(i) for i in inputs],expected=repr(expected),actual=actual,reason=reason,status='PASS' if ok else 'FAIL'))
    direct('normal','PV',['110.25','5','2'],Decimal('100'),'100 grows to 110.25 in two 5% periods')
    direct('zero','PV',['0','5','2'],Decimal(0),'Zero receipt allowed')
    direct('zero','PV',['100','5','0'],Decimal(100),'No discount periods')
    direct('zero','PV',['100','0','10'],Decimal(100),'No discount rate')
    direct('meaningful negative','PV',['100','-50','1'],Decimal(200),'Negative effective rate can imply PV > FV')
    direct('large','PV',['1000000000000000000','0','100'],Decimal('1e18'),'Maximum input amount remains supported')
    direct('fractional','PV',['1.25','25','1'],Decimal(1),'Fractional amount is allowed')
    direct('normal','discount',['100','80'],Decimal(20),'Discount means a price reduction, not PV discounting')
    direct('zero','discount',['0','0'],Decimal(0),'Zero prices are permitted')
    direct('business boundary','discount',['100','100'],Decimal(0),'Equal prices imply zero reduction')
    direct('business boundary','discount',['100','100.01'],'0 <= final <= original','Markup excluded by this contract',True)
    direct('business boundary','discount',['100','-0.01'],'0 <= final <= original','Negative final price excluded',True)
    direct('fractional','discount',['10.005','9'],Decimal('1.005'),'Keep raw difference before final-only cents')
    direct('normal','bps',['25'],(Decimal('.0025'),Decimal('.25')),'Rate and percentage-point units distinguished')
    direct('meaningful negative','bps',['-25'],(Decimal('-.0025'),Decimal('-.25')),'Signed rate movement permitted')
    direct('fractional','bps',['0.5'],(Decimal('.00005'),Decimal('.005')),'Fractional basis points supported')
    direct('zero','bps',['0'],(Decimal(0),Decimal(0)),'Zero movement permitted')
    for text in ['abc','']:
        direct('invalid text','bps',[text],'decimal numeric text','Invalid Decimal conversion is handled',True)
    for text in ['NaN','sNaN','Infinity','-Infinity']:
        direct('nonfinite','bps',[text],'must be finite','Reject before comparisons/arithmetic',True)
    direct('precision boundary','bps',['.0000000000001'],'precision/magnitude','More than 12 decimal places rejected',True)
    direct('precision boundary','bps',['1e19'],'precision/magnitude','Above amount magnitude cap rejected',True)
    direct('resource boundary','bps',['1'*65],'64 characters','Bound external text size',True)
    for p,r,n,expected in [('100','-100','1','(-100, 1000]'),('100','-100.01','1','(-100, 1000]'),('100','1000.01','1','(-100, 1000]'),('-1','5','1','nonnegative'),('100','5','-1','0..100'),('100','5','101','0..100'),('100','5','1.5','whole integer'),('100','5','99999','0..100'),('100','-99','100','output bound')]:
        direct('mathematical/business boundary','PV',[p,r,n],expected,'Explicit selected PV domain',True)
    direct('rate upper boundary','PV',['1100','1000','1'],Decimal(100),'Inclusive maximum supported effective percent')
    direct('normal','simple',['1000','5','2'],(Decimal(100),'Interest: USD 100.00'),'Separate raw interest from posted display')
    direct('meaningful negative','simple',['1000','-5','2'],(Decimal(-100),'Interest: USD -100.00'),'Signed interest allowed; no savings balance guarantee')
    direct('fractional','simple',['100','5','.5'],(Decimal('2.5'),'Interest: USD 2.50'),'Fractional time allowed for simple interest')
    direct('rounding boundary','simple',['100','1.005','1'],(Decimal('1.005'),'Interest: USD 1.01'),'Raw value retained through final rounding')
    for p,r,n in [('0','5','1'),('100','5','-1'),('100','1000.01','1'),('100','5','100.01')]:
        direct('business boundary','simple',[p,r,n],'Require principal','Selected simple-interest contract enforced',True)
    for value,expected in [('1.004','1.00'),('1.005','1.01'),('1.006','1.01'),('-1.005','-1.01')]:
        direct('rounding boundary','round',[Decimal(value)],Decimal(expected),'Declared ROUND_HALF_UP; cents only at output')
    # Independently assess recurring PV with exact Fraction and a fixed relative bound.
    raw=present_value('100','7','10');oracle=Fraction(100)*Fraction(100,107)**10
    difference=abs(Fraction(raw)-oracle)
    rows.append(dict(category='independent oracle',operation='PV',inputs=['100','7','10'],expected='relative error <= 1e-35 against exact Fraction',actual=str(difference/abs(oracle)),reason='Independent rational oracle, not the Decimal implementation',status='PASS' if difference<=abs(oracle)*Fraction(1,10**35) else 'FAIL'))
    # Prove local policy does not inherit caller precision or rounding.
    with localcontext() as context:
        context.prec=6
        raw2=present_value('100','7','10')
    rows.append(dict(category='context isolation',operation='PV',inputs=['100','7','10','caller precision 6'],expected=str(raw),actual=str(raw2),reason='Local 40-digit policy',status='PASS' if raw2==raw else 'FAIL'))
    cli_cases=[
        ('original SI','1\n1000\n5\n2\n','Interest:       $100.00'),
        ('original FV','2\n1000\n5\n2\n1\n','Future Value:  $1,102.50'),
        ('original change','3\n100\n110\n','Percentage Change: 10.00%'),
        ('original trade','4\n100\n110\n2\n','Status: PROFIT'),
        ('original fee','5\n100\n1\n','Fee:                $1.00'),
        ('original reconciliation','6\n100\n100.01\n.01\n','Status: WITHIN TOLERANCE'),
        ('PV','7\n110.25\n5\n2\n','Present Value: USD 100.00'),
        ('PV negative rate','7\n100\n-50\n1\n','Present Value: USD 200.00'),
        ('PV invalid periods','7\n100\n5\n1.5\n','Invalid input: Periods must be whole integer text'),
        ('PV invalid factor','7\n100\n-100\n1\n','Invalid input: Effective rate percent'),
        ('discount rounding','8\n10.005\n9\n','Discount Amount: USD 1.01'),
        ('discount invalid markup','8\n100\n101\n','Invalid input: Price reduction'),
        ('bps','9\n25\n','Decimal rate: 0.0025\nPercentage points: 0.25'),
        ('bps negative','9\n-25\n','Decimal rate: -0.0025'),
        ('bps nonfinite','9\nNaN\n','Invalid input: Financial input must be finite'),
        ('bps invalid text','9\nabc\n','Invalid input: Enter decimal numeric text'),
        ('invalid menu','10\n','Invalid calculator selection.'),
    ]
    transcripts=[]
    for label,stdin,expected in cli_cases:
        proc=subprocess.run([sys.executable,str(HERE/'extended_calculator.py')],input=stdin,text=True,capture_output=True,timeout=5)
        ok=proc.returncode==0 and expected in proc.stdout and not proc.stderr
        rows.append(dict(category='CLI integration',operation=label,inputs=stdin.splitlines(),expected=expected,actual=proc.stdout,reason='Fresh subprocess; original handled input errors retain exit code zero',status='PASS' if ok else 'FAIL'))
        transcripts.append(dict(label=label,stdin=stdin,stdout=proc.stdout,stderr=proc.stderr,exit_code=proc.returncode))
    output=dict(source_revision='7ee99f60d5089510f860a0b6f695f971beb2eac6',python=sys.version,platform=platform.platform(),checks=len(rows),passed=sum(r['status']=='PASS' for r in rows),failed=sum(r['status']=='FAIL' for r in rows),cli_cases=len(cli_cases),matrix=rows,transcripts=transcripts)
    (HERE/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    def clean(value):
        return str(value).replace('|', '\\|').replace('\n', ' / ')
    table = '# Integrated challenge test matrix\n\nSee [results.json](results.json) for actual results and complete CLI transcripts. Predicates are not counts of exercises or reference methods.\n\n| # | Category | Operation | Inputs | Expected | Status | Reason |\n|---|---|---|---|---|---|---|\n'
    for i, row in enumerate(rows, 1):
        table += '| ' + ' | '.join(map(clean, [i, row['category'], row['operation'], row['inputs'], row['expected'], row['status'], row['reason']])) + ' |\n'
    (HERE/'MATRIX.md').write_text(table)
    print(json.dumps({k:v for k,v in output.items() if k not in ('matrix','transcripts')},indent=2))
    return bool(output['failed'])

if __name__=='__main__':raise SystemExit(run())
