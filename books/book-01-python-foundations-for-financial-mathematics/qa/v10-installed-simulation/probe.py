"""Run with -I in a clean wheel consumer, outside the scaffold."""
from pathlib import Path
from fractions import Fraction as F
import financial_toolkit.simulation as simulation
import financial_toolkit.statistics as statistics
import json,sys,math,itertools,hashlib,platform
rows=[]
def ck(name,actual,expected):
 ok=actual==expected if isinstance(expected,(tuple,bool)) else math.isclose(float(actual),float(expected),rel_tol=5e-13,abs_tol=0)
 rows.append(dict(name=name,actual=actual,expected=str(expected),passed=ok))
for mod in [simulation,statistics]:assert Path(mod.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
original=simulation.random.Random;weighted_mean=weighted_mse=weighted_se2=0.;mass=F(0)
for i,bits in enumerate(itertools.product([0,1],repeat=4)):
 instances=[]
 class Controlled:
  def __init__(self,seed):assert seed==42;self.index=0;instances.append(self)
  def random(self):
   bit=bits[self.index];self.index+=1;return .125 if bit else .5
 try:
  simulation.random.Random=Controlled
  record=simulation.simulate_two_outcome(100.,.25,-.25,.25,4,42)
 finally:simulation.random.Random=original
 values=tuple(125. if bit else 75. for bit in bits);n=4;up=sum(bits);weight=F(1,4)**up*F(3,4)**(4-up);mass+=weight
 expected_mean=F(sum(values))/n
 # Pairwise identity is distinct from source's rounded-mean squared deviations.
 variance=sum((F(values[a])-F(values[b]))**2 for a in range(n) for b in range(a+1,n))/(n*(n-1))
 summary=statistics.summarize_sample(record.terminal_values)
 ck(str(i)+' terminal mapping',record.terminal_values,values)
 ck(str(i)+' metadata',record.seed==42 and record.scenarios==4 and record.up_probability==.25,True)
 ck(str(i)+' controlled draw count',instances[0].index,4)
 for field,want in [('count',4),('mean',expected_mean),('sample_variance',variance),('sample_stddev',math.sqrt(float(variance)))]:ck(str(i)+' '+field,getattr(summary,field),want)
 se=summary.sample_stddev/math.sqrt(4);ck(str(i)+' caller mean SE',se,math.sqrt(float(variance/4)))
 weighted_mean+=float(weight)*summary.mean;weighted_mse+=float(weight)*(summary.mean-87.5)**2;weighted_se2+=float(weight)*se*se
ck('exact path probability mass',mass,1)
ck('weighted native mean',weighted_mean,F(175,2))
ck('exact model variance of mean',weighted_mse,F(1875,16))
ck('weighted native caller SE squared',weighted_se2,F(1875,16))
for seed in [0,7,42]:
 record=simulation.simulate_two_outcome(100.,.25,-.25,.25,4,seed);values=record.terminal_values;up=sum(x==125. for x in values);mean=F(75)+F(50*up,4);variance=F(up)*(125-mean)**2/3+F(4-up)*(75-mean)**2/3;s=statistics.summarize_sample(values)
 ck('native seed'+str(seed)+' support',all(x in [75.,125.] for x in values),True)
 for field,want in [('mean',mean),('sample_variance',variance),('sample_stddev',math.sqrt(float(variance)))]:ck('native seed'+str(seed)+' '+field,getattr(s,field),want)
 ck('native seed'+str(seed)+' caller SE',s.sample_stddev/2,math.sqrt(float(variance/4)))
for p,want in [(0.,75.),(1.,125.)]:
 r=simulation.simulate_two_outcome(100.,.25,-.25,p,4,42);s=statistics.summarize_sample(r.terminal_values);ck('p'+str(p)+' terminals',r.terminal_values,(want,)*4);ck('p'+str(p)+' mean',s.mean,want);ck('p'+str(p)+' variance',s.sample_variance,0)
result=dict(python=platform.python_version(),platform=platform.platform(),rows=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),installed_modules={m.__name__:dict(path=m.__file__,sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for m in [simulation,statistics]},scope='16 finite IID Bernoulli product paths, controlled dependency mapping; actual native runs descriptive; no RNG-distribution or CI/model acceptance')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2,default=str)+'\n');print(result['passed'],result['failed']);assert result['failed']==0
