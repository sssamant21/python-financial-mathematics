"""Repack provided installed dependency payloads for an offline clean consumer.
Not vendor wheels or approval of release provenance. External installed files (script wrappers/man pages)
are omitted;wheel entry_points generate consumer scripts where applicable.
"""
from pathlib import Path
from importlib import metadata
import sys,json,hashlib,base64,tempfile,shutil
try:
 from wheel._commands.pack import pack
except ImportError:
 from wheel.cli.pack import pack
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
names=[];queue=['matplotlib'];closure=[]
while queue:
 name=canonicalize_name(queue.pop(0))
 if name in names:continue
 d=metadata.distribution(name);names.append(name)
 for spec in d.requires or []:
  req=Requirement(spec)
  if req.marker is not None and not req.marker.evaluate({'extra':''}):continue
  version=metadata.version(req.name);assert not req.specifier or req.specifier.contains(version,prereleases=True),(name,spec,version)
  queue.append(req.name);closure.append(dict(parent=name,requirement=spec,provided_version=version))
dest=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve();rows=[]
for name in names:
 d=metadata.distribution(name);root=Path(d.locate_file('')).resolve();files=[];omitted=[]
 with tempfile.TemporaryDirectory() as temp:
  stage=Path(temp)
  for f in d.files:
   p=Path(d.locate_file(f)).resolve()
   if not p.is_relative_to(root):omitted.append(str(f));continue
   rel=p.relative_to(root)
   if p.suffix=='.pyc' or '__pycache__' in p.parts or p.name=='RECORD':continue
   if not p.is_file():raise FileNotFoundError(p)
   raw=p.read_bytes()
   if f.hash:
    actual=base64.urlsafe_b64encode(hashlib.new(f.hash.mode,raw).digest()).rstrip(b'=').decode();assert actual==f.hash.value,(name,str(f))
   q=stage/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);files.append(dict(path=str(rel),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
  before=set(dest.glob('*.whl'));pack(str(stage),str(dest),None);new=set(dest.glob('*.whl'))-before;assert len(new)==1;wheel=new.pop();digest=hashlib.sha256(json.dumps(sorted(files,key=lambda x:x['path']),sort_keys=True,separators=(',',':')).encode()).hexdigest();rows.append(dict(distribution=name,version=d.version,source_root=str(root),files=len(files),source_tree_sha256=digest,omitted_external_wrappers=omitted,wheel=wheel.name,wheel_sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),wheel_bytes=wheel.stat().st_size,record_hashes_verified=True))
output.write_text(json.dumps(dict(dependencies=rows,default_dependency_closure=closure,limits='Local provided-runtime payload snapshots repacked offline,not vendor artifacts,canonical hashes,full CLI distribution preservation,approved provenance or cross-platform acceptance. Exact installed RECORD hashes checked where supplied;wheel RECORD regenerated.'),indent=2)+'\n');print('SNAPSHOTS',len(rows))
