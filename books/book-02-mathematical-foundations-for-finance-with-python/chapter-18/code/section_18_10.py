"""Book 02 Section 18.10: Chapter 18 applied exercises and reference calculations."""
import json
import math
from section_18_07 import central_difference as _shared_central_difference
import section_18_06 as interpolation_lab
import section_18_09 as solver_project

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        y=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} out of range") from exc
    if not math.isfinite(y):
        raise ValueError(f"{name} must be finite")
    return y

def zero_price(r,face=1000.0,years=2.0):
    r,face,years=finite(r,"rate"),finite(face,"face"),finite(years,"years")
    if r<=-1 or face<=0 or years<=0:
        raise ValueError("invalid zero-coupon inputs")
    return finite(face*math.exp(-years*math.log1p(r)),"price")

def npv(rate,flows):
    r=finite(rate,"rate")
    if r<=-1 or not isinstance(flows,(tuple,list)) or not flows:
        raise ValueError("invalid rate or cash flows")
    values=[finite(x,"cash flow") for x in flows]
    z=math.exp(-math.log1p(r))
    return finite(math.fsum(c*z**i for i,c in enumerate(values)),"NPV")

def bisect(f,a,b,tol=1e-12,max_iter=200):
    a,b,tol=finite(a,"lower"),finite(b,"upper"),finite(tol,"tolerance")
    if not a<b or tol<=0 or type(max_iter) is not int or max_iter<1:
        raise ValueError("invalid solver controls")
    fa,fb=finite(f(a),"f(lower)"),finite(f(b),"f(upper)")
    if fa==0:
        return {"root":a,"bracket":(a,a),"status":"endpoint_root","iterations":0}
    if fb==0:
        return {"root":b,"bracket":(b,b),"status":"endpoint_root","iterations":0}
    if not ((fa<0<fb) or (fb<0<fa)):
        raise ValueError("no sign change")
    if not math.isfinite(b-a):
        raise OverflowError("bracket width exceeds float range")
    for k in range(max_iter+1):
        m=a+(b-a)/2
        if m==a or m==b:
            return {"root":m,"bracket":(a,b),"status":"stagnation","iterations":k}
        fm=finite(f(m),"f(mid)")
        if fm==0:
            return {"root":m,"bracket":(m,m),"status":"exact_root","iterations":k+1}
        if b-a<=tol:
            return {"root":m,"bracket":(a,b),"status":"converged","iterations":k}
        if k==max_iter:
            return {"root":m,"bracket":(a,b),"status":"max_iter","iterations":k}
        if (fa<0<fm) or (fm<0<fa):
            b,fb=m,fm
        else:
            a,fa=m,fm
    raise AssertionError("unreachable")

def interpolate(x0,y0,x1,y1,x):
    x0,y0,x1,y1,x=(finite(v,"interpolation input") for v in (x0,y0,x1,y1,x))
    if x0>=x1:
        raise ValueError("knots must increase")
    return y0+(x-x0)*(y1-y0)/(x1-x0)

def central_derivative(f,x,h):
    return _shared_central_difference(f,x,h)

def simpson(f,a,b,n):
    a,b=finite(a,"lower"),finite(b,"upper")
    if b<=a or type(n) is not int or n<2 or n%2:
        raise ValueError("Simpson requires positive even panels")
    h=(b-a)/n
    terms=[finite(f(a),"f(a)"),finite(f(b),"f(b)")]
    terms.extend((4 if i%2 else 2)*finite(f(a+i*h),"integrand") for i in range(1,n))
    return finite(h*math.fsum(terms)/3,"integral")

def solver_comparison():
    calls=0
    def objective(rate):
        nonlocal calls
        calls+=1
        return zero_price(rate)-900
    bisection=bisect(objective,0.0,0.2,tol=1e-12,max_iter=200)
    safeguarded=solver_project.solve(solver_project.zero_coupon,solver_project.zero_coupon_derivative,
                                     0.0,0.2,atol=1e-12,rtol=0.0,max_iter=200)
    return {"bisection":bisection,"safeguarded_newton":safeguarded,
            "bisection_width":bisection["bracket"][1]-bisection["bracket"][0],
            "bisection_residual":zero_price(bisection["root"])-900,
            "bisection_function_evaluations":calls,"bisection_residual_evaluations":1,
            "initial_bracket":(0.0,0.2),"absolute_width_tolerance":1e-12,
            "model":"face1000,price900,maturity2; annual effective rate",
            "count_convention":"solver calls; separate bisection residual verification"}

def assessment():
    yield_reference=math.sqrt(10/9)-1
    comparison=solver_comparison()
    solved=comparison["bisection"]
    two_irrs=(bisect(lambda r:npv(r,(-100,230,-132)),0,0.15),
              bisect(lambda r:npv(r,(-100,230,-132)),0.15,0.3))
    curve=interpolation_lab.financial_comparison()
    rate=curve["rate_midpoint"]
    derivative=central_derivative(lambda r:zero_price(r),0.05,1e-4)
    pv=simpson(lambda t:100*math.exp(-0.03*t),0,5,40)
    return {"yield_reference":yield_reference,"yield_solution":solved,
            "solver_comparison":comparison,"interpolation_comparison":curve,
            "multiple_irr_solutions":two_irrs,
            "rate_interpolation":rate,
            "discount_interpolation":curve["discount_linear"],
            "discount_log_interpolation":curve["discount_log_linear"],
            "discount_from_rate_interpolation":curve["discount_from_rate"],
            "duration_estimate":-derivative/zero_price(0.05),
            "duration_reference":2/1.05,
            "simpson_continuous_pv":pv,
            "continuous_pv_reference":-100*math.expm1(-0.15)/0.03,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
