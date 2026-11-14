"""Exact floating-point manuscript source and independent Decimal acceptance gates."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math,random
from decimal import Decimal,Context,localcontext
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.05-testing-floating-point-results.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];rows=[];commands=[]
def test(name,fn,want,atol=0):
 try:a=fn();ok=math.isfinite(a) and abs(a-want)<=atol if atol else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),absolute_tolerance=atol,passed=ok))
def gate(a,b,atol,rtol):
 refs=[]
 for prec in (1800,2400):
  with localcontext(Context(prec=prec)):
   A,B,AT,RT=map(Decimal,(a,b,atol,rtol));refs.append(abs(A-B)<=AT+RT*abs(B))
 assert refs[0]==refs[1]
 return refs[0]
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'floating_point_tests.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','floating_point_tests']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import floating_point_tests']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('float_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 mx=sys.float_info.max;tiny=math.ulp(0.);vectors=[(100.02,100.,.01,.00005),(1e-12,0.,1e-10,0.),(1.,2.,0.,.6),(2.,1.,0.,.6),(mx,-mx,mx,.5),(mx,-mx,mx,1.),(3*tiny,tiny,0.,1.5),(0.,tiny,0.,math.nextafter(1.,0.)),(100.,100.,0.,0.),(2.,1.,.7,.4)]
 rng=random.Random(2005)
 for i in range(32):
  a,b=[math.ldexp(rng.uniform(-1,1),rng.randrange(-1000,1001)) for _ in range(2)];at,rt=[abs(math.ldexp(rng.uniform(-1,1),rng.randrange(-1000,1001))) for _ in range(2)];vectors.append((a,b,at,rt))
 for i,args in enumerate(vectors):test('independent represented gate '+str(i)+' '+repr(args),lambda x=args:m.close_to_reference(*x),gate(*args))
 for name,args in [('NaN actual',(math.nan,0,1,0)),('infinite reference',(1,math.inf,1,0)),('infinite atol',(1,1,math.inf,0)),('NaN rtol',(1,1,0,math.nan)),('negative atol',(1,1,-1,0)),('negative rtol',(1,1,0,-1)),('bool actual',(True,1,0,0)),('text ref',(1,'1',0,0)),('oversized actual',(10**1000,1,0,0)),('oversized rtol',(1,1,0,10**1000))]:test(name,lambda x=args:m.close_to_reference(*x),'ValueError')
 for flows,rate in [([-100,110],.1),([0,110],.1),([0,100],0),([0,95],-.05),([5,-7,9],-.1)]:test('rational NPV '+repr((flows,rate)),lambda f=flows,r=rate:m.npv(f,r),float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction())),atol=1e-10)
 for name,flows,rate in [('empty NPV',[],0),('invalid rate',[1],-1),('infinite flow',[math.inf],0),('oversized flow',[10**1000],0),('oversized rate',[1],10**1000)]:test(name,lambda f=flows,r=rate:m.npv(f,r),'ValueError')
 test('NPV scaling',lambda:m.npv([-200,220],.05),2*m.npv([-100,110],.05),atol=1e-10);test('future payment monotonic',lambda:m.npv([0,100],.05)>m.npv([0,100],.06),True)
# Supplemental arithmetic/primitive observations,not source financial functions.
with localcontext(Context(prec=100)):
 x=Decimal('1e-12');logref=float((1+x).ln());expref=float(x.exp()-1)
supplement=[dict(name='binary .1+.2 equality',actual=.1+.2==.3,expected=False),dict(name='same-sign infinity math.isclose',actual=math.isclose(math.inf,math.inf),expected=True),dict(name='sum vs max criterion',actual=math.isclose(2,1,rel_tol=.4,abs_tol=.7),expected=False),dict(name='log1p small accuracy',actual=math.isclose(math.log1p(1e-12),logref,rel_tol=2e-15,abs_tol=0),expected=True),dict(name='expm1 small accuracy',actual=math.isclose(math.expm1(1e-12),expref,rel_tol=2e-15,abs_tol=0),expected=True),dict(name='decimal unit arithmetic',actual=str(Decimal('.01')*1000000),expected='10000.00')]
for x in supplement:x['passed']=x['actual']==x['expected']
d=dict(candidate_based_on='cc4c3de4d314d0bb569f78b8be94abe4c1d41c2e',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,supplemental_primitive_predicates=supplement,existing_unique_methods=14,method_invocations=42,new_historical_unique_methods=0,limits='Complete represented finite-input comparison plus ordinary NPV scope;broader NPV discount/sum/underflow/resource/platform and independent acceptance remain open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;',len(supplement),'supplemental predicates;5 source commands');assert all(x['passed'] for x in rows+supplement) and all(x['returncode']==0 for x in commands)
