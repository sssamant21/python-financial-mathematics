"""Exact companion plus traced rerun; independent prompt-derived QA oracles."""
import contextlib,hashlib,io,json,os,platform,re,subprocess,sys,tempfile,types,unittest
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    source=BOOK/'chapter-08/8.14-solutions-and-reference-implementations.md'
    prompt=BOOK/'chapter-08/8.14-exercises-and-applied-problems.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(problem,label,ok,**detail):checks.append(dict(problem=problem,label=label,passed=bool(ok),**detail))
    with tempfile.TemporaryDirectory(prefix='chapter08-answers-') as tmp:
        lab=Path(tmp);path=lab/'chapter08_solutions.py';path.write_bytes(code)
        for label,args in [('original reference suite',['chapter08_solutions.py']),('original compilation',['-m','compileall','-q','chapter08_solutions.py'])]:
            r=subprocess.run([sys.executable,'-B','-W','error::FutureWarning',*args],cwd=lab,
                             capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests?',r.stderr);count=int(match[1]) if match else None
            ok=r.returncode==0 and (count==20 and bool(re.search(r'^OK\s*$',r.stderr,re.M)) if label.startswith('original reference') else not(r.stdout or r.stderr))
            commands.append(dict(label=label,args=args,stdout=r.stdout,stderr=r.stderr,returncode=r.returncode,methods=count,passed=ok))
        m=types.ModuleType('exact_companion');exec(compile(code,str(path),'exec'),m.__dict__)
        captured={}
        def trace(frame,event,arg):
            if event=='return' and frame.f_code.co_filename==str(path) and frame.f_code.co_name.startswith('test_'):
                captured[int(frame.f_code.co_name.split('_')[1])]=frame.f_locals.copy()
            return trace
        previous=sys.gettrace();stream=io.StringIO()
        try:
            sys.settrace(trace)
            observer=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.Chapter08Solutions))
        finally:sys.settrace(previous)
        ck('ALL','observer rerun same20 methods and captures',observer.wasSuccessful() and observer.testsRun==20 and len(captured)==20)
        c=captured
        ck(1,'indexed values from per-column rational bases',np.array_equal(c[1]['indexed'],[[100,100],[110,80],[120,120]]))
        ck(2,'upper Axes owns line and vertical Axis',c[2]['line'].axes is c[2]['axes'][0,0] and c[2]['axes'].shape==(2,1))
        ck(3,'observed coordinate spacing',np.array_equal(c[3]['line'].get_xdata(),[0,1,4]))
        ck(4,'dropped point does not preserve unknown slot',c[4]['dropped'].get_xdata().tolist()==[0,1,3] and np.isnan(c[4]['retained'].get_ydata()[2]))
        ck(5,'post-step first vertices are exact held states',np.array_equal(c[5]['line'].get_path().vertices[:3],[[0,10],[1,10],[1,12]]))
        ck(6,'UTC instants differ one hour independent of local labels',(c[6]['stamps'][1]-c[6]['stamps'][0]).total_seconds()==3600)
        ck(7,'independent row and cell counts',c[7]['present'].tolist()==[True,False,True] and c[7]['aligned'].notna().sum(axis=1).tolist()==[2,0,1])
        ck(8,'rational gross product and log reconstruction',np.allclose(c[8]['r'],[float(F(110,100)-1),float(F(99,110)-1)],atol=1e-12,rtol=0) and abs(np.expm1(c[8]['logs'].sum())-float(F(99,100)-1))<1e-12)
        ck(9,'full strict path including baseline and unrestarted gap',np.allclose(c[9]['linked'],[0,.1,-.01,np.nan,np.nan,np.nan],atol=1e-12,rtol=0,equal_nan=True))
        nums=[-8,-4,-2,-1,0,0,1,2,3,4,10];edges=[-10,-2,0,2,10]
        counts=[sum(a<=x and (x<b or (i==3 and x==b)) for x in nums) for i,(a,b) in enumerate(zip(edges,edges[1:]))]
        ck(10,'scalar bin assignment',c[10]['counts'].tolist()==counts)
        widths=[F(b-a,100) for a,b in zip(edges,edges[1:])]
        ck(11,'rational densities and areas',np.allclose(c[11]['density'],[float(F(n,11)/w) for n,w in zip(counts,widths)],atol=1e-12,rtol=0) and sum(F(n,11) for n in counts)==1)
        ck(12,'manual label pair map',c[12]['pairs'].index.day.tolist()==[1,3,4] and np.allclose(c[12]['pairs'],[[.01,.015],[0,0],[-.01,-.02]],atol=1e-12,rtol=0))
        ck(13,'affine y values not equality',np.allclose(c[13]['y'],[-.03,.01,.03,.07],atol=1e-12,rtol=0))
        ck(14,'integer denominators and rational exposure shares',(c[14]['net'],c[14]['absolute'])==(1000,1400) and np.allclose(c[14]['shares'],[float(x) for x in [F(3,7),F(2,7),F(1,7),F(1,7)]],atol=1e-12,rtol=0))
        ck(15,'complete call and put payoff oracles',c[15]['call'].tolist()==[0,0,0,600,2000] and c[15]['put'].tolist()==[10000,400,0,0,0])
        with localcontext() as ctx:
            ctx.prec=60;one=Decimal(1);r=Decimal('.05')
            annual=Decimal(1000)*(one+r)**20
            monthly=Decimal(1000)*(one+r/12)**240
            nominal=12*((one+r)**(one/12)-one);continuous=(one+r).ln()
        ck(16,'independent high-precision rates and endpoints',
           abs(c[16]['annual']-float(annual))<1e-9 and abs(c[16]['monthly_same_number']-float(monthly))<1e-9 and
           abs(c[16]['equivalent_nominal']-float(nominal))<1e-14,
           annual=str(annual),monthly=str(monthly),nominal=str(nominal),continuous=str(continuous))
        oracle=np.array([[float(1000*F(100+r,100)**n) for n in [5,10,15,20]] for r in [1,3,5,7,9]])
        ck(17,'entire grid and joint difference',np.allclose(c[17]['grid'],oracle,atol=1e-8,rtol=0) and abs(c[17]['joint']-c[17]['reference']-float(1000*F(107,100)**12-1000*F(105,100)**10))<1e-9)
        ck(18,'correct label order zero and hatch',c[18]['known'].index.tolist()==['D','A','C','B'] and c[18]['bars'][2].get_width()==0 and c[18]['bars'][-1].get_hatch()=='//')
        ck(19,'plotted balance oracle and cleanup',np.array_equal(c[19]['line'].get_ydata(),[100,105,110.25]) and set(m.plt.get_fignums())==c[19]['before'])
        ck(20,'mini fixture only: five cells one complete pair null result',
           (c[20]['report']['observed'],c[20]['report']['expected'],c[20]['report']['complete_pairs'],c[20]['report']['A_final_strict'])==(5,6,1,None))
        # Explicit Problem20 integration task, independently extracted from project source.
        project_path=BOOK/'chapter-08/8.13-chapter-project-financial-analytics-dashboard.md'
        pblocks=re.findall(rb'^```python\n(.*?)^```',project_path.read_bytes(),re.M|re.S)
        project_dir=lab/'integration';project_dir.mkdir()
        for name,body in zip(('dashboard.py','test_dashboard.py'),pblocks[:2]):
            (project_dir/name).write_bytes(body)
        # The original suite supplies its own fixture; no prices.csv is imported.
        run=subprocess.run([sys.executable,'-B','-W','error::FutureWarning','-m','unittest','-v'],
                           cwd=project_dir,capture_output=True,text=True,timeout=120)
        match=re.search(r'Ran (\d+) tests?',run.stderr);methods=int(match[1]) if match else None
        commands.append(dict(label='Problem20 separate original project integration suite',
                             args=['-m','unittest','-v'],stdout=run.stdout,stderr=run.stderr,
                             returncode=run.returncode,methods=methods,
                             passed=run.returncode==0 and methods==16 and bool(re.search(r'^OK\s*$',run.stderr,re.M))))
        # QA labels and exports for the figure exercises; source tests remain unchanged.
        for problem in (2,3,4,5,18,19):
            fig=c[problem]['fig']
            for ax in fig.axes:
                if problem in (2,3,4):ax.set(xlabel='Elapsed days' if problem!=2 else 'Observation coordinate',
                                            ylabel='Illustrative value')
                elif problem==5:ax.set(xlabel='Elapsed days',ylabel='Units held')
                elif problem==18:ax.set(xlabel='Simple price return over common interval',ylabel='Asset')
            fig.suptitle('QA display of source figure: Problem '+str(problem))
            fig.savefig(HERE/('problem-'+str(problem)+'.png'),dpi=120)
        prior=HERE.parent/'chapter-08-dashboard-review/results.json'
        evidence=json.loads(prior.read_text())
        project=BOOK/'chapter-08/8.13-chapter-project-financial-analytics-dashboard.md'
        ck(20,'prior real project integration remains exact-source applicable',
           evidence['source_sha256']==sha(project.read_bytes()) and all(x['passed'] for x in evidence['commands']+evidence['checks']),
           evidence='../chapter-08-dashboard-review/README.md',scope='Earlier batch integration,not rerun here')
        (HERE/'observer.log').write_text(stream.getvalue())
    out=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,matplotlib=m.matplotlib.__version__,
             platform=platform.platform(),source_sha256=sha(source.read_bytes()),prompt_sha256=sha(prompt.read_bytes()),
             listing_sha256=sha(code),commands=commands,checks=checks,observer_methods=observer.testsRun,
             historical_unique_methods_added=0,source_method_invocations_this_batch=56)
    (HERE/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks))
    return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
