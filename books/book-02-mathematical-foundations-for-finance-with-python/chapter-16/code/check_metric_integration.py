"""Independent references through Section 16.9/16.10 report entry points."""
import json
import math
import section_16_09 as project
import section_16_10 as final
from check_residual_metric_boundaries import reference


def checked(actual,expected):
    for key in ('mae','bias','max_abs'):
        assert actual[key] == expected[key],(key,actual,expected)
    assert abs(actual['rmse']-expected['rmse']) <= 2*math.ulp(expected['rmse'])
    json.dumps(actual,allow_nan=False)


def check():
    cases = (
        (0,((1,1e308),(1,1e308)),(-1e308,-1e308)),
        (-1,((1,-1e-200),(1,2e-200)),(1e-200,-2e-200)),
        (0,((1,-1e308),(1,999),(1,1e308)),(1e308,1.,-1e308)),
    )
    for rate,rows,errors in cases:
        actual = project.price_metrics(rate,rows)
        assert actual['residuals'] == errors
        expected = reference(errors)
        checked(actual,expected)
        checked(final.metrics(errors),expected)
    # Observe actual shared-helper use while preserving real calculations.
    observed = []
    for module,call in ((project,lambda:project.price_metrics(0,((1,1001),))),
                        (final,lambda:final.metrics((-1.,)))):
        original = module.checked_metrics
        def spy(errors):
            observed.append(tuple(errors))
            return original(errors)
        module.checked_metrics = spy
        try:
            checked(call(),reference((-1.,)))
        finally:
            module.checked_metrics = original
    assert observed == [(-1.,),(-1.,)]
    return {'entry_point_reference_sets':6,'shared_helper_calls':2,
            'strict_json_reference_sets':8}


if __name__ == '__main__':
    print(check())
