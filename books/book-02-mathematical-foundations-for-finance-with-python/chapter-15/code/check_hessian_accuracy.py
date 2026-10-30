"""Independent Decimal second-difference references for analytic Hessians."""
from decimal import Decimal as D, localcontext
import math
from section_15_06 import rate_time_hessian
from section_15_09 import hessians

def reference_value(point, output):
    p,r,t=point
    return p*(r*t).exp() if output==0 else p*(-r*t).exp()/2

def stencil(point,i,j,h,output):
    if i==j:
        plus=list(point);minus=list(point)
        plus[i]+=h;minus[i]-=h
        return (reference_value(plus,output)-2*reference_value(point,output)+reference_value(minus,output))/(h*h)
    total=D(0)
    for si,sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
        shifted=list(point);shifted[i]+=si*h;shifted[j]+=sj*h
        total+=si*sj*reference_value(shifted,output)
    return total/(4*h*h)

def run():
    with localcontext() as ctx:
        ctx.prec=90
        point=(D(2),D("0.125"),D(2))
        analytic=hessians(2.0,0.125,2.0)
        steps=(D(1)/16,D(1)/32,D(1)/64)
        checked=0
        for output in range(2):
            for i in range(3):
                for j in range(3):
                    assert analytic[output][i][j]==analytic[output][j][i]
                    estimates=[stencil(point,i,j,h,output) for h in steps]
                    if i==j==0:
                        assert analytic[output][i][j]==0
                        assert all(abs(v)<D("1e-80") for v in estimates)
                    else:
                        target=D.from_float(analytic[output][i][j])
                        errors=[abs(v-target) for v in estimates]
                        for coarse,fine in zip(errors,errors[1:]):
                            ratio=float(coarse/fine)
                            assert 3.9<ratio<4.1,(output,i,j,ratio)
                        extrapolated=(4*estimates[-1]-estimates[-2])/3
                        assert math.isclose(float(extrapolated),analytic[output][i][j],
                                            rel_tol=2e-6,abs_tol=1e-12)
                    checked+=1
        small=rate_time_hessian(2.0,0.125,2.0)
        for i in range(2):
            for j in range(2):
                assert small[i][j]==analytic[0][i+1][j+1]
        assert checked==18
    print("PASS: 18 analytic Hessian entries against 90-digit valuation stencils and selected order ladders")

if __name__=="__main__":
    run()
