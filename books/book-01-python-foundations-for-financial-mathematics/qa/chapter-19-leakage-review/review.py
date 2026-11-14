"""Exact as-of source and synthetic revision-selection boundaries."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform,copy
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=ROOT/'chapter-19/19.13-avoiding-look-ahead-and-data-leakage.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(REPO))],cwd=REPO,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,call,expected):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'point_in_time.py';path.write_text(code)
    for argv in [[sys.executable,str(path)],[sys.executable,'-m','compileall','-q',str(path)],[sys.executable,'-c','import point_in_time']]:
        z=subprocess.run(argv,cwd=tmp,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('asof_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    fixture=m.example_rows();saved=copy.deepcopy(fixture)
    def selected(data,decision,inst='EXAMPLE',effective='2026-03-31'):
        row=m.select_as_of(data,inst,effective,decision);return None if row is None else row['value']
    for decision,expected in [('2026-04-15T00:00:00Z',None),('2026-05-05T00:00:00Z',Decimal('100')),('2026-05-12T00:00:00Z',Decimal('105')),('2026-05-01T12:00:30Z',None),('2026-05-01T12:01:00Z',Decimal('100')),('2026-05-10T12:00:59.999999Z',Decimal('100')),('2026-05-10T12:01:00Z',Decimal('105'))]:check('cutoff '+decision,lambda d=decision:selected(fixture,d),expected)
    check('caller rows unchanged',lambda:fixture,saved)
    check('generator selection',lambda:selected(iter(fixture),'2026-05-12T00:00:00Z'),Decimal('105'))
    check('reversed input ordering',lambda:selected(list(reversed(fixture)),'2026-05-12T00:00:00Z'),Decimal('105'))
    check('empty input',lambda:selected([],'2026-05-12T00:00:00Z'),None)
    check('normalized query instrument',lambda:selected(fixture,'2026-05-12T00:00:00Z',' EXAMPLE '),Decimal('105'))
    check('other instrument',lambda:selected(fixture,'2026-05-12T00:00:00Z','OTHER'),None)
    check('other period',lambda:selected(fixture,'2026-05-12T00:00:00Z',effective='2026-03-30'),None)
    check('latest eligible tie',lambda:selected(fixture+[dict(fixture[1])],'2026-05-12T00:00:00Z'),'ValueError')
    check('older tie ignored when later winner exists',lambda:selected([fixture[0],dict(fixture[0]),fixture[1]],'2026-05-12T00:00:00Z'),Decimal('105'))
    d=copy.deepcopy(fixture);d[1]['ingested_at']='2026-05-20T00:00:00Z';check('latest published but not ingested',lambda:selected(d,'2026-05-12T00:00:00Z'),Decimal('100'))
    check('invalid irrelevant row rejects',lambda:selected(fixture+[{'instrument':'OTHER'}],'2026-05-12T00:00:00Z'),'ValueError')
    for field,value in [('value','NaN'),('value','Infinity'),('effective_date','20260331'),('published_at','2026-05-01T12:00:00'),('ingested_at',None)]:check('record invalid '+field+repr(value),lambda field=field,value=value:m.parse_record({**fixture[0],field:value}),'ValueError')
    for value in ['0','-100']:check('finite generic value '+value,lambda v=value:m.parse_record({**fixture[0],'value':v})['value'],Decimal(value))
    for name,inst,effective,decision in [('blank instrument',' ','2026-03-31','2026-05-12T00:00:00Z'),('compact query date','EXAMPLE','20260331','2026-05-12T00:00:00Z'),('naive decision','EXAMPLE','2026-03-31','2026-05-12T00:00:00')]:check(name,lambda i=inst,e=effective,d=decision:selected(fixture,d,i,e),'ValueError')
    check('offset equivalence',lambda:m.instant('2026-05-01T08:00:00-04:00')==m.instant('2026-05-01T12:00:00Z'),True)
    check('fractional precision',lambda:m.instant('2026-05-01T12:00:00.123456Z').microsecond,123456)
    for bad in ['2026-05-01T12:00:00+01:60','2026-05-01T12:00:00-01:60','2026-05-01T12:00:00+00:99','0001-01-01T00:00:00+00:01','9999-12-31T23:59:59-00:01','2026-05-01T12:00:00+25:00','2026-05-01T12:00:00.1234567Z','2026-05-01T12:00:60Z','2026-05-01T12:00:00Z\n']:check('timestamp reject '+repr(bad),lambda bad=bad:m.instant(bad),'ValueError')
    if REV is None:(OUT/'synthetic-revisions.json').write_text(json.dumps(fixture,indent=2)+'\n')
d=dict(selected_revision=REV,candidate_based_on='953fa30f7a29cc4a27a2817238e5b72f25c635ef',source_sha256=hashlib.sha256(code.encode()).hexdigest(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,predicates=rows,existing_methods=12,new_historical_unique_methods=0,limits='Synthetic as-of publication/ingestion policy only;not source truth/history,market calendars,model train/test or independent acceptance')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;3 commands/12 existing methods')
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows)
