"""Book 02 Section 14.6: transparent diagonal-column 3x2 SVD example."""
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

def diagonal_exposure_svd(first,second,target,rank_tolerance=0.0):
    """Special-case A=((first,0),(0,second),(0,0)); nonnegative coefficients.

    This is NOT a general SVD implementation. Singular values are reported in
    descending order; input/output singular directions remain in factor order.
    """
    first=finite(first,"first exposure")
    second=finite(second,"second exposure")
    tolerance=finite(rank_tolerance,"rank tolerance")
    if first<0 or second<0:
        raise ValueError("exposure magnitudes must be nonnegative")
    if tolerance<0:
        raise ValueError("rank tolerance must be nonnegative")
    try:
        b=tuple(target)
    except TypeError as exc:
        raise ValueError("target must have three components") from exc
    if len(b)!=3:
        raise ValueError("target must have three components")
    b=tuple(finite(v,"target component") for v in b)
    matrix=((first,0.0),(0.0,second),(0.0,0.0))
    singular_values=tuple(sorted((first,second),reverse=True))
    rank=sum(value>tolerance for value in singular_values)
    positions=(finite(b[0]/first,"position") if first>tolerance else 0.0,
               finite(b[1]/second,"position") if second>tolerance else 0.0)
    achieved=(finite(first*positions[0],"achieved exposure"),
              finite(second*positions[1],"achieved exposure"),0.0)
    residual=tuple(finite(b[i]-achieved[i],"residual") for i in range(3))
    objective=finite(0.5*math.fsum(v*v for v in residual),"objective")
    condition=(singular_values[0]/singular_values[1]
               if singular_values[1]>0 else None)
    if condition is not None:
        condition=finite(condition,"condition number")
    return {"matrix":matrix,"singular_values":singular_values,
            "left_singular_directions":((1.0,0.0,0.0),(0.0,1.0,0.0)),
            "right_singular_directions":((1.0,0.0),(0.0,1.0)),
            "rank_at_tolerance":rank,"rank_tolerance":tolerance,
            "positions":positions,"achieved_exposure":achieved,
            "signed_residual":residual,"half_squared_residual":objective,
            "condition_number_full_column_rank":condition,
            "runtime_certified":False}

def assessment():
    return {"reference":diagonal_exposure_svd(3,2,(6,4,5)),
            "rank_deficient":diagonal_exposure_svd(3,0,(6,4,5)),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
