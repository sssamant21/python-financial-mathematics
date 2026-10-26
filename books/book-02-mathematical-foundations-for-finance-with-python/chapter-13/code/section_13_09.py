"""Book 02 Section 13.9: least-squares replication analyzer project."""
import json
import math
from section_13_06 import solve_qr,finite,labels

def checked_mapping(mapping,keys,name,positive=False,nonnegative=False):
    if not isinstance(mapping,dict) or set(mapping)!=set(keys) or len(mapping)!=len(keys):
        raise ValueError(f"{name}: labels mismatch")
    result={key:finite(mapping[key],name) for key in keys}
    if positive and any(v<=0 for v in result.values()):
        raise ValueError(f"{name}: positive values required")
    if nonnegative and any(v<0 for v in result.values()):
        raise ValueError(f"{name}: nonnegative values required")
    return result

def analyze(factors,instruments,rows,target,scales,hard_limits,units):
    factors=labels(factors,"factor labels")
    instruments=labels(instruments,"instrument labels")
    target=checked_mapping(target,factors,"target")
    scales=checked_mapping(scales,factors,"scales",positive=True)
    limits=checked_mapping(hard_limits,factors,"hard limits",nonnegative=True)
    if not isinstance(units,dict) or set(units)!=set(factors) or len(units)!=len(factors):
        raise ValueError("factor units mismatch")
    if any(type(units[k]) is not str or not units[k].strip() for k in factors):
        raise ValueError("factor unit missing")
    raw=tuple(tuple(row) for row in rows)
    if len(raw)!=len(factors) or any(len(row)!=len(instruments) for row in raw):
        raise ValueError("matrix shape mismatch")
    matrix=tuple(tuple(finite(v,"sensitivity") for v in row) for row in raw)
    scaled=tuple(tuple(v/scales[factors[i]] for v in row) for i,row in enumerate(matrix))
    scaled_target=tuple(target[f]/scales[f] for f in factors)
    result=solve_qr(factors,instruments,scaled,factors,scaled_target)
    positions=result["positions"]
    achieved={f:finite(math.fsum(matrix[i][j]*positions[instruments[j]]
                      for j in range(len(instruments))),"achieved")
              for i,f in enumerate(factors)}
    residual={f:finite(target[f]-achieved[f],"residual") for f in factors}
    standardized={f:finite(residual[f]/scales[f],"standardized residual") for f in factors}
    objective=finite(0.5*math.fsum(v*v for v in standardized.values()),"objective")
    gradient={instrument:finite(-math.fsum(
                scaled[i][j]*standardized[factors[i]] for i in range(len(factors))),"gradient")
              for j,instrument in enumerate(instruments)}
    passed={f:abs(residual[f])<=limits[f] for f in factors}
    return {"positions":positions,"achieved":achieved,
            "residual_target_minus_achieved":residual,
            "standardized_residual":standardized,
            "weighted_objective":objective,"weighted_gradient":gradient,
            "factor_units":{f:units[f] for f in factors},
            "factor_pass":passed,
            "decision":"ACCEPT" if all(passed.values()) else "REJECT",
            "solver":"educational_householder_qr",
            "runtime_certified":False}

def assessment():
    factors=("RATE","CREDIT","LIQUIDITY")
    return {"reference":analyze(factors,("BOND_A","BOND_B"),
            ((1,0),(0,1),(1,1)),
            {"RATE":2,"CREDIT":3,"LIQUIDITY":6},
            {"RATE":1,"CREDIT":1,"LIQUIDITY":1},
            {"RATE":0.4,"CREDIT":0.4,"LIQUIDITY":0.25},
            {f:"standardized_exposure" for f in factors}),
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
