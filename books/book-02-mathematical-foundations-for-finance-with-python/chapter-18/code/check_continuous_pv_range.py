"""Independent high-precision continuous-stream PV range references."""
from decimal import Decimal as D, localcontext
import json
import math
import section_18_07 as lab


def reference(c,r,t):
    with localcontext() as ctx:
        ctx.prec=2500
        c,r,t=map(D.from_float,map(float,(c,r,t)))
        if c==0 or t==0:return D(0)
        if r==0:return c*t
        x=-r*t
        if x < -D(20000):return c/r
        return -c*(x.exp()-1)/r


def rejects(error,fn,*args):
    try:fn(*args)
    except error:return
    raise AssertionError('expected '+error.__name__)


def check():
    tiny=math.nextafter(0.0,1.0);threshold=2**-26
    cases=((1e308,-4.0,0.5),(1.0,tiny,1.5),(1.0,1e-308,1e-308),
           (1e308,1e-308,1e-308),(100.0,0.03,5.0),(100.0,0.0,5.0),
           (0.0,-1000.0,1.0),(1.0,-1000.0,0.0),(1e-308,-1000.0,1.0),
           (1.0,-1e308,1e-305),(1e-300,-700.0,1.0),(1.0,1e308,1.0),
           (tiny,0.0,1.0),(1e308,0.0,0.5),(1.0,threshold,1.0),
           (1.0,-threshold,1.0),(1.0,math.nextafter(threshold,math.inf),1.0),
           (0.0,-1e308,1e308))
    records=[]
    for c,r,t in cases:
        expected=reference(c,r,t);actual=lab.continuous_cashflow_pv(c,r,t)
        rounded=float(expected)
        assert math.isfinite(actual)
        assert (actual==0)==(expected==0)
        if abs(rounded)<2**-1022:
            assert actual==rounded
        else:
            # The log-growth branch is approximate binary64, not a globally
            # correctly-rounded transcendental contract. Retain its allowance.
            logarithmic=r<0 and -r*t>709
            budget=max(16*math.ulp(rounded),abs(rounded)*(2e-12 if logarithmic else 2e-15))
            assert abs(actual-rounded)<=budget,(c,r,t,actual,rounded,budget)
        records.append({'cashflow_rate':c,'discount_rate':r,'years':t,'actual':actual,
                        'decimal_reference':str(expected),'rounded_reference':rounded})
    ranges=((1.0,-1000.0,1.0),(1e308,0.0,2.0),(tiny,1e308,1.0),
            (tiny,0.0,0.25),(1.0,-1e308,1e308))
    for args in ranges:rejects(ValueError,lab.continuous_cashflow_pv,*args)
    invalid=((0.0,math.nan,1.0,ValueError),(1.0,math.inf,0.0,ValueError),
             (False,0.0,1.0,TypeError),(-1.0,0.0,1.0,ValueError),(1.0,0.0,-1.0,ValueError))
    for c,r,t,error in invalid:rejects(error,lab.continuous_cashflow_pv,c,r,t)
    return {'complete_pv_references':records,'final_range_rejections':len(ranges),
            'invalid_inputs_before_zero_shortcuts':len(invalid),
            'scope':'selected constant continuous streams; log branch uses explicit relative allowance, not exact rounding'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
