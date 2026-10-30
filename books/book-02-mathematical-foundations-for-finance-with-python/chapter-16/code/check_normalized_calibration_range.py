"""Independent references for both normalized calibration API copies."""
from fractions import Fraction
import math
import section_16_09 as project
import section_16_10 as final
from check_calibration_range import decimal_fit


def rejected(call,exception=ValueError):
    try:
        call()
    except exception:
        return
    raise AssertionError(f'expected {exception.__name__}')


def check():
    fit_cases=[((2.0**k,2000.),) for k in (-540,-200,0,200,540,1000)]
    fit_cases += [((2.,1e308),(2.,-1e308)),((math.ulp(0.),1000.),)]
    fit_pairs=curvature_pairs=gradient_pairs=rejections=0
    for module,curvature in ((project,project.curvature),(final,final.hessian)):
        for rows in fit_cases:
            assert module.analytical_rate(rows)==decimal_fit(rows)
            fit_pairs+=1
        # In particular, raw price curvature at t=2^510 is unrepresentable,
        # while the normalized curvature is exactly 2^1020 and must survive.
        for exponent in (-530,-100,0,100,510):
            rows=((2.0**exponent,1000.),)
            assert curvature(rows)==float(Fraction(2)**(2*exponent))
            curvature_pairs+=1
        for rows,rate in ((((3.,997.),),0),
                          (((2.,-1e308),(2.,999.),(2.,1e308)),0),
                          (((2.0**500,-2.0**530),),-2.0**-500)):
            if module is project:
                errors=module.normalized_residuals(rate,rows)
                expected=sum(Fraction(t)*Fraction(e) for (t,y),e in zip(rows,errors))
            else:
                errors=module.residuals(rate,rows)
                expected=sum(Fraction(t)*Fraction(e)/1000 for (t,y),e in zip(rows,errors))
            assert module.gradient(rate,rows)==float(expected)
            gradient_pairs+=1
        for call in (
            lambda:curvature(((2.0**-540,1000.),)),
            lambda:curvature(((2.0**540,1000.),)),
            lambda:module.analytical_rate(((math.ulp(0.),2000.),)),
            lambda:module.analytical_rate(((1e308,math.nextafter(1000.,math.inf)),)),
            lambda:module.gradient(-2.0**540,((2.0**-540,-2.0**-540),)),
            lambda:module.gradient(-2.0**-600,((2.0**600,-2.0**600),)),
            lambda:module.analytical_rate(()),
            lambda:module.analytical_rate(((0,1000),)),
        ):
            rejected(call)
            rejections+=1
        rejected(lambda:module.analytical_rate(((True,1000),)),TypeError)
        rejections+=1
    # Both nominal examples keep their own normalized scale, not raw-price
    # curvature fourteen million. Their rounded-residual conventions differ.
    assert project.curvature()==final.hessian()==14
    assert project.gradient(0,((3,997),))==float(3*Fraction(0.003))
    assert final.gradient(0,((3,997),))==float(Fraction(9,1000))
    return {'decimal_fit_pairs':fit_pairs,'normalized_curvature_pairs':curvature_pairs,
            'gradient_pairs':gradient_pairs,'rejection_cases':rejections,
            'default_scale_and_residual_policy_checks':3}


if __name__=='__main__':
    print(check())
