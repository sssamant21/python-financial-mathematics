"""Independent report/tolerance references and accepted-domain range rescues."""
import math,json
from decimal import Decimal,localcontext
import section_8_09 as source

def observations():
    rows=[]
    def add(name,actual,expected):rows.append(dict(name=name,actual=actual,expected=expected,passed=actual==expected))
    tiny=math.ulp(0.)
    for a in (0.,tiny):
        for r in (0.,.25,.5,.75,1.,1.5,2.):
            report=source.compare_derivatives(lambda x:0.,lambda x:tiny,0.,1.,lambda x:tiny,a,r)
            with localcontext() as ctx:
                ctx.prec=2500
                # Exact Decimal representations of supplied finite binary values.
                gate=Decimal.from_float(tiny)<=Decimal.from_float(a)+Decimal.from_float(r)*Decimal.from_float(tiny)
            for name,row in list(report['first_derivatives'].items())+[('second',report['second_derivative'])]:
                add(f'exact threshold a={a!r} r={r!r} {name}',[row['estimate'],row['signed_error'],row['absolute_error'],row['pass']],[0.,-tiny,tiny,gate])
    for name,function,first,second,h,expected in [('large linear',lambda x:1e308*x,lambda x:1e308,None,1.,1e308),('large constant with second',lambda x:1e308,lambda x:0.,lambda x:0.,1.,0.)]:
        try:
            report=source.compare_derivatives(function,first,0.,h,second,0.,0.)
            actual=[all(row['estimate']==expected and row['signed_error']==0 and row['pass'] for row in report['first_derivatives'].values()),'second_derivative' not in report if second is None else report['second_derivative']['estimate']==0 and report['second_derivative']['pass']]
        except Exception as exc:actual=type(exc).__name__
        add(name,actual,[True,True])
    trace=[]
    def f(x):trace.append(['f',x]);return x*x
    def d1(x):trace.append(['d1',x]);return 2*x
    def d2(x):trace.append(['d2',x]);return 2.
    source.compare_derivatives(f,d1,2.,.5,d2)
    add('callback order and seven-call budget',trace,[['f',2.],['f',2.5],['f',1.5],['f',2.25],['f',1.75],['d1',2.],['d2',2.]])
    trace.clear();report=source.compare_derivatives(f,d1,2.,.5)
    add('first-only six calls and absent field',[len(trace),'second_derivative' in report],[6,False])
    trace.clear()
    try:source.compare_derivatives(f,d1,2.,0.,d2)
    except ValueError:pass
    add('invalid step before callbacks',trace,[])
    trace.clear();sentinel=RuntimeError('sentinel')
    def bad(x):trace.append(x);raise sentinel
    try:source.compare_derivatives(bad,d1,2.,.5);identity=False
    except RuntimeError as exc:identity=exc is sentinel
    add('callback original exception and short circuit',[identity,trace],[True,[2.]])
    trace.clear();ladder=source.step_ladder(f,d1,2.,iter([.5,.25]),d2)
    add('finite ladder order and fourteen calls',[[x['step'] for x in ladder],len(trace)],[[.5,.25],14])
    for label,function,expected in [('constant negative zero',lambda x:-0.,[1,1,1,1,1]),('negative zero on positive x',lambda x:-0. if x>0 else 0.,[-1,1,-1,1,1]),('negative zero on nonnegative x',lambda x:-0. if x>=0 else 0.,[1,-1,-1,1,1])]:
        report=source.compare_derivatives(function,lambda x:0.,0.,1.,lambda x:0.,0.,0.)
        signs=[int(math.copysign(1,row['estimate'])) for row in report['first_derivatives'].values()]+[int(math.copysign(1,report['second_derivative']['estimate']))]
        add(label+' stencil zero signs',signs,expected)
    return rows
if __name__=='__main__':
    rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'report predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
