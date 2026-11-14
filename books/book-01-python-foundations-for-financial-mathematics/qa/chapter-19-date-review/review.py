"""Exact-source date/offset contracts; DST is a separate supplemental implementation."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib.util,json,hashlib,platform
from datetime import date,datetime,timezone
from zoneinfo import ZoneInfo,TZPATH
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
REV=sys.argv[1] if len(sys.argv)>1 else None
p=ROOT/'chapter-19/19.09-date-and-timestamp-normalization.md'
text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(REPO))],cwd=REPO,text=True) if REV else p.read_text()
code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);rows=[];commands=[]
def check(name,call,expected):
    try:actual=call()
    except Exception as exc:actual=type(exc).__name__
    rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'timestamp_normalization.py';path.write_text(code)
    for argv in [[sys.executable,str(path)],[sys.executable,'-m','compileall','-q',str(path)],[sys.executable,'-c','import timestamp_normalization']]:
        z=subprocess.run(argv,cwd=tmp,capture_output=True,text=True);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
    spec=importlib.util.spec_from_file_location('timestamp_reference',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    for textdate,expected in [('2026-01-05',date(2026,1,5)),('2024-02-29',date(2024,2,29)),('2026-02-29','ValueError'),('2026-02-30','ValueError'),('20260105','ValueError'),('2026-W01-1','ValueError'),('2026-1-05','ValueError'),('2026-01-05\n','ValueError'),('２０２６-01-05','ValueError'),(None,'ValueError')]:check('date '+repr(textdate),lambda t=textdate:m.parse_date(t),expected)
    cases=[('2026-01-05T09:30:00-05:00','2026-01-05T14:30:00+00:00'),('2026-01-05T14:30:00Z','2026-01-05T14:30:00+00:00'),('2026-01-01T00:15:00+05:30','2025-12-31T18:45:00+00:00'),('2026-01-01T23:45:00-02:00','2026-01-02T01:45:00+00:00'),('2026-01-05T14:30:00.1Z','2026-01-05T14:30:00.100000+00:00'),('2026-01-05T14:30:00.123456Z','2026-01-05T14:30:00.123456+00:00'),('2026-01-05T14:30:00-00:00','2026-01-05T14:30:00+00:00'),('2026-01-05T23:59:00+23:59','2026-01-05T00:00:00+00:00')]
    for t,expected in cases:check('normalize '+t,lambda t=t:m.normalize_utc(t).isoformat(),expected)
    bad=['2026-01-05T09:30:00','2026-01-05 09:30:00Z','2026-01-05T09:30Z','2026-01-05T09:30:00.1234567Z','2026-01-05T09:30:60Z','2026-01-05T24:00:00Z','2026-01-05T09:30:00+25:00','2026-01-05T09:30:00+01:60','2026-01-05T09:30:00-01:60','2026-01-05T09:30:00+00:99','0001-01-01T00:00:00+00:01','9999-12-31T23:59:59-00:01','2026-01-05T09:30:00America/New_York','2026-01-05T09:30:00Z\n',None]
    for t in bad:check('reject '+repr(t),lambda t=t:m.normalize_utc(t),'ValueError')
    for name,a,d,expected in [('before','2026-01-05T14:30:00Z','2026-01-05T15:00:00Z',True),('after','2026-01-05T15:00:00Z','2026-01-05T14:30:00Z',False),('equal offsets','2026-01-05T14:30:00Z','2026-01-05T09:30:00-05:00',True),('microsecond order','2026-01-05T14:30:00.000001Z','2026-01-05T14:30:00Z',False),('invalid availability','bad','2026-01-05T15:00:00Z','ValueError')]:check(name,lambda a=a,d=d:m.available_by(a,d),expected)
# Lab9 supplemental zoneinfo roundtrip; no named-zone source API is claimed.
z=ZoneInfo('America/New_York');dst=[]
for fold,utc in [(0,'2026-11-01T05:30:00+00:00'),(1,'2026-11-01T06:30:00+00:00')]:
    value=datetime(2026,11,1,1,30,tzinfo=z,fold=fold).astimezone(timezone.utc).isoformat();dst.append(dict(name='autumn fold '+str(fold),actual=value,expected=utc,passed=value==utc))
for fold in (0,1):
    wall=datetime(2026,3,8,2,30,tzinfo=z,fold=fold);back=wall.astimezone(timezone.utc).astimezone(z);valid=back.replace(tzinfo=None)==wall.replace(tzinfo=None);dst.append(dict(name='spring roundtrip fold '+str(fold),actual=valid,expected=False,passed=valid is False))
zonefiles=[]
for base in TZPATH:
    f=Path(base)/'America/New_York'
    if f.exists():zonefiles.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
d=dict(selected_revision=REV,candidate_based_on='926330850a54eb97363c131b2d0188e7d7ee0bfa',manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,predicates=rows,supplemental_dst=dict(predicates=dst,zonefiles=zonefiles,limits='Supplemental zoneinfo implementation;not reference-source named-zone or supported-platform acceptance'),existing_methods=12,new_historical_unique_methods=0)
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source-call predicates;',sum(not x['passed'] for x in rows),'failed;4 separate supplemental DST predicates')
assert all(x['returncode']==0 for x in commands) and all(x['passed'] for x in rows+dst)
