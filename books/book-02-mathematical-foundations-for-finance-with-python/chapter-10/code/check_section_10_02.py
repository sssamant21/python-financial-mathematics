"""Independent reference checks for Section 10.2."""
import math
from section_10_02 import (
    finite,polynomial_antiderivative,polynomial_definite,
    exponential_definite,midpoint_sum)

def close(a,b,rel_tol=1e-9,abs_tol=1e-9):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    close(polynomial_antiderivative([0,0,6],2,5),21)
    close(polynomial_antiderivative([100,20],2),240)
    close(polynomial_definite([100,20],0,2),240)
    close(polynomial_definite([-1,1],0,2),0)
    close(polynomial_definite([0,0,3],2,0),-8)
    close(polynomial_definite([2,3,4],1,1),0)
    close(polynomial_definite([0,0,1],0,1),1/3)
    for coeff in ([3,2],[1,-2,4],[0,0,6]):
        x=0.7
        h=1e-5
        numerical=(polynomial_antiderivative(coeff,x+h)-polynomial_antiderivative(coeff,x-h))/(2*h)
        expected=math.fsum(c*x**i for i,c in enumerate(coeff))
        close(numerical,expected,rel_tol=1e-7)
    c,k=500,0.03
    exact=c*math.expm1(2*k)/k
    close(exponential_definite(c,k,0,2),exact)
    close(exponential_definite(c,0,0,2),1000)
    close(exponential_definite(c,k,2,0),-exact)
    close(exponential_definite(c,k,0,2),
          exponential_definite(c,k,0,1)+exponential_definite(c,k,1,2))
    errors=[abs(midpoint_sum(lambda t:c*math.exp(k*t),0,2,n)-exact)
            for n in (4,16,64)]
    assert errors[0]>errors[1]>errors[2]
    close(midpoint_sum(lambda t:100+20*t,0,2,4),240)
    rejects(ValueError,polynomial_antiderivative,[],1)
    rejects(ValueError,midpoint_sum,lambda t:t,0,1,0)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("inf"),"value")
    print("PASS: Section 10.2 independent reference checks")

if __name__=="__main__":
    run()
