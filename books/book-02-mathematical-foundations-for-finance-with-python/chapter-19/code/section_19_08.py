"""Book 02 Section 19.8: continuous/discrete financial comparison."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def nominal_to_continuous(nominal,frequency):
    j=finite(nominal,"nominal")
    if type(frequency) is not int or frequency<1 or j/frequency<=-1:
        raise ValueError("invalid nominal rate or frequency")
    return finite(frequency*math.log1p(j/frequency),"continuous rate")

def continuous_to_nominal(rate,frequency):
    r=finite(rate,"continuous rate")
    if type(frequency) is not int or frequency<1:
        raise ValueError("frequency must be a positive integer")
    return finite(frequency*math.expm1(r/frequency),"nominal rate")

def continuous_growth(initial,rate,years):
    a,r,t=finite(initial,"initial"),finite(rate,"rate"),finite(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    return finite(a*math.exp(r*t),"balance")

def discrete_growth(initial,nominal,frequency,periods):
    a,j=finite(initial,"initial"),finite(nominal,"nominal")
    if type(frequency) is not int or frequency<1 or type(periods) is not int or periods<0:
        raise ValueError("frequency positive; periods nonnegative integer")
    if j/frequency<=-1:
        raise ValueError("periodic gross growth factor must be positive")
    return finite(a*math.exp(periods*math.log1p(j/frequency)),"balance")

def continuous_contributions(initial,rate,flow,years):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0:
        raise ValueError("years must be nonnegative")
    if r==0:
        return finite(a+u*t,"balance")
    exponent=r*t
    factor=t if exponent==0 else t*(math.expm1(exponent)/exponent)
    return finite(a*math.exp(exponent)+u*factor,"balance")

def end_period_contributions(initial,rate,flow,years,periods):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(periods) is not int or periods<1:
        raise ValueError("invalid years or periods")
    h=t/periods
    if r==0 or t==0:
        return finite(a+u*t,"balance")
    total_exponent=r*t
    period_exponent=r*h
    # expm1(x)/x has the continuous value 1 at zero, including when
    # a nonzero mathematical product rounds to zero in floating point.
    def exprel(x):
        return 1.0 if x==0 else math.expm1(x)/x
    factor=t*(exprel(total_exponent)/exprel(period_exponent))
    return finite(a*math.exp(total_exponent)+u*factor,"balance")

def euler_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or steps")
    h=t/steps
    for _ in range(steps):
        a=finite(a+h*(r*a+u),"Euler balance")
    return a

def rk4_account(initial,rate,flow,years,steps):
    a,r,u,t=(finite(v,n) for v,n in
             ((initial,"initial"),(rate,"rate"),(flow,"flow"),(years,"years")))
    if t<0 or type(steps) is not int or steps<1:
        raise ValueError("invalid years or steps")
    h=t/steps
    for _ in range(steps):
        k1=r*a+u
        k2=r*(a+h*k1/2)+u
        k3=r*(a+h*k2/2)+u
        k4=r*(a+h*k3)+u
        a=finite(a+h*(k1+2*k2+2*k3+k4)/6,"RK4 balance")
    return a

def depletion_time(initial,rate,withdrawal):
    a,r,w=(finite(v,n) for v,n in
           ((initial,"initial"),(rate,"rate"),(withdrawal,"withdrawal")))
    if a<0 or w<0:
        raise ValueError("balance and withdrawal must be nonnegative")
    if a==0:
        return 0.0
    if w==0:
        return None
    if r==0:
        return a/w
    ratio=r*a/w
    if ratio>=1:
        return None
    if ratio==0:
        return finite(a/w,"depletion time")
    return finite(-math.log1p(-ratio)/r,"depletion time")

def assessment():
    j=0.06
    rc=nominal_to_continuous(j,12)
    exact=continuous_contributions(1000,0.04,200,5)
    convergence={}
    for n in (10,20,40):
        e=euler_account(1000,0.04,200,5,n)
        k=rk4_account(1000,0.04,200,5,n)
        convergence[str(n)]={"euler":e,"rk4":k,
                             "euler_absolute_error":abs(e-exact),
                             "rk4_absolute_error":abs(k-exact)}
    return {"equivalent_continuous_rate":rc,
            "nominal_annual_balance":discrete_growth(1000,j,12,12),
            "continuous_annual_balance":continuous_growth(1000,rc,1),
            "continuous_flow_balance":exact,
            "monthly_end_period_balance":end_period_contributions(1000,0.04,200,5,60),
            "convergence":convergence,
            "depletion_time":depletion_time(1000,0.04,100),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
