"""Exact means, Decimal RMS oracles and selected Section 16.8 input contracts."""
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import permutations
import math
from section_16_08 import metrics, observations, weighted_loss, residuals


def rejected(call, exception=ValueError):
    try:
        call()
    except exception:
        return
    raise AssertionError(f"expected {exception.__name__}")


def reference(values):
    e = tuple(Fraction(v) for v in values)
    mae, bias = sum(map(abs,e))/len(e),sum(e)/len(e)
    mean_square = sum(v*v for v in e)/len(e)
    with localcontext() as ctx:
        ctx.prec = 100
        rms = (Decimal(mean_square.numerator)/Decimal(mean_square.denominator)).sqrt()
    return {'mae':float(mae),'bias':float(bias),'rmse':float(rms),
            'max_abs':float(max(map(abs,e)))}


def check():
    datasets = ((0.,0.),(3.,-4.),(1e308,1e308),(1e308,1.,-1e308),
                (1e-200,-2e-200),(math.ulp(0.0),-math.ulp(0.0)),
                (1e308,1e-308,-1e308,-1e-308),(1e-300,1e-300))
    metric_pairs = 0
    for values in datasets:
        expected, actual = reference(values),metrics(values)
        for key in ('mae','bias','max_abs'):
            assert actual[key] == expected[key], (values,key,actual,expected)
            metric_pairs += 1
        assert abs(actual['rmse']-expected['rmse']) <= 2*math.ulp(expected['rmse'])
        metric_pairs += 1
    for values in permutations((1e308,1.,-1e308)):
        result = metrics(values)
        assert result['bias'] == float(Fraction(1,3))
        assert abs(result['rmse']-reference(values)['rmse']) <= 2*math.ulp(result['rmse'])
    invalid = 0
    for errors in ((),[],None,'bad',(math.inf,),(-math.inf,),(math.nan,),
                   (True,),(False,),('1',)):
        rejected(lambda:metrics(errors),TypeError if errors in ((True,),(False,),('1',)) else ValueError)
        invalid += 1
    invalid_rows = ((),[],None,'bad',((1,),),((1,2,3),),(1,),
                    ((0,1000),),((-1,1000),),((math.inf,1000),),
                    ((math.nan,1000),),((1,math.inf),),((1,math.nan),),
                    ((True,1000),),((1,True),),((1,'bad'),))
    for rows in invalid_rows:
        kind = TypeError if rows in (((True,1000),),((1,True),),((1,'bad'),)) else ValueError
        rejected(lambda:observations(rows),kind)
        invalid += 1
    rows = ((1,1001),(2,1002))
    for weights in ((),(1,),None,'bad',(-1,1),(0,0),(math.inf,1),
                    (math.nan,1),(True,1),('bad',1)):
        kind = TypeError if weights in ((True,1),('bad',1)) else ValueError
        rejected(lambda:weighted_loss(0,rows,weights),kind)
        invalid += 1
    for rate in (math.inf,math.nan,True):
        rejected(lambda:residuals(rate,rows),TypeError if rate is True else ValueError)
        invalid += 1
    # Independent integer residuals and weighted half-square sum; zero weight
    # is allowed when at least one other weight is strictly positive.
    assert residuals(0,rows) == (-1,-2)
    assert weighted_loss(0,rows,(0,3)) == float(Fraction(1,2)*(0*1+3*4)) == 6
    return {'metric_reference_pairs':metric_pairs,'cancellation_permutations':6,
            'invalid_cases':invalid,'weighted_residual_references':2}


if __name__ == '__main__':
    print(check())
