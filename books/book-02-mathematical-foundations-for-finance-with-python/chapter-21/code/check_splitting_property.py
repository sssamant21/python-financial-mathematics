"""Check CF-04 against exact represented amounts and independent term references."""
from decimal import Context, Decimal as D, localcontext
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys
if len(sys.argv) == 2:
    sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import section_21_03 as cash
import section_21_08 as plan


def half_ulp(value):
    return Q(math.ulp(value))/2


def reference(amounts, t, rate, convention):
    with localcontext(Context(prec=1000)):
        factor = (-D(rate)*D(t)).exp() if convention=="continuous" else (-(1+D(rate)).ln()*D(t)).exp()
        terms = [float(D(a)*factor) for a in amounts]
        combined = float(sum((D(a) for a in amounts), D(0))*factor)
    if not all(math.isfinite(x) for x in terms) or not math.isfinite(combined):
        return "range exclusion"
    split = float(sum(map(Q,terms),Q(0)))
    if not math.isfinite(split):
        return "range exclusion"
    bound = sum((half_ulp(x) for x in terms),Q(0)) + half_ulp(combined) + half_ulp(split)
    return terms, split, combined, bound


def check():
    rows=[]
    def record(name,expected,actual,**details):
        rows.append(dict(case=name,expected=expected,actual=actual,passed=expected==actual,**details))
    policy = next(c for c in plan.make_plan()["cases"] if c["id"]=="CF-04").get("acceptance",{})
    record("CF-04 declares represented-amount identity", True,
           policy.get("amount_identity")=="exact sum of normalized split floats equals merged float")
    record("CF-04 declares comparison and range scope", 
           ["absolute rounding bound","each discounted term and final value finite"],
           [policy.get("comparison"),policy.get("range_scope")])
    u=math.ulp(0.)
    fixtures=[
        ("subnormal continuous",[u,u],1.,1.,"continuous"),
        ("subnormal effective",[u,u],1.,2.,"effective_annual"),
        ("cancellation continuous",[float(2**52),-float(2**52)+1.],1.,.1,"continuous"),
        ("cancellation effective",[float(2**52),-float(2**52)+1.],1.,.1,"effective_annual"),
        ("signed dyadic split",[-.25,-.75],2.,-.2,"continuous"),
        ("three payments",[.25,.25,.5],.5,.25,"effective_annual"),
        ("zero-date cancellation",[float(2**52),-float(2**52)+1.],0.,.1,"continuous"),
        ("zero-rate signed split",[-.25,-.75],3.,0.,"continuous"),
    ]
    for name, amounts,t,r,c in fixtures:
        merged=float(sum(map(Q,amounts),Q(0)))
        assert sum(map(Q,amounts),Q(0))==Q(merged)
        expected=reference(amounts,t,r,c)
        assert expected!="range exclusion"
        terms,split,whole,bound=expected
        actual_split=cash.present_value([(a,t) for a in amounts],r,c)
        actual_whole=cash.present_value([(merged,t)],r,c)
        residual=abs(Q(actual_split)-Q(actual_whole))
        record(name+" independent rounded-term oracle",[split,whole],[actual_split,actual_whole],
               split_hex=actual_split.hex(),merged_hex=actual_whole.hex())
        record(name+" property within rounding bound",True,residual<=bound,
               absolute_residual=str(residual),absolute_bound=str(bound),
               exact_float_equality=actual_split==actual_whole)
    M=sys.float_info.max
    try:
        cash.present_value([(M,1.),(-M,1.)],-1.,"continuous")
    except OverflowError:
        actual="range exclusion"
    else:
        actual="returned"
    record("unrepresentable individual term excludes property comparison","range exclusion",actual)
    record("merged cancelling amount still valid",0.,cash.present_value([(0.,1.)],-1.,"continuous"))
    # This also establishes why a fixed ordinary-scale tolerance is insufficient.
    _, split, whole, bound=reference(fixtures[2][1],1.,.1,"continuous")
    record("finite cancellation exceeds old fixed tolerance",False,
           math.isclose(split,whole,rel_tol=1e-12,abs_tol=1e-9))
    record("altered result is rejected by same bound",False,
           abs(Q(split)+100-Q(whole))<=bound)
    flags=plan.make_plan()
    record("plan stays pending",["not run","pending","pending"],
           [flags[k] for k in ["execution","independent_review","approval"]])
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
