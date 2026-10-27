"""Book 02 Section 18.4: safeguarded Newton and bisection lab."""
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

def opposite(a,b):
    return (a<0<b) or (b<0<a)

def safeguarded_newton(f,df,lower,upper,atol=1e-12,rtol=1e-12,max_iter=200):
    a,b=finite(lower,"lower"),finite(upper,"upper")
    atol,rtol=finite(atol,"atol"),finite(rtol,"rtol")
    if not a<b or atol<=0 or rtol<0:
        raise ValueError("invalid bracket or tolerances")
    if type(max_iter) is not int or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    fa,fb=finite(f(a),"f(lower)"),finite(f(b),"f(upper)")
    if fa==0 or fb==0:
        root=a if fa==0 else b
        return {"root":root,"bracket":(root,root),"width":0.0,
                "residual":0.0,"iterations":0,"newton_steps":0,
                "bisection_steps":0,"status":"endpoint_root"}
    if not opposite(fa,fb):
        raise ValueError("endpoints must have opposite signs")
    if not math.isfinite(b-a) or not math.isfinite(atol+rtol*max(abs(a),abs(b))):
        raise OverflowError("bracket width or tolerance exceeds float range")
    x=a+(b-a)/2
    newton_steps=bisection_steps=0
    for k in range(max_iter+1):
        width=b-a
        mid=a+width/2
        if mid==a or mid==b:
            return {"root":mid,"bracket":(a,b),"width":width,
                    "residual":finite(f(mid),"f(mid)"),"iterations":k,
                    "newton_steps":newton_steps,
                    "bisection_steps":bisection_steps,"status":"stagnation"}
        if width<=atol+rtol*max(abs(a),abs(b)):
            return {"root":mid,"bracket":(a,b),"width":width,
                    "residual":finite(f(mid),"f(mid)"),"iterations":k,
                    "newton_steps":newton_steps,
                    "bisection_steps":bisection_steps,"status":"converged"}
        if k==max_iter:
            return {"root":mid,"bracket":(a,b),"width":width,
                    "residual":finite(f(mid),"f(mid)"),"iterations":k,
                    "newton_steps":newton_steps,
                    "bisection_steps":bisection_steps,"status":"max_iter"}
        fx=finite(f(x),"f(iterate)")
        if fx==0:
            return {"root":x,"bracket":(x,x),"width":0.0,
                    "residual":0.0,"iterations":k,"newton_steps":newton_steps,
                    "bisection_steps":bisection_steps,"status":"exact_root"}
        deriv=finite(df(x),"df(iterate)")
        proposal=None
        if deriv!=0:
            candidate=x-fx/deriv
            if math.isfinite(candidate) and a+width/4<candidate<b-width/4:
                proposal=candidate
        if proposal is None:
            proposal=mid
            bisection_steps+=1
        else:
            newton_steps+=1
        fp=finite(f(proposal),"f(proposal)")
        if fp==0:
            return {"root":proposal,"bracket":(proposal,proposal),
                    "width":0.0,"residual":0.0,"iterations":k+1,
                    "newton_steps":newton_steps,
                    "bisection_steps":bisection_steps,"status":"exact_root"}
        if opposite(fa,fp):
            b,fb=proposal,fp
        else:
            a,fa=proposal,fp
        x=proposal
    raise AssertionError("unreachable")

def zero_coupon(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return 1000*math.exp(-2*math.log1p(r))-900

def zero_coupon_derivative(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return -2000*math.exp(-2*math.log1p(r))/(1+r)

def npv(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return -1000+1100/(1+r)

def npv_derivative(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return -1100/(1+r)**2

def assessment():
    return {"zero_coupon":safeguarded_newton(zero_coupon,zero_coupon_derivative,0,0.2),
            "zero_coupon_analytic":math.sqrt(1000/900)-1,
            "npv":safeguarded_newton(npv,npv_derivative,0,0.2),
            "npv_analytic":0.1,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
