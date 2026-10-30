"""Reproduce retained QA path collision and preserve original child diagnostics."""
import importlib.util
import json
from pathlib import Path
import subprocess
import traceback

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('initial_511_review',HERE/'initial-review.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
original_run=subprocess.run
records=[]
def observed(*args,**kwargs):
    result=original_run(*args,**kwargs)
    records.append(dict(args=[str(x) for x in args[0]],returncode=result.returncode,
                        stdout=result.stdout,stderr=result.stderr))
    return result
subprocess.run=observed
try:
    module.run()
    failure='NO FAILURE'
except Exception:
    failure=traceback.format_exc()
finally:
    subprocess.run=original_run
expected=any(r['returncode']!=0 and 'FileExistsError' in r['stderr']
             and r['args'][r['args'].index('--input')+1]=='whitespace.json'
             and r['args'][-1].endswith('/whitespace.json') for r in records if '--input' in r['args'])
expected=expected and 'ValueError: unsuccessful process' in failure
(HERE/'failure-reproduction.json').write_text(json.dumps(dict(expected_failure_observed=expected,
    records=records,runner_traceback=failure),indent=2)+'\n')
print('Expected retained QA failure reproduced:',expected)
raise SystemExit(0 if expected else 1)
