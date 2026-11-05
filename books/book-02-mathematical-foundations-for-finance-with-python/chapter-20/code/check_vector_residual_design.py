"""Selected Section 20.5 design exercises, not a general vector-solver API."""
from fractions import Fraction as F
import json
import math
from section_20_05 import close_to_reference, errors


def check():
    rows=[]
    for n,expected_norm in ((4,.25),(64,1.)):
        delta=.125
        actual=[delta]*n
        reference=[0.]*n
        squared=sum((F(a)-F(b))**2 for a,b in zip(actual,reference))
        assert squared==F(expected_norm)**2
        component_decisions=[close_to_reference(a,b,atol=delta,rtol=0)
                             for a,b in zip(actual,reference)]
        norm=math.hypot(*(a-b for a,b in zip(actual,reference)))
        norm_decision=close_to_reference(norm,0,atol=delta,rtol=0)
        passed=all(component_decisions) and norm==expected_norm and not norm_decision
        rows.append(dict(kind='vector',dimension=n,component_tolerance=delta,
                         components_pass=all(component_decisions),norm=norm,
                         expected_norm=expected_norm,norm_pass=norm_decision,passed=passed))
    for exponent in (10,20,40,100):
        eps=F(1,2**exponent)
        A=((F(1),F(0)),(F(0),eps))
        b=(F(1),eps);candidate=(F(1),F(0));solution=(F(1),F(1))
        residual=tuple(sum(A[i][j]*candidate[j] for j in range(2))-b[i] for i in range(2))
        matrix_norm=max(sum(abs(v) for v in row) for row in A)
        state_norm=max(abs(v) for v in candidate)
        rhs_norm=max(abs(v) for v in b)
        residual_norm=max(abs(v) for v in residual)
        beta=residual_norm/(matrix_norm*state_norm+rhs_norm)
        forward=max(abs(candidate[i]-solution[i]) for i in range(2))/max(abs(v) for v in solution)
        accepted=close_to_reference(float(beta),0,atol=float(eps),rtol=0)
        passed=(residual==(0,-eps) and beta==eps/2 and forward==1
                and accepted and errors(float(candidate[1]),float(solution[1]))==(1.,1.))
        rows.append(dict(kind='scaled residual',epsilon=str(eps),residual=list(map(str,residual)),
                         scaled_residual=str(beta),relative_solution_error=str(forward),
                         residual_pass=accepted,condition_infinity=str(1/eps),passed=passed))
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
