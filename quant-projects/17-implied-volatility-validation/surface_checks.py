"""Necessary European call strike/calendar quote screens; synthetic research only."""
import math

def _finite(x):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x):
        raise ValueError("finite numeric input required")
    return float(x)

def _rows(rows):
    out=[]
    for row in rows:
        if len(row)!=3: raise ValueError("expected (coordinate,bid,ask)")
        x,b,a=map(_finite,row)
        if x<=0 or b<0 or b>a: raise ValueError("invalid or crossed quotes")
        out.append((x,b,a))
    if len(out)<2 or any(out[i][0]>=out[i+1][0] for i in range(len(out)-1)):
        raise ValueError("need increasing coordinates and at least two quotes")
    return out

def check_call_strikes(rows,spot,maturity,rate=0.,dividend=0.,tol=1e-10):
    """Flag unavoidable violations of call bounds, vertical spreads and convexity."""
    s,t,r,q,eps=map(_finite,(spot,maturity,rate,dividend,tol))
    if s<=0 or t<=0 or q<0 or eps<0: raise ValueError("invalid assumptions")
    rows=_rows(rows)
    df=math.exp(-r*t); ds=s*math.exp(-q*t)
    if not math.isfinite(df) or not math.isfinite(ds): raise ValueError("invalid discount")
    failures=[]
    for k,b,a in rows:
        if b>ds+eps or a<max(0.,ds-k*df)-eps: failures.append(("bounds",k))
    for (k0,b0,a0),(k1,b1,a1) in zip(rows,rows[1:]):
        if b1>a0+eps: failures.append(("monotonic",k0,k1))
        if b0-a1>(k1-k0)*df+eps: failures.append(("vertical_spread",k0,k1))
    for (k0,b0,a0),(k1,b1,a1),(k2,b2,a2) in zip(rows,rows[1:],rows[2:]):
        w=(k2-k1)/(k2-k0)
        if b1>w*a0+(1-w)*a2+eps: failures.append(("butterfly",k0,k1,k2))
    return {"passed":not failures,"violations":failures,"tested_strikes":len(rows)}

def check_call_calendar(rows,strike,spot,rate=0.,dividend=0.,tol=1e-10):
    """Call maturity monotonicity only under q=0, r>=0, identical underlying."""
    k,s,r,q,eps=map(_finite,(strike,spot,rate,dividend,tol))
    if k<=0 or s<=0 or r<0 or q!=0 or eps<0:
        raise ValueError("calendar test requires zero dividend and nonnegative rate")
    rows=_rows(rows); failures=[]
    for t,b,a in rows:
        if b>s+eps or a<max(0.,s-k*math.exp(-r*t))-eps: failures.append(("bounds",t))
    for (t0,b0,a0),(t1,b1,a1) in zip(rows,rows[1:]):
        if b0>a1+eps: failures.append(("calendar",t0,t1))
    return {"passed":not failures,"violations":failures,"tested_expiries":len(rows)}

if __name__=="__main__":
    from implied_vol import price
    strikes=[(k,price("call",100.,k,1.,.05,.2)-.01,price("call",100.,k,1.,.05,.2)+.01) for k in (90.,100.,110.)]
    terms=[(t,price("call",100.,100.,t,.05,.2)-.01,price("call",100.,100.,t,.05,.2)+.01) for t in (.5,1.,2.)]
    print(check_call_strikes(strikes,100.,1.,.05))
    print(check_call_calendar(terms,100.,100.,.05))
