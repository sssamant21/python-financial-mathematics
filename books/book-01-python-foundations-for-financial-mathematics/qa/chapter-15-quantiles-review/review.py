"""Section 15.2 exact quantile lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.02-mean-median-and-quantiles.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1502-') as tmp:
        Path(tmp,'mean_median_quantiles.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['mean_median_quantiles.py']),('isolated import',['-c','import mean_median_quantiles']),('exact compilation',['-m','compileall','-q','mean_median_quantiles.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['mean_median_quantiles.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('quantiles');exec(compile(code,str(source),'exec'),m.__dict__)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    x=[-.04,-.01,0,.02,.08]
    for label,fn,want in [
        ('E1 mean',lambda:m.arithmetic_mean(x),F(1,100)),
        ('E2 odd median',lambda:m.median(x),0),
        ('E3 even median',lambda:m.median([-.04,-.01,.02,.08]),F(1,200)),
        ('E4 minimum',lambda:m.quantile_type7(x,0),F(-4,100)),
        ('E5 maximum',lambda:m.quantile_type7(x,1),F(8,100)),
        ('E6 Q1',lambda:m.quantile_type7(x,.25),F(-1,100)),
        ('E7 Q3',lambda:m.quantile_type7(x,.75),F(2,100)),
        ('E8 IQR',lambda:m.quantile_type7(x,.75)-m.quantile_type7(x,.25),F(3,100)),
        ('E9 interpolation',lambda:m.quantile_type7([0,10,20,30],.25),F(15,2)),
        ('E10 nearest rank',lambda:m.nearest_rank_quantile([0,10,20,30],.25),0),
        ('E11 median equivalence',lambda:m.quantile_type7(x,.5),0),
        ('E12 strict downside',lambda:m.downside_fraction(x),F(2,5)),
        ('E13 outlier mean',lambda:m.arithmetic_mean([.01,.02,.03,.2]),F(13,200)),
        ('E13 outlier median',lambda:m.median([.01,.02,.03,.2]),F(1,40)),
        ('E14 trimmed',lambda:m.trimmed_mean([.01,.02,.03,.2],1),F(1,40)),
        ('E15 weighted',lambda:m.weighted_mean([.02,.08],[.75,.25]),F(7,200)),
        ('E16 unequal weights',lambda:m.weighted_mean([.01,.03,.05],[1,2,1]),F(3,100)),
        ('E19 stress mean',lambda:m.arithmetic_mean(x[:-1]+[.28]),F(1,20)),
        ('E20 stress median',lambda:m.median(x[:-1]+[.28]),0),
        ('E22 Q05',lambda:m.quantile_type7(x,.05),F(-17,500)),
        ('E23 Q95',lambda:m.quantile_type7(x,.95),F(17,250)),
        ('E24 stylized loss',lambda:-100000*m.quantile_type7(x,.05),3400),
        ('F128 large mean',lambda:m.arithmetic_mean([1e308,1e308]),1e308),
        ('F128 large even median',lambda:m.median([1e308,1e308]),1e308),
        ('F128 large trimmed mean',lambda:m.trimmed_mean([1e308]*4,1),1e308),
        ('F128 opposite extreme interpolation',lambda:m.quantile_type7([-1e308,1e308],.5),0),
        ('F128 extreme endpoint',lambda:m.quantile_type7([-1e308,1e308],0),-1e308),
        ('F128 weighted product overflow',lambda:m.weighted_mean([1e308,1e308],[2,2]),1e308),
        ('F128 weight sum overflow',lambda:m.weighted_mean([1,3],[1e308,1e308]),2),
        ('F128 exact nearest-rank boundary',lambda:m.nearest_rank_quantile(list(range(100)),.14),13),
    ]:num(label,fn,want)
    a=10**18
    ck('F128 integer order preserved',m.clean([a+2,a])==[a,a+2])
    ck('F128 integer ranked value preserved',m.nearest_rank_quantile([a,a+2],1)==a+2)
    for name,fn in [('mean',m.arithmetic_mean),('median',m.median),('quantile',lambda z:m.quantile_type7(z,.3))]:
        close('E17 shift '+name,fn([v+.02 for v in x]),fn(x)+.02)
        close('E18 scale '+name,fn([v*100 for v in x]),fn(x)*100)
    for label,fn in [
        ('E21 missing rejected',lambda:m.arithmetic_mean([None,.01])),
        ('empty rejected',lambda:m.median([])),
        ('boolean rejected',lambda:m.quantile_type7([True,1],.5)),
        ('nonfinite rejected',lambda:m.median([math.inf])),
        ('bad probability rejected',lambda:m.quantile_type7(x,math.nan)),
        ('nearest-rank zero rejected',lambda:m.nearest_rank_quantile(x,0)),
        ('trim all rejected',lambda:m.trimmed_mean([1,2],1)),
        ('negative weight rejected',lambda:m.weighted_mean([1],[-1])),
        ('zero weights rejected',lambda:m.weighted_mean([1],[0])),
        ('weight mismatch rejected',lambda:m.weighted_mean([1,2],[1])),
    ]:reject(label,fn)
    ck('source input unchanged',x==[-.04,-.01,0,.02,.08])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=24,
             mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,
             project_report=dict(source_returns=x,dates=None,frequency='not supplied; hypothetical common period',units='decimal simple returns',
                fixture_sha256=hashlib.sha256(json.dumps(x).encode()).hexdigest(),quantile_method='type 7',missing_policy='reject; filtering must be disclosed upstream',
                weighted_fixture_returns=[.02,.08],weighted_fixture_weights=[.75,.25],
                mean=m.arithmetic_mean(x),median=m.median(x),quantiles={str(p):m.quantile_type7(x,p) for p in [.05,.25,.5,.75,.95]},
                iqr=m.quantile_type7(x,.75)-m.quantile_type7(x,.25),negative_fraction=m.downside_fraction(x),
                nearest_q25=m.nearest_rank_quantile(x,.25),stress_mean=m.arithmetic_mean(x[:-1]+[.28]),stress_median=m.median(x[:-1]+[.28]),
                weighted_mean=m.weighted_mean([.02,.08],[.75,.25])))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
