"""Exact fixed-model references for the Section 16.8 missing lab step."""
from copy import deepcopy
from fractions import Fraction
import json
from itertools import combinations
import section_16_08 as lab


def validate(report):
    data=tuple(Fraction(v) for v in report['observations'])
    assert data==(2,3,4)
    jacobian=report['jacobian']
    assert tuple(map(tuple,jacobian))==((1,1),)*3
    # Independent row minors show rank <= 1; the nonzero first column gives
    # rank >= 1. This fixed exact result is not a numerical-rank threshold.
    minors=[Fraction(jacobian[i][0])*jacobian[j][1]-Fraction(jacobian[j][0])*jacobian[i][1]
            for i,j in combinations(range(len(data)),2)]
    assert minors==[0,0,0] and jacobian[0][0]!=0
    assert report['jacobian_rank']==1 and tuple(report['jacobian_minors'])==(0,0,0)
    assert tuple(map(tuple,report['normal_matrix']))==((3,3),(3,3))
    assert report['normal_determinant']==0
    direction=tuple(Fraction(v) for v in report['null_direction'])
    assert direction==(1,-1)
    assert all(sum(Fraction(a)*b for a,b in zip(row,direction))==0 for row in jacobian)
    assert all(sum(Fraction(a)*b for a,b in zip(row,direction))==0 for row in report['normal_matrix'])
    fitted=sum(data)/len(data)
    assert Fraction(report['fitted_sum'])==fitted==3
    evaluated=0
    for name,center,loss,gradient in (('optimal_family',(1,2),1,(0,0)),
                                     ('nonoptimal_family',(0,0),Fraction(29,2),(-9,-9))):
        family=report[name]
        assert [row['offset'] for row in family]==[-4,-0.5,0,0.5,4]
        for row in family:
            offset=Fraction(row['offset'])
            parameters=tuple(Fraction(v) for v in row['parameters'])
            assert parameters==(center[0]+offset,center[1]-offset)
            prediction=sum(parameters)
            errors=tuple(prediction-y for y in data)
            assert tuple(Fraction(v) for v in row['predictions'])==(prediction,)*3
            assert tuple(Fraction(v) for v in row['residuals'])==errors
            assert Fraction(row['loss'])==sum(e*e for e in errors)/2==loss
            assert tuple(row['gradient'])==gradient==(sum(errors),)*2
            evaluated+=1
    probe=report['off_null_probe']
    assert tuple(probe['parameters'])==(2,2)
    assert tuple(probe['predictions'])==(4,4,4)
    assert tuple(probe['residuals'])==(2,1,0)
    assert Fraction(probe['loss'])==Fraction(5,2)
    assert tuple(probe['gradient'])==(3,3)
    assert report['individual_parameters_identified'] is False
    return evaluated+1


def check():
    result=lab.assessment()
    assert 'rank_deficient_example' in result,'lab step10 needs executable evidence'
    report=result['rank_deficient_example']
    evaluated=validate(report)
    detected=0
    for fault in ('wrong_rank','wrong_null_shift'):
        changed=deepcopy(report)
        if fault=='wrong_rank':
            changed['jacobian_rank']=2
        else:
            changed['optimal_family'][0]['parameters']=(0,0)
        try:
            validate(changed)
        except AssertionError:
            detected+=1
        else:
            raise AssertionError('incorrect identifiability evidence must be detected')
    json.dumps(result,allow_nan=False)
    return {'exact_parameter_cases':evaluated,'rank_minor_references':3,
            'null_vector_products':5,'wrong_output_variants_detected':detected,
            'strict_json_reports':1}


if __name__=='__main__':
    print(check())
