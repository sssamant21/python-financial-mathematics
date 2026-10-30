"""Observe return-event locals of unchanged source methods; no source rewriting."""
import json,math,runpy,sys
from pathlib import Path
import numpy as np
import pandas as pd

def clean(value):
    if value is None or value is pd.NA or value is pd.NaT:return None
    if isinstance(value,pd.Timestamp):return value.isoformat()
    if isinstance(value,pd.DataFrame):return dict(kind='DataFrame',index=clean(value.index.tolist()),columns=clean(value.columns.tolist()),values=clean(value.to_numpy().tolist()),dtypes=[str(x) for x in value.dtypes])
    if isinstance(value,pd.Series):return dict(kind='Series',name=value.name,index_name=value.index.name,index=clean(value.index.tolist()),values=clean(value.tolist()),dtype=str(value.dtype))
    if isinstance(value,pd.DatetimeIndex):return dict(kind='DatetimeIndex',values=clean(value.tolist()),timezone=str(value.tz),is_unique=value.is_unique)
    if isinstance(value,np.ndarray):return dict(kind='ndarray',shape=list(value.shape),dtype=str(value.dtype),values=clean(value.tolist()))
    if isinstance(value,(bool,np.bool_)):return bool(value)
    if isinstance(value,(int,np.integer)):return int(value)
    if isinstance(value,(float,np.floating)):return float(value) if math.isfinite(float(value)) else None
    if isinstance(value,str):return value
    if isinstance(value,(tuple,list)):return [clean(x) for x in value]
    if isinstance(value,dict):return {str(k):clean(v) for k,v in value.items()}
    return dict(unserialized_type=type(value).__name__)

script=Path(sys.argv[1]).resolve();destination=Path(sys.argv[2]);observed={}
def trace(frame,event,arg):
    if event=='return' and frame.f_code.co_filename==str(script) and frame.f_code.co_name.startswith('test_problem_'):
        observed[frame.f_code.co_name]={key:clean(value) for key,value in frame.f_locals.items() if key!='self'}
    return trace
sys.argv=[str(script),'-v'];status=0
try:
    sys.settrace(trace)
    runpy.run_path(str(script),run_name='__main__')
except SystemExit as error:
    status=error.code or 0
finally:
    sys.settrace(None)
    destination.write_text(json.dumps(observed,indent=2,allow_nan=False)+'\n')
raise SystemExit(status)
