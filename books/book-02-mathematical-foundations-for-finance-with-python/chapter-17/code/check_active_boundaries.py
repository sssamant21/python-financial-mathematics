"""Exact rational cap geometry versus rounded display/activity diagnostics."""
from fractions import Fraction
import math
import section_17_04 as lab


def check():
    t=lab.TRANSITION
    down=math.nextafter(t,0.0);up=math.nextafter(t,1.0)
    caps=(0.0,math.nextafter(0.0,1.0),math.nextafter(down,0.0),down,t,up,
          math.nextafter(up,1.0),math.nextafter(1.0,0.0),1.0)
    optimum=Fraction(8,11)
    assert Fraction(down)<optimum<Fraction(t)<Fraction(up)
    checks=0
    for cap in caps:
        u=Fraction(cap);x=min(u,optimum);y=1-x
        mu=max(Fraction(0),(8-11*x)/50)
        lam=(8*x-9)/50
        value=Fraction(11,100)*x*x-Fraction(4,25)*x+Fraction(9,100)
        solution=lab.optimal_portfolio(cap)
        # Relative error becomes material near the transition despite a tiny
        # absolute error. Require a correctly rounded exact decimal-model dual.
        assert solution['multipliers'][2]==float(mu),(cap,solution['multipliers'][2],float(mu))
        assert solution['lambda']==float(lam)
        assert solution['weights']==(float(x),float(y))
        assert abs(solution['variance']-float(value))<=4*math.ulp(float(value))
        expected_regime='degenerate_endpoint' if u==0 else 'binding' if u<optimum else 'inactive'
        assert solution['exact_model_regime']==expected_regime
        assert solution['model_cap_active']==(u==x)
        assert solution['model_cap_slack']==float(u-x)
        checks+=7
        # The legacy display tag recognizes the rounded transition. Keep its
        # stated policy distinct from exact cap geometry and numerical activity.
        display='degenerate_endpoint' if cap==0 else 'binding' if cap<t else 'weakly_active_transition' if cap==t else 'inactive'
        assert solution['regime']==display
        for tolerance in (0.0,1e-18,1e-9):
            report=lab.kkt_report(solution,tolerance)
            w1,w2=solution['weights']
            raw=(-w1,-w2,w1-cap)
            assert report['inequalities']==raw
            assert report['active']==[i for i,g in enumerate(raw) if abs(Fraction(g))<=Fraction(tolerance)]
        assert lab.kkt_report(solution)['passes'] is True
    rounded=lab.optimal_portfolio(t)
    assert rounded['regime']=='weakly_active_transition'
    assert rounded['exact_model_regime']=='inactive' and rounded['model_cap_slack']>0
    assert lab.kkt_report(rounded,0)['active']==[2]
    above=lab.optimal_portfolio(up)
    assert lab.kkt_report(above,0)['active']==[]
    assert lab.kkt_report(above,1e-9)['active']==[2]
    return {'cap_reference_sets':len(caps),'weight_dual_value_geometry_checks':checks,
            'raw_activity_reports':3*len(caps),'rounded_transition_distinctions':3}


if __name__=='__main__':
    print(check())
