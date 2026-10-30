"""Supplemental observer: execute an unchanged source script, retain child results.

No subprocess arguments, return codes or streams are changed. Never record env.
"""
import json,runpy,subprocess,sys
from pathlib import Path
script=Path(sys.argv[1]).resolve();destination=Path(sys.argv[2]).resolve();records=[]
original_run=subprocess.run
def string(value):
 if isinstance(value,bytes):return value.decode('utf-8',errors='replace')
 return value

def observe(*args,**kwargs):
 result=original_run(*args,**kwargs)
 records.append(dict(args=[str(x) for x in result.args] if not isinstance(result.args,str) else result.args,returncode=result.returncode,stdout=string(result.stdout),stderr=string(result.stderr)))
 return result
subprocess.run=observe
# Match normal direct-file launch semantics, including its sibling helper import.
sys.path[0]=str(script.parent)
sys.argv=[str(script)]
try:runpy.run_path(str(script),run_name='__main__')
finally:destination.write_text(json.dumps(records,indent=2)+'\n')
