"""Quadrature range, exact grid geometry and final-helper integration checks."""
from decimal import Decimal as D, localcontext
import json
import math
from unittest.mock import patch
import section_18_07 as lab
import section_18_10 as final


def rejects(error,fn,*args):
    try:fn(*args)
    except error:return
    raise AssertionError('expected '+error.__name__)


def check():
    tiny=math.nextafter(0.0,1.0);records=[]
    methods=(('trapezoid',lab.trapezoid),('simpson',lab.simpson),('final_simpson',final.simpson))
    constants=((1e308,0.0,1e-308,2),(-1e308,0.0,1e-308,4),
               (tiny,0.0,1.0,2),(1.0,0.0,1.0,4),
               (1e-308,-1e308,1e308,2),(1e308,0.0,2*tiny,2),
               (0.0,-1e308,1e308,2))
    def evaluate(name,method,f,a,b,n,reference):
        points=[]
        def callback(x):points.append(x);return f(x)
        actual=method(callback,a,b,n)
        assert actual==float(reference),(name,a,b,n,actual,float(reference))
        with localcontext() as ctx:
            ctx.prec=2500
            lo,hi=D.from_float(a),D.from_float(b)
            grid=[float(lo+(hi-lo)*i/n) for i in range(n+1)]
        assert points==[grid[0],grid[-1],*grid[1:-1]]
        assert all(math.isfinite(x) for x in points)
        assert all(x<y for x,y in zip(grid,grid[1:]))
        records.append({'method':name,'lower':a,'upper':b,'panels':n,
                        'actual':actual,'decimal_reference':str(reference),'observed_points':points})
    with localcontext() as ctx:
        ctx.prec=2500
        for name,method in methods:
            for c,a,b,n in constants:
                exact=D.from_float(c)*(D.from_float(b)-D.from_float(a))
                evaluate(name,method,lambda x:c,a,b,n,exact)
            for a,b in ((0.0,2.0),(-1.0,1.0)):
                # Exact affine integral: x/2+1/4, with dyadic node values.
                da,db=D.from_float(a),D.from_float(b)
                exact=(db*db-da*da)/4+(db-da)/4
                evaluate(name,method,lambda x:x/2+0.25,a,b,4,exact)
            evaluate(name,method,lambda x:1.7e308*x,-1.0,1.0,4,D(0))
        for c,a,b in ((tiny,0.0,1.0),(1e-308,-1e308,1e308)):
            exact=D.from_float(c)*(D.from_float(b)-D.from_float(a))
            evaluate('one_panel_trapezoid',lab.trapezoid,lambda x:c,a,b,1,exact)
    collapsed=bad_values=range_errors=0
    for name,method in methods:
        for a,b in ((0.0,tiny),(1e308,math.nextafter(1e308,math.inf))):
            calls=[]
            def should_not_run(x):calls.append(x);return 1.0
            rejects(ValueError,method,should_not_run,a,b,2)
            assert calls==[];collapsed+=1
        for value,error in ((math.nan,ValueError),(math.inf,ValueError),(True,TypeError)):
            rejects(error,method,lambda x:value,0.0,1.0,2);bad_values+=1
        for c,a,b in ((1e308,0.0,2.0),(tiny,0.0,0.25)):
            rejects(ValueError,method,lambda x:c,a,b,2);range_errors+=1
    with patch.object(lab,'simpson',wraps=lab.simpson) as shared:
        assert final.simpson(lambda x:1.0,0.0,1.0,2)==1.0
        shared.assert_called_once()
    return {'complete_rule_references':records,'pre_callback_collapsed_grids':collapsed,
            'invalid_callback_values':bad_values,'unrepresentable_final_results':range_errors,
            'observed_final_shared_call':1,
            'scope':'represented nominal uniform grid and finite callback samples; no general quadrature error certificate'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
