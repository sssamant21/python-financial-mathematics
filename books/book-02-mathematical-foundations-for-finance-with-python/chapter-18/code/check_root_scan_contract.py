"""Exact finite-period polynomial, scan and deduplication contract checks."""
from fractions import Fraction as F
import json
import math
from unittest.mock import patch
import section_18_05 as lab


def reference(rate,flows):
    # Direct rational sum, independent of the lab's Horner evaluation.
    base=1+F(rate)
    return sum(F(c)/base**i for i,c in enumerate(flows))


def rejects(exc,fn,*args,**kwargs):
    try:fn(*args,**kwargs)
    except exc:return
    raise AssertionError('expected '+exc.__name__)


def check():
    delta=2**-30;flows=(-1.0,2+delta,-(1+delta))
    rates=(-delta,delta/4,delta/2,3*delta/4,delta,2*delta)
    npv_checks=0
    for rate in rates:
        exact=reference(rate,flows)
        assert lab.npv(rate,flows)==float(exact),(rate,lab.npv(rate,flows),float(exact))
        assert (lab.npv(rate,flows)==0)==(exact==0)
        npv_checks+=1
    for rate in (-0.5,0.0,0.05,0.1,0.15,0.2,0.3):
        assert lab.npv(rate)==float(reference(rate,(-100,230,-132)))
        npv_checks+=1
    # Multiplication by (1+r)^2 gives -r*(r-delta), so both close roots
    # and every selected sign can be derived without a numerical solver.
    assert all(reference(r,flows)==-F(r)*(F(r)-F(delta))/(1+F(r))**2 for r in rates)
    exact_scan=lab.scan_brackets(flows,-delta,2*delta,6)
    assert exact_scan['exact_grid_roots']==[0.0,delta]
    assert exact_scan['brackets']==[] and exact_scan['exhaustive'] is False
    distinct=lab.discover_roots(flows,-delta,2*delta,6,dedup_tol=0)
    assert distinct['roots']==[0.0,delta] and distinct['candidate_roots']==[0.0,delta]
    assert distinct['deduplication']['absolute_rate_tolerance']==0
    assert distinct['deduplication']['merged_count']==0
    merged=lab.discover_roots(flows,-delta,2*delta,6)
    assert merged['roots']==[0.0] and merged['deduplication']['merged_count']==1
    assert merged['deduplication']['absolute_rate_tolerance']==1e-9
    assert merged['completeness_certified'] is False
    refined=lab.discover_roots(flows,-delta,2*delta,5,dedup_tol=0)
    assert len(refined['scan']['brackets'])==len(refined['roots'])==2
    for root,expected in zip(refined['roots'],(0.0,delta)):
        assert abs(F(root)-F(expected))<=F(1e-12)
    for a,b in refined['scan']['brackets']:
        assert reference(a,flows)*reference(b,flows)<0
    repeated=[]
    for stream,lo,hi,steps,expected in (((-1,2,-1),-0.5,0.5,2,[0.0]),
                                      ((-1,2,-1),-0.5,0.5,3,[]),
                                      ((-1,4,-4),0.0,2.0,2,[1.0]),
                                      ((-1,4,-4),0.0,2.0,3,[])):
        scan=lab.scan_brackets(stream,lo,hi,steps)
        assert scan['exact_grid_roots']==expected and scan['brackets']==[]
        assert scan['exhaustive'] is False
        discovered=lab.discover_roots(stream,lo,hi,steps,dedup_tol=0)
        assert discovered['roots']==expected and discovered['completeness_certified'] is False
        repeated.append({'flows':stream,'steps':steps,'report':discovered})
    # Isolate the candidate-merging policy from scanning/NPV conditioning.
    threshold=1e-9
    sets=(([0.0,math.nextafter(threshold,0)],1),([0.0,threshold],1),
          ([0.0,math.nextafter(threshold,math.inf)],2),
          ([0.0,0.75*threshold,1.5*threshold],2),([0.0,0.0,threshold],1))
    for candidates,count in sets:
        fake={'brackets':[],'exact_grid_roots':candidates,'exhaustive':False,'grid_steps':1}
        with patch.object(lab,'scan_brackets',return_value=fake):
            actual=lab.discover_roots(dedup_tol=threshold)
        retained=[]
        for x in sorted(candidates):
            if not retained or abs(F(x)-F(retained[-1]))>F(threshold):retained.append(x)
        assert actual['roots']==retained and len(retained)==count
        assert actual['candidate_roots']==sorted(candidates)
        assert actual['deduplication']['merged_count']==len(candidates)-count
    for value,exc in ((-1,ValueError),(math.nan,ValueError),(math.inf,ValueError),(True,TypeError),('x',TypeError)):
        with patch.object(lab,'scan_brackets',side_effect=AssertionError('must validate before scanning')):
            rejects(exc,lab.discover_roots,dedup_tol=value)
    grids=((-0.5,0.5,2),(0.0,1e308,2),(1e308,1.7e308,3),(-0.5,1.7e308,4))
    for lo,hi,steps in grids:
        scan=lab.scan_brackets((-1.0,2.0),lo,hi,steps)
        expected=[float(F(lo)+(F(hi)-F(lo))*F(i,steps)) for i in range(steps+1)]
        assert scan['grid']==expected and expected[0]==lo and expected[-1]==hi
        assert all(a<b for a,b in zip(scan['grid'],scan['grid'][1:]))
        assert scan['npv_values']==[float(reference(r,(-1,2))) for r in expected]
    rejects(ValueError,lab.scan_brackets,(-1,2),1.0,math.nextafter(1.0,2.0),2)
    tiny=math.nextafter(0.0,1.0)
    rejects(ValueError,lab.npv,1.0,(0.0,tiny))
    rejects(ValueError,lab.npv,0.0,(1e308,1e308))
    assert lab.npv(0.0,(1e308,-1e308))==0.0
    # Wrong merge settings and a false grid root are detected by exact scope.
    assert len(merged['roots'])!=len(distinct['roots'])
    assert reference(delta/2,flows)!=0
    serialized=json.dumps(distinct,sort_keys=True,allow_nan=False)
    assert json.dumps(json.loads(serialized),sort_keys=True,allow_nan=False)==serialized
    return {'npv_references':npv_checks,'close_root_exact_grid':distinct,
            'close_root_default_merge':merged,'close_root_refined':refined,
            'repeated_root_cases':repeated,'isolated_dedup_boundary_sets':len(sets),
            'invalid_tolerance_cases':5,'range_rejections':2,
            'grid_reference_sets':len(grids),'collapsed_grid_rejections':1,
            'scope':'selected finite-period exact represented-input model; scans remain nonexhaustive'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
