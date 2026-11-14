"""Final answer lab:exact earlier source fences plus separately labelled stdlib arithmetic."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,csv,io,hashlib,platform
from decimal import Decimal
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
specs=[('csv','19.02-csv-and-text-data.md','def parse_csv'),('schema','19.07-schema-and-data-types.md','def parse_record'),('units','19.10-currency-and-unit-normalization.md','def percent_to_decimal'),('quality','19.11-data-quality-checks.md','def check_batch'),('time','19.09-date-and-timestamp-normalization.md','def normalize_utc'),('asof','19.13-avoiding-look-ahead-and-data-leakage.md','def select_as_of'),('project','19.14-chapter-project-financial-data-pipeline.md','def run_pipeline'),('snippet','19.15-exercises-and-applied-problems.md','simple return:')]
source=[];supplement=[];commands=[];manifest=[]
def check(name,call,expected,group=source):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    group.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as temp:
    temp=Path(temp);mods={}
    for name,file,needle in specs:
        path=ROOT/'chapter-19'/file;text=path.read_text();code=next(x for x in re.findall(r'~~~python\n(.*?)\n~~~',text,re.S) if needle in x);p=temp/('ref_'+name+'.py');p.write_text(code);raw=path.read_bytes();manifest.append(dict(path=str(path.relative_to(ROOT.parents[1])),sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest(),extracted_sha256=hashlib.sha256(code.encode()).hexdigest()))
        if name!='snippet':
            spec=importlib.util.spec_from_file_location('ref_'+name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);mods[name]=m
    for label,argv in [('exact final snippet',[sys.executable,str(temp/'ref_snippet.py')]),('compile eight source fences',[sys.executable,'-m','compileall','-q',str(temp)]),('exact project reference tests',[sys.executable,str(temp/'ref_project.py')]),('quiet seven-module import',[sys.executable,'-c','import ref_csv,ref_schema,ref_units,ref_quality,ref_time,ref_asof,ref_project'])]:
        z=subprocess.run(argv,cwd=temp,text=True,capture_output=True);commands.append(dict(label=label,argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n');writer.writerow(['instrument','date','close','currency']);writer.writerows([['EXAMPLE','2026-01-05','100.00','USD'],['EXAMPLE','2026-01-06','101.50','USD']]);raw=stream.getvalue().encode();parsed=mods['csv'].parse_csv(raw)
    check('lab CSV two rows',lambda:len(parsed),2)
    check('lab source CSV return',lambda:mods['csv'].simple_return(parsed[0]['close'],parsed[1]['close']),Decimal('.015'))
    check('CSV raw identity',lambda:mods['csv'].raw_sha256(raw),hashlib.sha256(raw).hexdigest())
    check('BOM logical equivalence',lambda:mods['csv'].parse_csv(b'\xef\xbb\xbf'+raw),parsed)
    check('missing close rejection',lambda:mods['csv'].parse_csv(raw.replace(b'101.50',b'')),'ValueError')
    duplicate=raw+raw.splitlines(keepends=True)[1];check('duplicate instrument/date rejection',lambda:mods['csv'].parse_csv(duplicate),'ValueError')
    row=dict(instrument='EXAMPLE',observation_date='2026-01-05',close='123456.78',currency='USD',price_type='unadjusted_close')
    check('P18 width accepted',lambda:mods['schema'].parse_record(row)['close'],Decimal('123456.78'))
    for value in ['1234567.00','1.234']:check('P18 width/scale rejection '+value,lambda v=value:mods['schema'].parse_record({**row,'close':v}),'ValueError')
    check('P32 UTC conversion',lambda:mods['time'].normalize_utc('2026-01-05T09:30:00-05:00').isoformat(),'2026-01-05T14:30:00+00:00')
    check('P35 percent',lambda:mods['units'].percent_to_decimal('5'),Decimal('.05'))
    check('P35 bp',lambda:mods['units'].basis_points_to_decimal('100'),Decimal('.01'))
    check('P37 cents',lambda:mods['units'].cents_to_dollars('10000'),Decimal('100'))
    check('P38 FX',lambda:mods['units'].convert_target_per_source('100','1.10'),Decimal('110'))
    check('P39 FX PnL',lambda:mods['units'].convert_target_per_source('100','1.05')-mods['units'].convert_target_per_source('100','1.10'),Decimal('-5'))
    check('P40 rounding',lambda:mods['units'].round_usd_cents('1.005'),Decimal('1.00'))
    base=dict(instrument='EXAMPLE',date='2026-01-05',close='100',currency='USD');four=[base,{**base,'date':'2026-01-06','close':''},{**base,'date':'2026-01-07'},{**base,'date':'2026-01-08'}]
    check('P26 missing denominator',lambda:mods['quality'].check_batch(four)['missing_close_rate'],.25)
    check('P27 empty rate',lambda:mods['quality'].check_batch([])['missing_close_rate'],None)
    check('P29 sparse valid not source completeness',lambda:mods['quality'].check_batch([base,{**base,'date':'2026-02-01'}])['complete'],True)
    check('P34 ingestion delay',lambda:mods['asof'].select_as_of(mods['asof'].example_rows(),'EXAMPLE','2026-03-31','2026-05-01T12:00:30Z'),None)
    check('P45 before publication',lambda:mods['asof'].select_as_of(mods['asof'].example_rows(),'EXAMPLE','2026-03-31','2026-04-15T00:00:00Z'),None)
    check('P46 original revision',lambda:mods['asof'].select_as_of(mods['asof'].example_rows(),'EXAMPLE','2026-03-31','2026-05-05T00:00:00Z')['value'],Decimal('100'))
    project_raw=mods['project'].example();encoded,meta=mods['project'].run_pipeline(project_raw,'2026-01-07T12:00:00Z');enc2,meta2=mods['project'].run_pipeline(project_raw+b' ','2026-01-07T12:00:00Z')
    check('P50 project return',lambda:json.loads(encoded)['simple_return'],'0.015')
    check('P42 byte identity differs',lambda:meta['input_sha256']!=meta2['input_sha256'],True)
    check('P42 logical output same',lambda:encoded,enc2)
    check('reference snippet output',lambda:commands[0]['stdout'],'simple return: 0.015\n')
    check('P6 stdlib quoted field',lambda:next(csv.reader(['EXAMPLE,"Example, Class A",100'])),['EXAMPLE','Example, Class A','100'],supplement)
    check('P36 relative rate change',lambda:(Decimal('6')-Decimal('5'))/Decimal('5'),Decimal('.2'),supplement)
    check('P50 exact rational benchmark',lambda:Fraction(Decimal('101.50')-Decimal('100'))/Fraction(100),Fraction(3,200),supplement)
    (OUT/'two-closes.csv').write_bytes(raw);(OUT/'project-output.json').write_bytes(encoded)
d=dict(candidate_based_on='2bd9edae71a0f1def7176b33ec516d3a798393af',python=sys.version,platform=platform.platform(),source_fences=manifest,commands=commands,source_predicates=source,supplemental_predicates=supplement,existing_project_methods=12,new_historical_unique_methods=0,limits='Final50 prompt/lab scope;seven imported source modules plus exact snippet/project commands;conceptual/source/platform/independent limits remain')
(OUT/'results.json').write_text(json.dumps(d,indent=2)+'\n');print(len(source),'source predicates;',len(supplement),'supplemental;4 commands/eight compiled fences/12 existing project methods');assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in source+supplement)
