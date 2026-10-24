"""Section 3.7: exact convexity and concavity calculations."""
from fractions import Fraction

def q(x):
    if type(x) not in (int,str,Fraction): raise TypeError("use int, str, or Fraction")
    return Fraction(x)

def quadratic(x,a,b,c):
    x,a,b,c=map(q,(x,a,b,c))
    return a*x*x+b*x+c

def chord_gap(x,y,weight,a,b,c):
    x,y,t=map(q,(x,y,weight))
    if not 0<=t<=1: raise ValueError("weight must be in [0,1]")
    return t*quadratic(x,a,b,c)+(1-t)*quadratic(y,a,b,c)-quadratic(t*x+(1-t)*y,a,b,c)

def second_differences(values):
    v=tuple(q(x) for x in values)
    if len(v)<3: raise ValueError("at least three equally spaced values required")
    return tuple(v[i+2]-2*v[i+1]+v[i] for i in range(len(v)-2))

def discrete_shape(values):
    d=second_differences(values)
    return {"convex_on_grid":all(x>=0 for x in d),
            "concave_on_grid":all(x<=0 for x in d),
            "strictly_convex_on_grid":all(x>0 for x in d),
            "strictly_concave_on_grid":all(x<0 for x in d),
            "second_differences":d}

def total_cost(units):
    n=q(units)
    if n<0 or n.denominator!=1: raise ValueError("nonnegative whole units required")
    return quadratic(n,2,5,40)

def profit(units):
    n=q(units)
    if n<0 or n.denominator!=1: raise ValueError("nonnegative whole units required")
    return 25*n-total_cost(n)

def best_integer_profit(capacity):
    n=q(capacity)
    if n<0 or n.denominator!=1: raise ValueError("capacity must be nonnegative integer")
    pairs=tuple((i,profit(i)) for i in range(int(n)+1))
    m=max(v for _,v in pairs)
    return {"maximum":m,"quantities":tuple(i for i,v in pairs if v==m)}

if __name__=="__main__":
    print("Cost:",discrete_shape(total_cost(i) for i in range(9)))
    print("Profit:",discrete_shape(profit(i) for i in range(9)))
    print("Optimum:",best_integer_profit(12))
