"""Section 15.5 exact covariance lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.05-covariance.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1505-') as tmp:
        Path(tmp,'covariance.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['covariance.py']),('isolated import',['-c','import covariance']),('exact compilation',['-m','compileall','-q','covariance.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['covariance.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations,product
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def oracle(a,b,ddof=1):
        x=list(map(lambda v:F(str(v)),a));y=list(map(lambda v:F(str(v)),b));n=len(x)
        return sum((x[i]-x[j])*(y[i]-y[j]) for i,j in combinations(range(n),2))/(n*(n-ddof))
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    a=[.01,.02,.03];b=[.02,.04,.06]
    for label,fn,want in [
        ('E5 sample covariance',lambda:m.covariance(a,b),F(1,5000)),
        ('E6 population covariance',lambda:m.covariance(a,b,0),F(1,7500)),
        ('E7 variance A',lambda:m.variance(a),F(1,10000)),
        ('E8 variance B',lambda:m.variance(b),F(1,2500)),
        ('E9 correlation',lambda:m.correlation(a,b),1),
        ('E10 reflected covariance',lambda:m.covariance(a,[-v for v in b]),F(-1,5000)),
        ('E11 symmetry',lambda:m.covariance(b,a),F(1,5000)),
        ('E12 shifted covariance',lambda:m.covariance([v+.05 for v in a],b),F(1,5000)),
        ('E13 scaled covariance',lambda:m.covariance(a,[3*v for v in b]),F(3,5000)),
        ('E14 constant covariance',lambda:m.covariance([.02]*3,b),0),
        ('E16 equal-weight variance',lambda:m.two_asset_variance(a,b,.5),F(9,40000)),
        ('E17 portfolio SD',lambda:math.sqrt(m.two_asset_variance(a,b,.5)),F(3,200)),
        ('E23 singleton population',lambda:m.covariance([.01],[.02],0),0),
        ('E24 percent-unit covariance',lambda:m.covariance([1,2,3],[2,4,6]),2),
        ('F131 integer-offset covariance',lambda:m.covariance([10**18,10**18+1,10**18+2],[0,1,2]),1),
        ('F131 integer-offset correlation',lambda:m.correlation([10**18,10**18+1,10**18+2],[0,1,2]),1),
        ('F131 small-variance correlation',lambda:m.correlation([0,1e-100,2e-100],[0,2e-100,4e-100]),1),
        ('F131 large-variance correlation',lambda:m.correlation([0,1e100,2e100],[0,2e100,4e100]),1),
        ('F131 balanced-scale covariance',lambda:m.covariance([-1e200,0,1e200],[-1e-200,0,1e-200]),1),
        ('F131 balanced-scale correlation',lambda:m.correlation([-1e200,0,1e200],[-1e-200,0,1e-200]),1),
        ('F131 large common-offset constant',lambda:m.covariance([1e308]*3,[1,2,3]),0),
        ('F131 offset portfolio cancellation',lambda:m.two_asset_variance([1,2,3],[1,2,3],1e200),1),
    ]:num(label,fn,want)
    matrix=m.covariance_matrix([a,b]);want=[[F(1,10000),F(1,5000)],[F(1,5000),F(1,2500)]]
    for i,j in product(range(2),repeat=2):close('E18/E19 matrix '+str((i,j)),matrix[i][j],want[i][j],atol=0)
    ck('E20 Cauchy-Schwarz equality and singular matrix',want[0][1]**2==want[0][0]*want[1][1])
    ck('matrix quadratic form nonnegative for nine signed vectors',all(sum(F(u[i])*want[i][j]*F(u[j]) for i,j in product(range(2),repeat=2))>=0 for u in product([-1,0,1],repeat=2)))
    for label,x,y in [('nonlinear zero covariance',[-1,0,1],[1,0,1]),('mixed unsorted pairs',[2,-3,5,1],[7,2,-1,4])]:
        for ddof in (0,1):num(label+' '+str(ddof),lambda x=x,y=y,ddof=ddof:m.covariance(x,y,ddof),oracle(x,y,ddof))
    for label,fn in [
        ('E15 constant correlation undefined',lambda:m.correlation([.02]*3,b)),
        ('E23 single sample undefined',lambda:m.covariance([1],[2])),
        ('empty rejected',lambda:m.covariance([],[])),
        ('missing rejected',lambda:m.covariance([1,None],[1,2])),
        ('nonfinite rejected',lambda:m.covariance([1,math.inf],[1,2])),
        ('boolean rejected',lambda:m.covariance([True,1],[1,2])),
        ('invalid ddof rejected',lambda:m.covariance(a,b,2)),
        ('length mismatch rejected',lambda:m.covariance([1,2],[1])),
        ('matrix unequal lengths rejected',lambda:m.covariance_matrix([[1,2],[1,2,3]])),
        ('weight nonfinite rejected',lambda:m.two_asset_variance(a,b,math.nan)),
        ('F131 unreportable covariance rejected',lambda:m.covariance([-1e308,1e308],[-1e308,1e308])),
    ]:reject(label,fn)
    ck('project fixtures preserved',a==[.01,.02,.03] and b==[.02,.04,.06])
    project=dict(dates=['synthetic period 1','synthetic period 2','synthetic period 3'],frequency='unspecified common period',units='decimal simple returns',source='synthetic manuscript fixture',a=a,b=b,
        fixture_sha256=hashlib.sha256(json.dumps([a,b]).encode()).hexdigest(),supplemental_means=[str(sum(map(lambda v:F(str(v)),z))/3) for z in [a,b]],
        sample_covariance=m.covariance(a,b),population_covariance=m.covariance(a,b,0),covariance_matrix=matrix,correlation=m.correlation(a,b),
        portfolio_variance=m.two_asset_variance(a,b,.5),portfolio_sd=math.sqrt(m.two_asset_variance(a,b,.5)),reflected_covariance=m.covariance(a,[-v for v in b]))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
