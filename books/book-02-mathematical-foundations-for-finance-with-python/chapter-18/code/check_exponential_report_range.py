"""Independent Decimal and rational references for Section 18.1 reports."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import section_18_01 as lab


def check():
    rows = []

    def observe(fn,x,expected,verify=None):
        try:
            actual=fn(x)
        except (TypeError,ValueError,OverflowError) as exc:
            actual=type(exc).__name__
        passed=verify(actual) if isinstance(actual,dict) and verify else actual==expected
        rows.append(dict(helper=fn.__name__,x=repr(x),expected=expected,
                         actual=actual,passed=passed))

    with localcontext() as ctx:
        ctx.prec=900
        for x in (-800.,-746.,-745.,-710.,-704.,-54.,-37.,-1.,-2**-54,
                  -math.ulp(0.),0.,math.ulp(0.),2**-54,1.,709.,709.78,710.,800.):
            dx=D(x)
            er=dx.exp()
            exp_ref=float(er)
            stable_ref=float(er-1)
            linear=float(1+dx)
            if not math.isfinite(exp_ref) or exp_ref==0:
                observe(lab.exponential_approximation,x,'ValueError')
            else:
                delta=abs(F(linear)-F(exp_ref))
                try:
                    rel=float(delta/F(exp_ref))
                except OverflowError:
                    rel=math.inf
                if not math.isfinite(rel):
                    observe(lab.exponential_approximation,x,'ValueError')
                else:
                    def approx(a):
                        ref=a['exact']
                        diff=abs(F(linear)-F(ref))
                        return (abs(ref-exp_ref)<=math.ulp(exp_ref)
                                and a['first_order']==linear
                                and a['error']==dict(absolute=float(diff),
                                                     relative=float(diff/F(ref))))
                    observe(lab.exponential_approximation,x,'finite approximation',approx)
            if not math.isfinite(stable_ref):
                observe(lab.cancellation_demo,x,'ValueError')
            else:
                def cancellation(a):
                    direct=exp_ref-1
                    return (a['x']==x
                            and abs(a['direct']-direct)<=math.ulp(exp_ref)
                            and abs(a['stable']-stable_ref)<=math.ulp(stable_ref)
                            and (a['stable']==0)==(stable_ref==0)
                            and (stable_ref!=-1 or a['stable']==-1)
                            and (exp_ref!=1 or a['direct']==0))
                observe(lab.cancellation_demo,x,'finite cancellation report',cancellation)
    for fn in (lab.exponential_approximation,lab.cancellation_demo):
        for x,expected in [(True,'TypeError'),(float('nan'),'ValueError'),
                           (float('inf'),'ValueError'),(1e308,'ValueError')]:
            observe(fn,x,expected)
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
