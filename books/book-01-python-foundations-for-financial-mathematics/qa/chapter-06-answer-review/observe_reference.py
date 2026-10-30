"""Read local values from exact reference test frames, without editing code.

This is a supplemental observer rerun of the same twenty existing methods.
No timing/performance inference is made under tracing.
"""
import json,math,runpy,sys,unittest
import numpy as np

def encode(value):
    if isinstance(value,np.ndarray):
        return dict(shape=list(value.shape),dtype=str(value.dtype),nbytes=value.nbytes,
                    values=encode(value.tolist()) if value.size<=1000 else 'OMITTED_LARGE_PAYLOAD')
    if isinstance(value,np.generic):return encode(value.item())
    if isinstance(value,float) and not math.isfinite(value):return repr(value)
    if isinstance(value,(str,int,float,bool)) or value is None:return value
    if isinstance(value,(list,tuple)):return [encode(x) for x in value]
    if isinstance(value,dict):return {str(k):encode(v) for k,v in value.items()}
    return type(value).__name__

module=runpy.run_path(sys.argv[1]);records={}
def trace(frame,event,arg):
    if event=='return' and frame.f_code.co_name.startswith('test_problem_'):
        records[frame.f_code.co_name]={k:encode(v) for k,v in frame.f_locals.items() if k!='self'}
    return trace
suite=unittest.defaultTestLoader.loadTestsFromTestCase(module['ChapterSixSolutions'])
result=unittest.TestResult()
sys.settrace(trace)
try:suite.run(result)
finally:sys.settrace(None)
print(json.dumps(dict(tests_run=result.testsRun,successful=result.wasSuccessful(),
    failures=[(str(t),message) for t,message in result.failures],
    errors=[(str(t),message) for t,message in result.errors],locals=records),sort_keys=True,allow_nan=False))
raise SystemExit(not result.wasSuccessful())
