"""Exact Armijo sufficient-decrease and selected optimizer status references."""
from fractions import Fraction as F
import math
from section_16_05 import armijo_step, gradient_descent
from section_16_07 import local_descent

def run():
    for curvature in (1.0,2.0,8.0):
        objective=lambda x,a=curvature: a*x*x/2
        gradient=lambda x,a=curvature: a*x
        boundary=1.5/curvature  # 2*(1-c)/a at c=1/4.
        for step,expected in ((math.nextafter(boundary,0.0),"accepted"),
                              (boundary,"accepted"),
                              (math.nextafter(boundary,math.inf),"line_search_failed")):
            calls=[]
            def traced(x):
                calls.append(x);return objective(x)
            result=armijo_step(1.0,traced,gradient,initial_step=step,c=0.25,max_backtracks=0)
            assert result["status"]==expected
            assert len(calls)==2 and result["backtracks"]==0
            if expected=="accepted":
                a,h=F(curvature),F(step)
                trial=F(1)-h*a
                exact_new=a*trial*trial/2
                exact_rhs=a/2-F(1,4)*h*a*a
                assert exact_new<=exact_rhs and exact_new<a/2
                assert result["new_x"]==float(trial)
                assert result["new_objective"]==float(exact_new)
            else:
                assert result["step"]==0 and result["new_x"]==1 and result["new_objective"]==curvature/2
    result=armijo_step(1,lambda x:x*x,lambda x:2*x,initial_step=1,c=0.25)
    assert result["status"]=="accepted" and result["backtracks"]==1
    assert result["step"]==0.5 and result["new_x"]==0 and result["new_objective"]==0
    calls=[]
    result=armijo_step(1,lambda x:(calls.append(x) or x*x),lambda x:2*x,
                       initial_step=8,c=0.25,max_backtracks=2)
    assert result["status"]=="line_search_failed" and result["backtracks"]==2
    assert calls==[1.0,-15.0,-7.0,-3.0]  # base + budget+1 trial evaluations.
    result=armijo_step(0,lambda x:x*x,lambda x:2*x)
    assert result["status"]=="stationary" and result["step"]==0 and result["new_x"]==0
    result=armijo_step(1e20,lambda x:x,lambda x:1)
    assert result["status"]=="stagnation" and result["new_x"]==1e20
    result=gradient_descent(1,lambda x:x*x,lambda x:2*x,step=0.25,tolerance=0,max_iterations=2)
    assert result["status"]=="max_iterations" and result["iterations"]==2
    assert [row["x"] for row in result["history"]]==[1.0,0.5,0.25]
    assert result["gradient"]==0.5 and result["objective"]==0.0625
    result=gradient_descent(0,lambda x:x*x,lambda x:2*x,tolerance=0)
    assert result["status"]=="gradient_tolerance" and result["iterations"]==0
    result=local_descent(1,step=1,tolerance=0,max_iterations=2)
    assert result["status"]=="no_descent" and result["iterations"]==0 and result["x"]==1
    result=local_descent(0,step=0.05,tolerance=0,max_iterations=1)
    assert result["status"]=="max_iterations" and result["iterations"]==1
    print("PASS: nine exact Armijo boundaries, backtracking counts and selected stationary/stagnation/budget/no-descent states")

if __name__=="__main__":
    run()
