"""Exact assessment inputs across existing APIs; supplemental references kept separate."""
import math,json
from decimal import Decimal,localcontext
from fractions import Fraction
import section_8_10 as lab
import section_8_06 as higher
import section_8_08 as difference
import section_8_09 as comparator

def observations():
    source=[];supplement=[]
    def check(name,actual,expected,rtol=1e-10):
        ok=math.isclose(actual,expected,rel_tol=rtol,abs_tol=1e-10)
        source.append(dict(name=name,actual=actual,expected=expected,passed=ok))
    def exact(name,actual,expected):source.append(dict(name=name,actual=actual,expected=expected,passed=actual==expected))
    def supp(name,actual,expected,tol=0):supplement.append(dict(name=name,actual=actual,expected=expected,passed=abs(actual-expected)<=tol,scope='Independent supplemental arithmetic;not a missing lab API implementation'))
    exact('P1 x² derivative coefficients',higher.derivative_coefficients([0,0,1]),(0.,2.))
    exact('P2 exact assessment polynomial derivative',higher.derivative_coefficients([-9,7,0,-3,0,4]),(7.,0.,-9.,0.,20.))
    check('P8 stationary slope',lab.marginal_profit(125),0)
    check('P8 maximal profit',lab.profit(125),2525)
    exact('P8 endpoint comparison',[lab.profit(125)>lab.profit(0),lab.profit(125)>lab.profit(200)],[True,True])
    with localcontext() as c:
        c.prec=100;P=Decimal(10000)*Decimal('-.2').exp();first=-5*P;second=25*P;H=Decimal('.001')
        check('P10 PV',lab.present_value(10000,.04,5),float(P))
        actual=lab.pv_rate_derivatives(10000,.04,5)
        check('P10 first',actual[1],float(first));check('P10 second',actual[2],float(second))
        shock=lab.pv_rate_shock(10000,.04,5,.001)
        for name,expected in [('first_order',first*H),('second_order',first*H+second*H*H/2),('exact',P*((-5*H).exp()-1))]:check('P11 '+name,shock[name],float(expected))
        exact('P11 improvement',abs(shock['second_order']-shock['exact'])<abs(shock['first_order']-shock['exact']),True)
        check('P12 log',lab.log_return(80,84),float((Decimal(21)/20).ln()))
        supp('P9 accumulation first at3',float(150*Decimal('.18').exp()),179.5826,.00005)
        supp('P9 accumulation second coefficient',2500*.06*.06,9.,1e-14)
    supp('P12 simple return',float(Fraction(4,80)),.05)
    supp('P13 demand elasticity',float(Fraction(-600,400)),-1.5)
    check('P14 quantity',lab.break_even_quantity(45,15,900),30)
    check('P14 derivative',lab.break_even_derivative(45,15,900),-1)
    check('P15 yield',lab.bond_yield_from_price(110,100),.1)
    check('P15 inverse',lab.bond_yield_price_derivative(110,100),-.011)
    supp('P15 direct price derivative',float(Fraction(-1000,11)),-90.9090909090909,1e-12)
    exact('P16 second coefficients',higher.derivative_coefficients([4,0,-6,1],2),(-12.,6.))
    exact('P16 sign change',[higher.polynomial([-12,6],1)<0,higher.polynomial([-12,6],3)>0],[True,True])
    check('P16 inflection ordinate',higher.polynomial([4,0,-6,1],2),-12)
    exact('P17 second coefficients',higher.derivative_coefficients([0,0,0,0,1],2),(0.,0.,12.))
    exact('P17 selected nonnegative curvature',[higher.polynomial([0,0,12],x) for x in [-1,0,1]],[12.,0.,12.])
    f=lambda x:x**3
    check('P18 forward earlier exact-source API',difference.forward_difference(f,2,.1),12.61)
    check('P18 backward earlier exact-source API',difference.backward_difference(f,2,.1),11.41)
    check('P18 centered assessment API',lab.centered_first(f,2,.1),12.01)
    check('P19 second assessment API',lab.centered_second(lambda x:x*x,2,.1),2)
    check('P20 Richardson exact cubic API',difference.richardson_first(f,2,.1),12)
    exact('P21 source kink stencils',[difference.backward_difference(abs,0,.125),difference.forward_difference(abs,0,.125),difference.centered_difference(abs,0,.125)],[-1.,1.,0.])
    supp('P22 forward epsilon root',math.sqrt(2.**-52),2.**-26)
    supp('P22 second epsilon root',(2.**-52)**.25,2.**-13)
    for rate in [-.01,0.,.04,.1]:
        with localcontext() as c:
            c.prec=100;R=Decimal.from_float(rate)
            refs=[sum(Decimal(c)*(-Decimal(t)*R).exp() for c,t in [(100,1),(200,2),(300,3)]),sum(-Decimal(c*t)*(-Decimal(t)*R).exp() for c,t in [(100,1),(200,2),(300,3)]),sum(Decimal(c*t*t)*(-Decimal(t)*R).exp() for c,t in [(100,1),(200,2),(300,3)])]
        actual=higher.cash_flow_rate_derivatives([(100,1),(200,2),(300,3)],rate)
        for j in range(3):check(f'P23 exact schedule r{rate} field{j}',actual[j],float(refs[j]))
        exact(f'P23 selected sensitivity signs r{rate}',[actual[1]<0,actual[2]>0],[True,True])
    supp('P24 one basis point',float(Fraction(1,10000)),.0001)
    reports=comparator.step_ladder(f,lambda x:3*x*x,2,[1e-2,1e-3,1e-4],abs_tol=1e-5,rel_tol=1e-5)
    exact('P25 three step order',[x['step'] for x in reports],[1e-2,1e-3,1e-4])
    exact('P25 centered acceptance',[x['first_derivatives']['centered']['pass'] for x in reports],[True]*3)
    exact('P25 forward disagreement',[x['first_derivatives']['forward']['pass'] for x in reports],[False]*3)
    wrong=comparator.step_ladder(f,lambda x:0,2,[1e-2,1e-3,1e-4],abs_tol=1e-5,rel_tol=1e-5)
    exact('P25 wrong reference rejected',[x['first_derivatives']['centered']['pass'] for x in wrong],[False]*3)
    return source,supplement
if __name__=='__main__':
    source,supplement=observations();print(json.dumps(dict(source_predicates=source,supplemental_predicates=supplement),indent=2));assert all(x['passed'] for x in source+supplement);print(len(source),'source predicates;',len(supplement),'supplemental predicates passed')
