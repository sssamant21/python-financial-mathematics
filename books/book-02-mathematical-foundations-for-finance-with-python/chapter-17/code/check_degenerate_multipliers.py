"""Exact cap-zero multiplier families; finite selected binary64 diagnostics."""
from fractions import Fraction as F
import json
import math
import section_17_04 as lab


def exact_residuals(a, b, c, lam):
    # w=(0,1), cap=0, exact decimal covariance. No lab gradient used.
    return (F(1,50)+lam-a+c, F(9,50)+lam-b), (F(0), -b, F(0))


def candidate(a, b=F(0), c=None, lam=F(-9,50)):
    if c is None:
        c=a+F(4,25)
    result=lab.optimal_portfolio(0.0)
    result.update({'lambda':float(lam),'multipliers':tuple(map(float,(a,b,c)))})
    return result


def check():
    tol=1e-12
    rows=[]
    parameters=(F(0),F(1,1024),F(1,16),F(1,4),F(1),F(8))
    canonical=lab.optimal_portfolio(0.0)
    assert canonical['weights']==(0.0,1.0)
    assert canonical['lambda']==float(F(-9,50))
    assert canonical['multipliers']==(0.0,0.0,float(F(4,25)))
    for a in parameters:
        s,p=exact_residuals(a,F(0),a+F(4,25),F(-9,50))
        assert s==(0,0) and p==(0,0,0)
        trial=candidate(a)
        report=lab.kkt_report(trial,tol)
        assert report['passes'] and report['active']==[0,2]
        assert report['equality_residual']==0 and report['inequalities']==(0.0,-1.0,0.0)
        assert report['complementarity']==(0.0,0.0,0.0)
        assert all(abs(v)<=tol for v in report['stationarity'])
        assert trial['variance']==float(F(9,100))
        rows.append({'a':str(a),'solution':trial,'report':report,
                     'zero_tolerance_report':lab.kkt_report(trial,0.0)})
    # Each row violates exactly one KKT family, with the others below tol.
    trials=(('dual_sign',F(-1,16),F(0),F(4,25)-F(1,16),F(-9,50)),
            ('stationarity',F(0),F(0),F(4,25)+F(1,32),F(-9,50)),
            ('complementarity',F(0),F(1,16),F(4,25)-F(1,16),F(-9,50)+F(1,16)))
    rejected=[]
    for name,a,b,c,lam in trials:
        sr,pr=exact_residuals(a,b,c,lam)
        exact={'dual_sign':min(a,b,c)<0,
               'stationarity':any(sr),'complementarity':any(pr)}
        assert [k for k,v in exact.items() if v]==[name]
        trial=candidate(a,b,c,lam);report=lab.kkt_report(trial,tol)
        violations={'dual_sign':any(m < -tol for m in trial['multipliers']),
                    'stationarity':any(abs(v)>tol for v in report['stationarity']),
                    'complementarity':any(abs(v)>tol for v in report['complementarity'])}
        assert violations==exact and report['passes'] is False
        assert report['equality_residual']==0 and max(report['inequalities'])==0
        # Omitting this single family would incorrectly accept this candidate.
        assert all(not v for k,v in violations.items() if k!=name)
        rejected.append({'failure':name,'exact_stationarity':list(map(str,sr)),
                         'exact_complementarity':list(map(str,pr)),
                         'solution':trial,'report':report})
    # A tiny negative multiplier can pass a declared numerical tolerance;
    # this is not exact dual feasibility and is deliberately characterized.
    tiny=-F(1,2**45)
    tiny_report=lab.kkt_report(candidate(tiny),tol)
    assert tiny<0 and tiny_report['passes'] is True
    assert lab.kkt_report(candidate(tiny),0.0)['passes'] is False
    # Dependency of active lower/cap normals: (-1,0)+(1,0)=(0,0).
    assert tuple(x+y for x,y in zip((-1,0),(1,0)))==(0,0)
    return {'valid_families':rows,'isolated_rejections':rejected,
            'omitted_family_variants_detected':3,
            'tiny_negative_tolerance_report':tiny_report,
            'tolerance':tol,'scope':'fixed decimal covariance; selected moderate finite multipliers only'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
