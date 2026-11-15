"""Stage exact finlib project fences;root-import/source execution is not installation."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib,json,hashlib,math,platform,logging,io,contextlib
from decimal import Decimal
from fractions import Fraction
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.15-chapter-project-production-quality-financial-library.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();fences=re.findall(r'```python\n(.*?)\n```',text,re.S);assert len(fences)==4;paths=['finlib/__init__.py','finlib/valuation.py','example_usage.py','tests/test_valuation.py'];commands=[];rows=[];limits=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=math.isfinite(a) and math.isclose(a,want,rel_tol=5e-14,abs_tol=tol) if isinstance(want,float) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),relative_tolerance=5e-14 if isinstance(want,float) else 0,absolute_tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp)
 for rel,code in zip(paths,fences):
  f=tmp/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(code)
 quiet='import logging;before=(list(logging.getLogger().handlers),logging.getLogger().level);import finlib;assert before==(list(logging.getLogger().handlers),logging.getLogger().level)'
 for label,args in [('documented discovery',[sys.executable,'-m','unittest','discover','-s','tests','-v']),('reference main via root',[sys.executable,'-c','import runpy;runpy.run_path("tests/test_valuation.py",run_name="__main__")']),('optimized discovery',[sys.executable,'-O','-m','unittest','discover','-s','tests','-v']),('four fence compilation',[sys.executable,'-m','compileall','-q','finlib','tests','example_usage.py']),('quiet import/root state',[sys.executable,'-c',quiet]),('provided example',[sys.executable,'example_usage.py'])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 sys.path.insert(0,str(tmp));m=importlib.import_module('finlib');fn=m.npv
 for i,(flows,rate) in enumerate([([-100.,110.],.1),([-100.,60.,60.],.1),([-100.,60.,60.],0.),((50.,),.1),([0.,95.],-.05),([0.,-110.],.1),([-200.,120.,120.],.1),([1.,0.,1.],1.),([0.,100.],1e308),([0.,math.ulp(0.)],1.)]):
  want=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));test('independent NPV'+str(i),lambda f=flows,r=rate:fn(f,r),want,1e-10 if i==0 or abs(want)>1 else 0)
 for label,flows in [('empty',[]),('empty tuple',()),('generator',iter([1.])),('None',None),('text','1'),('mapping',{0.:1.}),('integer member',[1]),('bool member',[True]),('Decimal member',[Decimal(1)]),('NaN',[math.nan]),('inf',[math.inf])]:test('flow reject '+label,lambda f=flows:fn(f,.1),'ValueError')
 for label,rate in [('integer',0),('bool',True),('None',None),('text','0.1'),('Decimal',Decimal('.1')),('NaN',math.nan),('inf',math.inf),('boundary',-1.),('below',-1.1)]:test('rate reject '+label,lambda r=rate:fn([1.],r),'ValueError')
 test('rate validates before schedule',lambda:fn(None,True),'ValueError')
 original=[-100.,60.,60.];copy=original.copy();fn(original,.1);test('caller list unchanged',lambda:original,copy)
 test('exports npv',lambda:m.__all__,['npv']);test('package root module',lambda:fn.__module__,'finlib.valuation')
 stream=io.StringIO();before=(list(logging.getLogger().handlers),logging.getLogger().level)
 with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):fn([1.,2.],0.)
 test('calculation emits no output',lambda:stream.getvalue(),'');test('calculation root state unchanged',lambda:(list(logging.getLogger().handlers),logging.getLogger().level)==before,True)
 test('monotonic positive future flow',lambda:fn([0.,100.],.05)>fn([0.,100.],.1),True);test('mixed-sign direction counterexample',lambda:fn([100.,-110.],.05)<fn([100.,-110.],.1),True)
 test('scaling',lambda:math.isclose(fn([-200.,120.,120.],.1),2*fn([-100.,60.,60.],.1),rel_tol=5e-14,abs_tol=1e-10),True);test('additivity same timing/rate',lambda:math.isclose(fn([-150.,90.,90.],.1),fn([-100.,60.,60.],.1)+fn([-50.,30.,30.],.1),rel_tol=5e-14,abs_tol=1e-10),True)
 test('detected intermediate overflow',lambda:fn([0.,1e308],-.5),'ValueError')
 try:a=fn([-1e308,1e308],-.5)
 except Exception as e:a=type(e).__name__
 exact=float(Fraction(-1e308)+Fraction(1e308)/(1+Fraction(-.5)));limits.append(dict(name='documented finite final value rejected by intermediate range',actual=repr(a),independent_final=repr(exact),status='RETAINED LIMIT — intentional documented intermediate rejection,not a newly failing acceptance predicate'))
 test('example display output',lambda:next(x['stdout'] for x in commands if x['label']=='provided example'),'NPV: 4.132231\n')
 sys.path.pop(0)
d=dict(candidate_based_on='78b2ddb63e3bef63f54b89e6e879ef2c4ea46f2c',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=[hashlib.sha256(x.encode()).hexdigest() for x in fences],staged_paths=paths,commands=commands,source_call_predicates=rows,documented_range_observations=limits,existing_unique_methods=12,method_invocations=36,new_historical_unique_methods=0,limits='Exact project-root imports/examples/tests only;no packaging/installed artifact,all-range NPV,release/production/model/platform or independent acceptance. F28/F32/F209/static-checker and broader gaps open.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;1 separate range observation;6 commands/4 fences');assert all(x['passed'] for x in rows) and all(x['returncode']==0 for x in commands)
