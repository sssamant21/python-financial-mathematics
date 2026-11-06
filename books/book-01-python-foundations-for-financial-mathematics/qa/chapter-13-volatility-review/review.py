"""Section 13.11 exact volatility lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.11-volatility.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1311-') as tmp:
        Path(tmp,'volatility.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['volatility.py']),('isolated import',['-c','import volatility']),('exact compilation',['-m','compileall','-q','volatility.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['volatility.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_volatility');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    from itertools import combinations
    def root(value):
        f=F(value)
        with localcontext() as ctx:
            ctx.prec=55
            return (D(f.numerator)/D(f.denominator)).sqrt()
    def pairs(xs, sample):
        return root(sum((x-y)**2 for x,y in combinations(xs,2))/(len(xs)*(len(xs)-int(sample))))
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    five=list(map(F,('.02','-.01','.03','-.02','.01')))
    namespace={};exec(compile(fragment,str(source),'exec'),namespace)
    ck('exact data fragment matches independent five-day fixture',namespace['returns']==list(map(float,five)))
    days=list(map(F,('.01','-.005','.015','-.01','.007','-.008','.022','-.017','.004','-.003')))
    values=list(map(float,days))
    for label,fn,want in [
        ('E1 mean',lambda:m.mean_return([.1,-.1]),0),
        ('E3 population',lambda:m.population_volatility([.1,-.1]),F('.1')),
        ('E5 sample',lambda:m.sample_volatility([.1,-.1]),root(F('.02'))),
        ('E6 constant',lambda:m.sample_volatility([.03]*3),0),
        ('E7 five-day mean',lambda:m.mean_return(list(map(float,five))),F('.006')),
        ('E9 five-day population',lambda:m.population_volatility(list(map(float,five))),pairs(five,False)),
        ('E10 five-day sample',lambda:m.sample_volatility(list(map(float,five))),pairs(five,True)),
        ('E11 annualization',lambda:m.annualize_volatility(.01,252),root(F('.0252'))),
        ('E13 downside',lambda:m.downside_deviation([.1,-.1]),root(F('.005'))),
        ('E16 zero correlation',lambda:m.portfolio_volatility(.5,.2,.5,.2,0),root(F('.02'))),
        ('E17 positive correlation',lambda:m.portfolio_volatility(.5,.2,.5,.2,1),F('.2')),
        ('E18 ideal hedge',lambda:m.portfolio_volatility(.5,.2,.5,.2,-1),0),
        ('F105 finite mean despite sum overflow',lambda:m.mean_return([1e308,1e308]),F('1e308')),
        ('F105 integer spread survives input conversion',lambda:m.population_volatility([10**18,10**18+2]),1),
        ('F105 finite large population',lambda:m.population_volatility([-1e308,1e308]),F('1e308')),
        ('F105 finite large sample',lambda:m.sample_volatility([-1e308,1e308]),root(F('2e616'))),
        ('F105 tiny sample',lambda:m.sample_volatility([-1e-250,1e-250]),root(F('2e-500'))),
        ('F105 tiny downside',lambda:m.downside_deviation([-1e-250,1e-250]),root(F('5e-501'))),
        ('F105 large perfectly offset portfolio exposures',lambda:m.portfolio_volatility(1e308,2,1e308,2,-1),0),
        ('F105 tiny portfolio exposure',lambda:m.portfolio_volatility(.5,2e-250,.5,0,0),F('1e-250')),
        ('F105 near-cancelling portfolio exposure',lambda:m.portfolio_volatility(1,1e154,1,1e154,-.9999999999999999),root(F('2e292'))),
        ('project mean',lambda:m.mean_return(values),sum(days)/10),
        ('project population',lambda:m.population_volatility(values),pairs(days,False)),
        ('project sample',lambda:m.sample_volatility(values),pairs(days,True)),
        ('project annual',lambda:m.annualize_volatility(m.sample_volatility(values),252),pairs(days,True)*root(252)),
        ('project downside',lambda:m.downside_deviation(values),root(sum(x*x for x in days if x<0)/10)),
        ('project stressed sample',lambda:m.sample_volatility(values+[.15]),pairs(days+[F('.15')],True)),
        ('project stressed last window',lambda:m.rolling_sample_volatility(values+[.15],3)[-1],pairs(days[-2:]+[F('.15')],True)),
    ]:num(label,fn,want)
    ck('E8 independently derived sum of squared deviations',sum((x-y)**2 for x,y in combinations(five,2))/5==F('.00172'))
    ck('E14 complete four-observation windows',len(m.rolling_sample_volatility(values,4))==7)
    rolling=m.rolling_sample_volatility(values,3)
    ck('project eight complete windows',len(rolling)==8)
    for i,result in enumerate(rolling):close(f'project window ending day {i+3}',result,pairs(days[i:i+3],True),atol=0)
    ck('project latest window vs full sample',rolling[-1]<m.sample_volatility(values))
    for label,fn in [
        ('F105 nonrepresentable annual volatility',lambda:m.annualize_volatility(1e308,4)),
        ('F105 nonrepresentable sample',lambda:m.sample_volatility([-1.7e308,1.7e308])),
        ('F105 sample flag must be bool',lambda:m.downside_deviation([-.1,.1],sample='no')),
        ('missing observation',lambda:m.population_volatility([.1,None])),
    ]:reject(label,fn)
    ck('exact demo',commands[0]['stdout'].splitlines()==[
        f'Sample daily volatility: {pairs(five,True):.4%}',
        f'Annualized volatility (252-day convention): {pairs(five,True)*root(252):.4%}'])
    prose=source.read_text()
    ck('F105 printed five-day results match rounded roots',all(prose.count(f'{x:.4%}')>=2 for x in [pairs(five,True),pairs(five,False)]))
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
