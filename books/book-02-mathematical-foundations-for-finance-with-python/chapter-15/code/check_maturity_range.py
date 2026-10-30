"""Independent Decimal references for adjusted-maturity intermediate range."""
from decimal import Decimal as D, localcontext
import math
from section_15_08 import exact_unchanged_value_time as adjusted

def run():
    cases=((1e308,2.0,0.0),(-1e308,2.0,0.0),
           (1e-300,1e-100,0.0),(1e-300,1e-100,1e-300),
           (0.125,2.0,0.125),(-0.125,2.0,-0.0625),
           (math.ulp(0.0),1.0,0.0),(0.125,0.0,-0.25))
    with localcontext() as ctx:
        ctx.prec=100
        for rate,years,shock in cases:
            new_rate=rate+shock
            exact=D.from_float(rate)*D.from_float(years)/D.from_float(new_rate)
            expected=float(exact)
            actual=adjusted(rate,years,shock)
            assert actual==expected,(rate,years,shock,actual,expected)
            if years>0:
                assert actual>0
                # Compare exponents directly: extreme exponentials need not be representable.
                old_exponent=D.from_float(rate)*D.from_float(years)
                new_exponent=D.from_float(new_rate)*D.from_float(actual)
                assert abs(new_exponent-old_exponent)<=abs(old_exponent)*D("2e-16")
    rejected=(
        ((1e308,1.0,1e308),"shocked rate"),
        ((1.0,1e308,math.nextafter(-1.0,0.0)),"range"),
        ((math.ulp(0.0),math.ulp(0.0),1.0),"underflow"),
        ((0.125,2.0,-0.125),"zero rate"),
        ((0.125,2.0,-0.25),"nonnegative"),
    )
    for args,message in rejected:
        try:
            adjusted(*args)
        except ValueError as exc:
            assert message in str(exc),(args,str(exc))
        else:
            raise AssertionError("unrepresentable/domain result accepted")
    print("PASS: eight Decimal adjusted-maturity references and five range/domain rejections")

if __name__=="__main__":
    run()
