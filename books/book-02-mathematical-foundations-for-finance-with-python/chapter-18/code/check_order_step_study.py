"""Exact signed quadrature errors and three-step polynomial/bond studies."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
import math
import section_18_07 as lab


def quadrature(trapezoid,simpson):
    rows=[];orders=[]
    for method,degree,power in ((trapezoid,2,2),(simpson,4,4)):
        for coefficient in (F(1),F(-2)):
            for a,b in ((F(0),F(1)),(F(-1),F(1)),(F(1),F(3))):
                integral=coefficient*(b**(degree+1)-a**(degree+1))/(degree+1)+(b*b-a*a)/4
                values=[];errors=[]
                def f(x):return float(coefficient*F(x)**degree+F(x)/2)
                for n in (2,4,8,16):
                    width=b-a;h=width/n
                    error=coefficient*width*h*h/6 if degree==2 else coefficient*2*width*h**4/15
                    actual=method(f,float(a),float(b),n)
                    # This includes final float rounding of the exact rule.
                    assert actual==float(integral+error),(degree,a,b,n,actual,float(integral+error))
                    observed=F(actual)-integral
                    assert observed*error>0
                    assert abs(observed-error)<=F(math.ulp(actual))
                    values.append(actual);errors.append(observed)
                ratios=[float(errors[i]/errors[i+1]) for i in range(3)]
                measured=[math.log2(ratio) for ratio in ratios]
                assert all(abs(order-power)<1e-8 for order in measured)
                orders.extend(measured)
                rows.append({'degree':degree,'coefficient':str(coefficient),'interval':[str(a),str(b)],
                             'exact_integral':str(integral),'panels':[2,4,8,16],
                             'rule_values':values,'signed_errors':list(map(str,errors)),
                             'error_ratios':ratios,'measured_orders':measured})
    return rows,orders


def polynomial_differences(forward):
    x=F(1,2);rows=[]
    for h in (F(1,8),F(1,16),F(1,32)):
        f=lambda t:t*t*t+t
        g=lambda t:t**4
        values=(forward(f,float(x),float(h)),lab.central_difference(f,float(x),float(h)),
                lab.second_difference(g,float(x),float(h)))
        expected=(3*x*x+1+3*x*h+h*h,3*x*x+1+h*h,12*x*x+2*h*h)
        assert values==tuple(map(float,expected))
        rows.append({'step':str(h),'values':values,
                     'signed_errors':list(map(str,(3*x*h+h*h,h*h,2*h*h)))})
    return rows


def financial_steps():
    rows=[];r=0.05
    with localcontext() as ctx:
        ctx.prec=100
        dr=D.from_float(r)
        true_first=-D(2000)/(1+dr)**3;true_second=D(6000)/(1+dr)**4
        for h in (2e-4,1e-4,5e-5):
            dh=D.from_float(h);points=(r+h,r,r-h)
            ideal=[D(1000)/(1+D.from_float(q))**2 for q in points]
            prices=[lab.zero_price(q) for q in points]
            price_errors=[abs(D.from_float(v)-ref) for v,ref in zip(prices,ideal)]
            expected=((ideal[0]-ideal[1])/dh,(ideal[0]-ideal[2])/(2*dh),
                      (ideal[0]-2*ideal[1]+ideal[2])/dh**2)
            actual=(lab.forward_difference(lab.zero_price,r,h),lab.central_difference(lab.zero_price,r,h),
                    lab.second_difference(lab.zero_price,r,h))
            propagated=((price_errors[0]+price_errors[1])/dh,
                        (price_errors[0]+price_errors[2])/(2*dh),
                        (price_errors[0]+2*price_errors[1]+price_errors[2])/dh**2)
            # Selected finite-rounding allowance, retained explicitly rather
            # than presenting ideal-stencil truncation as all observed error.
            unit=D.from_float(math.ulp(max(prices)))
            budgets=tuple(p+8*unit/den for p,den in zip(propagated,(dh,2*dh,dh**2)))
            for value,reference,budget in zip(actual,expected,budgets):
                assert abs(D.from_float(value)-reference)<=budget
            rows.append({'rate':r,'step':h,'represented_queries':points,'prices':prices,
                         'decimal_stencils':list(map(str,expected)),'actual_stencils':actual,
                         'selected_rounding_budgets':list(map(str,budgets)),
                         'signed_analytic_errors':list(map(str,(D.from_float(actual[0])-true_first,
                                                               D.from_float(actual[1])-true_first,
                                                               D.from_float(actual[2])-true_second))),
                         'numerical_duration':-actual[1]/prices[1],
                         'numerical_convexity':actual[2]/prices[1]})
    return rows


def check():
    rows,orders=quadrature(lab.trapezoid,lab.simpson)
    differences=polynomial_differences(lab.forward_difference)
    financial=financial_steps()
    detected=[]
    for name,trap,simp in (('zero_trapezoid',lambda *args:0.0,lab.simpson),
                           ('trapezoid_as_simpson',lab.trapezoid,lab.trapezoid)):
        try:quadrature(trap,simp)
        except AssertionError:detected.append(name)
        else:raise AssertionError('undetected quadrature variant '+name)
    try:polynomial_differences(lambda *args:-lab.forward_difference(*args))
    except AssertionError:detected.append('reversed_forward_sign')
    else:raise AssertionError('undetected difference variant')
    return {'quadrature_reference_sets':rows,'rounded_rule_references':48,
            'measured_order_checks':len(orders),'polynomial_three_step_study':differences,
            'bond_three_step_study':financial,'wrong_methods_detected':detected,
            'scope':'selected smooth polynomial/zero-coupon cases; no universal asymptotic or optimal-step guarantee'}


if __name__=='__main__':
    print(json.dumps(check(),indent=2,allow_nan=False))
