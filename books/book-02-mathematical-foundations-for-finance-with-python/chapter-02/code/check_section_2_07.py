"""Independent exact row reduction, original residuals, domains, and invariance."""
from fractions import Fraction as Q
from itertools import product
import json
from section_2_07 import rational, row, solve_system, residuals, allocation
assert __debug__, 'run without -O: assertions required'
counts={}
def count(name):counts[name]=counts.get(name,0)+1

def reduce_reference(first,second):
    # Normalize pivots and clear their columns; no determinant formulas.
    rows=[list(map(Q,first)),list(map(Q,second))]
    pivot_row=0
    pivots=[]
    for column in range(2):
        candidate=next((i for i in range(pivot_row,2) if rows[i][column]),None)
        if candidate is None:continue
        rows[pivot_row],rows[candidate]=rows[candidate],rows[pivot_row]
        factor=rows[pivot_row][column]
        rows[pivot_row]=[v/factor for v in rows[pivot_row]]
        for i in range(2):
            if i!=pivot_row:
                factor=rows[i][column]
                rows[i]=[v-factor*w for v,w in zip(rows[i],rows[pivot_row])]
        pivots.append(column)
        pivot_row+=1
        if pivot_row==2:break
    if any(a==b==0 and c!=0 for a,b,c in rows):return 'none',None
    if len(pivots)==2:return 'unique',(rows[0][2],rows[1][2])
    return ('line' if pivots else 'all_pairs'),None

for six in product([-1,0,1],repeat=6):
    first,second=six[:3],six[3:]
    got=solve_system(first,second)
    kind,point=reduce_reference(first,second)
    assert got['kind']==kind,(six,got,kind)
    if kind=='unique':
        assert got['point']==point
        assert residuals(first,second,point)==(0,0)
    elif kind=='line':
        base,direction=got['base'],got['direction']
        assert direction!=(0,0)
        for t in [Q(-3),Q(-1,2),Q(0),Q(2,3),Q(5)]:
            point=tuple(v+t*w for v,w in zip(base,direction))
            assert residuals(first,second,point)==(0,0)
            count('line_membership_cases')
    elif kind=='all_pairs':
        assert residuals(first,second,(Q(7,3),-11))==(0,0)
    # Equation order and nonzero scaling preserve classification.
    swapped=solve_system(second,first)
    scaled=solve_system(tuple(-3*v for v in first),tuple(2*v for v in second))
    assert swapped['kind']==scaled['kind']==kind
    if kind=='unique':assert swapped['point']==scaled['point']==got['point']
    count('grid_systems')
    count('swap_and_scale_cases')

for a,b,d,e in product(range(-2,3),repeat=4):
    if a*e==d*b:continue
    for x,y in [(Q(-3,2),Q(7,3)),(Q(0),Q(0)),(Q(12),Q(-9))]:
        first=(a,b,a*x+b*y);second=(d,e,d*x+e*y)
        assert solve_system(first,second)['point']==(x,y)
        count('planted_unique_pairs')

for r1,r2 in product([Q(-1,10),Q(0),Q(1,25),Q(3,50)],repeat=2):
    for budget in [0,10,1000]:
        low=min(r1,r2)*budget;high=max(r1,r2)*budget
        for target in [low-1,low,(low+high)/2,high,high+1]:
            got=allocation(budget=budget,rate_one=r1,rate_two=r2,interest=target)
            assert (got['feasible']!='empty')==(low<=target<=high)
            if got['algebraic']['kind']=='unique':
                assert got['residuals']==(0,0)
                x,y=got['algebraic']['point']
                assert x+y==budget and r1*x+r2*y==target
                assert (got['feasible']=='unique')==(x>=0 and y>=0)
            elif got['feasible']=='segment':
                assert got['x_interval']==(0,budget)
                for x in [Q(0),Q(budget,2),Q(budget)]:
                    assert r1*x+r2*(budget-x)==target
            elif got['feasible']=='unique':assert got['point']==(0,0)
            count('allocation_boundary_cases')

assert solve_system((1,1,18),(3,-1,10))['point']==(7,11)
assert solve_system((20,50,700),(2,1,34))['point']==(Q(25,2),9)
assert solve_system((3,-6,9),(1,-2,3))['kind']=='line'
assert solve_system((3,-6,9),(1,-2,4))['kind']=='none'
assert solve_system((0,0,0),(0,0,0))['kind']=='all_pairs'
assert solve_system((0,0,2),(1,1,1))['kind']=='none'
assert allocation(budget=2000,rate_one='.03',rate_two='.07',interest=100)['algebraic']['point']==(1000,1000)
assert allocation(budget=2000,rate_one='.03',rate_two='.07',interest=150)['algebraic']['point']==(-250,2250)
assert allocation(budget=500,rate_one='.04',rate_two='.04',interest=21)['feasible']=='empty'
for t in [Q(-3),Q(0),Q(1,2),Q(4)]:assert residuals((3,-6,9),(1,-2,3),(3+2*t,t))==(0,0)
assert residuals((0,2,8),(0,0,0),(3,5))==(2,0)
assert solve_system((0,2,8),(3,0,9))['point']==(3,4)
assert rational('.04')==Q(1,25)
invalid=[(lambda:rational(True),TypeError),(lambda:rational(.04),TypeError),
(lambda:rational(None),TypeError),(lambda:rational('NaN'),ValueError),
(lambda:rational('1/0'),ZeroDivisionError),(lambda:row([1,2]),ValueError),
(lambda:row([1,2,3,4]),ValueError),(lambda:row([1,False,3]),TypeError),
(lambda:residuals((1,1,2),(1,-1,0),(1,)),ValueError),
(lambda:allocation(budget=-1,rate_one=0,rate_two=1,interest=0),ValueError),
(lambda:allocation(budget=1,rate_one=.04,rate_two='.06',interest=0),TypeError)]
for operation,error in invalid:
    try:operation()
    except error:pass
    else:raise AssertionError('expected '+error.__name__)
    count('rejected_calls')
print('PASS: '+json.dumps(counts,sort_keys=True))
