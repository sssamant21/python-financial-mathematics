"""Independent analytic reference checks for Book 02 Section 17.9."""
import math
from fractions import Fraction
from section_17_09 import (assessment,finite,validate_caps,objective,
                           gradient,verify_candidate,optimize,financial_report)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-9),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_certificate_fields(weights,lam,multipliers,caps=(0.6,1),expected_pass=None):
    report=verify_candidate(weights,lam,multipliers,caps)
    x,y=(Fraction(str(v)) for v in weights)
    u,v=(Fraction(str(z)) for z in caps)
    multiplier=tuple(Fraction(str(z)) for z in multipliers)
    lagrange=Fraction(str(lam))
    # Differentiate the explicit variance polynomial using rational constants.
    stationarity=(2*x/25+y/50+lagrange-multiplier[0]+multiplier[2],
                  x/50+9*y/50+lagrange-multiplier[1]+multiplier[3])
    inequalities=(-x,-y,x-u,y-v)
    products=tuple(a*b for a,b in zip(multiplier,inequalities))
    equality=x+y-1
    expected={
        "equality_residual":equality,
        "primal_violation":max(abs(equality),*(max(0,z) for z in inequalities)),
        "dual_violation":max(0,*(-z for z in multiplier)),
        "stationarity_norm":max(abs(z) for z in stationarity),
        "complementarity_norm":max(abs(z) for z in products),
        "objective":x*x/25+x*y/50+9*y*y/100,
    }
    for key,value in expected.items():
        near(report[key],float(value))
    for key,values in (("inequality_residuals",inequalities),
                       ("stationarity",stationarity),("complementarity",products)):
        assert len(report[key])==len(values)
        for actual,value in zip(report[key],values):
            near(actual,float(value))
    if expected_pass is not None:
        assert report["passes"] is expected_pass
    return report

def check_independent_kkt():
    for caps in ((0.6,1),(1,1),(1,0.2),(0.6,0.4)):
        candidate=optimize(*caps)
        check_certificate_fields(candidate["weights"],candidate["lambda"],
                                 candidate["multipliers"],caps,True)
    # Isolate each residual family: the other three norms are zero.
    equality=check_certificate_fields((0,0),0,(0,0,0,0),(1,1),False)
    near(equality["primal_violation"],1)
    for key in ("dual_violation","stationarity_norm","complementarity_norm"):
        near(equality[key],0)
    dual=check_certificate_fields((0,1),-0.18,(-0.16,0,0,0),(1,1),False)
    near(dual["dual_violation"],0.16)
    for key in ("primal_violation","stationarity_norm","complementarity_norm"):
        near(dual[key],0)
    stationarity=check_certificate_fields((0.5,0.5),0,(0,0,0,0),(1,1),False)
    near(stationarity["stationarity_norm"],0.1)
    for key in ("primal_violation","dual_violation","complementarity_norm"):
        near(stationarity[key],0)
    complementarity=check_certificate_fields((0.5,0.5),0,(0.05,0.1,0,0),(1,1),False)
    near(complementarity["complementarity_norm"],0.05)
    for key in ("primal_violation","dual_violation","stationarity_norm"):
        near(complementarity[key],0)
    # The second-cap multiplier has a separate closed-form benchmark.
    near(optimize(1,0.2)["multipliers"][3],0.016)

def check_financial_range():
    for capital,cost_bps in ((1000000,10),(1e308,10),(1e-308,1e308),(5e-324,1e308)):
        result=financial_report((1,0),(0.5,0.5),capital,cost_bps)
        # Trade weights differ by exact halves; at the smallest subnormal,
        # individual trades underflow. The reported cost uses reported gross.
        gross=result["gross_traded_notional"]
        expected_cost=float(Fraction.from_float(gross)*Fraction.from_float(float(cost_bps))/10000)
        assert math.isclose(result["modeled_transaction_cost"],expected_cost,
                            rel_tol=1e-12,abs_tol=0)
        near(result["gross_turnover"],1)
        for key in ("expected_return","gross_turnover","gross_traded_notional","modeled_transaction_cost"):
            assert math.isfinite(result[key])
        assert all(math.isfinite(value) for value in result["signed_trades"])
    huge=financial_report((1,0),(0.5,0.5),1e308,10)
    assert math.isclose(huge["modeled_transaction_cost"],1e305,rel_tol=1e-12)
    # A smallest-subnormal gross with a huge cost multiplier remains nonzero.
    tiny=financial_report((1,0),(0,1),5e-324,1e308)
    expected=float(Fraction.from_float(1e-323)*Fraction.from_float(1e308)/10000)
    assert tiny["modeled_transaction_cost"]==expected>0
    idle=financial_report((0.5,0.5),(0.5,0.5),1e308,1e308)
    assert idle["gross_turnover"]==idle["gross_traded_notional"]==idle["modeled_transaction_cost"]==0
    rejects(OverflowError,financial_report,(1,0),(0,1),1e308,10)
    rejects(OverflowError,financial_report,(1,0),(0.5,0.5),1e308,1e308)
    rejects(TypeError,financial_report,(1,0),(0,1),True,10)
    rejects(TypeError,financial_report,(1,0),(0,1),100,True)

def run():
    check_financial_range()
    check_independent_kkt()
    a=assessment()
    s=a["allocation"]
    assert s["certificate"]["passes"]
    near(s["weights"][0],0.6)
    near(s["weights"][1],0.4)
    near(s["variance"],0.0336)
    near(s["lambda"],-0.084)
    near(s["multipliers"][2],0.028)
    near(objective((0.6,0.4)),0.0336)
    near(gradient((0.6,0.4))[0],0.056)
    near(gradient((0.6,0.4))[1],0.084)
    f=a["financial_report"]
    near(f["expected_return"],0.068)
    near(f["gross_turnover"],0.2)
    near(f["gross_traded_notional"],200000)
    near(f["modeled_transaction_cost"],200)
    assert not f["taxes_included"]
    assert not f["market_impact_included"]
    # Inactive first cap: unconstrained-on-budget benchmark.
    unconstrained=optimize(1,1)
    assert unconstrained["certificate"]["passes"]
    near(unconstrained["weights"][0],8/11)
    near(unconstrained["variance"],7/220)
    # Binding second cap: the optimizer must certify the opposite regime.
    second_cap=optimize(1,0.2)
    assert second_cap["certificate"]["passes"]
    near(second_cap["weights"][0],0.8)
    near(second_cap["weights"][1],0.2)
    assert second_cap["multipliers"][3]>0
    # Both caps exactly sum to one: feasible but multiplier nonuniqueness.
    endpoint=optimize(0.6,0.4)
    assert endpoint["certificate"]["passes"]
    # Negative cases: feasibility, stationarity, and multiplier signs.
    bad=verify_candidate((0.7,0.3),-0.084,(0,0,0.028,0))
    assert not bad["passes"] and bad["primal_violation"]>0
    nonstationary=verify_candidate((0.5,0.5),0,(0,0,0,0))
    assert not nonstationary["passes"]
    wrong_sign=verify_candidate((0.6,0.4),-0.084,(0,0,-0.028,0))
    assert not wrong_sign["passes"]
    rejects(ValueError,validate_caps,0.4,0.4)
    # A tolerance in the certificate must not turn an empty interval feasible.
    rejects(ValueError,optimize,0.5,0.499999999999995)
    assert optimize(0.5,0.5)["certificate"]["passes"]
    rejects(ValueError,optimize,-0.1,1)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,financial_report,(0.6,0.4),(0.5,0.5),-1)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 17.9 independent analytic reference checks")

if __name__=="__main__":
    run()
