"""Section 15.1 exact descriptive statistics lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.01-descriptive-statistics.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1501-') as tmp:
        Path(tmp,'descriptive_statistics.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['descriptive_statistics.py']),('isolated import',['-c','import descriptive_statistics']),('exact compilation',['-m','compileall','-q','descriptive_statistics.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['descriptive_statistics.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('descriptive');exec(compile(code,str(source),'exec'),m.__dict__)
    from itertools import combinations
    from decimal import Decimal as D, localcontext
    r=[.02,-.01,.03,0]; points=list(map(F,('.02','-.01','.03','0')))
    mu=sum(points)/4
    sq=sum((a-b)**2 for a,b in combinations(points,2))/4
    expected={'count':4,'mean':mu,'median':mu,'minimum':F('-.01'),'maximum':F('.03'),'range':F('.04'),
              'population_variance':sq/4,'population_sd':math.sqrt(sq/4),'sample_variance':sq/3,
              'sample_sd':math.sqrt(sq/3),'negative_fraction':F(1,4)}
    actual=m.describe(r)
    for k,v in expected.items():close('project '+k,actual[k],v,atol=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    g=math.prod(1+x for x in points)
    with localcontext() as ctx:
        ctx.prec=60
        geo=(D(g.numerator)/D(g.denominator))**(D(1)/4)-1
        two=D('.99').sqrt()-1
    for label,fn,want in [
        ('E8 percentage-point population variance',lambda:m.describe([2,-1,3,0])['population_variance'],F(5,2)),
        ('E9 percentage-point sample variance',lambda:m.describe([2,-1,3,0])['sample_variance'],F(10,3)),
        ('E15 two-period geometric mean',lambda:m.geometric_mean_return([.1,-.1]),two),
        ('E16 two-period cumulative loss',lambda:m.compounded_return([.1,-.1]),F('-.01')),
        ('E17 outlier mean',lambda:m.describe([.01,.02,.03,.2])['mean'],F('.065')),
        ('E17 outlier median',lambda:m.describe([.01,.02,.03,.2])['median'],F('.025')),
        ('E22 shift preserves dispersion',lambda:m.describe([x+.01 for x in r])['sample_sd'],math.sqrt(sq/3)),
        ('project cumulative return',lambda:m.compounded_return(r),g-1),
        ('project geometric mean',lambda:m.geometric_mean_return(r),geo),
        ('F127 mean despite oversized sum',lambda:m.describe([1e308,1e308])['mean'],1e308),
        ('F127 small spread at integer offset',lambda:m.describe([10**18,10**18+2])['sample_variance'],2),
        ('F127 tiny cumulative gain',lambda:m.compounded_return([1e-18]),F('1e-18')),
        ('F127 true total loss after extreme growth',lambda:m.compounded_return([1e308,1e308,-1]),-1),
    ]:num(label,fn,want)
    single=m.describe([5])
    ck('E20 single sample undefined and population zero',single['sample_sd'] is None and single['sample_variance'] is None and single['population_sd']==0)
    ck('E13/E14 sign frequencies',sum(x>0 for x in r)/4==.5 and r.count(0)/4==.25)
    for label,fn in [
        ('E19 missing value rejected',lambda:m.describe([.1,None])),
        ('nonfinite value rejected',lambda:m.describe([.1,math.nan])),
        ('invalid long-only return',lambda:m.compounded_return([-1.01])),
        ('F127 false total loss rejected',lambda:m.compounded_return([-.99]*10)),
        ('F127 unreportable variance rejected',lambda:m.describe([-1e308,1e308])),
    ]:reject(label,fn)
    import ast
    reported=ast.literal_eval(commands[0]['stdout'].split(': ',1)[1].strip())
    ck('exact demo output equals report',reported==actual)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=24,
             mini_project_records=1,mini_project_deliverable_records=6,historical_unique_methods_added=0,
             project_report=dict(instrument='Fictional strategy, synthetic four-observation fixture',dates=None,
                                 frequency='hypothetical daily',units='decimal simple returns',currency='unspecified',adjustment_policy='no price data; supplied return fixture',
                                 source_returns=r,summary=actual,cumulative=m.compounded_return(r),geometric=m.geometric_mean_return(r)))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
