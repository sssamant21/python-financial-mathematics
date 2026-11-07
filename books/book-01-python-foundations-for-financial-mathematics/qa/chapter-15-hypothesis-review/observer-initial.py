"""Section 15.9 exact hypothesis lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.09-hypothesis-testing-foundations.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1509-') as tmp:
        Path(tmp,'hypothesis_testing.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['hypothesis_testing.py']),('isolated import',['-c','import hypothesis_testing']),('exact compilation',['-m','compileall','-q','hypothesis_testing.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['hypothesis_testing.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('hypothesis_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations,product
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    def gaussian_p(z):
        # Integrate exp(-u^2/2) by its power series; no erfc or normal CDF oracle.
        with localcontext() as ctx:
            ctx.prec=80
            z=D(str(z));pi=D('3.14159265358979323846264338327950288419716939937510582097494459230781640628620899')
            term=z;integral=z
            for k in range(1,300):
                term*=(-z*z)/(2*k)
                piece=term/(2*k+1);integral+=piece
                if abs(piece)<D('1e-75'):break
            return 1-2*integral/(2*pi).sqrt()
    x=[.01,.02,.03];t=root(12)
    for label,fn,want in [
        ('E8 source t statistic',lambda:m.one_sample_t_statistic(x),t),
        ('source null at sample mean',lambda:m.one_sample_t_statistic(x,.02),0),
        ('E11 normal p zero',lambda:m.normal_two_sided_p(0),1),
        ('E12 normal p at 1.96',lambda:m.normal_two_sided_p(1.96),gaussian_p(1.96)),
        ('normal CDF zero',lambda:m.normal_cdf(0),F(1,2)),
        ('normal p symmetry',lambda:m.normal_two_sided_p(-1.96),gaussian_p(1.96)),
        ('E20 sign five positive',lambda:m.exact_sign_test_p([1,2,3,4,5]),F(1,16)),
        ('E21 sign ties discarded',lambda:m.exact_sign_test_p([0,1,2,3]),F(1,4)),
        ('balanced sign',lambda:m.exact_sign_test_p([-2,-1,1,2]),1),
        ('F135 integer centered t',lambda:m.one_sample_t_statistic([10**18,10**18+2],10**18),1),
        ('F135 small-scale t',lambda:m.one_sample_t_statistic([1e-200,2e-200,3e-200]),t),
        ('F135 large-scale t',lambda:m.one_sample_t_statistic([1e308,1.1e308,1.2e308]),11*root(3)),
        ('F135 extreme finite t',lambda:m.one_sample_t_statistic([-1e308,1e308],1e308),-1),
        ('F135 integer sign counts',lambda:m.exact_sign_test_p([10**18+1,10**18+2],10**18),F(1,2)),
        ('F135 reportable subnormal sign probability',lambda:m.exact_sign_test_p([1]*1075),F(1,2**1074)),
        ('project hypothetical cost threshold t',lambda:m.one_sample_t_statistic(x,.005),F(3,2)*root(3)),
    ]:num(label,fn,want)
    for label,p,alpha,want in [('E13 reject',.01,.05,'reject H0'),('E14 not reject',.2,.05,'do not reject H0'),('E15 boundary',.05,.05,'reject H0')]:ck(label,m.decision(p,alpha)==want)
    states=list(product([-1,1],repeat=5));exact_tail=F(sum(abs(sum(s))>=5 for s in states),len(states))
    close('enumerated 32 sign outcomes',m.exact_sign_test_p([1,2,3,4,5]),exact_tail,atol=0)
    for label,fn in [
        ('singleton rejected',lambda:m.one_sample_t_statistic([1])),
        ('constant rejected',lambda:m.one_sample_t_statistic([1,1,1])),
        ('F135 decimal constant rejected',lambda:m.one_sample_t_statistic([.05]*3)),
        ('missing rejected',lambda:m.one_sample_t_statistic([1,None])),
        ('boolean rejected',lambda:m.one_sample_t_statistic([True,2])),
        ('nonfinite rejected',lambda:m.one_sample_t_statistic([1,math.inf])),
        ('bad null rejected',lambda:m.one_sample_t_statistic(x,math.nan)),
        ('all ties rejected',lambda:m.exact_sign_test_p([0,0])),
        ('bad p rejected',lambda:m.decision(-.1)),
        ('bad alpha rejected',lambda:m.decision(.1,0)),
        ('F135 unreportable sign probability rejected',lambda:m.exact_sign_test_p([1]*2000)),
        ('F135 unreportable normal tail rejected',lambda:m.normal_two_sided_p(40)),
    ]:reject(label,fn)
    ci_source=BOOK/'chapter-15/15.08-confidence-intervals.md'
    ci_code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',ci_source.read_bytes(),re.M|re.S)
    ci=types.ModuleType('matching_ci');exec(compile(ci_code,str(ci_source),'exec'),ci.__dict__)
    interval=ci.t_mean_ci(x,4.302652729911275)
    with localcontext() as ctx:
        ctx.prec=80
        df2_p=1-root(F(6,7))
    ck('project matching t CI and df2 test both do not reject',interval[0]<0<interval[1] and m.decision(float(df2_p),.05)=='do not reject H0')
    ck('project sign p .0625 does not reject',m.decision(m.exact_sign_test_p([1,2,3,4,5]),.05)=='do not reject H0')
    ck('source returns unchanged',x==[.01,.02,.03])
    project=dict(source_returns=x,period_labels=[1,2,3],dates=None,frequency='hypothetical daily',units='decimal simple returns',null_mean=0,alternative='two-sided, prespecified',alpha=.05,
        fixture_sha256=hashlib.sha256(json.dumps(x).encode()).hexdigest(),source_t=m.one_sample_t_statistic(x),df=2,supplemental_df2_p=str(df2_p),
        supplemental_df2_method='closed-form t(df=2) CDF=1/2+t/(2sqrt(t^2+2)); p=1-sqrt(6/7)',decision=m.decision(float(df2_p),.05),
        matching_ci=interval,ci_listing_sha256=hashlib.sha256(ci_code).hexdigest(),ci_source_sha256=hashlib.sha256(ci_source.read_bytes()).hexdigest(),
        source_sign_p=m.exact_sign_test_p([1,2,3,4,5]),hypothetical_per_period_cost=.005,net_effect=.015,cost_threshold_t=m.one_sample_t_statistic(x,.005))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,additional_exact_source_ci_calls=1,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
