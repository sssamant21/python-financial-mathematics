"""Section 11.9: labeled portfolio exposure calculator capstone."""
from dataclasses import dataclass
import json
import math

def finite(x,name):
    if type(x) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        y=float(x)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(y):
        raise ValueError(f"{name} must be finite")
    return y

@dataclass(frozen=True)
class Vector:
    labels: tuple
    values: tuple
    unit: str
    def __post_init__(self):
        labels=tuple(self.labels)
        values=tuple(self.values)
        if not labels or len(labels)!=len(values):
            raise ValueError("nonempty matching labels and values required")
        if any(type(k) is not str or not k.strip() for k in labels):
            raise ValueError("labels must be nonempty strings")
        if len(set(labels))!=len(labels):
            raise ValueError("duplicate labels")
        if type(self.unit) is not str or not self.unit.strip():
            raise ValueError("unit required")
        object.__setattr__(self,"labels",labels)
        object.__setattr__(self,"values",tuple(finite(v,"component") for v in values))
    def align(self,labels):
        target=tuple(labels)
        if len(target)!=len(self.labels) or len(set(target))!=len(target) or set(target)!=set(self.labels):
            raise ValueError("asset labels must match exactly")
        lookup=dict(zip(self.labels,self.values))
        return Vector(target,tuple(lookup[k] for k in target),self.unit)

@dataclass(frozen=True)
class Policy:
    gross_cap: float=1.0
    absolute_name_cap: float=0.6
    max_unexplained_nav_gap_usd: float=40000.0
    def __post_init__(self):
        for key in ("gross_cap","absolute_name_cap","max_unexplained_nav_gap_usd"):
            value=finite(getattr(self,key),key)
            if value<0:
                raise ValueError(f"{key} must be nonnegative")
            object.__setattr__(self,key,value)

def calculate(prices,holdings,nav,scenarios,policy=Policy()):
    if not isinstance(prices,Vector) or not isinstance(holdings,Vector):
        raise TypeError("prices and holdings must be vectors")
    if prices.unit!="USD/share" or holdings.unit!="shares":
        raise ValueError("expected USD/share prices and shares holdings")
    if not isinstance(policy,Policy):
        raise TypeError("expected Policy")
    nav=finite(nav,"NAV")
    if nav<=0:
        raise ValueError("NAV must be positive")
    holdings=holdings.align(prices.labels)
    values=tuple(finite(p*q,"position value") for p,q in zip(prices.values,holdings.values))
    weights=tuple(finite(v/nav,"weight") for v in values)
    signed=finite(math.fsum(values),"signed position value")
    long=finite(math.fsum(max(w,0) for w in weights),"long exposure")
    short=finite(math.fsum(max(-w,0) for w in weights),"short exposure")
    gross=finite(long+short,"gross exposure")
    net=finite(math.fsum(weights),"net exposure")
    gap=finite(nav-signed,"NAV reconciliation difference")
    breaches=[]
    tolerance=1e-10
    gap_tolerance=1e-8
    if gross>policy.gross_cap+tolerance:
        breaches.append("gross_cap")
    for label,w in zip(prices.labels,weights):
        if abs(w)>policy.absolute_name_cap+tolerance:
            breaches.append("absolute_name_cap:"+label)
    if abs(gap)>policy.max_unexplained_nav_gap_usd+gap_tolerance:
        breaches.append("unexplained_nav_gap")
    if type(scenarios) is not dict or not scenarios:
        raise ValueError("nonempty scenario mapping required")
    scenario_results={}
    for name,returns in scenarios.items():
        if type(name) is not str or not name.strip() or not isinstance(returns,Vector):
            raise ValueError("scenario name and vector required")
        if returns.unit!="simple_return":
            raise ValueError("scenario unit must be simple_return")
        aligned=returns.align(prices.labels)
        pnl=finite(math.fsum(finite(v*r,"scenario PnL component") for v,r in zip(values,aligned.values)),"scenario PnL")
        scenario_results[name]={"pnl_USD":pnl,"nav_return_contribution":finite(pnl/nav,"NAV return contribution")}
    return {"assets":list(prices.labels),
            "position_values_USD":dict(zip(prices.labels,values)),
            "weights":dict(zip(prices.labels,weights)),
            "signed_risky_position_value_USD":signed,
            "unexplained_nav_difference_USD":gap,
            "exposures":{"net":net,"gross":gross,"long":long,"short":short},
            "scenarios":scenario_results,
            "policy":{"feasible":not breaches,"breaches":breaches,
                      "limits":{"gross_cap":policy.gross_cap,
                                "absolute_name_cap":policy.absolute_name_cap,
                                "max_unexplained_nav_gap_usd":policy.max_unexplained_nav_gap_usd},
                      "comparison_tolerances":{"exposure":tolerance,"nav_gap_USD":gap_tolerance}},
            "assumptions":"USD; static holdings; simple returns; independently supplied NAV; unexplained NAV gap is not assumed to be cash",
            "runtime_certified":False,"independent_review_completed":False}

def assessment():
    prices=Vector(("ALPHA","BETA","GAMMA"),(100,50,25),"USD/share")
    holdings=Vector(("GAMMA","ALPHA","BETA"),(800,500,-200),"shares")
    scenarios={
        "A":Vector(("GAMMA","ALPHA","BETA"),(0.04,0.02,-0.01),"simple_return"),
        "B":Vector(("BETA","GAMMA","ALPHA"),(0.02,-0.01,-0.03),"simple_return")}
    return calculate(prices,holdings,100000,scenarios)

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
