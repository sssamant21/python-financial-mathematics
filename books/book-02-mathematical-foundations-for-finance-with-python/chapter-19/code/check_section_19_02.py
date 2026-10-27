"""Independent analytic reference checks for Book 02 Section 19.2."""
import math
from section_19_02 import (assessment,finite,growth,variable_growth,logistic,
                            quadratic_growth,proportional_withdrawals)

def near(a,b,rel=1e-11,abs_=1e-10):
    assert math.isclose(a,b,rel_tol=rel,abs_tol=abs_),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    near(a["exponential_growth"],1000*math.exp(0.12))
    near(growth(0,0.04,3),0)
    near(growth(1000,-0.04,3),1000*math.exp(-0.12))
    near(a["variable_growth"],1000*math.exp(0.03*5+0.001*25))
    near(variable_growth(1000,0.03,0.002,0),1000)
    expected_logistic=1000/(1+4*math.exp(-2))
    near(a["logistic"],expected_logistic)
    near(logistic(200,0.4,1000,0),200)
    near(logistic(1000,0.4,1000,5),1000)
    near(a["logistic_zero_equilibrium"],0)
    near(a["quadratic_growth_before_singularity"],200)
    near(a["quadratic_singularity_time"],10)
    near(a["proportional_withdrawals"],1000*math.exp(-0.1))
    # Analytical ODE identity: logistic derivative = r*A*(1-A/K).
    t=2
    q=4*math.exp(-0.4*t)
    exact_derivative=1000*0.4*q/(1+q)**2
    balance=logistic(200,0.4,1000,t)
    near(exact_derivative,0.4*balance*(1-balance/1000))
    rejects(ValueError,logistic,-1,0.4,1000,5)
    rejects(ValueError,logistic,200,0.4,0,5)
    rejects(ValueError,quadratic_growth,100,0.001,10)
    rejects(ValueError,quadratic_growth,100,0.001,11)
    rejects(ValueError,proportional_withdrawals,1000,0.04,-0.06,5)
    rejects(ValueError,growth,1000,0.04,-1)
    rejects(ValueError,finite,float("nan"),"value")
    rejects(TypeError,finite,True,"value")
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 19.2 independent analytic reference checks")

if __name__=="__main__":
    run()
