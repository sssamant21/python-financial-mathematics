"""Section 12.17 exact assessment lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.17-exercises-and-applied-problems.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1217-') as tmp:
        Path(tmp,'chapter12_review.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['chapter12_review.py']),('isolated import',['-c','import chapter12_review']),('exact compilation',['-m','compileall','-q','chapter12_review.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['chapter12_review.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_assessment');exec(compile(code,str(source),'exec'),m.__dict__)
    import ast
    def pv(pos,bump=F(0)):
        face,c,n,f,y=pos
        value=F(str(face));c=value*F(str(c))/f
        base=1+(F(str(y))+bump)/f
        for _ in range(n):value=(value+c)/base
        return value
    def stats(pos):
        h=F('1e-8');v=pv(pos);u,d=pv(pos,h),pv(pos,-h)
        slope=(u-d)/(2*h);curvature=(u-2*v+d)/h**2
        mod=-slope/v
        return dict(price=v,macaulay=mod*(1+F(str(pos[-1]))/pos[3]),modified=mod,convexity=curvature/v,dv01=-slope/10000)
    def changes(pos,bp):
        dy=F(str(bp))/10000;a=stats(pos)
        linear=-a['price']*a['modified']*dy
        b=pv(pos,dy)
        return dict(exact=b-a['price'],duration=linear,duration_convexity=linear+a['price']*a['convexity']*dy**2/2,shocked_price=b)
    def matches(label,fn,want,rel=1e-12,atol=0):
        try: got=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,got.keys()==want.keys() and all(math.isclose(got[k],float(v),rel_tol=rel,abs_tol=atol) for k,v in want.items()),actual=repr(got),expected={k:float(v) for k,v in want.items()})
    def number(label,fn,want,atol=0):
        try:got=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,got,want,atol=atol)
    positions=[(1000,.06,6,2,.06),(2000,.04,10,2,.05),(1500,0,8,2,.045)]
    spec=lambda pos:(pos[0],pos[1],pos[2],pos[4],pos[3])
    def seq(label,fn,want,atol=0):
        want=tuple(want)
        try:got=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,len(got)==len(want) and all(math.isclose(a,float(b),rel_tol=1e-12,abs_tol=atol) for a,b in zip(got,want)),actual=repr(got),expected=[float(v) for v in want])
    for i,p in enumerate(positions,1):
        a=stats(p)
        seq(f'case bond {i} analytics',lambda:m.metrics(*spec(p)),a.values())
        f,c,n,mult,_=p
        flows=[(k/mult,f*F(str(c))/mult+(f if k==n else 0)) for k in range(1,n+1)]
        try:observed=m.cashflows(f,c,n,mult)
        except Exception as e:ck(f'F94 case bond {i} source cash flows',False,exception=repr(e))
        else:ck(f'F94 case bond {i} source cash flows',observed==flows)
    expected=[]
    for bp in (-200,-100,-50,50,100,200):
        rows=[changes(p,bp) for p in positions]
        keys=('exact','duration','duration_convexity')
        want=tuple(sum(w[k] for w in rows) for k in keys)
        for i,(p,w) in enumerate(zip(positions,rows),1):
            seq(f'case {bp:+} bp bond {i}',lambda:m.shock(*spec(p)[:4],bp,p[3]),(w[k] for k in keys),atol=1e-10)
        seq(f'F94 case {bp:+} bp portfolio',lambda:m.portfolio_shock([spec(p) for p in positions],bp),want,atol=1e-10)
        expected.append(f'Portfolio {bp:+} bp: '+', '.join(f'{float(v):.2f}' for v in want))
    losses=[changes(p,100)['exact'] for p in positions]
    ck('independent largest loss at +100 bp is B',losses.index(min(losses))==1,losses=[float(v) for v in losses])
    lines=commands[0]['stdout'].splitlines()
    ck('F94 demo portfolio lines and largest contributor',lines[-7:]==expected+[f'Largest +100 bp loss: B ({float(losses[1]):.2f})'],expected=expected)
    ck('demo five quote prices',lines[:5]==[f'YTM {k:.1f}%: price={float(pv((1000,.06,6,2,k/100))):.4f}' for k in range(4,9)])
    number('E4 premium fixture',lambda:m.price(1000,.08,6,.06),pv((1000,.08,6,2,.06)))
    number('E5 E8 matching par and YTM',lambda:m.price(1000,.06,6,.06),1000)
    number('E6 zero coupon price',lambda:m.price(1000,0,4,.04),1000/F('1.02')**4)
    ck('E7 rising yield lowers price',m.price(1000,.06,6,.06)<m.price(1000,.06,6,.05))
    ck('E9 E10 supplemental accrual arithmetic',F('99.25')+F('.80')==F('100.05') and round(float(F(30)*F(40,180)),2)==6.67)
    ck('E11–E14 duration and convexity arithmetic',round(float(F('4.2')/F('1.025')),5)==4.09756 and -50000*4*F('.0025')==-500 and 50000*4*F('.0001')==20 and -1000*F('4.5')*F('.01')+F(1000*25,2)*F('.01')**2==F('-43.75'))
    number('E16 source factor via unit flow',lambda:m.spot_pv([(2,1)],{2:.04}),F('1.04')**-2)
    number('E17 spot PV',lambda:m.spot_pv([(1,30),(2,1030)],{1:.04,2:.05}),30/F('1.04')+1030/F('1.05')**2)
    number('E18 annual forward',lambda:m.forward(float(1/F('1.03')),float(F('1.035')**-2),1,2),F('1.035')**2/F('1.03')-1)
    ck('E19–E22 supplemental signed risk and compounding',12+18+25==55 and -55*10==-550 and 100-80==20 and F('.041')-F('.048')==F('-.007') and F('1.03')**2-1==F('.0609'))
    number('E23 negative rate factor',lambda:m.spot_pv([(2,1)],{2:-.01}),F('.99')**-2)
    seq('F94 tiny nonzero shock preserved',lambda:m.shock(1000,.06,6,.06,1e-21),(changes(positions[0],1e-21)[k] for k in ('exact','duration','duration_convexity')))
    number('F54 finite PV after discount-factor underflow',lambda:m.spot_pv([(1000,1e308)],{1000:2}),float(F('1e308')/3**1000))
    number('F54 finite scaled price',lambda:m.price(1e308,2,4,2,4),F('1e308'))
    for label,fn in [
        ('F94 normalized time-zero factor',lambda:m.forward(.9,.8,0,1)),
        ('F54 reject unrepresentable price',lambda:m.price(1e-300,0,2,1e200,1)),
        ('F54 reject unrepresentable spot PV',lambda:m.spot_pv([(2,1e308)],{2:-.9})),
        ('reject missing spot',lambda:m.spot_pv([(2,100)],{1:.04})),
    ]:reject(label,fn)
    ck('F94 worked case states aggregate and contributor', f'{abs(float(sum(losses))):.2f}' in source.read_text() and f'{abs(float(losses[1])):.2f}' in source.read_text())
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,chapterwide_answer_records=24,applied_case_records=7,conceptual_prompts=[15,24],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
