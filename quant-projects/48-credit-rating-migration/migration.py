"""Synthetic rating-migration Markov chain; educational, not calibrated."""
import math

STATES = ('A', 'B', 'C', 'D')  # D is absorbing default
BASE = ((.88, .09, .02, .01), (.04, .84, .09, .03),
        (.01, .07, .80, .12), (0., 0., 0., 1.))
STRESS = ((.78, .14, .05, .03), (.02, .72, .17, .09),
          (.005, .035, .69, .27), (0., 0., 0., 1.))

def validate(matrix):
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise ValueError('expected 4x4 transition matrix')
    for row in matrix:
        if any(isinstance(x, bool) or not isinstance(x, (int, float))
               or not math.isfinite(x) or x < 0 or x > 1 for x in row):
            raise ValueError('probabilities must be finite numbers in [0,1]')
        if not math.isclose(sum(row), 1., rel_tol=0., abs_tol=1e-10):
            raise ValueError('each row must sum to one')
    if any(not math.isclose(matrix[3][j], float(j == 3), abs_tol=1e-12)
           for j in range(4)):
        raise ValueError('default state must be absorbing')

def distribution(start='B', years=3, matrix=BASE):
    validate(matrix)
    if start not in STATES:
        raise ValueError('unknown initial rating')
    if isinstance(years, bool) or not isinstance(years, int) or not 0 <= years <= 50:
        raise ValueError('years must be an integer in [0,50]')
    probs = [float(i == STATES.index(start)) for i in range(4)]
    for _ in range(years):
        probs = [sum(probs[i] * matrix[i][j] for i in range(4)) for j in range(4)]
    return dict(zip(STATES, probs))

def expected_loss(start='B', years=3, lgd=.6, matrix=BASE):
    if isinstance(lgd, bool) or not isinstance(lgd, (int, float)) or not math.isfinite(lgd) or not 0 <= lgd <= 1:
        raise ValueError('LGD must be finite in [0,1]')
    return distribution(start, years, matrix)['D'] * lgd

if __name__ == '__main__':
    for name, matrix in [('baseline', BASE), ('stress', STRESS)]:
        p = distribution('B', 3, matrix)
        print(f'{name}: three-year default probability={p["D"]:.4%}; expected loss/notional={expected_loss("B", 3, .6, matrix):.4%}')
