"""Selected zero-rate jump paths with exact conservation references."""
import json
import section_19_07 as lab


def check():
    rows=[]
    cases=[
        (10,2,10,[],False,'completed',10,-10),
        (10,2,10,[(6,20)],False,'completed',10,10),
        (10,2,10,[(6,20)],True,'depleted',5,0),
        (10,1,4,[(2,-10)],False,'completed',4,-4),
        (10,1,4,[(2,-10)],True,'depleted',2,0),
        (0,1,1,[],False,'completed',1,-1),
        (10,0,3,[(1,-20),(2,15)],False,'completed',3,5),
        (10,0,3,[(1,-20),(2,15)],True,'depleted',1,0),
    ]
    for initial,w,T,jumps,stop,status,end,balance in cases:
        try:
            actual=lab.simulate_jumps(initial,0,w,T,jumps,stop)
        except ValueError as exc:
            actual=type(exc).__name__
        expected=dict(status=status,event_time=None if status=='completed' else end,
                      final_time=end,final_balance=float(balance))
        rows.append(dict(initial=initial,withdrawal=w,horizon=T,jumps=jumps,
                         terminal=stop,actual=actual,expected=expected,passed=actual==expected))
    # Public account's initial-balance domain is unchanged.
    try:
        lab.account(-1,0,0,1)
    except ValueError:
        rejected=True
    else:
        rejected=False
    assert rejected
    print(json.dumps(rows,indent=2))
    assert all(r['passed'] for r in rows)


if __name__=='__main__':
    check()
