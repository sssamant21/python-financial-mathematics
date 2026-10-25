"""Section 9.8: reproducible valuation sensitivity and scenario reports."""
import json
import math

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        result=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside finite float range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result

def validate_flows(flows):
    items=list(flows)
    if not items:
        raise ValueError("at least one cash flow required")
    result=[]
    for cash,years in items:
        c,t=finite(cash,"cash"),finite(years,"years")
        if c<=0 or t<0:
            raise ValueError("cash must be positive and years nonnegative")
        result.append((c,t))
    return result

def bp_to_decimal(basis_points):
    return finite(basis_points,"basis_points")/10000.0

def scenario_from_terms(terms,years,shocks):
    exact=math.fsum(v*math.expm1(-t*h) for v,t,h in zip(terms,years,shocks))
    linear=-math.fsum(t*v*h for v,t,h in zip(terms,years,shocks))
    quadratic=linear+0.5*math.fsum(t*t*v*h*h for v,t,h in zip(terms,years,shocks))
    if not all(math.isfinite(x) for x in (exact,linear,quadratic)):
        raise ValueError("nonfinite scenario result")
    return {"exact_change":exact,"linear_change":linear,
            "quadratic_change":quadratic,"linear_error":exact-linear,
            "quadratic_error":exact-quadratic,
            "absolute_linear_error":abs(exact-linear),
            "absolute_quadratic_error":abs(exact-quadratic)}

def parallel_report(flows,rate,shock_bp_grid,error_tolerance=None):
    items=validate_flows(flows)
    r=finite(rate,"rate")
    if error_tolerance is not None:
        tol=finite(error_tolerance,"error_tolerance")
        if tol<0:
            raise ValueError("error_tolerance must be nonnegative")
    else:
        tol=None
    terms=[c*math.exp(-r*t) for c,t in items]
    value=math.fsum(terms)
    first=-math.fsum(t*v for (_,t),v in zip(items,terms))
    second=math.fsum(t*t*v for (_,t),v in zip(items,terms))
    if not all(math.isfinite(x) for x in (value,first,second)) or value<=0:
        raise ValueError("baseline value and derivatives must be finite")
    scenarios=[]
    for bp in shock_bp_grid:
        b=finite(bp,"shock_bp")
        h=bp_to_decimal(b)
        data=scenario_from_terms(terms,[t for _,t in items],[h]*len(items))
        data.update({"shock_bp":b,"shock_decimal":h,
                     "exact_value":value+data["exact_change"],
                     "linear_value":value+data["linear_change"],
                     "quadratic_value":value+data["quadratic_change"]})
        if tol is not None:
            data["linear_within_tolerance"]=data["absolute_linear_error"]<=tol
            data["quadratic_within_tolerance"]=data["absolute_quadratic_error"]<=tol
        scenarios.append(data)
    return {"model":"positive fixed cash flows; flat continuous annual rate",
            "baseline_rate":r,"baseline_value":value,
            "first_derivative":first,"second_derivative":second,
            "duration":-first/value,"convexity":second/value,
            "cash_flows":[{"cash":c,"years":t} for c,t in items],
            "error_tolerance_currency":tol,"scenarios":scenarios}

def spot_scenario(flows,spot_rates,shock_bp):
    items=validate_flows(flows)
    rates=[finite(x,"spot_rate") for x in spot_rates]
    bumps=[bp_to_decimal(x) for x in shock_bp]
    if len(items)!=len(rates) or len(items)!=len(bumps):
        raise ValueError("one spot rate and shock required per cash flow")
    terms=[c*math.exp(-z*t) for (c,t),z in zip(items,rates)]
    value=math.fsum(terms)
    if not math.isfinite(value) or value<=0:
        raise ValueError("baseline spot value must be finite and positive")
    data=scenario_from_terms(terms,[t for _,t in items],bumps)
    return {"model":"independent cash-flow spot rates; continuous annual",
            "baseline_value":value,"spot_rates":rates,
            "shock_bp":[finite(x,"shock_bp") for x in shock_bp],
            **data}

if __name__=="__main__":
    flows=[(100,1),(1100,2)]
    result={
        "parallel":parallel_report(flows,0.04,
                                   [-100,-50,-25,-10,0,10,25,50,100],
                                   error_tolerance=0.25),
        "nonparallel":spot_scenario(flows,[0.035,0.04],[10,-20])}
    print(json.dumps(result,indent=2,allow_nan=False))
