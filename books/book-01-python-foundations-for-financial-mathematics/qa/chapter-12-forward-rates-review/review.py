"""Section 12.15 exact forwards lab and rational benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=Path(sys.argv[1]) if len(sys.argv)>1 else BOOK/'chapter-12/12.15-forward-rates.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1215-') as tmp:
        Path(tmp,'forward_rates.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['forward_rates.py']),('exact compilation',['-m','compileall','-q','forward_rates.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) if args==['forward_rates.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_forward');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D, localcontext
    def number(label,fn,want):
        try:value=fn()
        except Exception as e:ck(label,False,exception=repr(e))
        else:close(label,value,want,atol=0)
    def dec(x):
        return D(x.numerator)/D(x.denominator)
    base=[(1,F('.03')),(2,F('.035')),(3,F('.04')),(5,F('.045'))]
    demo=[];changes={}
    for label,dy in [('base',F(0)),('shifted',F('.005'))]:
        nodes=[(t,float(r+dy)) for t,r in base]
        got=m.forward_table(nodes)
        ck(label+' count',len(got)==4)
        prior=0; a=F(1)
        for (t,r),row in zip(base,got):
            r+=dy; b=(1+r)**-t
            with localcontext() as ctx:
                ctx.prec=65
                f=dec(a/b)**(D(1)/(t-prior))-1
                fc=dec(a/b).ln()/(t-prior)
            ck(f'{label} {prior}–{t} timeline and spot',row[:3]==(prior,t,float(r)))
            close(f'{label} {t} discount',row[3],b,atol=0)
            close(f'{label} {prior}–{t} forward',row[4],f,atol=0)
            number(f'{label} {prior}–{t} reconstruct',lambda:m.forward_df(float(a),row[4],prior,t),b)
            number(f'{label} {prior}–{t} continuous conversion',lambda:m.forward_from_dfs(float(a),float(b),prior,t,'continuous'),fc)
            if not dy:
                demo.append(f'{prior:g}-{t:g}y spot={float(r):.3%} DF={float(b):.8f} implied_forward={float(f):.4%}')
                changes[t]=f
            else:changes[t]=f-changes[t]
            prior,a=t,b
    ck('parallel spot shift changes forward intervals differently',max(changes.values())-min(changes.values())>D('1e-8'),forward_changes={t:float(v) for t,v in changes.items()})
    ck('exact demo',commands[0]['stdout'].splitlines()==demo,expected=demo)
    number('P12 continuous forward',lambda:m.forward_from_spots(.03,.04,1,2,'continuous'),F('.05'))
    with localcontext() as ctx:
        ctx.prec=65
        ratio=F('1.01')**8/F('1.0075')**4
        periodic=4*(dec(ratio).sqrt().sqrt()-1)
    number('P13 nominal quarterly forward',lambda:m.forward_from_spots(.03,.04,1,2,'periodic',4),periodic)
    number('P16 negative forward',lambda:m.forward_from_spots(.05,.02,1,2),F('1.02')**2/F('1.05')-1)
    number('F92 tiny forward from spots',lambda:m.forward_from_spots(1e-50,1e-50,1,2),F('1e-50'))
    number('F54 forward despite standalone discounts underflowing',lambda:m.forward_from_spots(2,2,1000,1001),2)
    number('F54 scaled reconstruction despite standalone discount underflow',lambda:m.forward_df(1e308,2,1,1001),F('1e308')/3**1000)
    for label,fn in [
        ('F92 normalized time-zero factor',lambda:m.forward_from_dfs(.9,.8,0,1)),
        ('F92 reject invalid start quote at time zero',lambda:m.forward_from_spots(float('nan'),.03,0,1)),
        ('F92 reject forward rounded to lower bound',lambda:m.forward_from_dfs(1e-308,1e308,1,2)),
        ('F54 reject underflowed discount factor',lambda:m.discount_factor(2,1000)),
        ('F54 reject overflowed reconstruction',lambda:m.forward_df(1e308,-.9,1,2)),
        ('invalid reversed node order',lambda:m.forward_table([(2,.04),(1,.03)])),
    ]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=18,mini_project_records=1,conceptual_prompts=[1,2,17,18],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
