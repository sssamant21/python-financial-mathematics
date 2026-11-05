"""Represented-input logistic extremes against reciprocal-coordinate references."""
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_19_02 as lab


def check():
    tiny=math.ulp(0.0);big=sys.float_info.max
    cases=[
        (big,1,tiny,0),(tiny,1,big,0),(big,1,1,0),
        (big,tiny,tiny,tiny),(big,tiny,tiny,1),(tiny,tiny,big,1),
        (tiny,1,big,1),(big,1,tiny,1),(big,1,tiny,1000),
        (tiny,1,big,1000),(tiny,1,big,2000),
        (big,big,tiny,big),(tiny,big,big,big),
        (big,1,big,1),(tiny,1,tiny,1),(0,1,big,1),
        (200,.4,1000,5),(2000,.4,1000,5),(1,tiny,2,tiny),
        (1,1,2,math.nextafter(0.,1.)),
    ]
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for a,r,k,t in cases:
            if a==0 or t==0 or a==k:
                reference=D(a)
            elif D(r)*D(t)>2000:
                reference=D(k)
            else:
                decay=(-D(r)*D(t)).exp()
                reference=1/(1/D(k)+(1/D(a)-1/D(k))*decay)
            expected=float(reference)
            try:
                actual=lab.logistic(a,r,k,t)
            except (ValueError,OverflowError,ZeroDivisionError) as exc:
                actual=type(exc).__name__
            ok=(isinstance(actual,float) and math.isfinite(actual)
                and min(a,k)<=actual<=max(a,k)
                and abs(D(actual)-D(expected))<=2*D(math.ulp(expected))
                and (actual==0)==(a==0))
            rows.append(dict(initial=repr(a),rate=repr(r),capacity=repr(k),years=repr(t),
                             expected=repr(expected),actual=repr(actual),passed=ok))
    for args,error in [((0,0,1,0),'ValueError'),((0,1,0,0),'ValueError'),
                       ((-1,1,1,0),'ValueError'),((1,1,1,-1),'ValueError'),
                       ((True,1,1,0),'TypeError')]:
        try:
            lab.logistic(*args)
            actual='accepted'
        except (TypeError,ValueError) as exc:
            actual=type(exc).__name__
        rows.append(dict(invalid=repr(args),expected=error,actual=actual,passed=actual==error))
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
