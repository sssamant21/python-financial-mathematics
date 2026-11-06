"""Section 14.4 exact conditional probability lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-14/14.04-conditional-probability.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1404-') as tmp:
        Path(tmp,'conditional_probability.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['conditional_probability.py']),('isolated import',['-c','import conditional_probability']),('exact compilation',['-m','compileall','-q','conditional_probability.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['conditional_probability.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('conditional');exec(compile(code,str(source),'exec'),m.__dict__)
    table={'normal_survive':72,'normal_default':8,'stress_survive':15,'stress_default':5}
    w={k:v/100 for k,v in table.items()}
    stress={'stress_survive','stress_default'}; normal=set(w)-stress
    default={'normal_default','stress_default'}
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    common={'a':.09,'b':.14,'both':.06,'neither':.71}
    for label,fn,want in [
        ('E1 definition',lambda:m.conditional(common,{'a','both'},{'b','both'}),F('.30')),
        ('E2 reverse conditioning',lambda:m.conditional(common,{'b','both'},{'a','both'}),F('.40')),
        ('project full distribution',lambda:m.prob(w,w),1),
        ('E3 stress default',lambda:m.conditional(w,default,stress),F(1,4)),
        ('E4 normal default',lambda:m.conditional(w,default,normal),F(1,10)),
        ('E5 marginal default',lambda:m.prob(w,default),F(13,100)),
        ('E6 stress given default',lambda:m.conditional(w,stress,default),F(5,13)),
        ('E7 survival given stress',lambda:m.conditional(w,set(w)-default,stress),F(3,4)),
        ('E8/project joint, stress first',lambda:m.prob(w,stress)*m.conditional(w,default,stress),F(1,20)),
        ('project joint, default first',lambda:m.prob(w,default)*m.conditional(w,stress,default),F(1,20)),
        ('E9/project total probability',lambda:m.total_probability([(.2,.25),(.8,.1)]),F(13,100)),
        ('E10 alert posterior via integer counts',lambda:m.bayes(.01,.9,.1),F(90,1080)),
        ('E11 no false positives',lambda:m.bayes(.01,.9,0),1),
        ('E13 independent conditional',lambda:m.conditional({'a':.18,'b':.28,'both':.12,'none':.42},{'a','both'},{'b','both'}),F('.3')),
        ('E14 dependent conditional',lambda:m.conditional({'a':.1,'b':.2,'both':.2,'none':.5},{'a','both'},{'b','both'}),F('.5')),
        ('E15 disjoint conditional',lambda:m.conditional(w,normal,stress),0),
        ('E16 self conditional',lambda:m.conditional(w,stress,stress),1),
        ('E17 regime average',lambda:m.total_probability([(.1,.4),(.9,.02)]),F('.058')),
        ('E18 Bayes regime reversal',lambda:m.bayes(.1,.4,.02),F(20,29)),
        ('E23 total loss event mass',lambda:m.total_probability([(.6,.1),(.4,.3)]),F('.18')),
        ('F113 rare evidence remains positive before division',lambda:m.bayes(.5,5e-324,5e-324),F('.5')),
        ('F113 single-pass regime iterable',lambda:m.total_probability(iter([(.2,.25),(.8,.1)])),F('.13')),
    ]:num(label,fn,want)
    ck('F113 exact unit mass despite accepted weight rounding',m.prob({'a':.5,'b':.5000000000005},{'a','b'})==1)
    ck('F113 normalized total probability cannot exceed one',m.total_probability([(.5,1),(.5000000000005,1)])==1)
    for label,fn in [
        ('E12 zero evidence',lambda:m.bayes(.5,0,0)),
        ('zero-mass conditioning with nonempty event',lambda:m.conditional({'a':1,'b':0},{'a'},{'b'})),
        ('F113 unknown event cannot disappear in intersection',lambda:m.conditional(w,{'misspelled'},stress)),
        ('F113 invalid regime type raises domain error',lambda:m.total_probability([('1',.2)])),
        ('F113 oversized integer probability rejected',lambda:m.bayes(10**400,.9,.1)),
        ('invalid probability sum',lambda:m.prob({'a':.9,'b':.2},{'a'})),
        ('negative conditional rate rejected',lambda:m.total_probability([(1,-.01)])),
    ]:reject(label,fn)
    ck('project independence fails on direct atoms',table['stress_default']*100!=20*13)
    ck('test-only listing has no demo stdout',commands[0]['stdout']=='')
    report=dict(version='14.4 synthetic fixture',assumptions='Hypothetical exhaustive market/default atoms, no calibration',
                weights=w,conditioning_denominators={'stress':.2,'normal':.8,'default':.13,'flag':.108},
                weight_mass_tolerance='1e-12',comparison_relative_tolerance=1e-12,
                source_results={'stress':m.prob(w,stress),'default':m.prob(w,default),
                'default_given_stress':m.conditional(w,default,stress),
                'default_given_normal':m.conditional(w,default,normal),
                'stress_given_default':m.conditional(w,stress,default),'alert_posterior':m.bayes(.01,.9,.1)})
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
             listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,
             local_prompt_records=24,mini_project_records=1,mini_project_task_records=10,project_report=report,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
