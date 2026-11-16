"""Pinned18.3 source calls versus fresh-seed chunks and external state continuation.
Usage: python THIS first|replay
"""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,inspect
from fractions import Fraction as F
here=Path(__file__).resolve().parent;root=here.parents[3];pin='1ba1206bc29ac02dbdbc0576fd41cc953463bc52';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.03-reproducible-simulation.md';stem=sys.argv[1];raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(fences)==4;rows=[];commands=[];partitions=[]
def check(name,ok,**data):rows.append(dict(name=name,passed=bool(ok),**data));assert ok,name
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);s=t/'reproducible_simulation.py';s.write_text(fences[-1])
 for argv in [[sys.executable,s.name],[sys.executable,'-m','compileall','-q',s.name]]:
  z=subprocess.run(argv,cwd=t,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 spec=importlib.util.spec_from_file_location('reference_repro',s);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);Original=m.random.Random
 def capture(n):
  trace=[]
  class Traced:
   def __init__(self,seed):self.inner=Original(seed)
   def random(self):u=self.inner.random();trace.append(u);return u
  m.random.Random=Traced
  try:manifest=m.run(42,n,.6)
  finally:m.random.Random=Original
  want=sum(F(u)<F(3,5) for u in trace)
  check('count '+str(n),manifest['up_count']==want,actual=manifest['up_count'],expected=want,kind='source report from observed draws')
  check('mean '+str(n),manifest['mean']==float(F(90)+F(20*want,n)),actual=manifest['mean'],independent_expected=str(F(90)+F(20*want,n)),kind='independent count arithmetic')
  check('constructor restored '+str(n),m.random.Random is Original,kind='observer restoration')
  return manifest,trace
 full,draws=capture(8);full_count=full['up_count']
 check('native signature has no state/offset argument',list(inspect.signature(m.run).parameters)==['seed','count','up_probability'],kind='source API boundary')
 for n in (2,3,4,5,6):
  left,L=capture(n);right,R=capture(8-n);stitched=L+R;total=left['up_count']+right['up_count'];combined=F(90)+F(20*total,8)
  check('partition '+str(n)+' left fresh prefix',L==draws[:n],kind='source draw-order observation')
  check('partition '+str(n)+' right fresh prefix',R==draws[:8-n],kind='source draw-order observation')
  check('partition '+str(n)+' restarted draw mapping differs',stitched!=draws,kind='source draw-order observation')
  check('partition '+str(n)+' aggregate count mean',float(combined)==(n*left['mean']+(8-n)*right['mean'])/8,kind='caller aggregate arithmetic')
  parent=Original(42);prefix=[parent.random() for _ in range(n)];state=parent.getstate();resumed=Original();resumed.setstate(state);suffix=[resumed.random() for _ in range(8-n)]
  check('partition '+str(n)+' external continuation trace',prefix+suffix==draws,kind='supplemental trusted-state continuation')
  correct_count=sum(F(u)<F(3,5) for u in prefix+suffix)
  check('partition '+str(n)+' external continuation count',correct_count==full_count,kind='supplemental trusted-state continuation')
  partitions.append(dict(sizes=[n,8-n],left_manifest=left,right_manifest=right,restarted_draw_hex=[u.hex() for u in stitched],full_draw_hex=[u.hex() for u in draws],restarted_count=total,full_count=full_count,restarted_mean=float(combined),full_mean=full['mean'],same_aggregate_mean=float(combined)==full['mean'],same_draw_mapping=stitched==draws,external_state_resume_matches=True,checkpoint_state_sha256=hashlib.sha256(repr(state).encode()).hexdigest()))
 four=next(x for x in partitions if x['sizes']==[4,4]);check('chosen4plus4restart changes mean',four['restarted_mean']==105 and full['mean']==100,kind='selected source/caller illustration')
 check('matching aggregates do not imply matching draw mapping',any(x['same_aggregate_mean'] and not x['same_draw_mapping'] for x in partitions),kind='reproducibility interpretation')
 assert s.read_text()==fences[-1]
result=dict(source_revision=pin,source_path=path,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=[hashlib.sha256(c.encode()).hexdigest() for c in fences],python=sys.version,platform=platform.platform(),commands=commands,rows=rows,passed=len(rows),failed=0,full_manifest=full,full_manifest_digest=m.manifest_digest(full),partitions=partitions,limits='Source API always starts fresh local seed;trustedstatecontinuation andchunkaggregation are supplemental. Matchingmeans/digestsnotindependence/model/security/platformapproval;no nativecheckpointAPI invented.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(len(rows),'predicates;',len(partitions),'partition designs')
