"""Assessment multiplicity assumptions and external capstone report assembly."""
from pathlib import Path
from fractions import Fraction as F
import re,sys,subprocess,tempfile,importlib.util,json,math,hashlib,platform
from datetime import datetime,timezone
if not __debug__:raise RuntimeError('Assertions required')
here=Path(__file__).resolve().parent;root=here.parents[3];pin='41ab3fbc4d0207aa3c2fa39aca56ee6a5f5c939c';book='books/book-01-python-foundations-for-financial-mathematics';paths=[book+'/chapter-15/15.15-exercises-and-applied-problems.md',book+'/chapter-15/15.14-chapter-project-financial-statistical-analysis-toolkit.md'];rows=[];commands=[];sources={};models=[]
def ck(name,got,want,kind,approx=False):rows.append(dict(name=name,actual=str(got),expected=str(want),kind=kind,passed=math.isclose(float(got),float(want),rel_tol=5e-14,abs_tol=1e-15) if approx else got==want))
with tempfile.TemporaryDirectory() as tmp:
 mods=[]
 for path,name in zip(paths,['chapter15_applied_problems','financial_statistics_toolkit']):
  raw=subprocess.check_output(['git','show',pin+':'+path],cwd=root);fences=re.findall(r'^```python\n(.*?)^```',raw.decode(),re.M|re.S);p=Path(tmp)/(name+'.py');p.write_text(fences[0]);spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);mods.append(m);sources[name]=dict(path=path,source_sha256=hashlib.sha256(raw).hexdigest(),listing_sha256=hashlib.sha256(fences[0].encode()).hexdigest())
  z=subprocess.run([sys.executable,p.name],cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=[sys.executable,p.name],returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
  if name=='chapter15_applied_problems':assessment_raw=raw.decode()
  else:
   csv=re.findall(r'^```csv\n(.*?)^```',raw.decode(),re.M|re.S)[0];(Path(tmp)/'prices.csv').write_text(csv);(Path(tmp)/'csv_usage.py').write_text(fences[1])
 for args in [[sys.executable,'csv_usage.py'],[sys.executable,'-m','compileall','-q','.']]:
  z=subprocess.run(args,cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(argv=args,returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));assert z.returncode==0
 assessment,kit=mods;alpha=F(1,20);m=20;adjusted=assessment.bonferroni(.05,m);ck('source Bonferroni threshold',adjusted,alpha/m,'exact supplied family alpha/count',True)
 # Four hundred exactly equiprobable valid null p-values. Source supplies threshold only.
 for name,threshold,size in [('unadjusted',alpha,F(1,20)),('Bonferroni',F(str(adjusted)),F(1,400))]:
  rejects=0
  for k in range(1,401):
   p=F(k,400);decision=p<=threshold;expected=k<=(20 if name=='unadjusted' else 1)
   ck(name+' external p-grid decision'+str(k),decision,expected,'external decision using source adjusted threshold; no native p-value/test API');rejects+=decision
  actual=F(rejects,400);ck(name+' exact marginal size',actual,size,'specified discrete uniform null law, ties included')
  independent=1-(1-actual)**20;shared=actual
  ck(name+' IID familywise risk',independent,1-(1-size)**20,'independent20-test joint law, exact complement product')
  ck(name+' identical-p familywise risk',shared,size,'perfectly dependent20-test joint law, not IID')
  if name=='Bonferroni':ck('Bonferroni IID within supplied family alpha',independent<=alpha,True,'union-bound consequence for valid null p-values, no independence required for bound')
  models.append(dict(name=name,grid='k/400,k=1..400,uniform null',single_size=str(actual),iid_FWER=str(independent),identical_p_FWER=str(shared),scope='external finite probability law and decision policy; not calibrated market p-values or discovered strategy acceptance'))
 # Same rejection event can carry different posterior null probability under different priors.
 for prior,want in [(F(9,10),F(27,107)),(F(1,10),F(1,241))]:
  posterior=(prior*F(3,100))/(prior*F(3,100)+(1-prior)*F(4,5))
  ck('external posterior with null prior'+str(prior),posterior,want,'Bayes event calculation: null rejection .03, alternative power .8; p-value is not posterior null probability')
 ck('power from supplied beta',1-F(1,5),F(4,5),'answer19 definition, no source power API')
 dates,asset,bench=kit.load_prices_csv(Path(tmp)/'prices.csv');ar=kit.simple_returns(asset);br=kit.simple_returns(bench);A=[F(str(x)) for x in ar];B=[F(str(x)) for x in br];n=len(A);cov=(sum(x*y for x,y in zip(A,B))-sum(A)*sum(B)/n)/(n-1);native=kit.report(asset,bench)
 ck('native report omits covariance field','covariance' in native,False,'native interface observation, capstone permits caller report assembly')
 expanded=dict(native,covariance=kit.sample_covariance(ar,br));ck('external capstone native covariance',expanded['covariance'],cov,'native standalone covariance vs independent raw-product sum',True)
 ck('capstone report required metric names',set(expanded),{'observations','mean_return','volatility','cumulative_return','correlation','regression','normal_ci_approx','historical_tail','rolling_mean','covariance'},'supplemental report assembly, not an invented native field')
 ck('capstone four returns',expanded['observations'],4,'exact price fixture');ck('report SD agrees with assessment source',expanded['volatility'],assessment.sd(ar),'same shared return vector',True);ck('report mean agrees with assessment source',expanded['mean_return'],assessment.mean(ar),'same shared return vector',True);ck('report cumulative agrees with assessment source',expanded['cumulative_return'],assessment.cumulative(ar),'same shared return vector',True)
 ck('net1bp less4bp',assessment.mean([float(F(1,10000)-F(4,10000))]),F(-3,10000),'native mean of disclosed external net-cost transformation, not measured execution cost',True)
 ck('all48 answer headings retained',[int(x) for x in re.findall(r'^### Exercise (\d+)',assessment_raw,re.M)],list(range(1,49)),'static prompt-record inventory, not48 newly executed tests')
 checklist=assessment_raw.split('**Acceptance checklist:**')[1].split('## Part G')[0];ck('nine capstone checklist records',len(re.findall(r'^- \[[ x]\]',checklist,re.M)),9,'static inventory, not nine accepted gates')
 rubric=assessment_raw.split('## Assessment rubric')[1].split('## Troubleshooting')[0];scores=[int(x) for x in re.findall(r'^\| [^|]+ \| (\d+) \|',rubric,re.M)];ck('rubric point sum',sum(scores),100,'static rubric arithmetic, no student grade/certification')
 for name,prior_dir in [('chapter15_applied_problems','chapter-15-applied-answers-review'),('financial_statistics_toolkit','chapter-15-toolkit-review')]:
  prior=json.loads((here.parent/prior_dir/'results.json').read_text())
  for field in ['source_sha256','listing_sha256']:ck(name+' retained '+field,sources[name][field],prior[field],'prior F141/F140 failure/corrected scopes preserved')
r=dict(pin=pin,sources=sources,executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),rows=rows,commands=commands,models=models,capstone_external_report=expanded,capstone_metadata=dict(dates=dates,csv_sha256=hashlib.sha256(csv.encode()).hexdigest(),currency='fictional USD',basis='raw synthetic prices, no distributions',alignment='ordered CSV rows only; actual sessions/availability not verified'),passed=sum(x['passed'] for x in rows),failed=sum(not x['passed'] for x in rows),scope='Source threshold/helper/report execution separate from external probability laws/report assembly and conceptual research-data acceptance; no independent/platform/canonical approval')
(here/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['passed'],r['failed']);assert r['failed']==0
