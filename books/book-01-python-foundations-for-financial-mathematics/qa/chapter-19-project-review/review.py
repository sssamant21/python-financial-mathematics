"""Exact integrated project execution;source and supplemental fixture identities separate."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform,copy
from decimal import Decimal,localcontext,Inexact
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=ROOT/'chapter-19/19.14-chapter-project-financial-data-pipeline.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(REPO))],cwd=REPO,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,call,expected):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as temp:
    path=Path(temp)/'financial_data_pipeline.py';path.write_text(code)
    for argv in [[sys.executable,str(path)],[sys.executable,'-m','compileall','-q',str(path)],[sys.executable,'-c','import financial_data_pipeline']]:
        z=subprocess.run(argv,cwd=temp,text=True,capture_output=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('project_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    raw=m.example();cutoff='2026-01-07T12:00:00Z';data=json.loads(raw);encoded,manifest=m.run_pipeline(raw,cutoff)
    expected=dict(instrument='EXAMPLE',currency='USD',price_type='unadjusted_close',start_date='2026-01-05',end_date='2026-01-06',simple_return='0.015')
    canonical=json.dumps(expected,sort_keys=True,separators=(',',':')).encode()
    check('independent canonical output',lambda:encoded,canonical)
    check('manifest input identity',lambda:manifest['input_sha256'],hashlib.sha256(raw).hexdigest())
    check('manifest output identity',lambda:manifest['output_sha256'],hashlib.sha256(canonical).hexdigest())
    check('manifest count/schema/context',lambda:(manifest['record_count'],manifest['schema_version'],manifest['decimal_precision'],manifest['rounding']),(2,1,28,'ROUND_HALF_EVEN'))
    check('exact replay',lambda:m.run_pipeline(raw,cutoff),(encoded,manifest))
    other,othermeta=m.run_pipeline(raw+b' ',cutoff)
    check('whitespace input identity differs',lambda:othermeta['input_sha256']!=manifest['input_sha256'],True)
    check('whitespace output stable',lambda:(other,othermeta['output_sha256']),(encoded,manifest['output_sha256']))
    check('equivalent cutoff normalization',lambda:m.run_pipeline(raw,'2026-01-07T07:00:00-05:00'),(encoded,manifest))
    check('early cutoff',lambda:m.run_pipeline(raw,'2026-01-06T21:00:00Z'),'ValueError')
    check('equal cutoff',lambda:m.run_pipeline(raw,'2026-01-06T22:00:00Z')[0],encoded)
    for name,bad in [('wrong bytes','text'),('invalid UTF8',b'\xff'),('invalid JSON',b'['),('not list',b'{}'),('empty',b'[]'),('one row',b'[{}]'),('duplicate JSON key',raw.replace(b'"close":"100.00"',b'"close":"100.00","close":"99"')),('nonstandard constant',raw.replace(b'"101.50"',b'NaN'))]:check(name,lambda v=bad:m.run_pipeline(v,cutoff),'ValueError')
    changes=[('missing',lambda d:d[0].pop('close')),('extra',lambda d:d[0].update(venue='X')),('null',lambda d:d[0].update(close=None)),('bool',lambda d:d[0].update(close=True)),('NaN',lambda d:d[0].update(close='NaN')),('zero',lambda d:d[0].update(close='0')),('currency',lambda d:d[0].update(currency='EUR')),('adjusted type',lambda d:d[0].update(price_type='adjusted_close')),('invalid date',lambda d:d[0].update(observation_date='2026-02-30')),('compact date',lambda d:d[0].update(observation_date='20260105')),('duplicate date',lambda d:d[1].update(observation_date=d[0]['observation_date'])),('reverse dates',lambda d:d.reverse()),('other instrument',lambda d:d[1].update(instrument='OTHER'))]
    for name,change in changes:
        d=copy.deepcopy(data);change(d);check(name,lambda d=d:m.run_pipeline(json.dumps(d).encode(),cutoff),'ValueError')
    for value in ['2026-01-07T12:00:00+01:60','2026-01-07T12:00:00-01:60','2026-01-07T12:00:00+00:99','0001-01-01T00:00:00+00:01','9999-12-31T23:59:59-00:01']:check('timestamp '+value,lambda v=value:m.instant(v),'ValueError')
    d=copy.deepcopy(data);d[0]['close']='1';d[1]['close']='1.000000000000000000000000000001'
    check('near unity complete return',lambda:Decimal(json.loads(m.run_pipeline(json.dumps(d).encode(),cutoff)[0])['simple_return']),Decimal('1e-30'))
    d=copy.deepcopy(data);d[0]['close']='3';d[1]['close']='4'
    with localcontext() as ctx:
        ctx.traps[Inexact]=True
        check('private rounding trap policy',lambda:Decimal(json.loads(m.run_pipeline(json.dumps(d).encode(),cutoff)[0])['simple_return']),Decimal('0.3333333333333333333333333333'))
    d[0]['close']='1';d[1]['close']='1001'
    with localcontext() as ctx:
        ctx.Emax=2
        check('private exponent range',lambda:Decimal(json.loads(m.run_pipeline(json.dumps(d).encode(),cutoff)[0])['simple_return']),Decimal('1000'))
    if REV is None:
        (OUT/'input.json').write_bytes(raw);(OUT/'output.json').write_bytes(encoded);(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
d=dict(selected_revision=REV,candidate_based_on='2bd9edae71a0f1def7176b33ec516d3a798393af',source_sha256=hashlib.sha256(code.encode()).hexdigest(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,predicates=rows,existing_methods=12,new_historical_unique_methods=0,limits='Synthetic two-close strict batch/cutoff/context and byte replay only;not provider truth,revision/sink/resource/platform/independent acceptance')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;3 commands/12 existing methods')
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows)
