"""Chapter 19.10 applied C/D: independent deviation and timed-cash references."""
from decimal import Decimal as D, localcontext
import json
import math
import section_19_10 as lab


def check():
    report=lab.assessment()
    rows=[]
    def record(name,actual,expected):
        ok=(math.isclose(actual,expected,rel_tol=2e-15,abs_tol=2e-12)
            if isinstance(actual,(int,float)) and isinstance(expected,float)
            else actual==expected)
        rows.append(dict(case=name,actual=actual,expected=expected,passed=ok))
    c=report.get("applied_target_adjustment",{})
    d=report.get("applied_jump_timing",{})
    with localcontext() as ctx:
        ctx.prec=80
        k=D(.6)
        half=D(2).ln()/k
        record("equilibrium",c.get("equilibrium"),5000.)
        record("classification",c.get("classification"),"asymptotically_stable")
        record("half life",c.get("half_life"),float(half))
        record("balance at half life",c.get("balance_at_half_life"),4000.)
        record("balance at year 5",c.get("balance_at_year_five"),
               float(5000-2000*(-5*k).exp()))
        r=D(.05)
        base=1000*(5*r).exp()
        early=500*(4*r).exp()
        late=500*(2*r).exp()
        record("deposit amount",d.get("deposit"),500.)
        record("horizon",d.get("horizon"),5.)
        record("year 1 deposit terminal balance",d.get("deposit_year_one"),float(base+early))
        record("year 3 deposit terminal balance",d.get("deposit_year_three"),float(base+late))
        record("timing difference",d.get("earlier_minus_later"),float(early-late))
        record("earlier is larger",d.get("deposit_year_one",0)>d.get("deposit_year_three",0),True)
    print(json.dumps(rows,indent=2,allow_nan=False))
    assert all(row["passed"] for row in rows)


if __name__=="__main__":
    check()
