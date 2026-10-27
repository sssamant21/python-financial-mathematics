"""Book 02 Section 15.5: Jacobians of vector-valued functions."""
import json
import math

def number(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be a real number, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside floating-point range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def algebra_outputs(x,y):
    x=number(x,"x")
    y=number(y,"y")
    return tuple(number(v,"algebra output") for v in (x*x+y,x*y*y))

def algebra_jacobian(x,y):
    x=number(x,"x")
    y=number(y,"y")
    return ((number(2*x,"jacobian"),1.0),
            (number(y*y,"jacobian"),number(2*x*y,"jacobian")))

def financial_outputs(rate,years):
    r=number(rate,"rate")
    t=number(years,"years")
    if t<0:
        raise ValueError("years must be nonnegative")
    try:
        return (number(1000*math.exp(r*t),"first output"),
                number(500*math.exp(2*r*t),"second output"))
    except OverflowError as exc:
        raise ValueError("financial output overflow") from exc

def financial_jacobian(rate,years):
    r=number(rate,"rate")
    t=number(years,"years")
    f1,f2=financial_outputs(r,t)
    return ((number(t*f1,"jacobian"),number(r*f1,"jacobian")),
            (number(2*t*f2,"jacobian"),number(2*r*f2,"jacobian")))

def apply_jacobian(jacobian,displacement):
    if not isinstance(jacobian,(tuple,list)) or len(jacobian)!=2:
        raise ValueError("jacobian must be 2x2")
    if not isinstance(displacement,(tuple,list)) or len(displacement)!=2:
        raise ValueError("displacement must have two components")
    dx=(number(displacement[0],"displacement"),
        number(displacement[1],"displacement"))
    output=[]
    for row in jacobian:
        if not isinstance(row,(tuple,list)) or len(row)!=2:
            raise ValueError("jacobian must be 2x2")
        output.append(number(math.fsum(number(row[i],"jacobian entry")*dx[i]
                                       for i in range(2)),"jacobian product"))
    return tuple(output)

def centered_financial_column(rate,years,column,step=1e-5):
    r=number(rate,"rate")
    t=number(years,"years")
    h=number(step,"step")
    if h<=0:
        raise ValueError("step must be positive")
    if type(column) is not int or column not in (0,1):
        raise ValueError("column must be 0 or 1")
    center=r if column==0 else t
    if not math.isfinite(center+h) or not math.isfinite(center-h) or center+h==center or center-h==center:
        raise ValueError("step must produce finite distinct perturbations")
    if not math.isfinite(2*h):
        raise OverflowError("finite-difference denominator exceeds float range")
    if column==0:
        plus=financial_outputs(r+h,t)
        minus=financial_outputs(r-h,t)
    else:
        if t-h<0:
            raise ValueError("centered time perturbation leaves domain")
        plus=financial_outputs(r,t+h)
        minus=financial_outputs(r,t-h)
    return tuple(number((plus[i]-minus[i])/(2*h),"finite difference")
                 for i in range(2))

def assessment():
    r,t=0.05,2.0
    shock=(0.01,0.5)
    base=financial_outputs(r,t)
    shocked=financial_outputs(r+shock[0],t+shock[1])
    j=financial_jacobian(r,t)
    return {
        "algebra_outputs":algebra_outputs(2,3),
        "algebra_jacobian":algebra_jacobian(2,3),
        "algebra_first_order_change":
            apply_jacobian(algebra_jacobian(2,3),(0.1,-0.2)),
        "algebra_exact_change":
            tuple(algebra_outputs(2.1,2.8)[i]-algebra_outputs(2,3)[i]
                  for i in range(2)),
        "financial_outputs":base,
        "financial_jacobian":j,
        "financial_first_order_change":apply_jacobian(j,shock),
        "financial_exact_change":tuple(shocked[i]-base[i] for i in range(2)),
        "centered_rate_column":centered_financial_column(r,t,0),
        "centered_time_column":centered_financial_column(r,t,1),
        "jacobian_determinant":number(j[0][0]*j[1][1]-j[0][1]*j[1][0],
                                      "jacobian determinant"),
        "runtime_certified":False,
        "independent_review_completed":False,
    }

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
