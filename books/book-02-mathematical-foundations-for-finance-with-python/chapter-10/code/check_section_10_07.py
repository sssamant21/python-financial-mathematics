"""Independent checks for Section 10.7."""
import math
from section_10_07 import integrate,refinement,finance_integrand,assessment,finite,MAX_PANELS

def close(x,y,tol=1e-9):
    assert math.isclose(x,y,rel_tol=tol,abs_tol=tol),(x,y)

def rejects(exc,fn,*args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError("expected "+exc.__name__)

def check_orders_and_estimators():
    # Exact composite-rule error identities on [0,1].
    cases=(("midpoint",lambda x:x*x,1/3,-1/12,2),
           ("trapezoid",lambda x:x*x,1/3,1/6,2),
           ("simpson",lambda x:x**4,1/5,2/15,4))
    for method,function,integral,coefficient,order in cases:
        rows=refinement(function,0,1,method,[2,4,8,16])
        assert "estimated_fine_error" not in rows[0]
        errors=[]
        for row in rows:
            signed=row["estimate"]-integral
            expected=coefficient/row["n"]**order
            assert math.isclose(signed,expected,rel_tol=1e-8,abs_tol=1e-15),(method,row)
            errors.append(abs(signed))
            if row is not rows[0]:
                assert math.isclose(row["estimated_fine_error"],abs(expected),
                                    rel_tol=1e-8,abs_tol=1e-15),(method,row)
        for coarse,fine in zip(errors,errors[1:]):
            assert math.isclose(coarse/fine,2**order,rel_tol=1e-8)
        reversed_value=integrate(function,1,0,8,method)
        assert math.isclose(reversed_value+integral,-coefficient/8**order,
                            rel_tol=1e-8,abs_tol=1e-15)
        # Only a consecutive doubling earns an estimator field.
        irregular=refinement(function,0,1,method,[2,6,12])
        assert "estimated_fine_error" not in irregular[0]
        assert "estimated_fine_error" not in irregular[1]
        assert math.isclose(irregular[2]["estimated_fine_error"],
                            abs(coefficient)/12**order,rel_tol=1e-8,abs_tol=1e-15)

    # Independent integral exp(1)-1; selected smooth nonpolynomial example.
    for method,ratio in (("midpoint",4),("trapezoid",4),("simpson",16)):
        rows=refinement(math.exp,0,1,method,[8,16,32,64])
        errors=[abs(row["estimate"]-math.expm1(1)) for row in rows]
        for coarse,fine in zip(errors,errors[1:]):
            assert math.isclose(coarse/fine,ratio,rel_tol=0.01),(method,errors)
        for row,error in zip(rows[1:],errors[1:]):
            assert math.isclose(row["estimated_fine_error"],error,rel_tol=0.01),(method,row,error)

def check_weighted_range():
    tiny=math.nextafter(0.0,1.0)
    for method in ("midpoint","trapezoid","simpson"):
        assert integrate(lambda t:1e308,0.,.5,4,method)==5e307
        assert integrate(lambda t:tiny,0.,1.,4,method)==tiny
        assert integrate(lambda t:1.7e308*t,-1.,1.,4,method)==0.
        rejects(ValueError,integrate,lambda t:tiny,0.,.25,2,method)
        rejects(ValueError,integrate,lambda t:1e308,0.,2.,2,method)
    values={0.:1e308,.5:1.,1.:-1e308}
    assert integrate(values.__getitem__,0.,1.,2,"trapezoid")==.5
    assert integrate(values.__getitem__,0.,1.,2,"simpson")==2/3


def check_grid_contracts():
    from decimal import Decimal,localcontext
    tiny=math.ulp(0.)
    for method in ("midpoint","trapezoid","simpson"):
        calls=[]
        def f(t):calls.append(t);return 1e-308
        with localcontext() as ctx:
            ctx.prec=2500
            expected=float(Decimal.from_float(1e-308)*2*Decimal.from_float(1e308))
        assert integrate(f,-1e308,1e308,2,method)==expected
        assert all(math.isfinite(t) for t in calls)
        for a,b,n in ((0.,tiny,2),(1e308,math.nextafter(1e308,math.inf),2),(0.,1.,MAX_PANELS+2)):
            calls=[]
            rejects(ValueError,integrate,f,a,b,n,method)
            assert calls==[]
    calls=[]
    rejects(ValueError,integrate,lambda t:calls.append(t) or 1.,0.,tiny,1,"midpoint")
    assert calls==[]
    values=[]
    integrate(lambda t:values.append(t) or 1.,.1,.7,6,"trapezoid")
    with localcontext() as ctx:
        ctx.prec=100
        lo,hi=Decimal.from_float(.1),Decimal.from_float(.7)
        nominal=[float(lo+(hi-lo)*i/6) for i in range(7)]
    assert values==[nominal[0],nominal[-1],*nominal[1:-1]]


def check_refinement_reporting():
    from decimal import Decimal,localcontext
    from unittest.mock import patch
    import section_10_07 as lab
    for method,divisor in (("midpoint",3),("trapezoid",3),("simpson",15)):
        with patch.object(lab,"integrate",side_effect=[-1.7e308,1.7e308]):
            result=refinement(lambda t:0.,0.,1.,method,[2,4])
        with localcontext() as ctx:
            ctx.prec=2500
            expected=float(2*Decimal.from_float(1.7e308)/divisor)
        assert result[1]["estimated_fine_error"]==expected
        with patch.object(lab,"integrate",side_effect=[0.,math.ulp(0.)]):
            rejects(ValueError,refinement,lambda t:0.,0.,1.,method,[2,4])
    q=refinement(lambda t:-1e308 if t==.5 else 1e308,0.,1.,"midpoint",[1,2])
    with localcontext() as ctx:
        ctx.prec=2500
        assert q[1]["estimated_fine_error"]==float(2*Decimal.from_float(1e308)/3)
    supplied=[2]
    def mutates(t):
        if len(supplied)==1:supplied.append(4)
        return 1.
    assert [row["n"] for row in refinement(mutates,0.,1.,"midpoint",supplied)]==[2]
    assert supplied==[2,4]
    for counts,error in (([],ValueError),([2,True],TypeError),([2,100002],ValueError),([2]*33,ValueError)):
        calls=[]
        rejects(error,refinement,lambda t:calls.append(t) or 1.,0.,1.,"midpoint",counts)
        assert calls==[]


def run():
    check_refinement_reporting()
    check_grid_contracts()
    check_weighted_range()
    check_orders_and_estimators()
    for method in ("midpoint","trapezoid","simpson"):
        close(integrate(lambda t:7,0,3,8,method),21)
        close(integrate(lambda t:2+3*t,0,2,8,method),10)
        close(integrate(lambda t:2+3*t,2,0,8,method),-10)
        close(integrate(lambda t:t,1,1,8,method),0)
    close(integrate(lambda t:t*t,0,1,2,"midpoint"),0.3125)
    close(integrate(lambda t:t*t,0,1,2,"trapezoid"),0.375)
    close(integrate(lambda t:t*t,0,1,2,"simpson"),1/3)
    close(integrate(lambda t:t**3,0,1,2,"simpson"),1/4)
    for method in ("midpoint","trapezoid","simpson"):
        rows=refinement(lambda t:math.exp(t),0,1,method,[8,16,32,64])
        errors=[abs(x["estimate"]-math.expm1(1)) for x in rows]
        assert all(a>b for a,b in zip(errors,errors[1:])),(method,errors)
        assert all(x.get("estimated_fine_error",0)>=0 for x in rows)
    reference=integrate(finance_integrand,0,4,8192,"simpson")
    for method in ("midpoint","trapezoid","simpson"):
        close(integrate(finance_integrand,0,4,1024,method),reference,tol=1e-5)
    rejects(ValueError,integrate,lambda t:t,0,1,3,"simpson")
    rejects(ValueError,integrate,lambda t:t,0,1,0,"midpoint")
    rejects(ValueError,integrate,lambda t:t,0,1,2,"other")
    rejects(TypeError,integrate,lambda t:t,0,1,True,"midpoint")
    rejects(ValueError,finite,float("nan"),"value")
    report=assessment()
    assert len(report["methods"])==3 and report["runtime_certified"] is False
    print("PASS: Section 10.7 independent checks")

if __name__=="__main__":
    run()
