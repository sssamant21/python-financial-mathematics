"""Book 02 Section 13.8: closed-form ridge for two identical hedge instruments."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def solve_redundant_hedges(lam,limits,unit="standardized_exposure"):
    lam=finite(lam,"ridge strength")
    if lam<=0:
        raise ValueError("ridge strength must be positive")
    if unit!="standardized_exposure":
        raise ValueError("unsupported unit")
    if not isinstance(limits,dict) or set(limits)!={"RATE","CREDIT"}:
        raise ValueError("factor limits must specify RATE and CREDIT")
    bounds={k:finite(v,"factor limit") for k,v in limits.items()}
    if any(v<0 for v in bounds.values()):
        raise ValueError("factor limits must be nonnegative")
    t=finite(15.0/(10.0+lam),"position")
    achieved={"RATE":finite(2*t,"rate exposure"),
              "CREDIT":finite(4*t,"credit exposure")}
    residual={"RATE":finite(3-achieved["RATE"],"rate residual"),
              "CREDIT":finite(6-achieved["CREDIT"],"credit residual")}
    data=finite(0.5*math.fsum(v*v for v in residual.values()),"data objective")
    penalty=finite(lam*t*t,"penalty objective")
    passed={k:abs(residual[k])<=bounds[k] for k in ("RATE","CREDIT")}
    return {"positions":{"BOND_A":t,"BOND_B":t},
            "achieved":achieved,"residual_target_minus_achieved":residual,
            "data_objective":data,"penalty_objective":penalty,
            "total_objective":finite(data+penalty,"total objective"),
            "gradient":{"BOND_A":finite(5*(2*t-3)+lam*t,"gradient"),
                        "BOND_B":finite(5*(2*t-3)+lam*t,"gradient")},
            "factor_pass":passed,
            "decision":"ACCEPT" if all(passed.values()) else "REJECT",
            "runtime_certified":False}

def assessment():
    limits={"RATE":0.4,"CREDIT":1.1}
    return {"reference":solve_redundant_hedges(2,limits),
            "penalty_sweep":{str(lam):solve_redundant_hedges(lam,limits)
                             for lam in (0.5,2,20)},
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
