"""Independent analytic reference checks for Book 02 Section 16.9."""
import math
from fractions import Fraction
from unittest.mock import patch
from section_16_09 import (TRAIN,HOLDOUT,STARTS,assessment,finite,price,
                           objective,gradient,curvature,analytical_rate,
                           optimize,price_metrics)

def near(a,b):
    assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-8),(a,b)

def rejects(exc,fn,*args,**kwargs):
    try:
        fn(*args,**kwargs)
    except exc:
        return
    raise AssertionError("expected "+str(exc))

def check_candidate_evidence():
    a=assessment()
    for item in a["runs"]:
        r=Fraction(str(item["rate"]))
        for name,rows in (("training",TRAIN),("holdout",HOLDOUT)):
            residuals=tuple(float(1000+1000*Fraction(str(time))*r-Fraction(str(value)))
                            for time,value in rows)
            actual=item[name]
            assert len(actual["residuals"])==len(residuals)
            for observed,expected in zip(actual["residuals"],residuals):
                near(observed,expected)
            near(actual["mae"],sum(abs(e) for e in residuals)/len(residuals))
            near(actual["rmse"],math.sqrt(sum(e*e for e in residuals)/len(residuals)))
            near(actual["bias"],sum(residuals)/len(residuals))
            near(actual["max_abs"],max(abs(e) for e in residuals))
        near(item["recomputed_gradient"],float(14*(r-Fraction(1,20))))
        near(item["recomputed_loss"],float(7*(r-Fraction(1,20))**2))
        assert item["provisional_acceptance"] is True

    def candidate(rate=0.05,status="gradient_tolerance",reported_gradient=0):
        return {"rate":rate,"status":status,"gradient":reported_gradient}
    for fake in (candidate(status="max_iterations"),
                 candidate(rate=0.06),
                 candidate(reported_gradient=1),
                 candidate(rate=0.05+1e-9),
                 candidate(rate=0.05+8e-9)):
        with patch("section_16_09.optimize",side_effect=lambda *args, fake=fake:dict(fake)):
            rejected=assessment()
        assert rejected["provisional_acceptance"] is False
        assert all(item["provisional_acceptance"] is False for item in rejected["runs"])
    with patch("section_16_09.optimize",side_effect=lambda *args:candidate(rate=0.05+1e-9)):
        rejected=assessment()
    assert abs(rejected["runs"][0]["recomputed_gradient"])>1e-8

    with patch("section_16_09.HOLDOUT",((4.0,1203.0),)):
        rejected=assessment()
    near(rejected["analytical_rate"],0.05)
    assert rejected["provisional_acceptance"] is False
    for item in rejected["runs"]:
        near(item["holdout"]["residuals"][0],float(4000*Fraction(str(item["rate"]))-203))
        assert item["provisional_acceptance"] is False

    with patch("section_16_09.optimize",
               side_effect=lambda start,method:optimize(start,method,max_iterations=1)):
        partial=assessment()
    assert partial["provisional_acceptance"] is False
    assert any(item["status"]=="max_iterations" for item in partial["runs"])
    for rows in ((),((0,1000),),((1,float("nan")),),((True,1000),),((1,),)):
        rejects((ValueError,TypeError),price_metrics,0.05,rows)

def run():
    check_candidate_evidence()
    a=assessment()
    near(a["analytical_rate"],0.05)
    near(a["curvature"],14)
    near(objective(0.05),0)
    near(gradient(0.05),0)
    near(gradient(0),-0.7)
    near(price(0.05,4),1200)
    assert len(a["runs"])==6
    assert len(STARTS)==3
    for item in a["runs"]:
        assert item["status"]=="gradient_tolerance"
        near(item["rate"],0.05)
        assert abs(item["gradient"])<=1e-9
    for item in a["runs"]:
        if item["method"]=="newton" and item["start"]!=0.05:
            assert item["iterations"]==1
    near(a["training"]["mae"],0)
    near(a["training"]["rmse"],0)
    assert a["holdout"]["residuals"]==(-1.0,)
    near(a["holdout"]["rmse"],1)
    near(price_metrics(0.05,HOLDOUT)["bias"],-1)
    near(analytical_rate(TRAIN),0.05)
    assert a["provisional_acceptance"] is True
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,optimize,0,method="unknown")
    rejects(ValueError,optimize,0,step=0)
    rejects(ValueError,optimize,0,max_iterations=0)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 16.9 independent analytic reference checks")

if __name__=="__main__":
    run()
