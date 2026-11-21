"""Selected installed threshold policies and separate numerical-limit observations."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,Context,localcontext
import financial_toolkit.simulation as simulation
import financial_toolkit.statistics as statistics
import json,sys,math,hashlib,platform
rows=[];observations=[]
def ck(name,got,want):rows.append(dict(name=name,actual=got,expected=str(want),passed=got==want))
for m in [simulation,statistics]:assert Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
original=simulation.random.Random
probabilities=[0.,math.ulp(0.0),2**-54,math.nextafter(.25,0),.25,math.nextafter(.25,1),math.nextafter(1.,0),1.]
draws=[0.,.25,.5,1-2**-53]
for p in probabilities:
 class Controlled:
  def __init__(self,seed):self.i=0
  def random(self):v=draws[self.i];self.i+=1;return v
 try:simulation.random.Random=Controlled;r=simulation.simulate_two_outcome(100.,.5,0.,p,4,42)
 finally:simulation.random.Random=original
 expected=tuple(150. if F(x)<F(p) else 100. for x in draws)
 ck('threshold terminals p'+repr(p),r.terminal_values,expected)
 s=statistics.summarize_sample(r.terminal_values);ck('observed mean p'+repr(p),s.mean,float(sum(map(F,expected))/4))
 ck('threshold parameter p'+repr(p),r.up_probability,p)
 # Conditional uniform-grid CDF, not a validation of the actual RNG law.
 cells=math.ceil(F(p)*2**53);grid=F(cells,2**53)
 ck('conditional grid at/above p'+repr(p),grid>=F(p),True)
 observations.append(dict(kind='conditional 53-bit uniform-grid law only',probability=str(F(p)),grid_probability=str(grid),difference=str(grid-F(p)),claim='No actual PRNG uniformity/independence certification; controlled draw mapping only.'))
for initial in [1e-150,1e-160,1e-200,math.ulp(0.0)]:
 draws=[0.,1-2**-53,0.,1-2**-53]
 class Controlled:
  def __init__(self,seed):self.i=0
  def random(self):v=draws[self.i];self.i+=1;return v
 try:simulation.random.Random=Controlled;r=simulation.simulate_two_outcome(initial,.25,-.25,.5,4,42)
 finally:simulation.random.Random=original
 s=statistics.summarize_sample(r.terminal_values);values=list(map(F,r.terminal_values));mean=sum(values)/4;variance=sum((values[i]-values[j])**2 for i in range(4) for j in range(i+1,4))/12
 with localcontext(Context(prec=120)):sd=float((D(variance.numerator)/D(variance.denominator)).sqrt())
 ck('finite actual terminals '+repr(initial),all(math.isfinite(v) for v in r.terminal_values),True)
 ck('documented finite nonnegative fields '+repr(initial),all(math.isfinite(v) and v>=0 for v in [s.sample_variance,s.sample_stddev]),True)
 exact_up=F(initial)*F(5,4);exact_down=F(initial)*F(3,4)
 observations.append(dict(kind='declared rounding/underflow limit, not accuracy pass',initial=initial,actual_terminal_values=r.terminal_values,exact_model_up=str(exact_up),exact_model_down=str(exact_down),distinct_model_outcomes=exact_up!=exact_down,distinct_float_outcomes=len(set(r.terminal_values))>1,native_variance=s.sample_variance,exact_variance_of_actual_float_sample=str(variance),native_stddev=s.sample_stddev,reference_stddev_of_actual_float_sample=sd,caller_native_SE=s.sample_stddev/2,caller_reference_SE=sd/2,status='Documented floating product/squared-deviation underflow can erase modeled variation or report zero SD/SE despite a representable reference; not a new defect, not closed by finite outputs.'))
result=dict(python=platform.python_version(),platform=platform.platform(),rows=rows,observations=observations,passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),installed_modules={m.__name__:dict(path=m.__file__,sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for m in [simulation,statistics]},scope='40 mapping/finite-policy predicates; 12 separate conditional-grid/numerical observations; not financial accuracy or RNG acceptance')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
