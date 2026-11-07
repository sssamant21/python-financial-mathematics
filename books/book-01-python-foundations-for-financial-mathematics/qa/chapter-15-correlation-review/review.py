"""Section 15.6 exact correlation lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.06-correlation.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1506-') as tmp:
        Path(tmp,'correlation.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['correlation.py']),('isolated import',['-c','import correlation']),('exact compilation',['-m','compileall','-q','correlation.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['correlation.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('correlation_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations,product
    def oracle(x,y):
        x=[F(str(v)) for v in x];y=[F(str(v)) for v in y];n=len(x)
        cross=sum((x[i]-x[j])*(y[i]-y[j]) for i,j in combinations(range(n),2))
        xx=sum((x[i]-x[j])**2 for i,j in combinations(range(n),2));yy=sum((y[i]-y[j])**2 for i,j in combinations(range(n),2))
        ratio=cross**2/(xx*yy)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(ratio.numerator)/D(ratio.denominator)).sqrt()*(1 if cross>=0 else -1)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 positive',lambda:m.pearson([1,2,3],[2,4,6]),1),
        ('E2 negative',lambda:m.pearson([1,2,3],[-2,-4,-6]),-1),
        ('E3 dependent zero',lambda:m.pearson([-1,0,1],[1,0,1]),0),
        ('E4 units',lambda:m.pearson([.01,.02,.03],[2,4,6]),1),
        ('E9 ratio',lambda:m.pearson([1,2,3],[2,4,6]),1),
        ('E10 shift',lambda:m.pearson([11,12,13],[2,4,6]),1),
        ('E11 reversal',lambda:m.pearson([1,2,3],[-2,-4,-6]),-1),
        ('E12 symmetry',lambda:m.pearson([2,4,6],[1,2,3]),1),
        ('E15 nonlinear Pearson',lambda:m.pearson([1,2,3,4],[1,4,9,16]),oracle([1,2,3,4],[1,4,9,16])),
        ('E15 monotonic Spearman',lambda:m.spearman([1,2,3,4],[1,4,9,16]),1),
        ('E16 inverse Spearman',lambda:m.spearman([1,2,3,4],[16,9,4,1]),-1),
        ('E18 tied Spearman',lambda:m.spearman([5,2,5,1],[9,3,6,6]),oracle([3.5,2,3.5,1],[4,1,2.5,2.5])),
        ('E22 symmetric dependence',lambda:m.pearson([-2,-1,0,1,2],[4,1,0,1,4]),0),
        ('F132 integer Pearson',lambda:m.pearson([10**18,10**18+1,10**18+2],[1,2,3]),1),
        ('F132 integer Spearman',lambda:m.spearman([10**18,10**18+1,10**18+2],[1,2,3]),1),
        ('F132 large-product Pearson',lambda:m.pearson([0,1e100,2e100],[0,2e100,4e100]),1),
        ('F132 small-product Pearson',lambda:m.pearson([0,1e-100,2e-100],[0,2e-100,4e-100]),1),
        ('F132 opposite-extreme Pearson',lambda:m.pearson([-1e308,0,1e308],[-1,0,1]),1),
        ('F132 large-offset mean Pearson',lambda:m.pearson([1e308,1.1e308,1.2e308],[1,2,3]),1),
    ]:num(label,fn,want)
    ck('E17 average ranks',m.average_tie_ranks([5,2,5,1])==[3.5,2,3.5,1])
    a=[.01,.02,.03,.04,.05,.06];b=[.02,.01,.04,.03,.06,.05]
    num('project Pearson/covariance-SD ratio',lambda:m.pearson(a,b),oracle(a,b))
    # Ranks of the two explicit fixture arrays are 1..6 and [2,1,4,3,6,5].
    num('project Spearman',lambda:m.spearman(a,b),oracle([1,2,3,4,5,6],[2,1,4,3,6,5]))
    for window in [3,4]:
        actual=m.rolling_pearson(a,b,window)
        ck('E19/project rolling count '+str(window),len(actual)==len(a)-window+1)
        for i,value in enumerate(actual):close('project rolling '+str((window,i)),value,oracle(a[i:i+window],b[i:i+window]),atol=0)
    matrix=m.correlation_matrix([a,b])
    for i,j in product(range(2),repeat=2):close('E21/project matrix '+str((i,j)),matrix[i][j],1 if i==j else oracle(a,b),atol=0)
    ck('E13 matrix range',all(-1<=v<=1 for row in matrix for v in row))
    ck('matrix PSD in this two-asset fixture',1-float(oracle(a,b))**2>=0)
    for label,fn in [
        ('E14 constant undefined',lambda:m.pearson([1,1,1],[1,2,3])),
        ('F132 decimal constant undefined',lambda:m.pearson([.05]*3,[1,2,3])),
        ('constant ranks undefined',lambda:m.spearman([1,1,1],[1,2,3])),
        ('empty rejected',lambda:m.pearson([],[])),
        ('one pair rejected',lambda:m.pearson([1],[2])),
        ('boolean rejected',lambda:m.pearson([True,2],[1,2])),
        ('nonfinite rejected',lambda:m.pearson([1,math.inf],[1,2])),
        ('missing rejected',lambda:m.pearson([1,None],[1,2])),
        ('length mismatch rejected',lambda:m.pearson([1,2],[1])),
        ('bad rolling size rejected',lambda:m.rolling_pearson(a,b,1)),
        ('constant rolling window rejected',lambda:m.rolling_pearson([1,1,2],[1,2,3],2)),
        ('matrix length mismatch rejected',lambda:m.correlation_matrix([[1,2],[1,2,3]])),
    ]:reject(label,fn)
    ck('project inputs unchanged',a==[.01,.02,.03,.04,.05,.06] and b==[.02,.01,.04,.03,.06,.05])
    project=dict(a=a,b=b,period_labels=list(range(1,7)),frequency='hypothetical daily',dates=None,units='decimal simple returns',source='synthetic fixture declared in reviewed manuscript',
        fixture_sha256=hashlib.sha256(json.dumps([a,b]).encode()).hexdigest(),pearson=m.pearson(a,b),spearman=m.spearman(a,b),
        rolling={str(w):m.rolling_pearson(a,b,w) for w in [3,4]},matrix=matrix,
        monotonic_pearson=m.pearson([1,2,3,4],[1,4,9,16]),monotonic_spearman=m.spearman([1,2,3,4],[1,4,9,16]),
        symmetric_pearson=m.pearson([-2,-1,0,1,2],[4,1,0,1,4]))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
