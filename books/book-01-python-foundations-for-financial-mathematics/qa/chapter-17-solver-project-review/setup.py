"""Attempt the printed Linux clean-venv setup without changing global packages."""
import hashlib,json,os,platform,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
records=[];source_hash=None;implementation_hash=None;tests_hash=None
def run(label,args,cwd,timeout):
    try:
        p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=timeout,env={**os.environ,'PIP_RETRIES':'0','PIP_TIMEOUT':'10','PIP_DISABLE_PIP_VERSION_CHECK':'1'})
        row=dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,timed_out=False)
    except subprocess.TimeoutExpired as e:
        row=dict(label=label,args=args,returncode=None,stdout=(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else (e.stdout or ''),stderr=(e.stderr or b'').decode() if isinstance(e.stderr,bytes) else (e.stderr or ''),timed_out=True)
    records.append(row);return row['returncode']==0
with tempfile.TemporaryDirectory(prefix='book1-1714-setup-') as tmp:
    created=run('printed clean venv creation',[sys.executable,'-m','venv','.venv'],tmp,30)
    if created:
        executable=str(Path(tmp)/'.venv/bin/python')
        installed=run('printed SciPy install in clean venv',[executable,'-m','pip','install','scipy'],tmp,45)
        if installed:
            run('clean venv installed dependency import/version',[executable,'-c','import sys,scipy,numpy;print(sys.version);print(scipy.__version__);print(numpy.__version__)'],tmp,15)
            data=(HERE.parents[1]/'chapter-17/17.14-chapter-project-financial-numerical-solver.md').read_bytes()
            blocks=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)
            Path(tmp,'financial_solver.py').write_bytes(blocks[0]);Path(tmp,'test_financial_solver.py').write_bytes(blocks[1])
            source_hash=hashlib.sha256(data).hexdigest();implementation_hash=hashlib.sha256(blocks[0]).hexdigest();tests_hash=hashlib.sha256(blocks[1]).hexdigest()
            run('clean venv exact project demonstration',[executable,'-B','financial_solver.py'],tmp,30)
            run('clean venv same twelve existing methods',[executable,'-B','-m','unittest','-v','test_financial_solver'],tmp,30)
            run('clean venv compile both exact files',[executable,'-B','-m','compileall','-q','financial_solver.py','test_financial_solver.py'],tmp,30)
            run('clean venv silent imports',[executable,'-B','-c','import financial_solver,test_financial_solver'],tmp,30)
result=dict(python=platform.python_version(),platform=platform.platform(),records=records,source_sha256=source_hash,implementation_sha256=implementation_hash,tests_sha256=tests_hash,scope='Actual Linux clean-venv creation/install/import and same exact project commands. Existing supported-runtime scientific results are separate; repeated methods are not new unique methods. No Windows/PowerShell/notebook/platform-matrix acceptance.')
(HERE/'setup-results.json').write_text(json.dumps(result,indent=2)+'\n')
print([(x['label'],x['returncode'],x['timed_out']) for x in records])
