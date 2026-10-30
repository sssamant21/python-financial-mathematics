"""Supplemental exercise caller; original snapshot implementation unchanged."""
import numpy as np
from array_contracts import price_snapshot

def main():
    dates = ('2026-01-05', '2026-01-06', '2026-01-07')
    ids = ('ASSET-A', 'ASSET-B', 'ASSET-C')
    prices = np.array([[100.,80.,50.], [105.,76.,50.], [103.,78.,52.]])
    result = price_snapshot(prices, dates, ids)
    print('Axes: date, instrument')
    print('Shape:', result.shape)
    print('Dimensions:', result.ndim)
    print('Elements:', result.size)
    print('Dtype:', result.dtype)
    print('Bytes per element:', result.itemsize)
    print('Element bytes:', result.nbytes)
    print('Stored rows:', result.tolist())

if __name__ == '__main__':
    main()
