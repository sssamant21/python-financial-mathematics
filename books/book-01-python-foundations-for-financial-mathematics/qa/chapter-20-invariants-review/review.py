"""Exact invariant source; independent numeric references and zero-defect experiment."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction
from decimal import Decimal,Context,localcontext
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.07-financial-invariants.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];rows=[];commands=[]
def test(name,fn,want,rtol=0,atol=0):
 try:a=fn();ok=math.isfinite(a) and math.isclose(a,want,rel_tol=rtol,abs_tol=atol) if (rtol or atol) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),relative_tolerance=rtol,absolute_tolerance=atol,passed=ok))
def dec_ref(values,kind):
 refs=[]
 for prec in (1800,2400):
  with localcontext(Context(prec=prec)):
   d=list(map(Decimal,values));x=(d[1]-d[0])/d[0] if kind=='return' else sum((d[i]*d[i+2] for i in range(2)),Decimal(0));f=float(x);refs.append(f if math.isfinite(f) else 'ValueError')
 assert refs[0]==refs[1]
 return refs[0]
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'financial_invariants.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','financial_invariants']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import financial_invariants']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('invariant_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for flows,rate in [([-100,110],0),([-100,110],.1),([-100,0,110],.1),([5,-7,9],-.1)]:test('rational NPV '+repr((flows,rate)),lambda f=flows,r=rate:m.npv(f,r),float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction())),atol=1e-10)
 test('nonzero NPV scaling',lambda:m.npv([-200,220],.05),2*m.npv([-100,110],.05),atol=1e-10);test('append zero',lambda:m.npv([-100,110,0],.1),m.npv([-100,110],.1),atol=1e-10);test('insertion shifts timing',lambda:m.npv([-100,0,110],.1)<m.npv([-100,110],.1),True);test('positive future monotonic',lambda:m.npv([0,100],.05)>m.npv([0,100],.06),True);test('negative future direction',lambda:m.npv([0,-100],.05)<m.npv([0,-100],.06),True);test('time zero constant',lambda:m.npv([100],.05)==m.npv([100],.1),True)
 for s,e in [(100,101.5),(200,203),(100,0),(1e308,math.nextafter(1e308,math.inf)),(1e-308,1e308)]:test('complete return '+repr((s,e)),lambda s=s,e=e:m.simple_return(s,e),dec_ref([s,e],'return'),rtol=4e-15)
 test('return scale invariant',lambda:m.simple_return(100,101.5),m.simple_return(200,203),atol=1e-12)
 tol=1e-12;mx=sys.float_info.max
 for w,r in [([.6,.4],[.1,-.05]),([1.,0.],[.1,-1.]),([.5,.5],[-1.,-1.]),([1.,tol],[.1,.1]),([1.,math.nextafter(tol,0.)],[.1,.1]),([1.+5e-13,0.],[mx,0.]),([math.ulp(0.),1.],[mx,0.])]:test('complete portfolio '+repr((w,r)),lambda w=w,r=r:m.portfolio_return(w,r),dec_ref(w+r,'portfolio'),rtol=4e-15)
 for name,fn in [('bad weight count',lambda:m.portfolio_return([1],[.1])),('bad return count',lambda:m.portfolio_return([.5,.5],[.1])),('short weight',lambda:m.portfolio_return([-.1,1.1],[.1,.2])),('weight sum',lambda:m.portfolio_return([.6,.5],[.1,.2])),('just outside weight budget',lambda:m.portfolio_return([1.,math.nextafter(tol,math.inf)],[.1,.1])),('return below -1',lambda:m.portfolio_return([1.,0.],[math.nextafter(-1.,-math.inf),0.])),('bool weight',lambda:m.portfolio_return([True,0],[0,0])),('oversized weight',lambda:m.portfolio_return([10**1000,0],[0,0])),('NaN return',lambda:m.portfolio_return([1,0],[math.nan,0])),('oversized return start',lambda:m.simple_return(10**1000,1)),('zero start',lambda:m.simple_return(0,1)),('negative end',lambda:m.simple_return(1,-1)),('invalid rate',lambda:m.npv([1],-1)),('oversized flow',lambda:m.npv([10**1000],0)),('oversized rate',lambda:m.npv([1],10**1000))]:test(name,fn,'ValueError')
 test('portfolio generators',lambda:m.portfolio_return(iter([.6,.4]),iter([.1,-.05])),.04,atol=1e-12)
 # Deliberate always-zero NPV variant:scaling alone passes,known nonzero fails.
 faulty=re.sub(r'def npv\(.*?(?=\ndef simple_return)', 'def npv(cashflows,rate):\n    return 0.0\n',code,flags=re.S);(tmp/'faulty.py').write_text(faulty);experiments=[]
 for label,args,want in [('supplemental zero NPV scaling',[sys.executable,'faulty.py','InvariantTests.test_npv_scaling'],0),('supplemental zero NPV known nonzero',[sys.executable,'faulty.py','InvariantTests.test_known_nonzero_npv'],1),('unchanged source control',[sys.executable,src.name,'InvariantTests.test_known_nonzero_npv'],0)]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);experiments.append(dict(label=label,argv=args,returncode=z.returncode,expected_returncode=want,stdout=z.stdout,stderr=z.stderr,passed=z.returncode==want))
 if not REV:(OUT/'always_zero_variant.py.txt').write_text(faulty)
supp=[dict(name='plus10 minus10 compounds',actual=str(Decimal('1.1')*Decimal('.9')-1),expected='-0.01'),dict(name='units percent and basis point',actual=(str(Decimal(5)/100),str(Decimal(1)/10000)),expected=('0.05','0.0001'))]
for x in supp:x['passed']=x['actual']==x['expected']
d=dict(candidate_based_on='55b8ebef2ca9338976fa27b140aae386e7e0d82b',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,supplemental_experiments=experiments,supplemental_arithmetic_predicates=supp,existing_unique_methods=14,method_invocations=45,new_historical_unique_methods=0,limits='Selected periodic NPV/complete return/long-only approximate weight budget and dot product;broader NPV range,ingestion/resources,covariance/FX/model/platform/independent acceptance open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;2 supplemental arithmetic;3 supplemental method invocations;5 source commands');assert all(x['passed'] for x in rows+supp+experiments) and all(x['returncode']==0 for x in commands)
