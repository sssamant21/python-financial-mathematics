"""Section 13.4 exact logarithmic returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.04-logarithmic-returns.md'
    *fragments,code=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),independent_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1304-') as tmp:
        Path(tmp,'logarithmic_returns.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['logarithmic_returns.py']),('isolated import',['-c','import logarithmic_returns']),('exact compilation',['-m','compileall','-q','logarithmic_returns.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['logarithmic_returns.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_logs');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    import ast
    def ln(x):
        with localcontext() as ctx:
            ctx.prec=85
            v=F(x)
            return (D(v.numerator)/D(v.denominator)).ln()
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    ck('two contextual source fragments inventoried',len(fragments)==2)
    fixture=dict(math=math,R=.08,ell=float(ln('1.08')))
    for i,(fragment,want) in enumerate(zip(fragments,(ln('1.08'),F('.08'))),1):
        numeric(f'contextual source fragment {i}',lambda:eval(compile(fragment,str(source),'eval'),fixture),want)
    for label,fn,want in [
        ('E1 positive log return',lambda:m.log_from_simple(.1),ln('1.1')),
        ('E2 negative log return',lambda:m.log_from_simple(-.1),ln('.9')),
        ('E3 zero',lambda:m.log_from_simple(0),0),
        ('E4 price ratio',lambda:m.log_from_prices(100,110),ln('1.1')),
        ('E5 inverse positive',lambda:m.simple_from_log(float(ln('1.08'))),F('.08')),
        ('E6 inverse negative',lambda:m.simple_from_log(float(ln('.95'))),F('-.05')),
        ('E7 two log periods',lambda:m.sum_log_returns([.1,-.1]),ln('.99')),
        ('E8 linked two periods',lambda:m.linked_simple([.1,-.1]),F('-.01')),
        ('E9 three-period gross',lambda:1+m.linked_simple([.1,-.1,.1]),F('1.089')),
        ('E10 three-period log',lambda:m.sum_log_returns([.1,-.1,.1]),ln('1.089')),
        ('E12 small log',lambda:m.log_from_simple(1e-6),ln('1.000001')),
        ('E13 annualized log',lambda:m.annualized_log(float(ln('1.21')),2),ln('1.1')),
        ('E14 annual-effective equivalent',lambda:m.simple_from_log(float(ln('1.1'))),F('.1')),
        ('E15 domestic log',lambda:m.domestic_log_return(.08,-.02),ln('1.0584')),
        ('F98 finite log of extreme positive price ratio',lambda:m.log_from_prices(1e-308,1e308),ln(F('1e616'))),
        ('F98 finite log of extreme negative price ratio',lambda:m.log_from_prices(1e308,1e-308),ln(F('1e-616'))),
        ('F98 linked exact recovery',lambda:m.linked_simple([-.2,.25]),0),
        ('F98 aggregate log preserves tiny gain between recovery factors',lambda:m.sum_log_returns([-.2,1e-30,.25]),D('1e-30')),
    ]:numeric(label,fn,want)
    ck('E16 E17 supplemental portfolio aggregation',F('.5')*F('.2')+F('.5')*F('-.2')==0 and ln('1.2')/2+ln('.8')/2<0)
    prices=[100,103,99.91,104.9055,102.80739]
    simple=list(map(F,('.03','-.03','.05','-.02')))
    logs=m.log_return_series(prices);product=F(1)
    for i,(r,obs) in enumerate(zip(simple,logs),1):
        product*=1+r
        numeric(f'project log series row {i}',lambda:obs,ln(1+r))
        numeric(f'project source conversion row {i}',lambda:m.log_from_simple(float(r)),ln(1+r))
        numeric(f'project cumulative row {i}',lambda:m.linked_simple(list(map(float,simple[:i]))),product-1)
    numeric('project endpoint log',lambda:m.log_from_prices(prices[0],prices[-1]),ln(product))
    numeric('project sum of source logs',lambda:math.fsum(logs),ln(product))
    numeric('project inverse linked',lambda:m.simple_from_log(math.fsum(logs)),product-1)
    ck('project means differ',sum(simple)/len(simple)==F('.0075') and not math.isclose(math.fsum(logs)/len(logs),.0075))
    ck('project zero terminal price has simple return minus one',(F(0)-F(str(prices[-1])))/F(str(prices[-1]))==-1)
    for label,fn in [
        ('E11 total loss log rejected',lambda:m.log_from_simple(-1)),
        ('project zero terminal price rejected by log series',lambda:m.log_return_series(prices+[0])),
        ('F54 unrepresentable annual log rejected',lambda:m.annualized_log(1e308,1e-308)),
        ('F54 overflowing inverse rejected',lambda:m.simple_from_log(1000)),
        ('F98 positive gross cannot report total loss',lambda:m.simple_from_log(-100)),
    ]:reject(label,fn)
    lines=commands[0]['stdout'].splitlines()
    ck('demo prices and logs',len(lines)==5 and ast.literal_eval(lines[0].split(': ',1)[1])==[100,110,99,108.9] and ast.literal_eval(lines[1].split(': ',1)[1])==[round(float(ln(r)),8) for r in ('1.1','.9','1.1')])
    for i,w in [(2,ln('1.089')),(3,ln('1.089')),(4,F('.089'))]:
        ck(f'demo line {i}',len(lines)==5 and math.isclose(float(lines[i].split(': ',1)[1]),float(w),rel_tol=1e-12))
    ck('F98 E10 shown at six-place rounding',f'{float(ln("1.089")):.6f}' in source.read_text())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,contextual_fragments=2,conceptual_prompts=[11,16,17],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
