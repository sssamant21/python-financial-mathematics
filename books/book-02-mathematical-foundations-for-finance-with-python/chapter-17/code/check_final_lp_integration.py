"""Exact fixed-LP vertices/certificates and actual final-report integration."""
import copy
from fractions import Fraction as F
import itertools
import json
from unittest.mock import patch
import section_17_05 as lp
import section_17_10 as final


def exact_vertices():
    # Derive all six intersections from the manuscript inequalities; no lab
    # constants, benefit, intersection or optimizer functions are used.
    rows=((F(1),F(1),F(8)),(F(2),F(1),F(10)),
          (F(-1),F(0),F(0)),(F(0),F(-1),F(0)))
    candidates=[]
    for (a,b,c),(d,e,f) in itertools.combinations(rows,2):
        determinant=a*e-b*d
        assert determinant
        x=(c*e-b*f)/determinant;y=(a*f-c*d)/determinant
        candidates.append(((x,y),all(a*x+b*y<=c for a,b,c in rows)))
    return candidates


def exact_certificate(x,y,a,b):
    x,y,a,b=map(F,(x,y,a,b))
    primal=(8-x-y,10-2*x-y,x,y)
    dual=(a+2*b-5,a+b-4,a,b)
    benefit=5*x+4*y;dual_value=8*a+10*b;gap=dual_value-benefit
    comp=(a*primal[0],b*primal[1],x*dual[0],y*dual[1])
    return {'primal':primal,'dual':dual,'benefit':benefit,
            'dual_value':dual_value,'gap':gap,'comp':comp,
            'passes':min(primal)>=0 and min(dual)>=0 and gap==0 and all(v==0 for v in comp)}


def validate_certificate(report,x,y,a,b):
    ref=exact_certificate(x,y,a,b)
    assert report['primal']['allocation']==(x,y)
    assert report['dual']['multipliers']==(a,b)
    assert report['primal']['slacks']==tuple(map(float,ref['primal']))
    assert report['dual']['slacks']==tuple(map(float,ref['dual']))
    assert report['primal']['benefit']==float(ref['benefit'])
    assert report['dual']['dual_objective']==float(ref['dual_value'])
    assert report['duality_gap']==float(ref['gap'])
    assert report['complementarity']==tuple(map(float,ref['comp']))
    assert report['primal']['feasible']==(min(ref['primal'])>=0)
    assert report['dual']['feasible']==(min(ref['dual'])>=0)
    assert report['certified_by_residuals'] is ref['passes']


def validate_report(report):
    cert=report['certificate']
    vertices={point for point,feasible in exact_vertices() if feasible}
    actual=report['vertices']
    assert len(actual)==len(vertices) and set(actual)==vertices
    assert report['scores']==tuple(5*F(x)+4*F(y) for x,y in actual)
    best=max(vertices,key=lambda p:5*p[0]+4*p[1])
    assert report['optimal_point']==best
    assert report['primal_value']==5*best[0]+4*best[1]==34
    # Both primal variables are positive, so the two dual inequalities bind.
    a,b=F(3),F(1)
    assert a+2*b==5 and a+b==4
    assert report['dual_multipliers']==(a,b) and report['dual_value']==34
    validate_certificate(cert,*best,a,b)


def check():
    validate_report(final.linear_program_reference())
    candidates=exact_vertices()
    assert len(candidates)==6 and sum(ok for _,ok in candidates)==4
    with patch.object(lp,'solve_vertices',wraps=lp.solve_vertices) as solve, \
         patch.object(lp,'certificate',wraps=lp.certificate) as certificate:
        result=final.linear_program_reference()
        validate_report(result)
        solve.assert_called_once_with()
        certificate.assert_called_once_with(2.0,6.0,3.0,1.0)
    cases=((2,6,3,1),(3,6,3,1),(2,6,2,1),
           (5,0,3,1),(2,6,4,1),(0,0,0,0))
    certificates=[]
    for values in cases:
        report=lp.certificate(*values)
        validate_certificate(report,*values)
        certificates.append({'inputs':values,'report':report})
    assert certificates[-1]['report']['duality_gap']==0
    assert not certificates[-1]['report']['certified_by_residuals']
    mutations=[]
    solution=lp.solve_vertices()
    for field,value in (('allocation',(5.0,0.0)),('benefit',35.0),
                        ('vertices',solution['vertices'][:-1])):
        bad=copy.deepcopy(solution);bad[field]=value
        mutations.append(('solve_vertices',field,bad))
    cert=lp.certificate()
    for field,value in (('certified_by_residuals',False),('duality_gap',1.0)):
        bad=copy.deepcopy(cert);bad[field]=value
        mutations.append(('certificate',field,bad))
    detected=[]
    for helper,field,bad in mutations:
        with patch.object(lp,helper,return_value=bad):
            try:validate_report(final.linear_program_reference())
            except AssertionError:detected.append(helper+'.'+field)
            else:raise AssertionError('wrong helper output was not detected: '+field)
    assert len(detected)==5
    validate_report(final.assessment()['linear_program'])
    serialized=json.dumps(final.assessment(),sort_keys=True,allow_nan=False)
    assert json.dumps(json.loads(serialized),sort_keys=True,allow_nan=False)==serialized
    return {'exact_intersections':6,'feasible_vertices':4,'certificate_cases':certificates,
            'actual_helper_calls':2,'wrong_helper_outputs_detected':detected,
            'scope':'fixed default LP only; not general infeasibility/unboundedness diagnosis'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
