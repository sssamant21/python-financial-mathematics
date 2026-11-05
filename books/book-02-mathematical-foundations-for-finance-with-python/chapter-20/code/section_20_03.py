"""Book 02 Section 20.3: financial and mathematical invariants (draft)."""
import json
import math
from fractions import Fraction
from _valuation_math import scaled_exponential as _scaled_valuation
from _continuous_account import account as _account_balance

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

def discount_factor(rate,years):
    r,t=finite(rate,"rate"),finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    return _scaled_valuation(1.,-Fraction(r)*Fraction(t))

def present_value(flow,rate,years):
    f,r,t=(finite(v,n) for v,n in ((flow,"flow"),(rate,"rate"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    return _scaled_valuation(f,-Fraction(r)*Fraction(t))

def future_value(flow,rate,years):
    f,r,t=finite(flow,"flow"),finite(rate,"rate"),finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    return _scaled_valuation(f,Fraction(r)*Fraction(t))

def account_transition(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    return _account_balance(a,r,u,t)

def cash_flow_pv(flows,rate):
    r=finite(rate,"rate")
    if not isinstance(flows,(list,tuple)):
        raise TypeError("flows must be a sequence of (amount, year) pairs")
    terms=[]
    for item in flows:
        if not isinstance(item,(list,tuple)) or len(item)!=2:
            raise ValueError("each cash flow must be (amount, year)")
        terms.append(present_value(item[0],r,item[1]))
    return finite(math.fsum(terms),"cash_flow_pv")

def portfolio_feasible(weights,tolerance=1e-10):
    tol=finite(tolerance,"tolerance")
    if tol<0:
        raise ValueError("tolerance must be nonnegative")
    if not isinstance(weights,(list,tuple)) or not weights:
        raise ValueError("weights must be a nonempty sequence")
    w=[finite(v,"weight") for v in weights]
    bound=Fraction(tol)
    return all(x>=-tol for x in w) and abs(sum(map(Fraction,w))-1)<=bound

def covariance_quadratic_2x2(a,b,c,d,x,y):
    a,b,c,d,x,y=(finite(v,n) for v,n in
                 ((a,"a"),(b,"b"),(c,"c"),(d,"d"),(x,"x"),(y,"y")))
    a,b,c,d,x,y=map(Fraction,(a,b,c,d,x,y))
    value=a*x*x+(b+c)*x*y+d*y*y
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError("quadratic outside floating-point range") from exc
    if value and result==0:
        raise ValueError("quadratic outside floating-point range")
    return result

def assessment():
    rate=0.04
    first=account_transition(1000,rate,200,2)
    return {
        "discount_zero_horizon":discount_factor(rate,0),
        "discount_composition_left":discount_factor(rate,5),
        "discount_composition_right":discount_factor(rate,2)*discount_factor(rate,3),
        "pv_split_left":present_value(100,rate,2),
        "pv_split_right":present_value(40,rate,2)+present_value(60,rate,2),
        "pv_future_round_trip":present_value(future_value(1000,rate,5),rate,5),
        "account_composition_left":account_transition(1000,rate,200,5),
        "account_composition_right":account_transition(first,rate,200,3),
        "cash_flow_split":cash_flow_pv([(40,2),(60,2)],rate),
        "zero_interest_reconciliation":account_transition(1000,0,200,5)-1000,
        "portfolio_feasible":portfolio_feasible([0.4,0.6]),
        "indefinite_matrix_quadratic":covariance_quadratic_2x2(1,2,2,1,1,-1),
        "runtime_certified":False,
        "independent_review_completed":False
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
