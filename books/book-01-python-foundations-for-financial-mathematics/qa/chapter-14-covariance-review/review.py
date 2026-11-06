"""Section 14.11 exact covariance lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.11-covariance-and-correlation.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1411-') as tmp:
        Path(tmp,'covariance_and_correlation.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['covariance_and_correlation.py']),('isolated import',['-c','import covariance_and_correlation']),('exact compilation',['-m','compileall','-q','covariance_and_correlation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['covariance_and_correlation.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from itertools import combinations
    x=[1,2,3]; y=[2,4,6]
    prod=sum((x[i]-x[j])*(y[i]-y[j]) for i,j in combinations(range(3),2))
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 population covariance via pairwise differences',lambda:m.population_covariance(x,y),F(prod,9)),
        ('E2 sample covariance',lambda:m.sample_covariance(x,y),F(prod,6)),
        ('E3 positive correlation',lambda:m.correlation(x,y),1),
        ('E4 negative correlation',lambda:m.correlation(x,[-v for v in y]),-1),
        ('E5 self covariance',lambda:m.population_covariance(x,x),F(2,3)),
        ('F120 single-pass variance',lambda:m.population_variance(iter(x)),F(2,3)),
        ('E6 symmetry',lambda:m.population_covariance(y,x),F(4,3)),
        ('E7/E8 zero covariance with nonlinear dependence',lambda:m.population_covariance([-1,0,1],[1,0,1]),0),
        ('E12 uncorrelated portfolio',lambda:m.portfolio_variance([.5,.5],[.04,.09],0),F('.0325')),
        ('E13 correlated portfolio',lambda:m.portfolio_variance([.6,.4],[.04,.09],.012),F('.03456')),
        ('E14 portfolio volatility',lambda:math.sqrt(m.portfolio_variance([.6,.4],[.04,.09],.012)),math.sqrt(.03456)),
        ('E19 opposite scale',lambda:m.sample_covariance([3*v for v in x],[-2*v for v in y]),-12),
        ('E20 shift invariance',lambda:m.sample_covariance([v+10 for v in x],[v-4 for v in y]),2),
        ('F120 small integer-offset covariance',lambda:m.population_covariance([10**18,10**18+1],x[:2]),F(1,4)),
        ('F120 correlation when variances are too large for float',lambda:m.correlation([-1e200,1e200],[1e200,-1e200]),-1),
        ('F120 correlation when variance product underflows',lambda:m.correlation([-1e-100,1e-100],[-1e-100,1e-100]),1),
        ('F120 finite portfolio with oversized weight square',lambda:m.portfolio_variance([1e200,0],[1e-300,0],0),1e100),
    ]:num(label,fn,want)
    for label,fn in [
        ('E18 impossible covariance',lambda:m.portfolio_variance([.6,.4],[.04,.09],.08)),
        ('constant correlation undefined',lambda:m.correlation([2,2],x[:2])),
        ('unequal paired lengths',lambda:m.sample_covariance(x,y[:2])),
        ('F120 infeasible zero-variance covariance',lambda:m.portfolio_variance([.5,.5],[0,0],1e-13)),
        ('F120 infeasible despite oversized variance product',lambda:m.portfolio_variance([.5,.5],[1e200,1e200],2e200)),
        ('F120 unreportable variance',lambda:m.portfolio_variance([1e308,0],[1e308,0],0)),
    ]:reject(label,fn)
    stress={}
    for rho in map(F,['-.5','0','.2','.8']):
        cov=rho*F('.06')
        want=F('.0288')*(1+rho)
        num(f'project variance at rho={rho}',lambda:m.portfolio_variance([.6,.4],[.04,.09],float(cov)),want)
        stress[str(rho)]=float(want)
    ck('project positive-weight stress monotone',list(stress.values())==sorted(stress.values()))
    ck('test-only listing emits no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(portfolio_variance_by_correlation=stress,paired_rows=list(zip(x,y)),units='common-period decimal return; synthetic pairs for estimator demo'))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
