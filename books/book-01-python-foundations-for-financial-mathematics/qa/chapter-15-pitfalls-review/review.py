"""Section 15.13 exact pitfalls lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.13-statistical-pitfalls-in-financial-data.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1513-') as tmp:
        Path(tmp,'statistical_pitfalls.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['statistical_pitfalls.py']),('isolated import',['-c','import statistical_pitfalls']),('exact compilation',['-m','compileall','-q','statistical_pitfalls.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['statistical_pitfalls.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('pitfalls_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import datetime,timezone
    from zoneinfo import ZoneInfo
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    def acf(v):
        x=[F(str(z)) for z in v];n=len(x);mu=sum(x)/n
        # Raw cross-sum expansion, independent of source centered products.
        numerator=sum(x[i]*x[i-1] for i in range(1,n))-mu*sum(x[i]+x[i-1] for i in range(1,n))+(n-1)*mu*mu
        denominator=sum(z*z for z in x)-n*mu*mu
        return numerator/denominator
    for label,fn,want in [
        ('E1 survivor-only mean',lambda:m.survivor_mean([.2,-.5],[True,False]),F(1,5)),
        ('E1 full-universe mean',lambda:m.sample_mean([.2,-.5]),F(-3,20)),
        ('E14 Bonferroni',lambda:m.bonferroni_threshold(.05,20),F(1,400)),
        ('overlap reference',lambda:m.overlapping_returns([.1,-.1],2)[0],F(-1,100)),
        ('source acf convention',lambda:m.lag_one_autocorrelation([1,2,3]),0),
        ('F139 large survivor mean',lambda:m.survivor_mean([1e308,1e308],[True,True]),1e308),
        ('F139 large full mean',lambda:m.sample_mean([1e308]*3),1e308),
        ('F139 integer-offset ACF',lambda:m.lag_one_autocorrelation([10**18+i for i in range(3)]),0),
        ('F139 tiny ACF',lambda:m.lag_one_autocorrelation([1e-200,2e-200,3e-200]),0),
        ('F139 large ACF',lambda:m.lag_one_autocorrelation([1e200,2e200,3e200]),0),
    ]:num(label,fn,want)
    ck('E2/E3 as-of safe/leak/equality',m.audit_asof([(10,9),(10,11),(10,10)])==[False,True,False])
    ck('empty audit preserves zero rows',m.audit_asof([])==[])
    utc_decision=datetime(2026,11,1,5,30,tzinfo=timezone.utc)
    utc_available=datetime.fromisoformat('2026-11-01T01:45:00-04:00')
    ck('aware timestamps compare instants',m.audit_asof([(utc_decision,utc_available)])==[True])
    zone=ZoneInfo('America/New_York')
    fold_decision=datetime(2026,11,1,1,30,tzinfo=zone,fold=0)
    fold_available=datetime(2026,11,1,1,15,tzinfo=zone,fold=1)
    ck('F139 repeated-hour timestamp compares UTC instants',m.audit_asof([(fold_decision,fold_available)])==[True],decision=fold_decision.isoformat(),available=fold_available.isoformat())
    r=[.01,.01,-.01,-.01]*3+[.04,.04,-.04,-.04]*3
    squares=[float(F(str(v))**2) for v in r]
    num('project raw-return ACF',lambda:m.lag_one_autocorrelation(r),acf(r))
    num('project squared-return ACF',lambda:m.lag_one_autocorrelation(squares),acf(squares))
    overlapping=m.overlapping_returns(r,2)
    expected=[(1+F(str(r[i])))*(1+F(str(r[i+1])))-1 for i in range(len(r)-1)]
    ck('E9/project all 23 overlapping outputs',len(overlapping)==23 and all(math.isclose(a,float(b),rel_tol=1e-12,abs_tol=0) for a,b in zip(overlapping,expected)),actual=overlapping,independent_references=list(map(str,expected)))
    threshold=m.bonferroni_threshold(.05,20);p_values=[.001,.003,.02,.07]+[.5]*16
    ck('project complete twenty-test ledger and adjusted decision',len(p_values)==20 and [i for i,p in enumerate(p_values) if p<=threshold]==[0])
    net=[float(F(str(v))-F(1,1000)) for v in r]
    num('project gross mean',lambda:m.sample_mean(r),0)
    num('project synthetic net-of-cost mean',lambda:m.sample_mean(net),F(-1,1000))
    for label,fn in [
        ('no retained units rejected',lambda:m.survivor_mean([1,2],[False,False])),
        ('bad retention flags rejected',lambda:m.survivor_mean([1,2],[1,0])),
        ('malformed audit row rejected',lambda:m.audit_asof([(1,)])),
        ('F139 NaN audit timestamp rejected',lambda:m.audit_asof([(10,math.nan)])),
        ('F139 infinite audit timestamp rejected',lambda:m.audit_asof([(math.inf,9)])),
        ('F139 boolean audit timestamp rejected',lambda:m.audit_asof([(True,False)])),
        ('F139 lexical timestamp rejected',lambda:m.audit_asof([('2026-1-2','2026-1-10')])),
        ('F139 naive datetime rejected',lambda:m.audit_asof([(datetime(2026,1,2),datetime(2026,1,1))])),
        ('F139 mixed clocks rejected',lambda:m.audit_asof([(utc_decision,10)])),
        ('constant ACF rejected',lambda:m.lag_one_autocorrelation([1,1,1])),
        ('F139 decimal constant ACF rejected',lambda:m.lag_one_autocorrelation([.05]*3)),
        ('too short ACF rejected',lambda:m.lag_one_autocorrelation([1,2])),
        ('missing returns rejected',lambda:m.sample_mean([1,None])),
        ('nonfinite returns rejected',lambda:m.sample_mean([math.nan,1])),
        ('bad overlap window rejected',lambda:m.overlapping_returns([.1],2)),
        ('below total loss rejected',lambda:m.overlapping_returns([-.1,-1.01],2)),
        ('bad alpha rejected',lambda:m.bonferroni_threshold(1,20)),
        ('bad test count rejected',lambda:m.bonferroni_threshold(.05,0)),
        ('F139 unreportable threshold rejected',lambda:m.bonferroni_threshold(1e-323,10)),
        ('F139 false total loss rejected',lambda:m.overlapping_returns([-.99]*10,10)),
        ('F139 unreportable overlap rejected',lambda:m.overlapping_returns([1e308,1e308],2)),
    ]:reject(label,fn)
    ck('source inputs preserved',r==[.01,.01,-.01,-.01]*3+[.04,.04,-.04,-.04]*3)
    project=dict(universe_fixture=dict(returns=[.2,-.5],retained=[True,False],scope='one cross-sectional period, separate from return time-series fixture'),
        raw_returns=r,squared_returns=squares,net_returns=net,period_labels=list(range(1,25)),dates=None,frequency='hypothetical daily',units='decimal simple returns',
        fixture_sha256=hashlib.sha256(json.dumps([[.2,-.5],r,p_values]).encode()).hexdigest(),survivor_mean=m.survivor_mean([.2,-.5],[True,False]),full_mean=m.sample_mean([.2,-.5]),
        availability_pairs=[[10,9],[10,11],[10,10]],late_flags=m.audit_asof([(10,9),(10,11),(10,10)]),equality_scope='latency unresolved; False is not proof of timing validity',
        revision_example=dict(event_label=1,decision=10,versions=[dict(version='original',available=9,value=100),dict(version='revised',available=12,value=150)],late_flags=m.audit_asof([(10,9),(10,12)])),
        p_values=p_values,bonferroni_threshold=threshold,raw_acf=m.lag_one_autocorrelation(r),squared_acf=m.lag_one_autocorrelation(squares),overlapping_returns=overlapping,
        hypothetical_per_period_cost=.001,gross_mean=m.sample_mean(r),net_mean=m.sample_mean(net),recommendation='Do not accept a real strategy claim from synthetic fixtures; actual membership, data versions, execution and costs remain unverified')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=12,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
