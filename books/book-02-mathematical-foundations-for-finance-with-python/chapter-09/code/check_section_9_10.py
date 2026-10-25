"""Independent checks for Section 9.10 cumulative assessment."""
import math
from section_9_10 import assessment
from section_9_09 import project_report
from section_9_07 import call_payoff,put_payoff,call_slopes,put_slopes

def close(a,b):
    assert math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-8),(a,b)

def run():
    result=assessment()
    flows=[(120,0.5),(120,1),(120,2),(1120,3)]
    discounted=[c*math.exp(-0.04*t) for c,t in flows]
    value=math.fsum(discounted)
    first=-math.fsum(t*v for (_,t),v in zip(flows,discounted))
    second=math.fsum(t*t*v for (_,t),v in zip(flows,discounted))
    close(result["baseline_value"],value)
    close(result["duration"],-first/value)
    close(result["convexity"],second/value)
    assert len(result["scenarios"])==7
    for row in result["scenarios"]:
        h=row["shock_bp"]/10000
        exact=math.fsum(v*math.expm1(-t*h) for (_,t),v in zip(flows,discounted))
        close(row["exact_change"],exact)
        close(row["linear_change"],first*h)
        close(row["quadratic_change"],first*h+0.5*second*h*h)
        assert row["linear_bound_pass"] and row["quadratic_bound_pass"]
        if h==0:
            close(exact,0)
        elif h>0:
            assert exact<0
        else:
            assert exact>0
    for spot in (98,100,102):
        close(call_payoff(spot,100)-put_payoff(spot,100),spot-100)
    assert not call_slopes(100,100)["differentiable"]
    assert not put_slopes(100,100)["differentiable"]
    close((call_payoff(102,100)-call_payoff(98,100))/4,0.5)
    close(25/10000,0.0025)
    close(-75/10000,-0.0075)
    assert result["runtime_certified"] is False
    assert result["independent_review_completed"] is False
    print("PASS: Section 9.10 cumulative reference checks")

if __name__=="__main__":
    run()
