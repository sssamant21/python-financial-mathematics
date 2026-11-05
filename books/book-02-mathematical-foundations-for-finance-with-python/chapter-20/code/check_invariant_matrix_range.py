"""Complete quadratic and feasibility checks at represented-input boundaries."""
from decimal import Decimal, localcontext
import json
import math
import sys
import section_20_03 as lab


def quadratic_reference(args):
    with localcontext() as ctx:
        ctx.prec=4000
        a,b,c,d,x,y=map(Decimal,args)
        value=x*(a*x+b*y)+y*(c*x+d*y)
        f=float(value)
        return f if math.isfinite(f) and (f or not value) else 'ValueError'


def feasible_reference(weights,tol):
    ratios=[float(x).as_integer_ratio() for x in [*weights,tol]]
    scale=max(d for _,d in ratios)
    *w,bound=[n*(scale//d) for n,d in ratios]
    return min(w)>=-bound and scale-bound<=sum(w)<=scale+bound


def observe(fn,args,expected):
    try:
        actual=fn(*args)
    except (TypeError,ValueError,OverflowError) as exc:
        actual=type(exc).__name__
    passed=type(actual) is type(expected) and actual==expected
    return dict(helper=fn.__name__,inputs=repr(args),expected=expected,actual=actual,passed=passed)


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    rows=[]
    for args in [(m,m,m,m,1e-154,1e-154),(m,m,m,m,1,-1),
                 (m,m,m,m,0,0),(0,m,m,0,s,1),(0,m,-m,0,m,m),
                 (m,0,0,-m,2,2),(s,0,0,0,.5,0),(m,0,0,0,2,0),
                 (-m,0,0,0,2,0),(1,2,2,1,1,-1),(2,3,-1,2,2,3),
                 (s,0,0,0,1,0),(0,1,0,0,1,-1)]:
        rows.append(observe(lab.covariance_quadratic_2x2,args,quadratic_reference(args)))
    for w,tol in [([1,s],0),([1,-s],s),([1,s],s),([1,2*s],s),
                  ([m,m],0),([m,m],m),([m,m,-m,-m,1],m),
                  ([.5,.5],0),([.4,.6],0),([.1,.9],0),([1.125],.125),
                  ([.875],.125),([math.nextafter(1.125,2.)],.125),
                  ([-.125,1.125],.125),([-math.nextafter(.125,1.),1.125],.125)]:
        rows.append(observe(lab.portfolio_feasible,(w,tol),feasible_reference(w,tol)))
    for fn,args,error in [(lab.covariance_quadratic_2x2,(True,0,0,0,0,0),'TypeError'),
                          (lab.covariance_quadratic_2x2,(1,0,0,1,0,float('nan')),'ValueError'),
                          (lab.portfolio_feasible,([],0),'ValueError'),
                          (lab.portfolio_feasible,([1],-s),'ValueError'),
                          (lab.portfolio_feasible,([True],0),'TypeError'),
                          (lab.portfolio_feasible,([1],float('inf')),'ValueError')]:
        rows.append(observe(fn,args,error))
    report=lab.assessment()
    assert report['runtime_certified'] is False and report['independent_review_completed'] is False
    for key,expected in [('portfolio_feasible',True),('indefinite_matrix_quadratic',-2.)]:
        actual=report[key]
        rows.append(dict(helper='assessment.'+key,expected=expected,actual=actual,
                         passed=type(actual) is type(expected) and actual==expected))
    calls=[]
    old_q,old_p=lab.covariance_quadratic_2x2,lab.portfolio_feasible
    def q(*args):
        calls.append(('quadratic',args));return 17.
    def p(*args):
        calls.append(('portfolio',args));return False
    lab.covariance_quadratic_2x2,lab.portfolio_feasible=q,p
    try:report=lab.assessment()
    finally:lab.covariance_quadratic_2x2,lab.portfolio_feasible=old_q,old_p
    assert calls==[('portfolio',([.4,.6],)),('quadratic',(1,2,2,1,1,-1))]
    assert report['portfolio_feasible'] is False and report['indefinite_matrix_quadratic']==17.
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
