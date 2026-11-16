"""Pinned Section18.2 threshold mapping and conditional finite-grid references.
Usage: python THIS first|replay
"""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction as F
here=Path(__file__).resolve().parent;root=here.parents[3];pin='102b658e1580bdffd0c980c36616788d619ae89a';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.02-random-number-generators.md';stem=sys.argv[1];raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S);assert len(fences)==6;M=2**53;rows=[];cases=[];commands=[]
def record(name,ok,**data):rows.append(dict(name=name,passed=bool(ok),**data));assert ok,name
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);p=t/'random_generators.py';p.write_text(fences[-1])
 for argv in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(argv,cwd=t,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 spec=importlib.util.spec_from_file_location('generator_reference',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 original=m.uniform_draws
 probabilities=[0.,1.,.1,.5,.6,float.fromhex('0x0.0000000000001p-1022'),2.**-54,math.nextafter(2.**-53,0.),2.**-53,math.nextafter(2.**-53,math.inf),math.nextafter(1.,0.)]
 for probability in probabilities:
  P=F(str(probability));product=M*P;count=(product.numerator+product.denominator-1)//product.denominator;q=F(count,M);indices=sorted({k for k in (0,count-1,count,count+1,M-1) if 0<=k<M});values=[float(F(k,M)) for k in indices];seen=[]
  def controlled(n,seed):seen.append((n,seed));return list(values)
  m.uniform_draws=controlled
  try:events=m.bernoulli_draws(probability,len(values),7)
  finally:m.uniform_draws=original
  expected=[int(k*P.denominator<M*P.numerator) for k in indices]
  record(str(probability)+' actual threshold map',events==expected,actual=events,expected=expected,grid_indices=indices)
  record(str(probability)+' source callback contract',seen==[(len(values),7)] and m.uniform_draws is original,actual=seen)
  cell=(count==0 and P==0) or F(count-1)<product<=count
  record(str(probability)+' exact ceil cell',cell,count=count,scaled_threshold=str(product),kind='supplemental conditional-grid algebra')
  record(str(probability)+' grid probability error',0<=q-P<F(1,M),effective_probability=str(q),specified_display_probability=str(P),absolute_error=str(q-P),kind='supplemental conditional-grid algebra')
  cases.append(dict(input_probability=repr(probability),displayed_probability=str(P),binary_input_probability=str(F(probability)),grid_count=count,conditional_effective_probability=str(q),absolute_probability_error=str(q-P),indices=indices,uniform_values=values,source_events=events))
 # Source-native output support illustration,not generator quality or uniform-mass proof.
 native=m.uniform_draws(32,42);record('selected native draws on declared grid',all(0<=u<1 and (F(u)*M).denominator==1 for u in native),native_draw_hex=[u.hex() for u in native])
 record('subgrid positive threshold has one accepted cell',cases[6]['grid_count']==1,kind='supplemental resolution interpretation')
 record('next grid-adjacent higher displayed threshold has two cells',cases[9]['grid_count']==2,kind='supplemental resolution interpretation')
 assert p.read_text()==fences[-1]
result=dict(source_revision=pin,source_path=path,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=[hashlib.sha256(c.encode()).hexdigest() for c in fences],python=sys.version,platform=platform.platform(),commands=commands,rows=rows,passed=len(rows),failed=0,grid_size=M,cases=cases,limits='Controlledthresholdsourcecalls distinct fromsupplementaluniform-mass53-bitgridprobabilities. No enumerationofall2^53draws,no MTuniformity/independence/cryptographic/rare-event/model/platformcertification;normalCDFtailF165unresolved.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(len(rows),'predicates',len(cases),'threshold cases')
