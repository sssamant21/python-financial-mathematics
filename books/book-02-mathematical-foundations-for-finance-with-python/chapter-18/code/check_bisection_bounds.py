"""Selected Section 18.3 width/error/count contracts from known rational roots."""
from fractions import Fraction as F
import json
import math
import section_18_03 as lab


def audit(result, points, root, lower, upper, reductions, status, exact_halves):
    assert points[:2] == [lower, upper]
    assert len(points) == reductions + 3
    assert result['iterations'] == reductions
    assert result['status'] == status
    a, b = F(lower), F(upper)
    initial = b-a
    for k, point in enumerate(points[2:]):
        q = F(point)
        # With dyadic endpoints every expected midpoint here is representable.
        if exact_halves:
            assert q == (a+b)/2
            assert b-a == initial / 2**k
        else:
            assert abs(q-(a+b)/2) <= F(math.ulp(point))/2
            assert abs((b-a)-initial/2**k) <= 2*F(math.ulp(upper))
        assert a < q < b and a < root < b
        assert abs(q-root) <= max(q-a,b-q)
        if exact_halves:
            assert abs(q-root) <= (b-a)/2
        if k < reductions:
            if q < root:
                a=q
            else:
                b=q
    assert tuple(result['bracket']) == (float(a),float(b))
    assert F(result['width']) == b-a
    assert result['root'] == points[-1]
    return {'reductions':reductions,'callbacks':len(points),'status':status,
            'final_width':result['width'],'root_error':float(abs(F(result['root'])-root)),
            'exact_halves':exact_halves}


def check():
    rows=[]; fixtures=[]
    for root,upper,tol,n,status,halves,max_iter in [
        (F(1,3),1.0,2**-8,8,'converged',True,30),
        (F(1,3),1.0,2**-18,18,'converged',True,30),
        (F(2,3),1.0,2**-12,12,'converged',True,30),
        (F(1,3),1.0,2**-18,4,'max_iter',True,4),
        (F(1,15),0.2,1e-6,18,'converged',False,30),
    ]:
        points=[]
        def objective(x):
            points.append(x)
            return float(F(x)-root)
        result=lab.bisection(objective,0.0,upper,atol=tol,rtol=0,max_iter=max_iter)
        row=audit(result,points,root,0.0,upper,n,status,halves)
        row.update({'points':list(points),'result':result,'exact_root':str(root)})
        rows.append(row)
        if status=='converged':
            assert result['width'] <= tol
            # Minimal theoretical budget, independent of the loop counter.
            assert F(upper)/2**n <= F(tol) < F(upper)/2**(n-1)
        fixtures.append((result,points,root,0.0,upper,n,status,halves))
    # Exercise 10 uses decimal 0.2; its stated mathematical count is also 18.
    assert F(1,5)/2**18 <= F(1,10**6) < F(1,5)/2**17
    base=fixtures[0]; mutations=[{'iterations':9},{'width':2*base[0]['width']},
                               {'root':0.0},{'status':'max_iter'}]
    detected=0
    for patch in mutations:
        try:
            audit(dict(base[0],**patch),*base[1:])
        except AssertionError:
            detected+=1
    assert detected==len(mutations)
    try:
        audit(base[0],base[1][:-1],*base[2:])
    except AssertionError:
        detected+=1
    assert detected==5
    return {'cases':rows,'exercise_10_bisections':18,'wrong_variants_detected':detected,
            'scope':'selected rational continuous affine roots; binary dyadic halving and rounded decimal-width exercise; not a generic continuity proof'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
