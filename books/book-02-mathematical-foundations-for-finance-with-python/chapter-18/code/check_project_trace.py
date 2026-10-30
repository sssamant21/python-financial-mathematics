"""Externally observed callback and exact-polynomial trace audit for 18.9."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction as F
import json
import math
import section_18_09 as lab


def opposite(a,b):
    return min(a,b)<0<max(a,b)


def audit(result,events,f,df,lower,upper):
    function=[e for e in events if e[0]=='f'];derivative=[e for e in events if e[0]=='df']
    assert result['function_evaluations']==len(function)
    assert result['derivative_evaluations']==len(derivative)
    assert events[:2]==[('f',lower,f(lower)),('f',upper,f(upper))]
    assert result['iterations']==len(result['trace'])
    assert result['newton_steps']==sum(row['step_type']=='newton' for row in result['trace'])
    assert result['bisection_steps']==sum(row['step_type']=='bisection' for row in result['trace'])
    a,b=lower,upper;fa,fb=f(a),f(b);x=a+(b-a)/2;cursor=2
    for index,row in enumerate(result['trace'],1):
        assert row['iteration']==index and (row['lower'],row['upper'])==(a,b)
        assert opposite(fa,fb)
        fx=f(x);slope=df(x)
        assert fx!=0
        assert events[cursor:cursor+2]==[('f',x,fx),('df',x,slope)]
        cursor+=2
        width=float(F(b)-F(a));midpoint=float(F(a)+F(width)/2)
        # Independently round the quotient and subtraction for the documented
        # binary64 proposal, rather than taking the reported step on trust.
        candidate=None
        if slope:
            quotient=float(F(fx)/F(slope))
            candidate=float(F(x)-F(quotient))
        left=float(F(a)+F(width)/4);right=float(F(b)-F(width)/4)
        use_newton=candidate is not None and left<candidate<right
        expected=candidate if use_newton else midpoint
        assert row['proposal']==expected
        assert row['step_type']==('newton' if use_newton else 'bisection')
        fp=f(expected)
        assert row['residual']==fp and events[cursor]==('f',expected,fp)
        cursor+=1
        assert a<expected<b
        if fp==0:
            a=b=expected;break
        if opposite(fa,fp):b,fb=expected,fp
        else:a,fa=expected,fp
        assert opposite(fa,fb)
        assert b-a<=0.75*width+math.ulp(width)
        x=expected
    status=result['status'];root=result['root']
    if status=='endpoint_root':
        assert not result['trace'] and f(root)==0 and root in (lower,upper)
        a=b=root
    elif status=='exact_root':
        assert f(root)==0
        if cursor<len(events):
            assert events[cursor:]==[('f',root,0.0)] and root==x
            cursor+=1
        a=b=root
    else:
        midpoint=float(F(a)+F(float(F(b)-F(a)))/2)
        assert root==midpoint
        assert events[cursor:]==[('f',root,f(root))]
        cursor+=1
        threshold=result['tolerances']['atol']+result['tolerances']['rtol']*max(abs(a),abs(b))
        if status=='converged':assert b-a<=threshold
        elif status=='max_iter':assert result['iterations']==result['max_iter'] and b-a>threshold
        elif status=='stagnation':assert root in (a,b)
        else:raise AssertionError(status)
    if status=='endpoint_root':assert len(events)==2
    else:assert cursor==len(events)
    assert result['bracket']==(a,b) and result['width']==b-a
    assert result['residual']==f(root)


def check():
    quadratic=lambda x:float(F(x)**2-2)
    derivative=lambda x:2*x
    zero=lambda x:0.0
    affine=lambda root:lambda x:float(F(x)-root)
    one=lambda x:1.0
    adjacent=math.nextafter(1.0,2.0)
    between=(F(1)+F(adjacent))/2
    cases=[('newton',quadratic,derivative,1.0,2.0,1e-12,0.0,100),
           ('zero_derivative',quadratic,zero,1.0,2.0,1e-12,0.0,100),
           ('interior_exact',affine(F(3,8)),one,0.0,1.0,1e-12,0.0,20),
           ('lower_quarter',affine(F(1,4)),one,0.0,1.0,1e-12,0.0,20),
           ('upper_quarter',affine(F(3,4)),one,0.0,1.0,1e-12,0.0,20),
           ('midpoint_exact',affine(F(1,2)),one,0.0,1.0,1e-12,0.0,20),
           ('endpoint',affine(F(1)),one,1.0,2.0,1e-12,0.0,20),
           ('initial_width',quadratic,derivative,1.0,2.0,2.0,0.0,20),
           ('exhausted',quadratic,zero,1.0,2.0,1e-16,0.0,1),
           ('adjacent',affine(between),one,1.0,adjacent,1e-20,0.0,20)]
    records=[];fixtures={}
    for name,f,df,a,b,atol,rtol,budget in cases:
        events=[]
        def objective(x):
            value=f(x);events.append(('f',x,value));return value
        def slope(x):
            value=df(x);events.append(('df',x,value));return value
        result=lab.solve(objective,slope,a,b,atol,rtol,budget)
        audit(result,events,f,df,a,b)
        if name in ('newton','zero_derivative'):
            with localcontext() as ctx:
                ctx.prec=100;root=Decimal(2).sqrt()
                assert Decimal.from_float(result['bracket'][0])<=root<=Decimal.from_float(result['bracket'][1])
                assert abs(Decimal.from_float(result['root'])-root)<=Decimal.from_float(result['width'])/2
        if name in ('lower_quarter','upper_quarter'):
            assert result['trace'][0]['step_type']=='bisection'
        if name=='interior_exact':assert result['trace'][0]['step_type']=='newton'
        fixtures[name]=(result,events,f,df,a,b)
        records.append({'case':name,'result':result,'observed_events':events})
    base,events,f,df,a,b=fixtures['newton'];detected=[]
    for name in ('endpoint','proposal','function_count','root_residual','step_kind'):
        bad=copy.deepcopy(base)
        if name=='endpoint':bad['trace'][0]['lower']=0.0
        elif name=='proposal':bad['trace'][0]['proposal']=1.0
        elif name=='function_count':bad['function_evaluations']+=1
        elif name=='root_residual':bad['residual']=1.0
        else:bad['trace'][0]['step_type']='bisection' if bad['trace'][0]['step_type']=='newton' else 'newton'
        try:audit(bad,events,f,df,a,b)
        except AssertionError:detected.append(name)
        else:raise AssertionError('undetected trace variant '+name)
    return {'selected_cases':records,'wrong_reports_detected':detected,
            'scope':'pure selected polynomial callbacks; conditional sign brackets, not continuity proof'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
