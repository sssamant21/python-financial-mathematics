"""Exact boundary manuscript source; Decimal oracles and semantic controls distinct."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction
from decimal import Decimal,Context,localcontext
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.04-boundary-and-edge-cases.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];rows=[];commands=[]
def test(name,fn,want,rtol=0,atol=0):
 try:
  a=fn();ok=(math.isfinite(a) and math.isclose(a,want,rel_tol=rtol,abs_tol=atol)) if (rtol or atol) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),relative_tolerance=rtol,absolute_tolerance=atol,passed=ok))
def oracle(values,kind):
 refs=[]
 for prec in (1600,2000):
  with localcontext(Context(prec=prec)):
   d=list(map(Decimal,values));z=sum(d,Decimal(0))/len(d) if kind=='mean' else (d[1]-d[0])/d[0];f=float(z);refs.append(f if math.isfinite(f) else 'ValueError')
 assert refs[0]==refs[1]
 return refs[0]
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'boundary_cases.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','boundary_cases']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import boundary_cases']),('optimized source suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('boundary_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for c,r,n in [(95,-.05,1),(-110,.1,1),(100,0,1),(100,.05,0),(17,.2,3),(1,math.nextafter(-1,math.inf),0),(1,math.nextafter(-1,math.inf),1)]:test('rational PV '+repr((c,r,n)),lambda c=c,r=r,n=n:m.present_value(c,r,n),float(Fraction(c)/(1+Fraction(r))**n),rtol=4e-14,atol=1e-10)
 for name,c,r,n in [('rate boundary',1,-1,1),('below boundary',1,math.nextafter(-1,-math.inf),1),('negative periods',1,0,-1),('fractional periods',1,0,1.5),('bool periods',1,0,True),('NaN flow',math.nan,0,1),('infinite rate',1,math.inf,1),('bool flow',True,0,1),('text rate',1,'0',1),('Decimal flow',Decimal(1),0,1),('oversized flow',10**1000,0,1),('oversized rate',1,10**1000,1),('zero identity invalid rate',0,-1,0)]:test(name,lambda c=c,r=r,n=n:m.present_value(c,r,n),'ValueError')
 for name,c,r,n,want in [('zero flow extreme discount',0,-.9,1000,0),('zero rate huge periods',7,0,10**1000,7),('zero flow huge periods',0,.1,10**1000,0)]:test(name,lambda c=c,r=r,n=n:m.present_value(c,r,n),want)
 for s,e in [(100,0),(100,101.5),(1e308,math.nextafter(1e308,math.inf)),(1e-308,1e308)]:test('complete return '+repr((s,e)),lambda s=s,e=e:m.simple_return(s,e),oracle([s,e],'return'),rtol=4e-15)
 for name,s,e in [('zero start',0,1),('negative start',-1,1),('negative end',1,-1),('missing start',None,1),('bool start',True,1),('NaN end',1,math.nan),('infinite end',1,math.inf),('oversized start',10**1000,1)]:test(name,lambda s=s,e=e:m.simple_return(s,e),'ValueError')
 mx=sys.float_info.max
 for vals in [[100],[0,2],[1e16,1,-1e16],[mx,mx],[mx,mx,-mx,-mx],[-mx,-mx],[math.ulp(0.),math.ulp(0.)]]:test('complete mean '+repr(vals),lambda v=vals:m.sample_mean(v),oracle(vals,'mean'),rtol=4e-15)
 for name,vals in [('empty mean',[]),('NaN mean',[math.nan]),('infinite mean',[math.inf]),('bool mean',[True]),('text mean',['1']),('oversized mean',[10**1000])]:test(name,lambda v=vals:m.sample_mean(v),'ValueError')
 test('mean generator',lambda:m.sample_mean(iter([1,2,3])),2.)
 def broken():
  yield 1
  raise RuntimeError('deliberate iterator failure')
 test('iterator error propagates',lambda:m.sample_mean(broken()),'RuntimeError')
# Supplemental comparison semantics,not financial API calls.
semantics=[dict(name='default relative remains with abs_tol',actual=math.isclose(100+1e-8,100,abs_tol=1e-10),expected=True),dict(name='explicit zero relative rejects',actual=math.isclose(100+1e-8,100,rel_tol=0,abs_tol=1e-10),expected=False)]
for x in semantics:x['passed']=x['actual']==x['expected']
d=dict(candidate_based_on='04aba8a51eb7b2ddf3208bb1ed045888704e18c2',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,supplemental_comparison_predicates=semantics,existing_unique_methods=14,method_invocations=42,new_historical_unique_methods=0,limits='Boundary helper finite/identity/complete-return/complete-mean scope;broader nonzero PV range,discount underflow,collection resources,platform and independent acceptance open')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source-call predicates;',sum(not x['passed'] for x in rows),'failed;2 supplemental controls;5 source commands');assert all(x['passed'] for x in rows+semantics) and all(x['returncode']==0 for x in commands)
