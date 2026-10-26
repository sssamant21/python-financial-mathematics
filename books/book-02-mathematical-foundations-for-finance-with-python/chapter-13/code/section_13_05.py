"""Book 02 Section 13.5: one-instrument ordinary least-squares objective."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        x=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x

def checked_labels(items,name):
    result=tuple(items)
    if not result or any(type(x) is not str or not x.strip() for x in result):
        raise ValueError(f"{name}: nonempty labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    return result

def align(source,values,order):
    source=checked_labels(source,"source labels")
    order=checked_labels(order,"target labels")
    values=tuple(values)
    if len(source)!=len(values) or len(source)!=len(order) or set(source)!=set(order):
        raise ValueError("factor label or shape mismatch")
    mapping=dict(zip(source,(finite(v,"factor value") for v in values)))
    return tuple(mapping[k] for k in order)

def solve_one_column(factors,sensitivity,target_labels,target_values,
                     tolerance_labels,tolerance_values,unit="standardized_exposure"):
    factors=checked_labels(factors,"factor labels")
    if unit!="standardized_exposure":
        raise ValueError("unsupported exposure unit")
    a=tuple(finite(v,"sensitivity") for v in sensitivity)
    if len(a)!=len(factors):
        raise ValueError("sensitivity shape mismatch")
    b=align(target_labels,target_values,factors)
    limits=align(tolerance_labels,tolerance_values,factors)
    if any(v<0 for v in limits):
        raise ValueError("negative tolerance")
    # Scale to avoid intermediate overflow in sums of squares.
    scale=max(abs(v) for v in a)
    if scale==0:
        raise ValueError("zero sensitivity vector")
    normalized=tuple(v/scale for v in a)
    denominator=math.fsum(v*v for v in normalized)
    coefficient=finite(math.fsum(normalized[i]*b[i] for i in range(len(a)))/
                       denominator/scale,"position")
    achieved=tuple(finite(v*coefficient,"achieved exposure") for v in a)
    residual=tuple(finite(b[i]-achieved[i],"residual") for i in range(len(a)))
    objective=finite(0.5*math.fsum(v*v for v in residual),"objective")
    gradient=finite(-math.fsum(a[i]*residual[i] for i in range(len(a))),"gradient")
    passed={factor:abs(residual[i])<=limits[i] for i,factor in enumerate(factors)}
    return {"position":coefficient,"achieved":dict(zip(factors,achieved)),
            "residual_target_minus_achieved":dict(zip(factors,residual)),
            "objective_half_squared_l2":objective,"gradient":gradient,
            "factor_pass":passed,
            "decision":"ACCEPT" if all(passed.values()) else "REJECT",
            "runtime_certified":False}

def assessment():
    reference=solve_one_column(("RATE","CREDIT"),(1,2),
                               ("CREDIT","RATE"),(7,3),
                               ("CREDIT","RATE"),(0.1,0.5))
    return {"reference":reference,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
