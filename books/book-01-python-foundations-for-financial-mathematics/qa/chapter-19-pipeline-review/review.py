"""Exact pipeline source, raw/output fixtures and controlled active-context review."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform,copy
from decimal import Decimal,getcontext,localcontext,ROUND_FLOOR,ROUND_CEILING
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=ROOT/'chapter-19/19.12-reproducible-data-pipelines.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(REPO))],cwd=REPO,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,call,expected):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
def raw_from(data):return json.dumps(data,separators=(',',':')).encode()
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'reproducible_pipeline.py';path.write_text(code)
    for argv in [[sys.executable,str(path)],[sys.executable,'-m','compileall','-q',str(path)],[sys.executable,'-c','import reproducible_pipeline']]:
        z=subprocess.run(argv,cwd=tmp,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('pipeline_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    raw=(OUT/'input.json').read_bytes();output,manifest=m.transform(raw);data=json.loads(raw)
    expected=b'{"currency":"USD","end_date":"2026-01-06","instrument":"EXAMPLE","simple_return":"0.015","start_date":"2026-01-05"}'
    check('independent canonical benchmark',lambda:output,expected)
    check('exact replay',lambda:m.transform(raw),(output,manifest))
    check('input identity',lambda:manifest['input_sha256'],hashlib.sha256(raw).hexdigest())
    check('output identity',lambda:manifest['output_sha256'],hashlib.sha256(expected).hexdigest())
    check('manifest schema/count',lambda:(manifest['schema_version'],manifest['record_count']),(1,2))
    check('manifest Python',lambda:manifest['python_version'],platform.python_version())
    spaced,spaced_manifest=m.transform(raw+b' ')
    check('whitespace changes input identity',lambda:spaced_manifest['input_sha256']!=manifest['input_sha256'],True)
    check('whitespace preserves output',lambda:(spaced,spaced_manifest['output_sha256']),(output,manifest['output_sha256']))
    check('JSON indentation preserves output',lambda:m.transform(json.dumps(data,indent=2).encode())[0],output)
    check('input bytes preserved',lambda:raw,(OUT/'input.json').read_bytes())
    check('no context metadata promised',lambda:'decimal_context' in manifest,False)
    for name,bad in [('wrong bytes type','text'),('invalid UTF8',b'\xff'),('invalid JSON',b'['),('not list',b'{}'),('zero rows',b'[]'),('one row',b'[{}]'),('duplicate JSON key',raw.replace(b'"close":"100.00"',b'"close":"100.00","close":"99"')),('nonstandard constant',raw.replace(b'"101.50"',b'NaN'))]:check(name,lambda bad=bad:m.transform(bad),'ValueError')
    changes=[('missing field',lambda d:d[0].pop('close')),('extra field',lambda d:d[0].update(venue='X')),('wrong type',lambda d:d[0].update(close=True)),('blank instrument',lambda d:d[0].update(instrument=' ')),('currency',lambda d:d[0].update(currency='EUR')),('calendar date',lambda d:d[0].update(date='2026-02-30')),('compact date',lambda d:d[0].update(date='20260105')),('nonfinite',lambda d:d[0].update(close='NaN')),('zero close',lambda d:d[0].update(close='0')),('negative close',lambda d:d[0].update(close='-1')),('different instruments',lambda d:d[1].update(instrument='OTHER')),('equal date',lambda d:d[1].update(date=d[0]['date'])),('reversed dates',lambda d:d.reverse())]
    for name,change in changes:
        d=copy.deepcopy(data);change(d);check(name,lambda d=d:m.transform(raw_from(d)),'ValueError')
    d=copy.deepcopy(data);d[0]['instrument']=' EXAMPLE ';check('instrument normalization',lambda:m.transform(raw_from(d))[0],output)
    d=copy.deepcopy(data);d[0]['close']='1';d[1]['close']='1.000000000000000000000000000001'
    check('near unity complete return',lambda:Decimal(json.loads(m.transform(raw_from(d))[0])['simple_return']),Decimal('1e-30'))
    with localcontext() as ctx:
        ctx.prec=2
        check('controlled precision2 ordinary return',lambda:Decimal(json.loads(m.transform(raw)[0])['simple_return']),Decimal('.015'))
        d=copy.deepcopy(data);d[0]['close']='3';d[1]['close']='4'
        for rounding,expected_value in [(ROUND_FLOOR,Decimal('.33')),(ROUND_CEILING,Decimal('.34'))]:
            ctx.rounding=rounding
            check('controlled active '+rounding,lambda:Decimal(json.loads(m.transform(raw_from(d))[0])['simple_return']),expected_value)
    if REV is None:(OUT/'output.json').write_bytes(output);(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
d=dict(selected_revision=REV,candidate_based_on='5106894e21bb783f3a895eb6df58e0f66bc9aed9',manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),active_decimal_context=str(getcontext()),input_sha256=hashlib.sha256(raw).hexdigest(),commands=commands,predicates=rows,existing_methods=12,new_historical_unique_methods=0,limits='Controlled active context;no source/availability/byte portability/idempotent sink/platform/independent acceptance')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;3 commands/12 existing methods')
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows)
