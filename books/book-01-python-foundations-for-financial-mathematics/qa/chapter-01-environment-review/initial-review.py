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
    import nbformat
    from nbclient import NotebookClient
    with tempfile.TemporaryDirectory(prefix='book1-notebook-') as temp:
        notebook=nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('import sys\nprint(sys.executable)'),nbformat.v4.new_code_cell(blocks[1]),nbformat.v4.new_code_cell(blocks[2]),nbformat.v4.new_code_cell(blocks[3])])
        notebook.metadata.kernelspec=dict(name='python3',display_name='Python 3',language='python')
        env=os.environ.copy();env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
        old=os.environ.get('PATH');os.environ['PATH']=env['PATH']
        try:
            NotebookClient(notebook,timeout=60,kernel_name='python3',resources={'metadata':{'path':temp}}).execute()
        finally:
            if old is None:os.environ.pop('PATH',None)
            else:os.environ['PATH']=old
        texts=[''.join(o.get('text','') for o in cell.outputs) for cell in notebook.cells]
        record('notebook kernel identity',texts[0].strip(),sys.executable,texts[0].strip()==sys.executable)
        record('notebook exact financial cell',texts[2].strip(),'1157.625',texts[2].strip()=='1157.625')
        record('notebook exact NumPy cell',texts[3].strip(),'array output and sum 370.0',texts[3].strip().endswith('370.0'))
        nbformat.write(notebook,HERE/'executed-smoke.ipynb')
        # Serve local authenticated JupyterLab, verify HTTP, then stop it.
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        token=secrets.token_hex(24)
        args=[str(Path(sys.executable).parent/'jupyter'),'lab','--no-browser','--ip=127.0.0.1',f'--port={port}','--ServerApp.port_retries=0','--ServerApp.allow_root=True',f'--IdentityProvider.token={token}',f'--ServerApp.root_dir={temp}']
        with tempfile.TemporaryFile(mode='w+') as log:
            server=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT)
            status=None
            try:
                for _ in range(100):
                    if server.poll() is not None:break
                    try:
                        req=urllib.request.Request(f'http://127.0.0.1:{port}/lab',headers={'Authorization':'token '+token})
                        with urllib.request.urlopen(req,timeout=1) as response:
                            status=response.status;html=response.read().decode()
                        if status==200:break
                    except OSError:time.sleep(.1)
                record('JupyterLab authenticated local HTTP',status,'HTTP 200 with JupyterLab HTML',status==200 and 'jupyter' in html.lower())
            finally:
                server.terminate()
                try:server.wait(timeout=10)
                except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
            record('JupyterLab stopped',server.poll(),'process exited',server.poll() is not None)
        # Git ignore behavior is exercised in an isolated test repository.
        project=Path(temp)/'git-probe';project.mkdir();(project/'.gitignore').write_text('.venv/\n');(project/'.venv').mkdir();(project/'.venv/probe').write_text('local')
        subprocess.run(['git','init','-q',str(project)],check=True)
        proc=subprocess.run(['git','-C',str(project),'check-ignore','.venv/probe'],text=True,capture_output=True)
        record('venv ignored by git',proc.stdout.strip(),'.venv/probe',proc.returncode==0 and proc.stdout.strip()=='.venv/probe')
    payload=dict(date='2026-10-29',source_revision='6d4d9828224dbd056da729644acb050ff690ce30',source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),python=sys.version,platform=platform.platform(),versions=versions,total=len(checks),passed=sum(c['status']=='PASS' for c in checks),failed=sum(c['status']=='FAIL' for c in checks),checks=checks)
    (HERE/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k!='checks'},indent=2))
    return bool(payload['failed'])

if __name__=='__main__':raise SystemExit(main())
