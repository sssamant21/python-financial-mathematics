"""Supplemental exercise caller using the unchanged source API."""
import numpy as np
from numpy_motivation import price_returns

def main():
    ids = ('ASSET-A', 'ASSET-B', 'ASSET-C', 'ASSET-D')
    start = np.array([100., 80., 50., 40.], dtype=np.float64)
    end = np.array([105., 76., 50., 44.], dtype=np.float64)
    result = price_returns(start, end)
    for sid, value in zip(ids, result):
        print(f'{sid}: {value:.2%}')
    print('Shape:', result.shape)
    print('Dtype:', result.dtype)

if __name__ == '__main__':
    main()
