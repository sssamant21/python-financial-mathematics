"""Section 9.10: cumulative Chapter 09 applied assessment."""
import json
import math
from section_9_09 import project_report
from section_9_07 import call_payoff, call_slopes

def assessment():
    flows=[(120,0.5),(120,1),(120,2),(1120,3)]
    report=project_report(flows,0.04,[-100,-50,-25,0,25,50,100])
    assert report["convexity"]+1e-12>=report["duration"]**2
    assert all(row["linear_bound_pass"] and row["quadratic_bound_pass"]
               for row in report["scenarios"])
    assert call_slopes(100,100)["left"]==0
    assert call_slopes(100,100)["right"]==1
    assert call_payoff(102,100)==2
    assert math.isclose(25/10000,0.0025)
    return {"assessment":"Chapter 09 cumulative",
            "baseline_value":report["baseline_value"],
            "duration":report["duration"],
            "convexity":report["convexity"],
            "scenarios":report["scenarios"],
            "in_model_checks_passed":True,
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
