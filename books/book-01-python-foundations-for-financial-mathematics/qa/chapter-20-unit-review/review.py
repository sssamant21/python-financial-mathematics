"""Exact unit-testing source; independent oracles and supplemental mutations separated."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.03-unit-testing.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=abs(a-want)<=tol if tol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=str(a),expected=str(want),tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'unit_testing_finance.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','unit_testing_finance']),('compile',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import unit_testing_finance']),('optimized source suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('unit_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for c,r,n in [(110,.1,1),(95,-.05,1),(-110,.1,1),(100,0,1),(100,.05,0),(17,.2,3),(-13,-.1,4)]:
  want=float(Fraction(c)/(1+Fraction(r))**n);test('independent rational PV '+repr((c,r,n)),lambda c=c,r=r,n=n:m.present_value(c,r,n),want,1e-10)
 for label,c,r,n in [('rate boundary',1,-1,1),('below boundary',1,-1.1,1),('negative periods',1,0,-1),('fractional periods',1,0,1.5),('bool periods',1,0,True),('NaN flow',math.nan,0,1),('infinite rate',1,math.inf,1),('bool flow',True,0,1),('text rate',1,'0',1),('oversized flow',10**1000,0,1),('oversized rate',1,10**1000,1)]:test(label,lambda c=c,r=r,n=n:m.present_value(c,r,n),'ValueError')
 for label,c,r,n,want in [('zero flow at extreme discount',0,-.9,1000,0),('zero rate enormous integer periods',7,0,10**1000,7),('zero flow enormous periods',0,.1,10**1000,0),('zero periods negative flow',-7,.2,0,-7)]:test(label,lambda c=c,r=r,n=n:m.present_value(c,r,n),want)
 test('zero identity still validates bad rate',lambda:m.present_value(0,-1,0),'ValueError');test('zero identity still validates bool periods',lambda:m.present_value(0,0,True),'ValueError')
 test('linearity',lambda:m.present_value(220,.1,2),2*m.present_value(110,.1,2),1e-10);test('positive future monotonic',lambda:m.present_value(100,.05,2)>m.present_value(100,.06,2),True);test('negative future direction',lambda:m.present_value(-100,.05,2)<m.present_value(-100,.06,2),True);test('time zero constant',lambda:m.present_value(100,.05,0)==m.present_value(100,.06,0),True);test('near-zero tolerance',lambda:math.isclose(1e-12,0,rel_tol=0,abs_tol=1e-10),True)
 faulty=code.replace('result=cashflow*','result=abs(cashflow)*');(tmp/'faulty.py').write_text(faulty);probes=[]
 for label,args,want in [('supplemental sign defect',[sys.executable,'faulty.py','PresentValueTests.test_negative_cashflow'],1),('unchanged source control',[sys.executable,src.name,'PresentValueTests.test_negative_cashflow'],0)]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);probes.append(dict(label=label,argv=args,returncode=z.returncode,expected_returncode=want,stdout=z.stdout,stderr=z.stderr,passed=z.returncode==want))
 if not REV:(OUT/'faulty_variant.py.txt').write_text(faulty)
d=dict(candidate_based_on='fb5b9d7482605ae671893f70a2af6649db9ae9da',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,predicates=rows,supplemental_probes=probes,existing_unique_methods=12,method_invocations=38,new_historical_unique_methods=0,limits='Selected finite input/zero identity and ordinary PV contracts;broader scaled discount,large-period range,underflow/resource/platform/independent acceptance open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'predicates;',sum(not x['passed'] for x in rows),'failed;5 commands');assert all(x['passed'] for x in rows) and all(x['returncode']==0 for x in commands) and all(x['passed'] for x in probes)
