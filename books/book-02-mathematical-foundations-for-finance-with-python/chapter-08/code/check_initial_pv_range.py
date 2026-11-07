"""Independent full-price and two-price references for Section 8.1 finance helpers."""
from decimal import Context, Decimal as D, localcontext
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv)==2:
    source_directory=Path(sys.argv[1]).resolve()
    if not (source_directory/"section_8_01.py").is_file():
        raise FileNotFoundError("requested source directory does not contain section_8_01.py")
    sys.path.insert(0,str(source_directory))
import section_8_01 as lab


def oracle(kind,a,r,t,h=None):
    if a==0 or t==0:
        return a if kind=="present_value" else -t*a
    with localcontext(Context(prec=2200)):
        base=D(a)*(-D(r)*D(t)).exp()
        if kind=="present_value": value=base
        elif kind=="present_value_derivative": value=-D(t)*base
        else:
            shifted=D(a)*(-(D(r)+D(h))*D(t)).exp()
            value=(shifted-base)/D(h)
        result=float(value)
    return result if math.isfinite(result) else "ValueError"


def check():
    rows=[]
    def observe(kind,args,want=None,label="numeric"):
        expected=oracle(kind,*args) if want is None else want
        try:
            actual=getattr(lab,kind)(*args)
            if not math.isfinite(actual): actual=repr(actual)
        except Exception as exc: actual=type(exc).__name__
        if type(expected) is float:
            passed=type(actual) is float and (actual==expected if expected==0 or abs(expected)<sys.float_info.min
                    else math.isclose(actual,expected,rel_tol=5e-14,abs_tol=0.))
            if passed and expected==0:
                passed=math.copysign(1,actual)==math.copysign(1,expected)
        else: passed=actual==expected
        rows.append(dict(helper=kind,control=label,expected=expected,actual=actual,passed=passed))
    M=sys.float_info.max
    u=math.ulp(0.)
    for name,args,want in [
        ("present_value",(M,1.,1000.),None),
        ("present_value",(u,-1.,800.),None),
        ("present_value",(0.,-M,M),0.),
        ("present_value",(-0.,-M,M),-0.),
        ("present_value",(M,0.,M),M),
        ("present_value",(1.,-1.,800.),"ValueError"),
        ("present_value",(1.,1.,1000.),0.),
        ("present_value_derivative",(M,1.,1000.),None),
        ("present_value_derivative",(u,-1.,800.),None),
        ("present_value_derivative",(M,0.,1e-308),None),
        ("present_value_derivative",(M,1.,M),-0.),
        ("present_value_derivative",(M,-M,0.),-0.),
        ("present_value_derivative",(M,0.,2.),"ValueError"),
        ("present_value_derivative",(0.,-M,M),-0.),
        ("stable_present_value_difference_quotient",(1000.,0.,u,.5),None),
        ("stable_present_value_difference_quotient",(M,1.,1000.,1e-6),None),
        ("stable_present_value_difference_quotient",(1.,1.,1000.,-1.),None),
        # For the next two huge-horizon cases, shifted rate is exactly zero
        # while the base price is too small to affect final float rounding.
        ("stable_present_value_difference_quotient",(1.,M,M,-M),-float(Q(1)/Q(M))),
        ("stable_present_value_difference_quotient",(M,M,M,-M),-1.),
        ("stable_present_value_difference_quotient",(M,1.,1000.,1.),None),
        ("stable_present_value_difference_quotient",(1.,-1.,1000.,1.),"ValueError"),
        ("stable_present_value_difference_quotient",(1.,0.,0.,M),-0.),
        ("stable_present_value_difference_quotient",(0.,-M,M,1.),-0.),
        ("stable_present_value_difference_quotient",(1000.,.05,3.,1e-6),None),
        ("stable_present_value_difference_quotient",(1000.,.05,3.,-1e-6),None),
    ]:
        observe(name,args,want)
    for name in ("present_value","present_value_derivative","stable_present_value_difference_quotient"):
        tail=(.5,) if name.startswith("stable") else ()
        for args,error,label in [
            ((-1.,.1,1.)+tail,"ValueError","negative amount"),
            ((1.,.1,-1.)+tail,"ValueError","negative horizon"),
            ((True,.1,1.)+tail,"TypeError","bool amount"),
            ((1.,math.nan,1.)+tail,"ValueError","nonfinite rate"),
        ]:
            observe(name,args,error,label)
    for step,error in [(0.,"ValueError"),(True,"TypeError"),(math.inf,"ValueError")]:
        observe("stable_present_value_difference_quotient",(1.,.1,1.,step),error,"invalid step")
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
