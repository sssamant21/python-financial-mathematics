"""Independent term, total, assessment and pending-dossier checks."""
from decimal import Decimal, localcontext
import io
import json
import math
import sys
import unittest
import section_20_09 as project
import check_section_20_10 as assessment


def expected_value(flows, rate):
    with localcontext() as ctx:
        ctx.prec=1600
        terms=[]
        for amount,years in flows:
            x=-Decimal(rate)*Decimal(years)
            if not amount:
                term=0.
            elif x>10000:
                return 'OverflowError'
            elif x<-10000:
                term=0.
            else:
                term=float(Decimal(amount)*x.exp())
            if not math.isfinite(term):
                return 'OverflowError'
            terms.append(Decimal(term))
        result=float(sum(terms,Decimal(0)))
        return result if math.isfinite(result) else 'OverflowError'


def observe(fn,args,expected,label):
    try:
        actual=fn(*args)
    except (TypeError,ValueError,OverflowError) as exc:
        actual=type(exc).__name__
    return dict(helper=label,inputs=repr(args),expected=expected,actual=actual,
                passed=type(actual) is type(expected) and actual==expected)


def check():
    m,s=sys.float_info.max,math.ulp(0.)
    rows=[]
    cases=[
        ([(s,1)],-1000),([(-s,1)],-1000),([(m,1)],1000),
        ([(m,1),(-m/2,1)],1000),([(0,2)],-m),([(s,2)],m),
        ([(m,2)],m),([(m,2)],-m),([(s,1)],1),([(m,1)],-1),
        ([(m,0),(m,0),(-m,0),(s,0)],0),
        ([(-m,0),(m,0),(s,0),(m,0)],0),
        ([(m,0),(m,0),(-m,0),(-m,0),(s,0)],0),
        ([(m,0),(math.ulp(m)/2,0)],0),
        ([(m,0),(math.nextafter(math.ulp(m)/2,0),0)],0),
        ([(80,1),(40,2)],math.log(2)),
        ([(2,1),(-3,4),(7,5)],.125),
        ([],.125),
    ]
    for flows,rate in cases:
        expected=expected_value(flows,rate)
        for fn,label in [(project.value,'project.value'),(assessment.value,'assessment.value')]:
            rows.append(observe(fn,(flows,rate),expected,label))
    for args,expected in [
        (([],float('nan')),'ValueError'),(([],True),'TypeError'),
        (([(0,-1)],0),'ValueError'),(([(0,float('inf'))],0),'ValueError'),
        (([(True,0)],0),'TypeError'),(([(1,)],0),'ValueError'),
        (([(m,1),(-m,1)],-1),'OverflowError'),
    ]:
        rows.append(observe(project.value,args,expected,'project guards'))
    flows=[(m,0),(m,0),(-m,0)]
    row=observe(assessment.value,(iter(flows),0),m,'assessment iterable')
    row['inputs']=repr((flows,0))
    rows.append(row)
    suite=unittest.defaultTestLoader.loadTestsFromModule(assessment)
    sink=io.StringIO()
    result=unittest.TextTestRunner(stream=sink).run(suite)
    rows.append(dict(helper='assessment suite',expected=12,actual=result.testsRun,
                     passed=result.testsRun==12 and result.wasSuccessful(),
                     detail=sink.getvalue()))
    same=assessment.value is project.value
    rows.append(dict(helper='assessment delegation identity',expected=True,actual=same,passed=same))
    dossier=project.pending_dossier()
    expected={'model':'constant-rate continuous discounting','source_commit':None,
              'environment':None,'execution':'not run','findings':[],
              'independent_review':'pending','approval':'pending'}
    rows.append(dict(helper='pending dossier after checks',expected=expected,actual=dossier.copy(),passed=dossier==expected))
    fresh=project.pending_dossier()
    fresh['findings'].append('local mutation')
    actual=project.pending_dossier()
    rows.append(dict(helper='fresh dossier isolation',expected=expected,actual=actual,passed=actual==expected))
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
