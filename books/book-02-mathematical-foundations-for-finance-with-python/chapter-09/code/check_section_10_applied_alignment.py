"""Exercise25 exact seven-shock project alignment; rational series oracle.
Assertions required. Optional results path; sibling -export.json is caller-side export.
"""
import sys,json,math,hashlib
from pathlib import Path
from fractions import Fraction as F
import section_9_09 as project
import section_9_10 as assessment
if not __debug__:raise RuntimeError('exercise checks require assertions enabled')
flows=[(120,.5),(120,1),(120,2),(1120,3)];rate=.04;grid=[-100,-50,-25,0,25,50,100];records=[]
def exponential(x):
 assert abs(x)<F(1,2)
 term=total=F(1)
 for k in range(1,101):term=term*x/k;total+=term
 return total
# exp remainder <2*(1/2)^101/101! for this restricted input family.
def check(name,actual,expected,kind='direct numerical'):
 if isinstance(expected,bool):ok=type(actual)is bool and actual is expected
 elif isinstance(expected,(dict,list,str)):ok=actual==expected
 else:ok=type(actual)is float and math.isclose(actual,float(expected),rel_tol=5e-14,abs_tol=1e-12)
 records.append(dict(name=name,kind=kind,actual=actual,expected=float(expected) if isinstance(expected,F) else expected,passed=ok));assert ok,name
R=F(rate);terms=[F(c)*exponential(-R*F(t)) for c,t in flows];V=sum(terms,F(0));A=-sum((F(t)*v for (_,t),v in zip(flows,terms)),F(0));B=sum((F(t)**2*v for (_,t),v in zip(flows,terms)),F(0))
report=project.project_report(flows,rate,grid)
for key,value in zip(('baseline_value','first_derivative','second_derivative','duration','convexity'),(V,A,B,-A/V,B/V)):check('E25 task1 '+key,report[key],value)
assert len(report['scenarios'])==7
for row,bp in zip(report['scenarios'],grid):
 h=float(bp)/10000;H=F(h);low=min(R,R+H)
 shifted=sum((F(c)*exponential(-(R+H)*F(t)) for c,t in flows),F(0));exact=shifted-V;linear=A*H;quadratic=linear+B*H*H/2
 bound1=sum((F(c)*F(t)**2*exponential(-low*F(t))*H*H/2 for c,t in flows),F(0));bound2=sum((F(c)*F(t)**3*exponential(-low*F(t))*abs(H)**3/6 for c,t in flows),F(0))
 values=dict(shock_bp=float(bp),shock_decimal=h,exact_change=exact,linear_change=linear,quadratic_change=quadratic,exact_value=shifted,linear_error=exact-linear,quadratic_error=exact-quadratic,absolute_linear_error=abs(exact-linear),absolute_quadratic_error=abs(exact-quadratic),linear_bound=bound1,quadratic_bound=bound2)
 assert set(row)==set(values)|{'linear_bound_pass','quadratic_bound_pass'}
 for key,value in values.items():check(f'E25 tasks2–4 {bp} '+key,row[key],value)
 for key in ('linear_bound_pass','quadratic_bound_pass'):check(f'E25 task4 {bp} '+key,row[key],True,'direct numerical flag')
 # Independent latent bound eligibility, without the implementation's baseline allowance.
 assert abs(exact-linear)<=bound1 and abs(exact-quadratic)<=bound2
check('E25 task1 cash schedule',report['cash_flows'],[dict(cash=float(c),years=float(t)) for c,t in flows],'direct metadata')
check('E25 rate convention',report['rate_convention'],'decimal annual continuously compounded','direct metadata')
check('certification',report['validation']['runtime_certified'],False,'direct metadata')
check('independent review',report['validation']['independent_review_completed'],False,'direct metadata')
a=assessment.assessment()
for key in ('baseline_value','duration','convexity','scenarios'):check('assessment projection '+key,a[key],report[key],'cross-module projection')
for key in ('runtime_certified','independent_review_completed'):check('assessment '+key,a[key],False,'cross-module projection')
# Task5 explicit smooth-polynomial counterexample; supplemental, not a project implementation.
x=F(0);h=F(2);exact=h**3-2*h**2;linear=F(0);quadratic=-2*h*h
ok=abs(exact-quadratic)>abs(exact-linear);assert ok
records.append(dict(name='E25 task5 smooth cubic counterexample',kind='supplemental analytical example',actual=dict(exact=str(exact),linear=str(linear),quadratic=str(quadratic)),expected='quadratic error8 exceeds linear error0',passed=ok))
text=json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+'\n'
check('E25 task6 repeated report serialization',json.dumps(project.project_report(flows,rate,grid),sort_keys=True,indent=2,allow_nan=False)+'\n',text,'caller export')
check('E25 task6 finite JSON roundtrip',json.loads(text),report,'caller export')
# Exercise asks to document failures: actual invalid project grids are rejected.
for label,g in [('missing zero',[-100,100]),('no downside',[0,100]),('no upside',[-100,0])]:
 try:project.project_report(flows,rate,g)
 except ValueError as e:records.append(dict(name='E25 task6 '+label,kind='direct rejection',exception=type(e).__name__,message=str(e),passed=True))
 else:raise AssertionError(label)
result=dict(passed=len(records),failed=0,records=records,export_sha256=hashlib.sha256(text.encode()).hexdigest(),oracle='100-term exact rational exponential series, |exponent|<.5; tail <2*(.5)^101/101!',limits='Exact exercise25 schedule/grid only. Analytical counterexample and JSON file export are caller/supplemental work; no native writer, financial lineage, market model or independent acceptance.')
if len(sys.argv)>1:
 out=Path(sys.argv[1]);out.write_text(json.dumps(result,indent=2)+'\n');out.with_name(out.stem+'-export.json').write_text(text)
print('PASS',len(records),'E25 alignment predicates',result['export_sha256'])
