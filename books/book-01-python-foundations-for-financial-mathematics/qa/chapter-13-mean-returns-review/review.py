"""Section 13.8 exact mean returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.08-arithmetic-vs-geometric-mean-return.md'
    fragment,code=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1308-') as tmp:
        Path(tmp,'arithmetic_geometric_means.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['arithmetic_geometric_means.py']),('isolated import',['-c','import arithmetic_geometric_means']),('exact compilation',['-m','compileall','-q','arithmetic_geometric_means.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['arithmetic_geometric_means.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_means');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def power(g,n,d):
        with localcontext() as ctx:
            ctx.prec=65
            return (D(g.numerator)/D(g.denominator))**(D(n)/d)-1
    def num(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    for label,fn,want in [
        ('E1 arithmetic mean',lambda:m.arithmetic_mean([.1,.2]),F('.15')),
        ('E2 geometric mean',lambda:m.geometric_mean([.1,.2]),power(F('1.32'),1,2)),
        ('E3 arithmetic mean',lambda:m.arithmetic_mean([.5,-.5]),0),
        ('E4 cumulative loss',lambda:m.cumulative_return([.5,-.5]),F('-.25')),
        ('E5 geometric loss',lambda:m.geometric_mean([.5,-.5]),power(F('.75'),1,2)),
        ('E6 terminal wealth',lambda:m.terminal_wealth(1000,[.5,-.5]),750),
        ('E7 constant geometric mean',lambda:m.geometric_mean([.1,.1,.1]),F('.1')),
        ('E8 arithmetic mixed',lambda:m.arithmetic_mean([.2,-.1]),F('.05')),
        ('E9 geometric mixed',lambda:m.geometric_mean([.2,-.1]),power(F('1.08'),1,2)),
        ('E10 recovery product',lambda:m.cumulative_return([.25,-.2]),0),
        ('E11 recovery arithmetic',lambda:m.arithmetic_mean([.25,-.2]),F('.025')),
        ('E11 recovery geometric',lambda:m.geometric_mean([.25,-.2]),0),
        ('E12 variance uses n',lambda:m.population_variance([.1,-.1]),F('.01')),
        ('E13 variance drag',lambda:m.approximate_geometric_mean([.1,-.1]),F('-.005')),
        ('E14 exact mean',lambda:m.geometric_mean([.1,-.1]),power(F('.99'),1,2)),
        ('E15 annual growth via equivalent wealth',lambda:m.equivalent_wealth(1,.01,12)-1,F('1.01')**12-1),
        ('E16 total loss',lambda:m.geometric_mean([.1,-1,.2]),-1),
        ('F102 finite terminal wealth despite cumulative saturation',lambda:m.terminal_wealth(1e308,[-.99]*10),F('1e288')),
        ('F54 finite mean despite sum overflow',lambda:m.arithmetic_mean([1e308,1e308]),F('1e308')),
        ('F54 finite variance despite sum overflow',lambda:m.population_variance([1e154]*5+[0]*5),F('2.5e307')),
        ('F54 finite equivalent wealth despite intermediate overflow',lambda:m.equivalent_wealth(1e-308,1e170,2),float(F('1e-308')*(1+F('1e170'))**2)),
    ]:num(label,fn,want)
    days=list(map(F,('.08','-.06','.05','-.04','.07','-.03'))); values=list(map(float,days))
    g=math.prod(1+r for r in days);mean=sum(days)/len(days)
    # Independent pairwise-difference variance identity.
    var=sum((a-b)**2 for a in days for b in days)/(2*len(days)**2)
    approximate=mean-var/2
    exact=power(g,1,6);observed=m.geometric_mean(values)
    for label,fn,want in [
        ('project arithmetic mean',lambda:m.arithmetic_mean(values),mean),
        ('project cumulative',lambda:m.cumulative_return(values),g-1),
        ('project geometric',lambda:observed,exact),
        ('project terminal wealth',lambda:m.terminal_wealth(20000,values),20000*g),
        ('project equivalent terminal wealth',lambda:m.equivalent_wealth(20000,observed,6),20000*g),
        ('project population variance',lambda:m.population_variance(values),var),
        ('project approximate geometric',lambda:m.approximate_geometric_mean(values),approximate),
        ('project annualized growth',lambda:m.equivalent_wealth(1,observed,12)-1,g**2-1),
        ('project zero-factor stress',lambda:m.terminal_wealth(20000,values+[-1]),0),
    ]:num(label,fn,want)
    ck('project AM–GM and nonzero variance-drag error',observed<m.arithmetic_mean(values) and observed!=m.approximate_geometric_mean(values))
    num('contextual exact expression with supplied math and returns',lambda:eval(compile(fragment,str(source),'eval'),dict(math=math,returns=values)),exact)
    for label,fn in [
        ('F54 unrepresentable variance rejected',lambda:m.population_variance([1e308,0])),
        ('F54 unrepresentable wealth rejected',lambda:m.terminal_wealth(1e308,[1])),
        ('F102 positive gross cannot report complete loss',lambda:m.cumulative_return([-.99]*10)),
    ]:reject(label,fn)
    ck('exact demo',commands[0]['stdout'].splitlines()==['Arithmetic mean: 0.0000%','Geometric mean: -13.3975%','Cumulative return: -25.0000%','Terminal wealth: $750.00'])
    ck('F102 worked final numbers supplied',f'{float(20000*g):,.2f}' in source.read_text() and f'{float(g**2-1):.6%}' in source.read_text())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,contextual_fragments=1,conceptual_prompts=[17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
