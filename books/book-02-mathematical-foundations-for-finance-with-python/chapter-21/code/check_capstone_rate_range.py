"""Independent effective gross powers, conversion boundaries and cash-flow totals."""
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_21_03 as lab
import section_21_09 as integrated

E='effective_annual'
C='continuous'


def rounded(x):
    f=float(x)
    return f if math.isfinite(f) else 'OverflowError'


def term(a,r,t,mode):
    if not a:return 0.
    if mode==E:
        # Selected effective fixtures use finite Decimal powers directly.
        f=(D(1)+D(r))**(-D(t))
    else:
        x=-D(r)*D(t)
        if x>2000:return 'OverflowError'
        if x<-2000:return math.copysign(0.,a)
        f=x.exp()
    return rounded(D(a)*f)


def portfolio(flows,r,mode):
    terms=[term(a,r,t,mode) for a,t in flows]
    if 'OverflowError' in terms:return 'OverflowError'
    return rounded(sum(map(D,terms),D(0)))


def observe(fn,args,expected):
    try:actual=fn(*args)
    except (ValueError,TypeError,OverflowError) as exc:actual=type(exc).__name__
    passed=type(actual) is type(expected) and actual==expected
    if type(expected) is float and type(actual) is float and expected and actual:
        passed=math.isfinite(actual) and abs(actual-expected)<=math.ulp(expected)
    return dict(helper=fn.__name__,inputs=repr(args),expected=expected,actual=actual,passed=passed)


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    near=math.nextafter(-1.,0.)
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for r,t,mode in [(3,.5,E),(-.75,.5,E),(.25,2.5,E),(near,.5,E),
                         (s,m,E),(2**-54,2**54,E),(m,.25,E),(m,2,C),
                         (-m,2,C),(-1.25,.75,C),(near,21.5,E),
                         (near,0,E),(0,2.5,E)]:
            rows.append(observe(lab.discount_factor,(r,t,mode),term(1,r,t,mode)))
        flows=[
            ([(s,21.5),(-s,20.5)],near,E),
            ([(0,21.5)],near,E),
            ([(m,1075.5)],1,E),
            ([(m,1024.5),(-m/2,1024.5)],1,E),
            ([(7,.5),(-3,1.5),(11,2.25)],-.75,E),
            ([(11,2.25),(-3,1.5),(7,.5)],-.75,E),
            ([(m,1),(m,1),(-m,1),(s,1)],0,E),
            ([(m,0),(m,0)],0,E),
            ([(m,21.5),(-m,21.5)],near,E),
            ([(0,2)],-m,C),
            ([(m,1000.5)],1,C),
            ([(s,1000.5)],-1,C),
            ([(s,1000.5)],1,C),
            ([(m,2)],-m,C),
            ([(1,.5)],s,E),
            ([],near,E),
        ]
        for f,r,mode in flows:rows.append(observe(lab.present_value,(f,r,mode),portfolio(f,r,mode)))
        for r in [near,-.75,-s,s,.25,m]:
            rows.append(observe(lab.to_continuous,(r,),rounded((1+D(r)).ln())))
        pivot=float(-54*D(2).ln())
        for r in [math.nextafter(pivot,-math.inf),pivot,math.nextafter(pivot,math.inf),
                  -1000.,-2.,-s,s,1.,710.]:
            expected=rounded(D(r).exp()-1)
            if expected==-1.:expected='OverflowError'
            rows.append(observe(lab.to_effective,(r,),expected))
        report=integrated.build_report()
        value=report['cash_flow']['value']
        expected=portfolio([(100,1)],math.log(2),C)
        rows.append(dict(helper='actual capstone cash-flow field',expected=expected,actual=value,
                         passed=value==expected and integrated.present_value is lab.present_value
                         and report['validation_execution']=='not run'
                         and report['approval']=='pending'))
    for fn,args,error in [(lab.present_value,([],True,E),'TypeError'),
                          (lab.present_value,([],-1,E),'ValueError'),
                          (lab.present_value,([],0,'nominal'),'ValueError'),
                          (lab.present_value,([(0,-1)],0,C),'ValueError'),
                          (lab.present_value,([(0,True)],0,E),'TypeError'),
                          (lab.discount_factor,(float('nan'),0,E),'ValueError'),
                          (lab.to_continuous,(-1,),'ValueError'),
                          (lab.to_effective,(True,),'TypeError')]:
        rows.append(observe(fn,args,error))
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
