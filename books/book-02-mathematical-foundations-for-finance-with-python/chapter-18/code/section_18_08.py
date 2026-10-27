"""Book 02 Section 18.8: stopping rules and diagnostics lab."""
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

def audited_bisection(function,lower,upper,atol=1e-10,rtol=1e-10,max_iter=100):
    a,b=finite(lower,"lower"),finite(upper,"upper")
    atol,rtol=finite(atol,"atol"),finite(rtol,"rtol")
    if not a<b or atol<=0 or rtol<0:
        raise ValueError("invalid bracket or tolerances")
    if type(max_iter) is not int or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    evaluations=0
    def evaluate(x):
        nonlocal evaluations
        y=finite(function(x),"function value")
        evaluations+=1
        return y
    fa,fb=evaluate(a),evaluate(b)
    def report(root,residual,status,iterations,trace,bracket):
        lo,hi=bracket
        return {"root":root,"bracket":bracket,"width":hi-lo,
                "residual":residual,"status":status,"iterations":iterations,
                "evaluations":evaluations,"atol":atol,"rtol":rtol,
                "max_iter":max_iter,"trace":trace,
                "bracket_invariant":status in
                ("converged","exact_root","endpoint_root","stagnation","max_iter")}
    if fa==0:
        return report(a,0.0,"endpoint_root",0,[],(a,a))
    if fb==0:
        return report(b,0.0,"endpoint_root",0,[],(b,b))
    if not opposite(fa,fb):
        raise ValueError("endpoints must have opposite signs")
    if not math.isfinite(b-a) or not math.isfinite(atol+rtol*max(abs(a),abs(b))):
        raise OverflowError("bracket width or tolerance exceeds float range")
    trace=[]
    for iteration in range(max_iter+1):
        width=b-a
        mid=a+width/2
        if mid==a or mid==b:
            return report(mid,evaluate(mid),"stagnation",iteration,trace,(a,b))
        fm=evaluate(mid)
        trace.append({"iteration":iteration,"lower":a,"upper":b,
                      "midpoint":mid,"width":width,"residual":fm})
        if fm==0:
            return report(mid,0.0,"exact_root",iteration+1,trace,(mid,mid))
        if width<=atol+rtol*max(abs(a),abs(b)):
            return report(mid,fm,"converged",iteration,trace,(a,b))
        if iteration==max_iter:
            return report(mid,fm,"max_iter",iteration,trace,(a,b))
        if opposite(fa,fm):
            b,fb=mid,fm
        else:
            a,fa=mid,fm
    raise AssertionError("unreachable")

def zero_coupon_residual(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return 1000*math.exp(-2*math.log1p(r))-900

def assessment():
    result=audited_bisection(zero_coupon_residual,0,0.2)
    return {"result":result,"analytic_yield":math.sqrt(1000/900)-1,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
