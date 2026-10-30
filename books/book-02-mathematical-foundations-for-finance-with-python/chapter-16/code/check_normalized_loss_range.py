"""Independent Decimal half-square references for normalized loss copies."""
from decimal import Decimal,localcontext
import math
import section_16_09 as project
import section_16_10 as final


def reference(errors,round_normalized):
    with localcontext() as ctx:
        ctx.prec=2500
        if round_normalized:
            normalized=[Decimal.from_float(float(e/1000)) for e in errors]
        else:
            normalized=[Decimal.from_float(float(e))/Decimal(1000) for e in errors]
        return float(sum(v*v for v in normalized)/2)


def rejected(call,exception=ValueError):
    try:
        call()
    except exception:
        return
    raise AssertionError(f'expected {exception.__name__}')


def check():
    datasets=((0.,),(2000.,-3000.,0.),(math.ldexp(1000.,512),),
              (math.ldexp(1000.,511),)*4,(math.ldexp(1000.,-538),)*16,
              (math.ldexp(1000.,-500),-math.ldexp(1000.,-500)),(1.,-2.,3.))
    pairs=rejections=0
    for loss,round_normalized in ((project.objective,True),(final.loss,False)):
        for errors in datasets:
            rows=tuple((1.,-e) for e in errors)
            actual=loss(-1.,rows)
            expected=reference(errors,round_normalized)
            assert actual==expected,(errors,actual,expected)
            pairs+=1
        for errors in ((math.ldexp(1000.,600),),(math.ldexp(1000.,-600),),
                       (math.ulp(0.),),(math.inf,),(math.nan,)):
            rejected(lambda:loss(-1.,tuple((1.,-e) for e in errors)))
            rejections+=1
        rejected(lambda:loss(-1.,((1.,True),)),TypeError)
        rejected(lambda:loss(-1.,()))
        rejections+=2
    # A loss of 2^-1073 is representable even though each of sixteen squared
    # normalized residuals 2^-1076 would individually underflow to zero.
    rows=((1.,-math.ldexp(1000.,-538)),)*16
    assert project.objective(-1.,rows)==final.loss(-1.,rows)==2.0**-1073
    # The first API retains rounding of normalized residuals but rejects their
    # nonzero-to-zero conversion rather than letting it look like perfect fit.
    rejected(lambda:project.normalized_residuals(-1.,((1.,-math.ulp(0.)),)))
    return {'decimal_loss_reference_pairs':pairs,'range_input_rejections':rejections,
            'representable_collective_subnormal_case':1,'normalization_underflow_rejection':1}


if __name__=='__main__':
    print(check())
