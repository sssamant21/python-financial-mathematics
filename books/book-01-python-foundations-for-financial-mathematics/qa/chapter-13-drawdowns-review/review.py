"""Section 13.12 exact drawdowns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.12-drawdowns.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1312-') as tmp:
        Path(tmp,'drawdowns.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['drawdowns.py']),('isolated import',['-c','import drawdowns']),('exact compilation',['-m','compileall','-q','drawdowns.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['drawdowns.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_drawdowns');exec(compile(code,str(source),'exec'),m.__dict__)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E2 current drawdown',lambda:m.drawdown_series([120,90])[-1],F(-1,4)),
        ('E3 maximum drawdown',lambda:m.max_drawdown([100,120,90,105]),F(-1,4)),
        ('E4 partial recovery',lambda:m.drawdown_series([120,105])[-1],F(-1,8)),
        ('E5 full recovery',lambda:m.drawdown_series([120,90,120])[-1],0),
        ('E12 compounded wealth',lambda:m.wealth_from_returns(100,[.2,-.25])[-1],90),
        ('E13 wealth after trough',lambda:m.wealth_from_returns(90,[.1])[-1],99),
        ('E13 remaining drawdown',lambda:m.drawdown_series([120,99])[-1],F(-7,40)),
        ('E14 underwater duration',lambda:m.longest_underwater_run([100,120,90,100,120]),2),
        ('§4 half then up half',lambda:m.wealth_from_returns(100,[-.5,.5])[-1],75),
        ('F106 tiny actual drawdown',lambda:m.max_drawdown([10**18,10**18-1]),F(-1,10**18)),
        ('F106 tiny recovery gain',lambda:m.recovery_gain(-1e-18),F(1,10**18-1)),
        ('F106 tied peak starts new episode',lambda:m.worst_drawdown_episode([100,95,100,80])['peak_index'],2),
        ('F106 genuine zero remains zero',lambda:m.wealth_from_returns(100,[-1,1e308])[-1],0),
    ]:num(label,fn,want)
    for i,loss in enumerate(map(F,('.1','.2','.25','.5','.8')),6):
        num(f'E{i} gain on remaining capital',lambda:m.recovery_gain(float(-loss)),loss/(1-loss))
    ck('E11 no finite recovery gain from zero',m.recovery_gain(-1)==math.inf)
    ep=m.worst_drawdown_episode([100,120,90])
    ck('E15–16 zero-based peak and trough',(ep['peak_index'],ep['trough_index'])==(1,2))
    p=m.wealth_from_returns(100,[.25,-.2,-.2]);q=m.wealth_from_returns(100,[-.2,.25,-.2])
    ck('E18 path dependence',p[-1]==q[-1] and m.max_drawdown(p)<m.max_drawdown(q))
    for label,fn in [
        ('F106 nonrepresentable wealth',lambda:m.wealth_from_returns(1e308,[1])),
        ('F106 positive wealth below float range',lambda:m.wealth_from_returns(5e-324,[-.99])),
        ('F106 positive wealth cannot report complete loss',lambda:m.drawdown_series([1e308,1])),
        ('project missing valuation',lambda:m.drawdown_series([100,108,104,112,98,None,100,112,118])),
    ]:reject(label,fn)

    from project import dashboard, ledger_csv
    values=[100,108,104,112,98,91,100,112,118]
    # Enumerate ordered pairs independently of the running-maximum algorithm.
    score,peak,trough=min((F(end,start)-1,i,j) for j,end in enumerate(values) for i,start in enumerate(values[:j+1]))
    recovery=next(i for i in range(trough+1,len(values)) if values[i]>=values[peak])
    states=['ok','ok','ok','ok','warning','critical','warning','ok','ok']
    rows=dashboard(values,m)
    for j,row in enumerate(rows):
        expected=min(F(values[j],previous)-1 for previous in values[:j+1])
        close(f'project observation {j} drawdown',row[3],expected,atol=0)
        ck(f'project observation {j} peak and alert',row[2]==max(values[:j+1]) and row[4]==states[j])
    ep=m.worst_drawdown_episode(values)
    ck('project worst episode and recovery',ep=={'depth':float(score),'peak_index':peak,'trough_index':trough} and (peak,trough,recovery)==(3,5,7))
    num('project recovery gain',lambda:m.recovery_gain(float(score)),F(21,91))
    num('project longest underwater run',lambda:m.longest_underwater_run(values),3)
    ck('project forward fill conceals trough',m.max_drawdown(values[:5]+[values[4]]+values[6:])==-.125)
    import csv,io
    parsed=list(csv.DictReader(io.StringIO(ledger_csv(rows))))
    ck('project supplemental CSV rows and alert',len(parsed)==9 and parsed[5]['observation']=='5' and parsed[5]['alert']=='critical')
    ck('exact demo',commands[0]['stdout'].splitlines()[-1]=='Maximum drawdown: -25.00%')
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
