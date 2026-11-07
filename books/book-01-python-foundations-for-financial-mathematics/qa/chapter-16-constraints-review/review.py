"""Portfolio mandate audit and independent rational constraint/fee references."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from decimal import Decimal as D,localcontext
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-16/16.13-portfolio-constraints.md'
    source_bytes=source.read_bytes() if len(sys.argv)==1 else subprocess.check_output(['git','-C',str(BOOK),'show',sys.argv[1]+':books/book-01-python-foundations-for-financial-mathematics/chapter-16/16.13-portfolio-constraints.md'])
    blocks=re.findall(rb'^```python\n(.*?)^```',source_bytes,re.M|re.S)
    code=next(b for b in blocks if b'import unittest' in b)
    commands=[];checks=[]
    def ck(label,ok,**kw):checks.append(dict(label=label,passed=bool(ok),**kw))
    def close(label,value,want):
        ck(label,math.isclose(value,float(want),rel_tol=1e-12,abs_tol=0),actual=float(value) if math.isfinite(value) else repr(value),independent_reference=str(want),relative_tolerance=1e-12,absolute_tolerance=0)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:
            if value is None:ck(label,False,actual='None',independent_reference=str(want))
            else:close(label,value,want)
    def reject(label,fn):
        try:v=fn()
        except ValueError as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(v))
    def root(v):
        v=F(v)
        with localcontext() as ctx:
            ctx.prec=80;return (D(v.numerator)/D(v.denominator)).sqrt()
    with tempfile.TemporaryDirectory(prefix='book1-1613-') as tmp:
        Path(tmp,'portfolio_constraints.py').write_bytes(code)
        for label,args in [('exact demonstration and 12 embedded tests',['portfolio_constraints.py']),('isolated import',['-c','import portfolio_constraints']),('exact compilation',['-m','compileall','-q','portfolio_constraints.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['portfolio_constraints.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('covariance_lab');exec(compile(code,str(source),'exec'),m.__dict__)
    w=[.5,.3,.2];lo=[0,0,0];hi=[.6,.6,.4];ref=[.4,.4,.2]
    def audit(weights=w,cap=.85,turnover=.1):return m.check_constraints(weights,lo,hi,{'equity':[0,1]},{'equity':(0,cap)},reference=ref,max_turnover=turnover)
    base=audit();cap=audit(cap=.7);trade=audit(turnover=.05);position=audit(weights=[.7,.2,.1])
    ck('lab base mandate passes',base['feasible']);close('E4 source equity exposure',base['group_exposures']['equity'],F(4,5));close('E13 source one-way turnover',base['one_way_turnover'],F(1,10))
    ck('E5 cap breach',not cap['feasible'] and any('equity' in v for v in cap['violations']))
    ck('E2 position maximum breach',not position['feasible'] and any('asset 0' in v for v in position['violations']))
    ck('E14 turnover breach',not trade['feasible'] and 'one-way turnover exceeds limit' in trade['violations'])
    floor=m.check_constraints([.05,.75,.2],[.1,0,0],[1,1,1]);ck('E3 position floor breach',not floor['feasible'])
    sector=m.check_constraints(w,lo,hi,{'equity':[0,1]},{'equity':(.5,1)});ck('E6 group floor passes',sector['feasible'])
    num('E7 gross signed exposure',lambda:m.gross_exposure([1.2,-.2]),F(7,5));close('E8 supplemental net signed exposure',F(6,5)-F(1,5),1)
    ck('E9 proposed short not long-only feasible',not m.check_constraints([1.2,-.2],[0,0],[1,1])['feasible'])
    ck('E10 contradictory lower budget',not m.necessary_budget_bounds([.6,.6],[.8,.8]))
    ck('E11 insufficient upper budget',not m.necessary_budget_bounds([0,0],[.4,.4]))
    ck('E12 feasible independent bounds',m.necessary_budget_bounds([0,0],[.6,.6]))
    close('E1 supplemental budget',sum(map(lambda x:F(str(x)),w)),1)
    for label,value,want in [('E2 cap excess',F(7,10)-F(3,5),F(1,10)),('E3 floor shortfall',F(1,10)-F(1,20),F(1,20)),('E5 sector excess',F(4,5)-F(7,10),F(1,10)),('E14 turnover excess',F(1,10)-F(1,20),F(1,20)),('E17 return floor shortfall',F(3,50)-F(59,1000),F(1,1000)),('E18 liquidity excess',F(3,10)-F(1,5),F(1,10)),('E19 cash shortfall',F(1,20)-F(1,50),F(3,100)),('E20 leverage excess',F(7,5)-F(6,5),F(1,5))]:close(label,value,want)
    # Exercise 15 quote is a rate per total buys plus sells, consistent with Section 11.
    solution=re.search(r'### Exercise 15.*?\*\*Worked solution:\*\* (.*?)(?=\n\n)',source_bytes.decode(),re.S).group(1)
    ck('F154 E15 prompt/answer total-traded-notional cost',('.0004' in solution or '0.0004' in solution) and '.0002' not in solution,worked_solution=solution,independent_reference='2 * .002 * .1 = .0004 of NAV',scope='text alignment plus supplemental rational fee formula, no source cost function')
    close('E15 supplemental symmetric fee from source turnover',2*F(2,1000)*F(str(base['one_way_turnover'])),F(1,2500))
    num('E16 source expected return',lambda:m.expected_return(w,[.08,.05,.02]),F(59,1000))
    overlap=m.check_constraints(w,lo,hi,{'equity':[0,1],'country':[0,2]},{'equity':(0,.85),'country':(0,.75)})
    close('E21 overlapping equity group',overlap['group_exposures']['equity'],F(4,5));close('E21 overlapping country group',overlap['group_exposures']['country'],F(7,10))
    close('E23 supplemental weighted duration',F(1,2)*2+F(1,2)*8,5)
    # Each independent bound test passes; joint disjoint-group floors cannot both fit unit budget.
    ck('E28 independent position bounds pass',m.necessary_budget_bounds(lo,[1,1,1]))
    conflict=m.check_constraints(w,lo,[1,1,1],{'first':[0],'rest':[1,2]},{'first':(.7,1),'rest':(.7,1)})
    ck('E28 proposed portfolio rejected under conflicting group floors',not conflict['feasible'],joint_infeasibility_proof='disjoint lower group sums .7+.7=1.4>1; supplemental proof, not a solver')
    for label,fn,want in [
      ('F154 tiny negative holding not hidden',lambda:not m.check_constraints([-1e-11,1.00000000001],[0,0],[1,1])['feasible'],True),
      ('F154 tiny position breach not hidden',lambda:not m.check_constraints([.50000000001,.49999999999],[0,0],[.5,1])['feasible'],True),
      ('F154 tiny group breach not hidden',lambda:not m.check_constraints([.5,.5],[0,0],[1,1],{'g':[0]},{'g':(0,.49999999999)})['feasible'],True),
      ('F154 tiny turnover breach not hidden',lambda:not m.check_constraints([.5,.5],[0,0],[1,1],reference=[.4,.6],max_turnover=.09999999999)['feasible'],True),
      ('F154 near-unit insufficient bounds not rounded feasible',lambda:m.necessary_budget_bounds([0,0],[.5,.49999999999]),False),
    ]:
      try:value=fn()
      except Exception as e:ck(label,False,exception=repr(e))
      else:ck(label,value is want,actual=value,expected=want)
    for label,fn,want in [
      ('F154 integer expectation cancellation',lambda:m.expected_return([.5,.5],[10**18+2,-10**18]),1),
      ('F154 signed product cancellation before overflow',lambda:m.expected_return([1e308,-1e308,1],[2,2,.1]),F(1,10)),
    ]:num(label,fn,want)
    for label,fn in [
      ('F154 malformed group container ValueError',lambda:m.check_constraints([1],[0],[1],5,{})),
      ('F154 group name schema ValueError',lambda:m.check_constraints([1],[0],[1],{1:[0]},{1:(0,.5)})),
      ('F154 huge integer input ValueError',lambda:m.gross_exposure([10**1000])),
      ('F154 unreportable gross ValueError',lambda:m.gross_exposure([1e308,1e308])),
      ('invalid budget rejected',lambda:m.check_constraints([.5,.4],[0,0],[1,1])),
      ('duplicate group member rejected',lambda:m.check_constraints([1],[0],[1],{'g':[0,0]},{'g':(0,1)})),
      ('group mismatch rejected',lambda:m.check_constraints([1],[0],[1],{'g':[0]},{})),
      ('invalid independent bounds rejected',lambda:m.necessary_budget_bounds([.5],[.4])),
      ('paired reference required',lambda:m.check_constraints(w,lo,hi,reference=ref)),
    ]:reject(label,fn)
    try:
      approximate=m.check_constraints([.50000000001,.49999999999],[0,0],[.5,1],tolerance=1e-10)
      ck('policy extension explicit approximate audit',approximate['feasible'])
    except Exception as e:ck('policy extension explicit approximate audit',False,exception=repr(e))
    num('policy extension recorded supplied budget residual',lambda:m.check_constraints([.5,.50000000005],[0,0],[1,1])['budget_residual'],F(1,20000000000))
    reject('F154 nonzero expectation underflow rejected',lambda:m.expected_return([1e-300],[1e-300]))
    ck('lab original fixtures preserved',w==[.5,.3,.2] and ref==[.4,.4,.2])
    report=dict(assets=['fictional A','fictional B','cash-like C'],weights=w,lower=lo,upper=hi,reference=ref,group={'equity':[0,1]},base=base,cap_breach=cap,position_breach=position,turnover_breach=trade,overlapping_groups=overlap,conflicting_groups=conflict,fee_rate_per_total_traded='.002',total_traded='.2',one_way_turnover='.1',supplemental_fee='.0004',units='weights/NAV fractions, common fictional USD',valuation_time='synthetic common t0',dates=None,external_flows='none',scope='proposal audit only, no optimizer, orders, actual classifications or mandate approval',fixture_sha256=hashlib.sha256(json.dumps([w,lo,hi,ref]).encode()).hexdigest())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source_bytes).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=30,lab_step_records=12,historical_unique_methods_added=0,project_report=report)
    (HERE/('results.json' if len(sys.argv)==1 else 'baseline.json')).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not v['passed'] for v in commands+checks))
    return not all(v['passed'] for v in commands+checks)
if __name__=='__main__':raise SystemExit(main())
