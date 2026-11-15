"""Execute exact 20.16/20.15 fences; independent benchmarks and scoped lab evidence."""
from pathlib import Path
import re,sys,subprocess,tempfile,importlib,json,math,hashlib,platform
from fractions import Fraction
from decimal import Decimal,localcontext,Context,ROUND_HALF_UP
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1]
REV=sys.argv[1] if len(sys.argv)>1 else None
paths=['chapter-20/20.16-exercises-and-applied-problems.md','chapter-20/20.15-chapter-project-production-quality-financial-library.md']
texts=[subprocess.check_output(['git','show',REV+':'+str((BOOK/p).relative_to(ROOT))],cwd=ROOT,text=True) if REV else (BOOK/p).read_text() for p in paths]
fences=[re.findall(r'```python\n(.*?)\n```',s,re.S) for s in texts];assert list(map(len,fences))==[1,4]
commands=[];rows=[];supp=[]
def check(name,fn,want,absolute=0):
 try:a=fn();ok=(isinstance(a,float) and math.isfinite(a) and math.isclose(a,want,rel_tol=5e-14,abs_tol=absolute)) if isinstance(want,float) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),relative_tolerance=5e-14 if isinstance(want,float) else None,absolute_tolerance=absolute,passed=ok))
with tempfile.TemporaryDirectory() as td:
 tmp=Path(td);save=['chapter20_reference_checks.py','finlib/__init__.py','finlib/valuation.py','example_usage.py','tests/test_valuation.py']
 for rel,code in zip(save,fences[0]+fences[1]):
  p=tmp/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(code)
 for label,args in [('20.16 direct',['chapter20_reference_checks.py']),('20.16 optimized',['-O','chapter20_reference_checks.py']),('20.16 discovery',['-m','unittest','chapter20_reference_checks','-v']),('20.15 discovery',['-m','unittest','discover','-s','tests','-v']),('20.15 optimized',['-O','-m','unittest','discover','-s','tests','-v']),('20.15 main via root',['-c','import runpy;runpy.run_path("tests/test_valuation.py",run_name="__main__")']),('compile five fences',['-m','compileall','-q','.']),('20.15 example',['example_usage.py'])]:
  argv=[sys.executable]+args;z=subprocess.run(argv,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 sys.path.insert(0,td);pv=importlib.import_module('chapter20_reference_checks').pv_one;npv=importlib.import_module('finlib').npv
 for name,flows,rate,want in [('ex2 time zero',[-100.,110.],.1,0.),('ex3 two periods',[-100.,60.,60.],.1,float(Fraction(500,121))),('ex4 zero rate',[-100.,60.,60.],0.,20.),('ex5 negative rate',[0.,95.],-.05,100.),('ex35 two-year timeline',[-100.,0.,121.],.1,0.)]:check(name,lambda f=flows,r=rate:npv(f,r),want,1e-10 if want==0 else 1e-12)
 for i,(cash,rate,want) in enumerate([(110.,.1,100.),(95.,-.05,100.),(100.,.05,float(Fraction(2000,21))),(100.,.1,float(Fraction(1000,11))),(-110.,.1,-100.),(0.,.1,0.)]):check('one-period benchmark '+str(i),lambda c=cash,r=rate:pv(c,r),want,1e-10)
 for label,fn in [('reference boundary',lambda:pv(100.,-1.)),('project boundary',lambda:npv([1.],-1.)),('reference bool',lambda:pv(True,.1)),('reference integer',lambda:pv(100,.1)),('project bool',lambda:npv([True],.1)),('project integer',lambda:npv([100],.1)),('project empty',lambda:npv([],.1)),('reference nan',lambda:pv(math.nan,.1)),('project infinity',lambda:npv([math.inf],.1)),('project wrong rate',lambda:npv([1.],True)),('reference overflow',lambda:pv(1e308,-.5))]:check(label,fn,'ValueError')
 check('ex16 scaling',lambda:math.isclose(npv([-200.,120.,120.],.1),2*npv([-100.,60.,60.],.1),rel_tol=5e-14),True)
 check('ex17 aligned additivity',lambda:math.isclose(npv([-150.,90.,90.],.1),npv([-100.,60.,60.],.1)+npv([-50.,30.,30.],.1),rel_tol=5e-14),True)
 check('ex18 positive future monotonic',lambda:pv(100.,.05)>pv(100.,.1),True)
 check('ex18 mixed-sign counterexample',lambda:npv([100.,-110.],.05)<npv([100.,-110.],.1),True)
 f=[-100.,60.,60.];copy=f.copy();npv(f,.1);check('ex30 caller ownership',lambda:f,copy)
 check('ex25 lost subnormal contribution',lambda:npv([1.,math.ulp(0.)],1.),1.)
 with localcontext(Context(prec=80)):
  monthly=(Decimal(28)/Decimal(25))**(Decimal(1)/Decimal(12))-1
  supp.append(dict(name='ex34 independently exponentiated monthly rate',actual=str(monthly),display='0.00948879',passed=abs(monthly-Decimal('0.00948879'))<Decimal('0.000000005')))
  x=Decimal('.005');cent=Decimal('.01');supp.append(dict(name='ex15 rounding stage',individual=str(2*x.quantize(cent,rounding=ROUND_HALF_UP)),combined=str((2*x).quantize(cent,rounding=ROUND_HALF_UP)),passed=2*x.quantize(cent,rounding=ROUND_HALF_UP)==Decimal('.02') and (2*x).quantize(cent,rounding=ROUND_HALF_UP)==Decimal('.01')))
 supp.append(dict(name='ex13/ex14 representation',passed=(.1+.2!=.3 and Decimal(.1)!=Decimal('.1'))))
 sys.path.pop(0)
d=dict(selected_revision=REV,python=sys.version,platform=platform.platform(),source_paths=[str((BOOK/p).relative_to(ROOT)) for p in paths],source_sha256=[hashlib.sha256(s.encode()).hexdigest() for s in texts],fence_sha256=[[hashlib.sha256(c.encode()).hexdigest() for c in ff] for ff in fences],commands=commands,source_predicates=rows,supplemental_demonstrations=supp,existing_unique_methods=dict(exercise_reference=12,project_reference=12),method_invocations=dict(exercise_reference=36,project_reference=36),new_historical_unique_methods=0,limits='Assistant scoped source execution plus separate supplemental arithmetic and conceptual records;not all-range correctness,installed-package/platform/model/release or independent acceptance. F28/F32 and other tracker gaps retained.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates',len(supp),'supplemental',len(commands),'commands');assert all(x['passed'] for x in rows+supp) and all(x['returncode']==0 for x in commands)
