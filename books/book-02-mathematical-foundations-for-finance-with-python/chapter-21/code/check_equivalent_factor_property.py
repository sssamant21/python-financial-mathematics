"""Independent conversion-error propagation for the INT-01 factor comparison."""
from decimal import Context, Decimal as D, localcontext
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv)==2:
    sys.path.insert(0,str(Path(sys.argv[1]).resolve()))
import section_21_03 as cash
import section_21_08 as plan


def allowance(rate,years,converted,left,right):
    # Exact represented effective rate; independent log and exp evaluations.
    with localcontext(Context(prec=1000)):
        c=(1+D(rate)).ln()
        delta=D(converted)-c
        effective=(-(1+D(rate)).ln()*D(years)).exp()
        continuous=(-D(converted)*D(years)).exp()
        propagation=effective*abs((-delta*D(years)).exp()-1)
        bound=propagation + D(math.ulp(left))/2 + D(math.ulp(right))/2
        return c,effective,continuous,delta,bound


def check():
    rows=[]
    def record(name,expected,actual,**details):
        rows.append(dict(case=name,expected=expected,actual=actual,passed=expected==actual,**details))
    policy=next(c for c in plan.make_plan()["cases"] if c["id"]=="INT-01").get("acceptance",{})
    record("INT-01 declares finite nonzero comparison domain",
           "finite converted rate and finite positive factors",policy.get("domain"))
    record("INT-01 declares propagation rather than bit equality",
           "conversion-error propagation plus factor rounding",policy.get("comparison"))
    cases=[
        ("positive long horizon",.25,1000.),
        ("negative long horizon",-.5,1000.),
        ("nearest valid negative rate",math.nextafter(-1.,0.),1.),
        ("largest effective rate",sys.float_info.max,1.),
        ("least positive effective rate",math.ulp(0.),sys.float_info.max),
        ("zero rate",0.,3.),
        ("zero horizon",.25,0.),
        ("fractional horizon",.125,.5),
    ]
    for name,r,t in cases:
        c=cash.to_continuous(r)
        left=cash.discount_factor(r,t,"effective_annual")
        right=cash.discount_factor(c,t,"continuous")
        assert math.isfinite(c) and math.isfinite(left) and math.isfinite(right) and left>0 and right>0
        exact_c,le,ri,delta,bound=allowance(r,t,c,left,right)
        record(name+" selected conversion oracle",float(exact_c).hex(),c.hex())
        record(name+" independent factors",[float(le).hex(),float(ri).hex()],[left.hex(),right.hex()])
        observed=abs(Q(left)-Q(right))
        record(name+" discrepancy within allowance",True,
               observed<=Q(bound),conversion_error=str(delta),absolute_bound=str(bound),
               exact_float_equality=left==right)
    r,t=.25,1000.
    c=cash.to_continuous(r)
    left=cash.discount_factor(r,t,"effective_annual")
    right=cash.discount_factor(c,t,"continuous")
    *_,bound=allowance(r,t,c,left,right)
    corrupted=right*(1+1e-6)
    record("changed factor rejected by original allowance",False,
           abs(Q(left)-Q(corrupted))<=Q(bound))
    record("changed conversion fails independent rate oracle",False,
           c+1e-6==float(allowance(r,t,c,left,right)[0]))
    def outcome(fn,*args):
        try: return fn(*args)
        except Exception as exc: return type(exc).__name__
    record("invalid effective endpoint","ValueError",outcome(cash.to_continuous,-1.))
    record("reverse conversion excluded endpoint","OverflowError",outcome(cash.to_effective,-1000.))
    record("overflowing factors excluded","OverflowError",
           outcome(cash.discount_factor,-.5,2000.,"effective_annual"))
    record("underflowed factor outside positive domain",0.,
           cash.discount_factor(1.,2000.,"effective_annual"))
    record("plan still pending",["not run","pending","pending"],
           [plan.make_plan()[k] for k in ["execution","independent_review","approval"]])
    print(json.dumps(rows,allow_nan=False))
    return all(row["passed"] for row in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
