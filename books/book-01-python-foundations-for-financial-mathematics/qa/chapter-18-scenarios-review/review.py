"""Exact deterministic scenario source; independent rational table and policy probes."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    path='chapter-18/18.07-scenario-analysis.md';data=(BOOK/path).read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/'+path]);code=re.findall(rb'^~~~python\n(.*?)^~~~',data,re.M|re.S)[0];commands=[];checks=[]
    def ck(label,fn,expected=True):
        try:actual=fn();ok=actual==expected
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=expected,passed=bool(ok)))
    def num(label,fn,want):
        try:actual=fn();ok=math.isclose(actual,float(want),rel_tol=1e-12,abs_tol=0)
        except Exception as e:actual=repr(e);ok=False
        checks.append(dict(label=label,actual=actual,expected=str(want),passed=bool(ok),relative_tolerance=1e-12,absolute_tolerance=0))
    def rejects(fn):
        try:fn()
        except ValueError:return True
        except Exception as e:return type(e).__name__
        return False
    with tempfile.TemporaryDirectory(prefix='book1-1807-') as tmp:
        Path(tmp,'scenario_analysis.py').write_bytes(code)
        for label,args in [('exact demo/tests',['scenario_analysis.py']),('quiet import',['-c','import scenario_analysis']),('compile',['-m','compileall','-q','scenario_analysis.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60);methods=re.search(r'Ran (\d+) tests',p.stderr);ok=p.returncode==0 and (bool(methods and int(methods[1])==10 and re.search(r'^OK\s*$',p.stderr,re.M)) if label=='exact demo/tests' else not(p.stdout or p.stderr));commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,existing_methods=int(methods[1]) if methods else 0,passed=ok))
    m=types.ModuleType('scenario_lab');exec(compile(code,str(BOOK/path),'exec'),m.__dict__)
    scenarios=[]
    for name,rs in [('base',[F(5,100),F(2,100)]),('downside',[F(-1,5),F(-1,10)]),('upside',[F(15,100),F(8,100)])]:
        actual=m.value_scenario([60,40],list(map(float,rs)));terminal=sum(e*(1+r) for e,r in zip([60,40],rs));pnl=terminal-100
        for key,want in [('baseline',100),('terminal',terminal),('pnl',pnl)]:num(name+' '+key,lambda actual=actual,key=key:actual[key],want)
        scenarios.append(actual)
    weighted=m.weighted_summary(scenarios,[.5,.3,.2])
    for key,want in [('expected_terminal',F(4977,50)),('expected_pnl',F(-23,50)),('loss_probability',F(3,10))]:num('E16-18 '+key,lambda key=key:weighted[key],want)
    for label,fn,want in [('E1 baseline',lambda:F(60)+40,100),('E2 A base',lambda:60*F(105,100),63),('E3 B base',lambda:40*F(102,100),F(204,5)),('E6 down A',lambda:60*F(4,5),48),('E7 down B',lambda:40*F(9,10),36),('E11 source 1pp sensitivity',lambda:m.value_scenario([60,40],[.01,0])['pnl'],F(3,5)),('E12 source 1bp sensitivity',lambda:m.value_scenario([60,40],[.0001,0])['pnl'],F(3,500)),('E13 100bp',lambda:F(100,10000),F(1,100)),('E14 sequential return',lambda:F(11,10)*F(9,10)-1,F(-1,100)),('E15 probability sum',lambda:F(1,2)+F(3,10)+F(1,5),1),('E21 source fee',lambda:m.value_scenario([60,40],[0,0],2)['pnl'],-2),('E22 source zero shock',lambda:m.value_scenario([60,40],[0,0])['pnl'],0),('E23 bond baseline',lambda:F(100)/F(105,100),F(2000,21)),('E24 bond shock',lambda:F(100)/F(106,100),F(5000,53)),('E25 bond PnL',lambda:F(5000,53)-F(2000,21),F(-1000,1113)),('E26 FX baseline',lambda:100*F(11,10),110),('E27 FX shocked',lambda:100*F(105,100),105),('E28 FX PnL',lambda:100*(F(105,100)-F(11,10)),-5),('E36 total loss',lambda:m.value_scenario([100],[-1])['terminal'],0)]:num(label,fn,want)
    for label,q,want in [('printed rate baseline',F(2000,21),95.2381),('printed rate shock',F(5000,53),94.3396),('printed rate PnL',F(-1000,1113),-.8985)]:ck(label,lambda q=q,want=want:round(float(q),4)==want)
    ck('zero-probability loss does not contribute',lambda:m.weighted_summary([{'terminal':90,'pnl':-10},{'terminal':100,'pnl':0}],[0,1])['loss_probability']==0)
    ck('strict PnL zero not loss',lambda:m.weighted_summary([{'terminal':100,'pnl':0}],[1])['loss_probability']==0)
    ck('one-pass inputs',lambda:m.value_scenario(iter([60,40]),iter([0,0]))['baseline']==100)
    ck('baseline identity large integer',lambda:m.value_scenario([10**18+1],[0])['baseline']==10**18+1)
    ck('terminal identity large integer',lambda:m.value_scenario([10**18+1],[0])['terminal']==10**18+1)
    num('tiny positive PnL',lambda:m.value_scenario([10**18],[1e-18])['pnl'],1)
    num('tiny negative PnL',lambda:m.value_scenario([10**18],[-1e-18])['pnl'],-1)
    ck('tiny loss recognized in weighted summary',lambda:m.weighted_summary([m.value_scenario([10**18],[-1e-18]),m.value_scenario([10**18],[0])],[.5,.5])['loss_probability']==.5)
    ck('terminal fee integer identity',lambda:m.value_scenario([10**18+1],[0],1)['terminal']==10**18)
    ck('finite helper huge int returns false',lambda:m.finite(10**1000),False)
    ck('normalization policy keeps all-loss probability exactly one',lambda:m.weighted_summary([{'terminal':99,'pnl':-1}],[1+5e-13])['loss_probability']==1)
    ck('normalization policy constant expectation identity',lambda:m.weighted_summary([{'terminal':100,'pnl':0}],[1-5e-13])['expected_terminal']==100)
    for label,fn in [('exposures noniterable',lambda:m.value_scenario(None,[0])),('returns noniterable',lambda:m.value_scenario([100],None)),('empty exposures',lambda:m.value_scenario([],[])),('mismatched inputs',lambda:m.value_scenario([60,40],[0])),('negative exposure',lambda:m.value_scenario([-100],[0])),('below total loss',lambda:m.value_scenario([100],[-1.1])),('huge exposure',lambda:m.value_scenario([10**1000],[0])),('huge return',lambda:m.value_scenario([100],[10**1000])),('huge fee',lambda:m.value_scenario([100],[0],10**1000)),('bool return',lambda:m.value_scenario([100],[True])),('negative fee',lambda:m.value_scenario([100],[0],-1)),('terminal overflow',lambda:m.value_scenario([1e308],[1e308])),('terminal underflow',lambda:m.value_scenario([5e-324],[-.75])),('results noniterable',lambda:m.weighted_summary(None,[1])),('probabilities noniterable',lambda:m.weighted_summary([{'terminal':100,'pnl':0}],None)),('missing key',lambda:m.weighted_summary([{'terminal':100}],[1])),('malformed result',lambda:m.weighted_summary([None],[1])),('huge result',lambda:m.weighted_summary([{'terminal':10**1000,'pnl':0}],[1])),('huge probability',lambda:m.weighted_summary([{'terminal':100,'pnl':0}],[10**1000])),('nonunit probability sum',lambda:m.weighted_summary([{'terminal':100,'pnl':0}],[.9])),('negative probability',lambda:m.weighted_summary([{'terminal':100,'pnl':0}],[-1])),('nonzero weighted underflow',lambda:m.weighted_summary([{'terminal':5e-324,'pnl':0},{'terminal':0,'pnl':0}],[.25,.75]))]:ck('reject '+label,lambda fn=fn:rejects(fn))
    # The source explicitly leaves common baseline/horizon consistency to the caller.
    ck('external baseline contract not enforced',lambda:m.weighted_summary([{'baseline':100,'terminal':100,'pnl':0},{'baseline':200,'terminal':200,'pnl':0}],[.5,.5])['expected_terminal']==150)
    out=dict(source_sha256=hashlib.sha256(data).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),python=platform.python_version(),platform=platform.platform(),commands=commands,checks=checks,scenarios=scenarios,weighted=weighted,counts=dict(workflows=1,local_answers=40,lab_steps=12,existing_unique_methods_rerun=10,new_historical_methods=0),model=dict(exposures=[60,40],currency='fictional common currency',horizon='one unspecified common portfolio period; separate bond example one year',valuation_date='no actual as-of date or market dataset supplied; execution date is not valuation date',returns=[[.05,.02],[-.2,-.1],[.15,.08]],probabilities=[.5,.3,.2],fee_timing='fixed end-period fee, subtracted once'),limits='Deterministic source scenarios and supplemental bond/FX calculations; no Monte Carlo source API, calibrated likelihood, joint-distribution or independent model acceptance. Common baseline/horizon externally required, not enforced. F28/F32/F165 retained.')
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,default=str)+'\n');print(len(commands),len(checks),sum(not c['passed'] for c in commands+checks));return not all(c['passed'] for c in commands+checks)
if __name__=='__main__':raise SystemExit(main())
