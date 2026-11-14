"""Bounded preset step sweeps with analytic error curves, not a production selector."""
import json,math
from fractions import Fraction
import section_8_08 as source

def observations():
    predicates=[];sweeps={};calls=0
    def add(name,actual,expected):predicates.append(dict(name=name,actual=actual,expected=expected,passed=actual==expected))
    for name,ks,eta in [('first',range(1,17),2.**-30),('second',range(1,19),2.**-40)]:
        records=[]
        for k in ks:
            h=2.**-k;trace=[]
            def callback(x):
                trace.append(x)
                if name=='first':return x**3+(eta if x>0 else -eta if x<0 else 0.)
                return x**4+(eta if x!=0 else -eta)
            value=(source.centered_difference if name=='first' else source.second_difference)(callback,0.,h)
            # Independently substitute exact polynomial/noise samples at ±h and zero.
            H,E=Fraction(h),Fraction(eta)
            truncation=H**2 if name=='first' else 2*H**2
            noise=E/H if name=='first' else 4*E/H**2
            expected=float(truncation+noise)
            add(f'{name} exact error curve k{k}',value,expected)
            expected_trace=[h,-h] if name=='first' else [h,0.,-h]
            add(f'{name} callback budget/order k{k}',[x.hex() for x in trace],[float(x).hex() for x in expected_trace])
            calls+=len(trace)
            records.append(dict(k=k,h=h,estimate=value,noiseless_derivative=0.,absolute_error=abs(value),expected_error=expected,truncation_component=float(truncation),noise_component=float(noise),callback_calls=len(trace),callback_inputs=[x.hex() for x in trace]))
        minimum=min(records,key=lambda x:x['absolute_error']);add(name+' finite-grid minimum k',minimum['k'],10)
        add(name+' improving coarse to minimum',records[0]['absolute_error']>minimum['absolute_error'],True)
        add(name+' worsening after minimum',records[-1]['absolute_error']>minimum['absolute_error'],True)
        sweeps[name]=dict(records=records,minimum=minimum,eta=eta,step_count=len(records),callback_budget=sum(x['callback_calls'] for x in records),meaning='Minimum of this preset finite grid under a known synthetic model;not an estimated provider noise budget or global optimum')
    add('total measured callback budget',calls,86)
    return predicates,dict(sweeps=sweeps,steps=34,callback_calls=calls,limits='Finite preset binary steps and known synthetic polynomial/noise models;no adaptive selection or real-data accuracy guarantee')
if __name__=='__main__':
    rows,report=observations();print(json.dumps(dict(predicates=rows,sweep_report=report),indent=2));assert all(x['passed'] for x in rows);print(len(rows),'sweep predicates passed;34 steps/86 callback calls')
