"""Exact-threshold and reciprocal-log depletion references, not old tiny-rate examples."""
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_19_08 as lab


def check():
    tiny,big=math.ulp(0.),sys.float_info.max
    upper=math.nextafter(1.,2.)
    lower=math.nextafter(math.nextafter(1.,0.),0.)
    cases=[(upper,lower,1.),(1,1,1),(upper,1,1),
           (1000,.04,100),(1000,-.02,50),
           (big,-big,tiny),(1,-big,tiny),(big,-1,big),
           (tiny,big,big),(big,big,big),
           (big,0,tiny),(tiny,0,big),(tiny,0,2),(tiny,0,.5),
           (big,0,big),(0,1,0),(1,1,0),(1,-1,0),
           (1,-1,1),(1,0,1)]
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for a,r,w in cases:
            da,dr,dw=D(a),D(r),D(w)
            if not a:
                expected=0.
            elif not w or (r>0 and dr*da>=dw):
                expected=None
            else:
                reference=da/dw if not r else (dw/(dw-dr*da)).ln()/dr
                expected=float(reference)
                if not math.isfinite(expected) or (reference and not expected):
                    expected='ValueError'
            rows.append(observe((a,r,w),expected))
        for args,error in [((-1,0,1),'ValueError'),((1,0,-1),'ValueError'),
                           ((0,float('nan'),0),'ValueError'),
                           ((True,0,0),'TypeError')]:
            rows.append(observe(args,error))
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


def observe(args,expected):
    try:
        actual=lab.depletion_time(*args)
    except (TypeError,ValueError,OverflowError,ZeroDivisionError) as exc:
        actual=type(exc).__name__
    if isinstance(expected,float):
        passed=(isinstance(actual,float) and math.isfinite(actual)
                and abs(actual-expected)<=3*math.ulp(expected)
                and (actual==0)==(expected==0))
    else:
        passed=actual==expected
    return dict(inputs=repr(args),expected=repr(expected),actual=repr(actual),passed=passed)


if __name__=='__main__':
    check()
