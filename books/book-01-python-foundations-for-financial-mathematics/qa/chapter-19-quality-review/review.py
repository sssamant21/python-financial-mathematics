"""Exact source quality-rule execution and scoped answer evidence."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform,copy
from decimal import Decimal,localcontext,InvalidOperation
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
p=ROOT/'chapter-19/19.11-data-quality-checks.md';text=p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,actual,expected):rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'data_quality_checks.py';path.write_text(code)
    for argv in [[sys.executable,str(path)],[sys.executable,'-m','compileall','-q',str(path)],[sys.executable,'-c','import data_quality_checks']]:
        z=subprocess.run(argv,cwd=tmp,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('quality_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    base=dict(instrument='EXAMPLE',date='2026-01-05',close='100.00',currency='USD')
    for name,row,expected in [('valid',base,None),('non-dict',None,'schema'),('absent close',{},'missing_close'),('null',{**base,'close':None},'missing_close'),('empty',{**base,'close':''},'missing_close'),('extra field',{**base,'venue':'X'},'schema'),('other missing field',{'close':'100'},'schema'),('bool',{**base,'close':True},'type'),('Decimal object',{**base,'close':Decimal('100')},'type'),('blank instrument',{**base,'instrument':' '},'instrument'),('currency',{**base,'currency':'EUR'},'currency'),('bad date',{**base,'date':'2026-02-30'},'date'),('compact date',{**base,'date':'20260105'},'date'),('week date',{**base,'date':'2026-W01-1'},'date'),('NaN',{**base,'close':'NaN'},'close'),('signaling NaN',{**base,'close':'sNaN'},'close'),('Infinity',{**base,'close':'Infinity'},'close'),('zero',{**base,'close':'0'},'close'),('negative',{**base,'close':'-1'},'close'),('malformed',{**base,'close':'abc'},'close'),('marker',{**base,'close':'N/A'},'close'),('missing before schema',{'close':'','extra':1},'missing_close'),('instrument before currency/date/close',{**base,'instrument':' ','currency':'EUR','date':'bad','close':'NaN'},'instrument')]:check(name,m.assess_record(row)[1],expected)
    check('normalized instrument',m.assess_record({**base,'instrument':' EXAMPLE '})[0]['instrument'],'EXAMPLE')
    check('Decimal scale',m.assess_record(base)[0]['close'].as_tuple().exponent,-2)
    four=[base,{**base,'date':'2026-01-06','close':''},{**base,'date':'2026-01-07'},{**base,'date':'2026-01-08'}];saved=copy.deepcopy(four);result=m.check_batch(iter(four))
    check('one missing among four',(result['submitted'],len(result['accepted']),result['rejected'],result['missing_close_rate'],result['complete']),(4,3,1,.25,False))
    check('reason denominator',result['reasons'],{'missing_close':1})
    check('caller preserved',four,saved)
    check('empty batch',m.check_batch([]),dict(submitted=0,accepted=[],rejected=0,reasons={},missing_close_rate=None,complete=False))
    d=m.check_batch([base,{**base,'instrument':' EXAMPLE '}]);check('normalized accepted-key duplicate',(len(d['accepted']),d['reasons']), (1,{'duplicate':1}))
    d=m.check_batch([{**base,'close':'bad'},base]);check('rejected key not reserved',(len(d['accepted']),d['reasons']),(1,{'close':1}))
    d=m.check_batch([base,{**base,'close':''},base]);check('one primary reason per row',(d['rejected'],d['reasons']),(2,{'missing_close':1,'duplicate':1}))
    check('valid sparse batch complete',m.check_batch([base,{**base,'date':'2026-02-01'}])['complete'],True)
    with localcontext() as ctx:
        ctx.traps[InvalidOperation]=False
        check('malformed with caller trap disabled',m.assess_record({**base,'close':'abc'})[1],'close')
    check('no per-row quarantine payload','quarantine' in result,False)
    check('demo two-row rate',m.check_batch([base,{**base,'close':''}])['missing_close_rate'],.5)
d=dict(executable_source_revision='da173ca7e4bffb6ec72bf861f30b242dda78f910',source_sha256=hashlib.sha256(code.encode()).hexdigest(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,predicates=rows,existing_methods=12,new_historical_unique_methods=0,source_changed=False,limits='Submitted decoded rows only;not expected coverage,freshness,source reconciliation,publication or independent acceptance')
(OUT/'results.json').write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;3 source commands/12 existing methods')
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows)
