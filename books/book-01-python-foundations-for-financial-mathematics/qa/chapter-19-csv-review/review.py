from pathlib import Path
from decimal import Decimal,localcontext
import re,subprocess,tempfile,importlib.util,sys,csv,io,json,hashlib,platform
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics';SOURCE=BOOK/'chapter-19/19.02-csv-and-text-data.md'
def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();blocks=re.findall(r'~~~python\n(.*?)\n~~~',text,re.S);raw=(re.search(r'~~~csv\n(.*?)\n~~~',text,re.S).group(1)+'\n').encode();bom=b'\xef\xbb\xbf'+raw;crlf=raw.replace(b'\n',b'\r\n');commands=[];rows=[]
    def check(name,call,expected=None,error=None):
        try:value=call();ok=error is None and value==expected;actual=repr(value)
        except Exception as exc:actual=type(exc).__name__+': '+str(exc);ok=type(exc) is error
        rows.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(expected)))
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp);(temp/'prices.csv').write_bytes(bom)
        for name,code in zip(['read_example.py','write_example.py','csv_financial_data.py'],blocks): (temp/name).write_text(code)
        for args in [[sys.executable,'read_example.py'],[sys.executable,'write_example.py'],[sys.executable,'csv_financial_data.py'],[sys.executable,'-m','compileall','-q','.'],[sys.executable,'-c','import csv_financial_data']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        p=temp/'csv_financial_data.py';spec=importlib.util.spec_from_file_location('csv_data',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        check('records',lambda:len(m.parse_csv(raw)),2);check('BOM normalization',lambda:m.parse_csv(raw)==m.parse_csv(bom),True);check('CRLF normalization',lambda:m.parse_csv(raw)==m.parse_csv(crlf),True)
        check('raw digest',lambda:m.raw_sha256(raw),hashlib.sha256(raw).hexdigest());check('BOM digest differs',lambda:m.raw_sha256(raw)!=m.raw_sha256(bom),True);check('CRLF digest differs',lambda:m.raw_sha256(raw)!=m.raw_sha256(crlf),True)
        output=(temp/'output.csv').read_bytes();check('writer dialect rows',lambda:list(csv.DictReader(io.StringIO(output.decode(),newline=''))),[{'instrument':'EXAMPLE','close':'101.50'}]);check('writer columns order',lambda:output.splitlines()[0],b'instrument,close')
        quoted=raw.replace(b'EXAMPLE',b'"Example, Class A"');check('quoted comma',lambda:m.parse_csv(quoted)[0]['instrument'],'Example, Class A')
        quoted_newline=raw.replace(b'EXAMPLE',b'"Example\nClass A"');check('quoted newline logical rows',lambda:len(m.parse_csv(quoted_newline)),2);check('quoted newline field',lambda:m.parse_csv(quoted_newline)[0]['instrument'],'Example\nClass A')
        cases=[('bad UTF8',b'\xff'),('wrong type',None),('no header',b''),('missing header',raw.replace(b'close,',b'price,')),('duplicate header',raw.replace(b'close,currency',b'close,close')),('extra column',raw.replace(b'close,currency',b'close,currency,extra')),('duplicate key',raw.replace(b'2026-01-06',b'2026-01-05')),('empty price',raw.replace(b'101.50',b'')),('NA price',raw.replace(b'101.50',b'NA')),('NaN price',raw.replace(b'101.50',b'NaN')),('inf price',raw.replace(b'101.50',b'Infinity')),('negative price',raw.replace(b'101.50',b'-1')),('zero price',raw.replace(b'101.50',b'0')),('short row',raw.replace(b'101.50,USD',b'101.50')),('long row',raw.replace(b'101.50,USD',b'101.50,USD,extra')),('bad currency',raw.replace(b'USD',b'EUR')),('empty instrument',raw.replace(b'EXAMPLE,2026-01-06',b',2026-01-06')),('invalid date',raw.replace(b'2026-01-06',b'bad')),('malformed header',b'instrument,date,"close,currency\n'),('malformed row',raw+b'"unterminated')]
        for name,bad in cases:check(name,lambda:m.parse_csv(bad),error=ValueError)
        check('unsorted accepted',lambda:len(m.parse_csv(raw.replace(b'2026-01-06',b'2026-01-04'))),2)
        check('different instruments same date accepted',lambda:len(m.parse_csv(raw.replace(b'EXAMPLE,2026-01-06',b'OTHER,2026-01-05'))),2)
        for start,end,expected in [('100','101.50','.015'),('1','1.000000000000000000000000000001','1e-30'),('2','0','-1')]:check('return '+repr((start,end)),lambda:m.simple_return(Decimal(start),Decimal(end)),Decimal(expected))
        with localcontext() as ctx:
            ctx.prec=2;check('private return context',lambda:m.simple_return(Decimal('100'),Decimal('101.50')),Decimal('.015'))
        for a,b in [(Decimal(0),Decimal(1)),(Decimal(1),Decimal(-1)),(True,Decimal(1))]:check('invalid return '+repr((a,b)),lambda:m.simple_return(a,b),error=ValueError)
        # Installed previous-section helper: supplemental integration parity,not a new independent oracle.
        linked=BOOK/'chapter-19/19.01-financial-data-sources-and-formats.md';linkedtext=linked.read_text();lp=temp/'basics.py';lp.write_text(re.search(r'~~~python\n(.*?)\n~~~',linkedtext,re.S).group(1));lspec=importlib.util.spec_from_file_location('basics',lp);lm=importlib.util.module_from_spec(lspec);lspec.loader.exec_module(lm)
        check('linked return contract',lambda:m.simple_return(Decimal(1),Decimal('1.000000000000000000000000000001')),lm.simple_return(Decimal(1),Decimal('1.000000000000000000000000000001')))
        artifacts={'synthetic.csv':raw,'synthetic-bom.csv':bom,'synthetic-crlf.csv':crlf,'writer-output.csv':output}
        for name,data in artifacts.items():(Path(__file__).parent/name).write_bytes(data)
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),linked_source_sha256=hashlib.sha256(linked.read_bytes()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=rows,existing_unique_methods=10,new_historical_methods=0,artifacts={name:hashlib.sha256(data).hexdigest() for name,data in artifacts.items()},limits='Synthetic CSV byte/schema and source read/write checks; no streaming,point-in-time,source accuracy,spreadsheet export safety,platform or independent acceptance')
        (Path(__file__).parent/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in rows);print(len(rows),'predicates;5 source commands;10 existing methods passed')
if __name__=='__main__':run()
