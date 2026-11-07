"""Exact manuscript listing execution; independent pairwise covariance benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.06-portfolio-variance.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.06-portfolio-variance.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want)
    def reject(label,fn):
        try:v=fn()
        except ValueError as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(v))
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80;return (D(v.numerator)/D(v.denominator)).sqrt()
    def paircov(rows,ddof):
        rows=[[F(str(v)) for v in row] for row in rows];t=len(rows);n=len(rows[0])
        return [[sum((rows[a][i]-rows[b][i])*(rows[a][j]-rows[b][j]) for a in range(t) for b in range(a+1,t))/(t*(t-ddof)) for j in range(n)] for i in range(n)]
    with tempfile.TemporaryDirectory(prefix='book1-1606-') as tmp:
        Path(tmp,'portfolio_variance.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['portfolio_variance.py']),('isolated import',['-c','import portfolio_variance']),('exact compilation',['-m','compileall','-q','portfolio_variance.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_variance.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    c=[[.04,.01],[.01,.09]];w=[.6,.4]
    def quad(weights,matrix):
        f=lambda x:F(str(x))
        return sum(f(weights[i])*f(matrix[i][j])*f(weights[j]) for i in range(len(weights)) for j in range(len(weights)))
    decomp=m.variance_decomposition(w,c);comp=m.asset_variance_contributions(w,c);grad=m.marginal_variance(w,c)
    for label,fn,want in [
      ('E1 single asset',lambda:m.portfolio_variance([1],[[.04]]),F(1,25)),
      ('E2 independent two-asset',lambda:m.portfolio_variance([.5,.5],[[.04,0],[0,.09]]),F(13,400)),
      ('E3/E7 worked total',lambda:m.portfolio_variance(w,c),F(21,625)),
      ('E4 worked volatility',lambda:m.volatility(w,c),root(F(21,625))),
      ('E5 diagonal',lambda:decomp['diagonal'],F(18,625)),
      ('E6 cross',lambda:decomp['cross'],F(3,625)),
      ('E8 zero correlation equal risk',lambda:m.portfolio_variance([.5,.5],[[.04,0],[0,.04]]),F(1,50)),
      ('E9 perfect positive equal risk',lambda:m.portfolio_variance([.5,.5],[[.04,.04],[.04,.04]]),F(1,25)),
      ('E10/E11 perfect hedge',lambda:m.portfolio_variance([.5,.5],[[1,-1],[-1,1]]),0),
      ('E12 concentrated portfolio',lambda:m.portfolio_variance([1,0],c),F(1,25)),
      ('E13 contribution A',lambda:comp[0],F(21,1250)),
      ('E14 contribution B',lambda:comp[1],F(21,1250)),
      ('E15 contribution reconciliation',lambda:math.fsum(comp),F(21,625)),
      ('E16 unconstrained marginal A',lambda:grad[0],F(7,125)),
      ('E17 unconstrained marginal B',lambda:grad[1],F(21,250)),
      ('E18 covariance sensitivity',lambda:m.portfolio_variance(w,[[.04,.015],[.015,.09]])-m.portfolio_variance(w,c),F(3,1250)),
      ('E20 permitted signed portfolio',lambda:m.portfolio_variance([1.2,-.2],c,True),F(141,2500)),
      ('E27 percent scaling',lambda:m.portfolio_variance(w,[[400,100],[100,900]]),336),
      ('E30 negative hedge contribution',lambda:m.asset_variance_contributions([.75,.25],[[1,-2],[-2,4]])[1],F(-1,8)),
      ('F147 integer weight cancellation',lambda:m.portfolio_variance([10**18+1,-10**18],[[1,1],[1,1]],True),1),
      ('F147 large signed quadratic cancellation',lambda:m.portfolio_variance([1e308,-1e308,1],[[2,2,2],[2,2,2],[2,2,2]],True),2),
      ('F147 large signed marginal cancellation',lambda:m.marginal_variance([1e308,-1e308,1],[[2,2,2],[2,2,2],[2,2,2]],True)[0],4),
      ('F147 normalized tolerated budget variance',lambda:m.portfolio_variance([1.00000000005],[[1]]),1),
      ('F147 normalized tolerated budget contribution',lambda:m.asset_variance_contributions([1.00000000005],[[1]])[0],1),
      ('F147 normalized tolerated budget marginal',lambda:m.marginal_variance([1.00000000005],[[1]])[0],2),
      ('F147 volatility before overflowing variance',lambda:m.volatility([1.5,-.5],[[1e308,0],[0,1e308]],True),root(F(25,10)*10**308)),
      ('F147 volatility before unreportable variance',lambda:m.volatility([.1,.9],[[1e-323,0],[0,0]]),root(F(1,10**325))),
    ]:num(label,fn,want)
    # Budget-preserving central difference of a quadratic is exact analytically.
    h=F(1,8);plus=[float(F(3,5)+h),float(F(2,5)-h)];minus=[float(F(3,5)-h),float(F(2,5)+h)]
    num('lab feasible central directional derivative',lambda:(m.portfolio_variance(plus,c)-m.portfolio_variance(minus,c))/float(2*h),F(-7,250))
    num('lab gradient directional derivative',lambda:grad[0]-grad[1],F(-7,250))
    close('lab diagonal plus cross reconciliation',decomp['diagonal']+decomp['cross'],quad(w,c))
    close('lab no covariance variance',m.portfolio_variance(w,[[.04,0],[0,.09]]),F(18,625))
    close('lab raised covariance variance',m.portfolio_variance(w,[[.04,.015],[.015,.09]]),F(9,250))
    ck('E19 supplemental scaling only',quad([1.2,.8],c)==4*quad(w,c),reference=str(4*quad(w,c)),scope='unnormalized rational quadratic, fully invested source rejects doubled weights')
    close('E24 supplementary annual variance',F(252,10000),F(63,2500))
    close('E25 supplementary annual volatility',root(F(252,10000)),root(F(63,2500)))
    # Demonstrate a material ordering error and its consistent-permutation correction.
    reverse=[[.09,.01],[.01,.04]]
    close('E28 misordered weights change variance',m.portfolio_variance(w,reverse),F(109,2500))
    close('E28 consistently permuted weights restore result',m.portfolio_variance(list(reversed(w)),reverse),F(21,625))
    # Full-matrix screen is an added scope beyond the old requested-direction boundary.
    for name,fn in [('variance',m.portfolio_variance),('decomposition',m.variance_decomposition),('marginal',m.marginal_variance),('contribution',m.asset_variance_contributions),('volatility',m.volatility)]:
      reject('PSD extension invalid untested direction '+name,lambda fn=fn:fn([1,0],[[1,2],[2,1]]))
    for label,fn in [
      ('F147 negative tiny diagonal rejected',lambda:m.portfolio_variance([1],[[-1e-300]])),
      ('F147 nonboolean short policy rejected',lambda:m.portfolio_variance([1],[[1]],'yes')),
      ('F147 bad tolerance rejected',lambda:m.validate_covariance([[1]],math.nan)),
      ('F147 boolean tolerance rejected',lambda:m.validate_covariance([[1]],True)),
      ('F147 unreportable variance rejected',lambda:m.portfolio_variance([1.5,-.5],[[1e308,0],[0,1e308]],True)),
      ('F147 underflow variance rejected',lambda:m.portfolio_variance([.1,.9],[[1e-323,0],[0,0]])),
      ('F147 unreportable decomposition field rejected',lambda:m.variance_decomposition([1e308,-1e308,1],[[2,2,2],[2,2,2],[2,2,2]],True)),
      ('F147 unreportable contribution rejected',lambda:m.asset_variance_contributions([1e308,-1e308,1],[[2,2,2],[2,2,2],[2,2,2]],True)),
      ('F147 unreportable marginal rejected',lambda:m.marginal_variance([1],[[1e308]])),
      ('F147 huge integer matrix ValueError',lambda:m.portfolio_variance([1],[[10**1000]])),
      ('F147 negative exact requested form rejected',lambda:m.portfolio_variance([.5,.5],[[1,-1.000000000001],[-1.000000000001,1]])),
      ('E19 doubled budget rejected',lambda:m.portfolio_variance([1.2,.8],c)),
      ('short permission required',lambda:m.portfolio_variance([1.2,-.2],c)),
      ('invalid budget rejected',lambda:m.portfolio_variance([.6,.3],c)),
      ('ragged matrix rejected',lambda:m.portfolio_variance(w,[[1,0],[0]])),
      ('nonfinite matrix rejected',lambda:m.portfolio_variance([1],[[math.inf]])),
      ('zero diagonal nonzero covariance rejected',lambda:m.portfolio_variance([1,0],[[1,1e-20],[1e-20,0]])),
    ]:reject(label,fn)
    ck('lab original inputs preserved',w==[.6,.4] and c==[[.04,.01],[.01,.09]])
    report=dict(assets=['fictional A','fictional B'],weights=w,covariance=c,horizon='one common synthetic period',currency='fictional common USD',units='squared decimal simple-return units',dates=None,estimator='supplied synthetic PSD matrix; no sampling/calibration claim',
      decomposition=decomp,variance_contributions=comp,marginal_variance=grad,variance=m.portfolio_variance(w,c),volatility=m.volatility(w,c),covariance_weighted_exposures=['.028','.042'],feasible_direction=[1,-1],feasible_derivative='-.028',covariance_increase='.005',variance_increase='.0024',fixture_sha256=hashlib.sha256(json.dumps([w,c]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
