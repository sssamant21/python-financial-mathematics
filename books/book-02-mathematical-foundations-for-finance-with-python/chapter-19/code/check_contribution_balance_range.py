"""Independent integrals and separately accumulated payment references."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import sys
import section_19_08 as lab


def rounded(value):
    result=float(value)
    return 'ValueError' if not math.isfinite(result) or (value and not result) else result


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    continuous=[(1000,.04,200,5),(1000,-.04,-200,5),
                (tiny,1000,0,1),(big,-1000,0,1),(0,1000,tiny,1),
                (1,1000,-1000,1),(1,big,-big,1),
                (0,big,0,big),(big,0,-big,2),(1,0,-1,1),
                (0,tiny,big,tiny),(tiny,-2,tiny,5e307),
                (0,-2,tiny,5e307),(0,0,tiny,tiny),(big,0,big,1)]
    end=[(1000,.04,200,5,12),(1000,-.04,-200,5,12),
         (tiny,1000,0,1,2),(0,1000,tiny,1,2),
         (big,-1000,0,1,2),(big,0,-big,2,2),
         (1,0,-1,1,12),(0,0,tiny,tiny,2),
         (0,big,0,0,1),(0,.04,200,5,10**1000)]
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for a,r,u,t in continuous:
            x=D(r)*D(t)
            if r==0:
                ref=D(a)+D(u)*D(t)
            elif F(a)+F(u)/F(r)==0:
                ref=D(a)
            elif x < -4000:
                # Explicit half-subnormal tie controls: sign of the decaying
                # coefficient determines the side of the limiting midpoint.
                ref=D(tiny) if a==tiny else D(0)
                if a==0:
                    expected='ValueError'
            else:
                ref=D(a)*x.exp()+D(u)*((x.exp()-1)/D(r))
            expected=('ValueError' if (a==0 and r==-2 and t>1e300) else rounded(ref))
            rows.append(observe(lab.continuous_contributions,(a,r,u,t),expected))
        for a,r,u,t,n in end:
            if not t or not r:
                ref=D(a)+D(u)*D(t)
            elif n>1000:
                # End-period gap is below rounding at this selected frequency.
                x=D(r)*D(t)
                ref=D(a)*x.exp()+D(u)*(x.exp()-1)/D(r)
            else:
                h=D(t)/n
                ref=D(a)*(D(r)*D(t)).exp()+sum(
                    (D(u)*h*(D(r)*(D(t)-k*h)).exp() for k in range(1,n+1)),D(0))
            rows.append(observe(lab.end_period_contributions,(a,r,u,t,n),rounded(ref)))
        # At continuous equilibrium, end-period timing adds
        # approximately exp(4000)*2000/n. For these two n values this
        # is respectively beyond float range or below the rounding of 1.
        rows.append(observe(lab.end_period_contributions,
                            (1,4000,-4000,1,10**1200),'ValueError'))
        rows.append(observe(lab.end_period_contributions,
                            (1,4000,-4000,1,10**2000),1.0))
        rows.append(observe(lab.end_period_contributions,(0,5000,0,1,2),0.0))
        # Explicit educational evaluation limit, not mathematical overflow.
        rows.append(observe(lab.end_period_contributions,
                            (1,5001,-5001,1,10**2000),'ValueError'))
        for fn,args in [(lab.continuous_contributions,(0,float('inf'),0,0)),
                        (lab.continuous_contributions,(0,0,0,-1)),
                        (lab.end_period_contributions,(0,0,0,0,0)),
                        (lab.end_period_contributions,(0,0,0,0,True))]:
            rows.append(observe(fn,args,'ValueError'))
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


def observe(fn,args,expected):
    try:
        actual=fn(*args)
    except (TypeError,ValueError,OverflowError,ZeroDivisionError) as exc:
        actual=type(exc).__name__
    passed=(isinstance(actual,float) and math.isfinite(actual)
            and abs(actual-expected)<=4*math.ulp(expected)
            and (actual==0)==(expected==0)
            if isinstance(expected,float) else actual==expected)
    return dict(helper=fn.__name__,args=repr(args),expected=repr(expected),
                actual=repr(actual),passed=passed)


if __name__=='__main__':
    check()
