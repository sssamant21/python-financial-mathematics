"""Exact written-objective references, distinct from the aggregate calibration."""
from copy import deepcopy
from fractions import Fraction
import math
import section_16_10 as lab


def validate(evidence):
    single=evidence['single_observation']
    assert single['rows']==((2.0,1100.0),)
    assert single['curvature']==4
    assert single['stationary_rate']==float(Fraction(1,20))
    assert single['stationary_loss']==single['stationary_gradient']==0
    pairs=0
    # Independently expanded polynomial, rather than a squared-residual copy:
    # L(r)=2*r^2-r/5+1/200, g(r)=4*r-1/5.
    for row in single['evaluations']:
        r=Fraction(row['rate'])
        loss=2*r*r-r/5+Fraction(1,200)
        gradient=4*r-Fraction(1,5)
        assert abs(row['loss']-float(loss))<=3*math.ulp(float(loss))
        assert abs(row['gradient']-float(gradient))<=2*math.ulp(float(gradient))
        pairs+=2
    shifted=evidence['shifted_quadratic']
    assert shifted['curvature']==1 and shifted['center']==3
    assert evidence['three_observation_curvature']==14
    history_fields=0
    assert [case['step'] for case in shifted['gradient_descent']]==[0.5,1.0,2.0,3.0]
    for case in shifted['gradient_descent']:
        step=Fraction(case['step']);run=case['result']
        expected_iterations=1 if step==1 else 2
        expected_status='gradient_tolerance' if step==1 else 'max_iterations'
        assert run['iterations']==expected_iterations and run['status']==expected_status
        assert len(run['history'])==expected_iterations+1
        for k,row in enumerate(run['history']):
            # Closed-form recurrence for the written curvature-one objective.
            x=3*(1-(1-step)**k)
            assert Fraction(row['x'])==x
            assert Fraction(row['objective'])==(x-3)**2/2
            assert Fraction(row['gradient'])==x-3
            history_fields+=3
        assert run['x']==run['history'][-1]['x']
    newton=shifted['newton']
    assert newton['x']==3 and newton['iterations']==1
    assert newton['status']=='gradient_tolerance'
    assert [(r['x'],r['gradient']) for r in newton['history']]==[(0.,-3.),(3.,0.)]
    return pairs,history_fields


def check():
    report=lab.assessment()
    assert 'exercise_objectives' in report,'written exercise objectives need distinct executable evidence'
    evidence=report['exercise_objectives']
    pairs,history_fields=validate(evidence)
    detected=0
    for fault in ('aggregate_curvature_substitution','curvature_two_history'):
        changed=deepcopy(evidence)
        if fault=='aggregate_curvature_substitution':
            changed['single_observation']['curvature']=14
        else:
            changed['shifted_quadratic']['gradient_descent'][0]['result']['history'][1]['x']=3.0
        try:
            validate(changed)
        except AssertionError:
            detected+=1
        else:
            raise AssertionError('wrong objective scope must be detected')
    return {'single_objective_reference_fields':pairs,'gradient_descent_history_fields':history_fields,
            'curvature_scopes':3,'newton_one_step_history':1,'wrong_scope_variants_detected':detected}


if __name__=='__main__':
    print(check())
