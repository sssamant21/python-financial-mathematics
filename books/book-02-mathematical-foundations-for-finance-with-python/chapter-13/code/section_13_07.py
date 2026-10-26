"""Book 02 Section 13.7: labeled, unit-aware, one-column weighted least squares."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def checked_labels(items,name):
    result=tuple(items)
    if not result or any(type(x) is not str or not x.strip() for x in result):
        raise ValueError(f"{name}: nonempty string labels required")
    if len(set(result))!=len(result):
        raise ValueError(f"{name}: duplicate labels")
    return result

def checked_map(data,factors,name):
    if not isinstance(data,dict) or set(data)!=set(factors) or len(data)!=len(factors):
        raise ValueError(f"{name}: factor labels mismatch")
    return tuple(finite(data[factor],name) for factor in factors)

def solve_weighted(factors,sensitivities,target,scales,hard_limits,units):
    factors=checked_labels(factors,"factor labels")
    a=checked_map(sensitivities,factors,"sensitivity")
    b=checked_map(target,factors,"target")
    s=checked_map(scales,factors,"scale")
    limits=checked_map(hard_limits,factors,"hard limit")
    if not isinstance(units,dict) or set(units)!=set(factors) or len(units)!=len(factors):
        raise ValueError("unit labels mismatch")
    if any(type(units[f]) is not str or not units[f].strip() for f in factors):
        raise ValueError("missing factor unit")
    if any(v<=0 for v in s):
        raise ValueError("scales must be positive")
    if any(v<0 for v in limits):
        raise ValueError("hard limits must be nonnegative")
    standardized_a=tuple(finite(a[i]/s[i],"standardized sensitivity") for i in range(len(factors)))
    standardized_b=tuple(finite(b[i]/s[i],"standardized target") for i in range(len(factors)))
    normalizer=max(abs(v) for v in standardized_a)
    if normalizer==0:
        raise ValueError("zero sensitivity vector")
    scaled=tuple(v/normalizer for v in standardized_a)
    denominator=math.fsum(v*v for v in scaled)
    numerator=math.fsum(scaled[i]*standardized_b[i] for i in range(len(factors)))
    position=finite((numerator/denominator)/normalizer,"position")
    achieved=tuple(finite(position*v,"achieved exposure") for v in a)
    residual=tuple(finite(b[i]-achieved[i],"residual") for i in range(len(factors)))
    z=tuple(finite(residual[i]/s[i],"standardized residual") for i in range(len(factors)))
    objective=finite(0.5*math.fsum(v*v for v in z),"weighted objective")
    gradient=finite(-math.fsum(standardized_a[i]*z[i] for i in range(len(factors))),"weighted gradient")
    passed={f:abs(residual[i])<=limits[i] for i,f in enumerate(factors)}
    return {"position":position,"units":dict((f,units[f]) for f in factors),
            "achieved":dict(zip(factors,achieved)),
            "residual_target_minus_achieved":dict(zip(factors,residual)),
            "standardized_residual":dict(zip(factors,z)),
            "weighted_objective":objective,"weighted_gradient":gradient,
            "factor_pass":passed,
            "decision":"ACCEPT" if all(passed.values()) else "REJECT",
            "runtime_certified":False}

def assessment():
    factors=("RATE","CREDIT")
    return {"reference":solve_weighted(
        factors,{"RATE":1,"CREDIT":2},{"RATE":3,"CREDIT":7},
        {"RATE":1,"CREDIT":2},{"RATE":0.2,"CREDIT":0.6},
        {"RATE":"rate_sensitivity_units","CREDIT":"credit_sensitivity_units"}),
        "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
