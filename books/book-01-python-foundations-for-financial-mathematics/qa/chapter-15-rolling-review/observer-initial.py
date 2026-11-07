"""Section 15.12 exact rolling lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.12-rolling-statistics.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1512-') as tmp:
        Path(tmp,'rolling_statistics.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['rolling_statistics.py']),('isolated import',['-c','import rolling_statistics']),('exact compilation',['-m','compileall','-q','rolling_statistics.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['rolling_statistics.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('rolling_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def fs(v):return [F(str(x)) for x in v]
    def var(v):
        v=fs(v);n=len(v)
        return sum((a-b)**2 for a,b in combinations(v,2))/(n*(n-1))
    def corr(a,b):
        a=fs(a);b=fs(b);n=len(a)
        xx=sum((a[i]-a[j])**2 for i,j in combinations(range(n),2));yy=sum((b[i]-b[j])**2 for i,j in combinations(range(n),2))
        if xx==0 or yy==0:return None
        cross=sum((a[i]-a[j])*(b[i]-b[j]) for i,j in combinations(range(n),2))
        return float(root(cross**2/(xx*yy)))*(1 if cross>=0 else -1)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    def series(label,fn,wants):
        try:values=fn()
        except Exception as exc:ck(label,False,exception=repr(exc));return None
        valid=len(values)==len(wants) and all((v is None if w is None else v is not None and math.isclose(v,float(w),rel_tol=1e-12,abs_tol=0)) for v,w in zip(values,wants))
        ck(label,valid,actual=values,independent_references=[None if w is None else str(w) for w in wants],absolute_tolerance=0,relative_tolerance=1e-12)
        return values
    series('E1 rolling means',lambda:m.rolling_mean([1,2,3,4],2),[F(3,2),F(5,2),F(7,2)])
    series('E2 full window',lambda:m.rolling_mean([1,2,3],3),[2])
    num('E5 sample SD',lambda:m.rolling_sample_std([1,2,3],3)[0],1)
    series('E6 constant SD',lambda:m.rolling_sample_std([2,2,2],2),[0,0])
    num('E7 positive correlation',lambda:m.rolling_correlation([1,2,3],[2,4,6],3)[0],1)
    num('E8 negative correlation',lambda:m.rolling_correlation([1,2,3],[6,4,2],3)[0],-1)
    series('E9 constant correlation',lambda:m.rolling_correlation([1,1,1],[1,2,3],3),[None])
    num('E10 compounded return',lambda:m.rolling_compounded_return([.1,-.1],2)[0],F(-1,100))
    series('E11 total loss and independent local restart',lambda:m.rolling_compounded_return([.1,-1,.1,.2],2),[-1,-1,F(8,25)])
    a=[.01]*10+[.01,-.01]*5+[.04,-.04]*5
    b=[.005,-.005]*5+[.02,-.02]*10
    reports={};total_outputs=0
    for w in [5,10,20]:
        aa=[a[i-w:i] for i in range(w,31)];bb=[b[i-w:i] for i in range(w,31)]
        means=[sum(fs(z))/w for z in aa];sds=[root(var(z)) for z in aa];correlations=[corr(u,v) for u,v in zip(aa,bb)]
        compounded=[math.prod((1+x for x in fs(z)),start=F(1))-1 for z in aa]
        actual_mean=series('project mean w='+str(w),lambda w=w:m.rolling_mean(a,w),means)
        actual_sd=series('project SD w='+str(w),lambda w=w:m.rolling_sample_std(a,w),sds)
        actual_corr=series('project correlation w='+str(w),lambda w=w:m.rolling_correlation(a,b,w),correlations)
        actual_compound=series('project compound w='+str(w),lambda w=w:m.rolling_compounded_return(a,w),compounded)
        series('project annual SD w='+str(w),lambda actual_sd=actual_sd:[v*math.sqrt(252) for v in actual_sd],[root(var(z)*252) for z in aa])
        lagged=m.lagged_signal(actual_mean)
        ck('project lag map w='+str(w),lagged==[None]+actual_mean[:-1] and len(lagged)==31-w)
        expanding=[sum(fs(a[:i]))/i for i in range(w,31)]
        series('project expanding mean via full-prefix calls w='+str(w),lambda w=w:[m.rolling_mean(a[:i],i)[0] for i in range(w,31)],expanding)
        cutoff=20
        changed=a[:cutoff]+[.08]*10
        ck('project no future influence w='+str(w),m.rolling_mean(a,w)[:cutoff-w+1]==m.rolling_mean(changed,w)[:cutoff-w+1])
        reports[str(w)]=dict(ending_periods=list(range(w,31)),warmup_periods=list(range(1,w)),mean=actual_mean,sample_sd=actual_sd,correlation=actual_corr,compound=actual_compound,lagged_mean=lagged,
            annualization_factor=252,annual_sd=[v*math.sqrt(252) for v in actual_sd],expanding_mean_reference=[float(v) for v in expanding])
        total_outputs+=len(aa)
    for label,fn,want in [
        ('F138 large mean',lambda:m.rolling_mean([1e308,1e308],2)[0],1e308),
        ('F138 integer-offset SD',lambda:m.rolling_sample_std([10**18,10**18+2],2)[0],root(2)),
        ('F138 tiny SD',lambda:m.rolling_sample_std([0,2e-200],2)[0],root(F(2,10**400))),
        ('F138 large SD',lambda:m.rolling_sample_std([-1e200,1e200],2)[0],root(F(2)*10**400)),
        ('F138 integer-offset correlation',lambda:m.rolling_correlation([10**18+i for i in range(3)],[1,2,3],3)[0],1),
        ('F138 large product correlation',lambda:m.rolling_correlation([0,1e100,2e100],[0,2e100,4e100],3)[0],1),
        ('F138 small product correlation',lambda:m.rolling_correlation([0,1e-100,2e-100],[0,2e-100,4e-100],3)[0],1),
    ]:num(label,fn,want)
    series('F138 decimal constant SD',lambda:m.rolling_sample_std([.05]*3,3),[0])
    series('F138 decimal constant correlation',lambda:m.rolling_correlation([.05]*3,[1,2,3],3),[None])
    ck('F138 empty lag preserves length',m.lagged_signal([])==[])
    for label,fn in [
        ('bad window rejected',lambda:m.rolling_mean(a,0)),
        ('window too large rejected',lambda:m.rolling_mean(a,31)),
        ('sample window one rejected',lambda:m.rolling_sample_std(a,1)),
        ('unequal pairs rejected',lambda:m.rolling_correlation(a,b[:-1],5)),
        ('missing rejected',lambda:m.rolling_mean([1,None],2)),
        ('nonfinite rejected',lambda:m.rolling_mean([1,math.inf],2)),
        ('boolean rejected',lambda:m.rolling_mean([True,2],2)),
        ('below -100 rejected',lambda:m.rolling_compounded_return([-1.01,0],2)),
        ('F138 false total loss rejected',lambda:m.rolling_compounded_return([-.99]*10,10)),
        ('F138 unreportable compound rejected',lambda:m.rolling_compounded_return([1e308,1e308],2)),
    ]:reject(label,fn)
    ck('project inputs preserved',a==[.01]*10+[.01,-.01]*5+[.04,-.04]*5 and b==[.005,-.005]*5+[.02,-.02]*10)
    project=dict(a=a,b=b,period_labels=list(range(1,31)),dates=None,frequency='hypothetical daily',units='decimal simple returns',fixture_sha256=hashlib.sha256(json.dumps([a,b]).encode()).hexdigest(),
        regime_shift_first_period=21,complete_window_positions=total_outputs,core_metric_values=4*total_outputs,reports=reports,
        execution_scope='lag alignment on synthetic period labels; actual data-availability/order execution not performed')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
