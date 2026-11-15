"""Exact educational software example;conceptual model review is not acceptance."""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,math,platform
from fractions import Fraction
from decimal import Decimal
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else None
p=BOOK/'chapter-20/20.14-model-validation-vs-software-validation.md';text=subprocess.check_output(['git','show',REV+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True) if REV else p.read_text();code=re.search(r'~~~python\n(.*?)\n~~~',text,re.S)[1];commands=[];rows=[];supp=[]
def test(name,fn,want,tol=0):
 try:a=fn();ok=math.isclose(a,want,rel_tol=5e-14,abs_tol=tol) if isinstance(want,float) else a==want
 except Exception as e:a=type(e).__name__;ok=a==want
 rows.append(dict(name=name,actual=repr(a),expected=repr(want),relative_tolerance=5e-14 if isinstance(want,float) else 0,absolute_tolerance=tol,passed=ok))
with tempfile.TemporaryDirectory() as temp:
 tmp=Path(temp);src=tmp/'validation_example.py';src.write_text(code)
 for label,args in [('source suite',[sys.executable,src.name]),('module suite',[sys.executable,'-m','unittest','-v','validation_example']),('compilation',[sys.executable,'-m','compileall','-q',src.name]),('quiet import',[sys.executable,'-c','import validation_example']),('optimized suite',[sys.executable,'-O',src.name])]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True);commands.append(dict(label=label,argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr))
 spec=importlib.util.spec_from_file_location('model_ref',src);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 for i,(c,r) in enumerate([(100.,.1),(100.,0.),(95.,-.05),(0.,.1),(-110.,.1),(200.,.1),(math.ulp(0.),0.),(1e308,1e308),(100.,math.nextafter(-1.,0.))]):
  expected=float(Fraction(c)/(1+Fraction(r)));test('independent periodic value'+str(i),lambda c=c,r=r:m.present_value(c,r),expected,1e-10 if abs(expected)>1 else 0)
 for v in [100,True,None,'100',Decimal(100),math.nan,math.inf]:test('payment rejects '+repr(v),lambda v=v:m.present_value(v,.1),'ValueError')
 for v in [0,True,None,'0.1',Decimal('.1'),math.nan,math.inf,-1.,-1.1]:test('rate rejects '+repr(v),lambda v=v:m.present_value(100.,v),'ValueError')
 test('detected final overflow',lambda:m.present_value(1e308,-.9),'ValueError')
 test('rate sensitivity direction',lambda:m.present_value(100.,.05)>m.present_value(100.,.1),True);test('scaling invariant',lambda:math.isclose(m.present_value(200.,.1),2*m.present_value(100.,.1),rel_tol=5e-14,abs_tol=0),True)
 # Counterexample is a separate hypothetical richer model,not executed source/default-risk validation.
 certain=Fraction(100,1)/Fraction(11,10);risky=(Fraction(9,10)*100+Fraction(1,10)*40)/Fraction(11,10)
 supp=[dict(name='hypothetical default/recovery counterexample',certain_payment_value=str(certain),hypothetical_value=str(risky),assumptions='Illustrative90% full-payment probability and10% recovery40;no observed calibration or market evidence',passed=risky<certain,scope='Supplemental rational scenario,not an implemented credit model or independent financial acceptance'),dict(name='rate units differ',decimal_five_percent_value=str(Fraction(100)/(1+Fraction(5,100))),literal_five_rate_value=str(Fraction(100)/6),passed=Fraction(100)/(1+Fraction(5,100))!=Fraction(100)/6,scope='Supplemental exact-unit illustration,not a source input-convention validator')]
d=dict(candidate_based_on='824ab9a1f874f18f379e8137812958f3a841f15a',selected_revision=REV,python=sys.version,platform=platform.platform(),manuscript_sha256=hashlib.sha256(text.encode()).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),commands=commands,source_call_predicates=rows,supplemental_conceptual_scenarios=supp,existing_unique_methods=12,method_invocations=36,new_historical_unique_methods=0,limits='Selected software/PV/input checks only;conceptual assumptions/governance/source applicability/outcome analysis not independently accepted. F28/F32/F209/static-checker and broad numerical/platform/model/release gaps open.')
(OUT/('baseline.json' if REV else 'results.json')).write_text(json.dumps(d,indent=2)+'\n');print(len(rows),'source predicates;',sum(not x['passed'] for x in rows),'failed;2 separate conceptual scenarios;5 source commands');assert all(x['passed'] for x in rows+supp) and all(x['returncode']==0 for x in commands)
