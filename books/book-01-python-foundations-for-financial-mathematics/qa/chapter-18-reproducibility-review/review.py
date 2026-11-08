"""Verbatim reproducibility source, separate arithmetic/hash and design probes."""
import hashlib,json,math,platform,random,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.03-reproducible-simulation.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);fences=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S);commands=[];checks=[]
    def ck(label,fn,expected=True):
        try:actual=fn();ok=actual==expected
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=expected,passed=bool(ok)))
    def rejects(fn):
        try:fn()
        except ValueError:return True
        except Exception as e:return type(e).__name__
        return False
    with tempfile.TemporaryDirectory(prefix='book1-1803-') as tmp:
        for i,code in enumerate(fences):
            name='reproducible_simulation.py' if i==len(fences)-1 else f'example{i+1}.py';Path(tmp,name).write_bytes(code)
            p=subprocess.run([sys.executable,'-B',name],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr)
            commands.append(dict(label=f'exact fence {i+1}',args=[name],stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,existing_methods=int(methods[1]) if methods else 0,passed=p.returncode==0 and (i!=len(fences)-1 or bool(methods and int(methods[1])==10 and re.search(r'^OK\s*$',p.stderr,re.M)))))
        for args in [['-c','import reproducible_simulation'],['-m','compileall','-q','reproducible_simulation.py']]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);commands.append(dict(label='exact module check',args=args,stdout=p.stdout,stderr=p.stderr,returncode=p.returncode,existing_methods=0,passed=p.returncode==0 and not(p.stdout or p.stderr)))
    m=types.ModuleType('repro_lab');exec(compile(fences[-1],str(BOOK/path),'exec'),m.__dict__)
    manifests=[]
    for seed,count,p in [(42,10000,.6),(43,10000,.6),(42,10000,.5),(42,1000,.6)]:
        actual=m.run(seed,count,p);r=random.Random(seed);k=sum(F.from_float(r.random())<F(str(p)) for _ in range(count));expected_mean=F(90)+F(20*k,count)
        ck('shared-generator count '+str((seed,count,p)),lambda actual=actual,k=k:actual['up_count']==k)
        ck('rational mean '+str((seed,count,p)),lambda actual=actual,expected_mean=expected_mean:actual['mean']==float(expected_mean))
        # Independent encoding oracle: field order explicitly listed, not source canonical_json.
        encoded='{'+','.join(json.dumps(k)+':'+json.dumps(actual[k],ensure_ascii=True,allow_nan=False,separators=(',',':')) for k in sorted(actual))+'}'
        ck('canonical bytes '+str((seed,count,p)),lambda actual=actual,encoded=encoded:m.canonical_json(actual)==encoded)
        digest=hashlib.sha256(encoded.encode('utf-8')).hexdigest()
        ck('digest of independently encoded fields '+str((seed,count,p)),lambda actual=actual,digest=digest:m.manifest_digest(actual)==digest)
        manifests.append(dict(manifest=actual,canonical=encoded,digest=digest,analytical_mean=str(F(90)+20*F(str(p))),limit='count replay uses the same generator; rational summary/hash checks do not establish statistical independence'))
    base=m.run(42,10000,.6)
    ck('identical manifest replay',lambda:m.run(42,10000,.6)==base)
    ck('identical digest replay',lambda:m.manifest_digest(m.run(42,10000,.6))==m.manifest_digest(base))
    ck('input change seed changes fields/digest',lambda:m.manifest_digest(base)!=m.manifest_digest(m.run(43,10000,.6)))
    ck('input change probability changes fields/digest',lambda:m.manifest_digest(base)!=m.manifest_digest(m.run(42,10000,.5)))
    ck('input change count changes fields/digest',lambda:m.manifest_digest(base)!=m.manifest_digest(m.run(42,1000,.6)))
    ck('ideal mean E7 independent rational',lambda:F(3,5)*110+F(2,5)*90==102)
    ck('ideal mean E8 independent rational',lambda:F(110+90,2)==100)
    ck('all-up source',lambda:m.run(1,10,1)['mean']==110)
    ck('all-down source',lambda:m.run(1,10,0)['mean']==90)
    state=random.getstate();m.run(42,20,.6);ck('local generator preserves global state',lambda:random.getstate()==state)
    r=random.Random(42);saved=r.getstate();a=[r.random() for _ in range(20)];r.setstate(saved);ck('restore complete selected stream',lambda:[r.random() for _ in range(20)]==a)
    r=random.Random(42);r.random();shifted=[r.random() for _ in range(20)];ck('extra draw shifts selected sequence',lambda:shifted[:-1]==a[1:] and shifted!=a)
    ck('reset-per-path duplicates first draws',lambda:len({random.Random(42).random() for _ in range(20)})==1)
    for actual,reference,atol,rtol in [(100.01,100,.02,0),(100.02,100,.01,0),(1.1,1,.1,0),(-1.1,-1,.1,0),(1.2,1,.1,.1),(1.79e308,-1.79e308,1e308,1),(5e-324,1e-323,0,.4),(1e-10,0,1e-10,0),(1e-10,0,0,1e-3),(100.11,100,.01,.001),(0,0,0,0)]:
        a,b,c,d=map(lambda x:F(x) if type(x) is int else F(str(x)),(actual,reference,atol,rtol));want=abs(a-b)<=c+d*abs(b)
        ck('displayed-decimal additive tolerance '+str((actual,reference,atol,rtol)),lambda actual=actual,reference=reference,atol=atol,rtol=rtol:m.within_tolerance(actual,reference,atol,rtol),want)
    for label,fn in [('probability huge int',lambda:m.run(1,2,10**1000)),('probability bool',lambda:m.run(1,2,True)),('probability outside',lambda:m.run(1,2,1.1)),('seed bool',lambda:m.run(True,2,.5)),('count bool',lambda:m.run(1,True,.5)),('count1',lambda:m.run(1,1,.5)),('probability nan',lambda:m.run(1,2,float('nan'))),('comparator huge int',lambda:m.within_tolerance(10**1000,1,0,0)),('comparator bool',lambda:m.within_tolerance(True,1,0,0)),('negative tolerance',lambda:m.within_tolerance(1,1,-.1,0)),('nonfinite comparator',lambda:m.within_tolerance(float('inf'),1,0,0)),('nonfinite manifest',lambda:m.canonical_json({'x':float('nan')}))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    ck('key insertion order digest stable',lambda:m.manifest_digest({'b':2,'a':1})==m.manifest_digest({'a':1,'b':2}))
    ck('literal manifest encoding oracle',lambda:m.canonical_json({'b':2,'a':1})=='{"a":1,"b":2}')
    ck('known SHA256 empty object oracle',lambda:m.manifest_digest({})=='44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a')
    ck('encoding distinguishes int and float',lambda:m.manifest_digest({'x':1})!=m.manifest_digest({'x':1.0}))
    ck('adding timestamp changes manifest identity',lambda:m.manifest_digest({'run':1,'timestamp':'a'})!=m.manifest_digest({'run':1,'timestamp':'b'}))
    ck('reduction-order illustration',lambda:(1e16+(-1e16))+1!=1e16+((-1e16)+1))
    # Supplemental paired-outcome algebra, not a source paired-SE implementation.
    x=[F(110),F(90),F(110),F(90)];y=[F(120),F(100),F(120),F(100)];diff=[b-a for a,b in zip(x,y)];mean=sum(diff)/4
    ck('paired differences constant mean10',lambda:mean==10)
    ck('paired variance zero',lambda:sum((d-mean)**2 for d in diff)/3==0)
    ck('independent-estimates variance differs',lambda:sum((a-100)**2 for a in x)/3+sum((b-110)**2 for b in y)/3>0)
    import numpy as np
    children=np.random.SeedSequence(42).spawn(2);draws=[np.random.default_rng(c).random(5).tolist() for c in children]
    ck('spawn chosen child draws differ',lambda:draws[0]!=draws[1])
    ck('spawn fixed assignment replay',lambda:draws==[np.random.default_rng(c).random(5).tolist() for c in np.random.SeedSequence(42).spawn(2)])
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=[hashlib.sha256(c).hexdigest() for c in fences],python=platform.python_version(),python_implementation=platform.python_implementation(),platform=platform.platform(),numpy=np.__version__,bit_generator='PCG64',commands=commands,checks=checks,manifests=manifests,children=[dict(task=i,spawn_key=list(c.spawn_key),draws=draws[i]) for i,c in enumerate(children)],counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=10,new_historical_methods=0),limits='Source manifest has no external dataset, code checksum or financial conventions: QA source hashes and fictional-model contract supplement it. No production audit completeness, portable JSON canonicalization standard, cross-platform bitwise replay or independent statistical/model acceptance.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
