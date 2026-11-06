"""Section 19.9 terminal event decisions from independent signed-flow references."""
from decimal import Decimal as D, localcontext
import json
import math
import sys
import section_19_09 as lab


def check():
    upper=math.nextafter(1.,2.)
    lower=math.nextafter(math.nextafter(1.,0.),0.)
    big=sys.float_info.max
    tiny=math.ulp(0.)
    scenarios=[(upper,lower,-1.,80.,()),
               (upper,lower,-1.,80.,((75.,10.),)),
               (1.,-big,-tiny,1e-304,()),
               (big,-big,-tiny,1e-304,((1e-304,10.),))]
    rows=[]
    with localcontext() as ctx:
        ctx.prec=1600
        for a,r,u,T,jumps in scenarios:
            w=-D(u)
            crossing=float((w/(w-D(r)*D(a))).ln()/D(r))
            try:
                result=lab.simulate(a,r,u,T,jumps)
            except (ValueError,OverflowError) as exc:
                result=type(exc).__name__
            ok=(isinstance(result,dict) and result['status']=='depleted'
                and abs(result['final_time']-crossing)<=3*math.ulp(crossing)
                and result['depletion_time']==result['final_time']
                and result['final_balance']==0.
                and result['applied_jumps']==0 and result['scheduled_jumps']==len(jumps)
                and result['events']==[dict(type='depletion',time=result['final_time'])]
                and result['event_policy']['coincident_future_jump']=='depletion_first')
            rows.append(dict(inputs=repr((a,r,u,T,jumps)),expected_time=crossing,
                             result=result,passed=ok))
    original=lab._depletion_elapsed
    calls=[]
    def observed(a,r,w,*,for_order):
        calls.append((a,r,w,for_order))
        return .125
    lab._depletion_elapsed=observed
    try:
        result=lab.simulate(1,0,-1,1)
        assert result['depletion_time']==.125
    finally:
        lab._depletion_elapsed=original
    assert calls==[(1.,0.,1.,True)]
    print(json.dumps(rows,indent=2))
    assert all(row['passed'] for row in rows)


if __name__=='__main__':
    check()
