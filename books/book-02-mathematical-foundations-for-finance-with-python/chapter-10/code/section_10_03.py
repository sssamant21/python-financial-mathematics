"""Section 10.3: Fundamental Theorem of Calculus."""
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

def polynomial_value(coefficients,x):
    t=finite(x,"x")
    coeff=[finite(c,"coefficient") for c in coefficients]
    if not coeff:
        raise ValueError("at least one coefficient required")
    result=math.fsum(c*t**i for i,c in enumerate(coeff))
    if not math.isfinite(result):
        raise ValueError("nonfinite polynomial")
    return result

def polynomial_accumulation(coefficients,a,b):
    left,right=finite(a,"a"),finite(b,"b")
    coeff=[finite(c,"coefficient") for c in coefficients]
    if not coeff:
        raise ValueError("at least one coefficient required")
    value=math.fsum(c*(right**(i+1)-left**(i+1))/(i+1)
                    for i,c in enumerate(coeff))
    if not math.isfinite(value):
        raise ValueError("nonfinite accumulation")
    return value

def balance(initial,coefficients,start,time):
    return finite(initial,"initial")+polynomial_accumulation(coefficients,start,time)

def endpoint_derivative(coefficients,lower,upper,lower_rate,upper_rate):
    a,b=finite(lower,"lower"),finite(upper,"upper")
    ap,bp=finite(lower_rate,"lower_rate"),finite(upper_rate,"upper_rate")
    return polynomial_value(coefficients,b)*bp-polynomial_value(coefficients,a)*ap

def rolling_accumulation(coefficients,time,window=1):
    t,w=finite(time,"time"),finite(window,"window")
    if w<=0:
        raise ValueError("window must be positive")
    return polynomial_accumulation(coefficients,t-w,t)

def rolling_derivative(coefficients,time,window=1):
    t,w=finite(time,"time"),finite(window,"window")
    if w<=0:
        raise ValueError("window must be positive")
    return polynomial_value(coefficients,t)-polynomial_value(coefficients,t-w)

def centered_derivative(function,x,step=1e-5):
    if not callable(function):
        raise TypeError("function must be callable")
    t,h=finite(x,"x"),finite(step,"step")
    if h<=0 or t+h==t or t-h==t:
        raise ValueError("step must be positive and representable")
    result=(finite(function(t+h),"function")-finite(function(t-h),"function"))/(2*h)
    if not math.isfinite(result):
        raise ValueError("nonfinite derivative estimate")
    return result

if __name__=="__main__":
    coeff=[600,50]
    report={
        "accumulated_0_to_3":polynomial_accumulation(coeff,0,3),
        "balance_at_3":balance(1000,coeff,0,3),
        "instantaneous_rate_at_2":polynomial_value(coeff,2),
        "numeric_rate_at_2":centered_derivative(
            lambda t:polynomial_accumulation(coeff,0,t),2),
        "rolling_amount_at_2":rolling_accumulation(coeff,2),
        "rolling_derivative_at_2":rolling_derivative(coeff,2),
        "variable_endpoint_derivative":endpoint_derivative([1,0,1],1,3,2,3)}
    print(json.dumps(report,indent=2,allow_nan=False))
