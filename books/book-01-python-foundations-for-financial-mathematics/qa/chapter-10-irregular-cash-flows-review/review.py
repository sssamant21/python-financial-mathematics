"""Section 10.11 exact lab and independent ACT/365 Fixed benchmarks."""
import hashlib,json,math,platform,re,subprocess,sys,tempfile,types
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;BOOK=HERE.parents[1]
def main():
    source=BOOK/'chapter-10/10.11-irregular-cash-flows.md'
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
    with tempfile.TemporaryDirectory(prefix='book1-1011-') as tmp:
        Path(tmp,'irregular_cash_flows.py').write_bytes(code)
        for label,args in [('exact demonstration and embedded tests',['irregular_cash_flows.py']),('exact compilation',['-m','compileall','-q','irregular_cash_flows.py'])]:
            p=subprocess.run([sys.executable,'-B',*args],cwd=tmp,capture_output=True,text=True,timeout=60)
            match=re.search(r'Ran (\d+) tests',p.stderr);methods=int(match[1]) if match else None
            expected=methods==12 and bool(re.search(r'^OK\s*$',p.stderr,re.M)) and p.stdout=='' if args==['irregular_cash_flows.py'] else not(p.stdout or p.stderr)
            commands.append(dict(label=label,args=args,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,methods=methods,passed=p.returncode==0 and expected))
    m=types.ModuleType('exact_irregular_cash_flows');exec(compile(code,str(source),'exec'),m.__dict__)
    from datetime import date,datetime
    from decimal import Decimal as D,localcontext
    a=date(2026,1,1);b=date(2027,1,1)
    data=[(a,-1000),(date(2026,4,15),250),(date(2026,11,30),500),(date(2027,3,1),400)]
    def decimal_value(amounts,days,rate):
        with localcontext() as ctx:
            ctx.prec=100
            base=(D(1)+D(rate)).ln()
            return sum((D(amount)*(-D(day)*base/365).exp() for amount,day in zip(amounts,days,strict=True)),D(0))
    def probe(label,fn,expected):
        try:actual=fn()
        except Exception as e:ck(label,False,exception=repr(e),reference=str(expected))
        else:close(label,actual,expected)
    # Nonleap Jan–Mar totals 90 days; Jan–Oct totals 304;
    # following-year Mar 1 is 365+31+28 days after Jan 1.
    offsets=[0,31+28+31+14,304+29,365+31+28]
    ck('worked date offsets',[(day-a).days for day,_ in data]==offsets,expected=offsets)
    expected=decimal_value([-1000,250,500,400],offsets,'.1')
    close('worked PV explicit anchor',m.xnpv(.1,data,a),expected)
    close('P9 reversed default-anchor stream',m.xnpv(.1,reversed(data)),expected)
    close('P9 unsorted generator',m.xnpv(.1,(data[i] for i in [2,0,3,1])),expected)
    close('explicit later anchor',m.xnpv(.1,data,b),decimal_value([-1000,250,500,400],[k-365 for k in offsets],'.1'))
    close('explicit earlier anchor',m.xnpv(.1,data,date(2025,1,1)),decimal_value([-1000,250,500,400],[k+365 for k in offsets],'.1'))
    ck('P3 to P5 actual day-count fractions',[(b-a).days, (date(2025,1,1)-date(2024,1,1)).days]==[365,366],fractions=['1','366/365'])
    close('P5 leap-year PV',m.xnpv(.1,[(date(2025,1,1),100)],date(2024,1,1)),decimal_value([100],[366],'.1'))
    close('P6 one-year 110',m.xnpv(.1,[(b,110)],a),F(100))
    close('P7 time-zero receipt',m.xnpv(.1,[(a,100)],a),F(100))
    close('P8 time-zero outflow',m.xnpv(.1,[(a,-100)],a),F(-100))
    close('P10 repeated date',m.xnpv(.1,[(b,10),(b,20)],a),F(300,11))
    close('P10 consolidated payment',m.xnpv(.1,[(b,30)],a),F(300,11))
    close('P11 zero-rate signed sum',m.xnpv(0,data,a),F(150))
    close('negative discount',m.xnpv(-.1,[(b,90)],a),F(100))
    close('empty default anchor',m.xnpv(.1,[]),F(0))
    close('empty valid explicit anchor',m.xnpv(.1,[],a),F(0))
    close('fsum cancellation',m.xnpv(.1,[(a,1e16),(a,1),(a,-1e16)],a),F(1))
    probe('F56 exact zero payment with distant anchor',lambda:m.xnpv(.1,[(date.min,0)],date.max),F(0))
    for label,fn in [
        ('F53 empty stream invalid anchor',lambda:m.xnpv(.1,[],'2026-01-01')),
        ('F53 empty stream timestamp anchor',lambda:m.xnpv(.1,[],datetime(2026,1,1))),
        ('F54 discount factor underflow',lambda:m.xnpv(.1,[(date.max,100)],date.min)),
        ('F54 nonzero payment underflow',lambda:m.xnpv(1,[(b,5e-324)],a)),
        ('timestamp cash-flow date',lambda:m.xnpv(.1,[(datetime(2026,1,1),100)])),
        ('invalid amount',lambda:m.xnpv(.1,[(a,float('nan'))])),
        ('invalid rate',lambda:m.xnpv(-1,[])),
        ('invalid nonempty anchor',lambda:m.xnpv(.1,[(a,100)],'2026-01-01'))]:reject(label,fn)
    out=dict(python=platform.python_version(),platform=platform.platform(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),listing_sha256=hashlib.sha256(code).hexdigest(),commands=commands,checks=checks,workflow_records=1,local_prompt_records=12,conceptual_prompts=[1,2,3,12],historical_unique_methods_added=0)
    (HERE/'results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(len(commands),len(checks),sum(not x['passed'] for x in commands+checks))
    return not all(x['passed'] for x in commands+checks)
if __name__=='__main__':raise SystemExit(main())
