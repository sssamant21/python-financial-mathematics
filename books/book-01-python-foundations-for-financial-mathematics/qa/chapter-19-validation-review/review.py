from pathlib import Path
from datetime import date
from decimal import Decimal,localcontext
import re,json,copy,hashlib,tempfile,subprocess,sys,importlib.util,platform
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics';SOURCE=BOOK/'chapter-19/19.06-parsing-and-validation.md';OUT=Path(__file__).parent

def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);commands=[];checks=[]
    def check(name,call,ref=None,error=None):
        try:value=call();ok=error is None and value==ref;actual=repr(value)
        except Exception as exc:actual=type(exc).__name__+': '+str(exc);ok=type(exc) is error
        checks.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(ref)))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'parsing_validation.py';p.write_text(code)
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import parsing_validation']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        spec=importlib.util.spec_from_file_location('validation',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        row={'instrument':'EXAMPLE','date':'2026-01-05','close':'100.00','currency':'USD'};later=dict(row,date='2026-01-06',close='101.50')
        check('valid close',lambda:m.parse_record(row)['close'],Decimal('100.00'));check('canonical date',lambda:m.parse_record(row)['date'],date(2026,1,5))
        for key,value,reason in [('close',None,'type'),('close',True,'type'),('close','','close'),('close','NaN','close'),('close','Infinity','close'),('close','0','close'),('close','-1','close'),('currency','EUR','currency'),('instrument','  ','instrument'),('date','20260105','date'),('date','2026-W02-1','date'),('date','2026-01-05T00:00:00','date')]:
            bad=dict(row);bad[key]=value
            def observed():
                try:m.parse_record(bad)
                except ValueError as exc:return str(exc)
            check('reason '+repr((key,value)),observed,reason)
        for bad in [None,{'instrument':'X'},dict(row,extra='x')]:
            def observed():
                try:m.parse_record(bad)
                except ValueError as exc:return str(exc)
            check('schema '+repr(bad),observed,'schema')
        mixed=[row,dict(row,close='NaN'),dict(row,instrument=' EXAMPLE '),later,dict(later,currency='EUR')];result=m.validate_batch(iter(mixed))
        check('accepted count',lambda:len(result['accepted']),2);check('rejected reasons/index',lambda:result['rejected'],[{'record_number':2,'reason':'close'},{'record_number':3,'reason':'duplicate'},{'record_number':5,'reason':'currency'}]);check('mixed incomplete',lambda:result['complete'],False);check('accepted order',lambda:[x['date'] for x in result['accepted']],[date(2026,1,5),date(2026,1,6)])
        check('empty complete policy',lambda:m.validate_batch([]),{'accepted':[],'rejected':[],'complete':True});check('unsorted accepted',lambda:len(m.validate_batch([later,row])['accepted']),2)
        check('invalid first does not reserve key',lambda:len(m.validate_batch([dict(row,close='NaN'),row])['accepted']),1);check('reason has no raw record',lambda:set(result['rejected'][0]),{'record_number','reason'})
        before=copy.deepcopy(mixed);m.validate_batch(mixed);check('caller input unchanged',lambda:mixed,before)
        for a,b,ref in [('100','101.50','.015'),('1','1.000000000000000000000000000001','1e-30'),('2','0','-1')]:check('return '+repr((a,b)),lambda:m.simple_return(Decimal(a),Decimal(b)),Decimal(ref))
        with localcontext() as ctx:
            ctx.prec=2;check('private return context',lambda:m.simple_return(Decimal(100),Decimal('101.50')),Decimal('.015'))
        for a,b in [(Decimal(0),Decimal(1)),(True,Decimal(1)),(Decimal(1),Decimal(-1))]:check('bad return '+repr((a,b)),lambda:m.simple_return(a,b),error=ValueError)
        fixture=json.dumps(mixed,indent=2)+'\n';(OUT/'synthetic-batch.json').write_text(fixture)
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),fixture_sha256=hashlib.sha256(fixture.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=checks,existing_unique_methods=12,new_historical_methods=0,scope='Already-decoded synthetic rows/quarantine andreturn arithmetic;not syntax decoder,publication gate,source quality,point-in-time,resource/platform/independent acceptance')
        (OUT/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in checks);print(len(checks),'predicates;3 source commands;12 existing methods passed')
if __name__=='__main__':run()
