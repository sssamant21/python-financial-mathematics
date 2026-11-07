"""Check the distinct Section 8.3 wrapper and its shared centered stencil."""
import inspect
import json
import math
from pathlib import Path
import sys
from unittest.mock import patch
if len(sys.argv)==2:
    source_directory=Path(sys.argv[1]).resolve()
    if not (source_directory/"section_8_03.py").is_file():
        raise FileNotFoundError("requested source directory does not contain section_8_03.py")
    sys.path.insert(0,str(source_directory))
import section_8_01 as first
import section_8_03 as lab


def check():
    rows=[]
    def run(name,x,h,fn,expected,points):
        calls=[]
        def callback(at):
            calls.append(at if math.isfinite(at) else repr(at))
            return fn(at)
        try:
            actual=lab.centered_difference(callback,x,h)
            if not math.isfinite(actual): actual=repr(actual)
        except Exception as exc: actual=type(exc).__name__
        rows.append(dict(case=name,expected=expected,actual=actual,expected_calls=points,
                         actual_calls=calls,passed=actual==expected and calls==points))
    M=sys.float_info.max
    run("collapsed control",1.,1e-30,lambda p:p,"ValueError",[])
    run("nonfinite control",M,M,lambda p:1.,"ValueError",[])
    run("finite whole quotient",0.,M,lambda p:M if p>0 else -M,1.,[M,-M])
    run("genuine final overflow",0.,.25,lambda p:M if p>0 else -M,"ValueError",[.25,-.25])
    run("negative step",0.,-.5,lambda p:p,1.,[-.5,.5])
    value=inspect.signature(lab.centered_difference).parameters["step"].default
    rows.append(dict(case="public default retained",expected=1e-4,actual=value,passed=value==1e-4))
    calls=[]
    fn=lambda p:p
    def sentinel(function,x,h):
        calls.append([function is fn,x,h])
        return 7.
    try:
        with patch.object(lab,"_centered_difference",sentinel):
            actual=lab.centered_difference(fn,0.)
    except AttributeError:
        actual="missing shared wrapper"
    rows.append(dict(case="actual wrapper passes callback and default to helper",
                     expected=[7.,[[True,0.,1e-4]]],actual=[actual,calls],
                     passed=actual==7. and calls==[[True,0.,1e-4]]))
    same=getattr(lab,"_centered_difference",None) is first.centered_difference
    rows.append(dict(case="shared helper identity",expected=True,actual=same,passed=same))
    print(json.dumps(rows,allow_nan=False))
    return all(r["passed"] for r in rows)


if __name__=="__main__":
    raise SystemExit(0 if check() else 1)
