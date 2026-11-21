"""Section 10.3: Fundamental Theorem of Calculus."""
import json
import math
from fractions import Fraction

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

def _polynomial_coefficients(coefficients):
    values = [Fraction(finite(c,"coefficient")) for c in coefficients]
    if not values:
        raise ValueError("at least one coefficient required")
    return values

def _polynomial_report(value, name):
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("nonfinite " + name) from exc
    if not math.isfinite(result):
        raise ValueError("nonfinite " + name)
    return result

def _polynomial_value_exact(coeff,x):
    return sum((c*x**i for i,c in enumerate(coeff) if c), Fraction(0))

def _polynomial_accumulation_exact(coeff,left,right):
    if left == right:
        return Fraction(0)
    return sum((c*(right**i-left**i)/i
                for i,c in enumerate(coeff,1) if c), Fraction(0))

def polynomial_value(coefficients,x):
    t = Fraction(finite(x,"x"))
    coeff = _polynomial_coefficients(coefficients)
    return _polynomial_report(_polynomial_value_exact(coeff,t),"polynomial")

def polynomial_accumulation(coefficients,a,b):
    left,right = Fraction(finite(a,"a")),Fraction(finite(b,"b"))
    coeff = _polynomial_coefficients(coefficients)
    return _polynomial_report(_polynomial_accumulation_exact(coeff,left,right),"accumulation")

def balance(initial,coefficients,start,time):
    value = Fraction(finite(initial,"initial"))
    a,b = Fraction(finite(start,"start")),Fraction(finite(time,"time"))
    coeff = _polynomial_coefficients(coefficients)
    return _polynomial_report(value+_polynomial_accumulation_exact(coeff,a,b),"balance")

def endpoint_derivative(coefficients,lower,upper,lower_rate,upper_rate):
    a,b = Fraction(finite(lower,"lower")),Fraction(finite(upper,"upper"))
    ap,bp = Fraction(finite(lower_rate,"lower_rate")),Fraction(finite(upper_rate,"upper_rate"))
    coeff = _polynomial_coefficients(coefficients)
    result = _polynomial_value_exact(coeff,b)*bp-_polynomial_value_exact(coeff,a)*ap
    return _polynomial_report(result,"endpoint derivative")

def _rolling_arguments(coefficients,time,window):
    t,w = Fraction(finite(time,"time")),Fraction(finite(window,"window"))
    if w<=0:
        raise ValueError("window must be positive")
    return _polynomial_coefficients(coefficients),t,w

def rolling_accumulation(coefficients,time,window=1):
    coeff,t,w = _rolling_arguments(coefficients,time,window)
    return _polynomial_report(_polynomial_accumulation_exact(coeff,t-w,t),"rolling accumulation")

def rolling_derivative(coefficients,time,window=1):
    coeff,t,w = _rolling_arguments(coefficients,time,window)
    result = _polynomial_value_exact(coeff,t)-_polynomial_value_exact(coeff,t-w)
    return _polynomial_report(result,"rolling derivative")

def centered_derivative(function,x,step=1e-5):
    if not callable(function):
        raise TypeError("function must be callable")
    t,h=finite(x,"x"),finite(step,"step")
    if h<=0:
        raise ValueError("step must be positive and representable")
    right,left = t+h,t-h
    if not math.isfinite(right) or not math.isfinite(left) or not left<t<right:
        raise ValueError("finite distinct stencil points required")
    upper = Fraction(finite(function(right),"function"))
    lower = Fraction(finite(function(left),"function"))
    # The actual rounded stencil span preserves affine secant identities.
    result = (upper-lower)/(Fraction(right)-Fraction(left))
    return _polynomial_report(result,"derivative estimate")

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
