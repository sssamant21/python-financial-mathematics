"""Direct solver error contracts and externally observed callback sequencing."""
import json
import math
import section_18_09 as lab


def invalid_controls(solve):
    cases=[('rtol',v,ValueError if type(v) is not bool else TypeError)
           for v in (-1.0,math.nan,math.inf,True)]
    cases.extend(('max_iter',v,ValueError) for v in (0,-1,True,1.0,'1'))
    records=[]
    for key,value,error in cases:
        events=[]
        def f(x):events.append(('f',x));return x*x-2
        def df(x):events.append(('df',x));return 2*x
        try:solve(f,df,1.0,2.0,**{key:value})
        except error as exc:
            assert not events
            records.append({'control':key,'value':repr(value),'exception':type(exc).__name__})
        else:raise AssertionError('invalid control accepted: '+key+'='+repr(value))
    return records


def derivative_errors(solve):
    records=[]
    for value,error in ((math.nan,ValueError),(math.inf,ValueError),(-math.inf,ValueError),
                        (True,TypeError),('bad',TypeError)):
        events=[]
        def f(x):events.append(('f',x));return x*x-2
        def df(x):events.append(('df',x));return value
        try:solve(f,df,1.0,2.0)
        except error as exc:
            assert events==[('f',1.0),('f',2.0),('f',1.5),('df',1.5)]
            records.append({'value':repr(value),'exception':type(exc).__name__,'events':events})
        else:raise AssertionError('invalid derivative was accepted')
    return records


def check():
    controls=invalid_controls(lab.solve);derivatives=derivative_errors(lab.solve)
    # With zero derivative and one update: endpoint, current point, fallback
    # proposal and final midpoint evaluation points are known independently.
    sequence=[('f',1.0),('f',2.0),('f',1.5),('df',1.5),('f',1.5),('f',1.25)]
    objective_records=[]
    for fail_at in range(1,6):
        for value,error in ((math.nan,ValueError),(math.inf,ValueError),(True,TypeError)):
            events=[];calls=0
            def f(x):
                nonlocal calls
                calls+=1;events.append(('f',x))
                return value if calls==fail_at else x*x-2
            def df(x):events.append(('df',x));return 0.0
            try:lab.solve(f,df,1.0,2.0,max_iter=1)
            except error as exc:
                stop=[i for i,e in enumerate(sequence) if e[0]=='f'][fail_at-1]
                assert events==sequence[:stop+1]
                objective_records.append({'objective_call':fail_at,'value':repr(value),
                                          'exception':type(exc).__name__,'events':events})
            else:raise AssertionError('invalid objective accepted')
    skipped=[]
    for name,f,a,b,options,status in (
            ('endpoint',lambda x:x-1,1.0,2.0,{},'endpoint_root'),
            ('exact_midpoint',lambda x:x-1.5,1.0,2.0,{},'exact_root'),
            ('initial_width',lambda x:x*x-2,1.0,2.0,{'atol':2.0,'rtol':0.0},'converged')):
        d_events=[]
        def bad_derivative(x):d_events.append(x);return math.nan
        report=lab.solve(f,bad_derivative,a,b,**options)
        assert not d_events and report['derivative_evaluations']==0 and report['status']==status
        skipped.append({'case':name,'report':report})
    fallbacks=[]
    for slope in (0.0,math.nextafter(0.0,1.0)):
        f_events=[];d_events=[]
        def f(x):f_events.append(x);return x-0.375
        def df(x):d_events.append(x);return slope
        result=lab.solve(f,df,0.0,1.0)
        assert result['root']==0.375 and result['status']=='exact_root'
        assert result['bisection_steps']==3 and result['newton_steps']==0
        assert result['function_evaluations']==len(f_events)==8
        assert result['derivative_evaluations']==len(d_events)==3
        assert [row['proposal'] for row in result['trace']]==[0.5,0.25,0.375]
        fallbacks.append({'supplied_slope':slope,'report':result,'f_events':f_events,'df_events':d_events})
    class CallbackFailure(RuntimeError):pass
    propagated=[]
    for which in ('f','df'):
        failure=CallbackFailure('selected '+which+' failure')
        def broken(x):raise failure
        try:lab.solve(broken if which=='f' else lambda x:x*x-2,
                      broken if which=='df' else lambda x:2*x,1.0,2.0)
        except CallbackFailure as exc:
            assert exc is failure;propagated.append(which)
        else:raise AssertionError('callback exception swallowed')
    # Endpoint evaluation is eager: an exact lower root does not suppress an
    # invalid upper endpoint evaluation. Characterize the existing policy.
    eager=[]
    def endpoint(x):eager.append(x);return 0.0 if x==1.0 else math.nan
    try:lab.solve(endpoint,lambda x:1.0,1.0,2.0)
    except ValueError:assert eager==[1.0,2.0]
    else:raise AssertionError('nonfinite upper endpoint ignored')
    detected=[]
    def swallow(*args,**kwargs):
        try:return lab.solve(*args,**kwargs)
        except (ValueError,TypeError):return {'status':'converged'}
    try:derivative_errors(swallow)
    except AssertionError:detected.append('swallowed_evaluation_error')
    else:raise AssertionError('undetected swallowed error')
    def coerced_budget(*args,**kwargs):
        if 'max_iter' in kwargs:kwargs['max_iter']=int(kwargs['max_iter'])
        return lab.solve(*args,**kwargs)
    try:invalid_controls(coerced_budget)
    except AssertionError:detected.append('coerced_iteration_budget')
    else:raise AssertionError('undetected budget coercion')
    return {'invalid_controls':controls,'invalid_derivatives':derivatives,
            'objective_error_paths':objective_records,'unneeded_derivative_paths':skipped,
            'fallback_paths':fallbacks,'propagated_callback_exceptions':propagated,
            'eager_endpoint_evaluations':eager,'wrong_policies_detected':detected,
            'scope':'selected pure/control-injected callbacks; no financial model or continuity certification'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
