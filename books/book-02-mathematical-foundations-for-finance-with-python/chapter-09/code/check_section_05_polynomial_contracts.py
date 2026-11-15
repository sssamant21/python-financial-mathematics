"""Exact rational whole-polynomial oracles;no tolerance widening."""
from fractions import Fraction
from pathlib import Path
import math,json,sys,hashlib
from decimal import Decimal
import section_9_05 as m
FIELDS=('exact','linear','quadratic','quadratic_remainder','quadratic_bound')
VALUES=[0.,-0.,.1,-.1,1.,-1.,-2.,math.nextafter(-2.,0.),math.nextafter(-2.,-math.inf),-2/3,math.nextafter(-2/3,0.),math.ulp(2.)/2,2**-55,1e-110,-1e-110,1e100,-1e100,1e103,-1e103,1e308,-1e308,2]
rows=[]
for index,h in enumerate(VALUES):
 H=Fraction(float(h));exact=((2+H)**3,8+12*H,8+12*H+6*H*H,H**3,abs(H)**3)
 try:want=tuple(float(x) for x in exact);want=want if all(math.isfinite(x) for x in want) else 'ValueError'
 except OverflowError:want='ValueError'
 try:a=m.polynomial_example(h)
 except Exception as e:a=type(e).__name__
 for i,k in enumerate(FIELDS):
  expected=want if isinstance(want,str) else want[i];got=a if isinstance(a,str) else a[k]
  # Declared single-rounding report contract:exact binary64 comparison.
  passed=got==expected and (isinstance(expected,str) or math.copysign(1.,got)==math.copysign(1.,expected) or expected!=0)
  rows.append(dict(case=str(index),shock=repr(h),field=k,actual=repr(got),expected=repr(expected),comparison='exact rounded rational;exact mathematical zero reports positive zero',passed=passed))
for label,h,expected in [('bool',True,'TypeError'),('Decimal',Decimal('.1'),'TypeError'),('text','.1','TypeError'),('None',None,'TypeError'),('nan',math.nan,'ValueError'),('inf',math.inf,'ValueError'),('oversized integer',10**1000,'ValueError')]:
 try:a=m.polynomial_example(h)
 except Exception as e:a=type(e).__name__
 rows.append(dict(case=label,actual=repr(a),expected=expected,passed=a==expected))
H=Fraction(1,10);supplemental=[dict(name='exercise cubic exact',passed=(2+H)**3==Fraction(9261,1000)),dict(name='exercise first remainder bound',passed=Fraction(61,1000)<=Fraction(63,1000)),dict(name='exercise quadratic remainder bound',passed=H**3==Fraction(1,1000))]
d=dict(source_blob=hashlib.sha1(b'blob '+str(len(Path(m.__file__).read_bytes())).encode()+b'\0'+Path(m.__file__).read_bytes()).hexdigest(),source_predicates=rows,oracle_controls=supplemental,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),limits='Polynomial report only;declared complete single-rounding/positive exact-zero/finite whole-report policy. Supplemental exact-decimal exercise arithmetic separate from represented-float source references. Financialremainder/range/resources/platform/independent acceptance remain scoped.')
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(dict(source_predicates=len(rows),passed=d['passed'],failed=d['failed'],supplemental_controls=len(supplemental))))
assert d['failed']==0 and all(x['passed'] for x in supplemental)
