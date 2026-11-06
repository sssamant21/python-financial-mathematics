"""Section 14.5 exact independence lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.05-independence.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1405-') as tmp:
        Path(tmp,'independence.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['independence.py']),('isolated import',['-c','import independence']),('exact compilation',['-m','compileall','-q','independence.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['independence.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('independence');exec(compile(code,str(source),'exec'),m.__dict__)
    from itertools import combinations
    a={(1,0),(1,1)}; b={(0,1),(1,1)}
    independent_atoms={(0,0):9506,(0,1):294,(1,0):194,(1,1):6}
    stress_atoms={(0,0):9600,(0,1):200,(1,0):100,(1,1):100}
    baseline=m.bernoulli_joint(.02,.03)
    stressed={key:value/10000 for key,value in stress_atoms.items()}
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,float(value),want,atol=0)
    for label,fn,want in [
        ('E1 independent product',lambda:m.bernoulli_joint(.2,.3)[(1,1)],F('.06')),
        ('E2 independent union',lambda:m.at_least_one_independent([.2,.3]),F('.44')),
        ('E3 independent union',lambda:m.at_least_one_independent([.02,.03]),F('.0494')),
        ('E4 neither',lambda:baseline[(0,0)],F('.9506')),
        ('E5 exactly one',lambda:m.p(baseline,a^b),F('.0488')),
        ('E6 joint',lambda:m.p(baseline,a&b),F('.0006')),
        ('E7 conditional equals marginal',lambda:m.conditional(baseline,a,b),F('.02')),
        ('E15 three defaults',lambda:m.at_least_one_independent([.01,.02,.03]),F('.058906')),
        ('F114 tiny independent union remains nonzero',lambda:m.at_least_one_independent([1e-20,2e-20]),F('3e-20')-F('2e-40')),
        ('project stress-to-baseline multiple',lambda:m.p(stressed,a&b)/m.p(baseline,a&b),F(50,3)),
    ]:num(label,fn,want)
    ck('E8/E9 stress dependence',not m.independent(stressed,a,b))
    ck('E10 disjoint positive events',not m.independent(stressed,{(0,0)},{(0,1)}))
    ck('E11 impossible event',m.independent(stressed,a,set()))
    ck('E12 certain event',m.independent(stressed,a,stressed))
    parity={bits:.25 for bits in [(0,0,0),(0,1,1),(1,0,1),(1,1,0)]}
    p,q,r=[{x for x in parity if x[i]} for i in range(3)]
    ck('E13 parity pairwise but not mutual',all(m.independent(parity,u,v) for u,v in combinations([p,q,r],2)) and m.p(parity,p&q&r)==0)
    ck('E16 explicit conditional counterexample',m.conditional(parity,p&q,r)==0 and m.conditional(parity,p,r)*m.conditional(parity,q,r)==.25)
    ck('E22 feasible joint bounds',max(0,F('.8')+F('.7')-1)==F('.5') and min(F('.8'),F('.7'))==F('.7'))
    ck('E23 independent .20 and .30 model',m.independent(m.bernoulli_joint(.2,.3),a,b))
    ck('F114 rare event dependent on itself',not m.independent({'x':1e-15,'y':.999999999999999},{'x'},{'x'}))
    ck('F114 normalized near-unit mass',m.p({'x':.5,'y':.5000000000005},{'x','y'})==1)
    ck('F114 independent model remains exact when reused',m.independent(m.bernoulli_joint(.37,.13),a,b,tol=0))
    for label,fn in [
        ('F114 undeclared conditional operand',lambda:m.conditional(stressed,{'invalid'},a)),
        ('F114 bool is not a tolerance',lambda:m.independent(stressed,a,b,tol=True)),
        ('F114 huge invalid integer rejected',lambda:m.bernoulli_joint(10**400,.2)),
        ('invalid weight mass',lambda:m.p({'a':.6,'b':.5},{'a'})),
        ('zero conditioning mass',lambda:m.conditional(stressed,a,set())),
    ]:reject(label,fn)
    audit={}
    for name,dist,atoms,ind in [('baseline',baseline,independent_atoms,True),('stress',stressed,stress_atoms,False)]:
        for label,event in [('A',a),('B',b),('both',a&b),('neither',{(0,0)}),('either',a|b),('total',set(atoms))]:
            num(f'project {name} {label}',lambda:m.p(dist,event),F(sum(atoms[key] for key in event),10000))
        ck(f'project {name} independence',m.independent(dist,a,b)==ind)
        audit[name]=dict(joint_atoms=[[list(key),val] for key,val in atoms.items()],
                         probability_units='basis points',any_default=m.p(dist,a|b),both_default=m.p(dist,a&b),independent=ind)
    ck('test-only listing has no demo stdout',commands[0]['stdout']=='')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=8,project_report=audit,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
