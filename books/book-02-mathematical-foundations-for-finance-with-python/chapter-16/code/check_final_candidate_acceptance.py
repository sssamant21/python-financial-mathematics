"""Section 16.10 candidate-specific references and deliberately failed gates."""
from decimal import Decimal,localcontext
from fractions import Fraction
import json
import math
import section_16_10 as lab


def references(rate):
    r=Fraction(rate)
    training=tuple(1000*(1+Fraction(t)*r)-Fraction(y) for t,y in lab.TRAIN)
    holdout=tuple(1000*(1+Fraction(t)*r)-Fraction(y) for t,y in lab.HOLDOUT)
    def summary(errors):
        with localcontext() as ctx:
            ctx.prec=100
            square=sum(e*e for e in errors)/len(errors)
            rms=(Decimal(square.numerator)/Decimal(square.denominator)).sqrt()
        return {'mae':float(sum(map(abs,errors))/len(errors)),
                'rmse':float(rms),'bias':float(sum(errors)/len(errors)),
                'max_abs':float(max(map(abs,errors)))}
    return training,holdout,summary(training),summary(holdout)


def injected(field,value):
    original=lab.solve
    calls=[]
    def changed(*args,**kwargs):
        run=original(*args,**kwargs)
        if not calls:
            run[field]=value
        calls.append(run)
        return run
    lab.solve=changed
    try:
        return lab.assessment()
    finally:
        lab.solve=original


def check():
    report=lab.assessment()
    assert len(report['runs'])==6
    metric_fields=0
    for run in report['runs']:
        assert 'training_metrics' in run, 'metrics must be recomputed for each returned rate'
        train,holdout,tm,hm=references(run['rate'])
        for actual,expected in ((run['training_residuals'],train),
                                (run['holdout_residuals'],holdout)):
            assert len(actual)==len(expected)
            assert all(abs(a-float(e))<=2e-12 for a,e in zip(actual,expected))
        for actual,expected in ((run['training_metrics'],tm),(run['holdout_metrics'],hm)):
            for key,value in expected.items():
                assert abs(actual[key]-value)<=2e-12,(key,actual,expected)
                metric_fields+=1
        # Independent exact quadratic for the declared normalized objective.
        dr=Fraction(run['rate'])-Fraction(1,20)
        assert abs(run['recomputed_loss']-float(7*dr*dr))<=1e-24
        assert abs(run['recomputed_gradient']-float(14*dr))<=2e-12
        assert all(run['acceptance_checks'].values())
        assert run['provisional_acceptance'] is True
    assert report['provisional_acceptance'] is True
    json.dumps(report,allow_nan=False)
    # False status, stale rate/gradient/loss, failed holdout, actual budget.
    for field,value in (('status','max_iterations'),('rate',0.0),
                        ('gradient',1.0),('loss',1.0)):
        failed=injected(field,value)
        assert failed['runs'][0]['provisional_acceptance'] is False
        assert failed['provisional_acceptance'] is False
    stale=injected('rate',0.0)['runs'][0]
    assert stale['training_residuals']==(-50.,-100.,-150.)
    assert stale['recomputed_gradient']==-0.7
    assert math.isclose(stale['recomputed_loss'],0.0175,rel_tol=1e-15)
    original_holdout=lab.HOLDOUT
    lab.HOLDOUT=((4.,1202.),)
    try:
        failed=lab.assessment()
        assert not failed['provisional_acceptance']
        assert all(not r['acceptance_checks']['holdout_max_abs'] for r in failed['runs'])
    finally:
        lab.HOLDOUT=original_holdout
    original_solve=lab.solve
    lab.solve=lambda *a,**k:original_solve(*a,max_iterations=1)
    try:
        failed=lab.assessment()
        gd=[r for r in failed['runs'] if r['method']=='gradient_descent']
        assert len(gd)==3 and all(r['status']=='max_iterations' for r in gd)
        assert all(not r['provisional_acceptance'] for r in gd)
        assert not failed['provisional_acceptance']
    finally:
        lab.solve=original_solve
    try:
        injected('rate',math.nan)
    except ValueError:
        pass
    else:
        raise AssertionError('nonfinite candidate must be rejected')
    return {'candidate_reference_sets':6,'metric_reference_fields':metric_fields,
            'failed_gate_scenarios':6,'nonfinite_candidate_rejections':1,
            'stale_rate_reference_checks':3,'strict_json_reports':1}


if __name__=='__main__':
    print(check())
