"""Section 15.4 exact shape lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-15/15.04-skewness-and-kurtosis.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1504-') as tmp:
        Path(tmp,'skewness_kurtosis.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['skewness_kurtosis.py']),('isolated import',['-c','import skewness_kurtosis']),('exact compilation',['-m','compileall','-q','skewness_kurtosis.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['skewness_kurtosis.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('shape');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80
            return (D(v.numerator)/D(v.denominator)).sqrt()
    def oracle(values):
        xs=[F(str(x)) for x in values];n=len(xs);mu=sum(xs)/n
        # Raw-moment expansion, independent of source centered-power algorithm.
        raw={k:sum(v**k for v in xs)/n for k in range(1,5)}
        m2=raw[2]-mu**2;m3=raw[3]-3*mu*raw[2]+2*mu**3
        m4=raw[4]-4*mu*raw[3]+6*mu**2*raw[2]-3*mu**4
        g1=float(root(m3*m3/m2**3))*(1 if m3>=0 else -1)
        kurt=m4/m2**2;ex=kurt-3
        return dict(n=n,mean=mu,m2=m2,skewness=g1,kurtosis=kurt,excess_kurtosis=ex),dict(m3=m3,m4=m4)
    def num(label,fn,want):
        try:value=fn()
        except Exception as exc:ck(label,False,exception=repr(exc))
        else:close(label,value,want,atol=0)
    x=[-.04,-.01,0,.02,.08]
    report,central=oracle(x)
    for k,v in report.items():num('project '+k,lambda k=k:m.standardized_moments(x)[k],v)
    n=5
    num('project adjusted skew',lambda:m.adjusted_sample_skewness(x),report['skewness']*float(root(F(n*(n-1),(n-2)**2))))
    num('project adjusted excess',lambda:m.adjusted_sample_excess_kurtosis(x),F(n-1,(n-2)*(n-3))*((n+1)*report['excess_kurtosis']+6))
    for label,values in [('E1-E9 symmetric',[-1,0,1]),('E4 right skew',[0,0,0,4]),('E5 left skew',[-4,0,0,0]),('project positive stress',[-.04,-.01,0,.02,.28]),('project negative stress',[-.24,-.01,0,.02,.08])]:
        want,_=oracle(values)
        for key in ['skewness','kurtosis','excess_kurtosis']:
            num(label+' '+key,lambda key=key,values=values:m.standardized_moments(values)[key],want[key])
    for label,values in [('F130 integer offset',[10**18,10**18+1,10**18+2,10**18+5]),('F130 large fourth power',[0,0,0,1e100]),('F130 small fourth power',[0,0,0,1e-100])]:
        want,_=oracle(values)
        for key in ['skewness','kurtosis','excess_kurtosis']:
            num(label+' '+key,lambda key=key,values=values:m.standardized_moments(values)[key],want[key])
    for label,values,sign in [('E10 shifted',[10+v for v in [0,0,0,4]],1),('E11 scaled',[0,0,0,8],1),('E12 reflected',[-4,0,0,0],-1)]:
        num(label+' skew',lambda values=values:m.standardized_moments(values)['skewness'],sign*float(root(F(4,3))))
        num(label+' kurt',lambda values=values:m.standardized_moments(values)['kurtosis'],F(7,3))
    num('E18 downside',lambda:m.downside_frequency([-.03,-.01,.01,.02]),F(1,2))
    num('E23 adjusted n4',lambda:m.adjusted_sample_excess_kurtosis([0,0,0,4]),4)
    for label,fn in [
        ('E15 constant undefined',lambda:m.standardized_moments([2,2,2])),
        ('E16 adjusted skew n2',lambda:m.adjusted_sample_skewness([1,2])),
        ('E17 adjusted excess n3',lambda:m.adjusted_sample_excess_kurtosis([1,2,3])),
        ('empty rejected',lambda:m.standardized_moments([])),
        ('boolean rejected',lambda:m.standardized_moments([True,2])),
        ('nonfinite rejected',lambda:m.standardized_moments([math.inf,2])),
        ('threshold rejected',lambda:m.downside_frequency(x,math.nan)),
        ('F130 unreportable required variance rejected',lambda:m.standardized_moments([-1e308,1e308])),
    ]:reject(label,fn)
    ck('project input unchanged',x==[-.04,-.01,0,.02,.08])
    # Project comparison metrics are supplemental rational/order-statistic calculations.
    ordered=sorted(map(F,('-.04','-.01','0','.02','.08')))
    project=dict(source_returns=x,frequency=None,instrument='fictional strategy',units='decimal simple returns',source='synthetic manuscript fixture',
        fixture_sha256=hashlib.sha256(json.dumps(x).encode()).hexdigest(),source_report=m.standardized_moments(x),
        supplemental_m3=str(central['m3']),supplemental_m4=str(central['m4']),
        supplemental_population_sd=str(root(report['m2'])),supplemental_median=str(ordered[2]),supplemental_type7_q05=str(F(4,5)*ordered[0]+F(1,5)*ordered[1]),
        source_adjusted_skew=m.adjusted_sample_skewness(x),source_adjusted_excess=m.adjusted_sample_excess_kurtosis(x),
        positive_stress=m.standardized_moments([-.04,-.01,0,.02,.28]),negative_stress=m.standardized_moments([-.24,-.01,0,.02,.08]))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,
        workflow_records=1,local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0,project_report=project)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
