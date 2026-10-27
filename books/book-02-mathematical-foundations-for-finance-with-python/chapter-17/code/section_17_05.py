"""Book 02 Section 17.5: deterministic two-variable LP teaching lab."""
import itertools
import json
import math

# x,y are thousands of dollars; benefit is in synthetic benefit units.
A=((1.0,1.0),(2.0,1.0),(-1.0,0.0),(0.0,-1.0))
B=(8.0,10.0,0.0,0.0)
C=(5.0,4.0)

def finite(value,name):
    if type(value) not in (int,float):
        raise TypeError(f"{name} must be numeric, excluding bool")
    try:
        v=float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} outside float range") from exc
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v

def benefit(x,y):
    return finite(5*finite(x,"x")+4*finite(y,"y"),"benefit")

def primal_report(x,y,budget=8.0,resource=10.0,tol=1e-9):
    x,y=finite(x,"x"),finite(y,"y")
    b1,b2=finite(budget,"budget"),finite(resource,"resource")
    tol=finite(tol,"tolerance")
    if tol<0:
        raise ValueError("tolerance must be nonnegative")
    slacks=(b1-x-y,b2-2*x-y,x,y)
    return {"allocation":(x,y),"slacks":slacks,
            "feasible":all(s>=-tol for s in slacks),
            "benefit":benefit(x,y)}

def intersections(budget=8.0,resource=10.0):
    b1,b2=finite(budget,"budget"),finite(resource,"resource")
    rows=((1.0,1.0,b1),(2.0,1.0,b2),(-1.0,0.0,0.0),(0.0,-1.0,0.0))
    points=[]
    for (a,b,c),(d,e,f) in itertools.combinations(rows,2):
        determinant=a*e-b*d
        if abs(determinant)<1e-12:
            continue
        x=(c*e-b*f)/determinant
        y=(a*f-c*d)/determinant
        if primal_report(x,y,b1,b2)["feasible"]:
            point=(round(x,12),round(y,12))
            if point not in points:
                points.append(point)
    return tuple(sorted(points))

def solve_vertices(budget=8.0,resource=10.0):
    points=intersections(budget,resource)
    if not points:
        raise ValueError("no feasible vertex found; not a general LP diagnosis")
    best=max(points,key=lambda p:(benefit(*p),-p[0],-p[1]))
    return {"vertices":points,"allocation":best,
            "benefit":benefit(*best),
            "primal":primal_report(*best,budget,resource)}

def dual_report(u1,u2,budget=8.0,resource=10.0,tol=1e-9):
    a,b=finite(u1,"u1"),finite(u2,"u2")
    b1,b2=finite(budget,"budget"),finite(resource,"resource")
    tol=finite(tol,"tolerance")
    if tol<0:
        raise ValueError("tolerance must be nonnegative")
    slacks=(a+2*b-5,a+b-4,a,b)
    return {"multipliers":(a,b),"slacks":slacks,
            "feasible":all(v>=-tol for v in slacks),
            "dual_objective":b1*a+b2*b}

def certificate(x=2.0,y=6.0,u1=3.0,u2=1.0,budget=8.0,resource=10.0,tol=1e-9):
    p=primal_report(x,y,budget,resource,tol)
    d=dual_report(u1,u2,budget,resource,tol)
    gap=d["dual_objective"]-p["benefit"]
    complementary=(u1*p["slacks"][0],u2*p["slacks"][1],
                   x*d["slacks"][0],y*d["slacks"][1])
    return {"primal":p,"dual":d,"duality_gap":gap,
            "complementarity":complementary,
            "certified_by_residuals":p["feasible"] and d["feasible"]
            and abs(gap)<=tol and all(abs(v)<=tol for v in complementary)}

def assessment():
    solution=solve_vertices()
    return {"solution":solution,"certificate":certificate(),
            "runtime_certified":False,"independent_review_completed":False}

if __name__=="__main__":
    print(json.dumps(assessment(),indent=2,allow_nan=False))
