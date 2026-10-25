"""Section 10.10: Chapter 10 integrated assessment and numerical evidence."""
import json
import math

from section_10_09 import (Stream,Curve,analytic_pv,numerical_pv,
                           discrete_pv,portfolio_pv,parallel_shift_derivative)
from section_10_07 import integrate

def assessment():
    streams=[Stream("constant",1000),Stream("linear",200,50),
             Stream("exponential",150,0.02)]
    payments=[(2,500)]
    flat=Curve(0.05)
    affine=Curve(0.03,0.005)
    exact_components=[analytic_pv(s,flat,4) for s in streams]
    exact_discrete=discrete_pv(payments,flat)
    exact_total=math.fsum(exact_components+[exact_discrete])
    grids=[]
    for n in (128,256,512):
        result=portfolio_pv(streams,payments,flat,4,n)
        grids.append({"subintervals":n,"total_pv":result["total"],
                      "absolute_error":abs(result["total"]-exact_total)})
    affine_value=portfolio_pv(streams,payments,affine,4,512)
    examples={
        "accumulation_linear":1470,
        "fundamental_theorem_at_2":1280/3,
        "substitution_integral":-math.expm1(-4),
        "level_stream_pv":1500*(-math.expm1(-0.16))/0.04,
        "growing_stream_pv":800*(-math.expm1(-0.125))/0.025,
        "growth_matches_discount_pv":4000,
        "zero_rate_linear_pv":2200,
        "level_perpetuity_pv":20000,
        "growing_perpetuity_pv":30000,
        "tail_one_percent_years":math.log(100)/0.04,
        "discrete_two_payments_pv":500*(math.exp(-0.05)+math.exp(-0.10)),
        "quadrature_midpoint":integrate(lambda t:t*t,0,1,2,"midpoint"),
        "quadrature_trapezoid":integrate(lambda t:t*t,0,1,2,"trapezoid"),
        "quadrature_simpson":integrate(lambda t:t*t,0,1,2,"simpson"),
    }
    return {"examples":examples,"integrated_case":{
        "flat_analytic_components":exact_components,
        "flat_analytic_discrete":exact_discrete,
        "flat_analytic_total":exact_total,
        "simpson_reconciliation":grids,
        "affine_numerical_total":affine_value["total"],
        "flat_rate_derivative_1bp_bump":parallel_shift_derivative(
            streams,payments,flat,4,512,0.0001),
        "affine_rate_derivative_1bp_bump":parallel_shift_derivative(
            streams,payments,affine,4,512,0.0001),
    },"runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
