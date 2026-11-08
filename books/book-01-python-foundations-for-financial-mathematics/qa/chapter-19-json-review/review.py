from pathlib import Path
from decimal import Decimal,localcontext
import re,json,subprocess,tempfile,importlib.util,sys,hashlib,platform
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics';SOURCE=BOOK/'chapter-19/19.03-json-data.md'
def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);obj=json.loads(re.search(r'~~~json\n(.*?)\n~~~',text,re.S).group(1));raw=json.dumps(obj,separators=(',',':')).encode();pretty=json.dumps(obj,indent=2,sort_keys=True).encode();commands=[];rows=[]
    def check(name,call,expected=None,error=None):
        try:value=call();ok=error is None and value==expected;actual=repr(value)
        except Exception as exc:actual=type(exc).__name__+': '+str(exc);ok=type(exc) is error
        rows.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(expected)))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'financial_json_data.py';p.write_text(code)
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import financial_json_data']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        spec=importlib.util.spec_from_file_location('json_data',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        check('close exact',lambda:m.parse_record(raw)['close'],Decimal('101.50'));check('semantic key/whitespace equivalence',lambda:m.parse_record(raw)==m.parse_record(pretty),True);check('raw hash',lambda:m.raw_sha256(raw),hashlib.sha256(raw).hexdigest());check('format hash differs',lambda:m.raw_sha256(raw)!=m.raw_sha256(pretty),True)
        for name,bad in [('nonbytes',None),('bad encoding',b'\xff'),('BOM not supported',b'\xef\xbb\xbf'+raw),('syntax',raw[:-1]),('array',b'[]'),('null top',b'null'),('numeric top',b'1'),('duplicate',raw.replace(b'"101.50"',b'"101.50","close":"99"')),('nested duplicate',raw[:-1]+b',"extra":{"x":1,"x":2}}'),('NaN literal',raw.replace(b'"101.50"',b'NaN')),('Infinity literal',raw.replace(b'"101.50"',b'Infinity'))]:check(name,lambda:m.parse_record(bad),error=ValueError)
        for key,value,label in [('close',None,'null close'),('close',0,'zero numeric'),('close',101.50,'float close'),('close',True,'bool close'),('close','','empty close'),('close','NA','NA close'),('close','NaN','NaN string'),('close','Infinity','inf string'),('close','0','zero string'),('close','-1','negative close'),('instrument','','empty instrument'),('currency','EUR','EUR'),('price_type','adjusted_close','adjusted'),('observation_date','not-date','bad date')]:
            bad=dict(obj);bad[key]=value;payload=json.dumps(bad).encode();check(label,lambda:m.parse_record(payload),error=ValueError)
        bad=dict(obj);del bad['close'];check('missing close',lambda:m.parse_record(json.dumps(bad).encode()),error=ValueError)
        bad=dict(obj);bad['new_field']='x';check('extra field',lambda:m.parse_record(json.dumps(bad).encode()),error=ValueError)
        check('raw hash wrong type',lambda:m.raw_sha256('x'),error=ValueError)
        for a,b,expected in [('100','101.50','.015'),('1','1.000000000000000000000000000001','1e-30'),('2','0','-1')]:check('return '+repr((a,b)),lambda:m.simple_return(Decimal(a),Decimal(b)),Decimal(expected))
        with localcontext() as ctx:
            ctx.prec=2;check('private return context',lambda:m.simple_return(Decimal('100'),Decimal('101.50')),Decimal('.015'))
        for a,b in [(Decimal(0),Decimal(1)),(True,Decimal(1)),(Decimal(1),Decimal(-1))]:check('bad return '+repr((a,b)),lambda:m.simple_return(a,b),error=ValueError)
        for name,data in [('synthetic-compact.json',raw),('synthetic-pretty.json',pretty)]:(Path(__file__).parent/name).write_bytes(data)
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=rows,existing_unique_methods=10,new_historical_methods=0,scope='Strict synthetic record/schema and return arithmetic;no live API,pagination,resource cap,authenticity,point-in-time,platform or independent acceptance')
        (Path(__file__).parent/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in rows);print(len(rows),'predicates;3 source commands;10 existing methods passed')
if __name__=='__main__':run()
