"""Exact synthetic input bytes,source manifests and local process replay."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,math,platform
from fractions import Fraction
from decimal import Decimal
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.13-reproducibility.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[];byte_oracles=[];supp=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=math.isclose(a,want,rel_tol=0,abs_tol=tol) if tol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'reproducible_npv.py';src.write_text(code)
 replay='import json;from reproducible_npv import run;print(json.dumps(run([-100.0,110.0],.1,"synthetic-replay"),sort_keys=True,separators=(",",":")))'
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','reproducible_npv']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import reproducible_npv']),('optimized suite',[sys.executable,'-O',src.name]),('replay process1',[sys.executable,'-c',replay]),('replay process2',[sys.executable,'-c',replay])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('repro_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 vectors=[([-100.,110.],.1,b'{"cashflows":[-100.0,110.0],"rate":0.1}'),([1.,2.],.1,b'{"cashflows":[1.0,2.0],"rate":0.1}'),([0.,-0.],0.,b'{"cashflows":[0.0,-0.0],"rate":0.0}'),([-0.,0.],-0.,b'{"cashflows":[-0.0,0.0],"rate":-0.0}')]
 for i,(flows,rate,raw) in enumerate(vectors):
  test('literal bytes'+str(i),lambda f=flows,r=rate:m.input_bytes(f,r),raw)
  oracle=subprocess.run(['sha256sum'],input=raw,capture_output=True);assert oracle.returncode==0;digest=oracle.stdout.decode().split()[0];byte_oracles.append(dict(name='literal vector'+str(i),argv=['sha256sum'],stdin_utf8=raw.decode(),returncode=oracle.returncode,stdout=oracle.stdout.decode(),stderr=oracle.stderr.decode(),sha256=digest));test('manifest digest'+str(i),lambda f=flows,r=rate:m.run(f,r,'synthetic')['manifest']['input_sha256'],digest)
  if i==0:(OUT/'synthetic-input.json').write_bytes(raw)
 for name,flows,rate in [('known',[-100.,110.],.1),('t0',[3.],.1),('negative rate',[0.,95.],-.05),('negative flow',[0.,-110.],.1),('zero rate',[1.,2.],0.),('ordinary',[5.,-7.,9.],-.1)]:
  want=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));test(name,lambda f=flows,r=rate:m.run(f,r,'synthetic')['npv'],want,1e-10)
 d=m.run([1.,2.],.1,' revision label ');manifest=d['manifest'];test('manifest keys',lambda:sorted(manifest),sorted(['input_sha256','revision','python','model','convention']));test('revision retained unverified',lambda:manifest['revision'],' revision label ');test('python identity',lambda:manifest['python'],platform.python_version());test('model identity',lambda:manifest['model'],'periodic-npv-v1');test('timing convention',lambda:manifest['convention'],'first flow at time zero; effective rate per period')
 for rev in [None,'',' ',True]:test('bad revision '+repr(rev),lambda rev=rev:m.run([1.],0.,rev),'ValueError')
 for name,flows in [('empty',[]),('bool',[True]),('integer',[1]),('text','1'),('Decimal',[Decimal(1)]),('NaN',[math.nan]),('inf',[math.inf])]:test('flow '+name,lambda f=flows:m.run(f,0.,'x'),'ValueError')
 for name,rate in [('integer',0),('bool',True),('boundary',-1.),('NaN',math.nan),('inf',math.inf)]:test('rate '+name,lambda r=rate:m.run([1.],r,'x'),'ValueError')
 test('noniterable passthrough',lambda:m.run(None,0.,'x'),'TypeError')
 seen=[]
 def values():
  for x in [1.,2.]:seen.append(x);yield x
 test('generator result',lambda:m.run(values(),0.,'x')['npv'],3.);test('generator consumed once',lambda:seen,[1.,2.])
 instance=RuntimeError('synthetic iterator error')
 def broken():
  yield 1.
  raise instance
 try:m.run(broken(),0.,'x')
 except Exception as e:test('late iterator identity',lambda:e is instance,True)
 original=[1.,2.];m.run(original,0.,'x');test('caller list unchanged',lambda:original,[1.,2.])
 test('order changes bytes',lambda:m.input_bytes([1.,2.],.1)!=m.input_bytes([2.,1.],.1),True);test('rate changes bytes',lambda:m.input_bytes([1.,2.],.1)!=m.input_bytes([1.,2.],math.nextafter(.1,math.inf)),True);test('flow changes digest',lambda:m.run([1.,2.],.1,'x')['manifest']['input_sha256']!=m.run([1.,3.],.1,'x')['manifest']['input_sha256'],True)
 for label,fn in [('revision not input digest',lambda:m.run([1.],0.,'a')['manifest']['input_sha256']==m.run([1.],0.,'b')['manifest']['input_sha256']),('signed zero bytes differ',lambda:m.input_bytes([0.],0.)!=m.input_bytes([-0.],0.))]:supp.append(dict(name=label,passed=fn(),scope='Manifest/representation design observation;not full-run identity or provenance acceptance'))
 replay1=next(x['stdout'] for x in commands if x['label']=='replay process1');replay2=next(x['stdout'] for x in commands if x['label']=='replay process2');test('local process replay bytes',lambda:replay1,replay2);(OUT/'replay-process-1.json').write_text(replay1);(OUT/'replay-process-2.json').write_text(replay2)
d=dict(candidate_based_on='4b182d1e0aee83789733233f2f8ae151d989aa3f',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,independent_byte_oracle_commands=byte_oracles,supplemental_manifest_observations=supp,existing_unique_methods=12,method_invocations=36,new_historical_unique_methods=0,limits='Same candidate runtime synthetic process replay and input identity only;no external-data provenance,verified supplied revision,full environment capture,universal JSON standard,cross-platform or independent acceptance. F28/F32/F209/static-checker and broader NPV gaps remain open.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;4 separate byte-oracle commands;2 design observations;7 source commands');assert all(x['passed'] for x in rows+supp) and all(x['returncode']==0 for x in commands)
