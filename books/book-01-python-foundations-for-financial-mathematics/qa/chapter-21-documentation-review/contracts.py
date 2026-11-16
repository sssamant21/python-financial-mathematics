"""Manual expected metadata bytes,external digest control and separate PV run."""
from pathlib import Path
import json,sys,hashlib,subprocess,math,platform
from fractions import Fraction
import run_metadata as m
import time_value as tv
rows=[];external=[]
def add(case,actual,expected,kind='contract'):
 rows.append(dict(case=case,actual=repr(actual),expected=repr(expected),kind=kind,passed=actual==expected))
def rec(**changes):
 d=dict(revision='abc123',python='3.x',command='python -m unittest',status='not_run');d.update(changes);return d
fixtures=[(rec(),b'{"command":"python -m unittest","python":"3.x","revision":"abc123","status":"not_run"}'),(rec(status='passed'),b'{"command":"python -m unittest","python":"3.x","revision":"abc123","status":"passed"}'),(rec(status='failed'),b'{"command":"python -m unittest","python":"3.x","revision":"abc123","status":"failed"}'),(rec(status='blocked'),b'{"command":"python -m unittest","python":"3.x","revision":"abc123","status":"blocked"}'),(rec(revision='é😀'),b'{"command":"python -m unittest","python":"3.x","revision":"\\u00e9\\ud83d\\ude00","status":"not_run"}'),(rec(command='a"b\\c\nd'),b'{"command":"a\\"b\\\\c\\nd","python":"3.x","revision":"abc123","status":"not_run"}')]
for i,(record,want) in enumerate(fixtures):
 actual=m.metadata_bytes(record);add(f'manual expected bytes{i}',actual,want,'manual serialization reference')
 z=subprocess.run(['sha256sum'],input=want,capture_output=True,check=True);digest=z.stdout.decode().split()[0];external.append(dict(argv=['sha256sum'],input_hex=want.hex(),stdout=z.stdout.decode(),stderr=z.stderr.decode(),returncode=z.returncode));add(f'external expected-byte digest{i}',m.metadata_sha256(record),digest,'separate executable digest comparison,not cryptographic implementation review')
for name,record in [('None',None),('list',list(rec().items())),('extra',rec(extra='x')),('wrong status',rec(status='approved')),('bool status',rec(status=True)),('integer revision',rec(revision=123)),('float revision',rec(revision=1.)),('null command',rec(command=None)),('empty python',rec(python='')),('blank command',rec(command='  ')),('leading space',rec(revision=' abc')),('trailing newline',rec(revision='abc\n'))]:
 try:m.metadata_bytes(record);actual='returned'
 except Exception as e:actual=type(e).__name__
 add(name,actual,'ValueError')
for key in ('revision','python','command','status'):
 d=rec();del d[key]
 try:m.metadata_bytes(d);actual='returned'
 except Exception as e:actual=type(e).__name__
 add('missing '+key,actual,'ValueError')
class Subdict(dict):pass
try:m.metadata_bytes(Subdict(rec()));actual='returned'
except Exception as e:actual=type(e).__name__
add('dict subclass',actual,'ValueError');a=rec();copy=a.copy();b=dict(reversed(list(a.items())));add('insertion order',m.metadata_bytes(a),m.metadata_bytes(b));add('ownership',a,copy);add('status claim not authenticated',b'"status":"passed"' in m.metadata_bytes(rec(status='passed')),True);add('changed selected record changes digest',m.metadata_sha256(a)!=m.metadata_sha256(rec(revision='def456')),True)
actual=tv.present_value(110.,.1,1);expected=Fraction(110)/(1+Fraction(1,10));add('separate source PV benchmark',math.isclose(actual,float(expected),rel_tol=0.,abs_tol=1e-10),True,'separate financial source execution,not metadata integration')
calculation=dict(source_revision=sys.argv[2],module_fence_sha256=hashlib.sha256(Path(tv.__file__).read_bytes()).hexdigest(),source_mode='exact staged manuscript implementation;no installed wheel or metadata integration',inputs=dict(amount=110.0,effective_rate_per_period=.1,periods=1),units='synthetic amount',independent_expected='110/(11/10)=100',actual_output=actual,actual_float_hex=actual.hex(),relative_tolerance=0.,absolute_tolerance=1e-10,python=sys.version,platform=platform.platform(),owner='Educational synthetic record;independent owner/reviewer unassigned',approval='Not granted',excluded='default/fees/taxes/real input data/operational use')
summary=dict(revision=sys.argv[2],python=platform.python_version(),command='source PV110at10pct1period probe',status='passed');calculation['restricted_summary']=summary;calculation['restricted_summary_sha256']=m.metadata_sha256(summary);calculation['digest_scope']='Only four summary strings,not full calculation/source/artifact/data evidence.'
d=dict(predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),external_digest_runs=external,actual_calculation_record=calculation,limits='Manual expected byte fixtures plus external sha256sum executable. No universal canonical JSON,independent cryptographic implementation/security/provenance/authentication review. A syntactic passed claim is not proof;separate PV execution not metadata-helper integration.')
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
