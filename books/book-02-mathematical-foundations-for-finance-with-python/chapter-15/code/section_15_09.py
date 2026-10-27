"""Book 02 Section 15.9: multi-input valuation sensitivity engine."""
import json
import math

def real(value, label):
    if type(value) not in (int, float):
        raise TypeError(f"{label} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{label} outside floating-point range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result

def triple(values, label):
    if not isinstance(values,(list,tuple)) or len(values)!=3:
        raise ValueError(f"{label} must contain three values")
    return tuple(real(x,label) for x in values)

def valid_inputs(values):
    p,r,t=triple(values,"inputs")
    if p<=0 or t<0:
        raise ValueError("principal must be positive and years nonnegative")
    return p,r,t

def valuation(principal, rate, years):
    p,r,t=valid_inputs((principal,rate,years))
    try:
        return (real(p*math.exp(r*t),"future value"),
                real(0.5*p*math.exp(-r*t),"discounted value"))
    except OverflowError as exc:
        raise ValueError("exponential valuation overflow") from exc

def jacobian(principal, rate, years):
    p,r,t=valid_inputs((principal,rate,years))
    v1,v2=valuation(p,r,t)
    return ((real(v1/p,"Jacobian"),real(t*v1,"Jacobian"),real(r*v1,"Jacobian")),
            (real(v2/p,"Jacobian"),real(-t*v2,"Jacobian"),real(-r*v2,"Jacobian")))

def hessians(principal, rate, years):
    p,r,t=valid_inputs((principal,rate,years))
    v1,v2=valuation(p,r,t)
    first=((0.0,t*v1/p,r*v1/p),
           (t*v1/p,t*t*v1,(1+r*t)*v1),
           (r*v1/p,(1+r*t)*v1,r*r*v1))
    second=((0.0,-t*v2/p,-r*v2/p),
            (-t*v2/p,t*t*v2,(r*t-1)*v2),
            (-r*v2/p,(r*t-1)*v2,r*r*v2))
    return tuple(tuple(tuple(real(z,"Hessian") for z in row) for row in matrix)
                 for matrix in (first,second))

def dot(a,b):
    if len(a)!=len(b):
        raise ValueError("vector dimensions differ")
    return real(math.fsum(real(x,"dot input")*real(y,"dot input")
                          for x,y in zip(a,b)),"dot product")

def quadratic_form(matrix, vector):
    if len(matrix)!=len(vector) or any(len(row)!=len(vector) for row in matrix):
        raise ValueError("quadratic-form dimensions differ")
    return real(math.fsum(vector[i]*matrix[i][j]*vector[j]
                          for i in range(len(vector))
                          for j in range(len(vector))),"quadratic form")

def scenario(base, shock):
    p,r,t=valid_inputs(base)
    dp,dr,dt=triple(shock,"shock")
    new=(real(p+dp,"shocked principal"),real(r+dr,"shocked rate"),
         real(t+dt,"shocked maturity"))
    valid_inputs(new)
    base_values=valuation(p,r,t)
    new_values=valuation(*new)
    j=jacobian(p,r,t)
    hs=hessians(p,r,t)
    displacement=(dp,dr,dt)
    exact=tuple(real(new_values[i]-base_values[i],"exact change") for i in range(2))
    first=tuple(dot(row,displacement) for row in j)
    second=tuple(real(first[i]+0.5*quadratic_form(hs[i],displacement),
                      "second order change") for i in range(2))
    err1=tuple(real(first[i]-exact[i],"first order error") for i in range(2))
    err2=tuple(real(second[i]-exact[i],"second order error") for i in range(2))
    return {
        "base_inputs":(p,r,t),"shock":displacement,"shocked_inputs":new,
        "base_values":base_values,"shocked_values":new_values,
        "jacobian":j,"hessians":hs,
        "exact_changes":exact,"first_order_changes":first,
        "second_order_changes":second,
        "first_order_errors":err1,"second_order_errors":err2,
        "absolute_first_order_errors":tuple(abs(x) for x in err1),
        "absolute_second_order_errors":tuple(abs(x) for x in err2),
        "portfolio_base":real(math.fsum(base_values),"portfolio base"),
        "portfolio_shocked":real(math.fsum(new_values),"portfolio shocked"),
        "portfolio_exact_change":real(math.fsum(exact),"portfolio exact"),
        "portfolio_first_order_change":real(math.fsum(first),"portfolio first"),
        "portfolio_second_order_change":real(math.fsum(second),"portfolio second"),
    }

def centered_jacobian_column(base, index, step):
    x=list(valid_inputs(base))
    if type(index) is not int or index not in (0,1,2):
        raise ValueError("index must be 0, 1, or 2")
    h=real(step,"finite-difference step")
    if h<=0:
        raise ValueError("step must be positive")
    center=x[index]
    if not math.isfinite(center+h) or not math.isfinite(center-h) or center+h==center or center-h==center:
        raise ValueError("step must produce finite distinct perturbations")
    if not math.isfinite(2*h):
        raise OverflowError("finite-difference denominator exceeds float range")
    plus=x.copy()
    minus=x.copy()
    plus[index]+=h
    minus[index]-=h
    vp=valuation(*plus)
    vm=valuation(*minus)
    return tuple(real((vp[i]-vm[i])/(2*h),"finite-difference derivative")
                 for i in range(2))

def assessment():
    base=(1000,0.05,2)
    result=scenario(base,(100,0.01,0.5))
    result["finite_difference_columns"]=(
        centered_jacobian_column(base,0,0.01),
        centered_jacobian_column(base,1,1e-5),
        centered_jacobian_column(base,2,1e-4))
    result["runtime_certified"]=False
    result["independent_review_completed"]=False
    return result

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
