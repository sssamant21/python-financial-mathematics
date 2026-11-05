"""Independent wide-precision gross-factor and exponential rate references."""
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_19_08 as lab


def rounded(x):
    try:
        y=float(x)
    except OverflowError:
        return 'ValueError'
    return 'ValueError' if not math.isfinite(y) or (x and not y) else y


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    cases=[(tiny,1),(-tiny,1),(tiny,2),(-tiny,2),(tiny,3),(-tiny,3),
           (1e-200,10**1000),(-1e-200,10**1000),
           (.06,12),(-.06,12),(.06,10**1000),
           (big,10**1000),(-big,10**1000),(0.,10**1000),
           (big,1),(1000.,1),(-1000.,1),
           (math.nextafter(-1.,0.),1),(-1.,1),(-2.,1),
           (-big,int(big)+1),(1.,10**309)]
    rows=[]
    with localcontext() as ctx:
        ctx.prec=2200
        for rate,m in cases:
            dr,dm=D(rate),D(m)
            if dr+dm<=0:
                refs=['ValueError']
            else:
                # Log of the independently formed gross factor.
                refs=[rounded(((dm+dr)/dm).ln()*dm)]
            x=dr/dm
            refs.append('ValueError' if x>800 else
                        rounded(-dm if x < -800 else dm*(x.exp()-1)))
            for fn,reference in zip((lab.nominal_to_continuous,lab.continuous_to_nominal),refs):
                try:
                    actual=fn(rate,m)
                except (TypeError,ValueError,OverflowError) as exc:
                    actual=type(exc).__name__
                ok=(isinstance(actual,float) and abs(actual-reference)<=2*math.ulp(reference)
                    and (actual==0)==(reference==0)
                    if isinstance(reference,float) else actual==reference)
                rows.append(dict(helper=fn.__name__,rate=repr(rate),frequency=str(m),
                                 expected=repr(reference),actual=repr(actual),passed=ok))
        for m in (0,-1,True,12.):
            for fn in (lab.nominal_to_continuous,lab.continuous_to_nominal):
                try:
                    fn(.1,m)
                    actual='accepted'
                except (ValueError,TypeError) as exc:
                    actual=type(exc).__name__
                rows.append(dict(helper=fn.__name__,invalid_frequency=repr(m),
                                 expected='ValueError',actual=actual,passed=actual=='ValueError'))
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
