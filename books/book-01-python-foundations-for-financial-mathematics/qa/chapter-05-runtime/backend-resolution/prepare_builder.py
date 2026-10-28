"""Verify a downloaded setuptools 84.0.0 wheel against PyPI and prepare a builder.
Usage: python prepare_builder.py BACKEND_DIRECTORY
"""
import hashlib,json,pathlib,subprocess,sys,urllib.request,venv,os
out=pathlib.Path(sys.argv[1]).resolve();wheel=out/'setuptools-84.0.0-py3-none-any.whl'
metadata_url='https://pypi.org/pypi/setuptools/84.0.0/json'
with urllib.request.urlopen(metadata_url,timeout=30) as response:metadata=json.load(response)
entry=next(x for x in metadata['urls'] if x['filename']==wheel.name)
actual=hashlib.sha256(wheel.read_bytes()).hexdigest();assert actual==entry['digests']['sha256']
builder=out/'builder';venv.EnvBuilder(with_pip=True,system_site_packages=False).create(builder)
python=builder/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
env=os.environ.copy();env.pop('PYTHONPATH',None);env.pop('PYTHONHOME',None)
proc=subprocess.run([str(python),'-m','pip','--isolated','install','--no-index','--no-deps',str(wheel)],cwd=out,env=env,text=True,capture_output=True,timeout=90)
(out/'builder-install.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stdout+proc.stderr
proc=subprocess.run([str(python),'-I','-c','import json,platform;from importlib.metadata import version;print(json.dumps({"python":platform.python_version(),"pip":version("pip"),"setuptools":version("setuptools")}))'],cwd=out,env=env,text=True,capture_output=True,timeout=30)
assert proc.returncode==0;versions=json.loads(proc.stdout);assert versions['setuptools']=='84.0.0'
evidence={'metadata_url':metadata_url,'artifact_url':entry['url'],'filename':wheel.name,'sha256':actual,'published_sha256':entry['digests']['sha256'],'hash_match':True,'artifact_bytes':wheel.stat().st_size,'builder_versions':versions,'download_command':['python','-m','pip','download','--disable-pip-version-check','--no-deps','--only-binary=:all:','--retries','0','--timeout','20','--dest',str(out),'setuptools==84.0.0']}
(out/'builder-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps(evidence,indent=2))
