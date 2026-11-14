"""Independent complete model references;factory domain and JSON report controls."""
import math,json,sys
from decimal import Decimal,localcontext
import section_8_09 as source

def observations():
    rows=[]
    def check(name,call,expected):
        try:
            value=call();actual=repr(value)
            ok=not isinstance(expected,str) and math.isfinite(value) and (value==expected if expected==0 else math.isclose(value,expected,rel_tol=4e-15,abs_tol=0))
            if ok and expected==0:ok=math.copysign(1,value)==math.copysign(1,expected)
        except Exception as exc:actual=type(exc).__name__;ok=actual==expected
        rows.append(dict(name=name,actual=actual,expected=expected if isinstance(expected,str) else repr(expected),passed=ok))
    models={'accumulation':source.accumulation_model(),'dcf':source.discounted_cash_flow_model(),'ratio':source.ratio_model(),'profit':source.profit_model()}
    vectors={'accumulation':[0.,5.,-18750.,17650.,17675.,1e308,-1e308],'dcf':[.03,187.5,-176.5,0.,1e308,-1e308],'ratio':[5e-324,2.,1e100,1e308,sys.float_info.max],'profit':[0.,160.,500.]}
    def reference(model,j,x,precision):
        with localcontext() as ctx:
            ctx.prec=precision;X=Decimal.from_float(x)
            if model in ('accumulation','dcf'):
                R=Decimal.from_float(.04) if model=='accumulation' else Decimal(-4)
                C=Decimal(1000) if model=='accumulation' else Decimal(5000)
                coefficient=C*(R**j);exponent=R*X
                if exponent>10000:return 'ValueError'
                if exponent< -10000:return -0. if coefficient<0 else 0.
                value=coefficient*exponent.exp()
            elif model=='ratio':
                denominator=50+3*X
                value=(100+8*X)/denominator if j==0 else Decimal(100)/(denominator**2) if j==1 else Decimal(-600)/(denominator**3)
            else:value=-1000+80*X-X*X/4 if j==0 else 80-X/2 if j==1 else Decimal('-.5')
            result=float(value)
            return result if math.isfinite(result) else 'ValueError'
    for model,xs in vectors.items():
        for x in xs:
            for j in range(3):
                a,c=reference(model,j,x,2000),reference(model,j,x,2600);assert a==c
                check(f'{model} field{j} x={x!r}',lambda m=model,j=j,x=x:models[m][j](x),a)
    for model,items in models.items():
        for j in range(3):
            for label,x,error in [('bool',True,'TypeError'),('NaN',float('nan'),'ValueError'),('oversized integer',10**1000,'ValueError'),('text','bad','TypeError')]:check(f'{model} field{j} {label}',lambda m=model,j=j,x=x:models[m][j](x),error)
    for model,xs in [('profit',[-1.,500.1]),('ratio',[0.,-1.])]:
        for x in xs:
            for j in range(3):check(f'{model} domain field{j} x={x}',lambda m=model,j=j,x=x:models[m][j](x),'ValueError')
    report=source.run_demo();encoded=json.dumps(report,sort_keys=True,allow_nan=False);decoded=json.loads(encoded)
    for name,actual,expected in [('model report keys',sorted(report),['accumulation','discounted_cash_flow','profit','ratio']),('sixteen reports',sum(len(x['comparisons']) for x in report.values()),16),('JSON roundtrip',decoded,report)]:rows.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
    for model,(f,d1,d2,x,unit) in models.items():
        trace=[]
        def wrap(fn,label):
            def observed(z):trace.append(label);return fn(z)
            return observed
        source.compare_derivatives(wrap(f,'f'),wrap(d1,'d1'),x,.001,wrap(d2,'d2'))
        rows.append(dict(name=model+' facade callback budget',actual=trace,expected=['f']*5+['d1','d2'],passed=trace==['f']*5+['d1','d2']))
    return rows
if __name__=='__main__':
    rows=observations();print(json.dumps(rows,indent=2));print(len(rows),'factory predicates;',sum(not x['passed'] for x in rows),'failed');assert all(x['passed'] for x in rows)
