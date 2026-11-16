"""Exercise1–8 exact-source helper alignment;analytical/composed work explicit."""
from fractions import Fraction as F
from decimal import Decimal,Context,localcontext
from pathlib import Path
import sys,json,math,hashlib
from section_9_02 import point_elasticity
from section_9_03 import linear_taylor,compare_change
from section_9_04 import taylor_change
from section_9_05 import polynomial_example
rows=[]
def add(ex,field,got,want,tol=0.,kind='actual source helper'):
 ok=type(got)is bool and got==want if type(want)is bool else got==want if isinstance(want,str) else type(got)is float and math.isfinite(got) and math.isclose(got,float(want),rel_tol=5e-14,abs_tol=tol)
 rows.append(dict(exercise=ex,field=field,actual=repr(got),expected=repr(want),relative_tolerance=5e-14,absolute_tolerance=tol,kind=kind,passed=ok))
# Derivatives are analytical caller inputs;point_elasticity isnot a symbolic differentiator.
add('E1','elasticity',point_elasticity(4.,50.,24.),F(48,25));add('E2','exponential elasticity',point_elasticity(.5,math.e,2*math.e),F(1))
for label,x,y,d in [('nearzero',1.,1e-300,1e-300),('subnormal',1.,math.ulp(0.),math.ulp(0.)),('large x',1e308,1e-308,1e-308)]:add('E1/E3 domain '+label,'elasticity',point_elasticity(x,y,d),F(x)*F(d)/F(y))
for label,args,want in [('zero output',(4.,0.,24.),'ValueError'),('zero x contract',(0.,50.,24.),'ValueError'),('bool x',(True,50.,24.),'TypeError')]:
 try:point_elasticity(*args);a='returned'
 except Exception as e:a=type(e).__name__
 add('E3 '+label,'rejection',a,want)
add('E4','linear sqrt approximation',linear_taylor(10.,1/20,1.),F(201,20),1e-12);change=taylor_change(1/20,-1/4000,1.);add('E5','quadratic change',change,F(399,8000),1e-12);add('E5','composed value',10.+change,F(80399,8000),1e-12,'source change plus explicit caller addition')
for h in (-.1,.1):
 a=polynomial_example(h);H=F(h);want=dict(exact=(2+H)**3,linear=8+12*H,quadratic=8+12*H+6*H*H,quadratic_remainder=H**3,quadratic_bound=abs(H)**3)
 for k,v in want.items():add('E6/E7 h='+str(h),k,a[k],v)
# Compare_change uses rounded sampled point/function outputs,not an analytic x+h oracle.
x=2.;h=.1;f=lambda x:x**3;d=lambda x:3*x*x;a=compare_change(f,d,x,h);V,W,D,H=map(F,(f(x),f(x+h),d(x),h));E=W-V;L=D*H;error=E-L
want=dict(baseline_value=V,exact_change=E,linear_change=L,linear_value=V+L,signed_error=error,absolute_error=abs(error),relative_change_error=abs(error)/abs(E))
for k,v in want.items():add('E7 sampled callbacks',k,a[k],v)
add('E7','nominal signed error',a['signed_error'],F(61,1000),1e-12,'source result compared withnominal exercise model');add('E7','within separately derived .063 bound',abs(a['signed_error'])<=float(F(63,1000)),True,kind='source result plus analytical bound')
with localcontext(Context(prec=100)):r1=Decimal('.0001')**(Decimal(1)/3)
with localcontext(Context(prec=160)):r2=Decimal('.0001')**(Decimal(1)/3)
assert float(r1)==float(r2);root=float(r2);low=math.nextafter(root,0.);high=math.nextafter(root,math.inf)
for label,h in [('below root',low),('above root',high)]:
 H=F(h);a=polynomial_example(h);add('E8 '+label,'source cubic bound',a['quadratic_bound'],abs(H)**3);add('E8 '+label,'8x cubic bound eligibility',8*a['quadratic_bound']<=.0008,label=='below root',kind='explicit8xsourcebound composition,not inverse-budget API')
# Preserve the distinction between an approximate printed root and safe admission.
observation=dict(root=str(r2),printed_approximation=.046416,printed_as_input_bound=float(8*F(.046416)**3),budget=.0008,printed_exceeds_exact_admissible_root=8*F(.046416)**3>F(8,10000),interpretation='Exercise states the exactcube-root bound and an approximate decimal;rounded displayed value isnot a conservative admissible input. No native inverse-budget helper isclaimed.')
d=dict(source_predicates=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),supplemental_analytical_inputs=dict(E1_derivative='6*4=24',E2_derivative='2*exp(1)',E4_derivative='1/20',E5_second_derivative='-1/4000',E7_bound='max6x=12.6 on[2,2.1]',E8_model='8x^3 hasthirdderivative48;root and8xboundcomposition outside supplied helper API'),inverse_budget_observation=observation,limits='Matching actual source primitives forE1–8;derivatives/interval extrema are supplied analytical inputs,not computed symbolically. E5value addition/E7bound/E8root-and-scaling areexplicit supplemental compositions,notnativeinversebudgetcode. No independent model/platform/release approval;broaderdomains/resources remainopen.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(predicates=len(rows),passed=d['passed'],failed=d['failed'])));assert d['failed']==0
