"""Section 14.2 exact sample spaces and events lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.02-sample-spaces-and-events.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1402-') as tmp:
        Path(tmp,'sample_spaces_and_events.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['sample_spaces_and_events.py']),('isolated import',['-c','import sample_spaces_and_events']),('exact compilation',['-m','compileall','-q','sample_spaces_and_events.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['sample_spaces_and_events.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('sample_spaces');exec(compile(code,str(source),'exec'),m.__dict__)
    from itertools import combinations
    omega={'up','flat','down'}
    weights=dict(up=.5,flat=.2,down=.3)
    a={'up','flat'}; b={'flat','down'}
    for label,result,want in [
        ('E2 three-by-three ordered outcomes',len(m.sample_space(omega,omega)),9),
        ('E4 predicate event',m.event(omega,lambda x:x!='down'),a),
        ('E5 complement',m.complement(omega,{'down'}),a),
        ('E6 empty event',m.probability(weights,[]),0),
        ('E7 full event',m.probability(weights,omega),1),
        ('E9 union',m.union(a,b),omega),
        ('E10 intersection',m.intersection(a,b),{'flat'}),
        ('E11 disjoint',m.disjoint({'up'},{'down'}),True),
        ('E12 overlap',m.disjoint(a,b),False),
    ]:ck(label,result==want,actual=repr(result),expected=repr(want))
    close('E13/E15 no loss',m.probability(weights,a),F(7,10))
    close('E14 loss',m.probability(weights,{'down'}),F(3,10))
    ex16={'a only':.4,'b only':.3,'both':.2,'neither':.1}
    close('E16 union from disjoint atoms',m.probability(ex16,m.union({'a only','both'},{'b only','both'})),F(9,10))
    loans=m.sample_space(('S','D'),('S','D'))
    ck('E18 two-loan universe',set(loans)=={('S','S'),('S','D'),('D','S'),('D','D')})
    ck('E19 exactly one default',m.event(loans,lambda x:x.count('D')==1)=={('S','D'),('D','S')})
    ck('E20 at least one default',m.event(loans,lambda x:'D' in x)=={('S','D'),('D','S'),('D','D')})
    ck('E22 partition',m.union(m.union({'up'},{'flat'}),{'down'})==omega and all(m.disjoint({x},{y}) for x,y in combinations(omega,2)))
    for label,fn in [
        ('E17 reject excess mass',lambda:m.validate_distribution(dict(a=.4,b=.4,c=.4))),
        ('F111 exhausted dimension rejected',lambda:m.sample_space(iter(()),['up'])),
        ('F111 duplicate labels rejected',lambda:m.sample_space(['up','up'])),
        ('F111 unhashable labels rejected',lambda:m.sample_space([['up']])),
        ('F111 huge invalid integer weight rejected',lambda:m.validate_distribution({'up':10**400})),
        ('unknown event member rejected',lambda:m.probability(weights,['other'])),
        ('unknown complement member rejected',lambda:m.complement(omega,['other'])),
    ]:reject(label,fn)
    near={'up':.5,'down':.5000000000005}
    ck('F111 normalized mass stays within probability bounds',m.probability(near,near)==1)
    exact={('normal','survive'):72,('normal','default'):8,('stress','survive'):15,('stress','default'):5}
    distribution={k:v/100 for k,v in exact.items()}
    space=m.sample_space(('normal','stress'),('survive','default'))
    stress=m.event(space,lambda x:x[0]=='stress')
    default=m.event(space,lambda x:x[1]=='default')
    p=lambda outcomes:m.probability(distribution,outcomes)
    for label,selected,want in [
        ('project mass',space,100),
        ('project stress',stress,20),
        ('project default',default,13),
        ('project intersection',m.intersection(stress,default),5),
        ('project union',m.union(stress,default),28),
    ]:close(label,p(selected),F(want,100))
    close('project conditional with positive denominator',p(m.intersection(stress,default))/p(stress),F(1,4))
    ck('project dependence and inclusion–exclusion',5*100!=20*13 and math.isclose(p(m.union(stress,default)),p(stress)+p(default)-p(m.intersection(stress,default))))
    reject('project undeclared event state',lambda:p({('recovery','default')}))
    # Independent exhaustive subset oracle, based on the four integer masses.
    subsets=[s for n in range(5) for s in combinations(exact,n)]
    ck('all 16 joint-space events reconcile',all(math.isclose(p(s),sum(exact[x] for x in s)/100) for s in subsets))
    ck('exact demonstration',commands[0]['stdout'].splitlines()==[
        "Sample space: ('up', 'flat', 'down')",'Probability of loss: 0.3','Probability of no loss: 0.7'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,historical_unique_methods_added=0, project_report=dict(assumption='Hypothetical joint weights, not measured frequencies', stress=sorted(stress), default=sorted(default), input_weights=[[*k,v] for k,v in distribution.items()], p_stress=p(stress), p_default=p(default), p_both=p(m.intersection(stress,default)), p_either=p(m.union(stress,default)), p_default_given_stress=p(m.intersection(stress,default))/p(stress)))
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
