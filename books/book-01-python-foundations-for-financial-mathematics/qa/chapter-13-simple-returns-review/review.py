"""Section 13.2 exact simple returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.02-simple-returns.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1302-') as tmp:
        Path(tmp,'simple_returns.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['simple_returns.py']),('isolated import',['-c','import simple_returns']),('exact compilation',['-m','compileall','-q','simple_returns.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['simple_returns.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_simple');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D
    def numeric(label,fn,want,atol=0):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=atol)
    for label,fn,want in [
        ('E1 price gain',lambda:m.simple_return(100,112),F('.12')),
        ('E2 price loss',lambda:m.simple_return(100,88),F('-.12')),
        ('E3 flat price',lambda:m.simple_return(100,100),0),
        ('E4 total loss',lambda:m.simple_return(100,0),-1),
        ('E5 E6 price and dollar gain',lambda:m.simple_return(250,280),F(30,250)),
        ('E7 gross factor',lambda:m.wealth_after(1,.08),F('1.08')),
        ('E8 loss gross factor',lambda:m.wealth_after(1,-.3),F('.7')),
        ('E9 distribution',lambda:m.total_return(100,105,3),F('.08')),
        ('E10 net of cost',lambda:m.total_return(100,105,3,1),F('.07')),
        ('E11 two linked returns',lambda:m.link_returns([.1,-.1]),F('-.01')),
        ('E12 three linked returns',lambda:m.link_returns([.1,-.1,.1]),F('.089')),
        ('E13 arithmetic average',lambda:m.arithmetic_average([.1,-.1]),0),
        ('E15 recovery 20%',lambda:m.wealth_after(m.wealth_after(100,-.2),.25),100),
        ('E16 recovery 50%',lambda:m.wealth_after(m.wealth_after(100,-.5),1),100),
        ('E17 FX return',lambda:m.fx_converted_return(.08,-.02),F('.0584')),
        ('F96 tiny FX return',lambda:m.fx_converted_return(1e-30,0),F('1e-30')),
        ('F95 tiny linked return',lambda:m.link_returns([1e-30]),F('1e-30')),
        ('F54 finite mean despite sum overflow',lambda:m.arithmetic_average([1e308,1e308]),F('1e308')),
        ('F54 finite wealth despite intermediate rounding',lambda:m.wealth_after(1e-308,1e308),1),
        ('F54 finite total despite intermediate overflow',lambda:m.total_return(1e307,1e308,1e308,1e308),9),
    ]:numeric(label,fn,want)
    ck('E14 supplemental geometric mean',round(100*float(D('.99').sqrt()-1),4)==-.5013)
    values=[100,103,99.91,104.9055,102.80739]
    changes=[F('.03'),F('-.03'),F('.05'),F('-.02')]
    rs=m.period_returns(values)
    for k,(x,w) in enumerate(zip(rs,changes),1):
        numeric(f'project daily return {k}',lambda:x,w)
        numeric(f'project gross factor {k}',lambda:m.wealth_after(1,x),1+w)
    exact=F('102.80739')/100-1
    numeric('project arithmetic average',lambda:m.arithmetic_average(rs),F('.0075'))
    numeric('project linked endpoint reconciliation',lambda:m.link_returns(rs),exact)
    numeric('project direct endpoint',lambda:m.simple_return(values[0],values[-1]),exact)
    numeric('project terminal dividend increases total by 0.5pp',lambda:m.total_return(values[0],values[-1],.5),exact+F('.005'))
    for label,fn in [
        ('E18 zero denominator rejected',lambda:m.simple_return(0,10)),
        ('F96 negative terminal wealth rejected',lambda:m.total_return(100,0,0,1)),
        ('F54 wealth overflow rejected',lambda:m.wealth_after(1e308,1e308)),
        ('F54 price return overflow rejected',lambda:m.simple_return(1e-308,1e308)),
        ('F54 FX result overflow rejected',lambda:m.fx_converted_return(1e308,1e308)),
        ('F54 linked result overflow rejected',lambda:m.link_returns([1e308,1e308])),
    ]:reject(label,fn)
    import ast
    lines=commands[0]['stdout'].splitlines()
    ck('demo raw prices and period returns',len(lines)==5 and ast.literal_eval(lines[0].split(': ',1)[1])==[100,110,99,108.9] and ast.literal_eval(lines[1].split(': ',1)[1])==[.1,-.1,.1])
    for idx,want in [(2,F(1,30)),(3,F('.089')),(4,F('.089'))]:
        ck(f'demo numeric line {idx}',len(lines)==5 and math.isclose(float(lines[idx].split(': ',1)[1]),float(want),rel_tol=1e-12))
    ck('F96 worked project supplies average and total result','0.75%' in source.read_text() and '3.30739%' in source.read_text())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
