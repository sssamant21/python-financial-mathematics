"""Exact simulation source; analytical moments separate from shared-generator replay."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.01-simulation-fundamentals.md';source=BOOK/path
    data=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path])
    code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def num(label,fn,want,atol=0,rtol=1e-12):
        try:v=fn();ok=math.isclose(v,float(want),abs_tol=atol,rel_tol=rtol)
        except Exception as e:ck(label,False,exception=repr(e),reference=str(want));return
        ck(label,ok,actual=v,reference=str(want),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:v=fn()
        except Exception as e:ck(label,isinstance(e,ValueError),exception=repr(e),expected_exception='ValueError')
        else:ck(label,False,actual=repr(v),expected_exception='ValueError')
    def sqrt(q):
        q=F(q)
        with localcontext() as ctx:ctx.prec=200;return (D(q.numerator)/D(q.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1801-') as tmp:
        Path(tmp,'simulation_fundamentals.py').write_bytes(code)
        for label,args in [('exact demonstration and ten methods',['simulation_fundamentals.py']),('silent import',['-c','import simulation_fundamentals']),('compile exact listing',['-m','compileall','-q','simulation_fundamentals.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None;ok=p.returncode==0
            if label=='exact demonstration and ten methods':ok=ok and methods==10 and bool(re.search(r'^OK\s*$',p.stderr,re.M))
            else:ok=ok and not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=ok))
    m=types.ModuleType('simulation_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    sample=m.summarize([110,90,110,110],100)
    for label,fn,want in [
      ('E9 known sample mean',lambda:sample['mean'],105),
      ('E10 known loss frequency',lambda:sample['loss_frequency'],F(1,4)),
      ('known sample SD',lambda:sample['sample_sd'],10),
      ('known sample standard error',lambda:sample['standard_error'],5),
      ('E8 analytical model mean supplemental',lambda:F(1,2)*110+F(1,2)*90,100),
      ('E12 analytical changed probability mean supplemental',lambda:F(3,5)*110+F(2,5)*90,102),
      ('E16 analytical model variance supplemental',lambda:F(1,2)*(110-100)**2+F(1,2)*(90-100)**2,100),
      ('E17 theoretical SE supplemental',lambda:F(10,100),F(1,10)),
      ('E13 source discount',lambda:m.discounted(110,.1),100),
      ('E14 source discounted expectation',lambda:m.discounted(100,.1),F(1000,11)),
      ('E34 constant sample SE',lambda:m.summarize([100,100],100)['standard_error'],0),
      ('E35 equality is not loss',lambda:m.summarize([100,100],100)['loss_frequency'],0),
      ('E36 supplemental compound value',lambda:F(100)*F(11,10)*F(9,10),99),
    ]:num(label,fn,want)
    streams=[]
    for count,seed,p in [(1000,42,.5),(1000,43,.5),(10000,42,.5),(1000,42,.6)]:
        actual=m.simulate_values(100,.1,-.1,p,count,seed);summary=m.summarize(actual,100)
        rng=random.Random(seed);probability=F(str(p))
        k=sum(F.from_float(rng.random())<probability for _ in range(count))
        expected_mean=F(90)+F(20*k,count);variance=F(400*k*(count-k),count*(count-1))
        num('shared-generator replay mean '+str((count,seed,p)),lambda summary=summary:summary['mean'],expected_mean)
        num('shared-generator replay loss '+str((count,seed,p)),lambda summary=summary:summary['loss_frequency'],F(count-k,count))
        num('exact-count sample SD '+str((count,seed,p)),lambda summary=summary:summary['sample_sd'],sqrt(variance))
        num('exact-count sample SE '+str((count,seed,p)),lambda summary=summary:summary['standard_error'],sqrt(variance/count))
        streams.append(dict(count=count,seed=seed,up_probability=p,up_count=k,summary=summary,sample_sha256=hashlib.sha256(json.dumps(actual,separators=(',',':')).encode()).hexdigest(),oracle_limit='replays same random.Random generator; verifies mapping/arithmetic, not independent randomness/distribution quality'))
    ck('same seed reproduces sequence',m.simulate_values(100,.1,-.1,.5,1000,42)==m.simulate_values(100,.1,-.1,.5,1000,42))
    before=random.getstate();m.simulate_values(100,.1,-.1,.5,20,42);ck('local generator preserves global state',random.getstate()==before)
    ck('chosen alternate seed observed different stream',streams[0]['sample_sha256']!=streams[1]['sample_sha256'],scope='observation for these seeds, not all-seed independence proof')
    ck('E32 all-up outcome',all(math.isclose(x,110,rel_tol=1e-12) for x in m.simulate_values(100,.1,-.1,1,5,1)))
    ck('E33 all-down outcome',all(math.isclose(x,90,rel_tol=1e-12) for x in m.simulate_values(100,.1,-.1,0,5,1)))
    ck('E31 initial200 scaling',all(math.isclose(x,220,rel_tol=1e-12) for x in m.simulate_values(200,.1,-.1,1,5,1)))
    ck('F173 exact integer terminal increment preserved',m.simulate_values(10**18,1e-18,0,1,2,1)==[10**18+1]*2)
    num('F173 unreachable branch overflow not evaluated',lambda:m.simulate_values(1e308,1e308,0,0,2,1)[0],1e308)
    ck('F173 integer summary mean preserved',m.summarize([10**18,10**18+2],10**18)['mean']==10**18+1)
    num('F173 tiny SD remains reportable',lambda:m.summarize([-1e-308,1e-308],0)['sample_sd'],sqrt(F(2,10**616)))
    ck('true total-loss zero remains valid',m.simulate_values(100,-1,0,1,2,1)==[0,0])
    for label,fn in [
      ('invalid probability',lambda:m.simulate_values(100,.1,-.1,1.1,10,1)),
      ('invalid count',lambda:m.simulate_values(100,.1,-.1,.5,1,1)),
      ('invalid return below minus1',lambda:m.simulate_values(100,.1,-1.1,.5,10,1)),
      ('noninteger seed',lambda:m.simulate_values(100,.1,-.1,.5,10,True)),
      ('huge integer input',lambda:m.simulate_values(10**1000,.1,-.1,.5,10,1)),
      ('nonzero terminal underflow',lambda:m.simulate_values(5e-324,-.75,-.75,1,2,1)),
      ('nonfinite sample',lambda:m.summarize([1,float('inf')],0)),
      ('boolean sample',lambda:m.summarize([True,False],0)),
      ('boolean threshold',lambda:m.summarize([1,2],True)),
      ('malformed sample iterable',lambda:m.summarize(None,0)),
      ('malformed sample value',lambda:m.summarize([None,1],0)),
      ('unreportable sample SD',lambda:m.summarize([-1.79e308,1.79e308],0)),
      ('discount underflow',lambda:m.discounted(5e-324,3)),
      ('invalid rate',lambda:m.discounted(100,-1)),
      ('nonfinite rate',lambda:m.discounted(100,float('nan'))),
    ]:reject('F173 '+label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=40,lab_step_records=12,process_control_records=8,historical_unique_methods_added=0,streams=streams,model=dict(initial=100,returns=[.1,-.1],probabilities=[.5,.5],theoretical_mean=100,theoretical_sd=10,theoretical_SE_at10000=.1,loss_definition='terminal < initial',units='fictional common currency, one-year simple returns, annual-effective discount rate.1',timing='one-year terminal outcome; no market/as-of data or measure calibration'),statistical_limits='No requirement that every larger run be closer, no nominal interval coverage test or RNG independence proof; same-generator replay is not an independent statistical reference.')
    def safe(x):
        if isinstance(x,(F,D)):return str(x)
        if isinstance(x,float) and not math.isfinite(x):return repr(x)
        if isinstance(x,dict):return {k:safe(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)):return [safe(v) for v in x]
        return x
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(safe(out),indent=2,allow_nan=False)+'\n');print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
