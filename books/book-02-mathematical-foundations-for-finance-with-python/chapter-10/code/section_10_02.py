"""Section 10.2: definite and indefinite integrals."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def polynomial_antiderivative(coefficients,t,constant=0):
    x=finite(t,"t")
    c=finite(constant,"constant")
    values=[finite(a,"coefficient") for a in coefficients]
    if not values:
        raise ValueError("at least one coefficient required")
    result=math.fsum(a*x**(i+1)/(i+1) for i,a in enumerate(values))+c
    if not math.isfinite(result):
        raise ValueError("nonfinite antiderivative")
    return result

def polynomial_definite(coefficients,a,b):
    left,right=finite(a,"a"),finite(b,"b")
    result=polynomial_antiderivative(coefficients,right)-polynomial_antiderivative(coefficients,left)
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
    return result

def exponential_definite(scale,growth,a,b):
    c,k,left,right=(finite(v,name) for v,name in
                    ((scale,"scale"),(growth,"growth"),(a,"a"),(b,"b")))
    width=right-left
    if k==0:
        result=c*width
    else:
        result=c*math.exp(k*left)*math.expm1(k*width)/k
    if not math.isfinite(result):
        raise ValueError("nonfinite integral")
    return result

def midpoint_sum(function,a,b,n):
    if not callable(function):
        raise TypeError("function must be callable")
    left,right=finite(a,"a"),finite(b,"b")
    if type(n) is not int or n<=0:
        raise ValueError("n must be a positive integer")
    if left==right:
        return 0.0
    width=(right-left)/n
    result=math.fsum(finite(function(left+(i+0.5)*width),"integrand")*width
                     for i in range(n))
    if not math.isfinite(result):
        raise ValueError("nonfinite midpoint result")
    return result

if __name__=="__main__":
    result={
        "linear_antiderivative_at_2":polynomial_antiderivative([100,20],2),
        "linear_integral_0_to_2":polynomial_definite([100,20],0,2),
        "signed_integral":polynomial_definite([-1,1],0,2),
        "growing_payment_integral":exponential_definite(500,0.03,0,2),
        "midpoint_checks":[{"n":n,"estimate":midpoint_sum(lambda t:math.exp(0.03*t)*500,0,2,n)}
                           for n in (4,16,64,256)]}
    print(json.dumps(result,indent=2,allow_nan=False))
