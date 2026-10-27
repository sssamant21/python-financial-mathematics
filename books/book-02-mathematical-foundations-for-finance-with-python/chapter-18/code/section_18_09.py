"""Book 02 Section 18.9: financial numerical solver and diagnostics."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def opposite(a,b):
    return (a<0<b) or (b<0<a)

def solve(f,df,lower,upper,atol=1e-12,rtol=1e-12,max_iter=200):
    a,b=finite(lower,"lower"),finite(upper,"upper")
    atol,rtol=finite(atol,"atol"),finite(rtol,"rtol")
    if a>=b or atol<=0 or rtol<0:
        raise ValueError("invalid bracket or tolerances")
    if type(max_iter) is not int or max_iter<1:
        raise ValueError("max_iter must be a positive integer")
    f_calls=d_calls=newton=bisection=0
    trace=[]
    def evaluate(x):
        nonlocal f_calls
        result=finite(f(x),"function value")
        f_calls+=1
        return result
    def derivative(x):
        nonlocal d_calls
        result=finite(df(x),"derivative value")
        d_calls+=1
        return result
    def report(root,residual,status,k,bracket):
        lo,hi=bracket
        return {"root":root,"bracket":bracket,"width":hi-lo,
                "residual":residual,"status":status,"iterations":k,
                "function_evaluations":f_calls,
                "derivative_evaluations":d_calls,
                "newton_steps":newton,"bisection_steps":bisection,
                "tolerances":{"atol":atol,"rtol":rtol},
                "max_iter":max_iter,"trace":trace,
                "runtime_certified":False}
    fa,fb=evaluate(a),evaluate(b)
    if fa==0:
        return report(a,0.0,"endpoint_root",0,(a,a))
    if fb==0:
        return report(b,0.0,"endpoint_root",0,(b,b))
    if not opposite(fa,fb):
        raise ValueError("initial bracket must have opposite signs")
    x=a+(b-a)/2
    for k in range(max_iter+1):
        width=b-a
        midpoint=a+width/2
        if midpoint==a or midpoint==b:
            return report(midpoint,evaluate(midpoint),"stagnation",k,(a,b))
        if width<=atol+rtol*max(abs(a),abs(b)):
            return report(midpoint,evaluate(midpoint),"converged",k,(a,b))
        if k==max_iter:
            return report(midpoint,evaluate(midpoint),"max_iter",k,(a,b))
        fx=evaluate(x)
        if fx==0:
            return report(x,0.0,"exact_root",k,(x,x))
        slope=derivative(x)
        proposal=None
        if slope!=0:
            candidate=x-fx/slope
            if math.isfinite(candidate) and a+width/4<candidate<b-width/4:
                proposal=candidate
        if proposal is None:
            proposal=midpoint
            kind="bisection"
            bisection+=1
        else:
            kind="newton"
            newton+=1
        fp=evaluate(proposal)
        trace.append({"iteration":k+1,"lower":a,"upper":b,
                      "proposal":proposal,"residual":fp,"step_type":kind})
        if fp==0:
            return report(proposal,0.0,"exact_root",k+1,(proposal,proposal))
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

def one_period_npv(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return -1000+1100/(1+r)

def one_period_npv_derivative(rate):
    r=finite(rate,"rate")
    if r<=-1:
        raise ValueError("rate must exceed -1")
    return -1100/(1+r)**2

def assessment():
    return {"zero_coupon":solve(zero_coupon,zero_coupon_derivative,0,0.2),
            "zero_coupon_analytic":math.sqrt(10/9)-1,
            "one_period_npv":solve(one_period_npv,one_period_npv_derivative,0,0.2),
            "one_period_analytic":0.1,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
