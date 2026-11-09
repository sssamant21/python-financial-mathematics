from pathlib import Path
from decimal import Decimal,localcontext
from datetime import date
import re,json,copy,hashlib,tempfile,subprocess,sys,importlib.util,platform
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics';SOURCE=BOOK/'chapter-19/19.07-schema-and-data-types.md';OUT=Path(__file__).parent

def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);commands=[];checks=[]
    def check(name,call,reference=None,error=None):
        try:value=call();ok=error is None and value==reference;actual=repr(value)
        except Exception as exc:actual=type(exc).__name__+': '+str(exc);ok=type(exc) is error
        checks.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(reference)))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'schema_data_types.py';p.write_text(code)
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import schema_data_types']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        spec=importlib.util.spec_from_file_location('schema',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        row={'instrument':'EXAMPLE','observation_date':'2026-01-05','close':'100.00','currency':'USD','price_type':'unadjusted_close'};later=dict(row,observation_date='2026-01-06',close='101.50')
        for value in ['123456.78','999999.99','000001.20','000000.01','1','1.2','1.20']:
            check('accepted price '+value,lambda:m.parse_record(dict(row,close=value))['close'],Decimal(value))
        check('scale preserved',lambda:m.parse_record(dict(row,close='1.20'))['close'].as_tuple().exponent,-2)
        rejected=[('1234567.00','precision_or_scale'),('1000000.00','precision_or_scale'),('0000001.2','precision_or_scale'),('1.234','precision_or_scale'),('1e2','precision_or_scale'),('+1','precision_or_scale'),('-1','precision_or_scale'),('.5','precision_or_scale'),('1.','precision_or_scale'),('1.2\n','precision_or_scale'),('１２','precision_or_scale'),('NaN','precision_or_scale'),('0.00','close')]
        def reason(item):
            try:m.parse_record(item)
            except ValueError as exc:return str(exc)
        for value,expected in rejected:check('rejected price '+repr(value),lambda:reason(dict(row,close=value)),expected)
        for key,value,expected in [('close',True,'type'),('close',None,'type'),('currency','EUR','semantics'),('price_type','adjusted_close','semantics'),('instrument',' ','instrument'),('observation_date','20260105','date'),('observation_date','2026-W02-1','date')]:check('field '+repr((key,value)),lambda:reason(dict(row,**{key:value})),expected)
        check('extra field',lambda:reason(dict(row,venue='X')),'schema');check('missing fields',lambda:reason({'instrument':'X'}),'schema')
        check('two rows',lambda:len(m.validate_unique(iter([row,later]))),2);check('normalized duplicate',lambda:m.validate_unique([row,dict(row,instrument=' EXAMPLE ')]),error=ValueError);check('empty policy',lambda:m.validate_unique([]),[]);check('order retained',lambda:[r['observation_date'] for r in m.validate_unique([later,row])],[date(2026,1,6),date(2026,1,5)])
        original=copy.deepcopy(row);m.parse_record(row);check('caller unchanged',lambda:row,original)
        for a,b,reference in [('100','101.50','.015'),('1','1.000000000000000000000000000001','1e-30'),('2','0','-1')]:check('return '+repr((a,b)),lambda:m.simple_return(Decimal(a),Decimal(b)),Decimal(reference))
        with localcontext() as ctx:
            ctx.prec=2;check('private return context',lambda:m.simple_return(Decimal(100),Decimal('101.50')),Decimal('.015'));check('parser text exact under low context',lambda:m.parse_record(dict(row,close='123456.78'))['close'],Decimal('123456.78'))
        fixture=json.dumps([row,later],indent=2)+'\n';(OUT/'synthetic-records.json').write_text(fixture)
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),fixture_sha256=hashlib.sha256(fixture.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=checks,existing_unique_methods=12,new_historical_methods=0,scope='Decoded strict price-text/schema/key andstandalone return checks;not syntax decoder,source/financial/point-in-time/resource/platform/independent acceptance')
        (OUT/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in checks);print(len(checks),'predicates;3source commands;12existing methods passed')
if __name__=='__main__':run()
