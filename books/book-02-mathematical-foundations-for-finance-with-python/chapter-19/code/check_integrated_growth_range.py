"""Exact integrated-rate and independent Decimal scaled-exponential oracles."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_19_02 as lab


def expected(initial,integral):
    if initial==0 or integral==0:
        return float(initial)
    if abs(integral)>2000:
        return 'ValueError'
    with localcontext() as ctx:
        ctx.prec=1600
        exponent=D(integral.numerator)/D(integral.denominator)
        ref=D(initial)*exponent.exp()
        result=float(ref)
        return 'ValueError' if not math.isfinite(result) or not result else result


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    rows=[]
    def compare(fn,args,ref):
        try:
            actual=fn(*args)
        except (ValueError,OverflowError,ZeroDivisionError,TypeError) as exc:
            actual=type(exc).__name__
        ok=(abs(actual-ref)<=2*math.ulp(ref) and (actual==0)==(ref==0)
            if isinstance(actual,float) and isinstance(ref,float) else actual==ref)
        rows.append(dict(helper=fn.__name__,args=repr(args),expected=repr(ref),
                         actual=repr(actual),passed=ok))
    for a,r,t in [(tiny,1000,1),(big,-1000,1),(1,-1000,1),(1,1000,1),
                  (0,big,big),(1,big,0),(-tiny,1000,1),(-big,-1000,1),
                  (1000,.04,3),(big,tiny,1),(tiny,tiny,tiny),(1,tiny,big)]:
        compare(lab.growth,(a,r,t),expected(a,F(r)*F(t)))
    for a,base,slope,t in [
        (1,-big,big,2),(1,big,-big,2),
        (1,-big,math.nextafter(big,0),2),
        (tiny,1000,0,1),(big,-1000,0,1),
        (0,big,big,big),(1,big,big,0),
        (1000,.03,.002,5),(1,1e200,-2e100,1e100),
        (1,0,tiny,tiny)]:
        # Trapezoidal integration of the affine rate is exact.
        integral=F(t)*(F(base)+(F(base)+F(slope)*F(t)))/2
        compare(lab.variable_growth,(a,base,slope,t),expected(a,integral))
    for a,r,w,t in [(1,-big,big,0),(0,-big,big,big),(tiny,1000,0,1),
                    (big,0,1000,1),(1000,.04,.06,5),(1,big,big,big),
                    (1,-big,big,tiny),(tiny,big,math.nextafter(big,0),tiny)]:
        integral=F(r)*F(t)-F(w)*F(t)
        compare(lab.proportional_withdrawals,(a,r,w,t),expected(a,integral))
    for fn,args,error in [(lab.growth,(0,float('inf'),0),'ValueError'),
                          (lab.growth,(1,0,-1),'ValueError'),
                          (lab.variable_growth,(0,0,0,-1),'ValueError'),
                          (lab.variable_growth,(True,0,0,0),'TypeError'),
                          (lab.proportional_withdrawals,(-1,0,0,0),'ValueError'),
                          (lab.proportional_withdrawals,(0,0,-1,0),'ValueError')]:
        compare(fn,args,error)
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
