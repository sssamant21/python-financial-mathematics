"""Book 02 Chapter 13 closing assessment: reference calculations."""
import json
from section_13_06 import assessment as qr_assessment
from section_13_07 import assessment as weighted_assessment
from section_13_08 import assessment as ridge_assessment
from section_13_09 import assessment as project_assessment

def assessment():
    qr=qr_assessment()["reference"]
    weighted=weighted_assessment()["reference"]
    ridge=ridge_assessment()["reference"]
    project=project_assessment()["reference"]
    return {"chapter":"13","section":"13.10",
            "qr_positions":qr["positions"],
            "qr_objective":qr["objective_half_squared_l2"],
            "weighted_position":weighted["position"],
            "weighted_objective":weighted["weighted_objective"],
            "ridge_positions":ridge["positions"],
            "ridge_total_objective":ridge["total_objective"],
            "project_decision":project["decision"],
            "runtime_certified":False,
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
