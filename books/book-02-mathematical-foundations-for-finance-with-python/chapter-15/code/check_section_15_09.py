"""Independent analytic reference checks for Book 02 Section 15.9."""
import math
from section_15_09 import (assessment,valuation,jacobian,hessians,
                           scenario,centered_jacobian_column)

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-7,abs_tol=1e-7),(a,b)

def vector(a,b):
    assert len(a)==len(b)
    for x,y in zip(a,b):
        close(x,y)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    a=assessment()
    e=math.exp(0.1)
    d=math.exp(-0.1)
    vector(a["base_values"],(1000*e,500*d))
    vector(a["shocked_values"],(1100*math.exp(0.15),550*math.exp(-0.15)))
    vector(a["jacobian"][0],(e,2000*e,50*e))
    vector(a["jacobian"][1],(0.5*d,-1000*d,-25*d))
    h1,h2=a["hessians"]
    vector(h1[0],(0,2*e,0.05*e))
    vector(h1[1],(2*e,4000*e,1100*e))
    vector(h1[2],(0.05*e,1100*e,2.5*e))
    vector(h2[0],(0,-d,-0.025*d))
    vector(h2[1],(-d,2000*d,-450*d))
    vector(h2[2],(-0.025*d,-450*d,1.25*d))
    for h in (h1,h2):
        for i in range(3):
            for j in range(3):
                close(h[i][j],h[j][i])
    vector(a["exact_changes"],(
        1100*math.exp(0.15)-1000*e,
        550*math.exp(-0.15)-500*d))
    vector(a["first_order_changes"],(145*e,27.5*d))
    for i in range(2):
        close(a["first_order_errors"][i],
              a["first_order_changes"][i]-a["exact_changes"][i])
        close(a["second_order_errors"][i],
              a["second_order_changes"][i]-a["exact_changes"][i])
    close(a["portfolio_exact_change"],sum(a["exact_changes"]))
    close(a["portfolio_first_order_change"],sum(a["first_order_changes"]))
    close(a["portfolio_second_order_change"],sum(a["second_order_changes"]))
    for col in range(3):
        vector(a["finite_difference_columns"][col],
               (a["jacobian"][0][col],a["jacobian"][1][col]))
    zero=scenario((1000,0.05,2),(0,0,0))
    vector(zero["exact_changes"],(0,0))
    vector(zero["first_order_changes"],(0,0))
    vector(zero["second_order_changes"],(0,0))
    rejects(ValueError,valuation,0,0.05,2)
    rejects(ValueError,scenario,(1000,0.05,2),(-1100,0,0))
    rejects(ValueError,scenario,(1000,0.05,2),(0,0,-3))
    rejects(ValueError,centered_jacobian_column,(1000,0.05,0),2,1e-4)
    rejects(TypeError,valuation,True,0.05,2)
    rejects(ValueError,valuation,1000,float("nan"),2)
    assert a["runtime_certified"] is False
    assert a["independent_review_completed"] is False
    print("PASS: Section 15.9 independent reference checks")

if __name__=="__main__":
    run()
