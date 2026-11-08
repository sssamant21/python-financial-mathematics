"""Fixed-length circular moving-block VaR bootstrap and breach diagnostics."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2

def block_indices(n, block, samples, rng):
    if not all(isinstance(v,(int,np.integer)) for v in (n,block,samples)) or not (n>=20 and 1<=block<=n and samples>=1):
        raise ValueError("Require n>=20, 1<=block<=n, samples>=1")
    count=(n+block-1)//block
    starts=rng.integers(0,n,size=(samples,count))
    return ((starts[:,:,None]+np.arange(block))%n).reshape(samples,-1)[:,:n]

def block_var_interval(train, alpha=.05, block=4, samples=500, seed=42):
    x=np.asarray(train,dtype=float)
    if x.ndim!=1 or len(x)<20 or not np.isfinite(x).all() or np.any(x<=-1) or not 0<alpha<.5:
        raise ValueError("Invalid return series or alpha")
    ix=block_indices(len(x),block,samples,np.random.default_rng(seed))
    estimates=np.maximum(0.,-np.quantile(x[ix],alpha,axis=1))
    return tuple(float(v) for v in np.quantile(estimates,[.025,.975]))

def conditional_coverage(breaches, alpha=.05):
    """LR unconditional coverage and Markov independence; asymptotic only."""
    b=np.asarray(breaches)
    if b.ndim!=1 or len(b)<3 or not np.isin(b,[0,1]).all() or not 0<alpha<1:
        raise ValueError("Require >=3 binary flags and alpha in (0,1)")
    b=b.astype(int); n=len(b); k=int(b.sum())
    n00=int(np.sum((b[:-1]==0)&(b[1:]==0)))
    n01=int(np.sum((b[:-1]==0)&(b[1:]==1)))
    n10=int(np.sum((b[:-1]==1)&(b[1:]==0)))
    n11=int(np.sum((b[:-1]==1)&(b[1:]==1)))
    def ll(k,n,p):
        if not n:return 0.
        if p==0:return 0. if k==0 else -np.inf
        if p==1:return 0. if k==n else -np.inf
        return float(k*np.log(p)+(n-k)*np.log1p(-p))
    uc=max(0.,2*(ll(k,n,k/n)-ll(k,n,alpha)))
    identifiable=(n00+n01)>0 and (n10+n11)>0
    out=dict(observations=n,breaches=k,n00=n00,n01=n01,n10=n10,n11=n11,
             lr_uc=uc,p_uc=float(chi2.sf(uc,1)),independence_identifiable=bool(identifiable),
             lr_ind=None,p_ind=None,lr_cc=None,p_cc=None)
    if identifiable:
        p01=n01/(n00+n01);p11=n11/(n10+n11);pooled=(n01+n11)/(n-1)
        alt=ll(n01,n00+n01,p01)+ll(n11,n10+n11,p11)
        null=ll(n01+n11,n-1,pooled)
        ind=max(0.,2*(alt-null))
        out.update(lr_ind=ind,p_ind=float(chi2.sf(ind,1)),lr_cc=uc+ind,
                   p_cc=float(chi2.sf(uc+ind,2)))
    return out

def evaluate(frame,lookback=52,block=4,samples=500,seed=42,alpha=.05):
    """Week t forecast is trained strictly on [t-lookback,t)."""
    if not isinstance(lookback,int) or lookback<20 or not {'Date','Return'}.issubset(frame.columns):
        raise ValueError("Require lookback>=20 and Date,Return")
    df=frame[['Date','Return']].copy()
    df['Date']=pd.to_datetime(df.Date,errors='raise')
    df['Return']=pd.to_numeric(df.Return,errors='raise')
    x=df.Return.to_numpy(dtype=float)
    if df.Date.isna().any() or df.Date.duplicated().any() or not df.Date.is_monotonic_increasing or not np.isfinite(x).all() or np.any(x<=-1) or len(x)<=lookback:
        raise ValueError("Invalid dates, returns or history")
    rows=[]
    for t in range(lookback,len(x)):
        train=x[t-lookback:t]
        point=max(0.,-float(np.quantile(train,alpha)))
        low,high=block_var_interval(train,alpha,block,samples,seed+t)
        rows.append(dict(Date=df.Date.iloc[t].date().isoformat(),
                         TrainingEndDate=df.Date.iloc[t-1].date().isoformat(),
                         Return=float(x[t]),VaR=point,BlockBootstrapLower=low,
                         BlockBootstrapUpper=high,Breach=int(-x[t]>point)))
    scored=pd.DataFrame(rows)
    report=conditional_coverage(scored.Breach.to_numpy(),alpha)
    report.update(lookback=lookback,block_length=block,bootstrap_samples=samples,seed=seed,
                  alpha=alpha,data_points=len(df),
                  note="Asymptotic chi-square diagnostics; not regulatory certification.")
    return scored,report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--returns',type=Path,required=True,help="Licensed weekly Date,Return CSV")
    p.add_argument('--output',type=Path,default=Path(__file__).parent/'reports')
    p.add_argument('--lookback',type=int,default=52)
    p.add_argument('--block',type=int,default=4)
    p.add_argument('--bootstrap',type=int,default=500)
    p.add_argument('--seed',type=int,default=42)
    a=p.parse_args()
    scored,report=evaluate(pd.read_csv(a.returns),a.lookback,a.block,a.bootstrap,a.seed)
    a.output.mkdir(parents=True,exist_ok=True)
    scored.to_csv(a.output/'block_bootstrap_weekly.csv',index=False)
    (a.output/'conditional_coverage.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
