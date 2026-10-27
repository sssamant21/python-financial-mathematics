"""Book 02 Section 20.2: known-value and analytic benchmarks (draft)."""
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

def present_value(flow,rate,years):
    f,r,t=(finite(v,n) for v,n in ((flow,"flow"),(rate,"rate"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    try:
        return finite(f*math.exp(-r*t),"present_value")
    except OverflowError as exc:
        raise ValueError("present value overflow") from exc

def nominal_to_continuous(nominal,frequency):
    j=finite(nominal,"nominal")
    if type(frequency) is not int or frequency<1 or j/frequency<=-1:
        raise ValueError("invalid nominal rate or frequency")
    return finite(frequency*math.log1p(j/frequency),"continuous_rate")

def annuity_explicit(payment,period_rate,periods):
    c,i=finite(payment,"payment"),finite(period_rate,"period_rate")
    if type(periods) is not int or periods<0 or i<=-1:
        raise ValueError("invalid periods or rate")
    return finite(math.fsum(c*(1+i)**(-k) for k in range(1,periods+1)),"annuity")

def annuity_closed(payment,period_rate,periods):
    c,i=finite(payment,"payment"),finite(period_rate,"period_rate")
    if type(periods) is not int or periods<0 or i<=-1:
        raise ValueError("invalid periods or rate")
    if periods==0:
        return 0.0
    if i==0:
        return finite(c*periods,"annuity")
    return finite(-c*math.expm1(-periods*math.log1p(i))/i,"annuity")

def account(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0:
        return finite(a+u*t,"balance")
    try:
        return finite(a*math.exp(r*t)+u*math.expm1(r*t)/r,"balance")
    except OverflowError as exc:
        raise ValueError("balance overflow") from exc

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<0 or w<0:
        raise ValueError("initial and withdrawal must be nonnegative")
    if a==0:
        return 0.0
    if w==0:
        return None
    if r==0:
        return a/w
    if r*a/w>=1:
        return None
    return finite(-math.log1p(-r*a/w)/r,"depletion_time")

def solve_two_by_two(a,b,c,d,y1,y2):
    a,b,c,d,y1,y2=(finite(v,n) for v,n in
                    ((a,"a"),(b,"b"),(c,"c"),(d,"d"),(y1,"y1"),(y2,"y2")))
    det=a*d-b*c
    if det==0 or not math.isfinite(det):
        raise ValueError("singular or unrepresentable determinant")
    return (finite((d*y1-b*y2)/det,"x1"),
            finite((a*y2-c*y1)/det,"x2"))

def assessment():
    rc=nominal_to_continuous(0.06,12)
    return {
        "present_value":present_value(1000,0.05,2),
        "continuous_equivalent_rate":rc,
        "nominal_one_year_growth":(1+0.06/12)**12,
        "continuous_one_year_growth":math.exp(rc),
        "annuity_explicit":annuity_explicit(100,0.005,24),
        "annuity_closed":annuity_closed(100,0.005,24),
        "continuous_account":account(1000,0.04,200,5),
        "depletion_time":depletion_time(1000,0.04,100),
        "linear_system_solution":solve_two_by_two(2,1,1,3,5,7),
        "runtime_certified":False,
        "independent_review_completed":False
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
