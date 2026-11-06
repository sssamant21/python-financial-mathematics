"""Section 13.3 exact gross returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.03-gross-returns.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1303-') as tmp:
        Path(tmp,'gross_returns.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['gross_returns.py']),('isolated import',['-c','import gross_returns']),('exact compilation',['-m','compileall','-q','gross_returns.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['gross_returns.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_gross');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    import ast
    def calc(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    def power(g,n,d):
        with localcontext() as ctx:
            ctx.prec=65
            return (D(g.numerator)/D(g.denominator))**(D(n)/d)-1
    for r,g in [(.12,'1.12'),(-.25,'.75'),(0,'1'),(-1,'0')]:
        calc(f'E1–E4 gross factor {r}',lambda:m.gross_factor(r),F(g))
    calc('E5 inverse gain',lambda:m.simple_from_gross(1.08),F('.08'))
    calc('E6 inverse loss',lambda:m.simple_from_gross(.92),F('-.08'))
    calc('E7 price factor',lambda:m.factor_from_prices(100,110),F('1.1'))
    demo=[.1,-.1,.05,-.02]
    for k,w in [(2,F('.99')),(3,F('1.0395')),(4,F('1.01871'))]:
        calc(f'E8–E10 {k} periods factor',lambda:m.linked_factor(demo[:k]),w)
        calc(f'E8–E10 {k} periods return',lambda:m.linked_return(demo[:k]),w-1)
    ck('E11 gross wealth calculation',F(10000)*F('1.01871')==F('10187.10'))
    calc('E12 E13 geometric average',lambda:m.geometric_mean(demo[:2]),power(F('.99'),1,2))
    calc('E14 annualization',lambda:m.annualized_from_factor(1.21,2),F('.1'))
    calc('E15 income net of cost',lambda:m.factor_from_total_wealth(100,105,3,1),F('1.07'))
    calc('E16 FX gross',lambda:m.fx_factor(.08,-.02),F('1.0584'))
    ck('E17 supplemental beginning-weight arithmetic',F('.6')*F('1.1')+F('.4')*F('.95')==F('1.04'))
    calc('E18 geometric total loss branch',lambda:m.geometric_mean([.1,-1,.2]),-1)
    days=list(map(F,('.03','-.02','.04','-.01','.02')))
    total=F(1)
    for i,r in enumerate(days,1):
        total*=1+r
        prefix=list(map(float,days[:i]))
        calc(f'project day {i} factor',lambda:m.gross_factor(float(r)),1+r)
        calc(f'project day {i} cumulative factor',lambda:m.linked_factor(prefix),total)
        calc(f'project day {i} cumulative return',lambda:m.linked_return(prefix),total-1)
    values=list(map(float,days));factor=m.linked_factor(values)
    calc('project final wealth',lambda:25000*factor,25000*total)
    calc('project geometric daily mean',lambda:m.geometric_mean(values),power(total,1,5))
    calc('project annualization with 252 trading days',lambda:m.annualized_from_factor(factor,5/252),power(total,252,5))
    ck('project arithmetic mean supplemental',sum(days)/5==F('.012'))
    calc('project zero-factor wealth path',lambda:m.linked_factor([.03,-1,.04]),0)
    calc('F97 tiny geometric gain survives rounded gross factor',lambda:m.geometric_mean([1e-30]),F('1e-30'))
    calc('F95 tiny linked return',lambda:m.linked_return([1e-30]),F('1e-30'))
    calc('F54 linked factor survives intermediate overflow',lambda:m.linked_factor([1e170,1e170]+[-.999999]*30),(1+F('1e170'))**2*F('1e-6')**30)
    calc('F54 finite wealth factor despite intermediate overflow',lambda:m.factor_from_total_wealth(1e307,1e308,1e308,1e308),10)
    for label,fn in [
        ('F54 overflowed linked factor rejected',lambda:m.linked_factor([1e308,1e308])),
        ('F54 positive factor underflow rejected',lambda:m.factor_from_prices(1e308,1e-308)),
        ('F54 annualized overflow rejected',lambda:m.annualized_from_factor(2,.0001)),
        ('F97 positive annual gross cannot report total loss',lambda:m.annualized_from_factor(.1,.001)),
        ('negative terminal wealth rejected',lambda:m.factor_from_total_wealth(100,0,0,1)),
    ]:reject(label,fn)
    lines=commands[0]['stdout'].splitlines()
    ck('exact demo factors',len(lines)==4 and ast.literal_eval(lines[0].split(': ',1)[1])==[1.1,.9,1.05,.98])
    for i,w in [(1,F('1.01871')),(2,F('.01871')),(3,power(F('1.01871'),1,4))]:
        ck(f'exact demo line {i}',len(lines)==4 and math.isclose(float(lines[i].split(': ',1)[1]),float(w),rel_tol=1e-12))
    ck('F97 worked project states final results',f'{float(25000*total):,.2f}' in source.read_text() and '252' in source.read_text())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
