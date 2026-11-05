"""Selected independent complete PV, analytic derivative and Taylor checks."""
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_21_04 as lab
import section_21_09 as integrated


def expected(kind,a,r,t,change=None):
    if not a:
        return 0. if kind=='pv' else (0.,0.)
    discount=(-D(r)*D(t)).exp()
    base=D(a)*discount
    if kind=='pv':
        parts=(base,)
    else:
        first=-D(t)*base
        second=D(t)**2*base
        if kind=='derivatives':
            parts=(first,second)
        else:
            delta=D(change)
            parts=(base+first*delta,base+first*delta+second*delta**2/2)
    rounded=tuple(map(float,parts))
    if not all(map(math.isfinite,rounded)):return 'OverflowError'
    return rounded[0] if kind=='pv' else rounded


def matches(actual,ref):
    if type(actual) is not type(ref):return False
    if type(ref) is tuple:return len(actual)==len(ref) and all(matches(a,b) for a,b in zip(actual,ref))
    if type(ref) is float and ref and actual:
        return math.isfinite(actual) and abs(actual-ref)<=math.ulp(ref)
    return actual==ref


def observe(fn,args,ref):
    try:actual=fn(*args)
    except (TypeError,ValueError,OverflowError) as exc:actual=type(exc).__name__
    return dict(helper=fn.__name__,inputs=repr(args),expected=ref,actual=actual,passed=matches(actual,ref))


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=2500
        for fn,fixtures in [
            (lab.pv,[(m,1,1000.5),(s,-1,1000.5),(0,-m,m),(-m,1,1000.5),
                     (s,1,1000.5),(m,-1,1),(100,-.125,2.5),(100,.1,0)]),
            (lab.derivatives,[(1,1,750),(m,1.1e-305,m),(s,0,m),
                              (-m,1.1e-305,m),(0,-m,m),(1,0,m),
                              (s,-1000,1),(100,-.125,2.5),(-100,.1,0)]),
            (lab.approximations,[(1,0,2.**1023,2.**-1023),(m/4,0,2,1.5),
                                 (-m/4,0,2,1.5),(m,2e-305,m,m),
                                 (0,-m,m,1),(m,0,1,2),(100,0,2,.01),
                                 (1,0,2.**1023,-2.**-1023),(s,-1000,1,0)]),
        ]:
            for args in fixtures:rows.append(observe(fn,args,expected(fn.__name__,*args)))
    for fn,args,error in [(lab.pv,(True,0,0),'TypeError'),
                          (lab.derivatives,(0,float('nan'),0),'ValueError'),
                          (lab.derivatives,(0,0,-1),'ValueError'),
                          (lab.approximations,(0,0,0,True),'TypeError'),
                          (lab.approximations,(0,0,0,float('inf')),'ValueError')]:
        rows.append(observe(fn,args,error))
    report=integrated.build_report()
    actual=report['sensitivity']['first_second']
    rows.append(dict(helper='actual integrated analytic field',expected=(-200.,400.),actual=actual,
                     passed=actual==(-200.,400.) and integrated.derivatives is lab.derivatives
                     and report['validation_execution']=='not run' and report['approval']=='pending'))
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
