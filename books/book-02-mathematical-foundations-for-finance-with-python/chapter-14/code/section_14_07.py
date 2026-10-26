"""Book 02 Section 14.7: transparent low-rank diagonal-column 3x2 example."""
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

def low_rank_diagonal_exposure(first,second,rank):
    """Best rank-k approximation of ((first,0),(0,second),(0,0)).

    Nonnegative diagonal magnitudes; special case, not a general SVD.
    """
    first=finite(first,"first singular magnitude")
    second=finite(second,"second singular magnitude")
    if first<0 or second<0:
        raise ValueError("magnitudes must be nonnegative")
    if type(rank) is not int or rank not in (0,1,2):
        raise ValueError("rank must be an integer from 0 to 2")
    values=((first,0),(second,1))
    retained=sorted(values,key=lambda pair:(-pair[0],pair[1]))[:rank]
    kept={index for _,index in retained}
    a1=first if 0 in kept else 0.0
    a2=second if 1 in kept else 0.0
    original=((first,0.0),(0.0,second),(0.0,0.0))
    approximation=((a1,0.0),(0.0,a2),(0.0,0.0))
    residual=((first-a1,0.0),(0.0,second-a2),(0.0,0.0))
    squared_total=finite(math.fsum((first*first,second*second)),"total squared energy")
    squared_kept=finite(math.fsum((a1*a1,a2*a2)),"retained squared energy")
    frobenius_error=finite(math.hypot(first-a1,second-a2),"Frobenius error")
    spectral_error=finite(max(abs(first-a1),abs(second-a2)),"spectral error")
    retained_fraction=(squared_kept/squared_total if squared_total>0 else None)
    return {"original":original,"approximation":approximation,
            "residual":residual,"singular_values":tuple(sorted((first,second),reverse=True)),
            "requested_rank":rank,"actual_rank":sum(v>0 for v in (a1,a2)),
            "frobenius_error":frobenius_error,"spectral_error":spectral_error,
            "retained_squared_energy_fraction":retained_fraction,
            "runtime_certified":False}

def assessment():
    return {"rank_0":low_rank_diagonal_exposure(4,2,0),
            "rank_1":low_rank_diagonal_exposure(4,2,1),
            "rank_2":low_rank_diagonal_exposure(4,2,2),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
