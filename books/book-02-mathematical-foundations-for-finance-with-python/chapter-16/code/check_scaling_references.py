"""Independent Hessian/scaling references and real scalar descent modes."""
from fractions import Fraction as F
import math
from section_16_07 import raw_quadratic, scaled_quadratic, to_scaled, to_raw, assessment
from section_16_05 import gradient_descent

def run():
    # From explicit quadratics: H_raw=diag(10^6,1); dx/du=diag(1/1000,1).
    raw=(F(10**6),F(1))
    jac=(F(1,1000),F(1))
    scaled=tuple(raw[i]*jac[i]**2 for i in range(2))
    assert scaled==(1,1)
    report=assessment()
    assert report["raw_condition_number"]==max(raw)/min(raw)==10**6
    assert report["scaled_condition_number"]==max(scaled)/min(scaled)==1
    for x,y in ((0.02,3.0),(0.021,4.0),(-0.03,1.0),(0.12,-2.0)):
        u,v=to_scaled(x,y)
        assert math.isclose(raw_quadratic(x,y),scaled_quadratic(u,v),rel_tol=2e-15,abs_tol=1e-24)
        xx,yy=to_raw(u,v)
        assert math.isclose(xx,x,rel_tol=2e-15,abs_tol=1e-17) and yy==y
    # Second differences independently measure the actual objective curvatures.
    for h in (2.0**-6,2.0**-8,2.0**-10):
        for i,curvature in enumerate(raw):
            plus=[0.02,3.0];minus=plus.copy();plus[i]+=h;minus[i]-=h
            actual=(raw_quadratic(*plus)-2*raw_quadratic(0.02,3)+raw_quadratic(*minus))/(h*h)
            assert math.isclose(actual,float(curvature),rel_tol=2e-12)
        for i in range(2):
            plus=[0.,0.];minus=plus.copy();plus[i]+=h;minus[i]-=h
            actual=(scaled_quadratic(*plus)+scaled_quadratic(*minus))/(h*h)
            assert actual==1
    # This calls the real scalar solver for individual diagonal modes; it is
    # not a claim that the module exposes a two-dimensional optimizer.
    for a in (1.0,1e6):
        objective=lambda x,a=a:a*x*x/2
        gradient=lambda x,a=a:a*x
        optimum=gradient_descent(1,objective,gradient,step=1/a,tolerance=0,max_iterations=3)
        assert optimum["status"]=="gradient_tolerance" and optimum["iterations"]==1 and optimum["x"]==0
        boundary=gradient_descent(1,objective,gradient,step=2/a,tolerance=0,max_iterations=3)
        assert boundary["status"]=="max_iterations"
        assert [r["x"] for r in boundary["history"]]==[1.,-1.,1.,-1.]
        unstable=gradient_descent(1,objective,gradient,step=3/a,tolerance=0,max_iterations=2)
        assert unstable["status"]=="max_iterations"
        assert math.isclose(unstable["x"],4,rel_tol=1e-15)
        assert unstable["objective"]>objective(1)
    print("PASS: scaling Hessians/conditions, four transforms, twelve curvature stencils and six scalar mode runs")

if __name__=="__main__":
    run()
