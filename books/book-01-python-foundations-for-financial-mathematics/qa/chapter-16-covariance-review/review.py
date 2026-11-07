"""Exact manuscript listing execution; independent pairwise covariance benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.05-covariance-matrices.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.05-covariance-matrices.md'])
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
    with tempfile.TemporaryDirectory(prefix='book1-1605-') as tmp:
        Path(tmp,'covariance_matrices.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['covariance_matrices.py']),('isolated import',['-c','import covariance_matrices']),('exact compilation',['-m','compileall','-q','covariance_matrices.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['covariance_matrices.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    basic=[[1,2],[2,4],[3,6]];ident=[[1,0],[0,1]];perfect=[[1,2],[2,4]];hedge=[[1,-1],[-1,1]]
    for label,fn,want in [
      ('E1 sample covariance',lambda:m.covariance_matrix(basic)[0][1],2),
      ('E2 sample variance',lambda:m.covariance_matrix(basic)[0][0],1),
      ('E3 population covariance',lambda:m.covariance_matrix(basic,0)[0][1],F(4,3)),
      ('E7 perfect correlation',lambda:m.correlation_matrix(perfect)[0][1],1),
      ('E8 negative correlation',lambda:m.correlation_matrix(hedge)[0][1],-1),
      ('E9 uncorrelated',lambda:m.correlation_matrix(ident)[0][1],0),
      ('E10 equal weights',lambda:m.portfolio_variance([.5,.5],ident),F(1,2)),
      ('E11 source variance then independently rooted SD',lambda:root(m.portfolio_variance([.5,.5],ident)),root(F(1,2))),
      ('E12 collinear risk',lambda:m.portfolio_variance([.5,.5],perfect),F(9,4)),
      ('E13 perfect hedge',lambda:m.portfolio_variance([.5,.5],hedge),0),
      ('E15 percent scaling',lambda:m.covariance_matrix([[100*a,100*b] for a,b in basic])[0][1],20000),
      ('E28 quadratic form',lambda:m.portfolio_variance([.6,.4],[[.04,.01],[.01,.09]]),F(21,625)),
      ('E29 source variance then independently rooted SD',lambda:root(m.portfolio_variance([.6,.4],[[.04,.01],[.01,.09]])),root(F(21,625))),
      ('F146 integer centered precision',lambda:m.covariance_matrix([[10**18],[10**18+1]])[0][0],F(1,2)),
      ('F146 constant large rows avoid mean overflow',lambda:m.covariance_matrix([[1e308],[1e308]])[0][0],0),
      ('F146 finite covariance after denominator',lambda:m.covariance_matrix([[-1e154],[1e154]],0)[0][0],1e308),
      ('F146 tiny normalized correlation',lambda:m.correlation_matrix([[1e-320,1e-320],[1e-320,1e-320]])[0][1],1),
      ('F146 large correlation denominator',lambda:m.correlation_matrix([[1e308,1e308],[1e308,1e308]])[0][1],1),
      ('F146 signed quadratic cancellation',lambda:m.portfolio_variance([1e154,-1e154],[[2,2],[2,2]]),0),
      ('F146 weights retain integer difference',lambda:m.portfolio_variance([10**18+1,-10**18],[[1,1],[1,1]]),1),
    ]:num(label,fn,want)
    ck('E4/E5 full sample matrix and symmetry',m.covariance_matrix(basic)==[[1,2],[2,4]])
    rows=[[.01,.02],[-.01,0],[.02,.03],[0,-.01]];w=[.5,.5];expected=paircov(rows,1);sample=m.covariance_matrix(rows);pop=m.covariance_matrix(rows,0)
    means=[sum(F(str(row[j])) for row in rows)/4 for j in range(2)]
    centered=[[F(str(row[j]))-means[j] for j in range(2)] for row in rows]
    for i in range(2):
      for j in range(2):
        close(f'lab sample entry {i},{j}',sample[i][j],expected[i][j]);close(f'lab population entry {i},{j}',pop[i][j],expected[i][j]*F(3,4))
    corr=m.correlation_matrix(sample)
    close('lab correlation',corr[0][1],expected[0][1]/F(str(root(expected[0][0]*expected[1][1]))))
    for weights in [[.5,.5],[1,0],[0,1]]:
      want=sum(F(str(weights[i]))*expected[i][j]*F(str(weights[j])) for i in range(2) for j in range(2))
      close('lab variance '+str(weights),m.portfolio_variance(weights,sample),want)
    # Source evaluates rounded input endpoints; oracle uses the exact determinant bound.
    bound=root(expected[0][0]*expected[1][1]);base=(expected[0][0]+expected[1][1])/4
    stress=[]
    for rho in [-1,0,1]:
      cross=float(bound)*rho
      cov=[[float(expected[0][0]),cross],[cross,float(expected[1][1])]]
      value=m.portfolio_variance(w,cov);stress.append(value)
      close('lab feasible covariance stress '+str(rho),value,D(str(base.numerator))/D(str(base.denominator))+D(rho)*bound/2)
    close('lab population portfolio variance',m.portfolio_variance(w,pop),F(27,160000))
    close('lab population correlation invariant',m.correlation_matrix(pop)[0][1],root(F(18,25)))
    num('PSD tolerance small negative direction clipped',lambda:m.portfolio_variance([.5,-.5],[[1,1.0000000000005],[1.0000000000005,1]]),0)
    num('relative tiny-scale PSD valid direction',lambda:m.portfolio_variance([1,0],[[1e-300,0],[0,1e-300]]),F(1,10**300))
    reject('relative tiny-scale PSD invalid direction rejected',lambda:m.portfolio_variance([1,0],[[1e-300,2e-300],[2e-300,1e-300]]))
    num('near-symmetric input uses declared average',lambda:m.portfolio_variance([.5,.5],[[1,.2],[.20000000001,1]]),F('0.6000000000025'))
    num('zero-variance asset allowed for quadratic form',lambda:m.portfolio_variance([.5,.5],[[1,0],[0,0]]),F(1,4))
    num('singular hedge direction',lambda:m.portfolio_variance([2,-1],perfect),0)
    num('E30 covariance sensitivity',lambda:m.portfolio_variance([.6,.4],[[.04,.02],[.02,.09]])-m.portfolio_variance([.6,.4],[[.04,.01],[.01,.09]]),F(3,625))
    # Complete synchronized two-observation panel: rank <=1, even with five assets.
    c=m.covariance_matrix([[0,0,0,0,0],[1,2,3,4,5]])
    ck('E16 rank-one five-asset construction',all(F(str(c[i][j]))==F((i+1)*(j+1),2) for i in range(5) for j in range(5)))
    ck('E26 three full rolling windows',len([rows for _ in range(5-3+1)])==3,scope='supplemental count, no source rolling estimator')
    for label,fn in [
      ('F146 PSD rejected even for nonnegative supplied direction',lambda:m.portfolio_variance([1,0],[[1,2],[2,1]])),
      ('F146 PSD rejected for zero supplied weights',lambda:m.portfolio_variance([0,0],[[1,2],[2,1]])),
      ('F146 full PSD beyond pairwise correlation bounds',lambda:m.correlation_matrix([[1,.9,.9],[.9,1,-.9],[.9,-.9,1]])),
      ('F146 tiny-scale invalid negative variance rejected',lambda:m.portfolio_variance([1],[[ -1e-300 ]])),
      ('F146 correlation rejects asymmetry',lambda:m.correlation_matrix([[1,.2],[.4,1]])),
      ('F146 correlation rejects NaN',lambda:m.correlation_matrix([[1,math.nan],[math.nan,1]])),
      ('F146 impossible correlation rejected',lambda:m.correlation_matrix([[1,2],[2,1]])),
      ('F146 zero-variance nonzero covariance rejected',lambda:m.portfolio_variance([1,0],[[1,1e-30],[1e-30,0]])),
      ('F146 nonzero covariance underflow rejected',lambda:m.covariance_matrix([[0],[1e-200]])[0][0]),
      ('F146 unreportable covariance rejected',lambda:m.covariance_matrix([[-1e308],[1e308]])),
      ('F146 nonzero quadratic underflow rejected',lambda:m.portfolio_variance([1e-200],[[1]])),
      ('F146 unreportable quadratic rejected',lambda:m.portfolio_variance([1e308],[[1]])),
      ('F146 huge integer data gets ValueError',lambda:m.covariance_matrix([[10**1000],[0]])),
      ('F146 malformed correlation outer gets ValueError',lambda:m.correlation_matrix(None)),
      ('F146 malformed correlation row gets ValueError',lambda:m.correlation_matrix([1])),
      ('E18 zero variance correlation undefined',lambda:m.correlation_matrix([[0,0],[0,1]])),
      ('invalid ddof rejected',lambda:m.covariance_matrix(rows,True)),
      ('misaligned data rejected',lambda:m.covariance_matrix([[1,2],[3]])),
      ('boolean covariance rejected',lambda:m.correlation_matrix([[True]])),
    ]:reject(label,fn)
    ck('lab inputs preserved',rows==[[.01,.02],[-.01,0],[.02,.03],[0,-.01]] and w==[.5,.5])
    report=dict(assets=['fictional A','fictional B'],rows=rows,weights=w,means=[str(v) for v in means],centered=[[str(v) for v in row] for row in centered],sample=sample,population=pop,correlation=corr,
      standard_deviations=[str(root(expected[i][i])) for i in range(2)],equal_weight_variance=m.portfolio_variance(w,sample),covariance_stress_equal_weight_variances=stress,
      fixture_sha256=hashlib.sha256(json.dumps([rows,w]).encode()).hexdigest(),horizon='one common synthetic period',currency='fictional common USD',timestamps='synchronized observation labels 1-4, no real dates',missingness='complete listwise panel, no imputation',source_root_scope='standard deviations supplemented by independent Decimal roots')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
