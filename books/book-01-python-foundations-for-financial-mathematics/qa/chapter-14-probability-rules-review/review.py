"""Section 14.3 exact probability rules lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.03-probability-rules.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1403-') as tmp:
        Path(tmp,'probability_rules.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['probability_rules.py']),('isolated import',['-c','import probability_rules']),('exact compilation',['-m','compileall','-q','probability_rules.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['probability_rules.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('rules');exec(compile(code,str(source),'exec'),m.__dict__)
    table={'normal_ok':72,'normal_default':8,'stress_ok':15,'stress_default':5}
    weights={k:v/100 for k,v in table.items()}
    stress={'stress_ok','stress_default'}
    default={'normal_default','stress_default'}
    normal={'normal_ok','normal_default'}
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E2 whole space',lambda:m.probability(weights,weights),1),
        ('E3 empty event',lambda:m.probability(weights,[]),0),
        ('E4 complement',lambda:m.complement({'D':.04,'S':.96},{'D'}),F('.96')),
        ('E5 disjoint addition',lambda:m.union_probability({'a':.2,'b':.3,'n':.5},{'a'},{'b'}),F('.5')),
        ('E6 overlapping union',lambda:m.union_probability({'a':.3,'b':.2,'j':.1,'n':.4},{'a','j'},{'b','j'}),F('.6')),
        ('E7 intersection recovery',lambda:m.intersection_probability({'a':.3,'b':.2,'j':.2,'n':.3},{'a','j'},{'b','j'}),F('.2')),
        ('E9 complement of neither',lambda:m.complement({'none':.45,'some':.55},{'none'}),F('.55')),
        ('E10 exclusive or',lambda:m.probability({'a':.3,'b':.2,'j':.1,'n':.4},{'a','b'}),F('.5')),
        ('E11 independent joint atom',lambda:m.intersection_probability({'a':.3,'b':.2,'j':.3,'n':.2},{'a','j'},{'b','j'}),F('.3')),
        ('E12 independent union',lambda:m.union_probability({'a':.3,'b':.2,'j':.3,'n':.2},{'a','j'},{'b','j'}),F('.8')),
        ('E13/project conditional default under stress',lambda:m.conditional_probability(weights,default,stress),F(1,4)),
        ('E14/project conditional stress given default',lambda:m.conditional_probability(weights,stress,default),F(5,13)),
        ('E18 independent survival',lambda:m.probability({'SS':.9506,'SD':.0294,'DS':.0194,'DD':.0006},{'SS'}),F('.9506')),
        ('E19 at least one default',lambda:m.complement({'SS':.9506,'SD':.0294,'DS':.0194,'DD':.0006},{'SS'}),F('.0494')),
        ('project stress',lambda:m.probability(weights,stress),F('.20')),
        ('project default',lambda:m.probability(weights,default),F('.13')),
        ('project intersection',lambda:m.intersection_probability(weights,stress,default),F('.05')),
        ('project union',lambda:m.union_probability(weights,stress,default),F('.28')),
        ('project default under normal',lambda:m.conditional_probability(weights,default,normal),F('.10')),
        ('project total probability',lambda:sum(m.probability(weights,r)*m.conditional_probability(weights,default,r) for r in [normal,stress]),F('.13')),
        ('project Bayes inversion',lambda:m.conditional_probability(weights,default,stress)*m.probability(weights,stress)/m.probability(weights,default),F(5,13)),
    ]:num(label,fn,want)
    ck('E15 dependent',not m.independent(weights,stress,default))
    ck('E20 valid distribution',set(m.validate({'a':.5,'b':.2,'c':.3}))=={'a','b','c'})
    ck('E23 disjoint positive events not independent',not m.independent(weights,stress,normal))
    ck('exact independence on a four-atom product',m.independent({'a':.3,'b':.2,'j':.3,'n':.2},{'a','j'},{'b','j'}))
    ck('F112 rare event not independent of itself',not m.independent({'rare':1e-15,'ordinary':.999999999999999},{'rare'},{'rare'}))
    near={'a':.5,'b':.5000000000005}
    ck('F112 normalize accepted near-unit mass',m.probability(near,near)==1)
    for label,fn in [
        ('E1 invalid probability',lambda:m.validate({'a':1.2})),
        ('E21 invalid mass',lambda:m.validate({'a':.5,'b':.2,'c':.4})),
        ('E22 zero denominator',lambda:m.conditional_probability(weights,default,set())),
        ('F112 invalid complement operand',lambda:m.complement(weights,{'unknown'})),
        ('F112 invalid intersection operand',lambda:m.intersection_probability(weights,{'unknown'},default)),
        ('F112 invalid conditional numerator event',lambda:m.conditional_probability(weights,{'unknown'},stress)),
        ('F112 invalid union operand',lambda:m.union_probability(weights,{'unknown'},default)),
        ('F112 invalid negative tolerance',lambda:m.independent(weights,stress,default,-.01)),
        ('F112 invalid boolean tolerance',lambda:m.independent(weights,stress,default,True)),
        ('F112 invalid infinite tolerance',lambda:m.independent(weights,stress,default,math.inf)),
        ('F112 huge integer weight rejected',lambda:m.validate({'a':10**400})),
    ]:reject(label,fn)
    atoms=list(table);totals=[sum(table[x] for j,x in enumerate(atoms) if mask & 1<<j) for mask in range(16)]
    events=[{x for j,x in enumerate(atoms) if mask & 1<<j} for mask in range(16)]
    ck('all event pairs satisfy subset and union identities',all(
        math.isclose(m.union_probability(weights,a,b),totals[i|j]/100) and
        math.isclose(m.intersection_probability(weights,a,b),totals[i&j]/100) and
        (i&j!=i or totals[i]<=totals[j])
        for i,a in enumerate(events) for j,b in enumerate(events)))
    ck('test-only listing has no demo stdout',commands[0]['stdout']=='')
    report=dict(version='14.3 synthetic fixture',weights=weights,stress=sorted(stress),default=sorted(default),
                both='5/100',either='(20+13-5)/100',default_given_stress='5/20',default_given_normal='8/80',
                stress_given_default='5/13',independent=False,weight_mass_tolerance='1e-12',
                assumptions='Four hypothetical exhaustive joint states; no empirical calibration.')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,project_report=report,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
