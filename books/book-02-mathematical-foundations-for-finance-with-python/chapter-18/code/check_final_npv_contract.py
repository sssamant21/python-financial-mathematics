"""Final valuation compatibility and end-to-end false-root rejection."""
from fractions import Fraction as F
import json
import math
from unittest.mock import patch
import section_18_05 as shared
import section_18_10 as final


def reference(rate,flows):
    base=1+F(float(rate))
    return sum(F(float(c))/base**i for i,c in enumerate(flows))


def rejects(error,fn,*args):
    try:fn(*args)
    except error:return
    raise AssertionError('expected '+error.__name__)


def no_false_roots():
    d=2**-30;flows=(-1.0,2+d,-(1+d));records=[]
    for a,b in ((-d,-d/4),(d/4,3*d/4)):
        assert not (a<=0<=b or a<=d<=b)
        assert reference(a,flows)*reference(b,flows)>0
        rejects(ValueError,final.bisect,lambda r:final.npv(r,flows),a,b)
        records.append({'bracket':(a,b),'exact_endpoint_npvs':list(map(str,(reference(a,flows),reference(b,flows))))})
    return records


def check():
    # These intervals contain neither algebraic root; the old copied NPV
    # arithmetic made both endpoint values zero and falsely returned success.
    rejected=no_false_roots()
    d=2**-30;flows=(-1.0,2+d,-(1+d));tiny=math.nextafter(0.0,1.0)
    cases=[(r,flows) for r in (-d,-d/4,0.0,d/4,3*d/4,d)]
    cases.extend((r,(-100,230,-132)) for r in (0.0,0.05,0.15,0.25))
    cases.extend((r,(7,)) for r in (-0.5,0.0,1e308))
    cases.extend((r,(0,0,0)) for r in (-0.5,0.5))
    cases.extend(((0.0,(0,)),(0.0,(1e308,-1e308)),
                  (math.nextafter(-1.0,0.0),(1,-2,1)),(1e308,(-1,2)),(0.0,(0,tiny)),
                  (0.0,(2**60+1,))))
    values=[]
    for r,cashflows in cases:
        exact=reference(r,cashflows);actual=final.npv(r,cashflows)
        assert actual==float(exact)
        assert shared.periodic_npv(r,cashflows)==actual
        assert (actual==0)==(exact==0)
        values.append({'rate':r,'flows':cashflows,'actual':actual,'exact_reference':str(exact)})
    for cashflows in ((0,0),(1,),(0,)):
        rejects(ValueError,shared.npv,0.0,cashflows)
        rejects(ValueError,shared.scan_brackets,cashflows)
    ranges=((1.0,(0,tiny)),(0.0,(1e308,1e308)))
    for r,cashflows in ranges:rejects(ValueError,final.npv,r,cashflows)
    invalid=((True,(1,),TypeError),(math.inf,(1,),ValueError),(-1.0,(1,),ValueError),
             (0.0,(),ValueError),(0.0,None,ValueError),(0.0,(True,),TypeError),
             (0.0,[math.nan],ValueError))
    for r,cashflows,error in invalid:rejects(error,final.npv,r,cashflows)
    roots=[]
    for a,b,expected in ((-d/2,d/2,0.0),(d/2,1.5*d,d)):
        result=final.bisect(lambda r:final.npv(r,flows),a,b)
        assert result['root']==expected and result['status']=='exact_root'
        assert reference(expected,flows)==0
        roots.append(result)
    final_report=final.assessment()
    for result,exact_root in zip(final_report['multiple_irr_solutions'],(F(1,10),F(1,5))):
        a,b=map(F,result['bracket'])
        assert a<=exact_root<=b and b-a<=F(1e-12)
        assert abs(F(result['root'])-exact_root)<=F(1e-12)
    with patch.object(final,'_shared_periodic_npv',wraps=shared.periodic_npv) as evaluator:
        assert final.npv(0.15,(-100,230,-132))==float(reference(0.15,(-100,230,-132)))
        evaluator.assert_called_once_with(0.15,(-100,230,-132))
    with patch.object(final,'_shared_periodic_npv',return_value=0.0):
        try:no_false_roots()
        except AssertionError:detected=True
        else:raise AssertionError('undetected false-zero shared output')
    return {'valuation_references':values,'rejected_nonroot_brackets':rejected,
            'true_exact_root_cases':roots,'preserved_strict_discovery_rejections':6,
            'final_range_rejections':len(ranges),'invalid_final_inputs':len(invalid),
            'observed_shared_valuation_calls':1,'false_zero_variant_detected':detected,
            'scope':'finite periodic represented-input valuation; valuation zeros do not certify unique IRRs'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
