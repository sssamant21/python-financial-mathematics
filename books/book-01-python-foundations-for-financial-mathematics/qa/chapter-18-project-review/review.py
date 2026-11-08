from pathlib import Path
from fractions import Fraction
import re,sys,subprocess,hashlib,tempfile,importlib.util,json,math,platform
ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.14-chapter-project-monte-carlo-financial-simulator.md'
def number(x):return Fraction(x) if type(x) is int else Fraction(str(x))
def oracle(losses,alpha):
    xs=sorted(map(number,losses));alpha=number(alpha);n=len(xs)
    # Integrate quantile-cell overlap over [alpha,1], not the source tail loop.
    integral=sum((v*max(Fraction(0),Fraction(i+1,n)-max(alpha,Fraction(i,n))) for i,v in enumerate(xs)),Fraction(0))
    return xs[math.ceil(alpha*n)-1],integral/(1-alpha)
def run():
    revision=sys.argv[1] if len(sys.argv)>1 else None
    text=subprocess.check_output(['git','-C',str(ROOT),'show',revision+':'+str(SOURCE.relative_to(ROOT))],text=True) if revision else SOURCE.read_text()
    source=re.search(r'~~~python\n(.*?)\n~~~',text,re.S).group(1);commands=[];rows=[]
    def verify(name,call,expected=None,error=None,close=False):
        try:
            value=call();ok=error is None and (math.isclose(value,expected,rel_tol=1e-12,abs_tol=0) if close else value==expected);actual=repr(value)
        except Exception as exc:ok=type(exc) is error;actual=type(exc).__name__+': '+str(exc)
        rows.append(dict(name=name,passed=ok,actual=actual,expected=error.__name__ if error else repr(expected)))
    with tempfile.TemporaryDirectory() as temp:
        p=Path(temp)/'monte_carlo_financial_simulator.py';p.write_text(source)
        for args in [[sys.executable,p.name],[sys.executable,'-m','compileall','-q',p.name],[sys.executable,'-c','import monte_carlo_financial_simulator']]:
            out=subprocess.run(args,cwd=temp,capture_output=True,text=True);commands.append(dict(args=args,returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0
        spec=importlib.util.spec_from_file_location('simulator',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        verify('probabilities',lambda:Fraction(1,4)+Fraction(1,2)+Fraction(1,4),1)
        verify('model mean',lambda:sum(p*v for p,v in [(Fraction(1,4),80),(Fraction(1,2),100),(Fraction(1,4),120)]),100)
        verify('model variance',lambda:sum(p*(v-100)**2 for p,v in [(Fraction(1,4),80),(Fraction(1,2),100),(Fraction(1,4),120)]),200)
        verify('discounted expected value',lambda:float(Fraction(100)*20/21),100/1.05,close=True)
        verify('loss signs',lambda:m.losses_from_values(100,[110,100,80]),[-10,0,20])
        for losses,alpha in [([-10,0,20,40],.75),([-10,0,20,40],.625),([0,0,20,-20],.75),([1e308]*4,.5),([10**30+1]*3,.8),([5e-324,0],.5),([-40,-20,0,20],.9),([7],.9)]:
            var,es=oracle(losses,alpha)
            verify('VaR '+repr((losses,alpha)),lambda:m.empirical_risk(iter(losses),alpha)[0],sorted(losses)[math.ceil(number(alpha)*len(losses))-1])
            verify('ES '+repr((losses,alpha)),lambda:m.empirical_risk(iter(losses),alpha)[1],int(es) if es.denominator==1 else float(es),close=es.denominator!=1)
        verify('displayed decimal rank',lambda:m.empirical_risk(range(1,51),.14)[0],7)
        for fn,args in [(m.empirical_risk,([True],.5)),(m.empirical_risk,([1,2],True)),(m.empirical_risk,([10**1000],.5)),(m.empirical_risk,(None,.5)),(m.losses_from_values,(100,None)),(m.losses_from_values,(10**1000,[1])),(m.losses_from_values,(100,[-1])),(m.report,([1],100,.75)),(m.report,(None,100,.75)),(m.sample_values,(2,True))]:
            verify('invalid '+repr(args),lambda:fn(*args),error=ValueError)
        verify('exact integer loss identity',lambda:m.losses_from_values(10**30+1,[10**30]),[1])
        verify('ES positive report underflow policy',lambda:m.empirical_risk([0,0,5e-324],.1),error=ValueError)
        verify('constant report integer identity',lambda:m.report([10**30+1]*2,10**30+1,.75)['mean_terminal'],10**30+1)
        samples=[]
        for seed in [42,7]:
            xs=m.sample_values(10000,seed);record=m.report(iter(xs),100,.75);n=len(xs);mean=sum(map(number,xs))/n;variance=sum((number(x)-mean)**2 for x in xs)/(n-1)
            verify('support '+str(seed),lambda:set(xs)<={80,100,120},True)
            verify('replay '+str(seed),lambda:xs==m.sample_values(10000,seed),True)
            verify('report mean '+str(seed),lambda:record['mean_terminal'],float(mean),close=True)
            verify('report variance '+str(seed),lambda:record['sample_sd']**2,float(variance),close=True)
            verify('report SE '+str(seed),lambda:record['standard_error_mean'],math.sqrt(float(variance)/n),close=True)
            verify('report loss frequency '+str(seed),lambda:record['loss_frequency'],sum(x<100 for x in xs)/n)
            for alpha in [.625,.75,.9]:
                risk=m.report(xs,100,alpha);v,e=oracle([100-x for x in xs],alpha)
                verify('sample risk '+repr((seed,alpha)),lambda:(risk['var_nearest_rank'],risk['es_fractional_tail']),tuple(float(x) for x in (v,e)))
            samples.append(dict(seed=seed,state_counts={str(x):xs.count(x) for x in [80,100,120]},report=record,standardized_mean_deviation=(record['mean_terminal']-100)/record['standard_error_mean'],loss_frequency_SE=math.sqrt(record['loss_frequency']*(1-record['loss_frequency'])/n)))
        # Exact installed Section18.12 risk copy, supplemental integration calls only.
        linked=ROOT/'books/book-01-python-foundations-for-financial-mathematics/chapter-18/18.12-risk-simulation.md';linked_text=linked.read_text();linked_code=re.search(r'~~~python\n(.*?)\n~~~',linked_text,re.S).group(1);lp=Path(temp)/'risk_simulation.py';lp.write_text(linked_code);lspec=importlib.util.spec_from_file_location('risk',lp);riskmod=importlib.util.module_from_spec(lspec);lspec.loader.exec_module(riskmod)
        for alpha in [.14,.625,.75]:
            losses=list(range(1,51)) if alpha==.14 else [-10,0,20,40]
            verify('linked empirical contract '+str(alpha),lambda:m.empirical_risk(losses,alpha),(riskmod.nearest_rank_var(losses,alpha),riskmod.empirical_es(losses,alpha)))
        out=dict(candidate_based_on=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),selected_revision=revision,source_sha256=hashlib.sha256(text.encode()).hexdigest(),linked_source_sha256=hashlib.sha256(linked_text.encode()).hexdigest(),python=sys.version,platform=platform.platform(),commands=commands,supplemental_predicates=rows,existing_unique_methods=12,new_historical_methods=0,samples=samples,scope='One discrete one-period position; sample arithmetic and replay, not independence, binomial/tail calibration, market pricing, platform or independent acceptance')
        (Path(__file__).parent/('baseline-replay.json' if revision else 'results.json')).write_text(json.dumps(out,indent=2)+'\n');assert all(x['passed'] for x in rows);print(len(rows),'supplemental predicates;3 source commands;12 existing unique methods passed')
if __name__=='__main__':run()
