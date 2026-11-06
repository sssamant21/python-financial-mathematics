"""Section 13.9 exact time-weighted returns lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-13/13.09-time-weighted-return.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1309-') as tmp:
        Path(tmp,'time_weighted_return.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['time_weighted_return.py']),('isolated import',['-c','import time_weighted_return']),('exact compilation',['-m','compileall','-q','time_weighted_return.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['time_weighted_return.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_twr');exec(compile(code,str(source),'exec'),m.__dict__)
    def num(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    for label,fn,want in [
        ('E1 one gain',lambda:m.subperiod_return(100,110),F(1,10)),
        ('E2 one loss',lambda:m.subperiod_return(160,144),F(-1,10)),
        ('E3 linked gain/loss',lambda:m.link_returns([.1,-.1]),F(-1,100)),
        ('E7 post-withdrawal',lambda:m.subperiod_return(90,99),F(1,10)),
        ('E8 linked withdrawal',lambda:m.exact_twr(100,[(110,-20),(99,0)]),F(21,100)),
        ('E10 quarterly factor 131222/125000',lambda:m.link_returns([.03,-.02,.04]),F(6222,125000)),
        ('E13 Dietz midpoint',lambda:m.modified_dietz(100,165,[(50,.5)]),F(3,25)),
        ('E14 zero profit',lambda:m.exact_twr(100,[(100,50),(150,0)]),0),
        ('§3 exact contribution',lambda:m.exact_twr(100,[(110,50),(144,0)]),F(-1,100)),
        ('§5 genuine depletion with recapitalization',lambda:m.exact_twr(100,[(0,100),(130,0)]),-1),
        ('§8 weight endpoints with signed flows',lambda:m.modified_dietz(100,140,[(50,1),(-25,0)]),F(1,10)),
        ('F103 tiny subperiod gain',lambda:m.subperiod_return(10**18,10**18+1),F(1,10**18)),
        ('F103 tiny subperiod loss',lambda:m.subperiod_return(10**18,10**18-1),F(-1,10**18)),
        ('F103 tiny linked loss',lambda:m.link_returns([-1e-18]),F(-1,10**18)),
        ('F103 tiny exact gain',lambda:m.exact_twr(10**18,[(10**18+1,0)]),F(1,10**18)),
        ('F103 offsetting huge factors',lambda:m.exact_twr(1e-308,[(1e308,0),(2e-308,0)]),1),
        ('F103 exact post-flow opening',lambda:m.exact_twr(1e308,[(1e308,1e308),(1e308,0)]),F(-1,2)),
        ('F103 true total loss after linked overflow',lambda:m.link_returns([1e308,1e308,-1]),-1),
        ('F103 Dietz offsetting large flows',lambda:m.modified_dietz(100,110,[(1e308,.5),(1e308,.5),(-1e308,.5),(-1e308,.5)]),F(1,10)),
    ]:num(label,fn,want)
    for label,fn in [
        ('F103 nonrepresentable subperiod',lambda:m.subperiod_return(1e-308,1e308)),
        ('F103 rounded subperiod total loss',lambda:m.subperiod_return(1e308,1)),
        ('F103 nonrepresentable linked return',lambda:m.link_returns([1e308,1e308])),
        ('F103 rounded linked total loss',lambda:m.link_returns([-.99]*10)),
        ('F103 rounded exact total loss',lambda:m.exact_twr(1e308,[(1,0)])),
        ('F103 oversized Dietz output',lambda:m.modified_dietz(1e-308,1e308,[])),
        ('empty ledger',lambda:m.exact_twr(100,[])),
        ('missing valuation',lambda:m.exact_twr(100,[(None,0)])),
        ('nonfinite external flow',lambda:m.exact_twr(100,[(100,float('inf')),(100,0)])),
        ('negative post-flow capital',lambda:m.exact_twr(100,[(100,-101),(100,0)])),
        ('flow at final event',lambda:m.exact_twr(100,[(100,1)])),
        ('zero weighted capital',lambda:m.modified_dietz(100,100,[(-100,1)])),
    ]:reject(label,fn)
    # Independent project benchmark: start with a unit price of 1 and issue
    # or redeem shares at the pre-flow price. External flows change units.
    from project import ledger, csv_text
    rows=[(1,1080,200),(2,1216,-100),(3,F('1227.60'),0)]
    shares=F(1000); index=[]
    for _,end,flow in rows:
        price=end/shares;index.append(100*price);shares+=flow/price
    report=ledger(1000,rows)
    ck('project row contracts',[(r.opening,r.post_flow,r.period_return) for r in report]==[
        (1000,1280,F(2,25)),(1280,1116,F(-1,20)),(1116,F('1227.60'),F(1,10))])
    ck('project supplemental index matches independent share accounting',[r.index for r in report]==index==list(map(F,('108','102.60','112.86'))))
    num('project exact TWR matches independent unit price',lambda:m.exact_twr(1000,[(float(v),float(f)) for _,v,f in rows]),index[-1]/100-1)
    ck('project naive growth and net flows',rows[-1][1]/1000-1==F('.2276') and sum(r[2] for r in rows)==100)
    import csv,io
    table=list(csv.DictReader(io.StringIO(csv_text(report))))
    ck('project supplemental CSV contract',len(table)==3 and list(table[0])==['event','opening','pre_flow','flow','post_flow','period_return','index'] and F(table[-1]['pre_flow'])==F('1227.60') and F(table[-1]['period_return'])==F('.1'))
    for label,data in [
        ('duplicate order',[rows[0],(1,1216,-100),rows[2]]),
        ('reverse order',[rows[1],rows[0],rows[2]]),
        ('missing valuation',[(1,None,200),*rows[1:]]),
        ('nonfinite flow',[(1,1080,float('inf')),*rows[1:]]),
        ('zero capital',[(1,1080,-1080),*rows[1:]]),
    ]:reject('project supplemental '+label,lambda:ledger(1000,data))
    ck('F103 project order field and worked index supplied','Event order' in source.read_text() and '102.60 → 112.86' in source.read_text())
    ck('exact demo',commands[0]['stdout'].splitlines()==['Exact TWR: -1.00%','Modified Dietz illustration: 12.00%'])
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[15,16,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
