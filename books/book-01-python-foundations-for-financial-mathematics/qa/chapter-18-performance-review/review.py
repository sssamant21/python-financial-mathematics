"""Section 18.13 source execution and supplemental performance checks."""
from pathlib import Path
from fractions import Fraction
import sys,subprocess,re,tempfile,importlib.util,json,math,random,time,statistics,tracemalloc,platform,hashlib,contextlib,io
ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.13-computational-performance.md'
def run():
    text=subprocess.check_output(['git','-C',str(ROOT),'show',sys.argv[1]+':'+str(SOURCE.relative_to(ROOT))],text=True) if len(sys.argv)>1 else SOURCE.read_text();fences=re.findall(r'~~~python\n(.*?)\n~~~',text,re.S);commands=[];checks=[]
    def verify(name,condition):checks.append(dict(name=name,passed=bool(condition)))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'simulation_performance.py';p.write_text(fences[0])
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import simulation_performance']]:
            result=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr));assert result.returncode==0,commands[-1]
        spec=importlib.util.spec_from_file_location('performance',p);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
        def exact_sample(xs):
            xs=list(map(Fraction,xs));mean=sum(xs)/len(xs);variance=sum((x-mean)**2 for x in xs)/(len(xs)-1);return float(mean),float(variance)
        for xs in [[80,100,120],[100,100],[80,80,100,120],[1e12+1,1e12+2,1e12+3]]:
            s=m.RunningStats()
            for x in xs:s.update(x)
            mean,var=exact_sample(xs)
            verify('sample mean '+repr(xs),math.isclose(s.mean,mean,rel_tol=1e-15))
            verify('sample variance '+repr(xs),math.isclose(s.sample_variance(),var,rel_tol=1e-12))
            verify('sample SE '+repr(xs),math.isclose(s.standard_error(),math.sqrt(var/len(xs)),rel_tol=1e-12))
        for n,b in [(2,1),(101,10),(100,1000),(100,100)]:verify('shared draw replay '+repr((n,b)),m.streaming_run(n,42)==m.run_batches(n,b,42))
        rng=random.Random(42);xs=[]
        for _ in range(10000):
            u=rng.random();xs.append(80 if u<.25 else 100 if u<.75 else 120)
        mean,var=exact_sample(xs);s=m.streaming_run(10000,42)
        verify('sample count',s.count==10000);verify('count-derived sample mean',math.isclose(s.mean,mean,rel_tol=1e-13));verify('count-derived sample variance',math.isclose(s.sample_variance(),var,rel_tol=1e-12))
        verify('bytes exact',m.array_bytes(100000,253,8)==202400000);verify('MiB rounding',round(202400000/2**20,1)==193.0);verify('partial partition',divmod(101,10)==(10,1));verify('full partition',100000//10000==10)
        verify('model expectation',Fraction(80,4)+Fraction(100,2)+Fraction(120,4)==100);verify('model variance',Fraction(400,4)+Fraction(400,4)==200);verify('fourfold SE',math.sqrt(200/40000)==math.sqrt(200/10000)/2)
        for fn,args in [(m.streaming_run,(True,42)),(m.streaming_run,(2,True)),(m.run_batches,(2,False,42)),(m.run_batches,(1,1,42)),(m.array_bytes,(1,True,8)),(m.RunningStats().update,(float('inf'),)),(m.RunningStats().update,(True,))]:
            try:fn(*args);ok=False
            except ValueError:ok=True
            verify('reject '+repr(args),ok)
        times=[]
        for _ in range(5):
            begin=time.perf_counter();m.streaming_run(10000,42);times.append(time.perf_counter()-begin)
        peaks=[]
        for n in [1000,10000,100000]:
            tracemalloc.start();m.streaming_run(n,42);current,peak=tracemalloc.get_traced_memory();tracemalloc.stop();peaks.append(dict(count=n,current=current,peak=peak))
        optional=subprocess.run([sys.executable,'-c',fences[1]],capture_output=True,text=True);commands.append(dict(args=['python','-c','exact NumPy fence'],returncode=optional.returncode,stdout=optional.stdout,stderr=optional.stderr));assert optional.returncode==0,commands[-1]
        import numpy as np
        config=io.StringIO()
        with contextlib.redirect_stdout(config):np.show_config()
        observations=[]
        for name,values in [('opposite-extremes',[-1e308,1e308]),('m2-overflow',[1e200,-1e200]),('huge-integer',[10**1000])]:
            obj=m.RunningStats()
            try:
                for x in values:
                    before=repr(obj);obj.update(x)
                result=repr(obj)
            except Exception as e:result=type(e).__name__+': '+str(e)
            observations.append(dict(name=name,result=result,state=repr(obj),previous_state=before))
            verify(name+' normalized rejection',result.startswith('ValueError:'))
            verify(name+' rejected update preserves state',repr(obj)==before)
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),source_revision=sys.argv[1] if len(sys.argv)>1 else 'candidate manuscript SHA256 below',source_sha256=hashlib.sha256(text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),cpu=platform.processor(),numpy_version=np.__version__,numpy_configuration=config.getvalue(),commands=commands,supplemental_predicates=checks,existing_unique_methods=12,new_historical_methods=0,independent_expectations=dict(model_mean=100,model_variance=200,sample_mean=mean,sample_variance=var,sample_SE=math.sqrt(var/10000),standardized_mean_deviation=(s.mean-100)/s.standard_error()),timing=dict(samples=times,median=statistics.median(times),range=[min(times),max(times)],setup='fresh RNG and accumulator included; import excluded;10000 paths,seed42'),python_traced_allocations=peaks,initial_range_observations=observations,limits='Candidate Linux execution; traced Python allocations exclude native NumPy memory/RSS and do not certify asymptotic memory or speedups. Source selected by retained SHA256. No independent statistical/platform acceptance.')
        (Path(__file__).parent/('baseline-replay.json' if len(sys.argv)>1 else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in checks);print(len(checks),'supplemental predicates;4 source commands;12 existing unique methods passed')
if __name__=='__main__':run()
