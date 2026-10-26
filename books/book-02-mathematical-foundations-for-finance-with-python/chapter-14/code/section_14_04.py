"""Book 02 Section 14.4: tolerance-aware definiteness of symmetric 2x2 matrices."""
import json
import math
from section_14_01 import eigenpairs_symmetric_2x2,finite

def classify(matrix,absolute_eigenvalue_tolerance=0.0):
    tolerance=finite(absolute_eigenvalue_tolerance,"absolute eigenvalue tolerance")
    if tolerance<0:
        raise ValueError("absolute eigenvalue tolerance must be nonnegative")
    eig=eigenpairs_symmetric_2x2(matrix)
    values=eig["eigenvalues"]
    signs=tuple(1 if v>tolerance else (-1 if v<-tolerance else 0) for v in values)
    if all(s>0 for s in signs):
        label="positive_definite"
    elif all(s<0 for s in signs):
        label="negative_definite"
    elif any(s>0 for s in signs) and any(s<0 for s in signs):
        label="indefinite"
    elif any(s>0 for s in signs):
        label="positive_semidefinite"
    elif any(s<0 for s in signs):
        label="negative_semidefinite"
    else:
        label="numerically_zero"
    return {"classification":label,"eigenvalues":values,
            "eigenvalue_signs":signs,
            "absolute_eigenvalue_tolerance":tolerance,
            "determinant":eig["determinant"],
            "trace":eig["trace"],
            "runtime_certified":False}

def assessment():
    cases={
        "positive_definite":((2,1),(1,2)),
        "positive_semidefinite":((1,1),(1,1)),
        "indefinite":((1,0),(0,-1)),
        "negative_definite":((-2,0),(0,-1)),
        "negative_semidefinite":((-1,0),(0,0)),
        "numerically_zero":((0,0),(0,0))
    }
    return {"cases":{name:classify(matrix) for name,matrix in cases.items()},
            "independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
