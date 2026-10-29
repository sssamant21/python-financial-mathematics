"""Exact selected null-basis identities for Section 13.3."""
from fractions import Fraction as F
from itertools import permutations
from section_13_03 import analyze, achieved

def run():
    cases = (
        (((1,2,4),(2,4,8)), 1),
        (((2,1,4),(1,-1,2)), 2),
        (((0,0,0),(0,0,0)), 0),
        (((1,0,0),(0,1,0),(0,0,1)), 3),
    )
    count = 0
    for original, expected_rank in cases:
        factors = tuple("F"+str(i) for i in range(len(original)))
        for order in permutations(range(3)):
            names = tuple("ABC"[j] for j in order)
            for scale in (1, 2**20, 2.0**-20):
                rows = tuple(tuple(row[j]*scale for j in order) for row in original)
                result = analyze(rows,factors,names)
                assert result["rank"] == expected_rank
                assert result["nullity"] == 3-expected_rank
                basis = result["null_space_basis"]
                assert len(basis) == result["nullity"]
                pivots = result["column_space_basis_instruments"]
                free = [name for name in names if name not in pivots]
                # Independent exact Az=0 for the actual returned float values.
                for k, vector in enumerate(basis):
                    assert set(vector) == set(names)
                    for row in rows:
                        assert sum((F(value)*F(vector[name]) for value,name in zip(row,names)),F(0)) == 0
                    # Free-coordinate identity minor proves independence of this basis.
                    assert [vector[name] for name in free] == [float(i==k) for i in range(len(free))]
                initial = dict(zip(names,(2.0,-1.0,0.5)))
                shifted = {name: initial[name]+sum((k+1)*v[name] for k,v in enumerate(basis))
                           for name in names}
                assert achieved(rows,factors,names,initial) == achieved(rows,factors,names,shifted)
                count += 1
    assert count == 72
    print("PASS: Section 13.3 seventy-two selected exact null-basis cases")

if __name__ == "__main__":
    run()
