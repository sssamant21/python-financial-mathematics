"""Section 10.13 exact lab and independent IRR benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.13-irr-and-numerical-root-finding.md'
    code,=re.findall(rb'^\x60\x60\x60python\n(.*?)^\x60\x60\x60',source.read_bytes(),re.M|re.S)
    commands=[];checks=[]
    def ck(label,ok,**detail):checks.append(dict(label=label,passed=bool(ok),**detail))
    def close(label,value,expected,atol=1e-10,rtol=1e-12):
        ck(label,math.isclose(value,float(expected),abs_tol=atol,rel_tol=rtol),actual=value if math.isfinite(value) else repr(value),rational_reference=str(expected),absolute_tolerance=atol,relative_tolerance=rtol)
    def reject(label,fn):
        try:actual=fn()
        except (TypeError,ValueError) as e:ck(label,True,exception=repr(e))
        except Exception as e:ck(label,False,exception=repr(e))
        else:ck(label,False,actual=repr(actual))
    with tempfile.TemporaryDirectory(prefix='book1-1013-') as tmp:
        Path(tmp,'irr_root_finding.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['irr_root_finding.py']),('exact compilation',['-m','compileall','-q','irr_root_finding.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout.startswith('IRR: ') if args==['irr_root_finding.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_irr');exec(compile(code,str(source),'exec'),m.__dict__)
    from decimal import Decimal as D,localcontext
    with localcontext() as ctx:
        ctx.prec=100
        two=(D(69).sqrt()-7)/10
    def residual(r,flows):
        with localcontext() as ctx:
            ctx.prec=100
            base=1+D.from_float(float(r))
            return sum((D.from_float(float(v))/base**t for t,v in enumerate(flows)),D(0))
    def probe(label,fn,expected,atol=1e-10):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected,atol=atol)
    for label,flows,low,high,expected in [
        ('P2 one-period',[-100,110],0,1,F(1,10)),
        ('P3 negative IRR',[-100,90],-.5,0,F(-1,10)),
        ('P4 zero IRR',[-100,100],0,1,F(0)),
        ('P5 quadratic IRR',[-100,60,60],0,1,two),
        ('P8 first root',[-100,230,-132],.05,.15,F(1,10)),
        ('P8 second root',[-100,230,-132],.15,.3,F(1,5)),
        ('P6 upper endpoint',[-100,200],0,1,F(1)),
        ('reverse cash-flow signs',[100,-110],0,1,F(1,10))]:
        actual=m.irr_bisect(iter(flows),low,high)
        close(label,actual,expected)
        value=residual(actual,flows)
        ck(label+' independent residual and bracket',abs(value)<D('1e-8') and low<=actual<=high,residual=str(value))
    demo=float(commands[0]['stdout'].split(':',1)[1])
    close('exact demonstration vs quadratic',demo,two)
    ck('P6 endpoints bracket conventional root',residual(0,[-100,110])>0>residual(1,[-100,110]))
    ck('P7 tangent root exact derivation',-100*F(11,10)**2+220*F(11,10)-121==0)
    annual=F(101,100)**12-1
    ck('P10 supplemental monthly conversion',round(float(annual)*100,5)==12.68250,exact=str(annual))
    probe('F60 tiny scaled root',lambda:m.irr_bisect([-1e-200,1.1e-200]),F(1,10))
    huge=F(1)/F(7e-309)-1
    probe('F60 finite midpoint with large endpoints',lambda:m.irr_bisect([-7e-309,1],1e308,1.7e308,tol=1e296),huge,0)
    probe('F56 zero flow does not require a factor',lambda:m.npv(-.9,[0]*400),F(0),0)
    for label,fn in [
        ('P7 tangent not detected by sign bracket',lambda:m.irr_bisect([-100,220,-121],0,.3)),
        ('P8 wide bracket can hide two roots',lambda:m.irr_bisect([-100,230,-132],0,.3)),
        ('F60 tiny same-sign bracket',lambda:m.irr_bisect([-1e-200,5e-201],0,1)),
        ('F54 discounted nonzero term underflow',lambda:m.npv(1,[0,5e-324])),
        ('F61 infinite tolerance',lambda:m.irr_bisect([-100,110],tol=float('inf'))),
        ('F61 bool rate',lambda:m.npv(True,[-100,110])),
        ('F61 bool flow',lambda:m.irr_bisect([True,-1.1])),
        ('F61 bool iteration cap',lambda:m.irr_bisect([-100,200],max_iter=True)),
        ('invalid bracket',lambda:m.irr_bisect([-100,110],.5,.1)),
        ('same-sign flows',lambda:m.irr_bisect([100,200]))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[1,6,7,9,11,12],supplemental_arithmetic=[10],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
