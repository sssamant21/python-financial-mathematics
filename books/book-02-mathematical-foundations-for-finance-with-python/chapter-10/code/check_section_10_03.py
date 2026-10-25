"""Independent reference checks for Section 10.3."""
import math
from section_10_03 import (
    finite,polynomial_value,polynomial_accumulation,balance,
    endpoint_derivative,rolling_accumulation,rolling_derivative,centered_derivative)

def close(a,b,rel_tol=1e-8,abs_tol=1e-8):
    assert math.isclose(a,b,rel_tol=rel_tol,abs_tol=abs_tol),(a,b)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def run():
    coeff=[600,50]
    close(polynomial_accumulation(coeff,0,3),2025)
    close(balance(1000,coeff,0,3),3025)
    close(polynomial_value(coeff,2),700)
    for t in (0.5,1,2,2.5):
        close(centered_derivative(lambda x:polynomial_accumulation(coeff,0,x),t),
              polynomial_value(coeff,t))
    close(polynomial_accumulation([3,2],0,4),28)
    close(polynomial_accumulation([0,4],1,3),16)
    close(polynomial_accumulation([-1,1],0,2),0)
    close(endpoint_derivative([1,1],0,4,0,8),40)
    close(endpoint_derivative([0,0,1],2,3,2,3),3*9-2*4)
    for t in (1,2,3):
        close(rolling_derivative(coeff,t),50)
        close(centered_derivative(lambda x:rolling_accumulation(coeff,x),t),50)
    close(polynomial_accumulation(coeff,0,3),
          polynomial_accumulation(coeff,0,1)+polynomial_accumulation(coeff,1,3))
    def jump_accumulation(t):
        return 0 if t<=1 else 2*(t-1)
    close((jump_accumulation(1)-jump_accumulation(1-1e-4))/1e-4,0)
    close((jump_accumulation(1+1e-4)-jump_accumulation(1))/1e-4,2)
    rejects(ValueError,polynomial_value,[],1)
    rejects(ValueError,rolling_accumulation,[1],1,0)
    rejects(ValueError,centered_derivative,lambda t:t,1,0)
    rejects(TypeError,finite,True,"value")
    rejects(ValueError,finite,float("nan"),"value")
    print("PASS: Section 10.3 independent reference checks")

if __name__=="__main__":
    run()
