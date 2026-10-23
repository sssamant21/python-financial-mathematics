"""Independent hand values, invariants, failure cases, and exercise answers."""
from math import isclose
from section_1_01 import compound_value

def close(actual,expected):
    assert isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-10),(actual,expected)

cases=[(1000,.05,1,1050),(1000,.05,2,1102.5),
       (1000,0,10,1000),(1000,.05,0,1000),(1000,-.02,1,980),
       (2000,.03,2,2121.8),(1000,5,1,6000)]
for principal,rate,periods,expected in cases:
    close(compound_value(principal,rate,periods),expected)
close(compound_value(500,.04,1)-5,515)
close(compound_value(495,.04,1),514.8)
close((compound_value(500,.04,1)-5)-compound_value(495,.04,1),.2)
close(121/1.1**2,100)
close(121*1.1**2,146.41)
close(100*1.1*.9,99)
# Recover principal and independently compare with an iterative recurrence.
scenarios=0
for principal in [0.,1.,1000.]:
    for rate in [-.02,0.,.05]:
        for periods in [0,1,2,5]:
            result=compound_value(principal,rate,periods)
            close(result/(1+rate)**periods,principal)
            iterative=principal
            for _ in range(periods):
                iterative*=1+rate
            close(result,iterative)
            scenarios+=1
invalid=[((-1,.05,1),ValueError),((100,-1,1),ValueError),
         ((100,.05,-1),ValueError),((100,.05,1.5),TypeError),
         ((True,.05,1),TypeError),((100,True,1),TypeError),
         ((100,.05,True),TypeError),((100,'0.05',1),TypeError),
         ((100,float('nan'),1),ValueError),((float('inf'),.05,1),ValueError),
         ((10**1000,.05,1),ValueError),((1,1.,2000),ArithmeticError),
         ((1,-.5,2000),ArithmeticError)]
for args,expected in invalid:
    try:
        compound_value(*args)
    except expected:
        pass
    else:
        raise AssertionError(f"expected {expected.__name__}: {args}")
print(f"PASS: {len(cases)} known growth cases; {scenarios} inverse/recurrence scenarios; "
      f"{len(invalid)} rejection/range cases; fee, discount, and exercise checks")
