"""Section 9.8: reproducible valuation sensitivity and scenario reports."""
import json
import math
from fractions import Fraction
from decimal import Decimal, Context, localcontext

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
    """Complete seven-field change/error report on represented baseline terms.

    Vectors are consumed once and must have equal lengths; empty is allowed.
    Terms/times are finite nonnegative numbers; shocks finite. No independent
    baseline-value eligibility gate is added by this direct helper.
    """
    values=[finite(x,"term") for x in terms]
    times=[finite(x,"years") for x in years]
    bumps=[finite(x,"shock") for x in shocks]
    if len(values)!=len(times) or len(values)!=len(bumps):
        raise ValueError("term, time and shock vectors must have equal lengths")
    if any(x<0 for x in values) or any(x<0 for x in times):
        raise ValueError("terms and years must be nonnegative")
    with localcontext(Context(prec=1700)):
        def dec(value):return Decimal(value.numerator)/Decimal(value.denominator)
        def reported(value):
            result=float(value)
            if not math.isfinite(result):
                raise ValueError("scenario report outside finite float range")
            return result
        exact=linear=second=Decimal(0)
        for v,t,h in zip(values,times,bumps):
            V,T,H=map(Fraction,(v,t,h))
            if V==0:
                continue
            exponent=-T*H
            if exponent>10000:
                raise ValueError("scenario report outside finite float range")
            baseline=dec(V)
            endpoint=Decimal(0) if exponent < -10000 else baseline*dec(exponent).exp()
            TT,HH=dec(T),dec(H)
            exact+=endpoint-baseline;linear-=TT*baseline*HH
            second+=TT*TT*baseline*HH*HH/2
        quadratic=linear+second
        return {"exact_change":reported(exact),"linear_change":reported(linear),
                "quadratic_change":reported(quadratic),
                "linear_error":reported(exact-linear),
                "quadratic_error":reported(exact-quadratic),
                "absolute_linear_error":reported(abs(exact-linear)),
                "absolute_quadratic_error":reported(abs(exact-quadratic))}

def _parallel_baseline(items,rate):
    """Complete positive baseline fields; latent normalization before conversion."""
    R=Fraction(rate)
    with localcontext(Context(prec=1500)):
        def dec(value):return Decimal(value.numerator)/Decimal(value.denominator)
        def reported(value):
            result=float(value)
            if not math.isfinite(result):
                raise ValueError("baseline report outside finite float range")
            return result
        value=first=second=Decimal(0);amounts=[]
        for cash,years in items:
            C,T=map(Fraction,(cash,years));exponent=-R*T
            if exponent>10000:
                raise ValueError("baseline report outside finite float range")
            amount=Decimal(0) if exponent < -10000 else dec(C)*dec(exponent).exp()
            TT=dec(T);value+=amount;first-=TT*amount;second+=TT*TT*amount
            amounts.append(amount)
        v=reported(value)
        if v<=0:
            raise ValueError("baseline value must report positive")
        return ([reported(x) for x in amounts],v,reported(first),reported(second),
                reported(-first/value),reported(second/value))

def _parallel_row(items,rate,shock):
    """Complete facade row from original cash/rate inputs, before rounding."""
    R,H=map(Fraction,(rate,shock))
    with localcontext(Context(prec=1700)):
        def dec(value):return Decimal(value.numerator)/Decimal(value.denominator)
        def amount(C,exponent):
            if exponent>10000:
                raise ValueError("parallel row outside finite float range")
            return Decimal(0) if exponent < -10000 else dec(C)*dec(exponent).exp()
        def reported(value):
            result=float(value)
            if not math.isfinite(result):
                raise ValueError("parallel row outside finite float range")
            return result
        baseline=shifted=first=second=Decimal(0)
        for cash,years in items:
            C,T=map(Fraction,(cash,years));v=amount(C,-R*T);TT=dec(T)
            baseline+=v;shifted+=amount(C,-(R+H)*T)
            first-=TT*v;second+=TT*TT*v
        HH=dec(H);exact=shifted-baseline;linear=first*HH
        quadratic=linear+second*HH*HH/2
        return {"exact_change":reported(exact),"linear_change":reported(linear),
                "quadratic_change":reported(quadratic),
                "linear_error":reported(exact-linear),
                "quadratic_error":reported(exact-quadratic),
                "absolute_linear_error":reported(abs(exact-linear)),
                "absolute_quadratic_error":reported(abs(exact-quadratic)),
                "exact_value":reported(shifted),
                "linear_value":reported(baseline+linear),
                "quadratic_value":reported(baseline+quadratic)}

def parallel_report(flows,rate,shock_bp_grid,error_tolerance=None):
    items=validate_flows(flows)
    r=finite(rate,"rate")
    if error_tolerance is not None:
        tol=finite(error_tolerance,"error_tolerance")
        if tol<0:
            raise ValueError("error_tolerance must be nonnegative")
    else:
        tol=None
    _terms,value,first,second,duration,convexity=_parallel_baseline(items,r)
    scenarios=[]
    for bp in shock_bp_grid:
        b=finite(bp,"shock_bp")
        h=bp_to_decimal(b)
        data=_parallel_row(items,r,h)
        data.update({"shock_bp":b,"shock_decimal":h})
        if tol is not None:
            data["linear_within_tolerance"]=data["absolute_linear_error"]<=tol
            data["quadratic_within_tolerance"]=data["absolute_quadratic_error"]<=tol
        scenarios.append(data)
    return {"model":"positive fixed cash flows; flat continuous annual rate",
            "baseline_rate":r,"baseline_value":value,
            "first_derivative":first,"second_derivative":second,
            "duration":duration,"convexity":convexity,
            "cash_flows":[{"cash":c,"years":t} for c,t in items],
            "error_tolerance_currency":tol,"scenarios":scenarios}

def spot_scenario(flows,spot_rates,shock_bp):
    items=validate_flows(flows)
    rates=[finite(x,"spot_rate") for x in spot_rates]
    used_bp=[finite(x,"basis_points") for x in shock_bp]
    bumps=[bp_to_decimal(x) for x in used_bp]
    if len(items)!=len(rates) or len(items)!=len(bumps):
        raise ValueError("one spot rate and shock required per cash flow")
    terms=[c*math.exp(-z*t) for (c,t),z in zip(items,rates)]
    value=math.fsum(terms)
    if not math.isfinite(value) or value<=0:
        raise ValueError("baseline spot value must be finite and positive")
    data=scenario_from_terms(terms,[t for _,t in items],bumps)
    return {"model":"independent cash-flow spot rates; continuous annual",
            "baseline_value":value,"spot_rates":rates,
            "shock_bp":used_bp,
            **data}

if __name__=="__main__":
    flows=[(100,1),(1100,2)]
    result={
        "parallel":parallel_report(flows,0.04,
                                   [-100,-50,-25,-10,0,10,25,50,100],
                                   error_tolerance=0.25),
        "nonparallel":spot_scenario(flows,[0.035,0.04],[10,-20])}
    print(json.dumps(result,indent=2,allow_nan=False))
