"""Pinned/working18.4 source;loss classification before/after terminal float reporting.
Usage: python THIS baseline|working output_stem
"""
from pathlib import Path
import sys,re,subprocess,tempfile,importlib.util,json,hashlib,platform,math
from fractions import Fraction as F
here=Path(__file__).resolve().parent;root=here.parents[3];pin='f557464a4f1e367f64d515a7818c5aac65c79766';path='books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.04-simulating-financial-outcomes.md';mode,stem=sys.argv[1:3];raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root) if mode=='baseline' else (root/path).read_bytes();code=re.findall(r'^~~~python\n(.*?)^~~~',raw.decode(),re.M|re.S)[0];rows=[];cases=[];commands=[]
with tempfile.TemporaryDirectory() as tmp:
 t=Path(tmp);p=t/'financial_outcomes.py';p.write_text(code)
 for argv in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name]]:
  z=subprocess.run(argv,cwd=t,capture_output=True,text=True,timeout=60);commands.append(dict(argv=argv,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 spec=importlib.util.spec_from_file_location('source_outcome',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);Original=m.random.Random
 fixtures=[('flat tinyfee',.5,1e-16),('flat smallfee',.5,1e-15),('up adjacent feeabove20',.9,math.nextafter(20.,math.inf)),('up adjacent feebelow20',.9,math.nextafter(20.,0.)),('up exactfee20',.9,20.),('flat representablefee',.5,1e-12),('flat nofee',.5,0.),('down tinyfee',.1,1e-16),('up normalfee',.9,2.),('flat normalfee',.5,2.),('down normalfee',.1,2.)]
 for label,u,fee in fixtures:
  gross=80 if u<.25 else 100 if u<.75 else 120
  net=F(gross)-F(str(fee));expected_loss=net<100;rounded=float(net);ambiguous=(F(str(rounded))<100)!=expected_loss
  class Controlled:
   def __init__(self,seed):pass
   def random(self):return u
  m.random.Random=Controlled;values=None;summary=None;exc=None
  try:values=m.simulate(4,7,fee);summary=m.summarize(values,100)
  except Exception as e:exc=dict(type=type(e).__name__,message=str(e))
  finally:m.random.Random=Original
  ok=(exc is not None and exc['type']=='ValueError') if ambiguous else (exc is None and summary['loss_count']==(4 if expected_loss else 0))
  rows.append(dict(name=label+' classification or explicit range rejection',kind='source integration',passed=ok,ambiguous=ambiguous,expected_latent_loss_count=4 if expected_loss else 0,source_summary=summary,exception=exc))
  restored=m.random.Random is Original;rows.append(dict(name=label+' RNG restore',kind='observer restoration',passed=restored));assert restored
  cases.append(dict(label=label,controlled_uniform=u,input_fee=repr(fee),exact_net=str(net),rounded_net=rounded,latent_strict_loss=expected_loss,reported_strict_loss=rounded<100,classification_ambiguous=ambiguous,actual_values=values,summary=summary,exception=exc))
 # A deterministic terminal fee is a paired constant shift;threshold effects remain distinct from mean uncertainty.
 for fee,expected_mean,expected_loss in [(0,100,F(1,4)),(2,98,F(3,4)),(20,80,F(3,4))]:
  states=[F(80-fee),F(100-fee),F(120-fee)];weights=[F(1,4),F(1,2),F(1,4)];mean=sum((w*x for w,x in zip(weights,states)),F(0));loss=sum((w for w,x in zip(weights,states) if x<100),F(0));variance=sum((w*(x-mean)**2 for w,x in zip(weights,states)),F(0))
  for name,actual,want in [('mean',mean,F(expected_mean)),('strict loss',loss,expected_loss),('variance',variance,F(200))]:rows.append(dict(name='model fee'+str(fee)+' '+name,kind='supplemental exact distribution',actual=str(actual),expected=str(want),passed=actual==want))
 assert p.read_text()==code
result=dict(source_revision=pin,source_mode=mode,source_path=path,source_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),fence_sha256=hashlib.sha256(code.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,rows=rows,passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),cases=cases,limits='Fixedmodelcost100/strictless-thanclassification. Controlledsourcecalls,reportedvalues andlatentFractionexpectations distinct;notarbitrarythreshold/currency/measure/rare-event/platformapproval.')
(here/(stem+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(mode,result['passed'],'passed',result['failed'],'failed');raise SystemExit(bool(result['failed']))
