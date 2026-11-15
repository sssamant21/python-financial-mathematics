"""Exact scaffold source;offline local build/editable and clean wheel consumer."""
from pathlib import Path
import subprocess,sys,re,tempfile,json,hashlib,platform,os,zipfile
OUT=Path(__file__).resolve().parent;BOOK=OUT.parents[1];ROOT=BOOK.parents[1];REV=sys.argv[1] if len(sys.argv)>1 else '0155afc15de96737b183aaf3eed45cf2280f93ba';base='books/book-01-python-foundations-for-financial-mathematics/chapter-21/';paths=[base+'21.10-portfolio-module.md',base+'21.09-return-and-performance-module.md',base+'21.08-bond-module.md',base+'21.07-loan-module.md',base+'21.06-cash-flow-module.md',base+'21.05-time-value-of-money-module.md',base+'21.03-project-structure.md'];texts=[subprocess.check_output(['git','show',REV+':'+p],cwd=ROOT,text=True) for p in paths];port,ret,bond,loan,cash,tvm,old=[re.findall(r'```python\n(.*?)\n```',x,re.S) for x in texts];tm=re.findall(r'```toml\n(.*?)\n```',texts[6],re.S);md=re.findall(r'```markdown\n(.*?)\n```',texts[6],re.S);assert len(port)==len(ret)==len(bond)==len(loan)==len(cash)==len(tvm)==len(old)==4 and len(tm)==len(md)==1
files={'src/financial_toolkit/portfolio.py':port[0],'examples/portfolio.py':port[2],'tests/test_portfolio.py':port[3],'src/financial_toolkit/returns.py':ret[0],'examples/returns.py':ret[2],'tests/test_returns.py':ret[3],'src/financial_toolkit/bonds.py':bond[0],'examples/bonds.py':bond[2],'tests/test_bonds.py':bond[3],'src/financial_toolkit/loans.py':loan[0],'examples/loans.py':loan[2],'tests/test_loans.py':loan[3],'src/financial_toolkit/cashflows.py':cash[0],'src/financial_toolkit/time_value.py':tvm[0],'src/financial_toolkit/__init__.py':port[1],'examples/cashflows.py':cash[2],'tests/test_cashflows.py':cash[3],'tests/test_tvm_multi.py':tvm[3],'tests/test_time_value.py':old[3],'pyproject.toml':tm[0],'README.md':md[0]};prior=json.loads((BOOK/'qa/chapter-21-portfolio-resume/results.json').read_text());assert all(hashlib.sha256(files[n].encode()).hexdigest()==sha for n,sha in prior['staged_fence_sha256'].items());commands=[]

def run(label,argv,cwd,env):
 z=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True);commands.append(dict(label=label,argv=list(map(str,argv)),returncode=z.returncode,stdout=z.stdout,stderr=z.stderr));return z
with tempfile.TemporaryDirectory(prefix='book1-scaffold-') as td:
 temp=Path(td);project=temp/'project';project.mkdir();outside=temp/'outside';outside.mkdir();build=temp/'build-env';consumer=temp/'consumer-env';env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONNOUSERSITE']='1';env['PIP_NO_INDEX']='1';env['PIP_DISABLE_PIP_VERSION_CHECK']='1'
 for name,s in files.items():p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
 run('build venv;preprovisioned local tooling',[sys.executable,'-m','venv','--system-site-packages',str(build)],temp,env);bp=str(build/'bin/python')
 run('build-tool versions',[bp,'-c','import sys,importlib.metadata as m;print(sys.version);print({n:m.version(n) for n in ("pip","setuptools","wheel")})'],temp,env)
 run('offline editable install',[bp,'-m','pip','install','--no-index','--no-build-isolation','--no-deps','-e','.'],project,env)
 run('editable example',[bp,'examples/portfolio.py'],project,env);run('editable reference suite',[bp,'-m','unittest','discover','-s','tests','-v'],project,env)
 wheels=temp/'wheels';wheels.mkdir();run('offline wheel build',[bp,'-m','pip','wheel','--no-index','--no-build-isolation','--no-deps','--wheel-dir',str(wheels),'.'],project,env)
 found=list(wheels.glob('*.whl'));assert len(found)==1;wheel=found[0]
 with zipfile.ZipFile(wheel) as z:artifact=dict(filename=wheel.name,sha256=hashlib.sha256(wheel.read_bytes()).hexdigest(),size=wheel.stat().st_size,members=[dict(name=i.filename,size=i.file_size) for i in z.infolist()])
 (outside/'test_portfolio.py').write_text(files['tests/test_portfolio.py']);(outside/'test_returns.py').write_text(files['tests/test_returns.py']);(outside/'test_bonds.py').write_text(files['tests/test_bonds.py']);(outside/'test_loans.py').write_text(files['tests/test_loans.py']);(outside/'test_time_value.py').write_text(files['tests/test_time_value.py']);(outside/'test_tvm_multi.py').write_text(files['tests/test_tvm_multi.py']);(outside/'test_cashflows.py').write_text(files['tests/test_cashflows.py']);(outside/'one_period.py').write_text(files['examples/portfolio.py'])
 run('clean consumer venv',[sys.executable,'-m','venv',str(consumer)],temp,env);cp=str(consumer/'bin/python');run('offline wheel install clean consumer',[cp,'-m','pip','install','--no-index','--no-deps',str(wheel)],outside,env)
 project.rename(temp/'source-hidden')
 run('outside-source wheel reference suite',[cp,'-I','-m','unittest','discover','-s',str(outside),'-v'],outside,env);run('outside-source wheel example',[cp,'-I','one_period.py'],outside,env)
 probe='''import financial_toolkit as m,sys,json,math
from fractions import Fraction
from decimal import Decimal
from pathlib import Path
assert Path(m.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
p=m.present_value_one_period
rows=[]
for c,r in [(110.,.1),(95.,-.05),(110.,0.),(-110.,.1),(100.,.05),(100.,.1),(0.,.1)]:
 expected=float(Fraction(c)/(1+Fraction(r)));actual=p(c,r);rows.append(dict(payment=c,rate=r,actual=actual,expected=expected,passed=math.isclose(actual,expected,rel_tol=5e-14,abs_tol=1e-10)))
for c,r in [(100,.1),(100.,True),(math.nan,.1),(100.,-1.),(1e308,-.5)]:
 try:p(c,r);passed=False
 except ValueError:passed=True
 rows.append(dict(input=repr((c,r)),passed=passed))
pv,fv=m.present_value,m.future_value
for name,fn in [('pv',pv),('fv',fv)]:
 for amount,rate,n in [(100.,.1,2),(121.,.1,2),(100.,-.05,2),(50.,.2,0),(50.,0.,10000),(0.,1e308,10000),(-100.,.05,5),(100.,.001,100)]:
  expected=0. if amount==0 else float(Fraction(amount)*(1+Fraction(rate))**n if name=='fv' else Fraction(amount)/(1+Fraction(rate))**n)
  working=0. if amount==0 else float(Fraction(amount)*Fraction(1.+rate)**n if name=='fv' else Fraction(amount)/Fraction(1.+rate)**n)
  actual=fn(amount,rate,n);rows.append(dict(function=name,amount=amount,rate=rate,periods=n,actual=actual,model_reference=expected,working_base_reference=working,relative_tolerance=5e-13,absolute_tolerance=1e-10,passed=math.isclose(actual,expected,rel_tol=5e-13,abs_tol=1e-10) and math.isclose(actual,working,rel_tol=5e-13,abs_tol=1e-10)))
 for n in [-1,10001,True,1.0]:
  try:fn(100.,.1,n);passed=False
  except ValueError:passed=True
  rows.append(dict(function=name,invalid_periods=repr(n),passed=passed))
for fn,args in [(fv,(1e308,1.,1)),(pv,(1e308,-.5,1))]:
 try:fn(*args);passed=False
 except ValueError:passed=True
 rows.append(dict(case='declared nonfinite intermediate',passed=passed))
assert m.__all__==['future_value','present_value','present_value_one_period','net_present_value','level_payment','fixed_coupon_bond_price','simple_price_return','linked_return','portfolio_return']
limit=dict(name='documented rounded-base loss',actual=fv(1.,2**-54,10000),independent_model=float((1+Fraction(2**-54))**10000),status='Documented rounding limitation;notfailed acceptance predicate.')
npv=m.net_present_value
for flows,rate in [([-100.,110.],.1),([-100.,60.,60.],.1),((25.,),.1),([-100.,0.,121.],.1),([0.,95.],-.05),([-100.,60.,60.],0.),([10.,-2.,3.],-.25),([-200.,120.,120.],.1),([0.]*1001,0.)]:
 expected=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows) if c),Fraction()));actual=npv(flows,rate);rows.append(dict(function='npv',flow_count=len(flows),rate=rate,actual=actual,model_reference=expected,relative_tolerance=5e-13,absolute_tolerance=1e-10,passed=math.isclose(actual,expected,rel_tol=5e-13,abs_tol=1e-10)))
for flows,rate in [(None,.1),([],.1),((),.1),((x for x in [1.]),.1),([1],.1),([True],.1),([math.nan],.1),([math.inf],.1),([0.]*1002,.1),([1.],True),([1.],-1.),([1.],math.inf),([1e308,1e308],0.)]:
 try:npv(flows,rate);passed=False
 except ValueError:passed=True
 rows.append(dict(function='npv invalid contract',passed=passed))
flows=[-100.,60.,60.];copy=flows.copy();npv(flows,.1);rows.append(dict(case='npv caller unchanged',passed=flows==copy))
rows.append(dict(case='npv scaling selected',passed=math.isclose(npv([-200.,120.,120.],.1),2*npv([-100.,60.,60.],.1),rel_tol=5e-13,abs_tol=1e-10)))
npvlimits=[]
for flows,rate,name in [([-1e308,1e308],-.5,'documented discounted-leg overflow before cancellation'),([1e308,1e308,-1e308],0.,'documented fsum intermediate overflow before cancellation')]:
 try:a=npv(flows,rate)
 except Exception as e:a=type(e).__name__
 expected=float(sum((Fraction(c)/(1+Fraction(rate))**i for i,c in enumerate(flows)),Fraction()));npvlimits.append(dict(name=name,actual=repr(a),independent_final=expected,status='Documented intermediate rejection;not failed acceptance predicate or new defect.'))
fn=m.level_payment
def add(label,ok,**data):rows.append(dict(case=label,passed=bool(ok),**data))
# The oracle discounts each payment as an exact rational. It does not use
# the implementation's log1p/expm1 denominator or its annuity quotient.
for principal in [1.,1000.,1e-200,1e200]:
 for rate,n in [(0.,12),(.1,1),(.1,2),(1e-12,12),(.01,360),(1.,1200),(1e-308,12),(math.ulp(0.),12)]:
  L,R=map(Fraction,(principal,rate));v=Fraction(1,1)/(1+R);power=v;total=Fraction(0)
  for _ in range(n):total+=power;power*=v
  exact=L/total;want=float(exact);got=fn(principal,rate,n)
  add(f'annuity sum L={principal} r={rate} n={n}',math.isclose(got,want,rel_tol=5e-14,abs_tol=0.),actual=got,expected=want)
for label,args in [('integer principal',(1000,.1,2)),('bool principal',(True,.1,2)),('decimal principal',(Decimal('1000'),.1,2)),('zero principal',(0.,.1,2)),('negative principal',(-1.,.1,2)),('nan principal',(math.nan,.1,2)),('inf principal',(math.inf,.1,2)),('integer rate',(1000.,0,2)),('bool rate',(1000.,True,2)),('decimal rate',(1000.,Decimal('.1'),2)),('negative rate',(1000.,-.01,2)),('over cap rate',(1000.,1.01,2)),('nan rate',(1000.,math.nan,2)),('inf rate',(1000.,math.inf,2)),('bool periods',(1000.,.1,True)),('float periods',(1000.,.1,2.)),('zero periods',(1000.,.1,0)),('over cap periods',(1000.,.1,1201)),('result overflow',(1e308,1.,1)),('zero rate underflow',(math.ulp(0.),0.,1200)),('positive rate underflow',(math.ulp(0.),1e-12,1200))]:
 try:got=fn(*args);kind='returned'
 except Exception as e:kind=type(e).__name__
 add(label,kind=='ValueError',actual=kind,expected='ValueError')
for r,n in [(0.,12),(.01,360),(.1,2),(1.,1200)]:
 a=fn(1000.,r,n);add(f'scale r={r} n={n}',math.isclose(fn(2000.,r,n),2*a,rel_tol=5e-14,abs_tol=0.))
for n in [1,2,360,1200]:add(f'rate monotonic n={n}',fn(1000.,0.,n)<fn(1000.,.01,n)<fn(1000.,1.,n))
for r in [0.,.01,.1]:add(f'term monotonic r={r}',fn(1000.,r,12)>fn(1000.,r,24)>fn(1000.,r,48))

for n in [2,1000]:
 payment=fn(1000.,.01,n);actual=npv([1000.]+[-payment]*n,.01)
 add(f'loan NPV integration n={n}',math.isclose(actual,0.,rel_tol=0.,abs_tol=1e-8),actual=actual,absolute_tolerance=1e-8)
try:npv([1000.]+[-fn(1000.,.01,1100)]*1100,.01);kind='returned'
except Exception as e:kind=type(e).__name__
add('1100-period loan exceeds integration cap without truncation',kind=='ValueError',actual=kind)

bond=m.fixed_coupon_bond_price
for face,coupon,yield_rate,n in [(100.,.05,.05,2),(100.,0.,.05,2),(100.,.05,.1,1),(100.,.05,0.,2),(95.,0.,-.05,1),(100.,.03,.05,12),(100.,.05,.03,12),(100.,0.,1e308,2),(100.,0.,0.,1000),(100.,.01,.01,1000),(1e-200,.05,.05,10),(1e200,.05,.05,10),(100.,1.,1.,1),(100.,0.,-.5,2)]:
 F,C,Y=map(Fraction,(face,coupon,yield_rate));v=1/(1+Y);ann=n if Y==0 else v*(1-v**n)/(1-v);want=float(F*C*ann+F*v**n);got=bond(face,coupon,yield_rate,n)
 add(f'bond rational complete sum face={face} c={coupon} y={yield_rate} n={n}',math.isclose(got,want,rel_tol=5e-13,abs_tol=0.),actual=got,expected=want,relative_tolerance=5e-13,absolute_tolerance=0.)
for label,args in [('integer face',(100,.05,.05,2)),('bool face',(True,.05,.05,2)),('zero face',(0.,.05,.05,2)),('negative face',(-1.,.05,.05,2)),('nan face',(math.nan,.05,.05,2)),('bool coupon',(100.,True,.05,2)),('negative coupon',(100.,-.01,.05,2)),('coupon over cap',(100.,1.01,.05,2)),('integer yield',(100.,.05,0,2)),('yield boundary',(100.,.05,-1.,2)),('inf yield',(100.,.05,math.inf,2)),('bool periods',(100.,.05,.05,True)),('periods over cap',(100.,.05,.05,1001)),('periods below cap',(100.,.05,.05,0)),('redemption overflow',(1e308,1.,.05,1))]:
 try:bond(*args);kind='returned'
 except Exception as e:kind=type(e).__name__
 add('bond '+label,kind=='ValueError',actual=kind,expected='ValueError')
a=bond(100.,.05,.04,12);add('bond scaling',math.isclose(bond(200.,.05,.04,12),2*a,rel_tol=5e-13,abs_tol=0.));add('bond yield monotonic',bond(100.,.05,.03,12)>a>bond(100.,.05,.07,12));add('bond par order',bond(100.,.05,.03,12)>100.>bond(100.,.05,.07,12));add('bond shared integration (not independent oracle)',bond(100.,.05,.05,2)==npv([0.,5.,105.],.05))

price,link=m.simple_price_return,m.linked_return
for start,end in [(100.,110.),(100.,90.),(100.,100.),(100.,0.),(110.,99.),(1e-200,1.1e-200),(1e200,1.1e200),(50.,100.)]:
 want=float(Fraction(end)/Fraction(start)-1);got=price(start,end);add(f'price return {start} to {end}',math.isclose(got,want,rel_tol=5e-13,abs_tol=1e-12),actual=got,expected=want)
for values in [[.1,-.1],[.05,0.],[-1.,.5],[0.]*10000,(.05,),[.2,.3],[-.5,1.],[-1.,1e308],[.001]*100,[0.]*3]:
 product=Fraction(1)
 for value in values:product*=1+Fraction(value)
 want=float(product-1);got=link(values);add(f'linked return n={len(values)} first={values[0]}',math.isclose(got,want,rel_tol=5e-13,abs_tol=1e-12),actual=got,expected=want)
for args in [(0.,1.),(-1.,1.),(1.,-1.),(100,110.),(100.,True),(math.nan,1.),(1.,math.inf),(Decimal('100'),110.),(True,1.),(1e-308,1e308)]:
 try:price(*args);kind='returned'
 except Exception as e:kind=type(e).__name__
 add('invalid price '+repr(args),kind=='ValueError',actual=kind)
for values in [[],(),None,(x for x in [0.]),[1],[True],[-1.01],[math.nan],[0.]*10001,[1e308,1e308]]:
 try:link(values);kind='returned'
 except Exception as e:kind=type(e).__name__
 add('invalid linked contract '+repr(values)[:50],kind=='ValueError',actual=kind)
values=[.1,-.1];copy=values.copy();link(values);add('return input ownership',values==copy);add('price scale',math.isclose(price(200.,220.),price(100.,110.),rel_tol=0.,abs_tol=1e-12));add('zero period factor',math.isclose(link([.1,0.,-.1]),link([.1,-.1]),rel_tol=0.,abs_tol=1e-12));add('shared endpoint integration (not independent oracle)',math.isclose(link([price(100.,110.),price(110.,99.)]),price(100.,99.),rel_tol=0.,abs_tol=1e-12))
try:a=link([1e308,1e308,-1.])
except Exception as e:a=type(e).__name__
returnlimits=[dict(name='documented tiny linked return rounding',actual=link([2**-54]),independent_model=2**-54,status='Documented rounded gross loss, not failed acceptance or new defect.'),dict(name='documented overflow before later total loss',actual=repr(a),independent_final=-1.,status='Declared nonfinite intermediate rejection, not repaired/reclassified as new defect.'),dict(name='documented positive gross underflow',actual=link([-1.+2**-52]*100),exact_gross_positive=(Fraction(2)**-52)**100>0,status='Finite return -1 cannot distinguish exact tiny positive wealth; documented observation only.')]

portfolio=m.portfolio_return
for weights,returns in [([.6,.4],[.1,-.05]),([1.],[.05]),([1.,0.],[.1,-1.]),([.5,.5],[-1.,-1.]),([.25,.75],[.1,.1]),([.5,.5],[1e308,1e308]),([.2,.3,.5],[.1,.2,-.1]),([1.]+[0.]*9999,[.1]+[0.]*9999),([.5,.5000000000005],[1.,1.]),([.5,.4999999999995],[-1.,-1.]),([.5,.5],[math.ulp(0.),0.])]:
 want=float(sum((Fraction(w)*Fraction(v) for w,v in zip(weights,returns)),Fraction()));got=portfolio(weights,returns);add(f'portfolio rational n={len(weights)}',math.isclose(got,want,rel_tol=5e-13,abs_tol=1e-12),actual=got,expected=want)
# Independent exact sum rounded once models the declared fsum acceptance gate.
for second in [.5+1e-12,math.nextafter(.5+1e-12,0.),math.nextafter(.5+1e-12,1.),.5-1e-12,math.nextafter(.5-1e-12,0.),math.nextafter(.5-1e-12,1.)]:
 weights=[.5,second];rounded_total=float(sum(map(Fraction,weights),Fraction()));eligible=abs(Fraction(rounded_total)-1)<=Fraction(1e-12)
 try:got=portfolio(weights,[1.,1.]);kind='returned'
 except Exception as e:got=None;kind=type(e).__name__
 add(f'portfolio weight gate second={second}',(kind=='returned' and got==rounded_total) if eligible else kind=='ValueError',actual=repr(got),expected_eligible=eligible,independent_rounded_sum=rounded_total)
for weights,returns in [(None,[0.]),((x for x in [1.]),[0.]),([1.],None),([],[]),([1.],[.1,.2]),([1],[.1]),([True],[.1]),([-0.1,1.],[0.,0.]),([1.01],[0.]),([.4,.4],[0.,0.]),([math.nan],[0.]),([1.],[True]),([1.],[0]),([1.],[-1.01]),([1.],[math.inf]),([1.,0.],[.1,math.nan]),([0.]*10001,[0.]*10001),([.5,.5000000000005],[sys.float_info.max,sys.float_info.max])]:
 try:portfolio(weights,returns);kind='returned'
 except Exception as e:kind=type(e).__name__
 add('portfolio invalid contract '+repr(weights)[:40],kind=='ValueError',actual=kind)
weights=[.6,.4];values=[.1,-.05];wc=weights.copy();vc=values.copy();a=portfolio(weights,values);add('portfolio input ownership',weights==wc and values==vc);add('paired asset permutation',portfolio(weights[::-1],values[::-1])==a);add('one-sided return permutation changes exposure',not math.isclose(portfolio(weights,values[::-1]),a,rel_tol=0.,abs_tol=1e-12));add('shared price-return integration (not independent oracle)',math.isclose(portfolio([.6,.4],[price(100.,110.),price(100.,95.)]),.04,rel_tol=0.,abs_tol=1e-12))
portfoliolimits=[dict(name='accepted sum drift is not normalization',actual=portfolio([.5,.5000000000005],[1.,1.]),asset_max=1.,status='Declared approximate-sum policy allows slight convex-hull deviation;not new defect.'),dict(name='positive product underflow',actual=portfolio([.5,.5],[math.ulp(0.),0.]),exact_positive=Fraction(math.ulp(0.))/2>0,status='Declared product rounding/underflow;not new defect or failed predicate.')]

assert all(x['passed'] for x in rows)
print(json.dumps(dict(documented_range_observations=[limit]+npvlimits+returnlimits+portfoliolimits,module=m.__file__,prefix=sys.prefix,source_path_injection=False,exports=m.__all__,predicates=rows)))'''
 z=run('wheel import provenance and updated portfolio contract predicates',[cp,'-I','-c',probe],outside,env);wheel_checks=json.loads(z.stdout) if z.returncode==0 else None
 d=dict(source_revision=REV,python=sys.version,platform=platform.platform(),staged_fence_sha256={n:hashlib.sha256(x.encode()).hexdigest() for n,x in files.items()},reused_source_commands=3,reused_source_revision=prior['source_revision'],commands=commands,artifact=artifact,wheel_checks=wheel_checks,existing_unique_methods=84,new_method_invocations=168,reused_method_invocations=84,new_historical_unique_methods=0,limits='Offline build/editable tooling venv exposes preprovisioned system-site packages;consumer venv is clean,isolated -I outside hidden source. Uses declared local compatible backend with no-build-isolation/no-index/no-deps,not default network-isolated resolution. Wheel hash/list retained;generated binary and temporary environments are not committed. Not reproducible-byte guarantee,all-range correctness,other platforms,model/security/release/independent approval.')
(OUT/'package-results.json').write_text(json.dumps(d,indent=2)+'\n');print(len(commands),'commands',sum(x['returncode']!=0 for x in commands),'failed;editable/wheel suites168method invocations;wheel contract predicates retained');assert all(x['returncode']==0 for x in commands) and wheel_checks
