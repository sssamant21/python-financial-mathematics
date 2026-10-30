"""Independent Decimal stationary-point references for the multistart example."""
from decimal import Decimal as D, localcontext
import math
from section_16_07 import multistart, local_descent

def root(lo,hi,tilt):
    lo,hi=D(lo),D(hi)
    f=lambda x:4*x*x*x-4*x+tilt
    left=f(lo)
    assert left*f(hi)<0
    for _ in range(210):
        mid=(lo+hi)/2
        value=f(mid)
        if left*value<=0:
            hi=mid
        else:
            lo=mid;left=value
    return (lo+hi)/2

def run():
    with localcontext() as ctx:
        ctx.prec=80
        tilt=D.from_float(0.2)
        roots=[root("-1.2","-0.8",tilt),root("0","0.2",tilt),root("0.8","1.2",tilt)]
        curvatures=[12*x*x-4 for x in roots]
        assert curvatures[0]>0 and curvatures[1]<0 and curvatures[2]>0
        values=[(x*x-1)**2+tilt*x for x in roots]
        assert values[0]<values[2]<values[1]
        result=multistart()
        assert len(result["runs"])==4
        matched=set()
        for run in result["runs"]:
            assert run["status"]=="gradient_tolerance"
            x=D.from_float(run["x"])
            nearest=min((0,2),key=lambda index:abs(x-roots[index]))
            assert abs(x-roots[nearest])<D("2e-10")
            matched.add(nearest)
            direct_value=(x*x-1)**2+tilt*x
            direct_gradient=4*x*x*x-4*x+tilt
            assert math.isclose(run["objective"],float(direct_value),rel_tol=2e-15,abs_tol=2e-15)
            assert abs(direct_gradient)<D("1.01e-9")
        assert matched=={0,2}
        best=result["best_observed"]
        assert best in result["runs"]
        assert abs(D.from_float(best["x"])-roots[0])<D("2e-10")
        assert result["global_optimality_certified"] is False
        failed=multistart((10.0,))
        assert failed["runs"][0]["status"]=="no_descent"
        assert failed["best_observed"] is None
        mixed=multistart((10.0,-1.5,1.5))
        assert mixed["runs"][0]["status"]=="no_descent"
        assert mixed["best_observed"]["status"]=="gradient_tolerance"
        # A stationary status alone can also describe the local maximum.
        maximum=local_descent(float(roots[1]))
        assert maximum["status"]=="gradient_tolerance"
        assert 12*D.from_float(maximum["x"])**2-4<0
    print("PASS: three independent stationary roots, four converged starts, failed/mixed pools and stationary-maximum distinction")

if __name__=="__main__":
    run()
