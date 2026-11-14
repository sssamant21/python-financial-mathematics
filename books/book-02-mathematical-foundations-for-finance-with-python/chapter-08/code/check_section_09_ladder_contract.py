"""Bounded caller prefixes,late failures and report contracts;not a resource cap API."""
import json,itertools
import section_8_09 as source

def observations():
    rows=[];trace=[]
    def add(name,actual,expected):rows.append(dict(name=name,actual=actual,expected=expected,passed=actual==expected))
    def f(x):trace.append(['f',x]);return x**3
    def d1(x):trace.append(['d1',x]);return 3*x*x
    def d2(x):trace.append(['d2',x]);return 6*x
    reports=source.step_ladder(f,d1,2.,iter([.5,.25]),d2,0.,0.)
    for report,h in zip(reports,[.5,.25]):
        expected={'forward':(12+6*h+h*h,6*h+h*h),'backward':(12-6*h+h*h,-6*h+h*h),'centered':(12+h*h,h*h),'richardson':(12.,0.)}
        for name,(estimate,error) in expected.items():
            add(f'h{h} {name} full row',report['first_derivatives'][name],dict(estimate=estimate,signed_error=error,absolute_error=abs(error),pass_=error==0))
            # Use actual schema key 'pass',not a language-keyword workaround in the oracle.
            row=rows[-1];row['expected']['pass']=row['expected'].pop('pass_');row['passed']=row['actual']==row['expected']
        add(f'h{h} second full row',report['second_derivative'],dict(analytic=12.,estimate=12.,signed_error=0.,absolute_error=0.,**{'pass':True}))
        add(f'h{h} report keys',sorted(report),sorted(['x','step','analytic_first','abs_tol','rel_tol','comparison_rule','first_derivatives','second_derivative']))
    add('caller order and initial fourteen calls',[[x['step'] for x in reports],len(trace)],[[.5,.25],14])
    trace.clear();repeated=source.step_ladder(f,d1,2.,[.25,.25],d2,0.,0.)
    add('duplicate steps retained and reevaluated',[repeated[0]==repeated[1],len(repeated),len(trace)],[True,2,14])
    trace.clear();add('empty ladder bypasses per-step validation',source.step_ladder(None,None,float('nan'),[],abs_tol=-1),[]);add('empty has no callbacks',trace,[])
    trace.clear();first_only=source.step_ladder(f,d1,2.,[.25]);add('first-only report and six callbacks',['second_derivative' in first_only[0],len(trace)],[False,6])
    trace.clear()
    try:source.step_ladder(f,d1,2.,None,d2);error='returned'
    except Exception as exc:error=type(exc).__name__
    add('noniterable steps before callbacks',[error,len(trace)],['TypeError',0])
    trace.clear();steps=iter([.5,0.,.125]);returned=False
    try:source.step_ladder(f,d1,2.,steps,d2);returned=True;error='none'
    except Exception as exc:error=type(exc).__name__
    add('late invalid step no returned partial list',[returned,error,len(trace)],[False,'ValueError',7])
    add('bad step consumed,next step unconsumed',next(steps),.125)
    trace.clear();sentinel=RuntimeError('callback sentinel');fcalls=0
    def late_f(x):
        nonlocal fcalls
        fcalls+=1
        if fcalls==6:raise sentinel
        return f(x)
    try:source.step_ladder(late_f,d1,2.,[.5,.25],d2);identity=False
    except RuntimeError as exc:identity=exc is sentinel
    add('late callback exception identity and previous work',[identity,fcalls,len(trace)],[True,6,7])
    trace.clear();sentinel2=RuntimeError('iterator sentinel')
    def failing_steps():yield .5;raise sentinel2
    try:source.step_ladder(f,d1,2.,failing_steps(),d2);identity=False
    except RuntimeError as exc:identity=exc is sentinel2
    add('late iterator error propagates after first report',[identity,len(trace)],[True,7])
    trace.clear();pulls=[]
    def unbounded_steps():
        i=0
        while True:
            pulls.append(i);yield .5/(2**i);i+=1
    bounded=source.step_ladder(f,d1,2.,itertools.islice(unbounded_steps(),2),d2,0.,0.)
    add('caller islice bounds pulls and work',[len(bounded),len(pulls),len(trace)],[2,2,14])
    encoded=json.dumps(reports,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    add('standard JSON roundtrip',json.loads(encoded),reports)
    add('selected two-report output budget',len(encoded)<=4096,True)
    return rows,dict(selected_reports=reports,serialized_bytes=len(encoded),selected_output_budget=4096,bounded_prefix_steps=2,bounded_prefix_pulls=len(pulls),bounded_prefix_callbacks=len(trace),limits='Caller-supplied finite prefix only;step_ladder has no built-in cap or rollback;arbitrary callback cost and nested input resources unbounded')
if __name__=='__main__':
    rows,report=observations();print(json.dumps(dict(predicates=rows,resource_report=report),indent=2));print(len(rows),'ladder predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
