"""Exact selected basis-span reconstructions for Section 13.2."""
from fractions import Fraction as F
from itertools import permutations
import math
from section_13_02 import pivot_basis, achieved

def coordinates(first, second, target):
    determinant = first[0]*second[1]-second[0]*first[1]
    assert determinant != 0
    return ((target[0]*second[1]-second[0]*target[1])/determinant,
            (first[0]*target[1]-target[0]*first[1])/determinant)

def run():
    factors = ("RATE", "CREDIT")
    raw = {"A": (F(2),F(1)), "B": (F(1),F(-1)), "C": (F(4),F(2))}
    cases = 0
    for order in permutations(raw):
        for scale in (F(1), F(2**40), F(1,2**40)):
            columns = {name: tuple(scale*x for x in raw[name]) for name in order}
            rows = tuple(tuple(float(columns[name][i]) for name in order) for i in range(2))
            result = pivot_basis(rows, factors, order)
            assert result["rank"] == result["dimension"] == 2
            basis = result["basis_instruments"]
            redundant = result["redundant_instruments"]
            assert len(basis) == 2 and len(redundant) == 1
            assert set(basis).isdisjoint(redundant)
            assert set(basis+redundant) == set(order)
            first, second = (columns[name] for name in basis)
            # Reconstruct every original column, including omitted columns,
            # from the actual selected basis using exact Cramer's rule.
            for target in columns.values():
                x,y = coordinates(first,second,target)
                assert tuple(x*first[i]+y*second[i] for i in range(2)) == target
                holdings = dict.fromkeys(order,0.0)
                holdings.update({basis[0]:float(x),basis[1]:float(y)})
                actual = achieved(rows,factors,order,holdings)
                for label, expected in zip(factors,target):
                    assert math.isclose(actual[label],float(expected),rel_tol=1e-12,abs_tol=0)
            # Independent attainable exposure, not restricted to an original column.
            target = (5*scale,scale)
            x,y = coordinates(first,second,target)
            holdings = dict.fromkeys(order,0.0)
            holdings.update({basis[0]:float(x),basis[1]:float(y)})
            actual = achieved(rows,factors,order,holdings)
            for label,expected in zip(factors,target):
                assert math.isclose(actual[label],float(expected),rel_tol=1e-12,abs_tol=0)
            cases += 1
    assert cases == 18
    print("PASS: Section 13.2 eighteen selected exact basis-span reconstructions")

if __name__ == "__main__":
    run()
