"""Book 02 Section 18.3: bracketing and bisection reference lab."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def opposite_signs(a,b):
    return (a<0 and b>0) or (a>0 and b<0)

def bisection(function,lower,upper,atol=1e-12,rtol=1e-12,max_iter=200):
    a,b=finite(lower,"lower"),finite(upper,"upper")
    atol,rtol=finite(atol,"atol"),finite(rtol,"rtol")
    if type(max_iter) is not int or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    if not a<b or atol<=0 or rtol<0:
        raise ValueError("invalid bracket or tolerances")
    fa,fb=finite(function(a),"f(lower)"),finite(function(b),"f(upper)")
    if fa==0:
        return {"root":a,"bracket":(a,a),"width":0.0,
                "residual":0.0,"iterations":0,"status":"endpoint_root"}
    if fb==0:
        return {"root":b,"bracket":(b,b),"width":0.0,
                "residual":0.0,"iterations":0,"status":"endpoint_root"}
    if not opposite_signs(fa,fb):
        raise ValueError("endpoints must have opposite function signs")
    if not math.isfinite(b-a) or not math.isfinite(atol+rtol*max(abs(a),abs(b))):
        raise OverflowError("bracket width or tolerance exceeds float range")
    for iteration in range(max_iter+1):
        midpoint=a+(b-a)/2
        if midpoint==a or midpoint==b:
            return {"root":midpoint,"bracket":(a,b),"width":b-a,
                    "residual":finite(function(midpoint),"f(midpoint)"),
                    "iterations":iteration,"status":"stagnation"}
        fm=finite(function(midpoint),"f(midpoint)")
        if fm==0:
            return {"root":midpoint,"bracket":(midpoint,midpoint),
                    "width":0.0,"residual":0.0,
                    "iterations":iteration+1,"status":"exact_root"}
        if b-a<=atol+rtol*max(abs(a),abs(b)):
            return {"root":midpoint,"bracket":(a,b),"width":b-a,
                    "residual":fm,"iterations":iteration,"status":"converged"}
        if iteration==max_iter:
            return {"root":midpoint,"bracket":(a,b),"width":b-a,
                    "residual":fm,"iterations":iteration,"status":"max_iter"}
        if opposite_signs(fa,fm):
            b,fb=midpoint,fm
        else:
            a,fa=midpoint,fm
    raise AssertionError("unreachable")

def zero_coupon_residual(rate,face=1000.0,price=900.0,years=2.0):
    r=finite(rate,"rate")
    f,p,t=(finite(v,n) for v,n in
           ((face,"face"),(price,"price"),(years,"years")))
    if r<=-1 or f<=0 or p<=0 or t<=0:
        raise ValueError("invalid financial inputs")
    return f*math.exp(-t*math.log1p(r))-p

def npv_residual(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return -1000+1100*math.exp(-math.log1p(r))

def assessment():
    yield_result=bisection(zero_coupon_residual,0,0.2)
    npv_result=bisection(npv_residual,0,0.2)
    return {"yield_solution":yield_result,
            "yield_analytical":math.sqrt(1000/900)-1,
            "yield_initial_signs":(zero_coupon_residual(0),
                                   zero_coupon_residual(0.2)),
            "npv_solution":npv_result,
            "npv_analytical":0.1,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
