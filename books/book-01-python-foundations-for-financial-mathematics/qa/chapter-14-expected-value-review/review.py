"""Section 14.9 exact expected value lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.09-expected-value.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1409-') as tmp:
        Path(tmp,'expected_value.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['expected_value.py']),('isolated import',['-c','import expected_value']),('exact compilation',['-m','compileall','-q','expected_value.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['expected_value.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('expected_value');exec(compile(code,str(source),'exec'),m.__dict__)
    d={-20:.25,5:.5,30:.25}
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 signed mean',lambda:m.expected(d),5),
        ('E2 certain payoff',lambda:m.expected({7:1}),7),
        ('E3 default indicator',lambda:m.expected({0:.98,1:.02}),F('.02')),
        ('E4 expected credit loss',lambda:m.expected_loss(10000,.4,.02),80),
        ('E5 zero default',lambda:m.expected_loss(10000,.4,0),0),
        ('E6 full loss',lambda:m.expected_loss(500,1,1),500),
        ('E7 negative mean',lambda:m.expected({-10:.8,10:.2}),-6),
        ('E8 transformed mean',lambda:m.transformed_expected(d,lambda x:2*x+1),11),
        ('E9 shifted mean',lambda:m.transformed_expected(d,lambda x:x-3),2),
        ('E10 second moment',lambda:m.transformed_expected(d,lambda x:x*x),F(675,2)),
        ('E12/E13 discounted expectation',lambda:m.discounted_expected({110:1},.10,1),100),
        ('E14 claim average',lambda:m.expected({0:.95,1000:.05}),50),
        ('E16 weighted scenarios',lambda:m.scenario_expected([.2,.5,.3],[-100,20,80]),14),
        ('E17 expected return',lambda:m.expected({-.1:.5,.2:.5}),F('.05')),
        ('E20 indicator',lambda:m.expected({0:.7,1:.3}),F('.3')),
        ('E21 conditional model',lambda:m.expected({0:.6,100:.4}),40),
        ('E22 square average',lambda:m.transformed_expected({0:.5,2:.5},lambda x:x*x),2),
        ('project PD 1 percent',lambda:m.expected_loss(10000,.4,.01),40),
        ('project PD 5 percent',lambda:m.expected_loss(10000,.4,.05),200),
        ('F118 cancellation preserves integer difference',lambda:m.expected({-10**18:.5,10**18+2:.5}),1),
        ('F118 transformed cancellation preserves difference',lambda:m.transformed_expected({0:.5,1:.5},lambda x:-10**18 if x==0 else 10**18+2),1),
        ('F118 scenario cancellation preserves difference',lambda:m.scenario_expected([.5,.5],[-10**18,10**18+2]),1),
        ('F118 discount rescues finite present value',lambda:m.discounted_expected({1e308:1},1e155,2),F('.01')),
        ('F118 negative rate and zero periods',lambda:m.discounted_expected({100:1},-.9,0),100),
    ]:num(label,fn,want)
    near=[.5,.5000000000005]
    ck('F118 normalize PMF mass',m.expected({0:near[0],1:near[1]})==float(F(str(near[1]))/(F('.5')+F(str(near[1])))))
    ck('F118 normalize scenario mass',m.scenario_expected(near,[5,5])==5)
    ck('E11 nonlinear expectation differs from squared mean',m.transformed_expected(d,lambda x:x*x)!=m.expected(d)**2)
    ck('E18 linearly related outcomes require no independence',m.transformed_expected(d,lambda x:x+2*x)==m.expected(d)+m.transformed_expected(d,lambda x:2*x))
    for label,fn in [
        ('E24 invalid probability mass',lambda:m.expected({0:.4,1:.4})),
        ('invalid PD',lambda:m.expected_loss(100,.4,1.1)),
        ('invalid LGD',lambda:m.expected_loss(100,-.1,.02)),
        ('nonfinite scenario payoff',lambda:m.scenario_expected([1],[math.inf])),
        ('scenario length mismatch',lambda:m.scenario_expected([1],[4,5])),
        ('F118 enormous invalid weight rejected',lambda:m.expected({0:10**400})),
        ('F118 nonrepresentable discounted output',lambda:m.discounted_expected({1e308:1},-.9,2)),
        ('F118 nonzero weighted expectation must not silently underflow',lambda:m.expected({0:.99,5e-324:.01})),
    ]:reject(label,fn)
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(fixture='hypothetical investment and credit loss, USD',credit_horizon_years=1,
                                 investment_horizon='one modeled period',credit_losses={str(pd):m.expected_loss(10000,.4,pd) for pd in (.01,.02,.05)}))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
