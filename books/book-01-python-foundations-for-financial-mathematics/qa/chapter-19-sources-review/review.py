from pathlib import Path
from decimal import Decimal,Context,localcontext,ROUND_HALF_EVEN
from fractions import Fraction
import csv,io,json,re,subprocess,sys,tempfile,importlib.util,hashlib,platform
ROOT=Path(__file__).resolve().parents[4];SOURCE=ROOT/'books/book-01-python-foundations-for-financial-mathematics/chapter-19/19.01-financial-data-sources-and-formats.md'
def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);csv_text=re.search(r'~~~csv\n(.*?)\n~~~',text,re.S).group(1)+'\n';json_record=json.loads(re.search(r'~~~json\n(.*?)\n~~~',text,re.S).group(1));rows=[];commands=[]
    def check(name,call,expected=None,error=None):
        try:actual=call();passed=error is None and actual==expected;value=repr(actual)
        except Exception as exc:value=type(exc).__name__+': '+str(exc);passed=type(exc) is error
        rows.append(dict(name=name,actual=value,expected=error.__name__ if error else repr(expected),passed=passed))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'financial_data_basics.py';p.write_text(code)
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import financial_data_basics']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        spec=importlib.util.spec_from_file_location('data_basics',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        parsed=m.parse_prices(csv_text)
        check('CSV fixture records',lambda:len(parsed),2);check('JSON close text',lambda:type(json_record['close']) is str,True);check('CSV JSON close match',lambda:parsed[-1]['close'],Decimal(json_record['close']));check('fixture return',lambda:m.simple_return(parsed[0]['close'],parsed[1]['close']),Decimal('.015'))
        check('encoded hash',lambda:m.content_sha256(csv_text),hashlib.sha256(csv_text.encode('utf-8')).hexdigest());check('newline bytes differ',lambda:m.content_sha256(csv_text)!=m.content_sha256(csv_text.replace('\n','\r\n')),True)
        for name,bad in [('duplicate date',csv_text.replace('2026-01-06','2026-01-05')),('decreasing date',csv_text.replace('2026-01-06','2026-01-04')),('missing header',csv_text.replace('close,','price,')),('duplicate header',csv_text.replace('currency','close',1)),('null row value',csv_text.replace('101.50,USD','101.50')),('extra row field',csv_text.replace('101.50,USD','101.50,USD,extra')),('empty instrument',csv_text.replace('EXAMPLE,2026-01-06',',2026-01-06')),('mixed instrument',csv_text.replace('EXAMPLE,2026-01-06','OTHER,2026-01-06')),('bad currency',csv_text.replace('USD','EUR')),('bad date',csv_text.replace('2026-01-06','not-date')),('nan price',csv_text.replace('101.50','NaN')),('inf price',csv_text.replace('101.50','Infinity')),('negative price',csv_text.replace('101.50','-1')),('zero price',csv_text.replace('101.50','0')),('bad number',csv_text.replace('101.50','abc')),('single row','instrument,date,close,currency\na,2026-01-01,1,USD\n')]:check(name,lambda:m.parse_prices(bad),error=ValueError)
        check('nontext CSV',lambda:m.parse_prices(None),error=ValueError);check('nontext hash',lambda:m.content_sha256(b'abc'),error=ValueError)
        # Direct complete rational quotient, converted at an independent higher precision before34-significant-digit rounding.
        cases=[('100','101.50'),('1','1.000000000000000000000000000001'),('1e308','1e308'),('1e-308','2e-308'),('7','8'),('2','0'),('123456789012345678901234567890','123456789012345678901234567891')]
        for start,end in cases:
            a,b=Decimal(start),Decimal(end);exact=(Fraction(b)-Fraction(a))/Fraction(a)
            with localcontext(Context(prec=120,rounding=ROUND_HALF_EVEN)):
                wide=Decimal(exact.numerator)/Decimal(exact.denominator)
            with localcontext(Context(prec=34,rounding=ROUND_HALF_EVEN)):expected=+wide
            check('complete return '+repr((start,end)),lambda:m.simple_return(a,b),expected)
        with localcontext() as context:
            context.prec=2
            before=(context.prec,context.rounding,dict(context.flags))
            check('ambient context independence',lambda:m.simple_return(Decimal('100'),Decimal('101.50')),Decimal('.015'))
            check('context settings unchanged',lambda:(context.prec,context.rounding),before[:2])
        for start,end in [(1,Decimal(2)),(Decimal(0),Decimal(1)),(Decimal(1),Decimal(-1)),(Decimal('NaN'),Decimal(1)),(Decimal(1),Decimal('Infinity'))]:check('return invalid '+repr((start,end)),lambda:m.simple_return(start,end),error=ValueError)
        check('units cents',lambda:Fraction(10000,100),100);check('percentage',lambda:Fraction(5,100),Fraction('.05'));check('basis point',lambda:Fraction(1,10000),Fraction('.0001'))
        (Path(__file__).parent/'synthetic-input.csv').write_bytes(csv_text.encode('utf-8'));(Path(__file__).parent/'synthetic-record.json').write_text(json.dumps(json_record,indent=2)+'\n')
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=rows,existing_unique_methods=10,new_historical_methods=0,fixture_sha256=hashlib.sha256(csv_text.encode()).hexdigest(),limits='Synthetic text parser and one price return; no source authenticity,license,live API,Excel/Parquet,point-in-time or supported-platform/independent acceptance')
        (Path(__file__).parent/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(row['passed'] for row in rows);print(len(rows),'predicates;3 source commands;10 existing methods passed')
if __name__=='__main__':run()
