"""Supplemental answers/checks, stdlib only. Run from any directory; --cli for pipeline."""
import contextlib
from datetime import date
from decimal import Decimal
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import platform
import subprocess
import sys


def calculate_future_value(principal, rate, periods):
    return principal * (1 + rate) ** periods


def parsed_principal(text):
    try:
        return float(text)
    except ValueError:
        raise ValueError('Principal must be numeric') from None


def pipeline(principal_text, percent_text, years_text):
    principal = parsed_principal(principal_text)
    percent = float(percent_text)
    years = int(years_text)
    if not math.isfinite(principal) or not math.isfinite(percent):
        raise ValueError('Principal and rate must be finite')
    if principal <= 0:
        raise ValueError('Principal must be positive')
    if years < 0:
        raise ValueError('Years must be nonnegative')
    if percent <= -100:
        raise ValueError('Annual effective percent must exceed -100')
    rate = percent / 100
    try:
        value = calculate_future_value(principal, rate, years)
    except OverflowError:
        raise ValueError('Future value exceeds float range') from None
    if not math.isfinite(value) or (principal > 0 and value == 0):
        raise ValueError('Future value outside representable positive float range')
    return (f'Principal: USD {principal:,.2f}\nAnnual effective rate: {rate:.2%}\n'
            f'Years: {years}\nFuture value: USD {value:,.2f}\n'
            'Assumptions: constant annual compounding; no fees, tax or cash flows; '
            'float teaching arithmetic; display only, no interim rounding.')


def cli():
    try:
        p = input('Principal (USD): ')
        r = input('Annual effective rate (%): ')
        n = input('Years (whole): ')
        print(pipeline(p, r, n))
    except (ValueError, EOFError) as error:
        print(f'Input error: {error}')
        return 2
    return 0


def run():
    results = []
    def check(id, label, actual, expected, close=False):
        ok = math.isclose(actual, float(expected)) if close else actual == expected
        results.append(dict(id=id, label=label, actual=str(actual), expected=str(expected), status='PASS' if ok else 'FAIL'))
    def rejects(id, label, texts, message):
        try:
            pipeline(*texts)
            actual = 'accepted'
        except ValueError as error:
            actual = str(error)
        check(id, label, actual, message)
    # Fractions are exact rational oracles, distinct from the float power implementation.
    for id,p,r,n,oracle in [
        ('S06-E01',5000,.04,5,Fraction(5000)*Fraction(26,25)**5),
        ('S06-E02',10000,.03,10,Fraction(10000)*Fraction(103,100)**10),
        ('S06-E02',10000,.05,10,Fraction(10000)*Fraction(21,20)**10),
        ('S06-E02',10000,.07,10,Fraction(10000)*Fraction(107,100)**10),
        ('S06-E03',1000,.05,3,Fraction(9261,8)),
        ('S06-E04',2500,.06,4,Fraction(7890481,2500)),
        ('S08-E04',50000,.07,10,Fraction(50000)*Fraction(107,100)**10)]:
        check(id,'FV rational benchmark',calculate_future_value(p,r,n),oracle,True)
    check('S06-E01','formatted result',f'{calculate_future_value(5000,.04,5):,.2f}','6,083.26')
    check('S06-E01','display contract',f'Principal: {5000:,.2f}; rate: {.04:.2%}; periods: {5}', 'Principal: 5,000.00; rate: 4.00%; periods: 5')
    check('S06-E03','incorrect rate diagnosis',calculate_future_value(1000,5,3),216000)
    values=[1000.0,.05,3,'USD',True]
    check('S07-E01','types',[type(v).__name__ for v in values],['float','float','int','str','bool'])
    check('S07-E02','float sum',repr(.1+.1+.1),'0.30000000000000004')
    check('S07-E02','Decimal sum',str(sum([Decimal('.1')]*3)),'0.3')
    check('S07-E03','exact vs approximate',((.1+.1+.1)==.3,math.isclose(.1+.1+.1,.3)),(False,True))
    bond=dict(name='Example zero coupon',face_value=Decimal('1000'),coupon_rate=Decimal('0'),currency='USD',maturity_date=date(2030,1,1),callable=False)
    check('S07-E04','bond fields',set(bond),{'name','face_value','coupon_rate','currency','maturity_date','callable'})
    check('S07-E04','maturity and callable types',(type(bond['maturity_date']).__name__,type(bond['callable']).__name__),('date','bool'))
    check('S07-E05','basis points',250/10000,.025)
    check('S07-E06','zero is not missing',bond['coupon_rate'] is None,False)
    check('S08-E01','net and ratios',(150000-112500,112500/150000,(150000-112500)/150000),(37500,.75,.25))
    weights=[v/100000 for v in (75000,20000,5000)]
    check('S08-E02','total',sum((75000,20000,5000)),100000)
    check('S08-E02','weights',weights,[.75,.2,.05]);check('S08-E02','weight sum',sum(weights),1,True)
    check('S08-E03','spread',150/10000,.015);check('S08-E03','combined',.0375+150/10000,.0525,True)
    fv=calculate_future_value(50000,.07,10)
    check('S08-E04','growth display',f'{fv-50000:,.2f}','48,357.57');check('S08-E04','relative growth',fv/50000-1,Fraction(107,100)**10-1,True)
    check('S08-E05','true vs floor',(100/12,100//12),(8.333333333333334,8))
    check('S08-E06','corrected exponent',calculate_future_value(100,.1,2),121,True)
    check('S08-E07','opposite percentage changes',1000*1.2*.8,960)
    check('S08-E08','Python integer addition',100+5,105) # Dimensional invalidity is prose review.
    check('S09-E01','translated FV',calculate_future_value(100,.05,1),105,True)
    factor=(1+.05)**2
    check('S09-E02','compact PV',110.25/(1+.05)**2,100,True);check('S09-E02','decomposed PV',110.25/factor,100,True)
    check('S09-E03','grouped return',(110-100)/100,.1);check('S09-E03','wrong return',110-100/100,109)
    check('S09-E04','grouped average',(1+2+3+4)/4,2.5)
    check('S09-E05','precedence',(-3**2,(-3)**2,3**-2),(-9,9,1/9))
    check('S09-E06','associativity',(2**3**2,(2**3)**2),(512,64))
    check('S09-E07','portfolio return',.5*.1+.3*.04+.2*(-.02),Fraction(29,500),True)
    check('S09-E08','combined rate',.0425+75/10000,.05,True);check('S09-E09','percent normalization',5/100,.05)
    for r,n,expected in [(.05,0,100),(0,7,100),(.05,1,105)]: check('S09-E10','known-result case',calculate_future_value(100,r,n),expected,True)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        original=sys.stdin
        try:
            sys.stdin=io.StringIO('1000\n');value=input('Enter a value: ')
        finally: sys.stdin=original
    check('S10-E01','actual input return',(value,type(value).__name__),('1000','str'))
    check('S10-E02','parsed value/type',(parsed_principal(value),type(parsed_principal(value)).__name__),(1000.0,'float'))
    check('S10-E03','rate normalization',float('6.25')/100,.0625)
    check('S10-E04','whole periods',int('12'),12)
    try: int('12.5');actual='accepted'
    except ValueError: actual='ValueError'
    check('S10-E04','fractional text rejected',actual,'ValueError')
    rejects('S10-E05','invalid text',('abc','5','1'),'Principal must be numeric')
    for p,r,n,msg in [('0','5','1','Principal must be positive'),('-1','5','1','Principal must be positive'),('100','5','-1','Years must be nonnegative')]:rejects('S10-E06','domain boundary',(p,r,n),msg)
    for p,r in [('nan','5'),('inf','5'),('100','nan'),('100','-inf')]:rejects('S10-E07','nonfinite input',(p,r,'1'),'Principal and rate must be finite')
    value=1234567.891;rate=.0475
    check('S10-E08','money display',f'${value:,.2f}','$1,234,567.89');check('S10-E08','value preserved',value,1234567.891)
    check('S10-E09','percent display',f'{rate:.2%}','4.75%');check('S10-E09','rate preserved',rate,.0475)
    rejects('S10-E10','rate boundary',('100','-100','1'),'Annual effective percent must exceed -100')
    rejects('S10-E10','overflow',('1e308','100','10'),'Future value outside representable positive float range')
    check('S10-E11','normal output', 'Future value: USD 1,102.50' in pipeline('1000','5','2'),True)
    cases=[('normal','1000\n5\n2\n',0,'Future value: USD 1,102.50'),('zero horizon','100\n5\n0\n',0,'Future value: USD 100.00'),('negative rate','100\n-50\n1\n',0,'Future value: USD 50.00'),('invalid text','abc\n5\n2\n',2,'Input error: Principal must be numeric'),('fractional periods','100\n5\n12.5\n',2,'Input error:'),('nonfinite','nan\n5\n2\n',2,'Input error: Principal and rate must be finite'),('missing input','100\n',2,'Input error:')]
    transcripts=[]
    for label,stdin,code,fragment in cases:
        result=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--cli'],input=stdin,text=True,capture_output=True,timeout=5)
        check('S10-E12',label,(result.returncode,fragment in result.stdout,result.stderr),(code,True,''))
        transcripts.append(dict(label=label,stdin=stdin,stdout=result.stdout,stderr=result.stderr,exit_code=result.returncode))
    here=Path(__file__).parent;root=here.parents[3]
    answers=json.loads((here/'answers.json').read_text())
    for path,sha in {(a['source'],a['source_sha256']) for a in answers}:
        check('PROVENANCE',path,hashlib.sha256((root/path).read_bytes()).hexdigest(),sha)
    payload=dict(python=sys.version,platform=platform.platform(),source_revision='ef9b06d8893c180b28a81de6dc07f0ba91fdf307',answer_records=len(answers),runtime_predicates=len(results),passed=sum(x['status']=='PASS' for x in results),failed=sum(x['status']=='FAIL' for x in results),checks=results,cli_transcripts=transcripts)
    (here/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('checks','cli_transcripts')},indent=2))
    return bool(payload['failed'])

if __name__=='__main__':
    raise SystemExit(cli() if '--cli' in sys.argv else run())
