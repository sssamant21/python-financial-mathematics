from pathlib import Path
from decimal import Decimal,localcontext
import re,json,subprocess,tempfile,importlib.util,sys,hashlib,platform,copy
ROOT=Path(__file__).resolve().parents[4];BOOK=ROOT/'books/book-01-python-foundations-for-financial-mathematics';SOURCE=BOOK/'chapter-19/19.05-apis-and-financial-data.md';OUT=Path(__file__).parent

def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None;text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);page=json.loads(re.search(r'~~~json\n(.*?)\n~~~',text,re.S).group(1));commands=[];rows=[];traces=[]
    def check(name,call,expected=None,error=None):
        try:value=call();ok=error is None and value==expected;actual=repr(value)
        except Exception as exc:actual=type(exc).__name__+': '+str(exc);ok=type(exc) is error
        rows.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(expected)))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'financial_api_basics.py';p.write_text(code);spec=importlib.util.spec_from_file_location('api_basics',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import financial_api_basics']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        calls=[]
        def fetch(cursor):calls.append(cursor);return m.mock_fetch(cursor)
        result=m.collect_pages(fetch,max_pages=2);check('records',lambda:len(result),2);check('fetch order',lambda:calls,[None,'p2']);traces.append(dict(case='complete',calls=calls.copy()))
        check('fixture page count',lambda:len(m.parse_page(page)[0]),2);check('return benchmark',lambda:m.simple_return(result[0]['close'],result[1]['close']),Decimal('.015'))
        check('empty complete',lambda:m.collect_pages(lambda _:{'records':[],'next_cursor':None}),[])
        for cap in [0,True,1.0]:
            calls=[]
            def fetch(cursor):calls.append(cursor);return page
            check('bad cap '+repr(cap),lambda:m.collect_pages(fetch,max_pages=cap),error=ValueError);check('bad cap no calls '+repr(cap),lambda:calls,[])
        calls=[]
        def fetch(cursor):calls.append(cursor);return m.mock_fetch(cursor)
        check('page bound incomplete',lambda:m.collect_pages(fetch,max_pages=1),error=RuntimeError);check('page bound trace',lambda:calls,[None]);traces.append(dict(case='page-bound',calls=calls.copy()))
        calls=[]
        def cyclic(cursor):calls.append(cursor);return {'records':[],'next_cursor':{None:'a','a':'b','b':'a'}[cursor]}
        check('cycle',lambda:m.collect_pages(cyclic),error=ValueError);check('cycle trace',lambda:calls,[None,'a','b']);traces.append(dict(case='cycle',calls=calls.copy()))
        calls=[]
        def failing(cursor):
            calls.append(cursor)
            if cursor is not None:raise RuntimeError('page unavailable')
            return m.mock_fetch(cursor)
        check('page failure not partial return',lambda:m.collect_pages(failing),error=RuntimeError);check('failure trace',lambda:calls,[None,'p2']);traces.append(dict(case='page-failure',calls=calls.copy()))
        row=page['records'][0]
        def duplicate(cursor):return {'records':[dict(row,instrument=' EXAMPLE ')],'next_cursor':'p2'} if cursor is None else {'records':[row],'next_cursor':None}
        check('cross-page normalized duplicate',lambda:m.collect_pages(duplicate),error=ValueError)
        def opaque(cursor):return {'records':[],'next_cursor':' '} if cursor is None else {'records':[row],'next_cursor':None}
        check('opaque whitespace cursor',lambda:len(m.collect_pages(opaque)),1)
        reversed_page={'records':list(reversed(page['records'])),'next_cursor':None};check('provider order retained',lambda:[r['close'] for r in m.collect_pages(lambda _:reversed_page)],[Decimal('101.50'),Decimal('100.00')])
        for name,bad in [('not object',None),('missing cursor',{'records':[]}),('extra page field',dict(page,extra=True)),('records not list',{'records':(),'next_cursor':None})]:check(name,lambda:m.parse_page(bad),error=ValueError)
        for cursor in ['',True,123,[]]:check('bad cursor '+repr(cursor),lambda:m.parse_page({'records':[],'next_cursor':cursor}),error=ValueError)
        for key,value in [('close',None),('close',101.5),('close',True),('close','NaN'),('close','Infinity'),('close','0'),('close','-1'),('currency','EUR'),('instrument',''),('date','bad')]:
            bad=copy.deepcopy(page);bad['records'][0][key]=value;check('bad record '+repr((key,value)),lambda:m.parse_page(bad),error=ValueError)
        bad=copy.deepcopy(page);bad['records'][0]['extra']='x';check('record extra',lambda:m.parse_page(bad),error=ValueError)
        for a,b,ref in [('1','1.000000000000000000000000000001','1e-30'),('2','0','-1')]:check('complete return '+repr((a,b)),lambda:m.simple_return(Decimal(a),Decimal(b)),Decimal(ref))
        with localcontext() as ctx:
            ctx.prec=2;check('private return context',lambda:m.simple_return(Decimal(100),Decimal('101.50')),Decimal('.015'))
        for a,b in [(Decimal(0),Decimal(1)),(True,Decimal(1)),(Decimal(1),Decimal(-1))]:check('bad return '+repr((a,b)),lambda:m.simple_return(a,b),error=ValueError)
        (OUT/'synthetic-page.json').write_text(json.dumps(page,indent=2)+'\n')
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=rows,fetch_traces=traces,existing_unique_methods=10,new_historical_methods=0,scope='Injected synthetic decoded pages only;no live HTTP,authentication,timeouts,retries,provider completeness,licensing,source authenticity,point-in-time,platform or independent acceptance')
        (OUT/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in rows);print(len(rows),'predicates;3 source commands;10 existing methods passed')
if __name__=='__main__':run()
