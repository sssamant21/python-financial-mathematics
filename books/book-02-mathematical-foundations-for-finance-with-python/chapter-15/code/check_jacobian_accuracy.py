"""Production float Jacobian columns versus independent Decimal references."""
from decimal import Decimal as D, localcontext
import math
from section_15_09 import centered_jacobian_column

def run():
    base=(2.0,0.125,2.0)
    steps=(2.0**-4,2.0**-5,2.0**-6)
    with localcontext() as ctx:
        ctx.prec=90
        p,r,t=map(D.from_float,base)
        for column in range(3):
            for output in range(2):
                sign=D(1) if output==0 else D(-1)
                coefficient=D(1) if output==0 else D("0.5")
                level=coefficient*p*(sign*r*t).exp()
                derivative=(level/p,sign*t*level,sign*r*level)[column]
                errors=[]
                for step in steps:
                    h=D.from_float(step)
                    if column==0:
                        stencil=level/p
                    else:
                        k=sign*(t if column==1 else r)
                        stencil=level*((k*h).exp()-(-k*h).exp())/(2*h)
                    actual=centered_jacobian_column(base,column,step)[output]
                    assert math.isclose(actual,float(stencil),rel_tol=2e-12,abs_tol=1e-14)
                    errors.append(abs(D.from_float(actual)-derivative))
                if column==0:
                    assert all(error<D("1e-13") for error in errors)
                else:
                    for coarse,fine in zip(errors,errors[1:]):
                        assert 3.99<float(coarse/fine)<4.01
        # Tiny valid perturbations do not guarantee accurate function differences.
        for column in range(3):
            tiny=centered_jacobian_column(base,column,2.0**-50)
            coarse=centered_jacobian_column(base,column,steps[-1])
            exact=(float((r*t).exp()),float(2*p*(r*t).exp()),float(r*p*(r*t).exp()))[column]
            assert abs(tiny[0]-exact)/abs(exact)>0.01
            assert abs(coarse[0]-exact)/abs(exact)<0.001
    # Existing contract accepts distinct finite but unequal represented offsets.
    h=3*2.0**-53
    assert 1.0+h!=1.0 and 1.0-h!=1.0
    assert (1.0+h)-1.0 != 1.0-(1.0-h)
    assert all(math.isfinite(v) for v in centered_jacobian_column((1.0,0.125,2.0),0,h))
    print("PASS: 18 float-column/reference pairs, four error ladders, three cancellation and one asymmetry case")

if __name__=="__main__":
    run()
