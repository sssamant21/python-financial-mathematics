"""Run with an isolated interpreter after installing numpy pandas matplotlib jupyterlab nbclient."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE=Path(__file__).resolve().parent
BOOK=HERE.parents[1]
SOURCE=BOOK/'chapter-01/1.05-setting-up-the-python-environment.md'


def main():
    checks=[]
    def record(name,actual,expected,ok):
        checks.append(dict(name=name,actual=actual,expected=expected,status='PASS' if ok else 'FAIL'))
    def command(name,args):
        proc=subprocess.run(args,text=True,capture_output=True,timeout=120)
        record(name,dict(stdout=proc.stdout,stderr=proc.stderr,exit_code=proc.returncode),'exit zero',proc.returncode==0)
        return proc
    source=SOURCE.read_text()
    blocks=re.findall(r'^```python\n(.*?)^```',source,re.M|re.S)
    record('isolated interpreter',dict(prefix=sys.prefix,base_prefix=sys.base_prefix),'prefix differs from base_prefix',sys.prefix!=sys.base_prefix)
    command('version',[sys.executable,'--version'])
    command('pip identity',[sys.executable,'-m','pip','--version'])
    command('pip dependency consistency',[sys.executable,'-m','pip','check'])
    listed=command('installed list',[sys.executable,'-m','pip','list','--format=json'])
    frozen=command('freeze',[sys.executable,'-m','pip','freeze'])
    (HERE/'requirements-resolved.txt').write_text(frozen.stdout)
    # Actual bash activation; no Windows/macOS emulation is claimed.
    activation=Path(sys.prefix)/'bin/activate'
    proc=subprocess.run(['bash','-c','source "$1"; python -c "import sys; print(sys.prefix)"','bash',str(activation)],text=True,capture_output=True,timeout=10)
    record('bash activation',proc.stdout.strip(),sys.prefix,proc.returncode==0 and proc.stdout.strip()==sys.prefix)
    versions={name:importlib.metadata.version(name) for name in ('numpy','pandas','matplotlib','jupyterlab','nbclient','ipykernel')}
    # Execute the exact six Python fences in the requested environment.
    for index,code in enumerate(blocks,1):
        result=subprocess.run([sys.executable,'-c',code],text=True,capture_output=True,timeout=30)
        expected={1:sys.executable,2:'NumPy: '+versions['numpy'],3:'1157.625',4:'370.0',5:sys.executable,6:sys.executable}[index]
        record(f'source Python fence {index}',dict(stdout=result.stdout,stderr=result.stderr,exit_code=result.returncode,sha256=hashlib.sha256(code.encode()).hexdigest()),expected,result.returncode==0 and expected in result.stdout and not result.stderr)
    command('JupyterLab CLI version',[str(Path(sys.executable).parent/'jupyter'),'lab','--version'])
    checks.append(dict(name='Notebook kernel execution',actual='Initial attempt: Operation not permitted (src/ip_resolver.cpp:542); Kernel died before replying to kernel_info',expected='Kernel starts and executes exact cells',status='BLOCKED_RUNTIME'))
    checks.append(dict(name='JupyterLab HTTP/browser validation',actual='Not executed after observed network/socket restriction; no server or browser success claimed',expected='Authenticated local HTTP and interactive UI validation',status='NOT_EXECUTED'))
    with tempfile.TemporaryDirectory(prefix='book1-git-probe-') as temp:
        # Git ignore behavior is exercised in an isolated test repository.
        project=Path(temp)/'git-probe';project.mkdir();(project/'.gitignore').write_text('.venv/\n');(project/'.venv').mkdir();(project/'.venv/probe').write_text('local')
        subprocess.run(['git','init','-q',str(project)],check=True)
        proc=subprocess.run(['git','-C',str(project),'check-ignore','.venv/probe'],text=True,capture_output=True)
        record('venv ignored by git',proc.stdout.strip(),'.venv/probe',proc.returncode==0 and proc.stdout.strip()=='.venv/probe')
    payload=dict(date='2026-10-29',source_revision='6d4d9828224dbd056da729644acb050ff690ce30',source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),python=sys.version,platform=platform.platform(),versions=versions,total=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),blocked=sum(c['status']=='BLOCKED_RUNTIME' for c in checks),not_executed=sum(c['status']=='NOT_EXECUTED' for c in checks),checks=checks)
    (HERE/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k!='checks'},indent=2))
    return bool(payload['failed'])

if __name__=='__main__':raise SystemExit(main())
